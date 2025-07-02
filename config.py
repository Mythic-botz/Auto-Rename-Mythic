import os

class Config:
    # ⚙️ Basic Bot Settings
    API_ID = int(os.environ.get("API_ID", "23476863"))
    API_HASH = os.environ.get("API_HASH", 69daa0835439c4211f34c2e9ad0acb5c")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7662888624:AAFvZo4r6bUrYHEKkZ8KkuRvY3pqYUMqjls")
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "AizenRenameBot")

    # 📢 Force Sub Channel
    FORCE_SUB_CHANNEL = os.environ.get("FORCE_SUB_CHANNEL", "https://t.me/MythicBot_Support")

    # 🎥 Start Image/Video
    START_PIC_URL = os.environ.get("START_PIC_URL", "https://graph.org/file/374f1cd9b7278e32736a0-772d68eaa0bf9ebb4d.jpg")
    FORCE_SUB_PIC = os.environ.get("FORCE_SUB_PIC", "https://graph.org/file/374f1cd9b7278e32736a0-772d68eaa0bf9ebb4d.jpg")
    START_VIDEO_URL = os.environ.get("START_VIDEO_URL", "https://ar-hosting.pages.dev/1751352310217.mp4")

    # 🏷️ Premium Settings
    PREMIUM_IDS = list(map(int, os.environ.get("PREMIUM_IDS", "").split()))
    PREMIUM_LIMIT = int(os.environ.get("PREMIUM_LIMIT", 0))

    # 💰 Token System
    DEFAULT_TOKENS = int(os.environ.get("DEFAULT_TOKENS", 60))  # Free user daily rename tokens
    TOKEN_RESET_HOURS = int(os.environ.get("TOKEN_RESET_HOURS", 24))

    # 📁 Channels
    DUMP_CHANNEL = int(os.environ.get("DUMP_CHANNEL", "-1002876112974"))

    # 🔑 Admins
    ADMINS = list(map(int, os.environ.get("ADMINS", "6617544956").split()))

    # 🧠 Bot Info
    BOT_NAME = os.environ.get("BOT_NAME", "Aizen")
    BOT_LANG = os.environ.get("BOT_LANG", "EN")

    # 🗃️ Database
    DB_NAME = os.environ.get("DB_NAME", "Rename")  # MongoDB database name
    MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://Rename:XoFpKwreyhCeEvcI@rename.aukmb5u.mongodb.net/")   # 🔥 ADD THIS LINE for MongoDB URI

    # 🔧 Misc
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001234567890"))
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", "MythicBot_Support")
    CONTACT_DEV = os.environ.get("CONTACT_DEV", "HARUTO_OFFICAL")

    # 🕓 Auto delete time (in seconds) for things like /leaderboard
    DELETE_DELAY = int(os.environ.get("DELETE_DELAY", 30))
