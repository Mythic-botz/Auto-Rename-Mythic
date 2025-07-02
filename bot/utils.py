# 📁 bot/utils.py

import os
from PIL import Image
from pyrogram.types import Message
import time

# 🧠 Format file size

def format_file_size(size):
    """
    Convert file size from bytes to human-readable format 📦
    """
    if size < 1024:
        return f"{size} B"
    elif size < 1024 ** 2:
        return f"{size / 1024:.2f} KB"
    elif size < 1024 ** 3:
        return f"{size / (1024 ** 2):.2f} MB"
    else:
        return f"{size / (1024 ** 3):.2f} GB"

# 🖼️ Save thumbnail from a replied image
async def save_thumbnail(message: Message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        return None

    user_id = message.from_user.id
    photo = message.reply_to_message.photo.file_id
    path = f"downloads/thumb_{user_id}.jpg"

    # 📥 Download thumbnail image
    file_path = await message.reply_to_message.download(file_name=path)

    # 🧱 Resize to 320x320 (Telegram's standard for thumbnails)
    try:
        img = Image.open(file_path)
        img = img.convert("RGB")
        img = img.resize((320, 320))
        img.save(path, "JPEG")
        return path
    except Exception as e:
        print(f"⚠️ Failed to process thumbnail: {e}")
        return None

# 🗑️ Delete user's saved thumbnail
def delete_thumbnail(user_id: int):
    path = f"downloads/thumb_{user_id}.jpg"
    if os.path.exists(path):
        os.remove(path)

# 📂 Get user's thumbnail path
def get_thumbnail_path(user_id: int):
    path = f"downloads/thumb_{user_id}.jpg"
    return path if os.path.exists(path) else None

# 📸 Placeholder for screenshot generation
async def generate_screenshots(file_path: str):
    # ⏳ To be implemented with ffmpeg or custom logic
    return []

# 🎞️ Placeholder for sample clip generation
async def generate_sample_clip(file_path: str):
    # ⏳ To be implemented with ffmpeg or custom logic
    return None
