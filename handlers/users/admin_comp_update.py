from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery

from keyboards.default.admins import back_admin_main_menu, admin_main_menu
from keyboards.inline.admin_comp import update_comp_def, update_comp_gifts_def
from loader import dp, _, bot
from main import config
from states.admins import UpdateCompetition
from utils.db_api.commands import get_competitions
from utils.db_api.update_comp import *


@dp.callback_query_handler(text="change_comp_image_uz", chat_id=config.ADMINS)
async def add_competition(call: CallbackQuery):
    text = _("O'zbek tili uchun yangi rasmni kiriting.")
    await call.message.answer(text, reply_markup=await back_admin_main_menu())
    await UpdateCompetition.image_uz.set()


@dp.message_handler(state=UpdateCompetition.image_uz, chat_id=config.ADMINS, content_types=types.ContentTypes.PHOTO)
async def image_uz(message: types, state: FSMContext):
    if await update_comp_image_uz(message, message.photo[-1].file_id):
        text = _("Rasm yangilandi.")
        await message.answer(text, reply_markup=await admin_main_menu())
        await state.finish()
        competition = await get_competitions()
        await message.answer_photo(photo=competition["image_uz"], caption=competition["conditions_uz"],
                                   reply_markup=await update_comp_def("uz"))
    else:
        await state.finish()
        text = _("Botda nosozlik yuz berdi.")
        await message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(text="change_comp_image_ru", chat_id=config.ADMINS)
async def add_competition(call: CallbackQuery):
    text = _("Rus tili uchun yangi rasmni kiriting.")
    await call.message.answer(text, reply_markup=await back_admin_main_menu())
    await UpdateCompetition.image_ru.set()


@dp.message_handler(state=UpdateCompetition.image_ru, chat_id=config.ADMINS, content_types=types.ContentTypes.PHOTO)
async def image_uz(message: types.Message, state: FSMContext):
    if await update_comp_image_ru(message, message.photo[-1].file_id):
        text = _("Rasm yangilandi.")
        await message.answer(text, reply_markup=await admin_main_menu())
        await state.finish()
        competition = await get_competitions()
        await message.answer_photo(photo=competition["image_ru"], caption=competition["conditions_ru"],
                                   reply_markup=await update_comp_def("ru"))
    else:
        await state.finish()
        text = _("Botda nosozlik yuz berdi.")
        await message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(text="change_comp_conditions_uz", chat_id=config.ADMINS)
async def comp_conditions_change(call: CallbackQuery):
    text = _("O'zbek tili uchun yangi matnni kiriting.")
    await call.message.answer(text, reply_markup=await back_admin_main_menu())
    await UpdateCompetition.conditions_uz.set()


@dp.message_handler(state=UpdateCompetition.conditions_uz, chat_id=config.ADMINS)
async def image_uz(message: types.Message, state: FSMContext):
    if await update_comp_conditions_uz(message, message.text):
        text = _("Shartlar yangilandi.")
        await message.answer(text, reply_markup=await admin_main_menu())
        await state.finish()
        competition = await get_competitions()
        await message.answer_photo(photo=competition["image_uz"], caption=competition["conditions_uz"],
                                   reply_markup=await update_comp_def("uz"))
    else:
        await state.finish()
        text = _("Botda nosozlik yuz berdi.")
        await message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(text="change_comp_conditions_ru", chat_id=config.ADMINS)
async def comp_conditions_change(call: CallbackQuery):
    text = _("Rus tili uchun yangi matnni kiriting.")
    await call.message.answer(text, reply_markup=await back_admin_main_menu())
    await UpdateCompetition.conditions_ru.set()


@dp.message_handler(state=UpdateCompetition.conditions_ru, chat_id=config.ADMINS)
async def image_uz(message: types.Message, state: FSMContext):
    if await update_comp_conditions_ru(message, message.text):
        text = _("Shartlar yangilandi.")
        await message.answer(text, reply_markup=await admin_main_menu())
        await state.finish()
        competition = await get_competitions()
        await message.answer_photo(photo=competition["image_ru"], caption=competition["conditions_ru"],
                                   reply_markup=await update_comp_def("ru"))
    else:
        await state.finish()
        text = _("Botda nosozlik yuz berdi.")
        await message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(text="gifts_uz", chat_id=config.ADMINS)
async def comp_conditions_change(call: CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    competition = await get_competitions()
    await call.message.answer_photo(photo=competition["gifts_image_uz"], caption=competition["gifts_uz"],
                                    reply_markup=await update_comp_gifts_def("uz"))


@dp.callback_query_handler(text="gifts_ru", chat_id=config.ADMINS)
async def comp_conditions_change(call: CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    competition = await get_competitions()
    await call.message.answer_photo(photo=competition["gifts_image_ru"], caption=competition["gifts_ru"],
                                    reply_markup=await update_comp_gifts_def("ru"))


@dp.callback_query_handler(text="change_comp_gifts_image_uz", chat_id=config.ADMINS)
async def change_comp_gifts_image_uz(call: CallbackQuery):
    text = _("O'zbek tili uchun sovg'alarning yangi rasmini kiriting.")
    await call.message.answer(text, reply_markup=await back_admin_main_menu())
    await UpdateCompetition.gifts_image_uz.set()


@dp.message_handler(state=UpdateCompetition.gifts_image_uz, chat_id=config.ADMINS,
                    content_types=types.ContentTypes.PHOTO)
async def image_uz(message: types.Message, state: FSMContext):
    if await update_comp_gifts_image_uz(message, message.photo[-1].file_id):
        text = _("Rasm yangilandi.")
        await message.answer(text, reply_markup=await admin_main_menu())
        await state.finish()
        competition = await get_competitions()
        await message.answer_photo(photo=competition["gifts_image_uz"], caption=competition["gifts_uz"],
                                   reply_markup=await update_comp_gifts_def("uz"))
    else:
        await state.finish()
        text = _("Botda nosozlik yuz berdi.")
        await message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(text="change_comp_gifts_image_ru", chat_id=config.ADMINS)
async def change_comp_gifts_image_uz(call: CallbackQuery):
    text = _("Rus tili uchun sovg'alarning yangi rasmini kiriting.")
    await call.message.answer(text, reply_markup=await back_admin_main_menu())
    await UpdateCompetition.gifts_image_ru.set()


@dp.message_handler(state=UpdateCompetition.gifts_image_ru, chat_id=config.ADMINS,
                    content_types=types.ContentTypes.PHOTO)
async def image_uz(message: types.Message, state: FSMContext):
    if await update_comp_gifts_image_ru(message, message.photo[-1].file_id):
        text = _("Rasm yangilandi.")
        await message.answer(text, reply_markup=await admin_main_menu())
        await state.finish()
        competition = await get_competitions()
        await message.answer_photo(photo=competition["gifts_image_ru"], caption=competition["gifts_ru"],
                                   reply_markup=await update_comp_gifts_def("ru"))
    else:
        await state.finish()
        text = _("Botda nosozlik yuz berdi.")
        await message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(text="change_comp_gifts_uz", chat_id=config.ADMINS)
async def change_comp_gifts_image_uz(call: CallbackQuery):
    text = _("O'zbek uchun sovg'alarning yangi matnini kiriting.")
    await call.message.answer(text, reply_markup=await back_admin_main_menu())
    await UpdateCompetition.gifts_uz.set()


@dp.message_handler(state=UpdateCompetition.gifts_uz, chat_id=config.ADMINS)
async def image_uz(message: types.Message, state: FSMContext):
    if await update_comp_gifts_uz(message, message.text):
        text = _("Matn yangilandi.")
        await message.answer(text, reply_markup=await admin_main_menu())
        await state.finish()
        competition = await get_competitions()
        await message.answer_photo(photo=competition["gifts_image_uz"], caption=competition["gifts_uz"],
                                   reply_markup=await update_comp_gifts_def("uz"))
    else:
        await state.finish()
        text = _("Botda nosozlik yuz berdi.")
        await message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(text="change_comp_gifts_ru", chat_id=config.ADMINS)
async def change_comp_gifts_image_uz(call: CallbackQuery):
    text = _("O'zbek uchun sovg'alarning yangi matnini kiriting.")
    await call.message.answer(text, reply_markup=await back_admin_main_menu())
    await UpdateCompetition.gifts_ru.set()


@dp.message_handler(state=UpdateCompetition.gifts_ru, chat_id=config.ADMINS)
async def image_uz(message: types.Message, state: FSMContext):
    if await update_comp_gifts_ru(message, message.text):
        text = _("Matn yangilandi.")
        await message.answer(text, reply_markup=await admin_main_menu())
        await state.finish()
        competition = await get_competitions()
        await message.answer_photo(photo=competition["gifts_image_ru"], caption=competition["gifts_ru"],
                                   reply_markup=await update_comp_gifts_def("ru"))
    else:
        await state.finish()
        text = _("Botda nosozlik yuz berdi.")
        await message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(text="comp_uz", chat_id=config.ADMINS)
async def comp_uz_get(call: CallbackQuery):
    competition = await get_competitions()
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await call.message.answer_photo(competition['image_uz'], caption=competition["conditions_uz"],
                                    reply_markup=await update_comp_def("uz"))


@dp.callback_query_handler(text="comp_ru", chat_id=config.ADMINS)
async def comp_ru_get(call: CallbackQuery):
    competition = await get_competitions()
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await call.message.answer_photo(competition['image_ru'], caption=competition["conditions_ru"],
                                    reply_markup=await update_comp_def("ru"))


@dp.callback_query_handler(text="comp_gifts_uz", chat_id=config.ADMINS)
async def comp_conditions_change(call: CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    competition = await get_competitions()
    await call.message.answer_photo(photo=competition["gifts_image_uz"], caption=competition["gifts_uz"],
                                    reply_markup=await update_comp_gifts_def("uz"))


@dp.callback_query_handler(text="comp_gifts_ru", chat_id=config.ADMINS)
async def comp_conditions_change(call: CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    competition = await get_competitions()
    await call.message.answer_photo(photo=competition["gifts_image_ru"], caption=competition["gifts_ru"],
                                    reply_markup=await update_comp_gifts_def("ru"))


@dp.callback_query_handler(text="back_comp_menu_uz", chat_id=config.ADMINS)
async def comp_conditions_change(call: CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    competition = await get_competitions()
    await call.message.answer_photo(photo=competition["image_uz"], caption=competition["conditions_uz"],
                                    reply_markup=await update_comp_def("uz"))


@dp.callback_query_handler(text="back_comp_menu_ru", chat_id=config.ADMINS)
async def comp_conditions_change(call: CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    competition = await get_competitions()
    await call.message.answer_photo(photo=competition["image_ru"], caption=competition["conditions_ru"],
                                    reply_markup=await update_comp_def("ru"))
