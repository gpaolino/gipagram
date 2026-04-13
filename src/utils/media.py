import os, time, hashlib, json
import magic
from dotenv import load_dotenv

load_dotenv()

MEDIA_ROOT = os.getenv("MEDIA_ROOT", "nomedia/")

def file_hash(path):
    return hashlib.md5(path.encode()).hexdigest()

def scan_media():
    media = []

    for root, _, files in os.walk("nomedia/" if not os.path.exists(MEDIA_ROOT) else MEDIA_ROOT):
        for f in files:
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".mp4", ".mov")):
                full = os.path.join(root, f)
                media.append({
                    "path": full,
                    "mtime": os.path.getmtime(full)
                })

    media.sort(key=lambda x: x["mtime"], reverse=True)
    return media
