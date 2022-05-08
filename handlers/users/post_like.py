import random

from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

from filters.private_chat import IsPrivate
from keyboards.default.admins import contact_def
from keyboards.default.users import after_like_menu, users_main_menu
from keyboards.inline.locations import locations_def
from keyboards.inline.users import post_like_call, post_like, comp_menu_def
from loader import dp, bot, _
from states.users import RegisterLike
from utils.db_api.commands import get_competitions, register, get_user, update_user_status
from utils.db_api.user_posts import get_user_liked_or_not, delete_user_post_like, \
    add_user_post_like, get_user_post, get_all_posts


@dp.callback_query_handler(post_like_call.filter(act="add_or_remove_like"))
async def showrooms_menu_back(call: CallbackQuery, callback_data: dict):
    post_id = int(callback_data.get("post_id"))
    post = await get_user_post(post_id)

    if await get_user_liked_or_not(post_id, call.from_user.id):
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        if await delete_user_post_like(post_id, call.from_user.id):
            link = f"https://t.me/cncele_bot?start={post_id}"
            await call.message.answer_photo(photo=post["images"][0], reply_markup=await post_like(post_id, link))
    else:
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        if await add_user_post_like(post_id, call.from_user.id):
            link = f"https://t.me/cncele_bot?start={post_id}"
            await call.message.answer_photo(photo=post["images"][0], reply_markup=await post_like(post_id, link))
        text = _("Boshqa ishtorkchilarni ham ko'rish uchun yana tugmasini bosing.")
        await call.message.answer(text, reply_markup=await after_like_menu())


@dp.message_handler(IsPrivate(), text=["Yana ko'rish ⏩", "Увидеть больше ⏩"])
async def admin_profile(message: types.Message):
    competition = await get_competitions()
    if competition:
        all_users_posts = await get_all_posts(competition["id"])
        if all_users_posts:
            random_user_posts = random.choices(all_users_posts, k=1)
            for user_post in random_user_posts:
                link = f"https://t.me/cncele_bot?start={user_post['id']}"
                await message.answer_photo(photo=user_post["images"][0],
                                           reply_markup=await post_like(user_post['id'], link))
        else:
            text = _("Boshqa qatnashuvchilar mavjud emas.")
            await message.answer(text, reply_markup=await users_main_menu())
    else:
        pass


@dp.message_handler(IsPrivate(), text=["Asosiy menyu ⏹"])
async def admin_profile(message: types.Message):
    text = _("Asosiy menyuga xush kelibsiz.")
    await message.answer(text, reply_markup=await users_main_menu())


@dp.callback_query_handler(state=RegisterLike.language)
async def language(call: CallbackQuery, state: FSMContext):
    await state.update_data({
        "language": call.data,
    })

    text = "Iltimos, Ism va Familiayangizni kiriting."
    await RegisterLike.full_name.set()
    await call.message.answer(text, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=RegisterLike.full_name)
async def full_name(message: types.Message, state: FSMContext):
    await state.update_data({
        "full_name": message.text,
    })

    text = "Iltimos, Telefon raqamingizni kiriting."
    await message.answer(text, reply_markup=await contact_def())
    await RegisterLike.phone_number.set()


@dp.message_handler(state=RegisterLike.phone_number)
async def get_phone_number(message: types.Message, state: FSMContext):
    text = "Iltimos tugmadan foydalaning."
    await message.answer(text, reply_markup=await contact_def())


@dp.message_handler(content_types=types.ContentTypes.CONTACT, state=RegisterLike.phone_number)
async def get_phone_number(message: types.Message, state: FSMContext):
    await state.update_data({
        "phone_number": message.contact.phone_number
    })

    text = "Asosiy ish hududingizni tanlang."
    await message.answer(text, reply_markup=await locations_def())
    await RegisterLike.location.set()


@dp.callback_query_handler(state=RegisterLike.location)
async def location(call: CallbackQuery, state: FSMContext):
    await state.update_data({
        "location": call.data,
        "telegram_id": call.from_user.id,
    })

    registered_user = await update_user_status(call.message, state)
    if registered_user:
        await state.finish()
        try:
            text = _("Siz muvofaqqiyatli ro'yxatdan o'tdingiz.")
            await call.message.answer(text, reply_markup=await users_main_menu())

            competition = await get_competitions()
            user = await get_user(call.from_user.id)

            if competition and user["language"] == "uz":
                await call.message.answer_photo(photo=competition["image_uz"], caption=competition["conditions_uz"],
                                                reply_markup=await comp_menu_def())
            elif competition and user["language"] == "ru":
                await call.message.answer_photo(photo=competition["image_ru"], caption=competition["conditions_ru"],
                                                reply_markup=await comp_menu_def())

        except Exception as exc:
            print(exc)
    else:
        text = _("Botda nosozlik yuz berdi.")
        await call.message.answer(text, reply_markup=await users_main_menu())
        await state.finish()
