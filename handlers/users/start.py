from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

from filters.private_chat import IsPrivate
from keyboards.default.admins import contact_def, admin_main_menu
from keyboards.default.users import users_main_menu
from keyboards.inline.admins import languages
from keyboards.inline.locations import locations_def
from keyboards.inline.users import comp_menu_def, post_like
from loader import dp, _
from main import config
from main.config import CHANNELS
from states.admins import Language
from states.users import Register
from utils.db_api.commands import register, get_competitions, get_user, register_start, get_user_active
from utils.db_api.user_posts import get_comp_user, get_user_post
from utils.misc.checking_user_membership import check


@dp.message_handler(IsPrivate(), chat_id=config.ADMINS, commands="start")
async def start_admin(message: types.Message):
    if await get_user(message.from_user.id):
        text = _("Assalomu alaykum. Siz bot boshqaruvchilaridan birisiz. 😊")
        await message.answer(text, reply_markup=await admin_main_menu())
    else:
        text = "Assalomu alaykum. Siz bot boshqaruvchilaridan birisiz. \nIltimos tilni tanlang. 😊"
        await message.answer(text, reply_markup=languages)
        await Language.select.set()


@dp.message_handler(IsPrivate(), commands="start")
async def start_users(message: types.Message):
    args = message.get_args()
    if args:
        user = await get_user(message.from_user.id)
        if not user:
            await register_start(message)

        args = int(args)

        post_data = await get_user_post(args)
        if post_data:
            link = f"https://t.me/cncele_bot?start={args}"
            await message.answer_photo(photo=post_data["images"][0],
                                       reply_markup=await post_like(args, link))
        else:
            text = "Xa'to havoladan foydalandingiz !"
            await message.answer(text, reply_markup=await users_main_menu())
    else:
        user = await get_user_active(message.from_user.id)
        if user:
            text = _("Siz ro'yxatdan o'tgansiz.")
            await message.answer(text, reply_markup=await users_main_menu())
        else:
            text = "Iltimos, tilni tanlang. 🇺🇿 \nВыберите язык. 🇷🇺"
            await message.answer(text, reply_markup=languages)
            await Register.language.set()


@dp.callback_query_handler(state=Register.language)
async def language(call: CallbackQuery, state: FSMContext):
    await state.update_data({
        "language": call.data,
    })

    text = "Iltimos, Ism va Familiayangizni kiriting."
    await Register.full_name.set()
    await call.message.answer(text, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=Register.full_name)
async def full_name(message: types.Message, state: FSMContext):
    await state.update_data({
        "full_name": message.text,
    })

    text = "Iltimos, Telefon raqamingizni kiriting."
    await message.answer(text, reply_markup=await contact_def())
    await Register.phone_number.set()


# @dp.message_handler(state=Register.phone_number)
# async def get_phone_number(message: types.Message, state: FSMContext):
#     if await is_valid(message.text):
#         await state.update_data({
#             "phone_number": message.text
#         })
#         text = "Asosiy ish hududingizni tanlang."
#         await message.answer(text, reply_markup=await locations_def())
#         await Register.location.set()
#     else:
#         text = "Iltimos telefon raqamingizni tog'ri kiriting !"
#         await message.answer(text)

@dp.message_handler(state=Register.phone_number)
async def get_phone_number(message: types.Message, state: FSMContext):
    text = "Iltimos tugmadan foydalaning."
    await message.answer(text, reply_markup=await contact_def())


@dp.message_handler(content_types=types.ContentTypes.CONTACT, state=Register.phone_number)
async def get_phone_number(message: types.Message, state: FSMContext):
    await state.update_data({
        "phone_number": message.contact.phone_number
    })

    text = "Asosiy ish hududingizni tanlang."
    await message.answer(text, reply_markup=await locations_def())
    await Register.location.set()


@dp.callback_query_handler(state=Register.location)
async def location(call: CallbackQuery, state: FSMContext):
    await state.update_data({
        "location": call.data,
        "telegram_id": call.from_user.id,
    })

    registered_user = await register(call.message, state)
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


@dp.callback_query_handler(text=["checking"])
async def checking(call: CallbackQuery):
    comp = await get_competitions()
    user = await get_user(call.from_user.id)
    lang = ""
    if user:
        lang = user["language"]

    for channel in CHANNELS:
        status = await check(call.from_user.id, channel)
        if status:
            if lang == "uz":
                answer = _("Kanalga a'zo bo'lgansiz. ✅")
            else:
                answer = _("Вы являетесь участником канала. ✅")
        else:
            if lang == "uz":
                answer = _("Kanalga a'zo bo'lmagansiz. ❌")
            else:
                answer = _("Вы не являетесь участником канала. ❌")
        await call.message.answer(answer, reply_markup=await users_main_menu())

    if await get_comp_user(call.from_user.id, comp["id"]):
        if lang == "uz":
            answer = _("Rasm yuborilgan. ✅")
        else:
            answer = _("Картинка отправлена. ✅")
    else:
        if lang == "uz":
            answer = _("Rasm yuborilmagan. ❌")
        else:
            answer = _("Картинка не отправлена. ❌")
    await call.message.answer(answer, reply_markup=await users_main_menu())
