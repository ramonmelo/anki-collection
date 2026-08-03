# Anki Collection — agent guide

## Project

Ukrainian Anki flashcards generated via local ollama models. Scripts in `scripts/`, card HTML/CSS in `card-design/`, tab-separated vocab files (`ukrainian_*.txt`) in root.

## Config

All in `scripts/config.py` — overridable via env vars:
- `ANKI_GENERATE_MODEL` (default `gemma4:12b`)
- `ANKI_TRANSLATE_MODEL` (default `translategemma:4b`)
- `ANKI_EXTRACT_MODEL` (default `gemma4:12b`)
- `ANKI_SOURCE_LANG` / `ANKI_TARGET_LANG` (default `uk` / `en`)

Ollama must be running locally with the configured models pulled.

## Key commands

```bash
# Build vocabulary from images in a folder
python scripts/build_vocab.py path/to/images/

# Extract vocabulary from folder (standalone)
python scripts/image_extraction.py path/to/images/

# Translate text
python scripts/translate.py <text>

# Generate example sentence
python scripts/generate_example.py <word>

# Populate Anki card fields (audio, images, examples) — AnkiConnect required
python scripts/review_cards.py --deck "Deck Name" --lang uk

# Validate tab-separated vocab files (8 columns)
python scripts/check_file.py ukrainian_*.txt
```

## Architecture notes

- `scripts/` is **not** a package (no `__init__.py`). `review_cards.py` uses `sys.path.append` hack to import siblings.
- `scripts/config.py` is the shared config module.
- Two Anki card types in `card-design/`: Card 1 (Front→Back+Example), Card 2 (Back→Front+Example). Both share `style.css` and use fields: Front, Back, Example, ExampleTranslated, Audio, AudioExample, Image.
- `review_cards.py` uses AnkiConnect (port 8765), gTTS (audio), DuckDuckGo (images), and calls `translate`/`generate_example` from sibling scripts.
- Known issues and planned improvements are tracked in `IMPROVEMENTS.md` — check before working on new features.

## Gotchas

- No `requirements.txt` or `pyproject.toml`. Dependencies: `ollama`, `gtts`, `ddgs`, `requests`.
- `DuckDuckGo` image scraping has ToS concerns (see `IMPROVEMENTS.md`).
- `review_cards.py` lowercases all text unconditionally (mangles proper nouns).
- Sequence scripts (`build_vocab.py`) make sequential ollama calls per word — slow on large sets.
- No tests, no linting/typecheck config exists.
- Tab-separated vocab files require exactly 8 columns — validated by `check_file.py`.
