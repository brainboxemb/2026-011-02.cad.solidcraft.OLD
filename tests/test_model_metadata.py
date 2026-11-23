"""Contract: local model.yml is the only CAD catalog/website content source.

The CRC is a frozen migration baseline of the previous Python MODELS table:
it protects public model descriptions, card order, stages, source links and
warnings from accidental change during the model.yml cut-over. It is NOT a
second editable catalog.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest
import zlib

import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "ci"))

from model_catalog import (  # noqa: E402
    COMMAND_SOURCES,
    MODELS,
    SECTIONS,
    load_models,
    model_metadata_paths,
    verification_input_paths,
    _model_entry,
)


class ModelMetadataTests(unittest.TestCase):
    def test_all_catalog_variants_come_from_local_model_yaml(self):
        metadata = sorted(ROOT.glob("models/*/*/model.yml"))
        self.assertEqual(len(metadata), 16)
        self.assertEqual(len(MODELS), 18)
        self.assertEqual(len(COMMAND_SOURCES), 5)
        self.assertEqual(
            {item.parent for item in metadata},
            {item.parent for item in ROOT.glob("models/*/*/ci.yml")},
        )
        self.assertEqual(MODELS, load_models())
        self.assertEqual(
            tuple(MODELS)[:3],
            ("plate", "vent-plate", "bolted-flange"),
        )
        self.assertEqual(
            tuple(MODELS)[-2:],
            ("hub75-wood-frame", "hub75-display2"),
        )
        self.assertEqual(
            tuple(SECTIONS),
            ("basic", "components", "advanced"),
        )

    def test_unchanged_previous_public_model_content_and_order(self):
        previous_fields = {
            "source", "section", "title", "tagline", "description",
            "parameters", "diagram", "stages", "scpc_source",
            "native", "native_snapshot_required",
            "component_source", "component_definition_primary",
            "extra_inputs", "dependencies", "warning", "featured",
        }
        rows = [
            [slug, {key: data[key] for key in data if key in previous_fields}]
            for slug, data in MODELS.items()
        ]
        payload = json.dumps(
            rows, ensure_ascii=False, separators=(",", ":"), sort_keys=True,
        ).encode("utf-8")
        actual_crc = zlib.crc32(payload)
        self.assertEqual(
            actual_crc, 0x7F00EA57,
            "Migration changed the established public model content/order; "
            f"actual CRC is {actual_crc:#010x}",
        )

    def test_scpc_command_count_is_not_model_metadata(self):
        path = ROOT / "models/basic/plate/model.yml"
        document = yaml.safe_load(path.read_text(encoding="utf-8"))
        info = {key: value for key, value in document.items() if key != "section"}
        info["scpc_command_count"] = 9

        with self.assertRaisesRegex(
            ValueError, r"unknown metadata keys .*scpc_command_count"
        ):
            _model_entry(
                "plate",
                info,
                "basic",
                Path("models/basic/plate"),
                path,
            )

    def test_model_metadata_does_not_change_geometry_fingerprints(self):
        for slug in MODELS:
            with self.subTest(slug=slug):
                metadata = model_metadata_paths(slug)
                self.assertTrue(any(path.endswith("/model.yml") for path in metadata))
                geometry_inputs = verification_input_paths(slug)
                self.assertFalse(
                    any(path.endswith("/model.yml") for path in geometry_inputs)
                )
                self.assertTrue((ROOT / MODELS[slug]["source"]).is_file())

    def test_model_variants_and_warnings_are_data_only(self):
        guide = (ROOT / "models/components/guide_rail/model.yml").read_text()
        mft = (ROOT / "models/advanced/simple_mft/model.yml").read_text()
        self.assertIn("variants:", guide)
        self.assertIn("guide-rail-makita:", guide)
        self.assertIn("variants:", mft)
        self.assertIn("simple-mft-assembly:", mft)
        self.assertIn("WARNING", MODELS["guide-rail"]["warning"]["title"])
        self.assertIn("extra_views", MODELS["simple-mft"])
        self.assertIn("extra_views", MODELS["hub75-panel"])

    def test_no_python_catalog_or_model_specific_view_hacks(self):
        catalog = (ROOT / "scripts/ci/model_catalog.py").read_text()
        adapter = (ROOT / "site/content/models/_content.gotmpl").read_text()
        page = (ROOT / "site/layouts/models/single.html").read_text()
        self.assertIn("MODELS = load_models()", catalog)
        self.assertNotIn("MODELS = {", catalog)
        self.assertIn("hugo.Data.cad.models", adapter)
        self.assertIn("extra_views", adapter)
        self.assertIn("extra_views", page)
        self.assertNotIn('if eq $slug "simple-mft"', adapter)
        self.assertNotIn('if eq $slug "hub75-panel"', adapter)


if __name__ == "__main__":
    unittest.main()
