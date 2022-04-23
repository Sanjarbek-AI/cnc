from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

from filters.private_chat import IsPrivate
from handlers.users.user_menu import return_admin_profile_text
from keyboards.default.admins import admin_main_menu, back_admin_main_menu, contact_def
from keyboards.inline.admins import profile_def, profile, languages
from keyboards.inline.locations import locations_def
from loader import dp, _, bot
from main import config
from states.admins import UpdateProfile
from utils.db_api.commands import *
from utils.db_api.user_update import *
from utils.misc.phone_checker import is_valid


@dp.message_handler(IsPrivate(), text=['Профиль 👤', 'Profil 👤'], chat_id=config.ADMINS)
async def admin_profile(message: types.Message):
    user = await get_user(message.from_user.id)
    if user:
        text = await return_admin_profile_text(user)
        await message.answer(text, reply_markup=await profile_def("uz", message.from_user.id))
    else:
        text = _("Botda nosozlik yuz berdi.")
        await message.answer(text, reply_markup=await admin_main_menu())


@dp.message_handler(IsPrivate(), text=['Ortga ◀'], chat_id=config.ADMINS)
async def back_main_menu(message: types):
    text = _("Asosiy menyu.")
    await message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(profile.filter(act="change_language"), chat_id=config.ADMINS)
async def change_language(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    user_id = int(callback_data.get("user_id"))

    await state.update_data({
        "user_id": user_id
    })

    text = _("Yangi tilni tanlang.")
    await call.message.answer(text, reply_markup=ReplyKeyboardRemove())
    text = "Iltimos, tilni tanlang. 🇺🇿 \nВыберите язык. 🇷🇺"
    await call.message.answer(text, reply_markup=languages)
    await UpdateProfile.language.set()


@dp.callback_query_handler(state=UpdateProfile.language, chat_id=config.ADMINS)
async def language(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    data = await state.get_data()
    user_id = int(data.get("user_id"))
    if await update_user_language(call.message, call.data, user_id):
        text = _("Til yangilangi.")
        await call.message.answer(text, reply_markup=await back_admin_main_menu())
        await state.finish()
        user = await get_user(user_id)
        text = await return_admin_profile_text(user)
        await call.message.answer(text, reply_markup=await profile_def(user['language'], user_id))

    else:
        await state.finish()
        text = _("Botda nosozlik yuz berdi.")
        await call.message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(profile.filter(act="change_full_name"), chat_id=config.ADMINS)
async def change_full_name(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    user_id = int(callback_data.get("user_id"))

    await state.update_data({
        "user_id": user_id
    })

    text = _("Yangi ism familiyani kiriting")
    await call.message.answer(text, reply_markup=await back_admin_main_menu())
    await UpdateProfile.full_name.set()


@dp.message_handler(state=UpdateProfile.full_name, chat_id=config.ADMINS)
async def full_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = int(data.get("user_id"))
    if await update_user_full_name(message, message.text, user_id):
        text = _("Ism familiya yangilangi.")
        await message.answer(text, reply_markup=await admin_main_menu())
        await state.finish()
        user = await get_user(user_id)
        text = await return_admin_profile_text(user)
        await message.answer(text, reply_markup=await profile_def(user['language'], user_id))

    else:
        await state.finish()
        text = _("Botda nosozlik yuz berdi.")
        await message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(profile.filter(act="change_location"), chat_id=config.ADMINS)
async def change_location(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    user_id = int(callback_data.get("user_id"))

    await state.update_data({
        "user_id": user_id
    })

    text = _("Yangi manzilni tanlang")
    await call.message.answer(text, reply_markup=await locations_def())
    await UpdateProfile.location.set()


@dp.callback_query_handler(state=UpdateProfile.location, chat_id=config.ADMINS)
async def location(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    data = await state.get_data()
    user_id = int(data.get("user_id"))
    if await update_user_location(call.message, call.data, user_id):
        await state.finish()
        user = await get_user(user_id)
        text = await return_admin_profile_text(user)
        await call.message.answer(text, reply_markup=await profile_def(user['language'], user_id))

    else:
        await state.finish()
        text = _("Botda nosozlik yuz berdi.")
        await call.message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(profile.filter(act="change_phone_number"), chat_id=config.ADMINS)
async def change_location(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    user_id = int(callback_data.get("user_id"))

    await state.update_data({
        "user_id": user_id
    })

    text = _("Yangi telefon raqamni kiriting.")
    await call.message.answer(text, reply_markup=await contact_def())
    await UpdateProfile.phone_number.set()


@dp.message_handler(state=UpdateProfile.phone_number, chat_id=config.ADMINS)
async def get_phone_number(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = int(data.get("user_id"))
    if await is_valid(message.text):
        if await update_user_phone_number(message, message.text, user_id):
            await state.finish()
            text = _("Telefon raqam yangilandi.")
            await message.answer(text, reply_markup=await admin_main_menu())
            user = await get_user(user_id)
            text = await return_admin_profile_text(user)
            await message.answer(text, reply_markup=await profile_def(user['language'], user_id))
        else:
            await state.finish()
            text = _("Botda nosozlik yuz berdi.")
            await message.answer(text, reply_markup=await admin_main_menu())
    else:
        text = "Iltimos telefon raqamingizni tog'ri kiriting !"
        await message.answer(text)


@dp.message_handler(state=UpdateProfile.phone_number, content_types=types.ContentTypes.CONTACT, chat_id=config.ADMINS)
async def get_phone_number(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = int(data.get("user_id"))
    if await update_user_phone_number(message, message.contact.phone_number, user_id):
        await state.finish()
        text = _("Telefon raqam yangilandi.")
        await message.answer(text, reply_markup=await admin_main_menu())
        user = await get_user(user_id)
        text = await return_admin_profile_text(user)
        await message.answer(text, reply_markup=await profile_def(user['language'], user_id))
    else:
        await state.finish()
        text = _("Botda nosozlik yuz berdi.")
        await message.answer(text, reply_markup=await admin_main_menu())

