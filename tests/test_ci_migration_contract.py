"""Migration guardrails: do not lose CAD models or website structure.

This tests the existing consumer model catalog and source layout only.
Released CAD-CI continues to own execution, dependency freshness and reuse.
"""

from __future__ import annotations

from pathlib import Path
import re
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / "scripts" / "ci"
sys.path.insert(0, str(CI))

from model_catalog import (  # noqa: E402
    COMMAND_SOURCES,
    MODELS,
    SECTIONS,
    dependency_closure,
    model_slugs,
)

def catalog_root(slug):
    source = Path(MODELS[slug]["source"])
    return Path(*source.parts[:3])


def item_members(root):
    relative = root.resolve().relative_to(ROOT.resolve())
    return tuple(slug for slug in MODELS if catalog_root(slug) == relative)


def item_id_for_slug(slug):
    root = catalog_root(slug)
    return next(candidate for candidate in MODELS if catalog_root(candidate) == root)



class MigrationCatalogContractTests(unittest.TestCase):
    def test_all_current_catalog_variants_have_an_owning_ci_item(self):
        self.assertEqual(len(MODELS), 18)
        roots = {catalog_root(slug) for slug in MODELS}
        self.assertEqual(len(roots), 16)

        physical = set()
        for section in ("basic", "components", "advanced"):
            physical.update(
                path.parent.relative_to(ROOT)
                for path in (ROOT / "models" / section).glob("*/ci.yml")
            )
        self.assertEqual(roots, physical)

        for slug in MODELS:
            with self.subTest(slug=slug):
                root = catalog_root(slug)
                ci_file = ROOT / root / "ci.yml"
                self.assertTrue(ci_file.is_file())
                declared = re.search(
                    r"(?m)^id:\s*([a-z0-9-]+)\s*$",
                    ci_file.read_text(encoding="utf-8"),
                )
                self.assertIsNotNone(declared, ci_file.as_posix())
                self.assertEqual(declared.group(1), item_id_for_slug(slug))
                self.assertIn(slug, item_members(ROOT / root))
                self.assertTrue((ROOT / MODELS[slug]["source"]).is_file())

    def test_shared_model_roots_have_two_variants_each(self):
        self.assertEqual(
            set(item_members(ROOT / "models/components/guide_rail")),
            {"guide-rail", "guide-rail-makita"},
        )
        self.assertEqual(
            set(item_members(ROOT / "models/advanced/simple_mft")),
            {"simple-mft", "simple-mft-assembly"},
        )

    def test_declared_dependencies_and_independent_command_sources_exist(self):
        for slug in MODELS:
            with self.subTest(slug=slug):
                for dependency in dependency_closure(slug):
                    self.assertIn(dependency, MODELS)
                    self.assertTrue((ROOT / MODELS[dependency]["source"]).is_file())

        self.assertEqual(len(COMMAND_SOURCES), 5)
        for slug, path in COMMAND_SOURCES.items():
            with self.subTest(scpc=slug):
                self.assertIn(slug, MODELS)
                self.assertTrue((ROOT / path).is_file())

    def test_site_preserves_current_public_model_routes_and_sections(self):
        self.assertEqual(tuple(SECTIONS), ("basic", "components", "advanced"))
        self.assertEqual(set(model_slugs()), set(MODELS))

        adapter = (ROOT / "site/content/models/_content.gotmpl").read_text(encoding="utf-8")
        page = (ROOT / "site/layouts/models/single.html").read_text(encoding="utf-8")
        stylesheet = (ROOT / "site/assets/css/custom.css").read_text(encoding="utf-8")

        self.assertIn("hugo.Data.cad.models", adapter)
        self.assertIn('"path" $slug', adapter)
        self.assertIn("Construction stages", page)
        self.assertIn("Forge commands", page)
        self.assertIn("cad-preview-layout", stylesheet)
        self.assertIn(".cad-warning", stylesheet)

    def test_dev_ci_uses_one_shared_model_build_batch(self):
        config = (ROOT / "cad-ci.yml").read_text(encoding="utf-8")
        self.assertIn("cad-model-build", config)
        self.assertIn("model-build-batch", config)
        self.assertIn("source: items/{item_path}", config)
        self.assertNotIn("run: [python, ../../../scripts/ci/model_verify.py]", config)
        self.assertIn("models/advanced/*", config)
        self.assertIn("models/components/*", config)
        self.assertIn("models/basic/*", config)
        self.assertIn("ci/*", config)

        repository_tests = (ROOT / "ci/repository-tests/ci.yml").read_text()
        self.assertIn("id: repository-tests", repository_tests)
        self.assertIn("scripts/ci/repository_tests.py", repository_tests)

        shared = (ROOT / "ci/model-build-batch/ci.yml").read_text()
        self.assertIn("forge-package", shared)
        self.assertIn("scpc-package", shared)
        self.assertIn("cad-verification-package", shared)
        self.assertIn("run: [python, ../../scripts/ci/model_build_batch.py]", shared)

        import json
        pin = json.loads(
            (ROOT / "ci/cad-verification-package/package.json").read_text()
        )
        self.assertEqual(pin["version"], "0.15.0")
        self.assertTrue((ROOT / "docs/handoff.md").is_file())

    def test_legacy_local_ci_implementations_are_retired_and_documented(self):
        legacy = (
            "build-results.py",
            "build_plan.py",
            "cad_ci.py",
            "native_ci.py",
            "output_store.py",
            "pipeline_ci.py",
            "publish_ci.py",
            "select_models.py",
            "snapshot_camera.py",
        )
        for name in legacy:
            with self.subTest(name=name):
                self.assertFalse((CI / name).exists())

        retained = {
            path.name
            for path in CI.glob("*.py")
            if path.name != "__init__.py"
        }
        self.assertEqual(
            retained,
            {
                "bootstrap_cad_ci.py",
                "forge_dependency.py",
                "model_build_batch.py",
                "model_catalog.py",
                "model_history.py",
                "model_checks.py",
                "model_verify.py",
                "repository_tests.py",
                "scpc_dependency.py",
                "verification_package.py",
            },
        )
        readme = (CI / "README.md").read_text(encoding="utf-8")
        for name in retained:
            with self.subTest(documented_adapter=name):
                self.assertIn(f"`{name}`", readme)

        for config in ROOT.glob("ci/*/ci.yml"):
            with self.subTest(item=config.parent.name):
                self.assertTrue((config.parent / "README.md").is_file())

    def test_development_branches_use_released_scopes_and_pages_publisher(self):
        workflow = (ROOT / ".github/workflows/cad.yml").read_text(encoding="utf-8")
        self.assertIn("branches: [main, dev-cad, dev-ci]", workflow)
        self.assertIn("durable_scope:", workflow)
        self.assertIn("steps.cad_ci.outputs.prepared_scope", workflow)
        self.assertIn("python -m cad_ci_tool publish pages", workflow)
        self.assertNotIn("pipeline_ci.py", workflow)
        self.assertNotIn("publish_ci.py", workflow)


if __name__ == "__main__":
    unittest.main()
