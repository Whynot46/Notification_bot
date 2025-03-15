from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
import bot.database as db
from bot.config import Config


async def get_main_menu_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    if Config.is_admin(user_id):
        reply_keyboard = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='🏠Напоминания Роутима'), KeyboardButton(text='🧑🏻‍💻Мои напоминания')],
            [KeyboardButton(text='🔔Создать напоминание')],
            [KeyboardButton(text='👥Пользователи и группы')],
        ], resize_keyboard=True)
    else:
        reply_keyboard = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='🏠Напоминания Роутима'), KeyboardButton(text='🧑🏻‍💻Мои напоминания')],
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
        users_keyboard.inline_keyboard.append([InlineKeyboardButton(text=button_text, callback_data=f"user_{user_id}")])

    return users_keyboard

async def get_groups_list_keyboard(selected_groups=None) -> InlineKeyboardMarkup:
    if selected_groups is None:
        selected_groups = []

    groups_dict = await db.get_all_groups()
    groups_keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for group_id, group_info in groups_dict.items():
        button_text = f"{group_info['name']}"
        if group_id in selected_groups:
            button_text += " ✅"
        groups_keyboard.inline_keyboard.append([InlineKeyboardButton(text=button_text, callback_data=f"group_{group_id}")])
    
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


async def get_time_keyboard() -> ReplyKeyboardMarkup:
    time_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='07:00'), KeyboardButton(text='07:30')],
            [KeyboardButton(text='08:00'), KeyboardButton(text='08:30')],
            [KeyboardButton(text='09:00'), KeyboardButton(text='09:30')],
            [KeyboardButton(text='10:00'), KeyboardButton(text='10:30')],
            [KeyboardButton(text='11:00'), KeyboardButton(text='11:30')],
            [KeyboardButton(text='12:00'), KeyboardButton(text='12:30')],
            [KeyboardButton(text='13:00'), KeyboardButton(text='13:30')],
            [KeyboardButton(text='14:00'), KeyboardButton(text='14:30')],
            [KeyboardButton(text='15:00'), KeyboardButton(text='15:30')],
            [KeyboardButton(text='16:00'), KeyboardButton(text='16:30')],
            [KeyboardButton(text='17:00'), KeyboardButton(text='17:30')],
            [KeyboardButton(text='18:00'), KeyboardButton(text='18:30')],
            [KeyboardButton(text='19:00'), KeyboardButton(text='19:30')],
            [KeyboardButton(text='20:00'), KeyboardButton(text='20:30')],
            [KeyboardButton(text='21:00'), KeyboardButton(text='21:30')],
            [KeyboardButton(text='22:00'), KeyboardButton(text='22:30')],
        ]
    )
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