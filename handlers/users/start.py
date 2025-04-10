import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ContentType

from loader import dp, db, bot


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    channel_data = await db.get_info(str(message.chat.id))
    if channel_data is None:
        await message.answer(text="assalomu aleykum")
        return
    count = channel_data['counts']
    await message.answer(f"Salom, {message.from_user.full_name}! \n\n Sizda qolgan reklamalar soni: {count} ta")


@dp.message_handler(content_types=ContentType.ANY)
async def handle_ads(message: types.Message):
    channel_data = await db.get_info(str(message.chat.id))
    if channel_data is None:
        return

    if channel_data:
        channel_id = channel_data['channel_id']
        count = channel_data['counts'] + 1

        await db.update_count(chat_id = str(message.chat.id), count = count)
        await bot.copy_message(from_chat_id=message.chat.id, chat_id=channel_id, message_id=message.message_id)
        await bot.send_message(channel_id=message.chat.id, text="Reklamangiz yuborildi")



