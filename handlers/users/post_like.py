from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery

from keyboards.default.users import after_like_menu, users_main_menu
from keyboards.inline.users import post_like_call, post_like
from loader import dp, bot, _
from utils.db_api.commands import get_competitions
from utils.db_api.user_posts import get_user_liked_or_not, delete_user_post_like, \
    add_user_post_like, get_user_post, get_all_posts


@dp.callback_query_handler(post_like_call.filter(act="add_or_remove_like"))
async def showrooms_menu_back(call: CallbackQuery, callback_data: dict, state: FSMContext):
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


@dp.message_handler(text=["Yana ko'rish ⏩", "Увидеть больше ⏩"])
async def admin_profile(message: types.Message):
    competition = await get_competitions()
    if competition:
        all_users_posts = await get_all_posts(competition["id"])
        if all_users_posts:
            for user in all_users_posts:
                post = await get_user_post(user["user_post_id"])
                link = f"https://t.me/cncele_bot?start={post['id']}"
                await message.answer_photo(photo=post["images"][0], reply_markup=await post_like(post['id'], link))
        else:
            text = _("Boshqa qatnashuvchilar mavjud emas.")
            await message.answer(text, reply_markup=await users_main_menu())
    else:
        pass


@dp.message_handler(text=["Asosiy menyu ⏹"])
async def admin_profile(message: types.Message):
    text = _("Asosiy menyuga xush kelibsiz.")
    await message.answer(text, reply_markup=await users_main_menu())
