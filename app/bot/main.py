
from aiogram import Bot, Dispatcher

from app.core.config import get_settings

from app.bot.handlers.start import start_router
from app.bot.handlers.search import search_router
from app.bot.middleware.database import DBMiddleware
from app.db.session import async_session_maker

bot = Bot(token=get_settings().bot_token)
dp = Dispatcher()
dp.include_routers(start_router,search_router)
dp.message.middleware(DBMiddleware(async_session_maker))

async def on_startup():
    await dp.start_polling(bot)

