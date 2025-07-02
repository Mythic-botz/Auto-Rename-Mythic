# 📁 rename.py
# 🔁 Handle rename command and file replies

from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import DUMP_CHANNEL, FREE_TOKENS, TOKEN_RESET_LIMIT
from bot.fscheck import force_sub, send_force_sub
from bot.database import (
    get_user_data, update_user_tokens,
    is_premium_user
)
from bot.utils import (
    save_thumbnail, delete_thumbnail,
    format_size, generate_sample_clip, take_screenshot
)

# 🖼 Handle media reply for rename
@Client.on_message(filters.private & filters.reply & filters.media)
async def reply_media_handler(client: Client, message: Message):
    # 🛡 Check force sub first
    if not await force_sub(client, message):
        await send_force_sub(message)
        return

    user_id = message.from_user.id
    user_data = await get_user_data(user_id)
    premium = await is_premium_user(user_id)

    # 🧪 Token check (free users only)
    if not premium:
        tokens = user_data.get("tokens", 0)
        if tokens <= 0:
            await message.reply_text("🪙 You’ve used all your rename tokens for today!\n\n🕛 Try again after some time or upgrade to Premium for unlimited usage.")
            return

    # 💾 Store original media
    media = message.document or message.video or message.audio
    if not media:
        await message.reply_text("❗Unsupported media type.")
        return

    # 📎 Save details for later use
    file_id = media.file_id
    file_name = media.file_name or "Renamed_File"
    file_size = media.file_size
    mime_type = media.mime_type or "application/octet-stream"

    # 📤 Dump to universal channel (if enabled)
    if user_data.get("use_dump") and DUMP_CHANNEL:
        try:
            await client.send_cached_media(DUMP_CHANNEL, file_id, caption=f"#DUMPED_BY: `{user_id}`\n📁 **File:** `{file_name}`")
        except Exception as e:
            print(f"❗ Dump failed: {e}")

    # ✅ Prepare Rename Caption
    rename_mode = user_data.get("rename_mode", "caption")  # 'caption' or 'filename'
    if rename_mode == "caption":
        prompt = "✏️ Send me new caption for the file."
    else:
        prompt = "📂 Send new file name with extension (e.g., `MyVideo.mp4`)."

    # 💡 Ask user for next step
    await message.reply_text(
        f"{prompt}\n\n⚠️ Renaming will consume 1 token.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ Cancel", callback_data="cancel_rename")]
        ])
    )

    # 🧠 Store file details in memory (alternatively use DB/temp if needed)
    client.rename_cache[user_id] = {
        "file_id": file_id,
        "file_name": file_name,
        "file_size": file_size,
        "mime_type": mime_type,
        "mode": rename_mode,
        "thumb": user_data.get("thumbnail"),
        "sample": user_data.get("sample_video"),
        "screenshot": user_data.get("screenshot"),
        "premium": premium
    }

# ✍️ Handle /rename command
@Client.on_message(filters.private & filters.command("rename"))
async def rename_command_handler(client: Client, message: Message):
    await message.reply_text(
        "🔁 To rename a file:\n1️⃣ Send any video/file.\n2️⃣ I'll ask for new name or caption.\n3️⃣ Renamed file will be sent back.\n\n💡 Premium users get sample clips & no token limits!"
    )
