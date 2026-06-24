from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.favorite_repo import FavoriteRepository
from app.services.favorite_service import FavoriteService
from app.repositories.user_repo import UserRepository
from app.services.user_service import UserService

favorite_router = Router()

@favorite_router.message(Command("favorites"))
async def get_favorites(message: Message, session: AsyncSession):
    if message.from_user is None:
        return

    user_repo = UserRepository(session)
    user_service = UserService(user_repo)

    user = await user_service.get_or_create_user(
     message.from_user.id,
     message.from_user.username,
     message.from_user.first_name
    )

    user_id = user.id

    favorite_repository = FavoriteRepository(session)
    favorite_service = FavoriteService(favorite_repository)

    favorites = await favorite_service.get_all(user_id)
    lines = []

    if not favorites:
        await message.answer("Ваш список избранного пустой")
        return

    for favorite in favorites:

        restaurant = favorite.restaurant

        rating = restaurant.rating if restaurant.rating is not None else "Не указан"
        average_check = restaurant.average_check if restaurant.average_check is not None else "Не указан"

        line = (
            f"{restaurant.id}. {restaurant.name}\n"
            f"Город: {restaurant.city}\n"
            f"Адрес: {restaurant.address}\n"
            f"Рейтинг: {rating}\n"
            f"Средний чек: {average_check}")
        lines.append(line)

    text = "\n\n".join(lines)
    await message.answer(text)
