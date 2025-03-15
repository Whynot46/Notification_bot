import aiosqlite
import asyncio


DB_PATH = "./db/database.db"


async def create_table():
    async with aiosqlite.connect(DB_PATH) as db:        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')
        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER NOT NULL,
                name TEXT NOT NULL
            )
        ''')
        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                firstname TEXT NOT NULL,
                middlename TEXT,
                lastname TEXT NOT NULL,
                role_id INTEGER DEFAULT 2,
                is_active INTEGER DEFAULT 1,
                FOREIGN KEY (role_id) REFERENCES roles(id)
            )
        ''')
        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                author_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                create_datetime TEXT NOT NULL,
                sender_date TEXT,
                sender_time TEXT NOT NULL,
                is_repeat BOOLEAN NOT NULL,
                sender_weekday TEXT,
                recipients_ids TEXT,
                FOREIGN KEY (author_id) REFERENCES users(id)
            )
        ''')

        await db.commit()


async def main():
    await create_table()


if __name__ == '__main__':
    asyncio.run(main())