from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

from filters.private_chat import IsPrivate
from keyboards.default.admins import back_admin_main_menu, admin_main_menu
from keyboards.inline.admins import contact_admin_def, add_contact_def
from loader import dp, _, bot
from main import config
from states.admins import AddContact, UpdateContact
from utils.db_api.commands import get_contact, add_contact
from utils.db_api.update_contact import *


@dp.message_handler(IsPrivate(), text=['Aloqalar ☎'], chat_id=config.ADMINS)
async def admin_profile(message: types.Message):
    contact = await get_contact()
    if contact:
        await message.answer_photo(
            contact['image_uz'], caption=contact["contact_uz"],
            reply_markup=await contact_admin_def("uz")
        )
    else:
        text = _("Bog'lanish malumotlari mavjud emas. Qo'shish uchun pastdagi tugmadan foydalaning.")
        await message.answer(text, reply_markup=await add_contact_def())


@dp.callback_query_handler(text="contact_uz", chat_id=config.ADMINS)
async def change_language(call: CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    contact = await get_contact()
    await call.message.answer_photo(
        contact['image_uz'], caption=contact["contact_uz"],
        reply_markup=await contact_admin_def("uz")
    )


@dp.callback_query_handler(text="contact_ru", chat_id=config.ADMINS)
async def change_language(call: CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    contact = await get_contact()
    await call.message.answer_photo(
        contact['image_ru'], caption=contact["contact_ru"],
        reply_markup=await contact_admin_def("ru")
    )


@dp.callback_query_handler(text="add_contact", chat_id=config.ADMINS)
async def change_language(call: CallbackQuery):
    text = _("O'zbek tili uchun kontank rasmini kiriting.")
    await call.message.answer(text, reply_markup=await back_admin_main_menu())
    await AddContact.image_uz.set()


@dp.message_handler(state=AddContact.image_uz, chat_id=config.ADMINS, content_types=types.ContentTypes.PHOTO)
async def contact_image_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "image_uz": message.photo[-1].file_id
    })

    text = _("Rus tili uchun kontank rasmini kiriting.")
    await message.answer(text, reply_markup=ReplyKeyboardRemove())
    await AddContact.image_ru.set()


@dp.message_handler(state=AddContact.image_ru, chat_id=config.ADMINS, content_types=types.ContentTypes.PHOTO)
async def contact_image_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "image_ru": message.photo[-1].file_id
    })

    text = _("O'zbek tili uchun kontank matnini kiriting.")
    await message.answer(text, reply_markup=ReplyKeyboardRemove())
    await AddContact.contact_uz.set()


@dp.message_handler(state=AddContact.contact_uz, chat_id=config.ADMINS)
async def contact_image_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "contact_uz": message.text
    })

    text = _("Rus tili uchun kontank matnini kiriting.")
    await message.answer(text, reply_markup=ReplyKeyboardRemove())
    await AddContact.contact_ru.set()


@dp.message_handler(state=AddContact.contact_ru, chat_id=config.ADMINS)
async def contact_image_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "contact_ru": message.text
    })

    if await add_contact(message, state):
        text = _("Kontakt ma'lumotlari qo'shildi.")
    else:
        text = _("Botda nosozlik yuz berdi.")

    await state.finish()
    await message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(text="change_contact_image_uz", chat_id=config.ADMINS)
async def change_contact_image_uz(call: CallbackQuery):
    text = _("O'zbek tili uchun kontank yangi rasmini kiriting.")
    await call.message.answer(text, reply_markup=await back_admin_main_menu())
    await UpdateContact.image_uz.set()


@dp.message_handler(state=UpdateContact.image_uz, chat_id=config.ADMINS, content_types=types.ContentTypes.PHOTO)
async def contact_image_uz(message: types.Message, state: FSMContext):
    if await update_contact_image_uz(message, message.photo[-1].file_id):
        await state.finish()
        text = _("Rasm yangilandi.")
        await message.answer(text, reply_markup=await admin_main_menu())
        contact = await get_contact()

        await message.answer_photo(
            contact['image_uz'], caption=contact["contact_uz"],
            reply_markup=await contact_admin_def("uz")
        )
    else:
        await state.finish()
        text = _("Botda nosozlik yuz berdi.")
        await message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(text="change_contact_image_ru", chat_id=config.ADMINS)
async def change_contact_image_ru(call: CallbackQuery):
    text = _("Rus tili uchun kontank yangi rasmini kiriting.")
    await call.message.answer(text, reply_markup=await back_admin_main_menu())
    await UpdateContact.image_ru.set()


@dp.message_handler(state=UpdateContact.image_ru, chat_id=config.ADMINS, content_types=types.ContentTypes.PHOTO)
async def contact_image_ru(message: types.Message, state: FSMContext):
    if await update_contact_image_ru(message, message.photo[-1].file_id):
        await state.finish()
        text = _("Rasm yangilandi.")
        await message.answer(text, reply_markup=await admin_main_menu())
        contact = await get_contact()

        await message.answer_photo(
            contact['image_ru'], caption=contact["contact_ru"],
            reply_markup=await contact_admin_def("ru")
        )
    else:
        await state.finish()
        text = _("Botda nosozlik yuz berdi.")
        await message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(text="change_contact_text_uz", chat_id=config.ADMINS)
async def change_contact_contact_uz(call: CallbackQuery):
    text = _("O'zbek tili uchun kontank yangi matnini kiriting.")
    await call.message.answer(text, reply_markup=await back_admin_main_menu())
    await UpdateContact.contact_uz.set()


@dp.message_handler(state=UpdateContact.contact_uz, chat_id=config.ADMINS)
async def contact_contact_uz(message: types.Message, state: FSMContext):
    if await update_contact_contact_uz(message, message.text):
        await state.finish()
        text = _("Rasm yangilandi.")
        await message.answer(text, reply_markup=await admin_main_menu())
        contact = await get_contact()

        await message.answer_photo(
            contact['image_uz'], caption=contact["contact_uz"],
            reply_markup=await contact_admin_def("uz")
        )
    else:
        await state.finish()
        text = _("Botda nosozlik yuz berdi.")
        await message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(text="change_contact_text_ru", chat_id=config.ADMINS)
async def change_contact_contact_ru(call: CallbackQuery):
    text = _("Rus tili uchun kontank yangi matnini kiriting.")
    await call.message.answer(text, reply_markup=await back_admin_main_menu())
    await UpdateContact.contact_ru.set()


@dp.message_handler(state=UpdateContact.contact_ru, chat_id=config.ADMINS)
async def contact_contact_uz(message: types.Message, state: FSMContext):
    if await update_contact_contact_ru(message, message.text):
        await state.finish()
        text = _("Rasm yangilandi.")
        await message.answer(text, reply_markup=await admin_main_menu())
        contact = await get_contact()

        await message.answer_photo(
            contact['image_ru'], caption=contact["contact_ru"],
            reply_markup=await contact_admin_def("ru")
        )
    else:
        await state.finish()
        text = _("Botda nosozlik yuz berdi.")
        await message.answer(text, reply_markup=await admin_main_menu())
