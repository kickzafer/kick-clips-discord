import requests
import os

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]

API_URL = "https://kick.com/api/v2/channels/kickzafer/clips"

LAST_ID_FILE = "last_id.txt"

response = requests.get(API_URL, timeout=30)
response.raise_for_status()

data = response.json()

clips = data.get("clips", [])

if not clips:
    print("Klip bulunamadı.")
    exit()

latest = clips[0]
latest_id = str(latest["id"])

old_id = None

if os.path.exists(LAST_ID_FILE):
    with open(LAST_ID_FILE, "r", encoding="utf-8") as f:
        old_id = f.read().strip()

if old_id != latest_id:

    title = latest.get("title", "Yeni Klip")
    clip_id = latest["id"]
    clip_url = f"https://kick.com/kickzafer/clips/{clip_id}"

    thumbnail = latest.get("thumbnail_url", "")
    creator = latest.get("creator", {}).get("username", "Bilinmiyor")

    payload = {
        "username": "Zafer Yayından Klipler",
        "avatar_url": latest["channel"]["profile_picture"],
        "embeds": [
            {
                "title": f"🎬 {title}",
                "url": clip_url,
                "color": 65280,
                "image": {
                    "url": thumbnail
                },
                "fields": [
                    {
                        "name": "👤 Klibi Alan Kişi",
                        "value": creator,
                        "inline": False
                    },
                    {
                        "name": "🔗 Klip Linki",
                        "value": clip_url,
                        "inline": False
                    }
                ],
                "footer": {
                    "text": "Kick Klip Bildirimi"
                }
            }
        ]
    }

    requests.post(WEBHOOK_URL, json=payload, timeout=30)

    with open(LAST_ID_FILE, "w", encoding="utf-8") as f:
        f.write(latest_id)

    print("Yeni klip gönderildi.")

else:
    print("Yeni klip yok.")
