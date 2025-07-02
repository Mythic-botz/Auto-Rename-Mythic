# 📁 bot/admin.py

from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config
ADMINS = Config.ADMINNS,
PREMIUM_LIMIT = Config.PREMIUM_LIMIT


from .database import (
    get_all_users, get_user_data, update_tokens,
    add_premium_user, remove_premium_user, is_premium_user
)
from .premium import is_admin
from .utils import format_file_size
import asyncio

# ✅ Check if user is admin
def admin_only(func):
    async def wrapper(client, message):
        if not await is_admin(message.from_user.id):
            return await message.reply("🚫 You don't have permission to use this command.")
        return await func(client, message)
    return wrapper

# 📊 Stats Command
@Client.on_message(filters.command("stats") & filters.private)
@admin_only
async def stats_cmd(client: Client, message: Message):
    users = await get_all_users()
    total_users = len(users)
    premium_users = sum(1 for u in users if u.get("premium"))
    total_tokens_used = sum(u.get("tokens_used", 0) for u in users)

    text = (
        f"📊 **Bot Stats:**\n\n"
        f"👥 Total Users: `{total_users}`\n"
        f"💎 Premium Users: `{premium_users}`\n"
        f"🔁 Rename Tokens Used: `{total_tokens_used}`\n"
    )
    await message.reply(text)

# 📣 Broadcast message to all users
@Client.on_message(filters.command("broadcast") & filters.private)
@admin_only
async def broadcast_cmd(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply("❗ Please reply to a message to broadcast.")

    users = await get_all_users()
    success = 0
    fail = 0

    for user in users:
        try:
            await client.copy_message(
                chat_id=user["_id"],
                from_chat_id=message.chat.id,
                message_id=message.reply_to_message.id
            )
            success += 1
        except:
            fail += 1
        await asyncio.sleep(0.05)

    await message.reply(f"✅ Broadcast complete!\n\nDelivered: `{success}`\nFailed: `{fail}`")

# ➕ Add Premium User
@Client.on_message(filters.command("addpremium") & filters.private)
@admin_only
async def add_premium(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("❗ Usage: /addpremium user_id")

    try:
        user_id = int(message.command[1])
        await add_premium_user(user_id)
        await update_tokens(user_id, -1, premium=True)  # Set unlimited
        await message.reply(f"✅ User `{user_id}` promoted to Premium.")
    except Exception as e:
        await message.reply(f"⚠️ Error:\n`{e}`")

# ➖ Remove Premium User
@Client.on_message(filters.command("removepremium") & filters.private)
@admin_only
async def remove_premium(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("❗ Usage: /removepremium user_id")

    try:
        user_id = int(message.command[1])
        await remove_premium_user(user_id)
        await update_tokens(user_id, PREMIUM_LIMIT, premium=False)
        await message.reply(f"✅ User `{user_id}` demoted to Free.")
    except Exception as e:
        await message.reply(f"⚠️ Error:\n`{e}`")

# 🔁 Reset tokens for a user
@Client.on_message(filters.command("reset") & filters.private)
@admin_only
async def reset_tokens(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("❗ Usage: /reset user_id")

    try:
        user_id = int(message.command[1])
        await update_tokens(user_id, PREMIUM_LIMIT if await is_premium_user(user_id) else 60)
        await message.reply(f"✅ Tokens reset for `{user_id}`.")
    except Exception as e:
        await message.reply(f"⚠️ Error:\n`{e}`")
