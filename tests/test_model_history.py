"""Contract tests for derived model Git-history presentation data."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "ci"))

from model_history import build_manifest, physical_model_roots, write_manifest  # noqa: E402


class ModelHistoryTests(unittest.TestCase):
    def test_history_uses_physical_model_roots_without_second_catalog(self):
        roots = physical_model_roots()
        self.assertEqual(len(roots), 17)
        self.assertIn("basic/plate", roots)
        self.assertIn("advanced/simple_mft", roots)
        self.assertNotIn("simple-mft-assembly", roots)

    def test_manifest_contains_only_source_and_root_timestamps(self):
        roots = physical_model_roots()
        values = {
            root: f"2026-11-{index + 1:02d}T12:00:00+00:00"
            for index, root in enumerate(roots)
        }

        manifest = build_manifest(
            source_commit="a" * 40,
            expected_source="a" * 40,
            lastmod_resolver=lambda model_root, root: values[model_root],
        )

        self.assertEqual(set(manifest), {"schema", "source_commit", "roots"})
        self.assertEqual(manifest["schema"], 1)
        self.assertEqual(manifest["source_commit"], "a" * 40)
        self.assertEqual(tuple(manifest["roots"]), roots)
        self.assertEqual(manifest["roots"]["basic/plate"], values["basic/plate"])

    def test_expected_source_mismatch_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "source mismatch"):
            build_manifest(
                source_commit="b" * 40,
                expected_source="a" * 40,
                lastmod_resolver=lambda model_root, root: "2026-11-01T00:00:00+00:00",
            )

    def test_model_yml_does_not_gain_hand_maintained_updated_field(self):
        for path in ROOT.glob("models/*/*/model.yml"):
            text = path.read_text(encoding="utf-8")
            self.assertNotRegex(text, r"(?m)^updated\s*:")

    def test_manifest_writer_creates_hugo_data_file(self):
        manifest = {
            "schema": 1,
            "source_commit": "c" * 40,
            "roots": {"basic/plate": "2026-11-01T00:00:00+00:00"},
        }
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "data" / "cad" / "model_history.json"
            write_manifest(path, manifest)
            self.assertEqual(json.loads(path.read_text()), manifest)


if __name__ == "__main__":
    unittest.main()
