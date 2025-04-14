from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from aiogram import Bot
from bot.logger import logger
from bot.notifications import send_notification
from datetime import datetime
from typing import Optional, Tuple


scheduler = AsyncIOScheduler()


async def add_notification(bot: Bot, notification_id: int, title: str, description: str, sender_date: str, sender_time: str,
                           sender_weekday: Optional[Tuple[str, ...]] = None, recipients_ids: tuple = None):
    try:
        weekday_to_number = {
            "Понедельник": 0,
            "Вторник": 1,
            "Среда": 2,
            "Четверг": 3,
            "Пятница": 4,
            "Суббота": 5,
            "Воскресенье": 6,
        }

        hour, minute = sender_time.split(":")

        if sender_weekday:
            day_of_week = ",".join(str(weekday_to_number[day]) for day in sender_weekday)
            trigger = CronTrigger(
                hour=hour,
                minute=minute,
                day_of_week=day_of_week, 
            )
        else:
            notification_datetime = datetime.strptime(f"{sender_date} {sender_time}", "%d.%m.%Y %H:%M")
            trigger = DateTrigger(
                run_date=notification_datetime,
            )

        scheduler.add_job(
            func=send_notification,
            trigger=trigger,
            args=(bot, title, description, recipients_ids),
            id=str(notification_id),
            replace_existing=True,
        )

        logger.info(f"В планировщик добавлено новое напоминание id:{notification_id}")

    except Exception as error:
        logger.error(f"Ошибка добавления напоминания id:{notification_id} - {error}")