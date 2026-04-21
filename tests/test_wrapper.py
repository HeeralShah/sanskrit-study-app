from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from support_api_server import serve_test_api

WRAPPER_SCRIPT = REPO_ROOT / "plugins" / "sanskrit-dictionary-lookup" / "scripts" / "lookup_word.py"


class WrapperTests(unittest.TestCase):
    def test_wrapper_outputs_json(self) -> None:
        with serve_test_api() as api_base_url:
            env = os.environ.copy()
            env["SANSKRIT_LOOKUP_API_BASE_URL"] = api_base_url
            completed = subprocess.run(
                [sys.executable, str(WRAPPER_SCRIPT), "--word", "deva", "--indent", "0"],
                check=True,
                capture_output=True,
                text=True,
                cwd=REPO_ROOT,
                env=env,
            )
            payload = json.loads(completed.stdout)
            self.assertEqual(payload["canonical_query"], "deva")
            self.assertEqual(payload["results"][0]["dictionary"], "mw")
            self.assertEqual(payload["results"][1]["dictionary"], "ap90")
            self.assertIn("definitions_english", payload["results"][0])


if __name__ == "__main__":
    unittest.main()
