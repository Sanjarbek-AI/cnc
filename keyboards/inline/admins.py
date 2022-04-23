from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import _

languages = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="O'zbek 🇺🇿", callback_data="uz"),
            InlineKeyboardButton(text="Pусский 🇷🇺", callback_data="ru")
        ]
    ]
)


async def new_comp_add():
    add_comp = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Yangi ko'nkurs boshlash"), callback_data="add_comp")]
        ]
    )
    return add_comp


async def contact_admin_def(lang):
    contact_admin = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Rasmni o'zgartirish"), callback_data="change_contact_image_" + lang),
                InlineKeyboardButton(text=_("Matnni o'zgartirish"), callback_data="change_contact_text_" + lang),
            ],
            [
                InlineKeyboardButton(text=_("Ruscha 🇷🇺") if lang == "uz" else _("O'zbek 🇺🇿"),
                                     callback_data="contact_ru" if lang == "uz" else "contact_uz")
            ]
        ]
    )
    return contact_admin


async def add_contact_def():
    add_contact = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Ma'lumotlarni qo'shish ➕"), callback_data="add_contact"),
            ]
        ]
    )
    return add_contact


async def send_post_def():
    send_post = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Jo'natish ⏫"), callback_data="send_post_yes"),
                InlineKeyboardButton(text=_("Bekor qilish ❌"), callback_data="send_post_no"),
            ]
        ]
    )
    return send_post


callback_comp_ask = CallbackData("comp_yes", "act", "comp_id")


async def new_comp_ask(comp_id):
    comp_ask = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Ha"),
                                     callback_data=callback_comp_ask.new(act="comp_yes", comp_id=comp_id)),
                InlineKeyboardButton(text=_("Yo'q"), callback_data="comp_no")
            ]
        ]
    )
    return comp_ask


profile = CallbackData("profile", "act", "lang", "user_id")


async def profile_def(lang, user_id):
    profile_change = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Ism Familya"),
                                     callback_data=profile.new(act="change_full_name", lang=lang, user_id=user_id)),
                InlineKeyboardButton(text=_("Til"),
                                     callback_data=profile.new(act="change_language", lang=lang, user_id=user_id))
            ],
            [
                InlineKeyboardButton(text=_("Raqam"),
                                     callback_data=profile.new(act="change_phone_number", lang=lang, user_id=user_id)),
                InlineKeyboardButton(text=_("Manzil"),
                                     callback_data=profile.new(act="change_location", lang=lang, user_id=user_id))
            ]
        ]
    )
    return profile_change


async def send_admin_post_all(text, link):
    post_link = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=text, url=link)
            ]
        ]
    )
    return post_link
