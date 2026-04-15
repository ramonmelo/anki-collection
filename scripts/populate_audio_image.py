"""
Populate Audio and Image fields for all notes in an Anki deck.

Audio: Google TTS (gTTS) — free, no API key.
Images: DuckDuckGo image search — free, no API key.

Prerequisites:
  1. Install dependencies:  pip install gtts ddgs requests
  2. Install AnkiConnect add-on in Anki (code: 2055492159)
  3. Have Anki running with AnkiConnect active

Usage:
  python populate_audio_image.py --deck "My Deck Name" --lang uk
"""

import argparse
import json
import os
import re
import time
import urllib.request

import requests
from ddgs import DDGS
from gtts import gTTS


def parse_args():
    parser = argparse.ArgumentParser(
        description="Populate Audio and Image fields for Anki notes."
    )
    parser.add_argument("--anki-url", default="http://localhost:8765",
                        help="AnkiConnect URL (default: %(default)s)")
    parser.add_argument("--deck", default="Personal UA",
                        help="Anki deck name (default: %(default)s)")
    parser.add_argument("--source-field", default="Front",
                        help="Field containing source text for TTS (default: %(default)s)")
    parser.add_argument("--back-field", default="Back",
                        help="Field containing back text for image search (default: %(default)s)")
    parser.add_argument("--audio-field", default="Audio",
                        help="Field to store audio in (default: %(default)s)")
    parser.add_argument("--example-field", default="Example",
                        help="Field to store example in (default: %(default)s)")
    parser.add_argument("--audio-example-field", default="AudioExample",
                        help="Field to store example audio in (default: %(default)s)")
    parser.add_argument("--image-field", default="Image",
                        help="Field to store images in (default: %(default)s)")
    parser.add_argument("--lang", default="uk",
                        help="TTS language code (default: %(default)s)")
    parser.add_argument("--no-audio", action="store_true",
                        help="Skip audio generation")
    parser.add_argument("--no-images", action="store_true",
                        help="Skip image generation")
    return parser.parse_args()


def anki_request(url, action, **params):
    payload = json.dumps({"action": action, "version": 6, "params": params})
    req = urllib.request.Request(url, data=payload.encode("utf-8"))
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


def generate_audio(text, filepath, lang):
    """Generate an mp3 file from text using gTTS."""
    tts = gTTS(text=text, lang=lang)
    tts.save(filepath)


def fetch_image(query, filepath):
    """Search DuckDuckGo for an image and download the first result."""
    with DDGS() as ddgs:
        results = list(ddgs.images(query, max_results=5, size="Medium", type_image="photo", layout="Wide", license_image="Public"))

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


def main(args):
    note_ids = anki_request(args.anki_url, "findNotes", query=f'"deck:{args.deck}"')
    if not note_ids:
        print(f"No notes found in deck '{args.deck}'.")
        return

    notes = anki_request(args.anki_url, "notesInfo", notes=note_ids)
    print(f"Found {len(notes)} notes in '{args.deck}'.")

    media_dir = anki_request(args.anki_url, "getMediaDirPath")
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
        if not args.no_audio:
            # Main Audio
            has_audio = fields.get(args.audio_field, {}).get("value", "").strip()
            source_text = clean_text(fields.get(args.source_field, {}).get("value", ""))

            if has_audio or not source_text:
                audio_skip += 1
            else:
                filename = f"anki_tts_{note_id}.mp3"
                filepath = os.path.join(media_dir, filename)
                try:
                    generate_audio(source_text, filepath, args.lang)
                    updates[args.audio_field] = f"[sound:{filename}]"
                    audio_gen += 1
                    print(f"  Audio: {source_text[:50]}...")
                except Exception as e:
                    print(f"  Audio error on {note_id}: {e}")

            # Example Audio
            has_ex_audio = fields.get(args.audio_example_field, {}).get("value", "").strip()
            ex_text = clean_text(fields.get(args.example_field, {}).get("value", ""))

            if not has_ex_audio and ex_text:
                filename = f"anki_tts_ex_{note_id}.mp3"
                filepath = os.path.join(media_dir, filename)
                try:
                    generate_audio(ex_text, filepath, args.lang)
                    updates[args.audio_example_field] = f"[sound:{filename}]"
                    audio_gen += 1
                    print(f"  Example Audio: {ex_text[:50]}...")
                except Exception as e:
                    print(f"  Example Audio error on {note_id}: {e}")

        # --- Image ---
        if not args.no_images:
            has_image = fields.get(args.image_field, {}).get("value", "").strip()
            back_text = clean_text(fields.get(args.back_field, {}).get("value", ""))

            if has_image or not back_text:
                image_skip += 1
            else:
                ext = "jpg"
                filename = f"anki_img_{note_id}.{ext}"
                filepath = os.path.join(media_dir, filename)
                try:
                    if fetch_image(back_text, filepath):
                        updates[args.image_field] = f'<img src="{filename}">'
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
                args.anki_url,
                "updateNoteFields",
                note={"id": note_id, "fields": updates},
            )

    print(f"\nDone!")
    print(f"  Audio — generated: {audio_gen}, skipped: {audio_skip}")
    print(f"  Images — generated: {image_gen}, skipped: {image_skip}")


if __name__ == "__main__":
    main(parse_args())
