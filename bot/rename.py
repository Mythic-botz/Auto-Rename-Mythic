# 📁 bot/rename.py
# 🔁 Rename file by replying with `/rename NewName.ext`

from pyrogram import Client, filters
from pyrogram.types import Message
from config import DELETE_DELAY, DUMP_CHANNEL
from .fscheck import force_sub, send_force_sub
from .utils import get_file_size
from .database import get_user_data, update_usage, is_premium_user
from .settings import get_settings

import os

@Client.on_message(filters.command("rename") & filters.private)
async def rename_file(client: Client, message: Message):
    # 🔐 Force subscribe
    if not await force_sub(client, message):
        return await send_force_sub(message)

    # ⚠️ Must reply to a media file
    if not message.reply_to_message or not message.reply_to_message.media:
        return await message.reply("❗ Please reply to a file to rename it!")

    # 📝 Extract new file name
    if len(message.command) < 2:
        return await message.reply("❗ Usage: `/rename NewFileName.ext`", quote=True)

    new_name = message.text.split(" ", 1)[1]
    user_id = message.from_user.id

    # 🔁 Check user data and settings
    user_data = await get_user_data(user_id)
    settings = await get_settings(user_id)
    is_premium = await is_premium_user(user_id)

    # 🧪 Free user token check
    if not is_premium:
        tokens = user_data.get("tokens", 0)
        if tokens <= 0:
            return await message.reply("🪙 You’ve used all your rename tokens for today!\n\nUpgrade to Premium for unlimited access.")

    # 📦 Get media file
    media = message.reply_to_message
    file = getattr(media, media.media.value, None)
    if not file or not file.file_id:
        return await message.reply("❌ Failed to read media file.")

    # 📤 Dump to universal dump channel
    if settings.get("use_dump") and DUMP_CHANNEL:
        try:
            await client.send_cached_media(DUMP_CHANNEL, file.file_id, caption=f"#DUMPED_BY: `{user_id}`\n📁 `{new_name}`")
        except Exception as e:
            print(f"[DUMP FAIL] {e}")

    # 📥 Download original
    sent_msg = await message.reply("📥 Downloading...")
    d_path = await client.download_media(media, file_name="temp/")
    if not os.path.exists(d_path):
        return await sent_msg.edit("⚠️ Download failed.")

    # 🪄 Rename file
    new_path = f"temp/{new_name}"
    os.rename(d_path, new_path)

    # 📤 Upload renamed file
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

    # 🧹 Clean up
    await sent_msg.delete()
    os.remove(new_path)
    await update_usage(user_id)

    # ⏳ Auto delete
    if DELETE_DELAY:
        await message.delete()
