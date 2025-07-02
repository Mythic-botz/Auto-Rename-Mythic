# main.py

from pyrogram import Client
from config import Config
import logging
import os

# 🧠 Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 📦 Pyrogram Client App
app = Client(
    name="AnimeRenameBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="bot")  # 🔌 Load all bot/ modules
)

# 🚀 Webhook Mode for Render
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 8080))  # 🌐 Render provides dynamic port
    app.run()  # ✅ Required for Render hosting