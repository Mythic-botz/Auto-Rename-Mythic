# 📁 bot/rename.py

from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import Config 
DELETE_DELAY = Config.DELETE_DELAY

from .fscheck import force_sub, send_force_sub
from .utils import get_file_size
from .database import update_usage, get_user_data
from .settings import get_settings

import os
import time

# ⛏ Combo Rename Cache
if not hasattr(Client, "rename_cache"):
    Client.rename_cache = {}

# ✨ Command: /rename NewFileName.ext (reply to a media file)
@Client.on_message(filters.command("rename") & filters.private)
async def rename_file(client: Client, message: Message):
    # 🔐 Check force sub
    if not await force_sub(client, message):
        return await send_force_sub(message)

    # ⚠️ Must be a reply to a media file
    if not message.reply_to_message or not message.reply_to_message.media:
        return await message.reply("❗ Please reply to a file to rename it!")

    # 📝 Extract the new filename
    if len(message.command) < 2:
        return await message.reply("❗ Usage: `/rename NewFileName.ext`", quote=True)

    new_name = message.text.split(" ", 1)[1]
    user_id = message.from_user.id

    # 🔄 Get user settings
    settings = await get_settings(user_id)

    # 📦 Extract original file
    media = message.reply_to_message
    file = getattr(media, media.media.value, None)
    if not file or not file.file_id:
        return await message.reply("❌ Unable to access file.")

    # 📥 Download the file
    sent_msg = await message.reply("📥 Downloading...")
    d_path = await client.download_media(media, file_name="temp/")
    if not os.path.exists(d_path):
        return await sent_msg.edit("⚠️ Failed to download.")

    # 🪄 Rename the file
    new_path = f"temp/{new_name}"
    os.rename(d_path, new_path)

    # 📤 Send renamed file
    await sent_msg.edit("📤 Uploading...")
    try:
        caption = new_name if settings.get("rename_mode") == "filename" else media.caption or new_name
        thumb = settings.get("thumbnail")
        await message.reply_document(
            document=new_path,
            caption=caption,
            thumb=thumb,
            quote=True
        )
    except Exception as e:
        await message.reply(f"⚠️ Upload failed:\n`{e}`")

    # 🧹 Cleanup and update usage
    await sent_msg.delete()
    os.remove(new_path)
    await update_usage(user_id)

    # ⏳ Auto delete /rename command if DELETE_DELAY set
    if DELETE_DELAY:
        await message.delete()


# 🔁 Media Reply Handler for Combo Rename Flow
@Client.on_message(filters.private & filters.reply & filters.media)
async def reply_media_handler(client: Client, message: Message):
    # ✅ Force sub check
    if not await force_sub(client, message):
        return await send_force_sub(message)

    user_id = message.from_user.id
    user_data = await get_user_data(user_id)
    premium = user_data.get("premium", False)

    # 🧪 Token check (Free users only)
    if not premium:
        tokens = user_data.get("tokens", 0)
        if tokens <= 0:
            return await message.reply("🪙 You’ve used all your rename tokens!\nUpgrade to Premium for unlimited renames.")

    # 📎 Extract media
    media = message.document or message.video or message.audio
    if not media:
        return await message.reply("❗ Unsupported media type.")

    # 📥 Save file info
    file_id = media.file_id
    file_name = media.file_name or "Renamed_File"
    file_size = media.file_size
    mime_type = media.mime_type or "application/octet-stream"

    # 🧠 Store in cache
    client.rename_cache[user_id] = {
        "file_id": file_id,
        "file_name": file_name,
        "file_size": file_size,
        "mime_type": mime_type,
        "mode": user_data.get("rename_mode", "caption"),
        "thumb": user_data.get("thumbnail"),
        "sample": user_data.get("sample_video"),
        "screenshot": user_data.get("screenshot"),
        "premium": premium
    }

    # ✏️ Prompt for new name or caption
    prompt = "📂 Send new file name with extension (e.g. `MyVideo.mp4`)." \
        if user_data.get("rename_mode", "caption") == "filename" \
        else "📝 Send new caption for the file."

    await message.reply_text(
        f"{prompt}\n\n⚠️ Renaming will consume 1 token.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ Cancel", callback_data="cancel_rename")]
        ])
    )
