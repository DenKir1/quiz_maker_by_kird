import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from database.settings import config
from database.db import create_db, session  # drop_db
from handlers.echo import echo_router
from handlers.play import play_router
from handlers.question import question_router
from handlers.quiz import quiz_router
from handlers.user import user_router

from middlewares.middlewares import SessionMiddleware


logging.basicConfig(level=logging.INFO)


bot = Bot(token=config.bot_token.get_secret_value(),
          default=DefaultBotProperties(parse_mode=ParseMode.HTML),
          )

dp = Dispatcher(storage=MemoryStorage())
dp.include_router(user_router)
dp.include_router(quiz_router)
dp.include_router(question_router)
dp.include_router(play_router)
dp.include_router(echo_router)


async def on_startup():
    await create_db()
    print('БОТ ЖИВ')


async def on_shutdown():
    # await drop_db()
    print('БОТ УМЕР')


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.outer_middleware(SessionMiddleware(session_pool=session))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt as kex:
        print("Good Bye")
