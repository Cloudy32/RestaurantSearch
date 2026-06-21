from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def inline_keyboard(restaurant_id: int) -> InlineKeyboardMarkup:
    add_to_favorite = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(
            text="Добавить в избранное",
            callback_data=f"add_favorite:{restaurant_id}")]]
    )

    return add_to_favorite