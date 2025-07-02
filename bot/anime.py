# 📁 bot/anime.py

import re

# 🧹 Clean anime filenames by removing extra tags, group names, etc.
def clean_filename(filename: str) -> str:
    # Remove [group] or (group)
    filename = re.sub(r"[].*?[]", "", filename)

    # Replace dots/underscores with spaces
    filename = filename.replace("_", " ").replace(".", " ")

    # Remove common tags like 1080p, x264, etc.
    filename = re.sub(r"\b(1080p|720p|480p|x264|x265|HEVC|Dual Audio|Eng Subs|Subbed|BD|WEB|HDR|AMZN|NF|Hi10)\b", "", filename, flags=re.IGNORECASE)

    # Collapse multiple spaces to single
    filename = re.sub(r"\s+", " ", filename)

    return filename.strip()

# 📦 Detect if file is likely anime (based on common tags or structure)
def is_anime_file(filename: str) -> bool:
    keywords = ["anime", "episode", "ep", "OVA", "BD", "WEB", "1080p", "720p", "subbed", "RAW", "fansub"]
    filename_lower = filename.lower()
    return any(word.lower() in filename_lower for word in keywords)