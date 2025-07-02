📁 fscheck.py

Force Subscribe Checker for Premium Auto Rename Bot

from config import FORCE_SUB_CHANNEL from pyrogram.types import Message from pyrogram import Client, errors, enums

✅ Check if user is a member of the updates channel

async def force_sub(client: Client, message: Message): if not FORCE_SUB_CHANNEL: return True  # No force sub configured

try:
    user = await client.get_chat_member(FORCE_SUB_CHANNEL, message.from_user.id)
    if user.status in [enums.ChatMemberStatus.BANNED, enums.ChatMemberStatus.RESTRICTED]:
        return False
    return True

except errors.UserNotParticipant:
    return False

except errors.ChatAdminRequired:
    # Bot is not admin in force sub channel
    return True

except Exception:
    return True

📤 Send Force Sub Message

async def send_force_sub(message: Message): from config import FORCE_SUB_TEXT, FORCE_SUB_PIC, UPDATES_CHANNEL from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

try:
    if FORCE_SUB_PIC:
        await message.reply_photo(
            photo=FORCE_SUB_PIC,
            caption=FORCE_SUB_TEXT.format(channel=UPDATES_CHANNEL),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Join Updates Channel", url=f"https://t.me/{UPDATES_CHANNEL}")]
            ]),
            quote=True
        )
    else:
        await message.reply(
            text=FORCE_SUB_TEXT.format(channel=UPDATES_CHANNEL),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Join Updates Channel", url=f"https://t.me/{UPDATES_CHANNEL}")]
            ]),
            quote=True
        )
except Exception as e:
    print(f"Error sending force sub message: {e}")

