import os

class Config:
    # ⚙️ Basic Bot Settings
    API_ID = int(os.environ.get("API_ID", "123456"))
    API_HASH = os.environ.get("API_HASH", "your_api_hash")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "AnimeRenameBot")

    # 📢 Force Sub Channel
    FORCE_SUB_CHANNEL = os.environ.get("FORCE_SUB_CHANNEL", "MythicUpdates")

    # 🎥 Start Image/Video
    START_PIC_URL = os.environ.get("START_PIC_URL", "https://telegra.ph/file/start_pic.jpg")
    FORCE_SUB_PIC = os.environ.get("FORCE_SUB_PIC", "https://telegra.ph/file/fs_pic.jpg")
    START_VIDEO_URL = os.environ.get("START_VIDEO_URL", "https://telegra.ph/file/start_video.mp4")

    # 🏷️ Premium Settings
    PREMIUM_IDS = list(map(int, os.environ.get("PREMIUM_IDS", "").split()))
    PREMIUM_LIMIT = int(os.environ.get("PREMIUM_LIMIT", 0))

    # 💰 Token System
    DEFAULT_TOKENS = int(os.environ.get("DEFAULT_TOKENS", 60))  # Free user daily rename tokens
    TOKEN_RESET_HOURS = int(os.environ.get("TOKEN_RESET_HOURS", 24))

    # 📁 Channels
    DUMP_CHANNEL = int(os.environ.get("DUMP_CHANNEL", "-1001234567890"))

    # 🔑 Admins
    ADMINS = list(map(int, os.environ.get("ADMINS", "").split()))

    # 🧠 Bot Info
    BOT_NAME = os.environ.get("BOT_NAME", "Anime Auto Rename Bot")
    BOT_LANG = os.environ.get("BOT_LANG", "EN")

    # 🗃️ Database
    DB_NAME = os.environ.get("DB_NAME", "Rename")  # MongoDB database name
    MONGO_URL = os.environ.get("MONGO_URL", "")   # 🔥 ADD THIS LINE for MongoDB URI

    # 🔧 Misc
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001234567890"))
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", "MythicSupport")
    CONTACT_DEV = os.environ.get("CONTACT_DEV", "MythicXBot")

    # 🕓 Auto delete time (in seconds) for things like /leaderboard
    DELETE_DELAY = int(os.environ.get("DELETE_DELAY", 30))
