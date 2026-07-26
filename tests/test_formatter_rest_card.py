from decimal import Decimal

from app.bot.formatters.restaurant import format_restaurant_card
from app.db.models import Restaurant

restaurant1 = Restaurant(
    id=1,
    name="Kizoku",
    description="Koku",
    city="Bryansk",
    address="Voistrochenko 5",
    average_check=1500,
    rating=Decimal("5.0"),
    latitude=None,
    longitude=None,
)

restaurant2 = Restaurant(
    id=2,
    name="No Data",
    description=None,
    city="Moscow",
    address="Unknown",
    average_check=None,
    rating=None,
    latitude=None,
    longitude=None,
)

def test_format_restaurant_card():

    text = format_restaurant_card(restaurant1)

    assert "1. Kizoku" in text
    assert "Описание: Koku" in text
    assert "Город: Bryansk" in text
    assert "Адрес: Voistrochenko 5" in text
    assert "Рейтинг: 5.0" in text
    assert "Средний чек: 1500" in text

def test_formatter_restaurant_card_with_none():

    text = format_restaurant_card(restaurant2)

    assert "Описание: Не указано" in text
    assert "Рейтинг: Не указан" in text
    assert "Средний чек: Не указан" in text
