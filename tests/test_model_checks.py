"""Contracts for optional model-owned snapshot presentation settings."""

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / "scripts" / "ci"
sys.path.insert(0, str(CI))

from model_catalog import MODELS  # noqa: E402
from model_checks import check_path, extra_snapshots, load_check, snapshot_camera  # noqa: E402


class ModelOwnedPresentationSettingsTests(unittest.TestCase):
    def test_present_check_modules_are_physical_model_root_settings(self):
        expected = {
            "hub75-display2",
            "hub75-screen",
            "hub75-wood-frame",
            "hub75-panel",
            "flex-bench-dog",
        }
        actual = {slug for slug in MODELS if check_path(slug).is_file()}
        self.assertEqual(actual, expected)
        for slug in actual:
            with self.subTest(slug=slug):
                self.assertIsNotNone(load_check(slug))
                self.assertIsInstance(snapshot_camera(slug), dict)

    def test_flex_bench_dog_owns_underside_review_view(self):
        views = extra_snapshots("flex-bench-dog")
        self.assertEqual([item["name"] for item in views], ["underside.png"])
        self.assertIsInstance(views[0].get("camera"), dict)

    def test_hub75_panel_owns_two_extra_face_views(self):
        views = extra_snapshots("hub75-panel")
        self.assertEqual([item["name"] for item in views], ["front.png", "rear.png"])
        self.assertTrue(all(isinstance(item.get("camera"), dict) for item in views))


if __name__ == "__main__":
    unittest.main()
