from aiogram import Bot


async def send_notification(bot: Bot, title: str, description: str, recipients_ids: dict):
    # Отправка уведомлений пользователям
    for user_id in recipients_ids.get("users", []):
        await bot.send_message(user_id, f"Напоминание: {title}\nОписание: {description}")
    
    # Отправка уведомлений группам
    for group_id in recipients_ids.get("groups", []):
        await bot.send_message(group_id, f"Напоминание: {title}\nОписание: {description}")
