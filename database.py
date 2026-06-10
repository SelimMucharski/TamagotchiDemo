import asyncio
from supabase import create_async_client

FAMILY_ID = "69302c27-65fa-4cb9-8f76-59fc0c0ff797"


class DatabaseManager:
    def __init__(self, url, key):
        self.url = url
        self.key = key
        self.client = None
        self.channel = None

        self.event_queue = asyncio.Queue()

        self.tasks_cache = {}
        self.pet_cache = None

    async def start(self):
        self.client = await create_async_client(self.url, self.key)
        self.channel = self.client.channel("family-realtime")

        self.channel.on_postgres_changes(
            event="*",
            schema="public",
            table="tasks",
            callback=self._on_task_change
        )

        await self.channel.subscribe()

        await self.load_tasks_cache()
        await self.load_pet_cache()

        self.event_queue.put_nowait({"type": "ready"})
        print("Connected to Database")

    async def load_pet_cache(self):
        result = (
            await self.table("pets")
            .select("id, name, energy, mood, family_id")
            .eq("family_id", FAMILY_ID)
            .single()
            .execute()
        )

        self.pet_cache = result.data

    async def update_pet(self, energy: int, mood: str):
        await (
            self.table("pets")
            .update({"mood": mood, "energy": energy})
            .eq("family_id", FAMILY_ID)
            .execute()
        )

    async def add_points_to_user(self, user_id: str, points_to_add: int):
        response = await (
            self.table("users")
            .select("points")
            .eq("id", user_id)
            .single()
            .execute()
        )

        current_points = response.data["points"] or 0
        print(current_points)
        new_points = current_points + points_to_add

        await (
            self.table("users")
            .update({"points": new_points})
            .eq("id", user_id)
            .execute()
        )

    def _on_pet_change(self, payload):
        pet = payload["data"].get("record") or payload["data"].get("new")

        if not pet or pet["family_id"] != FAMILY_ID:
            return

        self.pet_cache = pet

        self.event_queue.put_nowait({
            "type": "pet_update",
            "data": pet
        })

    async def load_tasks_cache(self):
        result = (
            await self.table("tasks")
            .select("id, status, family_id, assigned_to_user_id")
            .eq("family_id", FAMILY_ID)
            .in_("status", ["todo", "done", "expired"])
            .execute()
        )

        print(result.data)

        self.tasks_cache = {
            task["id"]: {
                "id": task["id"],
                "status": task["status"],
                "assigned_to_user_id": task["assigned_to_user_id"]
            }
            for task in result.data
        }

    def _on_task_change(self, payload):
        event_type = payload.get("eventType")
        data = payload.get("data", {})

        task = data.get("record") or data.get("new") or data.get("old")

        if not task or task.get("family_id") != FAMILY_ID:
            return

        task_id = task["id"]
        status = task.get("status")

        if event_type == "DELETE":
            self.tasks_cache.pop(task_id, None)
            return

        if status not in ("todo", "done", "expired"):
            import utils
            if task_id in self.tasks_cache:
                utils.ITEM_BIAS -= 1
            
            self.tasks_cache.pop(task_id, None)
            return

        userID = task["assigned_to_user_id"]

        self.tasks_cache[task_id] = {
            "id": task_id,
            "status": status,
            "assigned_to_user_id": userID
        }

        if status == "done":
            self.event_queue.put_nowait({
                "type": "task_done",
                "data": self.tasks_cache[task_id]
            })

    def get_tasks_cached(self):
        return list(self.tasks_cache.values())

    def get_pet_cached(self):
        return self.pet_cache

    def table(self, table_name: str):
        return self.client.table(table_name)


def run_db_loop(db_manager):
    loop = asyncio.new_event_loop()
    db_manager.loop = loop
    asyncio.set_event_loop(loop)
    loop.run_until_complete(db_manager.start())
    loop.run_forever()
