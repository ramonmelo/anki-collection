**Create a new Anki import file for the theme: {{args}}.**

If {{args}} points to an existing file:
- If it follows the format below, revise items for better quality and relevance.
- If it's a word list (one per line), create items for all words following the format below.

### Format (Tab-Separated)
```txt
#separator:tab
#html:true
#tags column:5
<FRONT>\t<BACK>\t<EXAMPLE>\t<EXAMPLE TRANSLATED>\t<TAG>
```

### Content Requirements
- **Quality over quantity**: Include diverse parts of speech (noun, adjective, verb, preposition, etc.), but only items directly relevant to the theme.
- **Field Specifications**:
  - **FRONT**: Ukrainian word or phrase. For verbs, use both aspects (e.g., "писати/написати").
  - **BACK**: English translation.
  - **EXAMPLE**: Natural Ukrainian phrase (A1-A2 level, max 10 words) with the target word wrapped in `<b>` tags. Example: `Я бачу <b>велику</b> хмару`.
  - **EXAMPLE TRANSLATED**: English translation of the example.
  - **TAG**: Space-separated tags including:
    - Part of speech (Ukrainian, e.g., "іменник").
    - Metadata: gender (nouns), aspect (verbs), degree (adjectives), case (prepositions).
    - Theme: Use the core part of {{args}} (e.g., for "Ukrainian weather" → "weather").

### Output
Provide the full tab-separated content. Suggest saving to `ukrainian_{{args}}.txt` at the root folder.