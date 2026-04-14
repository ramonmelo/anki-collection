"""
Populate Audio and Image fields for all notes in an Anki deck.

Audio: Google TTS (gTTS) — free, no API key.
Images: DuckDuckGo image search — free, no API key.

Prerequisites:
  1. Install dependencies:  pip install gtts ddgs requests
  2. Install AnkiConnect add-on in Anki (code: 2055492159)
  3. Have Anki running with AnkiConnect active

Usage:
  python populate_audio_image.py
"""

import json
import os
import re
import time
import urllib.request

import requests
from ddgs import DDGS
from gtts import gTTS

ANKI_CONNECT_URL = "http://localhost:8765"
DECK_NAME = "<REPLACE WITH YOUR DECK NAME>"
SOURCE_FIELD = "Front"  # field containing Ukrainian text
BACK_FIELD = "Back"     # field containing English text (used for image search)
AUDIO_FIELD = "Audio"
IMAGE_FIELD = "Image"
LANG = "uk"

POPULATE_AUDIO = True
POPULATE_IMAGES = True


def anki_request(action, **params):
    payload = json.dumps({"action": action, "version": 6, "params": params})
    req = urllib.request.Request(ANKI_CONNECT_URL, data=payload.encode("utf-8"))
    req.add_header("Content-Type", "application/json")
    response = json.loads(urllib.request.urlopen(req).read())
    if response.get("error"):
        raise Exception(f"AnkiConnect error: {response['error']}")
    return response["result"]


def clean_text(text):
    """Remove HTML tags and extra whitespace."""
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def generate_audio(text, filepath):
    """Generate an mp3 file from Ukrainian text using gTTS."""
    tts = gTTS(text=text, lang=LANG)
    tts.save(filepath)


def fetch_image(query, filepath):
    """Search DuckDuckGo for an image and download the first result."""
    with DDGS() as ddgs:
        results = list(ddgs.images(query, max_results=5))

    for result in results:
        try:
            resp = requests.get(result["image"], timeout=10, headers={
                "User-Agent": "Mozilla/5.0"
            })
            if resp.status_code == 200 and len(resp.content) > 1000:
                with open(filepath, "wb") as f:
                    f.write(resp.content)
                return True
        except Exception:
            continue
    return False


def main():
    note_ids = anki_request("findNotes", query=f'"deck:{DECK_NAME}"')
    if not note_ids:
        print(f"No notes found in deck '{DECK_NAME}'.")
        return

    notes = anki_request("notesInfo", notes=note_ids)
    print(f"Found {len(notes)} notes in '{DECK_NAME}'.")

    media_dir = anki_request("getMediaDirPath")
    print(f"Media folder: {media_dir}")

    audio_gen = 0
    audio_skip = 0
    image_gen = 0
    image_skip = 0

    for note in notes:
        fields = note["fields"]
        note_id = note["noteId"]
        updates = {}

        # --- Audio ---
        if POPULATE_AUDIO:
            has_audio = fields.get(AUDIO_FIELD, {}).get("value", "").strip()
            source_text = clean_text(fields.get(SOURCE_FIELD, {}).get("value", ""))

            if has_audio or not source_text:
                audio_skip += 1
            else:
                filename = f"anki_tts_{note_id}.mp3"
                filepath = os.path.join(media_dir, filename)
                try:
                    generate_audio(source_text, filepath)
                    updates[AUDIO_FIELD] = f"[sound:{filename}]"
                    audio_gen += 1
                    print(f"  Audio: {source_text[:50]}...")
                except Exception as e:
                    print(f"  Audio error on {note_id}: {e}")

        # --- Image ---
        if POPULATE_IMAGES:
            has_image = fields.get(IMAGE_FIELD, {}).get("value", "").strip()
            back_text = clean_text(fields.get(BACK_FIELD, {}).get("value", ""))

            if has_image or not back_text:
                image_skip += 1
            else:
                ext = "jpg"
                filename = f"anki_img_{note_id}.{ext}"
                filepath = os.path.join(media_dir, filename)
                try:
                    if fetch_image(back_text, filepath):
                        updates[IMAGE_FIELD] = f'<img src="{filename}">'
                        image_gen += 1
                        print(f"  Image: {back_text[:50]}...")
                    else:
                        print(f"  No image found for: {back_text[:50]}...")
                except Exception as e:
                    print(f"  Image error on {note_id}: {e}")
                # Be polite to DuckDuckGo
                time.sleep(1)

        # --- Update note ---
        if updates:
            anki_request(
                "updateNoteFields",
                note={"id": note_id, "fields": updates},
            )

    print(f"\nDone!")
    print(f"  Audio — generated: {audio_gen}, skipped: {audio_skip}")
    print(f"  Images — generated: {image_gen}, skipped: {image_skip}")


if __name__ == "__main__":
    main()
