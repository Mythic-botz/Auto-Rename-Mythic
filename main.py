# main.py

import os
import asyncio
import threading
from pyrogram import Client, idle
from pyrogram.errors import FloodWait
from fastapi import FastAPI
import uvicorn
from bot import start, help, rename, token, admin, settings  # etc.

from config import Config
app = Client(
    "AutoRenameBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
)



# ✅ Import all your handlers here so they are registered before app.start()
import bot.start
import bot.help
import bot.rename
import bot.token
import bot.settings
import bot.admin
import bot.anime

# 🌐 Dummy FastAPI app for keeping Render alive
web = FastAPI()

@web.get("/")
async def root():
    return {"status": "Auto Rename Bot is running 🎉"}

# ✅ Start bot async function
async def start_bot():
    print("🤖 Starting bot...")
    await app.start()
    print("✅ Bot started.")
    await idle()

# ✅ Entry point
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))

    # Start the FastAPI + Bot together
    loop = asyncio.get_event_loop()
    loop.create_task(start_bot())  # background bot task

    # Start web server (won't block the bot)
    uvicorn.run(web, host="0.0.0.0", port=port)