from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from app.core.config import get_settings

from app.bot.handlers.start import start_router
from app.bot.handlers.help import help_router
from app.bot.handlers.favorites import favorite_router
from app.bot.handlers.restaurants import restaurant_router
from app.bot.handlers.search import search_router
from app.bot.middleware.database import DBMiddleware
from app.db.session import async_session_maker


bot = Bot(token=get_settings().bot_token)
dp = Dispatcher()
dp.include_routers(
    start_router,
    help_router,
    restaurant_router,
    favorite_router,
    search_router,
)
dp.message.middleware(DBMiddleware(async_session_maker))
dp.callback_query.middleware(DBMiddleware(async_session_maker))

async def set_bot_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command="start", description="Начать работу"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="search", description="Поиск ресторанов"),
        BotCommand(command="restaurants", description="Рестораны из базы"),
        BotCommand(command="favorites", description="Избранное"),
    ]
    await bot.set_my_commands(commands)


async def on_startup():
    await set_bot_commands(bot)
    await dp.start_polling(bot)
