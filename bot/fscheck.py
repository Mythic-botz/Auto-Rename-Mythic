# 📁 fscheck.py
# 📁 bot/fscheck.py

from pyrogram.types import Message
from pyrogram import Client
from config import FORCE_SUB_CHANNEL, FORCE_SUB_PIC, BOT_USERNAME
from pyrogram.errors import UserNotParticipant, ChannelPrivate, ChatAdminRequired

# ✅ Check if user is subscribed to update channel
async def force_sub(client: Client, message: Message) -> bool:
    if not FORCE_SUB_CHANNEL:
        return True  # 🔓 No force sub set, skip

    try:
        user = await client.get_chat_member(FORCE_SUB_CHANNEL, message.from_user.id)
        return user.status in ("member", "administrator", "creator")
    except UserNotParticipant:
        return False
    except (ChannelPrivate, ChatAdminRequired):
        return True  # 🔒 Skip force sub check if bot lacks access

# ✉️ Send Force Sub message with button
async def send_force_sub(message: Message):
    buttons = [
        [
            message.reply_markup.inline_keyboard[0][0] if message.reply_markup else None,
            {"text": "🔄 Refresh", "callback_data": "refreshfs"}
        ]
    ] if message.reply_markup else [
        [
            {"text": "📢 Join Channel", "url": f"https://t.me/{FORCE_SUB_CHANNEL}"},
            {"text": "🔄 Refresh", "callback_data": "refreshfs"}
        ]
    ]

    await message.reply_photo(
        photo=FORCE_SUB_PIC,
        caption=f"**📛 You must join @{FORCE_SUB_CHANNEL} to use this bot.**\n\nClick the button below to join and then press 'Refresh'.",
        reply_markup={"inline_keyboard": buttons}
    )