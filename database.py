import asyncio
from supabase import create_async_client

FAMILY_ID = "acc4e8ca-ab29-4342-83e0-fd82736455ce"


class DatabaseManager:
    def __init__(self, url, key):
        self.url = url
        self.key = key
        self.client = None
        self.channel = None
        self.event_queue = asyncio.Queue()

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
        print("System zadań aktywny.")

    def _on_task_done(self, payload):
        new_task = payload['data']['record']

        if new_task['family_id'] == FAMILY_ID and new_task['status'] == 'done':
            self.event_queue.put_nowait(new_task)


def run_db_loop(db_manager):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(db_manager.start())
    loop.run_forever()
