# 📁 bot/settings.py

from pymongo import MongoClient
from config import Config 
MONGO_URL = Config.MONGO_URL
from .premium import is_premium_user

client = MongoClient(MONGO_URL)
db = client["Rename"]
collection = db["settings"]

# 📥 Default user settings
def default_settings():
    return {
        "rename_mode": "caption",    # 📝 Can be 'filename' or 'caption'
        "sample_video": False,       # 🎞️ Premium-only
        "use_dump": False,           # 📤 Premium-only
        "thumbnail": None            # 🖼️ File ID
    }

# 🔍 Get user settings or fallback to default
async def get_settings(user_id: int) -> dict:
    data = collection.find_one({"_id": user_id})
    return data or {"_id": user_id, **default_settings()}

# 🔄 Toggle a boolean setting (like sample_video, use_dump)
async def toggle_setting(user_id: int, key: str) -> str:
    user_settings = await get_settings(user_id)

    # 🔒 Only Premium users can toggle sample_video and use_dump
    if key in ["sample_video", "use_dump"] and not await is_premium_user(user_id):
        return "🔒 Premium feature only!"

    current_value = user_settings.get(key, False)
    new_value = not current_value
    collection.update_one({"_id": user_id}, {"$set": {key: new_value}}, upsert=True)
    return f"{'✅ Enabled' if new_value else '❌ Disabled'} {key}"