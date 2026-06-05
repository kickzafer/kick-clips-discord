import requests
import json
import os

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]

API_URL = "https://kick.com/api/v2/channels/kickzafer/videos"

LAST_ID_FILE = "last_id.txt"

response = requests.get(API_URL, timeout=30)
response.raise_for_status()

data = response.json()

if not data:
    print("Veri bulunamadı.")
    exit()

latest = data[0]
latest_id = str(latest["id"])

old_id = None

if os.path.exists(LAST_ID_FILE):
    with open(LAST_ID_FILE, "r", encoding="utf-8") as f:
        old_id = f.read().strip()

if old_id != latest_id:

    title = latest.get("session_title", "Yeni Klip")
    slug = latest.get("slug", "")

    clip_url = f"https://kick.com/kickzafer/videos/{slug}"

    payload = {
        "content": f"🎬 Yeni Kick klibi!\n**{title}**\n{clip_url}"
    }

    requests.post(WEBHOOK_URL, json=payload, timeout=30)

    with open(LAST_ID_FILE, "w", encoding="utf-8") as f:
        f.write(latest_id)

    print("Yeni klip gönderildi.")
else:
    print("Yeni klip yok.")
