"""Tests for exact external CAD dependency checkouts."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load_module():
    path = ROOT / "scripts" / "ci" / "bootstrap_cad_ci.py"
    spec = importlib.util.spec_from_file_location("bootstrap_cad_ci", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def commit(repo: Path, text: str) -> str:
    (repo / "tool.txt").write_text(text, encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-qm", text], cwd=repo, check=True)
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=repo, text=True
    ).strip()


def manifest(root: Path, name: str, url: str, sha: str) -> None:
    (root / "dependencies.repos").write_text(
        "repositories:\n"
        f"  {name}:\n"
        "    type: git\n"
        f"    url: {url}\n"
        f"    version: {sha}\n",
        encoding="utf-8",
    )


class BootstrapCadCiTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_repository_pins_are_exact(self):
        expected = {
            "scpf": "ea5710a5d2d33b0633b93c5da95dd5b74f126aa4",
            "scpc": "fcaa6f9fc8388bc715fcd2fbb149ce6b979566a7",
        }
        for name, sha in expected.items():
            _, actual = self.module.dependency(name)
            self.assertEqual(actual, sha)

    def test_checkout_moves_to_new_exact_revision(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            upstream = root / "upstream"
            upstream.mkdir()
            subprocess.run(["git", "init", "-q"], cwd=upstream, check=True)
            subprocess.run(
                ["git", "config", "user.email", "test@example.invalid"],
                cwd=upstream,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test"],
                cwd=upstream,
                check=True,
            )
            first = commit(upstream, "first")
            second = commit(upstream, "second")
            target = root / "ext" / "scpf"

            manifest(root, "scpf", str(upstream), first)
            self.assertEqual(
                self.module.ensure_checkout("scpf", root, target=target),
                first,
            )

            manifest(root, "scpf", str(upstream), second)
            self.assertEqual(
                self.module.ensure_checkout("scpf", root, target=target),
                second,
            )

    def test_tracked_changes_are_not_overwritten(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            upstream = root / "upstream"
            upstream.mkdir()
            subprocess.run(["git", "init", "-q"], cwd=upstream, check=True)
            subprocess.run(
                ["git", "config", "user.email", "test@example.invalid"],
                cwd=upstream,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test"],
                cwd=upstream,
                check=True,
            )
            first = commit(upstream, "first")
            second = commit(upstream, "second")
            target = root / "ext" / "scpc"

            manifest(root, "scpc", str(upstream), first)
            self.module.ensure_checkout("scpc", root, target=target)
            (target / "tool.txt").write_text("local edit", encoding="utf-8")
            manifest(root, "scpc", str(upstream), second)

            with self.assertRaisesRegex(RuntimeError, "tracked local changes"):
                self.module.ensure_checkout("scpc", root, target=target)


if __name__ == "__main__":
    unittest.main()
