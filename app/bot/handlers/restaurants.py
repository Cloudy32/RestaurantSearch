from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command


from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.restaurant_repo import RestaurantRepository
from app.services.restaurant_service import RestaurantService

restaurant_router = Router()

@restaurant_router.message(Command("restaurants"))
async def restaurants(message: Message, session: AsyncSession):

    repository = RestaurantRepository(session)
    service = RestaurantService(repository)

    restaurants = await service.get_all(limit=5)
    if not restaurants:
        await message.answer("Рестораны пока не добавлены")
        return

    lines = []
    for restaurant in restaurants:
        rating = restaurant.rating if restaurant.rating is not None else "Не указан"
        average_check = restaurant.average_check if restaurant.average_check is not None else "Не указан"

        lines.append(
            f"{restaurant.id}. {restaurant.name}\n"
            f"Город: {restaurant.city}\n"
            f"Адрес: {restaurant.address}\n"
            f"Рейтинг: {rating}\n"
            f"Средний чек: {average_check}"
        )

    text = "\n\n".join(lines)
    await message.answer(text)
