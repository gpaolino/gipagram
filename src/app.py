from flask import Flask, jsonify, render_template, request, send_file
import redis, json, os
from utils.media import scan_media, file_hash

app = Flask(__name__)
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

PAGE_SIZE = 12

@app.route("/")
def index():
    # Serve the main HTML page (frontend that will call /api/media)
    return render_template("index.html")

@app.route("/api/media")
def api_media():
    # Parse page query param (default 0) and compute slice indices
    page = int(request.args.get("page", 0))
    start = page * PAGE_SIZE
    end = start + PAGE_SIZE

    # Try to read cached media list from Redis
    cached = r.get("media:list")
    #cached = False # Force refresh for testing
    if not cached:
        # Cache miss: scan filesystem and cache JSON for 1 hour
        media = scan_media()
        r.setex("media:list", 3600, json.dumps(media))
    else:
        # Cache hit: deserialize JSON into Python list
        media = json.loads(cached)

    # Select current page slice (in-memory)
    chunk = media[start:end]

    result = []
    for m in chunk:
        # Derive stable id from file path and build response item
        h = file_hash(m["path"])
        result.append({
            "id": h,
            "url": f"/media/{h}",
            # Simple type detection: mp4 => video, else image
            "type": "video" if m["path"].lower().endswith("mp4") else "image"
        })

    # Return JSON array of items
    return jsonify(result)

@app.route("/media/<fid>")
def serve_media(fid):
    # Need cached list to map id->path; return 404 if missing
    cached = r.get("media:list")
    if not cached:
        return "", 404

    media = json.loads(cached)
    for m in media:
        # Recompute hash and compare to requested id; send file on match
        if file_hash(m["path"]) == fid:
            return send_file(m["path"])

    # Not found
    return "", 404
