from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command


from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.formatters.restaurant import format_restaurant_card
from app.bot.keyboards.inline import add_to_favorite_keyboard
from app.repositories.restaurant_repo import RestaurantRepository
from app.services.restaurant_service import RestaurantService
from app.repositories.favorite_repo import FavoriteRepository
from app.services.favorite_service import FavoriteService
from app.repositories.user_repo import UserRepository
from app.services.user_service import UserService


restaurant_router = Router()


@restaurant_router.message(Command("restaurants"))
async def restaurants(message: Message, session: AsyncSession):

    repository = RestaurantRepository(session)
    service = RestaurantService(repository)

    restaurants = await service.get_all(limit=5)
    if not restaurants:
        await message.answer("Рестораны пока не добавлены.\n\nПопробуй найти их через /search.")
        return

    for restaurant in restaurants:
        text = format_restaurant_card(restaurant)
        await message.answer(text, reply_markup=add_to_favorite_keyboard(restaurant.id))


@restaurant_router.callback_query(F.data.startswith("add_favorite:"))
async def add_favorite(callback_query: CallbackQuery, session: AsyncSession):

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

    await favorite_service.get_or_create_favorite(user_id, restaurant_id)
    await callback_query.answer("Ресторан сохранён в избранное", show_alert=False)