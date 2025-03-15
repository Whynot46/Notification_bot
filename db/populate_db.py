import aiosqlite
import asyncio


DB_PATH = "./db/database.db"


async def populate_database():
    async with aiosqlite.connect(DB_PATH) as db:
        # Вставляем данные в таблицу roles
        await db.execute('''
            INSERT INTO roles (name)
            VALUES (?)
        ''', ("Администратор",))

        await db.execute('''
            INSERT INTO roles (name)
            VALUES (?)
        ''', ("Пользователь",))
        
        # Вставляем данные в таблицу groups
        await db.execute('''
            INSERT INTO groups (group_id, name)
            VALUES (?, ?)
        ''', (4739497131, "Test group"))

        # Вставляем данные в таблицу users
        await db.execute('''
            INSERT INTO users (user_id, firstname, middlename, lastname, role_id, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (7348838870, "Алексей", "Дмитриевич", "Пахалев", 1, True))

        await db.commit()


if __name__ == '__main__':
    asyncio.run(populate_database())