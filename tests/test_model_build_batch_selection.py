"""Selection-contract tests for the shared CAD model-build batch."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
from unittest.mock import patch
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "ci" / "model_build_batch.py"


def load_module():
    spec = importlib.util.spec_from_file_location("model_build_batch", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ModelBuildBatchSelectionTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def active(self, value):
        with patch.dict(
            os.environ,
            {"CAD_CI_ACTIVE_DEPENDENTS_JSON": value},
            clear=False,
        ):
            return self.module.active_model_roots()

    def test_one_model_selects_only_that_physical_root(self):
        roots = self.active('["flex-bench-dog"]')
        self.assertEqual(
            roots,
            ((Path("models/components/flex_bench_dog"), ("flex-bench-dog",)),),
        )

    def test_multi_variant_item_keeps_only_its_owned_variants(self):
        roots = self.active('["guide-rail"]')
        self.assertEqual(len(roots), 1)
        self.assertEqual(roots[0][0], Path("models/components/guide_rail"))
        self.assertEqual(
            set(roots[0][1]),
            {"guide-rail", "guide-rail-makita"},
        )

    def test_empty_selection_is_valid(self):
        self.assertEqual(self.active("[]"), ())

    def test_unknown_item_is_rejected(self):
        with self.assertRaisesRegex(
            RuntimeError,
            "unexpected model batch direct dependent",
        ):
            self.active('["not-a-cad-model"]')

    def test_duplicate_item_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "unique string list"):
            self.active('["flex-bench-dog", "flex-bench-dog"]')

    def test_missing_context_is_rejected(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(
                RuntimeError,
                "CAD_CI_ACTIVE_DEPENDENTS_JSON is required",
            ):
                self.module.active_model_roots()


if __name__ == "__main__":
    unittest.main()
