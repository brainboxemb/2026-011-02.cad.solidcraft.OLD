"""Tests for Forge dependency compatibility with the CAD toolchain."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "ci"))


def load_module():
    path = ROOT / "scripts" / "ci" / "forge_dependency.py"
    spec = importlib.util.spec_from_file_location("forge_dependency", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ForgeDependencyTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_expected_solidcraft_version_comes_from_toolchain(self):
        self.assertEqual(
            self.module.expected_solidcraft_version(ROOT),
            "0.48.1",
        )

    def test_forge_tested_version_is_read_from_package_contract(self):
        with TemporaryDirectory() as directory:
            source = Path(directory)
            package = source / "scpf"
            package.mkdir()
            (package / "version.py").write_text(
                'TESTED_SOLIDCRAFT_VERSION = "0.48.1"\n',
                encoding="utf-8",
            )
            self.assertEqual(
                self.module.forge_tested_solidcraft_version(source),
                "0.48.1",
            )

    def test_missing_forge_version_contract_is_rejected(self):
        with TemporaryDirectory() as directory:
            source = Path(directory)
            package = source / "scpf"
            package.mkdir()
            (package / "version.py").write_text("# no version\n", encoding="utf-8")
            with self.assertRaisesRegex(
                RuntimeError,
                "TESTED_SOLIDCRAFT_VERSION",
            ):
                self.module.forge_tested_solidcraft_version(source)


if __name__ == "__main__":
    unittest.main()
