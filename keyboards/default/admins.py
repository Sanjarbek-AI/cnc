from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import _
from utils.db_api.commands import get_showrooms


async def admin_main_menu():
    admin_menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Konkurs 🎁")),
                KeyboardButton(text=_("Shovrumlar 🏣"))
            ],
            [
                KeyboardButton(text=_("Profil 👤")),
                KeyboardButton(text=_("Aloqalar ☎"))
            ],
            [
                KeyboardButton(text=_("Statistika 📈")),
                KeyboardButton(text=_("Post Jo'natish ⏫"))
            ],
        ], resize_keyboard=True
    )
    return admin_menu


async def back_admin_main_menu():
    admin_menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Asosiy menyu ◀")),
            ]
        ], resize_keyboard=True
    )
    return admin_menu


async def back_showroom_menu():
    admin_showroom = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Ortga ◀")),
            ]
        ], resize_keyboard=True
    )
    return admin_showroom


async def admin_showrooms_menu(lang):
    showrooms_list = await get_showrooms()
    markup = ReplyKeyboardMarkup(row_width=2)
    for showroom in showrooms_list:
        markup.insert(
            KeyboardButton(text=showroom[f'name_' + lang], resize_keyboard=True)
        )

    return markup


async def contact_def():
    contact = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Telefon raqamni jo'natish 📞"), request_contact=True)
            ]
        ], resize_keyboard=True
    )
    return contact
