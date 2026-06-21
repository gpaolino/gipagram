import os, time, hashlib, json
import magic
from dotenv import load_dotenv

load_dotenv()

MEDIA_ROOT = os.getenv("MEDIA_ROOT", "nomedia/")
SORT = os.getenv("SORT", "mtime")

def file_hash(path):
    # Return a stable id for a file path using MD5 of the path string
    return hashlib.md5(path.encode()).hexdigest()

def scan_media():
    # Walk MEDIA_ROOT (or fallback "nomedia/") and collect media entries
    media = []

    for root, _, files in os.walk("nomedia/" if not os.path.exists(MEDIA_ROOT) else MEDIA_ROOT):
        for f in files:
            # Filter by common image/video extensions
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".mp4", ".mov")):
                full = os.path.join(root, f)
                media.append({
                    "path": full,
                    # Store modification time for default orting
                    "mtime": os.path.getmtime(full)
                })

    # Sort by parameter (or default "mtime") and return list of dicts
    media.sort(key=lambda x: x[SORT])
    
    return media
