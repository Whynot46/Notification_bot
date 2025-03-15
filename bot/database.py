import aiosqlite
from bot.config import Config
from datetime import datetime


db_connection = None


# Инициализация соединения с базой данных
async def init_db():
    global db_connection
    db_connection = await aiosqlite.connect(Config.DB_URL)


# Закрытие соединения с базой данных
async def close_db():
    global db_connection
    if db_connection:
        await db_connection.close()


# Получить ФИО пользователя по user_id
async def get_fullname(user_id : int) -> str:
    global db_connection
    cursor = await db_connection.execute("SELECT firstname, middlename, lastname FROM users WHERE user_id = ?", (user_id,))
    result = await cursor.fetchone()
    if result:
        return f"{result[2]} {result[0]} {result[1]}"
    else:
        return None


# Проверка, зарегистрирован ли пользователь по user_id
async def is_old(user_id):
    global db_connection
    cursor = await db_connection.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
    result = await cursor.fetchone()
    return bool(result)


#Проверка, зарегистрирован ли пользователь по ФИО
async def is_register(firstname: str, middlename: str, lastname: str):
    global db_connection
    cursor = await db_connection.execute("SELECT 1 FROM users WHERE firstname = ? AND middlename= ? AND lastname= ?", (firstname, middlename, lastname))
    result = await cursor.fetchone()
    return bool(result)


# Проверка, активен ли пользователь
async def is_active(user_id : int):
    global db_connection
    cursor = await db_connection.execute("SELECT 1 FROM users WHERE user_id = ? AND is_active = 1", (user_id,))
    result = await cursor.fetchone()
    return bool(result)


# Получить id всех пользователей   
async def get_all_user_id() -> list:
    global db_connection
    cursor = await db_connection.execute("SELECT user_id FROM users")
    rows = await cursor.fetchall()
    return [row[0] for row in rows]


async def get_all_users_dict() -> dict:
    global db_connection
    cursor = await db_connection.execute("SELECT user_id, firstname, middlename, lastname FROM users")
    rows = await cursor.fetchall()
    
    users_dict = {}
    for row in rows:
        user_id, firstname, middlename, lastname = row
        users_dict[user_id] = {
            "firstname": firstname,
            "middlename": middlename,
            "lastname": lastname
        }
    
    return users_dict


async def get_all_groups() -> dict:
    global db_connection
    cursor = await db_connection.execute("SELECT group_id, name FROM groups")
    rows = await cursor.fetchall()
    groups_dict = {}
    for row in rows:
        group_id, name = row
        groups_dict[group_id] = {
            "name": name,
        }
        
    return groups_dict


async def add_notification(author_id: int, title: str, description: str, sender_date: str, sender_time: str, is_repeat: bool, sender_weekday: str, recipients_ids: str):
    global db_connection
    cursor = await db_connection.execute('''INSERT INTO notifications (author_id, title, description, create_datetime, sender_date, sender_time, is_repeat, sender_weekday, recipients_ids) 
                                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                                         ''', (author_id, title, description, str(datetime.now()), sender_date, sender_time, is_repeat, str(sender_weekday), str(recipients_ids))
                                        )
    await db_connection.commit() 
    
    
async def get_all_notifications() -> dict:
    global db_connection
    cursor = await db_connection.execute("SELECT * FROM notifications")
    rows = await cursor.fetchall()
    notifications_dict = {}
    for row in rows:
        notification_id, author_id, title, description, create_datetime, sender_date, sender_time, is_repeat, sender_weekday, recipients_ids = row
        notifications_dict[notification_id] = {
            "author_id": author_id,
            "title": title,
            "description": description,
            "create_datetime": create_datetime,
            "sender_date": sender_date,
            "sender_time": sender_time,
            "is_repeat": is_repeat,
            "sender_weekday": sender_weekday,
            "recipients_ids": recipients_ids
            }
    
    return notifications_dict


async def get_author_notifications(author_id: int) -> dict:
    global db_connection
    cursor = await db_connection.execute("SELECT * FROM notifications WHERE author_id = ?", (author_id,))  # Добавлена запятая
    rows = await cursor.fetchall()
    notifications_dict = {}
    for row in rows:
        notification_id, author_id, title, description, create_datetime, sender_date, sender_time, is_repeat, sender_weekday, recipients_ids = row
        notifications_dict[notification_id] = {
            "author_id": author_id,
            "title": title,
            "description": description,
            "create_datetime": create_datetime,
            "sender_date": sender_date,
            "sender_time": sender_time,
            "is_repeat": is_repeat,
            "sender_weekday": sender_weekday,
            "recipients_ids": recipients_ids
        }
    return notifications_dict


async def get_user_notifications(user_id: int) -> dict:
    global db_connection
    cursor = await db_connection.execute("SELECT * FROM notifications WHERE recipients_ids LIKE ?", f"%{user_id}%")
    rows = await cursor.fetchall()
    notifications_dict = {}
    for row in rows:
        notification_id, author_id, title, description, create_datetime, sender_date, sender_time, is_repeat, sender_weekday, recipients_ids = row
        notifications_dict[notification_id] = {
            "author_id": author_id,
            "title": title,
            "description": description,
            "create_datetime": create_datetime,
            "sender_date": sender_date,
            "sender_time": sender_time,
            "is_repeat": is_repeat,
            "sender_weekday": sender_weekday,
            "recipients_ids": recipients_ids
            }
    
    return notifications_dict


async def delete_notification(notification_id: int):
    global db_connection
    await db_connection.execute("DELETE FROM notifications WHERE id = ?", (notification_id,))
    await db_connection.commit()


async def edit_notification(notification_id: int, title: str, description: str, sender_date: str, sender_time: str, is_repeat: bool, sender_weekday: str, recipients_ids: str):
    global db_connection
    await db_connection.execute("UPDATE notifications SET title = ?, description = ?, sender_date = ?, sender_time = ?, is_repeat = ?, sender_weekday = ?, recipients_ids = ? WHERE id= ?",
                                (title, description, sender_date, sender_time, is_repeat, sender_weekday, recipients_ids, notification_id))
    await db_connection.commit()


async def delete_user(user_id: int):
    global db_connection
    await db_connection.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    await db_connection.commit()