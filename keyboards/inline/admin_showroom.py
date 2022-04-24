from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import _
from utils.db_api.commands import get_showrooms, get_dealers


async def add_showroom_def():
    add_showroom = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Shovrum qo'shish ➕"), callback_data="add_showroom")
            ]
        ]
    )
    return add_showroom


async def add_dealer_def():
    add_dealer = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Diller qo'shish ➕"), callback_data="add_dealer")
            ]
        ]
    )
    return add_dealer


async def showrooms_keyboard(lang):
    markup = InlineKeyboardMarkup(row_width=2)

    showrooms_list = await get_showrooms()

    for showroom in showrooms_list:
        markup.insert(
            InlineKeyboardButton(text=showroom['name_uz'] if lang == "uz" else showroom['name_ru'],
                                 callback_data="showroom_" + lang + "_" + str(showroom['id']))
        )
    markup.insert(
        InlineKeyboardButton(text=_("Shovrum qo'shish ➕"), callback_data='add_showroom')
    )
    if lang == "uz":
        markup.insert(
            InlineKeyboardButton(text=_("Ruscha 🇷🇺"), callback_data='showrooms_ru')
        )
    else:
        markup.insert(
            InlineKeyboardButton(text=_("O'zbek 🇺🇿"), callback_data='showrooms_uz')
        )

    markup.insert(
        InlineKeyboardButton(text=_("Dillerlarga o'tish ▶"), callback_data='admin_dealers')
    )
    return markup


async def dealers_keyboard(lang):
    markup = InlineKeyboardMarkup(row_width=2)

    dealers_list = await get_dealers()

    for dealer in dealers_list:
        markup.insert(
            InlineKeyboardButton(text=dealer['name_uz'] if lang == "uz" else dealer['name_ru'],
                                 callback_data="dealers_" + lang + "_" + str(dealer['id']))
        )
    markup.insert(
        InlineKeyboardButton(text=_("Diller qo'shish ➕"), callback_data='add_dealer')
    )
    if lang == "uz":
        markup.insert(
            InlineKeyboardButton(text=_("Ruscha 🇷🇺"), callback_data='dealers_ru')
        )
    else:
        markup.insert(
            InlineKeyboardButton(text=_("O'zbek 🇺🇿"), callback_data='dealers_uz')
        )
    markup.insert(
        InlineKeyboardButton(text=_("Shovrumlarga qaytish ◀"), callback_data='back_to_showroom_menu_user')
    )
    return markup


async def user_dealers_keyboard(lang):
    markup = InlineKeyboardMarkup(row_width=2)

    dealers_list = await get_dealers()

    for dealer in dealers_list:
        markup.insert(
            InlineKeyboardButton(text=dealer['name_uz'] if lang == "uz" else dealer['name_ru'],
                                 callback_data="dealers_" + lang + "_" + str(dealer['id']))
        )
    if lang == "ru":
        text = "Вернуться к Шоврумсу ◀"
    else:
        text = "Shovrumlarga qaytish ◀"
    markup.insert(
        InlineKeyboardButton(text=text, callback_data='back_user_showroom_menu')
    )
    return markup


async def showrooms_keyboard_user(lang):
    markup = InlineKeyboardMarkup(row_width=2)

    showrooms_list = await get_showrooms()

    for showroom in showrooms_list:
        markup.insert(
            InlineKeyboardButton(text=showroom['name_uz'] if lang == "uz" else showroom['name_ru'],
                                 callback_data="showroom_" + lang + "_" + str(showroom['id']))
        )
    if lang == "ru":
        text = "Посмотреть дилеров ⏩"
    else:
        text = "Dillerlarni ko'rish ⏩"
    markup.insert(
        InlineKeyboardButton(text=text, callback_data="user_dealers")
    )

    return markup


change_showroom = CallbackData("change_sh_image", "act", "lang", "sh_id")


async def update_showroom_def(lang, sh_id):
    add_showroom = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Rasmni o'zgartirish"),
                                     callback_data=change_showroom.new(act="change_sh_image", lang=lang, sh_id=sh_id)),
                InlineKeyboardButton(text=_("Matnni o'zgartirish"),
                                     callback_data=change_showroom.new(act="change_sh_text", lang=lang, sh_id=sh_id))
            ],
            [
                InlineKeyboardButton(text=_("Linkni o'zgartirish"),
                                     callback_data=change_showroom.new(act="change_sh_link", lang=lang, sh_id=sh_id)),
                InlineKeyboardButton(text=_("Nomni o'zgartirish"),
                                     callback_data=change_showroom.new(act="change_sh_name", lang=lang, sh_id=sh_id))
            ],
            [
                InlineKeyboardButton(text=_("Ruscha 🇷🇺") if lang == "uz" else _("O'zbek 🇺🇿"),
                                     callback_data=change_showroom.new(act="change_language", lang=lang, sh_id=sh_id)),

                InlineKeyboardButton(text=_("Ortga ◀"), callback_data="back_showroom_menu")
            ]
        ]
    )
    return add_showroom
