from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

from filters.private_chat import IsPrivate
from keyboards.default.admins import back_admin_main_menu, admin_main_menu
from keyboards.inline.admins import send_post_def, send_admin_post_all
from loader import dp, _, bot
from main import config
from states.admins import SendPost
from utils.db_api.commands import get_users


@dp.message_handler(IsPrivate(), text=["Post Jo'natish ⏫", "Опубликовать Отправить ⏫"], chat_id=config.ADMINS)
async def send_post(message: types.Message):
    text = _("Post uchun rasmni kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await SendPost.image.set()


@dp.message_handler(state=SendPost.image, chat_id=config.ADMINS, content_types=types.ContentTypes.PHOTO)
async def send_post(message: types.Message, state: FSMContext):
    await state.update_data({
        "image": message.photo[-1].file_id
    })
    text = _("Post uchun matnni kiriting.")
    await message.answer(text, reply_markup=ReplyKeyboardRemove())
    await SendPost.text.set()


@dp.message_handler(state=SendPost.text, chat_id=config.ADMINS)
async def send_post(message: types.Message, state: FSMContext):
    await state.update_data({
        "text": message.text
    })
    text = _("Post uchun pastki havolani kiriting.")
    await message.answer(text, reply_markup=ReplyKeyboardRemove())
    await SendPost.link.set()


@dp.message_handler(state=SendPost.link, chat_id=config.ADMINS)
async def send_post(message: types.Message, state: FSMContext):
    await state.update_data({
        "link": message.text
    })
    text = _("Post uchun pastki tugmadagi matnni kiriting.")
    await message.answer(text, reply_markup=ReplyKeyboardRemove())
    await SendPost.button_text.set()


@dp.message_handler(state=SendPost.button_text, chat_id=config.ADMINS)
async def send_post(message: types.Message, state: FSMContext):
    await state.update_data({
        "button_text": message.text
    })
    data = await state.get_data()

    await message.answer_photo(data.get("image"), caption=data.get("text"),
                               reply_markup=await send_admin_post_all(data.get("button_text"), data.get("link")))
    answer = "Jo'natishni hohlaysizmi ?"
    await message.answer(answer, reply_markup=await send_post_def())
    await SendPost.waiting.set()


@dp.callback_query_handler(state=SendPost.waiting, text="send_post_yes", chat_id=config.ADMINS)
async def send_post_yes(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    users = await get_users()
    try:
        for user in users:
            await bot.send_photo(chat_id=user["telegram_id"], photo=data.get("image"), caption=data.get("text"),
                                 reply_markup=await send_admin_post_all(data.get("button_text"), data.get("link")))

        await state.finish()
        text = _("Habar barcha foydalanuvchilarga jo'natildi.")
        await call.message.answer(text, reply_markup=await admin_main_menu())
    except Exception as exc:
        print(exc)
        await state.finish()
        text = _("Botda nosozlik yuz berdi.")
        await call.message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(state=SendPost.waiting, text="send_post_no", chat_id=config.ADMINS)
async def send_post_yes(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()
    text = _("Habar bekor qilindi.")
    await call.message.answer(text, reply_markup=await admin_main_menu())
