# 📁 callback.py
# 🤖 Handles inline button callbacks like settings toggle, cancel, etc.

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from config import Config 
ADMINS = Config.ADMINS
DELETE_DELAY = Config.DELETE_DELAY
from bot.database import get_user, update_setting
from bot.utils import get_settings_buttons

# 🚫 Cancel button handler (e.g., "cancel_rename" button)
@Client.on_callback_query(filters.regex("^cancel"))
async def cancel_button(client: Client, callback_query: CallbackQuery):
    await callback_query.message.delete()
    await callback_query.answer("❌ Operation cancelled", show_alert=False)

# ⚙️ Settings toggle handler
@Client.on_callback_query(filters.regex("^set_"))
async def toggle_setting(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    data = callback_query.data  # Example: "set_sample_off", "set_dump_on"
    setting, action = data.split("_")[1], data.split("_")[2]

    user = await get_user(user_id)
    if not user:
        return await callback_query.answer("⚠️ User not found in database!", show_alert=True)

    # ✨ Update setting value based on toggle
    user["settings"][setting] = True if action == "on" else False
    await update_settings(user_id, user["settings"])

    # 🔁 Update settings panel with new toggled buttons
    buttons = await get_settings_buttons(user_id)
    await callback_query.edit_message_reply_markup(reply_markup=buttons)
    await callback_query.answer("✅ Setting updated!", show_alert=False)

# 🔐 Admin-only callback (example: reset tokens or view user info)
@Client.on_callback_query(filters.regex("^admin_"))
async def admin_callback(client: Client, callback_query: CallbackQuery):
    if callback_query.from_user.id not in ADMINS:
        return await callback_query.answer("🚫 You are not allowed!", show_alert=True)

    await callback_query.answer("⚙️ Admin action placeholder.")
