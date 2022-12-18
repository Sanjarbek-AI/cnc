from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import _
from utils.db_api.user_posts import get_post_like


async def back_user_comp_menu():
    back = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Ortga ◀"), callback_data="user_back_comp_menu"),
            ]
        ]
    )
    return back


async def export_excel_users():
    users_excel = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Excel olish (ro'yxatdan o'tganlar)"), callback_data="registered_users"),
            ]
        ]
    )
    return users_excel


async def comp_menu_def():
    comp_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Kanalga a'zo bo'lish ➕"), url="https://t.me/electromaxgroup")
            ],
            [
                InlineKeyboardButton(text=_("Sovg'alar 🎁"), callback_data="user_comp_gifts")
            ],
            [
                InlineKeyboardButton(text=_("Rasmlarni yuborish ⏏"), callback_data="send_comp_post")
            ],
            [
                InlineKeyboardButton(text=_("Tekshirish ✅"), callback_data="checking")
            ]
        ]
    )
    return comp_menu


async def user_profile():
    user = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Ism Familiya"), callback_data="user_change_full_name"),
                InlineKeyboardButton(text=_("Til"), callback_data="user_change_language"),
            ],
            [
                InlineKeyboardButton(text=_("Telefon raqam"), callback_data="user_change_phone_number"),
                InlineKeyboardButton(text=_("Manzil"), callback_data="user_change_location"),
            ]
        ]
    )
    return user


delete_user_post_callback = CallbackData("delete_post", "act", "post_id")


async def delete_user_post(post_id):
    admin_answer = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="O'chirish 🗑",
                                     callback_data=delete_user_post_callback.new(act="delete_post", post_id=post_id)),
            ]
        ]
    )
    return admin_answer


async def showroom_menu_user(showroom_link):
    user = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Xaritada ko'rish 🗺"), url=showroom_link),
                InlineKeyboardButton(text=_("Ortga ◀"), callback_data="back_user_showroom_menu"),
            ]
        ]
    )
    return user


callback_admin_answer = CallbackData("admin_answer", "act", "post_id")


async def admin_answer_def(post_id):
    admin_answer = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Qabul qilish ✅",
                                     callback_data=callback_admin_answer.new(act="admin_answer_yes", post_id=post_id)),
                InlineKeyboardButton(text="Bekor qilish ❌",
                                     callback_data=callback_admin_answer.new(act="admin_answer_no", post_id=post_id))
            ]
        ]
    )
    return admin_answer


post_like_call = CallbackData("like", "act", "post_id")


async def post_like(post_id, link):
    post_like_data = await get_post_like(post_id)
    if post_like_data:
        post_like_num = len(post_like_data)
    else:
        post_like_num = ""

    admin_answer = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"{post_like_num} ❤",
                                     callback_data=post_like_call.new(act="add_or_remove_like", post_id=post_id))
            ],
            [
                InlineKeyboardButton(text=f"Ulashish ⏏", switch_inline_query=f"| {link}")
            ]
        ]
    )
    return admin_answer


async def user_electric_status():
    status = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Ha ✅"), callback_data="1"),
                InlineKeyboardButton(text=_("Yo'q ❌"), callback_data="0")
            ]
        ]
    )
    return status
