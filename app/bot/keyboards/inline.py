from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def add_to_favorite_keyboard(restaurant_id: int) -> InlineKeyboardMarkup:
    add_to_favorite = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(
            text="Добавить в избранное",
            callback_data=f"add_favorite:{restaurant_id}")]]
    )

    return add_to_favorite


def remove_from_favorite_keyboard(restaurant_id: int) -> InlineKeyboardMarkup:
    remove_from_favorite = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(
            text="Удалить ресторан из избранного",
            callback_data=f"remove_favorite:{restaurant_id}"
        )]]
    )

    return remove_from_favorite