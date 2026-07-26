from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.parsers.search import parse_search_query
from app.bot.formatters.restaurant import format_restaurant_card
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

    query, max_average_check = parse_search_query(parts[1])

    if len(query) < 2:
        await message.answer("Запрос слишком короткий")
        return

    restaurants = await service.search(query, limit=5, max_average_check=max_average_check)

    if not restaurants:
        await message.answer("Ресторанов по данному запросу не найдено")
        return

    for restaurant in restaurants:
        text = format_restaurant_card(restaurant)
        await message.answer(text, reply_markup=add_to_favorite_keyboard(restaurant.id))
