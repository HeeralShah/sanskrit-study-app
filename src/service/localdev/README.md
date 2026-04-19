# Local Development Tools

This folder contains runnable service entrypoints for local development and testing of the Sanskrit Study App.

## CLI Tool: Sanskrit Dictionary Lookup

The `run_cli.py` script provides a command-line interface for looking up Sanskrit headwords across multiple dictionaries.

### Prerequisites

- Python 3.8+
- Access to the Sanskrit dictionary API (default: https://api.c-salt.uni-koeln.de)

### Usage

```bash
python run_cli.py [OPTIONS]
```

### Options

- `--word WORD`: Headword to search for (required)
- `--dictionary DICT`: Dictionary ID to query (repeatable). Defaults to 'mw' and 'ap90'
  - Available: mw (Monier-Williams), ap90 (Apte Practical), ap (Apte), vcp (Vacaspatyam), ben (Benfey), etc.
- `--input-scheme SCHEME`: Input interpretation scheme. Default: 'auto'
  - Options: auto, hk, slp1, devanagari, iast
- `--api-base-url URL`: Override the default API base URL
- `--response-style STYLE`: Output schema style. Default: `compact`
  - Options: `compact`, `full`
- `--full-output`: Legacy alias for `--response-style full`
- `--max-definition-chars N`: Trim length per definition in compact mode. Default: 220
- `--indent INDENT`: JSON indentation level. Default: 2

### Examples

#### Basic lookup
```bash
python run_cli.py --word deva
```

#### Lookup with specific dictionary
```bash
python run_cli.py --word deva --dictionary mw
```

#### Lookup with custom indentation
```bash
python run_cli.py --word deva --indent 0
```

#### Full normalized payload (debug)
```bash
python run_cli.py --word deva --response-style full
```

#### Lookup with different input scheme
```bash
python run_cli.py --word deva --input-scheme devanagari
```

### Output

The tool outputs a JSON object containing:
- Query information and transliterations
- Dictionary results with entries
- Metadata for each dictionary entry
- Any issues encountered

### Testing with Mock API

For testing purposes, you can use the test API server included in the project:

```python
from tests.support_api_server import serve_test_api
import os

with serve_test_api() as api_base_url:
    os.environ["SANSKRIT_LOOKUP_API_BASE_URL"] = api_base_url
    # Then run the CLI
```

### Running from Repository Root

To run from the repository root:

```bash
python src/service/localdev/run_cli.py --word deva --indent 0
```

### Integration with VS Code

You can configure VS Code tasks to run this tool. Add to `.vscode/tasks.json`:

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Lookup Sanskrit Word",
            "type": "shell",
            "command": "python",
            "args": ["src/service/localdev/run_cli.py", "--word", "${input:word}"],
            "group": "test",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            }
        }
    ],
    "inputs": [
        {
            "id": "word",
            "description": "Sanskrit word to lookup",
            "default": "deva",
            "type": "promptString"
        }
    ]
}
```

