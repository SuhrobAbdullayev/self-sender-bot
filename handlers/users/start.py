from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ContentType

from loader import dp, db, bot

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    channel_data = await db.get_info(str(message.chat.id))
    if channel_data is None:
        await message.answer(text="Assalomu aleykum! Siz reklama yuboruvchilar qatorida yo`qsiz. \n\n- Reklama sotib olish uchun @Ish_Admin_AS adminga yozing.")
        return
    count = channel_data['counts']
    await message.answer(f"Salom, {message.from_user.full_name}! \n\n🔹 Sizda {count} ta reklama bor.")


@dp.message_handler(content_types=ContentType.ANY)
async def handle_ads(message: types.Message):
    channel_data = await db.get_info(str(message.chat.id))
    if channel_data is None:
        return
    if message.media_group_id:
        await bot.send_message(chat_id=message.chat.id, text="❌ Kop rasmli reklamalarni yuborish imkonsiz. Iltimos bunday reklamalarni admin orqali yuboring. \n\n Admin: @Ish_Admin_AS")
        return
    if channel_data:
        channel_id = channel_data['channel_id']
        count = channel_data['counts'] - 1
        if channel_data['counts'] <= 0:
            await bot.send_message(chat_id=message.chat.id, text=f"⭕️ Sizda yuborish uchun reklama qolmadi. \n\n- Reklama sotib olish uchun @Ish_Admin_AS adminga yozing.")
            return
        try:
            await db.update_count(chat_id = str(message.chat.id), count = count)
            await bot.copy_message(from_chat_id=message.chat.id, chat_id=channel_id, message_id=message.message_id)
            await bot.copy_message(from_chat_id=message.chat.id, chat_id=5606952183, message_id=message.message_id)
            await bot.send_message(chat_id=message.chat.id, text=f"Reklamangiz yuborildi ✅ \n\n- Sizda {count} ta reklama qoldi")
        except Exception as e:
            await bot.send_message(chat_id=5606952183, text=e)
