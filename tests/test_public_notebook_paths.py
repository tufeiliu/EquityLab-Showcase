import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


class NotebookPathTests(unittest.TestCase):
    def test_locates_public_repo_from_unrelated_trash_cwd(self):
        root = Path(__file__).resolve().parents[1]
        notebook = json.loads((root / "notebooks" / "01_public_readout.ipynb").read_text())
        code = "".join(notebook["cells"][1]["source"])
        with tempfile.TemporaryDirectory() as tmp:
            fake_cwd = Path(tmp) / ".local" / "share" / "Trash" / "files" / "notebooks.8"
            fake_cwd.mkdir(parents=True)
            old = Path.cwd()
            try:
                os.chdir(fake_cwd)
                with patch.dict(os.environ, {"EQUITYLAB_PUBLIC_ROOT": str(root)}):
                    ns = {}
                    exec(code, ns)
                self.assertEqual(ns["root"], root)
                self.assertFalse(ns["primary"].empty)
                self.assertFalse(ns["hybrid"].empty)
            finally:
                os.chdir(old)
