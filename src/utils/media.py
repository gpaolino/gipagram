import os, time, hashlib, json
import magic

MEDIA_ROOT = "media/"

def file_hash(path):
    return hashlib.md5(path.encode()).hexdigest()

def scan_media():
    media = []

    for root, _, files in os.walk(MEDIA_ROOT):
        for f in files:
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".mp4", ".mov")):
                full = os.path.join(root, f)
                media.append({
                    "path": full,
                    "mtime": os.path.getmtime(full)
                })

    media.sort(key=lambda x: x["mtime"], reverse=True)
    return media
