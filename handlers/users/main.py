from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp, _


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = _("""
    Buyruqlar: 
    
    /start => Botni ishga tushurish
    """)

    await message.answer(text)


@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer(message.text)
