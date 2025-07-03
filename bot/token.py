# 📁 token.py
# 🔐 Token System to manage Free & Premium user limits

from config import Config 
FREE_TOKENS = Config.DEFAULT_TOKENS
TOKEN_RESET_LIMIT = Config.TOKEN_RESET_LIMIT
from bot.database import get_user_data, update_user_tokens, is_premium_user
from pyrogram.types import Message

# 🔍 Get token status (current/limit) for user
async def get_token_status(user_id: int) -> tuple[int, int]:
    premium = await is_premium_user(user_id)
    if premium:
        return -1, -1  # ♾️ Unlimited for Premium
    data = await get_user_data(user_id)
    tokens = data.get("tokens", FREE_TOKENS)
    return tokens, FREE_TOKENS

# ✅ Use 1 token (on successful rename)
async def use_token(user_id: int) -> bool:
    premium = await is_premium_user(user_id)
    if premium:
        return True  # ♾️ No token reduction for Premium
    data = await get_user_data(user_id)
    tokens = data.get("tokens", FREE_TOKENS)
    if tokens > 0:
        await update_user_tokens(user_id, tokens - 1)
        return True
    return False  # ❌ No tokens left

# 🔁 Reset token manually (via /reset)
async def reset_tokens(user_id: int) -> bool:
    data = await get_user_data(user_id)
    used = FREE_TOKENS - data.get("tokens", FREE_TOKENS)
    if used < TOKEN_RESET_LIMIT:
        return False  # ⛔ Not enough used to reset
    await update_user_tokens(user_id, FREE_TOKENS)
    return True  # 🔄 Reset successful

# 📊 Format token info for message
async def token_message(user_id: int) -> str:
    premium = await is_premium_user(user_id)
    if premium:
        return "💎 You are a **Premium User**\n♾️ Unlimited renames!"
    
    tokens, limit = await get_token_status(user_id)
    used = limit - tokens
    return (
        f"👤 You are a **Free User**\n"
        f"✅ Tokens Left: `{tokens}` / `{limit}`\n"
        f"🔄 Used: `{used}`\n\n"
        f"⚠️ Use `/reset` to refresh tokens after `{TOKEN_RESET_LIMIT}` renames."
    )
