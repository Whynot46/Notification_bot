import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from bot.handlers import router
from bot.config import Config
from bot.database import init_db
from bot.logger import logger
from bot.scheduler import scheduler


async def main():
    try:
        bot = Bot(token=Config.TELEGRAM_TOKEN)
        dp = Dispatcher(bot=bot, storage=MemoryStorage())

        await init_db()
        logger.info("Database initialized successfully.")

        scheduler.start()
        logger.info("Scheduler started successfully.")

        dp.include_router(router)
        logger.info("Router included successfully.")

        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Webhook deleted. Starting polling...")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

    except Exception as error:
        logger.error(f"Bot error: {error}", exc_info=True)
        raise

    finally:
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
