from app.db.models.restaurant import Restaurant


def format_restaurant_card(restaurant: Restaurant) -> str:

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

    return text