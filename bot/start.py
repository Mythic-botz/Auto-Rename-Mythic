# 📁 bot/start.py

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
START_PIC_URL = Config.START_PIC_URL
START_VIDEO_URL = Config.START_VIDEO_URL
SUPPORT_CHAT = Config.SUPPORT_CHAT
CONTACT_DEV = Config.CONTACT_DEV

from .fscheck import force_sub, send_force_sub
from .premium import is_premium_user

# 🎀 Inline button layout with emojis (Anya Style)
def start_panel():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 Help", callback_data="help_callback")],
        [InlineKeyboardButton("⚙️ Settings", callback_data="settings_callback")],
        [
            InlineKeyboardButton("💠 My Tokens", callback_data="token_status"),
            InlineKeyboardButton("💎 Buy Premium", url=f"https://t.me/{CONTACT_DEV}")
        ],
        [InlineKeyboardButton("👥 Support", url=f"https://t.me/{SUPPORT_CHAT}")]
    ])

# 🚀 Start command handler
@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client: Client, message: Message):
    user = message.from_user

    # 📛 Force Subscription Check
    if not await force_sub(client, message):
        return await send_force_sub(message)

    # 💠 Premium check
    is_premium = await is_premium_user(user.id)

    # 🎥 Send Video to Premium / Image to Free Users
    caption = f"""
👋 𝐇𝐞𝐥𝐥𝐨 {user.mention},

🥷 I am your personal **Anime Auto Rename Bot**.
🪄 Rename files, set thumbnails, track usage tokens & more!

🔰 Free users: {user.id}
💎 Premium: {"✅" if is_premium else "❌"}
"""
    if is_premium:
        await client.send_video(
            chat_id=message.chat.id,
            video=START_VIDEO_URL,
            caption=caption,
            reply_markup=start_panel()
        )
    else:
        await client.send_photo(
            chat_id=message.chat.id,
            photo=START_PIC_URL,
            caption=caption,
            reply_markup=start_panel()
        )