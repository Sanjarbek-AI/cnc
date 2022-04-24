from aiogram import types
from aiogram.types.callback_query import CallbackQuery

from filters.private_chat import IsPrivate
from keyboards.default.users import users_main_menu
from keyboards.inline.admin_showroom import showrooms_keyboard_user, user_dealers_keyboard
from keyboards.inline.admins import profile_def
from keyboards.inline.users import comp_menu_def, back_user_comp_menu, post_like
from loader import dp, _, bot
from utils.db_api.commands import *
from utils.db_api.user_posts import get_user_post, get_user_active_comp_post


async def return_admin_profile_text(user):
    return f"""
<b>{_("Ism Familiya")}</b>: {user['full_name'] if user['full_name'] else "-"} \n
<b>{_("Manzil")}</b>: {user['location'] if user['location'] else "-"} \n
<b>{_("Til")}</b>: {"O'zbek 🇺🇿" if user['language'] == "uz" else "Pусский 🇷🇺"} \n
<b>{_("Telefon raqam")}</b>: {user['phone_number'] if user['phone_number'] else "-"} \n
"""


@dp.message_handler(IsPrivate(), text=['Профиль 👤', 'Profil 👤'])
async def profile(message: types.Message):
    user = await get_user(message.from_user.id)
    if user:
        text = await return_admin_profile_text(user)
        await message.answer(text, reply_markup=await profile_def(user['language'], message.from_user.id))
    else:
        text = _("Botda nosozlik yuz berdi.")
        await message.answer(text, reply_markup=await users_main_menu())


@dp.message_handler(IsPrivate(), text=['Конкурс 🎁', 'Konkurs 🎁'])
async def get_competition(message: types):
    user_id = message.from_user.id
    user = await get_user(user_id)
    competition = await get_competitions()

    if competition:
        post = await get_user_active_comp_post(user_id, competition["id"])
        if post:
            post_data = await get_user_post(post["id"])
            link = f"https://t.me/cncele_bot?start={post['id']}"
            await message.answer_photo(photo=post_data["images"][0],
                                       reply_markup=await post_like(post['id'], link))
        else:
            if competition and user["language"] == "uz":
                await message.answer_photo(photo=competition["image_uz"], caption=competition["conditions_uz"],
                                           reply_markup=await comp_menu_def())
            elif competition and user["language"] == "ru":
                await message.answer_photo(photo=competition["image_ru"], caption=competition["conditions_ru"],
                                           reply_markup=await comp_menu_def())
            else:
                text = _("Hozirda faol konkurslar mavjud emas. Tez orada yangi konkursimizni boshlaymiz.")
                await message.answer(text, reply_markup=await users_main_menu())
    else:
        text = _("Hozirda faol konkurslar mavjud emas. Tez orada yangi konkursimizni boshlaymiz.")
        await message.answer(text, reply_markup=await users_main_menu())


@dp.message_handler(IsPrivate(), text=['Aloqa ☎', 'Контакты ☎'])
async def admin_profile(message: types.Message):
    contact = await get_contact()
    user = await get_user(message.from_user.id)
    if contact and user:
        if user["language"] == "uz":
            await message.answer_photo(
                contact['image_uz'], caption=contact["contact_uz"],
                reply_markup=await users_main_menu()
            )
        else:
            await message.answer_photo(
                contact['image_ru'], caption=contact["contact_ru"],
                reply_markup=await users_main_menu()
            )
    else:
        text = _("Botda nosozlik yuz berdi.")
        await message.answer(text, reply_markup=await users_main_menu())


@dp.message_handler(IsPrivate(), text=["Do'konlar 🏣", "Магазины 🏣"])
async def get_user_showrooms(message: types):
    showroom_all = await get_showrooms()
    if showroom_all:
        user = await get_user(message.from_user.id)
        text = _("Bizning rasmiy diller va do'konlarimiz haqida:")
        if user:
            await message.answer(text, reply_markup=await showrooms_keyboard_user(user["language"]))
        else:
            await message.answer(text, reply_markup=await showrooms_keyboard_user("uz"))
    else:
        text = _("Botda nosozlik yuz berdi.")
        await message.answer(text, reply_markup=await users_main_menu())


@dp.callback_query_handler(text="user_dealers")
async def user_dealers(call: CallbackQuery):
    dealers_all = await get_dealers()
    if dealers_all:
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        user = await get_user(call.from_user.id)
        if user["language"] == "ru":
            text = _("Список наших официальных дилеров.")
        else:
            text = _("Bizning rasmiy dillerlarimiz ro'yxati.")
        user = await get_user(call.from_user.id)
        await call.message.answer(text, reply_markup=await user_dealers_keyboard(user["language"]))
    else:
        text = _("Hozirda dillerlar mavjud emas.")
        await call.message.answer(text, reply_markup=await users_main_menu())


@dp.callback_query_handler(text="back_user_showroom_menu")
async def back_user_showroom_menu(call: CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    showroom_all = await get_showrooms()
    if showroom_all:
        text = _("Bizning rasmiy diller va do'konlarimiz haqida:")
        user = await get_user(call.from_user.id)
        await call.message.answer(text, reply_markup=await showrooms_keyboard_user(user["language"]))
    else:
        text = _("Botda nosozlik yuz berdi.")
        await call.message.answer(text, reply_markup=await users_main_menu())


@dp.callback_query_handler(text="user_comp_gifts")
async def user_comp_gifts(call: CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    competition = await get_competitions()
    user = await get_user(call.from_user.id)

    if competition and user:
        if user["language"] == "uz":
            await call.message.answer_photo(
                photo=competition["gifts_image_uz"],
                caption=competition["gifts_uz"],
                reply_markup=await back_user_comp_menu())
        else:
            await call.message.answer_photo(
                photo=competition["gifts_image_ru"],
                caption=competition["gifts_ru"],
                reply_markup=await back_user_comp_menu())

    else:
        text = _("Botda nosozlik yuz berdi.")
        await call.message.answer(text, reply_markup=await users_main_menu())


@dp.callback_query_handler(text="user_back_comp_menu")
async def user_back_comp_menu(call: CallbackQuery):
    try:
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        user = await get_user(call.from_user.id)
        competition = await get_competitions()
        if competition and user["language"] == "uz":
            await call.message.answer_photo(photo=competition["image_uz"], caption=competition["conditions_uz"],
                                            reply_markup=await comp_menu_def())
        elif competition and user["language"] == "ru":
            await call.message.answer_photo(photo=competition["image_ru"], caption=competition["conditions_ru"],
                                            reply_markup=await comp_menu_def())
    except Exception as exc:
        print(exc)
