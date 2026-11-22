"""Unit checks for the CAD-owned generic model producer's catalog boundary."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / "scripts" / "ci"
sys.path.insert(0, str(CI))


def load_module():
    spec = importlib.util.spec_from_file_location(
        "model_verify", CI / "model_verify.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ModelVerifyRunnerTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_plate_and_vent_plate_derive_members_from_catalog(self):
        for item, folder in (
            ("plate", "models/basic/plate"),
            ("vent-plate", "models/basic/vent_plate"),
        ):
            with self.subTest(item=item):
                with patch.dict(os.environ, {
                    "CAD_CI_ITEM": item,
                    "CAD_CI_ITEM_PATH": str(ROOT / folder),
                }):
                    self.assertEqual(self.module.selected_models(), (item,))

    def test_wrong_item_identity_fails_closed(self):
        with patch.dict(os.environ, {
            "CAD_CI_ITEM": "vent-plate",
            "CAD_CI_ITEM_PATH": str(ROOT / "models/basic/plate"),
        }):
            with self.assertRaisesRegex(RuntimeError, "identity mismatch"):
                self.module.selected_models()

    def test_unknown_root_is_rejected(self):
        with patch.dict(os.environ, {
            "CAD_CI_ITEM": "unknown",
            "CAD_CI_ITEM_PATH": str(ROOT / "models/basic/unknown"),
        }):
            with self.assertRaisesRegex(RuntimeError, "no catalog variants"):
                self.module.selected_models()

    def test_scpc_compilation_consumes_one_shared_wheel(self):
        import inspect
        source = inspect.getsource(self.module.compile_scpc)
        self.assertIn("scpc_wheel", source)
        self.assertNotIn("ensure_checkout", source)
        config = (ROOT / "cad-ci.yml").read_text(encoding="utf-8")
        self.assertIn("- scpc-package", config)

    def test_independent_scpc_is_discovered_from_the_catalog(self):
        from model_catalog import COMMAND_SOURCES
        self.assertIn("plate", COMMAND_SOURCES)
        self.assertIn("vent-plate", COMMAND_SOURCES)
        self.assertNotIn("bracket", COMMAND_SOURCES)


if __name__ == "__main__":
    unittest.main()
