"""Tests for the released central SolidCraft runtime contract."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / "scripts" / "ci"
sys.path.insert(0, str(CI))


def load_module():
    path = ROOT / "scripts" / "ci" / "cad_runtime.py"
    spec = importlib.util.spec_from_file_location("cad_runtime", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class CadRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_repository_uses_released_central_runtime(self):
        data = self.module.load_toolchain()
        self.assertEqual(
            data["runtime_image"],
            "ghcr.io/brainboxemb/cad-solidcraft:v0.3.4",
        )
        self.assertEqual(data["solidcraft"], "0.45.0")

    def test_mutable_runtime_tags_are_rejected(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "ci").mkdir()
            for reference in (
                "ghcr.io/brainboxemb/cad-solidcraft:edge",
                "ghcr.io/brainboxemb/cad-solidcraft:latest",
                "ghcr.io/brainboxemb/other:v0.3.2",
            ):
                (root / "ci/toolchain.json").write_text(
                    json.dumps({
                        "schema": 2,
                        "runtime_image": reference,
                        "solidcraft": "0.42.0",
                    }),
                    encoding="utf-8",
                )
                with self.assertRaisesRegex(ValueError, "immutable released"):
                    self.module.load_toolchain(root)

    def test_metadata_keeps_consumer_pins_outside_runtime(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "ci").mkdir()
            (root / "ext/scpf/scpf").mkdir(parents=True)
            (root / "ci/toolchain.json").write_text(
                json.dumps({
                    "schema": 2,
                    "runtime_image": "ghcr.io/brainboxemb/cad-solidcraft:v9.8.7",
                    "solidcraft": "1.2.3",
                }),
                encoding="utf-8",
            )
            (root / "ext/scpf/scpf/pyproject.toml").write_text(
                '[project]\nname="scpf"\nversion="7.6.5"\n',
                encoding="utf-8",
            )
            with patch.object(
                self.module,
                "dependency",
                side_effect=[
                    ("https://example/scpf.git", "1" * 40),
                    ("https://example/scpc.git", "2" * 40),
                ],
            ):
                data = self.module.metadata(root)

        self.assertEqual(data["reference"], "ghcr.io/brainboxemb/cad-solidcraft:v9.8.7")
        self.assertEqual(data["scpf_sha"], "1" * 40)
        self.assertEqual(data["scpc_sha"], "2" * 40)
        self.assertEqual(data["scpf_release"], "7.6.5")


if __name__ == "__main__":
    unittest.main()
