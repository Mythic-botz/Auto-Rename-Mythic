# bot/__init__.py

# 🚀 Import all handlers to register them when the bot starts
from . import start
from . import help_cmd
from . import rename
from . import token
from . import admin
from . import settings
from . import fscheck
from . import premium
from . import callback  # if you use callback buttons

# ⚠️ Make sure to avoid emojis or raw text outside strings or comments.