from app import App
import asyncio


async def main():
    app = App()

    await app.init()

    await app.run()

if __name__ == "__main__":
    asyncio.run(main())
