from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards.inline import remove_from_favorite_keyboard

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

    if not favorites:
        await message.answer("Ваш список избранного пустой")
        return

    for favorite in favorites:

        restaurant = favorite.restaurant

        rating = restaurant.rating if restaurant.rating is not None else "Не указан"
        average_check = restaurant.average_check if restaurant.average_check is not None else "Не указан"
        description = restaurant.description if restaurant.description is not None else "Не указано"

        text = (
            f"{restaurant.id}. {restaurant.name}\n"
            f"Описание: {description}\n"
            f"Город: {restaurant.city}\n"
            f"Адрес: {restaurant.address}\n"
            f"Рейтинг: {rating}\n"
            f"Средний чек: {average_check}"
        )

        await message.answer(text, reply_markup=remove_from_favorite_keyboard(restaurant.id))


@favorite_router.callback_query(F.data.startswith("remove_favorite:"))
async def remove_favorite(callback_query: CallbackQuery, session: AsyncSession):
    if callback_query.from_user is None:
        return

    user_repository = UserRepository(session)
    user_service = UserService(user_repository)

    user = await user_service.get_or_create_user(
        callback_query.from_user.id,
        callback_query.from_user.username,
        callback_query.from_user.first_name,
    )

    user_id = user.id

    favorite_repository = FavoriteRepository(session)
    favorite_service = FavoriteService(favorite_repository)

    restaurant_id = int(callback_query.data.split(":")[1])

    result = await favorite_service.remove_favorite(user_id, restaurant_id)

    if result:
        await callback_query.message.edit_reply_markup(reply_markup=None)
        return await callback_query.answer("Удалено из избранного")

    return await callback_query.answer("Этого ресторана уже нет в избранном")
