from motor.motor_asyncio import AsyncIOMotorClient
from config import Config

# 🚀 Connect to MongoDB using values from Config
mongo_client = AsyncIOMotorClient(Config.MONGO_URL)
db = mongo_client[Config.DB_NAME]

# 🧵 Collections
users_col = db["users"]
settings_col = db["settings"]
tokens_col = db["tokens"]
stats_col = db["stats"]


# ✅ Get user settings
async def get_user(user_id):
    return await db.users.find_one({"_id": user_id})


# ✅ Get all user IDs (used in /broadcast and /leaderboard)
async def get_all_users():
    users = []
    async for doc in db.users.find({}, {"_id": 1}):
        users.append(doc["_id"])
    return users

# 📊 Get stats data for a user (rename count and usage)
async def get_user_data(user_id: int) -> dict:
    data = await stats_col.find_one({"_id": user_id}) or {}
    return {
        "total_renamed": data.get("total_renamed", 0),
        "used_tokens": data.get("used_tokens", 0)
    }


# ✅ Add to database.py
async def save_user_data(user_id: int, data: dict):
    await stats_col.update_one({"_id": user_id}, {"$set": data}, upsert=True)


# 📥 Add or update user
async def add_user(user_id: int):
    await users_col.update_one({"_id": user_id}, {"$setOnInsert": {"_id": user_id}}, upsert=True)

# ⚙️ Get user settings (with defaults)
async def get_settings(user_id: int):
    default = {
        "rename_mode": "caption",
        "thumbnail": None,
        "sample_video": False,
        "use_dump": False
    }
    doc = await settings_col.find_one({"_id": user_id}) or {}
    return {**default, **doc}

# 🛠️ Update a specific setting
async def update_setting(user_id: int, key: str, value):
    await settings_col.update_one({"_id": user_id}, {"$set": {key: value}}, upsert=True)

# 🔢 Get remaining tokens for user
async def get_tokens(user_id: int) -> int:
    doc = await tokens_col.find_one({"_id": user_id})
    return doc["tokens"] if doc else Config.DEFAULT_TOKENS

# 🔄 Set token count
async def set_tokens(user_id: int, tokens: int):
    await tokens_col.update_one({"_id": user_id}, {"$set": {"tokens": tokens}}, upsert=True)

# ➖ Decrease tokens by 1
async def use_token(user_id: int):
    await tokens_col.update_one({"_id": user_id}, {"$inc": {"tokens": -1}}, upsert=True)

# 📈 Track rename usage for leaderboard
async def update_usage(user_id: int):
    await stats_col.update_one({"_id": user_id}, {"$inc": {"count": 1}}, upsert=True)

# 🏆 Get leaderboard data
async def get_leaderboard(limit: int = 10):
    cursor = stats_col.find().sort("count", -1).limit(limit)
    return await cursor.to_list(length=limit)

# 💎 Add user to Premium collection
async def add_premium_user(user_id: int):
    await tokens_col.update_one({"_id": user_id}, {"$set": {"premium": True}}, upsert=True)

# ❌ Remove user from Premium
async def remove_premium_user(user_id: int):
    await tokens_col.update_one({"_id": user_id}, {"$unset": {"premium": ""}})

# ✅ Check if user is Premium
async def is_premium_user(user_id: int) -> bool:
    doc = await tokens_col.find_one({"_id": user_id})
    return doc.get("premium", False) if doc else False

# 🔁 Update tokens manually (admin use)
async def update_tokens(user_id: int, tokens: int):
    await tokens_col.update_one({"_id": user_id}, {"$set": {"tokens": tokens}}, upsert=True)

# ✅ Update user's token count
async def update_user_tokens(user_id: int, tokens: int):
    await users_collection.update_one(
        {"_id": user_id},
        {"$set": {"tokens": tokens}},
        upsert=True
    )