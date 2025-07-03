# main.py ✅ FINAL WORKING RENDER VERSION

import os
import asyncio
from pyrogram import Client, idle
from fastapi import FastAPI
import uvicorn
from config import Config

# ✅ Initialize Pyrogram Client
app = Client(
    "AutoRenameBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="bot")
)

# ✅ FastAPI dummy app
web = FastAPI()

@web.get("/")
async def root():
    return {"status": "Auto Rename Bot is running 🎉"}

# ✅ Start FastAPI server (non-blocking)
async def start_web():
    config = uvicorn.Config(web, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)), log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

# ✅ Combined startup
async def main():
    print("🤖 Starting Bot and FastAPI...")
    await app.start()
    await asyncio.gather(
        idle(),        # Wait for bot
        start_web(),   # Wait for FastAPI
    )
    await app.stop()
    print("🛑 Bot stopped.")

if __name__ == "__main__":
    asyncio.run(main())