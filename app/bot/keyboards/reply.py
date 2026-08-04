from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    main_menu = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='/help'), KeyboardButton(text='/search')],
                  [KeyboardButton(text='/restaurants'), KeyboardButton(text='/favorites')]], resize_keyboard=True
    )

    return main_menu