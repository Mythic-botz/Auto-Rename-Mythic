from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import START_PIC_URL, START_VIDEO_URL, UPDATES_CHANNEL, BOT_USERNAME
from bot.fscheck import force_sub_check
from bot.database import is_premium
import random

# 🎬 Emoji button layout
START_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("💡 Help", callback_data="help"),
     InlineKeyboardButton("⚙️ Settings", callback_data="settings")],
    [InlineKeyboardButton("💎 Buy Token", callback_data="buy_token")],
    [InlineKeyboardButton("📢 Updates", url=f"https://t.me/{UPDATES_CHANNEL}")]
])

# 🚀 /start command handler
@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client: Client, message: Message):
    user = message.from_user

    # 🔒 Force subscribe check
    if UPDATES_CHANNEL:
        fsub = await force_sub_check(client, message)
        if fsub:
            return

    # 💎 Check if user is premium
    premium = await is_premium(user.id)

    caption = f"👋 Hello {user.mention},\n\nWelcome to **Premium Auto Rename Bot**!\n\nUse this bot to rename your files with cool features like sample video, thumbnails, dump logging, and more!"

    if premium:
        try:
            await message.reply_video(
                video=START_VIDEO_URL,
                caption=caption,
                reply_markup=START_BUTTONS
            )
        except Exception:
            await message.reply_photo(
                photo=START_PIC_URL,
                caption=caption,
                reply_markup=START_BUTTONS
            )
    else:
        await message.reply_photo(
            photo=START_PIC_URL,
            caption=caption,
            reply_markup=START_BUTTONS
        )
