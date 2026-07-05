"""Upload out.mp4 to YouTube and add it to the motivational playlist.

Reads quote.txt / author.txt for the title & description, and these env vars
(set as GitHub Actions secrets):
    YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN, YT_PLAYLIST_ID

The title is prefixed with an incrementing Japanese day counter (一日, 二日, …)
derived from the number of videos already in the playlist.
"""
import os

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read().strip()


def to_kanji(n):
    """Integer -> Japanese kanji numerals (1->一, 6->六, 10->十, 100->百, 365->三百六十五)."""
    if n <= 0:
        return "〇"
    if n >= 10000:
        man, rem = divmod(n, 10000)
        return to_kanji(man) + "万" + (to_kanji(rem) if rem else "")
    digits = "〇一二三四五六七八九"
    units = ["", "十", "百", "千"]
    parts = []
    place = 0
    while n > 0:
        d = n % 10
        if d:
            parts.append(units[place] if (d == 1 and place > 0) else digits[d] + units[place])
        n //= 10
        place += 1
    return "".join(reversed(parts))


def playlist_total(youtube, playlist_id):
    resp = youtube.playlistItems().list(
        part="id", playlistId=playlist_id, maxResults=1
    ).execute()
    return resp.get("pageInfo", {}).get("totalResults", 0)


quote = read("quote.txt")
author = read("author.txt")

creds = Credentials(
    None,
    refresh_token=os.environ["YT_REFRESH_TOKEN"],
    token_uri="https://oauth2.googleapis.com/token",
    client_id=os.environ["YT_CLIENT_ID"],
    client_secret=os.environ["YT_CLIENT_SECRET"],
    scopes=[
        "https://www.googleapis.com/auth/youtube.upload",
        "https://www.googleapis.com/auth/youtube",
    ],
)

youtube = build("youtube", "v3", credentials=creds)

playlist_id = os.environ["YT_PLAYLIST_ID"]
day = playlist_total(youtube, playlist_id) + 1
counter = f"{to_kanji(day)}日"
print(f"Day {day} -> {counter}")

# YouTube titles: max 100 chars, no "<" or ">".
prefix = f"{counter}｜"
suffix = " #Shorts"
body = f'"{quote}" — {author}'.replace("<", "").replace(">", "")
budget = 100 - len(prefix) - len(suffix)
if len(body) > budget:
    body = body[: budget - 1] + "…"
title = f"{prefix}{body}{suffix}"

description = (
    f"{counter}\n\n"
    f'"{quote}"\n\n— {author}\n\n'
    "#motivation #quotes #shorts #daily #inspiration"
)

print("Uploading video...")
request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["motivation", "quotes", "shorts", "daily", "inspiration"],
            "categoryId": "22",  # People & Blogs
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
        },
    },
    media_body=MediaFileUpload("out.mp4", chunksize=-1, resumable=True, mimetype="video/mp4"),
)
# Resumable uploads must be driven with next_chunk() (the official YouTube pattern),
# not execute(). chunksize=-1 sends the whole file in a single chunk.
response = None
while response is None:
    _status, response = request.next_chunk()
video_id = response["id"]
print(f"Uploaded: https://youtu.be/{video_id}")

youtube.playlistItems().insert(
    part="snippet",
    body={
        "snippet": {
            "playlistId": playlist_id,
            "resourceId": {"kind": "youtube#video", "videoId": video_id},
        }
    },
).execute()
print(f"Added to playlist {playlist_id}")
