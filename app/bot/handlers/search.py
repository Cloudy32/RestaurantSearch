from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards.inline import add_to_favorite_keyboard
from app.repositories.restaurant_repo import RestaurantRepository
from app.services.search_service import SearchService

search_router = Router()


@search_router.message(Command('search'))
async def search(message: Message, session: AsyncSession):

    repository = RestaurantRepository(session)
    service = SearchService(repository)

    parts = message.text.split(maxsplit=1)
    if len(parts) != 2:
        await message.answer("Напиши запрос после команды: /search (Город) или (Название)")
        return

    query_text = parts[1].strip()
    query_parts = query_text.split()

    if not query_parts:
        await message.answer("Запрос слишком короткий")
        return

    max_average_check = None

    if query_parts[-1].isdigit():
        max_average_check = int(query_parts[-1])
        query = " ".join(query_parts[:-1])
    else:
        query = query_text

    if len(query) < 2:
        await message.answer("Запрос слишком короткий")
        return

    restaurants = await service.search(query, limit=5, max_average_check=max_average_check)

    if not restaurants:
        await message.answer("Ресторанов по данному запросу не найдено")
        return

    for restaurant in restaurants:
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

        await message.answer(text, reply_markup=add_to_favorite_keyboard(restaurant.id))
