from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

start_router=Router()

@start_router.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет {message.from_user.first_name} я бот по поиску хороших ресторанов, в которых ты"
                         f"сможешь хорошо провести время(сытно позавтракать, вкусно пообедать или хорошо провести вечер!")

