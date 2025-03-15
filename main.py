import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from bot.handlers import router
from bot.config import Config
from bot.database import init_db
from bot.logger import logger


async def main():
    try:
        # Инициализация бота и диспетчера
        bot = Bot(token=Config.TELEGRAM_TOKEN)
        dp = Dispatcher(bot=bot, storage=MemoryStorage())

        # Инициализация базы данных
        await init_db()
        logger.info("Database initialized successfully.")

        # Инициализация планировщика задач
        scheduler = AsyncIOScheduler()

        # # Добавление задач в планировщик
        # scheduler.add_job(
        #     func=send_morning_notification,
        #     trigger=CronTrigger(hour=8, minute=0, timezone="Europe/Moscow"),  # 08:00 МСК
        #     args=(bot,),
        #     id="morning_notification",
        #     name="Morning Notification",
        # )


        # Запуск планировщика
        scheduler.start()
        logger.info("Scheduler started successfully.")

        # Подключение роутера
        dp.include_router(router)
        logger.info("Router included successfully.")

        # Запуск бота
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Webhook deleted. Starting polling...")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

    except Exception as error:
        logger.error(f"Bot error: {error}", exc_info=True)
        raise  # Повторно выбрасываем исключение для завершения работы

    finally:
        # Корректное завершение работы
        logger.info("Shutting down the bot...")
        if scheduler.running:
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully.")
        if hasattr(dp, '_polling') and dp._polling:
            await dp.stop_polling()
            logger.info("Polling stopped successfully.")
        await bot.session.close()
        logger.info("Bot session closed.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
    except Exception as error:
        logger.error(f"Unexpected error: {error}", exc_info=True)
