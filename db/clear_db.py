import aiosqlite
import asyncio


DB_PATH = "./db/database.db"


async def clear_database():
    async with aiosqlite.connect(DB_PATH) as db:
        tables = [
            "users",
            "groups",
            "roles",
            "notification",
        ]

        for table in tables:
            await db.execute(f"DELETE FROM {table};")

        await db.commit()


if __name__ == '__main__':
    asyncio.run(clear_database())