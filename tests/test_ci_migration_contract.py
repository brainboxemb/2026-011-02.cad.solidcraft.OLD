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
from model_item import catalog_root, item_id_for_slug, item_members  # noqa: E402


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

        site_builder = (CI / "build-results.py").read_text(encoding="utf-8")
        site_smoke = (CI / "test-results.py").read_text(encoding="utf-8")
        stylesheet = (ROOT / "site/results.css").read_text(encoding="utf-8")

        self.assertIn('"models" / slug', site_smoke)
        self.assertIn("Construction stages", site_builder)
        self.assertIn("Native SolidCraft command sequence (SCPF)", site_builder)
        self.assertIn("model-preview-layout", site_builder)
        self.assertIn('out / "models" / slug', site_builder)
        self.assertIn(".model-warning", stylesheet)

    def test_dev_ci_runs_released_model_build_graph_without_touching_main(self):
        source = (ROOT / "cad-ci.yml").read_text(encoding="utf-8")
        self.assertIn("cad-solidcraft:v0.3.4", source)
        self.assertIn("cad-model-build", source)
        self.assertIn("scpc-package", source)
        self.assertIn("models/basic/plate", source)
        self.assertIn("models/basic/vent_plate", source)
        self.assertNotIn("models/advanced/*", source)
        self.assertIn("scripts/ci/model_verify.py", source)
        self.assertIn("scpc/**", source)
        self.assertTrue((ROOT / "ci/scpc-package/ci.yml").is_file())
        self.assertTrue((ROOT / "scripts/ci/scpc_dependency.py").is_file())

        config = __import__("json").loads(
            (ROOT / "ci/cad-verification-package/package.json").read_text()
        )
        self.assertEqual(config["version"], "0.15.0")
        self.assertEqual(config["commit"], "9a232798f06254454e6d302bd5f1bac81475194c")
        self.assertTrue(
            (ROOT / "models/basic/plate/verification/verify.py").is_file()
        )
        package_builder = (
            ROOT / "scripts/ci/verification_package.py"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "ROOT = Path(__file__).resolve().parents[2]",
            package_builder,
        )

        workflow = (ROOT / ".github/workflows/cad.yml").read_text()
        self.assertIn("tool.cad.ci@d88d6e189c12edb5a30158c068145c099c17a019", workflow)
        self.assertTrue(
            (ROOT / "models/basic/vent_plate/verification/verify.py").is_file()
        )
        self.assertFalse((ROOT / "scripts/ci/model_verify_pilot.py").exists())

    def test_development_branches_do_not_use_old_preview_publisher(self):
        workflow = (ROOT / ".github/workflows/cad.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("dev-cad, dev-ci", workflow)
        self.assertIn("github.event.pull_request.base.ref == 'main'", workflow)
        self.assertIn("test_site_generation.py", workflow)


if __name__ == "__main__":
    unittest.main()
