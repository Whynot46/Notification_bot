from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
import bot.database as db
from bot.config import Config
from datetime import datetime, timedelta


async def get_main_menu_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    if Config.is_admin(user_id):
        reply_keyboard = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='🏠Напоминания Роутима'), KeyboardButton(text='🧑🏻‍💻Мои напоминания')],
            [KeyboardButton(text='🔔Создать напоминание')],
            [KeyboardButton(text='👥Пользователи и группы')],
        ], resize_keyboard=True)
    else:
        reply_keyboard = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='🧑🏻‍💻Мои напоминания')],
            [KeyboardButton(text='🔔Создать напоминание')],
        ], resize_keyboard=True)
    
    return reply_keyboard


async def get_notification_users_list_keyboard(selected_users=None) -> InlineKeyboardMarkup:
    if selected_users is None:
        selected_users = []

    users_dict = await db.get_all_users_dict()
    users_keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for user_id, user_data in users_dict.items():
        button_text = f"{user_data['lastname']} {user_data['firstname']}"
        if user_id in selected_users:
            button_text += " ✅"
        users_keyboard.inline_keyboard.append([InlineKeyboardButton(text=button_text, callback_data=f"notification_user_{user_id}")])

    return users_keyboard


async def get_notification_groups_list_keyboard(selected_groups=None) -> InlineKeyboardMarkup:
    if selected_groups is None:
        selected_groups = []

    groups_dict = await db.get_all_groups()
    groups_keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for group_id, group_info in groups_dict.items():
        button_text = f"{group_info['name']}"
        if group_id in selected_groups:
            button_text += " ✅"
        groups_keyboard.inline_keyboard.append([InlineKeyboardButton(text=button_text, callback_data=f"notification_group_{group_id}")])
    
    return groups_keyboard


async def get_groups_list_keyboard() -> InlineKeyboardMarkup:
    groups_dict = await db.get_all_groups()
    groups_keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for group_id, group_info in groups_dict.items():
        groups_keyboard.inline_keyboard.append([InlineKeyboardButton(text=group_info['name'], callback_data=f"group_{group_id}")])
    return groups_keyboard


async def get_edit_notification_keyboard(notification_id: int) -> InlineKeyboardMarkup:
    edit_notification_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='✏️ Редактировать', callback_data=f'edit_notification_{notification_id}')],
            [InlineKeyboardButton(text='🗑️ Удалить', callback_data=f'delete_notification_{notification_id}')]
        ]
    )
    return edit_notification_keyboard


async def get_delete_keyboard() -> InlineKeyboardMarkup:
    delete_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Удалить', callback_data='delete')],
            [InlineKeyboardButton(text='Отмена', callback_data='cancel')]
            ]
        )
    return delete_keyboard


async def get_time_keyboard(selected_date: str = None) -> ReplyKeyboardMarkup:
    times = [
        "07:00", "07:30", "08:00", "08:30", "09:00", "09:30",
        "10:00", "10:30", "11:00", "11:30", "12:00", "12:30",
        "13:00", "13:30", "14:00", "14:30", "15:00", "15:30",
        "16:00", "16:30", "17:00", "17:30", "18:00", "18:30",
        "19:00", "19:30", "20:00", "20:30", "21:00", "21:30",
        "22:00", "22:30"
    ]

    if selected_date:
        try:
            selected_date_obj = datetime.strptime(selected_date, "%d.%m.%Y").date()
            current_date = datetime.now().date()

            if selected_date_obj == current_date:
                current_time = datetime.now().time()
                times = [time for time in times if datetime.strptime(time, "%H:%M").time() > current_time]
        except ValueError:
            pass

    time_keyboard = ReplyKeyboardMarkup(keyboard=[])
    row = []
    for time in times:
        row.append(KeyboardButton(text=time))
        if len(row) == 2:
            time_keyboard.keyboard.append(row)
            row = []
    if row:
        time_keyboard.keyboard.append(row)

    return time_keyboard


async def get_weekdays_keyboard(selected_weekdays=None):
    if selected_weekdays is None:
        selected_weekdays = []

    weekdays = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    weekdays_keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    for weekday in weekdays:
        if weekday in selected_weekdays:
            button_text = f"{weekday} ✅"
        else:
            button_text = weekday

        weekdays_keyboard.inline_keyboard.append([InlineKeyboardButton(text=button_text, callback_data=f"weekday_{weekday}")])

    return weekdays_keyboard


async def get_confirm_keyboard():
    confirm_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Да')],
            [KeyboardButton(text='Нет')]
        ]
    )
    return confirm_keyboard


async def get_continue_keyboard() -> ReplyKeyboardMarkup:
    continue_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Продолжить')],
        ]
    )
    return continue_keyboard


async def get_create_keyboard() -> ReplyKeyboardMarkup:
    create_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Создать')],
        ]
    )
    return create_keyboard


async def get_recipient_type_keyboard():
    recipient_type_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="В группу")],
            [KeyboardButton(text="В личные сообщения")],
        ]
    )
    return recipient_type_keyboard


async def remove_keyboard():
    return ReplyKeyboardRemove()


async def get_users_list_keyboard() -> InlineKeyboardMarkup:
    users_dict = await db.get_all_users_dict()
    users_keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for user_id, user_data in users_dict.items():
        button_text = f"{user_data['lastname']} {user_data['firstname']}"
        users_keyboard.inline_keyboard.append([InlineKeyboardButton(text=button_text, callback_data=f"user_{user_id}")])
    
    return users_keyboard


async def get_user_actions_keyboard(user_id: int) -> InlineKeyboardMarkup:
    user_actions_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Удалить', callback_data=f'delete_user_{user_id}')],
            [InlineKeyboardButton(text='Пощадить', callback_data=f'spare_user_{user_id}')]
        ]
    )
    return user_actions_keyboard


async def get_groups_list_keyboard() -> InlineKeyboardMarkup:
    groups_dict = await db.get_all_groups()
    groups_keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for group_id, group_info in groups_dict.items():
        button_text = f"{group_info['name']}"
        groups_keyboard.inline_keyboard.append([InlineKeyboardButton(text=button_text, callback_data=f"None")])
    
    return groups_keyboard


async def get_date_keyboard() -> ReplyKeyboardMarkup:
    weekday_translation = {
        "Monday": "Понедельник",
        "Tuesday": "Вторник",
        "Wednesday": "Среда",
        "Thursday": "Четверг",
        "Friday": "Пятница",
        "Saturday": "Суббота",
        "Sunday": "Воскресенье"
    }
    today = datetime.now().date()
    
    dates = [today + timedelta(days=i) for i in range(7)]
    
    date_strings = [
        f"Сегодня {dates[0].strftime('%d.%m.%Y')}",
        f"Завтра {dates[1].strftime('%d.%m.%Y')}",
        *[f"{weekday_translation[dates[i].strftime('%A')]} {dates[i].strftime('%d.%m.%Y')}" for i in range(2, 7)]
    ]  

    date_keyboard = ReplyKeyboardMarkup(keyboard=[])
    row = []
    for date_str in date_strings:
        row.append(KeyboardButton(text=date_str))
        if len(row) == 2:
            date_keyboard.keyboard.append(row)
            row = []
    if row:
        date_keyboard.keyboard.append(row)
    
    return date_keyboard