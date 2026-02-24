import asyncio
from aiogram import Bot, Dispatcher

from app.common.logging import configure_logging
from app.config import get_settings
from app.transport.telegram.handlers.common import router as common_router
from app.transport.telegram.handlers.game import router as game_router
from app.transport.telegram.middlewares.idempotency import IdempotencyMiddleware


async def main() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)
    bot = Bot(settings.bot_token)
    dp = Dispatcher()
    dp.update.middleware(IdempotencyMiddleware())
    dp.include_router(common_router)
    dp.include_router(game_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
