from pyrogram import Client, filters
from config import Config
import logging
import asyncio
import os

# 📜 Logging Setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# 🚀 Bot Initialization
bot = Client(
    "AnimeAutoRenameBot",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    plugins={"root": "bot"}
)

# 🔁 Startup Routine
async def startup_tasks():
    logger.info("Bot Started Successfully!")
    # You can add DB checks or welcome log here

# 🚦 Run Bot
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(startup_tasks())
    bot.run()
