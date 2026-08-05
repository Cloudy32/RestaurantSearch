from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command


help_router = Router()


@help_router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer("Что я умею:\n\n/start - начать работу\n/help - показать помощь\n"
                         "/restaurants - показать рестораны из базы\n/search <Город> - найти рестораны по городу\n"
                         "/search <Название Ресторана> <Город> - найти ресторан по названию и городу\n"
                         "/search <Средний чек> - найти рестораны по среднему чеку\n"
                         "/search <Оценка от 0 до 5> - найти рестораны с рейтингом\n"
                         "/favorites - показать избранное")

