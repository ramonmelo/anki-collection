# Remaining Improvements

Below are all suggested changes from the initial review that are **not yet implemented**. Items 5 and 2 were completed (prompt whitespace dedent + shared `config.py`).

---

## Package structure

- [x] Add `scripts/__init__.py` so `scripts/` becomes a proper Python package
- [x] Replace the `sys.path.append` hack in `review_cards.py` with a proper import
- [x] Add type hints to all function signatures

## Error handling & robustness

- [ ] Add error handling for ollama connection failures / missing models in all scripts
- [ ] Add retry logic with exponential backoff for all network calls (ollama, AnkiConnect, image downloads)
- [ ] Add `KeyError` guard for invalid language codes in `translate.py` (lookup into `LANGUAGE_NAMES`)
- [ ] Add per-image error handling in `image_extraction.py` — don't crash the whole batch on one bad image
- [ ] Add empty-string / whitespace guard in `build_vocab.py` loop (split produces `""` entries)
- [ ] Strip whitespace from split words in `build_vocab.py` to avoid false duplicates
- [ ] Make deduplication in `build_vocab.py` case-insensitive (add `word.lower()` to set)

## Performance

- [ ] Process image extraction calls in parallel (they are I/O-bound, waiting on ollama)
- [ ] Batch or parallelize LLM calls in `build_vocab.py` — currently sequential per word
- [ ] Dedup vocabulary across images in `image_extraction.py` (currently concatenates raw output per image)

## `review_cards.py`

- [ ] Use a single HTTP client (`requests` only) instead of mixing `urllib.request` and `requests`
- [ ] Fix `clean_text()` — lowercase-only mode mangles proper nouns and sentence starts; make it configurable
- [ ] Rename the shadowed `source_text` variable (line 184 reassigns it mid-function)
- [ ] Break up `main()` (~140 lines) into smaller focused functions
- [ ] Add `--dry-run` flag to preview changes without applying them
- [ ] Add checkpointing — if the script crashes mid-deck, resume where it left off
- [ ] Make the `"vocabulary"` tag configurable via CLI argument
- [ ] Replace DuckDuckGo image scraping (ToS concerns) with a proper API (e.g., Unsplash, Pexels)
- [ ] Replace `time.sleep(1)` with proper rate-limiting (exponential backoff or token bucket)
- [ ] Validate that required Anki fields exist before processing
- [ ] Handle network errors in `anki_request()` (connection refused, timeouts)
- [ ] Add `system=` parameter for ollama system prompts instead of stuffing everything into the user prompt in `generate_example.py` and `translate.py`

## `image_extraction.py`

- [ ] Make the extraction prompt configurable (currently a module-level constant)
- [ ] Add `--output` flag to write results to a file instead of stdout

## `build_vocab.py`

- [ ] Add `--output` flag to write results to a file
- [ ] Add `--source-lang` / `--target-lang` CLI flags (currently only uses config defaults)
- [ ] Handle the case where `extract_vocabulary_from_folder` returns `None`

## `create_vocab_prompt.md`

- [ ] Formalize the `{{args}}` template system — what processes it?
- [ ] Add input validation rules for the generated tab-separated format
- [ ] Formalize the "extract theme from args" logic currently described only in prose

## Testing & quality

- [ ] Add unit tests for all scripts
- [ ] Add structured logging (`logging` module) instead of `print()`
