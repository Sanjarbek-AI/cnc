from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

from keyboards.default.admins import back_admin_main_menu, admin_main_menu
from keyboards.inline.admin_comp import update_comp_def, comp_yes_or_no
from keyboards.inline.admins import new_comp_add, new_comp_ask, callback_comp_ask
from loader import dp, _, bot
from main import config
from states.admins import AddCompetition
from utils.db_api.commands import *
from utils.db_api.update_comp import update_comp_all_status


@dp.message_handler(text=['Конкурс 🎁', 'Konkurs 🎁'], chat_id=config.ADMINS)
async def select_language(message: types):
    user = await get_user(message.from_user.id)
    competition = await get_competitions()
    if competition and user:
        await message.answer_photo(photo=competition["image_uz"], caption=competition["conditions_uz"],
                                   reply_markup=await update_comp_def(user["language"]))
    else:
        text = _("Hozirda faol konkurslar mavjud emas. Yangi qo'shish uchun pastdagi tugmadan foydalaning.")
        await message.answer(text, reply_markup=await new_comp_add())


@dp.callback_query_handler(text="add_comp", chat_id=config.ADMINS)
async def add_competition(call: CallbackQuery):
    text = _("O'zbek tili uchun konkursni rasmini yuboring.")
    await call.message.answer(text, reply_markup=await back_admin_main_menu())
    await AddCompetition.image_uz.set()


@dp.message_handler(state=AddCompetition.image_uz, chat_id=config.ADMINS, content_types=types.ContentTypes.PHOTO)
async def image_uz(message: types, state: FSMContext):
    await state.update_data({
        "image_uz": message.photo[-1].file_id
    })
    text = _("Rus tili uchun konkursni rasmini yuboring.")
    await message.answer(text, reply_markup=ReplyKeyboardRemove())
    await AddCompetition.image_ru.set()


@dp.message_handler(state=AddCompetition.image_ru, chat_id=config.ADMINS, content_types=types.ContentTypes.PHOTO)
async def image_ru(message: types, state: FSMContext):
    await state.update_data({
        "image_ru": message.photo[-1].file_id
    })
    text = _("O'zbek tili uchun konkurs shartlarini yuboring.")
    await message.answer(text, reply_markup=ReplyKeyboardRemove())
    await AddCompetition.conditions_uz.set()


@dp.message_handler(state=AddCompetition.conditions_uz, chat_id=config.ADMINS)
async def conditions_uz(message: types, state: FSMContext):
    await state.update_data({
        "conditions_uz": message.text
    })
    text = _("Rus tili uchun konkurs shartlarini yuboring.")
    await message.answer(text, reply_markup=ReplyKeyboardRemove())
    await AddCompetition.conditions_ru.set()


@dp.message_handler(state=AddCompetition.conditions_ru, chat_id=config.ADMINS)
async def conditions_ru(message: types, state: FSMContext):
    await state.update_data({
        "conditions_ru": message.text
    })
    text = _("O'zbek tili uchun sovg'alarni rasmini jo'nating.")
    await message.answer(text, reply_markup=ReplyKeyboardRemove())
    await AddCompetition.gifts_image_uz.set()


@dp.message_handler(state=AddCompetition.gifts_image_uz, chat_id=config.ADMINS, content_types=types.ContentTypes.PHOTO)
async def gifts_image_uz(message: types, state: FSMContext):
    await state.update_data({
        "gifts_image_uz": message.photo[-1].file_id
    })
    text = _("Rus tili uchun sovg'alarni rasmini jo'nating.")
    await message.answer(text, reply_markup=ReplyKeyboardRemove())
    await AddCompetition.gifts_image_ru.set()


@dp.message_handler(state=AddCompetition.gifts_image_ru, chat_id=config.ADMINS, content_types=types.ContentTypes.PHOTO)
async def gifts_image_ru(message: types, state: FSMContext):
    await state.update_data({
        "gifts_image_ru": message.photo[-1].file_id
    })
    text = _("O'zbek tili uchun sovg'alarni matnini yuboring.")
    await message.answer(text, reply_markup=ReplyKeyboardRemove())
    await AddCompetition.gifts_uz.set()


@dp.message_handler(state=AddCompetition.gifts_uz, chat_id=config.ADMINS)
async def gifts_uz(message: types, state: FSMContext):
    await state.update_data({
        "gifts_uz": message.text
    })
    text = _("Rus tili uchun sovg'alarni matnini yuboring.")
    await message.answer(text, reply_markup=ReplyKeyboardRemove())
    await AddCompetition.gifts_ru.set()


@dp.message_handler(state=AddCompetition.gifts_ru, chat_id=config.ADMINS)
async def gifts_ru(message: types, state: FSMContext):
    await state.update_data({
        "gifts_ru": message.text
    })
    new_comp = await add_comp(message, state)
    if new_comp:
        await state.finish()
        text = _("Konkursni boshlashni hohlaysizmi ?")
        await message.answer(text, reply_markup=await new_comp_ask(new_comp))
    else:
        text = _("Botda xatolik yuz berdi !!!")
        await message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(callback_comp_ask.filter(act="comp_yes"), chat_id=config.ADMINS)
async def yes_competition(call: CallbackQuery, callback_data: dict):
    comp_id = int(callback_data.get("comp_id"))
    if await update_comp_status(call.message, comp_id):
        text = _("Konkurs boshlandi.")
        await call.message.answer(text, reply_markup=await admin_main_menu())
    else:
        text = _("Botda xatolik yuz berdi !!!")
        await call.message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(text="comp_no", chat_id=config.ADMINS)
async def no_competition(call: CallbackQuery):
    text = _("Konkurs bekor qilindi.")
    await call.message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(text="stop_comp", chat_id=config.ADMINS)
async def stop_comp(call: CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    text = _("Konkursni yakunlashni hohlaysizmi ?")
    await call.message.answer(text, reply_markup=await comp_yes_or_no())


@dp.callback_query_handler(text="stop_comp_yes", chat_id=config.ADMINS)
async def stop_comp(call: CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    if await update_comp_all_status(call.message):
        text = _("Konkurs yakunlandi.")
    else:
        text = _("Botda nosozlik yuz berdi.")

    await call.message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(text="stop_comp_no", chat_id=config.ADMINS)
async def stop_comp(call: CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    text = _("Konkurs to'xtatilmadi.")
    await call.message.answer(text, reply_markup=await admin_main_menu())
