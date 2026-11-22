"""Guard the CAD-specific shared batch adapter, not a second CI planner."""

from __future__ import annotations

import ast
from pathlib import Path
import re
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / "scripts" / "ci"
sys.path.insert(0, str(CI))

from model_catalog import COMMAND_SOURCES, MODELS  # noqa: E402


class SharedModelBatchTests(unittest.TestCase):
    def test_all_buildable_roots_participate_in_the_shared_build_batch(self):
        roots = sorted(ROOT.glob("models/*/*/ci.yml"))
        self.assertEqual(len(roots), 16)
        active = []
        semantic = []
        for file in roots:
            source = file.read_text(encoding="utf-8")
            self.assertRegex(source, r"(?m)^id: [a-z0-9-]+$")
            self.assertIn("template: cad-model-build", source)
            self.assertEqual(
                len(re.findall(r"(?m)^process: (true|false)$", source)),
                1,
            )
            self.assertNotIn("run:", source)
            self.assertNotIn("package", source)
            if "process: true" in source:
                root = file.parent.relative_to(ROOT).as_posix()
                active.append(root)
                if (file.parent / "verification/verify.py").is_file():
                    semantic.append(root)

        self.assertEqual(len(active), 14)
        blocked = {
            "models/advanced/hub75-display2",
            "models/advanced/hub75_wood_frame",
        }
        self.assertEqual(
            {
                file.parent.relative_to(ROOT).as_posix()
                for file in roots
                if "process: false" in file.read_text(encoding="utf-8")
            },
            blocked,
        )
        self.assertEqual(len(semantic), 11)
        self.assertEqual(len(MODELS), 18)
        self.assertEqual(len(COMMAND_SOURCES), 5)
        self.assertIn("models/components/guide_rail", active)
        self.assertIn("models/advanced/simple_mft", active)


    def test_one_batch_runtime_and_released_copy_projection(self):
        root = (ROOT / "cad-ci.yml").read_text(encoding="utf-8")
        self.assertIn("items/{item_path}", root)
        self.assertIn("dependency: model-build-batch", root)
        for section in ("basic", "components", "advanced"):
            self.assertIn(f"models/{section}/*", root)
        self.assertNotIn("models/basic/plate\n", root)
        self.assertIn("model-build-batch", root)

        batch = (CI / "model_build_batch.py").read_text(encoding="utf-8")
        model = (CI / "model_verify.py").read_text(encoding="utf-8")
        self.assertEqual(batch.count('"docker", "pull"'), 1)
        self.assertEqual(batch.count('"docker", "run"'), 1)
        self.assertNotIn('"docker", "run"', model)
        self.assertIn('ROOT.glob("models/*/*/ci.yml")', batch)
        self.assertIn('config.get("process", True) is False', batch)
        self.assertIn('source: items/{item_path}', root)
        self.assertNotIn("missing model-local verification/verify.py", batch)
        self.assertIn('"solidcraft_built": True', model)
        self.assertIn('"semantic_verification": semantic_status', model)
        self.assertIn("snapshot_camera(slug)", model)
        self.assertIn("extra_snapshots(slug)", model)

    def test_batch_source_adapter_has_no_syntax_errors(self):
        for path in (CI / "model_build_batch.py", CI / "model_verify.py"):
            text = path.read_text(encoding="utf-8")
            tree = ast.parse(text, filename=str(path))
            self.assertTrue(tree.body)

    def test_scpc_is_prepared_once_from_pinned_source(self):
        batch = (CI / "model_build_batch.py").read_text(encoding="utf-8")
        verify = (CI / "model_verify.py").read_text(encoding="utf-8")
        self.assertIn('dependency_wheel("scpc-package", "scpc-*.whl")', batch)
        self.assertIn("scpc_wheel", verify)
        self.assertNotIn("ensure_checkout", verify)
        self.assertTrue((ROOT / "ci/scpc-package/ci.yml").is_file())

    def test_all_models_have_a_model_ci_owner(self):
        for slug, config in MODELS.items():
            source = Path(config["source"])
            root = ROOT.joinpath(*source.parts[:3])
            with self.subTest(slug=slug):
                self.assertTrue((root / "ci.yml").is_file())

    def test_development_ci_follows_released_forge_tooling(self):
        workflow = (ROOT / ".github/workflows/cad.yml").read_text(encoding="utf-8")
        self.assertIn("tool.cad.ci@b62f9d0b169aa201a3c66c3166f364396b2d71bc", workflow)
        self.assertIn("durable_scope:", workflow)
        self.assertIn('jobs: "2"', workflow)
        self.assertNotIn("pipeline_ci.py", workflow)


if __name__ == "__main__":
    unittest.main()
