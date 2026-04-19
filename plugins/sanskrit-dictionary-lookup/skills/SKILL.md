---
name: sanskrit-dictionary-lookup
description: Look up Sanskrit headwords through the shared repo core and return normalized scholarly JSON. Use this when you need structured dictionary results rather than ad hoc browsing.
---

# Sanskrit Dictionary Lookup

Use the shared lookup library in `src/lib` through the repo-local plugin service wrapper:

```powershell
python plugins/sanskrit-dictionary-lookup/scripts/lookup_word.py --word deva
```

## Behavior

- Output must stay JSON-only on stdout.
- Default dictionaries are `mw` and `ap90`.
- Input schemes supported by the shared core are `auto`, `iast`, `hk`, `slp1`, `itrans`, and `devanagari`.
- The wrapper is intentionally thin and delegates to `src/service/plugin/lookup_word.py`, so future MCP or agent wrappers can reuse the same core package.

## Dictionary Data

By default the shared core calls the C-SALT REST API:

- `https://api.c-salt.uni-koeln.de/dicts/<dict>/restful/entries`

You can override the API base URL via:

- `SANSKRIT_LOOKUP_API_BASE_URL`

Current implemented dictionary codes in this wrapper:

- `mw`
- `ap90`

The wrapper normalizes the `data.entries` REST response into shared repo types so future MCP or agent wrappers can reuse the same behavior.
