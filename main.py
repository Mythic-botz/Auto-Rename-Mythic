# main.py ✅ Final Render-Compatible Version

import os
import asyncio
from pyrogram import Client, idle
from fastapi import FastAPI
import uvicorn
from config import Config

# ✅ Pyrogram Bot App
bot = Client(
    "AutoRenameBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="bot")
)

# ✅ FastAPI dummy app to keep Render alive
web = FastAPI()

@web.get("/")
async def root():
    return {"status": "Auto Rename Bot is running 🎉"}

# ✅ Async entry point that starts both FastAPI and bot
async def start_services():
    print("🤖 Starting Bot...")
    await bot.start()
    print("✅ Bot is now running.")
    await idle()
    await bot.stop()
    print("🛑 Bot stopped.")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    # Start both FastAPI and bot in same loop
    loop = asyncio.get_event_loop()

    # 🔁 Run both bot and FastAPI together
    def run():
        loop.run_until_complete(start_services())

    import threading
    threading.Thread(target=run).start()

    uvicorn.run(web, host="0.0.0.0", port=port)