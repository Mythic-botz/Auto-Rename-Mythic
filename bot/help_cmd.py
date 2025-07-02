# 📁 bot/help_cmd.py

from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# 📘 Help text
HELP_TEXT = """
👋 **How to Use This Bot?**

🔹 Just send me any media file (video/document).
🔹 I'll give you rename options via inline buttons.
🔹 You can set thumbnails, captions, and rename modes.
🔹 Premium users enjoy unlimited access and sample video features.

⚙️ **Available Commands:**
/start - Start the bot
/help - Show help message
/settings - Manage your preferences
/rename - Manually rename via reply
/leaderboard - Show top users
/token - Show token status
/reset - Reset tokens (free users)
/premium - Buy premium access

💡 Need help? Contact Support from the start menu!
"""

# 🧑‍🏫 Help command handler
@Client.on_message(filters.command("help") & filters.private)
async def help_command(client: Client, message: Message):
    await message.reply_text(
        text=HELP_TEXT,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 Back", callback_data="start_callback")]
        ])
    )

# 📲 Callback handler for inline help
@Client.on_callback_query(filters.regex("help_callback"))
async def help_callback(client: Client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text=HELP_TEXT,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 Back", callback_data="start_callback")]
        ])
    )