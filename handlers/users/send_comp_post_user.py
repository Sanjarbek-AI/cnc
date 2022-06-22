from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

from keyboards.default.users import users_main_menu
from keyboards.inline.admins import languages
from keyboards.inline.users import admin_answer_def, callback_admin_answer, post_like
from loader import dp, _, bot
from main.config import CHANNELS
from main.constants import UserPostStatus
from states.users import UserSendPost, RegisterLike
from utils.db_api.commands import get_competitions, get_user, get_user_active
from utils.db_api.user_posts import add_posts, get_comp_user, update_user_post_status, get_user_post, \
    get_user_post_by_id, delete_user_post_admin_no
from utils.misc.checking_user_membership import check


@dp.callback_query_handler(text="send_comp_post")
async def send_post(call: CallbackQuery):
    user = await get_user_active(call.from_user.id)
    if not user:
        text = "Iltimos, tilni tanlang. 🇺🇿 \nВыберите язык. 🇷🇺"
        await call.message.answer(text, reply_markup=languages)
        await RegisterLike.language.set()
    else:
        for channel in CHANNELS:
            status = await check(call.from_user.id, channel)
            if status:
                comp = await get_competitions()
                if await get_comp_user(call.from_user.id, comp["id"]):
                    text = _("Siz rasmlarni yuborgansiz. ✅")
                    await call.message.answer(text, reply_markup=await users_main_menu())
                else:
                    text = _("Eng yaxshi ishlaringizdan na'muna jo'nating (rasm sifatida).")
                    await call.message.answer(text, reply_markup=ReplyKeyboardRemove())
                    await UserSendPost.images.set()
            else:
                text = _("Avval kanalga a'zo bo'ling.")
                await call.message.answer(text, reply_markup=await users_main_menu())


@dp.message_handler(state=UserSendPost.images, content_types=types.ContentTypes.PHOTO)
async def get_images(message: types, state: FSMContext):
    images_list = list()
    try:
        images_list.extend(
            [message.photo[-1].file_id]
        )

        await state.update_data({
            "images": images_list
        })

        text = _("Yuborgan rasmdagi ishingizga qisqacha ta'rif bering.")
        await message.answer(text)
        await UserSendPost.text.set()

    except Exception as exc:
        print(exc)


@dp.message_handler(state=UserSendPost.text)
async def get_text(message: types, state: FSMContext):
    comp = await get_competitions()
    await state.update_data({
        "text": message.text,
        "comp_id": comp["id"],
    })
    await add_posts(message, state)
    post_data = await get_comp_user(message.from_user.id, comp["id"])
    if post_data:
        user = await get_user(message.from_user.id)
        caption = post_data["description"] + '\n\n' + user["phone_number"] + "\n" + user["full_name"]
        await bot.send_photo(
            chat_id="-1001538496752", photo=post_data["images"][0], caption=caption,
            reply_markup=await admin_answer_def(post_data["id"]))
        # await bot.send_photo(
        #     chat_id="-1001640626557", photo=post_data["images"][0], caption=caption,
        #     reply_markup=await admin_answer_def(post_data["id"]))

        text = _(
            "Konkursda ishtirok etish uchun so'rovingiz qabul qilindi. Iltimos kuting,  tez orada sizga ovoz (❤)"
            " yig'ish uchun Havola yuboriladi.")
    else:
        text = _("Botda nosozlik yuz berdi")

    await message.answer(text, reply_markup=await users_main_menu())
    await state.finish()


@dp.callback_query_handler(callback_admin_answer.filter(act="admin_answer_yes"))
async def admin_answer_yes(call: types.CallbackQuery, callback_data: dict):
    post_id = int(callback_data.get("post_id"))
    post = await get_user_post(post_id)
    if post:
        text = "Allaqachon qabul qilingan !!!"
        await bot.send_message(chat_id="-1001538496752", text=text)
        # await bot.send_message(chat_id="-1001640626557", text=text)
    else:
        if await update_user_post_status(call.message, post_id):
            text = "Qabul qilindi ✅ ✅ ✅"
            await bot.send_message(chat_id="-1001538496752", text=text)
            # await bot.send_message(chat_id="-1001640626557", text=text)

            post_data = await get_user_post(post_id)
            if post_data:
                link = f"https://t.me/cncele_bot?start={post_id}"
                # link = f"https://t.me/aiogramstatesbot?start={post_id}"
                text = _("Siz konkurs ishtirokchisiga aylandingiz. \nKo'proq like to'plang va g'olib bo'ling. \n\n")
                text += link
                await bot.send_message(chat_id=post_data["telegram_id"], text=text,
                                       reply_markup=await users_main_menu())

                await bot.send_photo(chat_id=post_data["telegram_id"], photo=post_data["images"][0],
                                     reply_markup=await post_like(post_id, link))

            else:
                print("Error in answer form group function")


@dp.callback_query_handler(callback_admin_answer.filter(act="admin_answer_no"))
async def admin_answer_no(call: CallbackQuery, callback_data: dict):
    post_id = int(callback_data.get("post_id"))
    post = await get_user_post_by_id(post_id)
    if post:
        if post["status"] == UserPostStatus.accepted:
            text = "Allaqachon qabul qilingan !!!"
            await bot.send_message(chat_id="-1001538496752", text=text)
        else:
            text = _("Sizning rasmlaringiz qabul qilinmadi.")
            await bot.send_message(chat_id=post["telegram_id"], text=text,
                                   reply_markup=await users_main_menu())
            await delete_user_post_admin_no(post_id)

            text = "Qabul qilinmadi ❌ ❌ ❌"
            await bot.send_message(chat_id="-1001538496752", text=text)
    else:
        text = "Botda nosozlik mavjud."
        await bot.send_message(chat_id="-1001538496752", text=text)
