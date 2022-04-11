from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import _


async def users_main_menu():
    user_menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Konkurs 🎁")),
                KeyboardButton(text=_("Do'konlar 🏣"))
            ],
            [
                KeyboardButton(text=_("Profil 👤")),
                KeyboardButton(text=_("Aloqa ☎"))
            ]
        ], resize_keyboard=True
    )
    return user_menu


async def user_comp_image_again():
    image = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Yana rasm 📷")),
                KeyboardButton(text=_("Habarga o'tish ➡"))
            ]
        ], resize_keyboard=True
    )
    return image


async def after_like_menu():
    menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Yana ko'rish ⏩")),
                KeyboardButton(text=_("Asosiy menyu ⏹"))
            ]
        ], resize_keyboard=True
    )
    return menu