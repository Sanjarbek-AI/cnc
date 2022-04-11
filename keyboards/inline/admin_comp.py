from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import _


async def update_comp_def(lang):
    update_comp = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Rasmni o'zgartirish"),
                                     callback_data=f"change_comp_image_" + lang),
                InlineKeyboardButton(text=_("Shartlarni o'zgartirish"),
                                     callback_data=f"change_comp_conditions_" + lang),
            ],
            [
                InlineKeyboardButton(text=_("Tamomlash 🛑"), callback_data="stop_comp"),
                InlineKeyboardButton(text=_("Sovg'alar 🎁"), callback_data=f"gifts_" + lang),
            ],
            [
                InlineKeyboardButton(text=_("O'zbek 🇺🇿"), callback_data="comp_uz"),
                InlineKeyboardButton(text=_("Ruscha 🇷🇺"), callback_data="comp_ru"),
            ]
        ]
    )
    return update_comp


async def update_comp_gifts_def(lang):
    update_comp = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Rasmni o'zgartirish"),
                                     callback_data=f"change_comp_gifts_image_" + lang),
                InlineKeyboardButton(text=_("Shartlarni o'zgartirish"),
                                     callback_data=f"change_comp_gifts_" + lang),
            ],
            [
                InlineKeyboardButton(text=_("O'zbek 🇺🇿"), callback_data="comp_gifts_uz"),
                InlineKeyboardButton(text=_("Ruscha 🇷🇺"), callback_data="comp_gifts_ru"),
            ],
            [
                InlineKeyboardButton(text=_("Ortga ◀"), callback_data="back_comp_menu_" + lang),
            ]
        ]
    )
    return update_comp


async def comp_yes_or_no():
    stop_comp = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Ha ✅", callback_data="stop_comp_yes"),
                InlineKeyboardButton(text="Yo'q ❌", callback_data="stop_comp_yes"),
            ]
        ]
    )
    return stop_comp
