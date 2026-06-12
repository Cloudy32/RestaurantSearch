from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repo import UserRepository
from app.services.user_service import UserService

start_router=Router()

@start_router.message(CommandStart())
async def start(message: Message, session: AsyncSession):
    if message.from_user is None:
        return

    repository = UserRepository(session)
    service = UserService(repository)

    await service.get_or_create_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name
    )

    await message.answer(f"Привет {message.from_user.first_name} я бот по поиску хороших ресторанов, в которых ты"
                         f"сможешь хорошо провести время(сытно позавтракать, вкусно пообедать или хорошо провести вечер!")

