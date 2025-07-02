# main.py

import os
import asyncio
import threading
from pyrogram import Client, idle
from pyrogram.errors import FloodWait
from fastapi import FastAPI
import uvicorn

from config import API_ID, API_HASH, BOT_TOKEN

app = Client(
    "AutoRenameBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# 🌐 FastAPI server (for Render.com health check)
web = FastAPI()

@web.get("/")
async def home():
    return {"status": "✅ Auto Rename Bot is running!"}

async def start_bot():
    try:
        print("🤖 Starting bot...")
        await app.start()
        print("✅ Bot started.")
        await idle()
    except FloodWait as e:
        print(f"⚠️ FloodWait: Sleeping for {e.value} seconds")
        await asyncio.sleep(e.value)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # 🔁 PORT from Render

    # 🔄 Start FastAPI server in background
    threading.Thread(target=uvicorn.run, args=(web,), kwargs={
        "host": "0.0.0.0",
        "port": port,
    }).start()

    # 🧠 Run bot after server starts
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())