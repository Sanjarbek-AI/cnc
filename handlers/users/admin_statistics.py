from aiogram import types
from aiogram.types import InputFile
from aiogram.types.callback_query import CallbackQuery

from filters.private_chat import IsPrivate
from handlers.users.excel_users import export_users_registered
from keyboards.default.admins import admin_main_menu
from keyboards.inline.users import export_excel_users
from loader import dp, _
from main import config
from utils.db_api.commands import get_showrooms, get_users, get_users_status_false, get_competitions, get_user, \
    get_top_users
from utils.db_api.user_posts import get_all_posts_users


async def return_statistics():
    showrooms = await get_showrooms()
    users = await get_users()
    start_users = await get_users_status_false()
    competition = await get_competitions()
    if competition:
        all_user = await get_all_posts_users(competition["id"])
        if all_user:
            user_number = len(all_user)
        else:
            user_number = 0
    else:
        user_number = _("Faol ko'nkurs yo'q")
    text = f"""
<b>{_("Ro'xatdan o'tganlar")}</b>: {len(users)} \n
<b>{_("Start bosganlar")}</b>: {len(start_users)} \n
<b>{_("Shovrumlar soni")}</b>: {len(showrooms)} \n
<b>{_("Faol ko'nkursdagi ishtirokchilar")}</b>: {user_number}\n
"""
    return text


@dp.message_handler(IsPrivate(), text=['Statistika 📈', 'Статистика 📈'], chat_id=config.ADMINS)
async def main_statistics(message: types.Message):
    text = await return_statistics()
    await message.answer(text, reply_markup=await export_excel_users())


@dp.callback_query_handler(text="registered_users", chat_id=config.ADMINS)
async def export_excel(call: CallbackQuery):
    users = await get_users()
    excel_file = await export_users_registered(users)

    with open("users_registered.xlsx", "wb") as binary_file:
        binary_file.write(excel_file)
    export_file = InputFile(path_or_bytesio="users_registered.xlsx")
    await call.message.reply_document(export_file)


@dp.callback_query_handler(text="competition_users", chat_id=config.ADMINS)
async def export_excel(call: CallbackQuery):
    comp = await get_competitions()

    if comp:
        all_users = await get_all_posts_users(comp['id'])
        if all_users:
            users_id_list = [user["telegram_id"] for user in all_users]
            users = list()
            for user in users_id_list:
                user_data = await get_user(user)
                users.append(user_data)
            excel_file = await export_users_registered(users)
            with open("competition_users.xlsx", "wb") as binary_file:
                binary_file.write(excel_file)
            export_file = InputFile(path_or_bytesio="competition_users.xlsx")
            await call.message.reply_document(export_file)
    else:
        text = _("Aktiv konkurs mavjud emas.")
        await call.message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(text="top_10_users", chat_id=config.ADMINS)
async def export_excel(call: CallbackQuery):
    comp = await get_competitions()
    if comp:
        active_posts = await get_all_posts_users(comp["id"])
        id_list = [post["id"] for post in active_posts]
        top_users_posts = await get_top_users(id_list)
        text = """**********************************"""
        for post in top_users_posts[-1: -11]:
            user = await get_user(post["telegram_id"])
            text += f"""
    IF: {user["full_name"]}              
    Raqam: {user["phone_number"]}
    Like: {post["like"]}  \n   
**********************************
    """
        await call.message.answer(text=text, reply_markup=await admin_main_menu())
    else:
        text = "Faol ko'nkur mavjud emas."
        await call.message.answer(text=text, reply_markup=await admin_main_menu())
