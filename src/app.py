from flask import Flask, jsonify, render_template, request, send_file
import redis, json, os
from utils.media import scan_media, file_hash

app = Flask(__name__)
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

PAGE_SIZE = 12

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/media")
def api_media():
    page = int(request.args.get("page", 0))
    start = page * PAGE_SIZE
    end = start + PAGE_SIZE

    cached = r.get("media:list")
    if not cached:
        media = scan_media()
        r.setex("media:list", 3600, json.dumps(media))
    else:
        media = json.loads(cached)

    chunk = media[start:end]

    result = []
    for m in chunk:
        h = file_hash(m["path"])
        result.append({
            "id": h,
            "url": f"/media/{h}",
            "type": "video" if m["path"].lower().endswith("mp4") else "image"
        })

    return jsonify(result)

@app.route("/media/<fid>")
def serve_media(fid):
    cached = r.get("media:list")
    if not cached:
        return "", 404

    media = json.loads(cached)
    for m in media:
        if file_hash(m["path"]) == fid:
            return send_file(m["path"])

    return "", 404
