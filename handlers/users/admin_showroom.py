from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery

from keyboards.default.admins import back_admin_main_menu, back_showroom_menu, admin_main_menu
from keyboards.inline.admin_showroom import *
from keyboards.inline.users import showroom_menu_user
from loader import dp, _, bot
from main import config
from states.admins import UpdateShowroom, AddShowroom
from utils.db_api.commands import *
from utils.db_api.update_showrooms import *


@dp.message_handler(text=["Shovrumlar 🏣", "Mагазины 🏣"], chat_id=config.ADMINS)
async def select_language(message: types):
    showroom_all = await get_showrooms()
    if showroom_all:
        text = _("Shovrumlar menyusi.")
        await message.answer(text, reply_markup=await showrooms_keyboard("uz"))
    else:
        text = _("Hozirda shovrumlar mavjud emas. Yangi qo'shish uchun pastdagi tugmadan foydalaning.")
        await message.answer(text, reply_markup=await add_showroom_def())


@dp.callback_query_handler(text="add_showroom", chat_id=config.ADMINS)
async def comp_conditions_change(call: CallbackQuery):
    text = _("O'zbek tili uchun shovrumning rasmini kiriting.")
    await call.message.answer(text, reply_markup=await back_admin_main_menu())
    await AddShowroom.image_uz.set()


@dp.message_handler(state=AddShowroom.image_uz, chat_id=config.ADMINS, content_types=types.ContentTypes.PHOTO)
async def showrooms_menu_back(message: types.Message, state: FSMContext):
    await state.update_data({
        "image_uz": message.photo[-1].file_id
    })
    text = _("Rus tili uchun shovrum rasmini kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddShowroom.image_ru.set()


@dp.message_handler(state=AddShowroom.image_ru, chat_id=config.ADMINS, content_types=types.ContentTypes.PHOTO)
async def showrooms_menu_back(message: types.Message, state: FSMContext):
    await state.update_data({
        "image_ru": message.photo[-1].file_id
    })
    text = _("O'zbek tili uchun shovrum matnini kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddShowroom.info_uz.set()


@dp.message_handler(state=AddShowroom.info_uz, chat_id=config.ADMINS)
async def showrooms_menu_back(message: types.Message, state: FSMContext):
    await state.update_data({
        "info_uz": message.text
    })
    text = _("Rus tili uchun shovrum matnini kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddShowroom.info_ru.set()


@dp.message_handler(state=AddShowroom.info_ru, chat_id=config.ADMINS)
async def showrooms_menu_back(message: types.Message, state: FSMContext):
    await state.update_data({
        "info_ru": message.text
    })
    text = _("O'zbek tili uchun shovrum nomini kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddShowroom.name_uz.set()


@dp.message_handler(state=AddShowroom.name_uz, chat_id=config.ADMINS)
async def showrooms_menu_back(message: types.Message, state: FSMContext):
    await state.update_data({
        "name_uz": message.text
    })
    text = _("Rus tili uchun shovrum nomini kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddShowroom.name_ru.set()


@dp.message_handler(state=AddShowroom.name_ru, chat_id=config.ADMINS)
async def showrooms_menu_back(message: types.Message, state: FSMContext):
    await state.update_data({
        "name_ru": message.text
    })
    text = _("Shovrumning xaritadagi linkini kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddShowroom.link.set()


@dp.message_handler(state=AddShowroom.link, chat_id=config.ADMINS)
async def showrooms_menu_back(message: types.Message, state: FSMContext):
    await state.update_data({
        "link": message.text
    })
    if await add_showroom(message, state):
        text = _("Shovrumning qo'shildi.")
    else:
        text = _("Botda nosozlik yuz berdi.")
    await message.answer(text, reply_markup=await admin_main_menu())
    await state.finish()


@dp.callback_query_handler(text="back_showroom_menu", chat_id=config.ADMINS)
async def showrooms_menu_back(call: CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    text = _("Shovrumlar menyusi.")
    await call.message.answer(text, reply_markup=await showrooms_keyboard("uz"))


@dp.callback_query_handler(change_showroom.filter(act="change_sh_image"), chat_id=config.ADMINS)
async def showrooms_menu_back(call: CallbackQuery, callback_data: dict, state: FSMContext):
    sh_id = int(callback_data.get("sh_id"))
    lang = callback_data.get("lang")

    await state.update_data({
        "sh_id": sh_id
    })

    if lang == "uz":
        text = _("O'zbek tili uchun shovrumning yangi rasmini kiriting")
        await call.message.answer(text, reply_markup=await back_showroom_menu())
        await UpdateShowroom.image_uz.set()
    else:
        text = _("Rus tili uchun shovrumning yangi rasmini kiriting")
        await call.message.answer(text, reply_markup=await back_showroom_menu())
        await UpdateShowroom.image_ru.set()


@dp.message_handler(state=UpdateShowroom.image_uz, chat_id=config.ADMINS, content_types=types.ContentTypes.PHOTO)
async def image_uz(message: types, state: FSMContext):
    data = await state.get_data()
    sh_id = int(data.get("sh_id"))
    if await update_showroom_image_uz(message, message.photo[-1].file_id, sh_id):
        text = _("Rasm yangilandi.")
        await message.answer(text, reply_markup=await admin_main_menu())
        await state.finish()
        showroom = await get_showroom(sh_id)
        await message.answer_photo(photo=showroom["image_uz"], caption=showroom["info_uz"],
                                   reply_markup=await update_showroom_def("uz", sh_id))
    else:
        await state.finish()
        text = _("Botda nosozlik yuz berdi.")
        await message.answer(text, reply_markup=await admin_main_menu())


@dp.message_handler(state=UpdateShowroom.image_ru, chat_id=config.ADMINS, content_types=types.ContentTypes.PHOTO)
async def image_uz(message: types, state: FSMContext):
    data = await state.get_data()
    sh_id = int(data.get("sh_id"))
    if await update_showroom_image_ru(message, message.photo[-1].file_id, sh_id):
        text = _("Rasm yangilandi.")
        await message.answer(text, reply_markup=await admin_main_menu())
        await state.finish()
        showroom = await get_showroom(sh_id)
        await message.answer_photo(photo=showroom["image_ru"], caption=showroom["info_ru"],
                                   reply_markup=await update_showroom_def("ru", sh_id))
    else:
        await state.finish()
        text = _("Botda nosozlik yuz berdi.")
        await message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(change_showroom.filter(act="change_sh_text"), chat_id=config.ADMINS)
async def showrooms_menu_back(call: CallbackQuery, callback_data: dict, state: FSMContext):
    sh_id = int(callback_data.get("sh_id"))
    lang = callback_data.get("lang")

    await state.update_data({
        "sh_id": sh_id
    })

    if lang == "uz":
        text = _("O'zbek tili uchun shovrumning yangi matnini kiriting")
        await call.message.answer(text, reply_markup=await back_showroom_menu())
        await UpdateShowroom.info_uz.set()
    else:
        text = _("Rus tili uchun shovrumning yangi matnini kiriting")
        await call.message.answer(text, reply_markup=await back_showroom_menu())
        await UpdateShowroom.info_ru.set()


@dp.message_handler(state=UpdateShowroom.info_uz, chat_id=config.ADMINS)
async def image_uz(message: types, state: FSMContext):
    data = await state.get_data()
    sh_id = int(data.get("sh_id"))
    if await update_showroom_info_uz(message, message.text, sh_id):
        text = _("Matn yangilandi.")
        await message.answer(text, reply_markup=await admin_main_menu())
        await state.finish()
        showroom = await get_showroom(sh_id)
        await message.answer_photo(photo=showroom["image_uz"], caption=showroom["info_uz"],
                                   reply_markup=await update_showroom_def("uz", sh_id))
    else:
        await state.finish()
        text = _("Botda nosozlik yuz berdi.")
        await message.answer(text, reply_markup=await admin_main_menu())


@dp.message_handler(state=UpdateShowroom.info_ru, chat_id=config.ADMINS)
async def image_uz(message: types, state: FSMContext):
    data = await state.get_data()
    sh_id = int(data.get("sh_id"))
    if await update_showroom_info_ru(message, message.text, sh_id):
        text = _("Matn yangilandi.")
        await message.answer(text, reply_markup=await admin_main_menu())
        await state.finish()
        showroom = await get_showroom(sh_id)
        await message.answer_photo(photo=showroom["image_ru"], caption=showroom["info_ru"],
                                   reply_markup=await update_showroom_def("ru", sh_id))
    else:
        await state.finish()
        text = _("Botda nosozlik yuz berdi.")
        await message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(change_showroom.filter(act="change_sh_name"), chat_id=config.ADMINS)
async def showrooms_menu_back(call: CallbackQuery, callback_data: dict, state: FSMContext):
    sh_id = int(callback_data.get("sh_id"))
    lang = callback_data.get("lang")

    await state.update_data({
        "sh_id": sh_id
    })

    if lang == "uz":
        text = _("O'zbek tili uchun shovrumning yangi nomini kiriting")
        await call.message.answer(text, reply_markup=await back_showroom_menu())
        await UpdateShowroom.name_uz.set()
    else:
        text = _("Rus tili uchun shovrumning yangi nomini kiriting")
        await call.message.answer(text, reply_markup=await back_showroom_menu())
        await UpdateShowroom.name_ru.set()


@dp.message_handler(state=UpdateShowroom.name_uz, chat_id=config.ADMINS)
async def image_uz(message: types, state: FSMContext):
    data = await state.get_data()
    sh_id = int(data.get("sh_id"))
    if await update_showroom_name_uz(message, message.text, sh_id):
        text = _("Nom yangilandi.")
        await message.answer(text, reply_markup=await admin_main_menu())
        await state.finish()
        showroom = await get_showroom(sh_id)
        await message.answer_photo(photo=showroom["image_uz"], caption=showroom["info_uz"],
                                   reply_markup=await update_showroom_def("uz", sh_id))
    else:
        await state.finish()
        text = _("Botda nosozlik yuz berdi.")
        await message.answer(text, reply_markup=await admin_main_menu())


@dp.message_handler(state=UpdateShowroom.name_ru, chat_id=config.ADMINS)
async def image_ru(message: types, state: FSMContext):
    data = await state.get_data()
    sh_id = int(data.get("sh_id"))
    if await update_showroom_name_ru(message, message.text, sh_id):
        text = _("Nom yangilandi.")
        await message.answer(text, reply_markup=await admin_main_menu())
        await state.finish()
        showroom = await get_showroom(sh_id)
        await message.answer_photo(photo=showroom["image_ru"], caption=showroom["info_ru"],
                                   reply_markup=await update_showroom_def("ru", sh_id))
    else:
        await state.finish()
        text = _("Botda nosozlik yuz berdi.")
        await message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(change_showroom.filter(act="change_sh_link"), chat_id=config.ADMINS)
async def showrooms_menu_back(call: CallbackQuery, callback_data: dict, state: FSMContext):
    sh_id = int(callback_data.get("sh_id"))

    await state.update_data({
        "sh_id": sh_id
    })

    text = _("Shovrum uchun yangi manzil linkini kiriting")
    await call.message.answer(text, reply_markup=await back_showroom_menu())
    await UpdateShowroom.link.set()


@dp.message_handler(state=UpdateShowroom.link, chat_id=config.ADMINS)
async def image_uz(message: types, state: FSMContext):
    data = await state.get_data()
    sh_id = int(data.get("sh_id"))
    if await update_showroom_link(message, message.text, sh_id):
        text = _("Manzil yangilandi.")
        await message.answer(text, reply_markup=await admin_main_menu())
        await state.finish()
        showroom = await get_showroom(sh_id)
        await message.answer_photo(photo=showroom["image_uz"], caption=showroom["info_uz"],
                                   reply_markup=await update_showroom_def("uz", sh_id))
    else:
        await state.finish()
        text = _("Botda nosozlik yuz berdi.")
        await message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(text="showrooms_uz", chat_id=config.ADMINS)
async def showrooms_menu(call: CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    text = _("Shovrumlar menyusi.")
    await call.message.answer(text, reply_markup=await showrooms_keyboard("uz"))


@dp.callback_query_handler(text="showrooms_ru", chat_id=config.ADMINS)
async def showrooms_menu(call: CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    text = _("Shovrumlar menyusi.")
    await call.message.answer(text, reply_markup=await showrooms_keyboard("ru"))


@dp.callback_query_handler(change_showroom.filter(act="change_language"), chat_id=config.ADMINS)
async def showrooms_menu_back(call: CallbackQuery, callback_data: dict):
    sh_id = int(callback_data.get("sh_id"))
    lang = callback_data.get("lang")

    if lang == "uz":
        showroom = await get_showroom(sh_id)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await call.message.answer_photo(photo=showroom["image_uz"], caption=showroom["info_uz"],
                                        reply_markup=await update_showroom_def("ru", sh_id))
    else:
        showroom = await get_showroom(sh_id)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await call.message.answer_photo(photo=showroom["image_ru"], caption=showroom["info_ru"],
                                        reply_markup=await update_showroom_def("uz", sh_id))


@dp.callback_query_handler(chat_id=config.ADMINS)
async def showroom_get(call: CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    callback_data = call.data.split("_")

    if callback_data[0] == "showroom":
        lang = callback_data[1]
        showroom = await get_showroom(int(callback_data[2]))

        await call.message.answer_photo(
            photo=showroom['image_uz'] if lang == "uz" else showroom['image_ru'],
            caption=showroom['info_uz'] if lang == "uz" else showroom['info_ru'],
            reply_markup=await update_showroom_def(lang, showroom['id']))
    else:
        pass


@dp.callback_query_handler()
async def showroom_get(call: CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    callback_data = call.data.split("_")

    if callback_data[0] == "showroom":
        showroom = await get_showroom(int(callback_data[2]))
        user = await get_user(call.from_user.id)
        if user["language"] == "uz":
            await call.message.answer_photo(
                photo=showroom['image_uz'],
                caption=showroom['info_uz'],
                reply_markup=await showroom_menu_user(showroom["location_link"]))
        else:
            await call.message.answer_photo(
                photo=showroom['image_ru'],
                caption=showroom['info_ru'],
                reply_markup=await showroom_menu_user(showroom["location_link"]))
    else:
        pass
