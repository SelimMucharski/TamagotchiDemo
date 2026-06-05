import asyncio
from supabase import create_async_client
import utils

FAMILY_ID = "acc4e8ca-ab29-4342-83e0-fd82736455ce"


class DatabaseManager:
    def __init__(self, url, key):
        self.url = url
        self.key = key
        self.client = None
        self.channel = None
        self.event_queue = asyncio.Queue()

    async def load_info(self):
        pet = (
            await self.table("pets")
            .select("name,energy")
            .eq("family_id", FAMILY_ID)
            .single()
            .execute()
        )

        utils.PET_NAME = pet.data['name']
        utils.HEALTH_LEVEL = int(pet.data['energy']) / 100 * utils.MAX_HEALTH

    async def start(self):
        self.client = await create_async_client(self.url, self.key)
        self.channel = self.client.channel("tasks-realtime")

        self.channel.on_postgres_changes(
            event="UPDATE",
            schema="public",
            table="tasks",
            callback=self._on_task_done
        )
        await self.channel.subscribe()
        await self.load_info()
        print("System zadań aktywny.")

    async def update_pet_energy(self):
        energy_percent = int(
            utils.HEALTH_LEVEL / utils.MAX_HEALTH * 100
        )

        await (
            self.table("pets")
            .update({"energy": energy_percent})
            .eq("family_id", FAMILY_ID)
            .execute()
        )

    def _on_task_done(self, payload):
        new_task = payload['data']['record']

        if new_task['family_id'] == FAMILY_ID and new_task['status'] == 'done':
            self.event_queue.put_nowait(new_task)

    def table(self, table_name: str):
        return self.client.table(table_name)


def run_db_loop(db_manager):
    loop = asyncio.new_event_loop()
    db_manager.loop = loop
    asyncio.set_event_loop(loop)
    loop.run_until_complete(db_manager.start())
    loop.run_forever()
