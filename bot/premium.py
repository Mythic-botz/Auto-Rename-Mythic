# 📁 bot/premium.py

from config import Config
PREMIUM_IDS = Config.PREMIUM_IDS
ADMINS = Config.ADMINS
from .database import get_user_data, save_user_data

# 🔍 Check if user is Premium
async def is_premium_user(user_id: int) -> bool:
    if user_id in PREMIUM_IDS:
        return True
    data = await get_user_data(user_id)
    return data.get("premium", False)

# ✅ Add user to Premium
async def add_premium_user(user_id: int):
    data = await get_user_data(user_id)
    data["premium"] = True
    await save_user_data(user_id, data)

# ❌ Remove user from Premium
async def remove_premium_user(user_id: int):
    data = await get_user_data(user_id)
    data["premium"] = False
    await save_user_data(user_id, data)

# 🛡️ Check if user is Admin
async def is_admin(user_id: int) -> bool:
    return user_id in ADMINS