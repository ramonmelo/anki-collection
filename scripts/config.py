import os

GENERATE_MODEL = os.environ.get("ANKI_GENERATE_MODEL", "gemma4:12b")
TRANSLATE_MODEL = os.environ.get("ANKI_TRANSLATE_MODEL", "translategemma:4b")
EXTRACT_MODEL = os.environ.get("ANKI_EXTRACT_MODEL", "gemma4:12b")

SOURCE_LANG = os.environ.get("ANKI_SOURCE_LANG", "uk")
TARGET_LANG = os.environ.get("ANKI_TARGET_LANG", "en")

LANGUAGE_NAMES = {"en": "English", "uk": "Ukrainian"}
