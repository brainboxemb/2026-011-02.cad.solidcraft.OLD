"""Hugo/Blowfish site ownership and route contracts."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"

class HugoSiteContractTests(unittest.TestCase):
    def test_theme_and_hugo_version_are_explicitly_pinned(self):
        self.assertIn("github.com/nunocoracao/blowfish/v3 v3.10.0", (SITE / "go.mod").read_text())
        self.assertIn('hugo-version: "0.169.0"', (ROOT / ".github/workflows/cad.yml").read_text())

    def test_model_yaml_is_mounted_without_python_sources(self):
        mounts = (SITE / "config/_default/module.toml").read_text()
        self.assertIn('source = "../models"', mounts)
        self.assertIn('target = "data/cad/models"', mounts)
        self.assertIn('files = ["**/model.yml"]', mounts)

    def test_content_adapter_owns_routes_without_second_catalog(self):
        adapter = (SITE / "content/models/_content.gotmpl").read_text()
        self.assertIn("hugo.Data.cad.models", adapter)
        self.assertIn("$.AddPage", adapter)
        self.assertIn('strings.Replace $rootName "_" "-"', adapter)
        self.assertIn('"path" $slug', adapter)
        self.assertNotIn('if eq $slug "simple-mft"', adapter)
        self.assertNotIn('if eq $slug "hub75-panel"', adapter)


    def test_homepage_uses_explicit_featured_models_grouped_by_category(self):
        home = (SITE / "layouts/home.html").read_text()
        self.assertIn('slice "basic" "components" "advanced"', home)
        self.assertIn('eq (index .Params.model "featured") true', home)
        self.assertIn('sort $featured "Params.model.priority"', home)
        self.assertIn('data-category="{{ $key }}"', home)
        self.assertNotIn('ne (index .Params.model "featured") false', home)

        featured = {
            "basic": ["models/basic/plate/model.yml", "models/basic/plastic_enclosure/model.yml"],
            "components": ["models/components/corner_bracket/model.yml", "models/components/guide_rail/model.yml"],
            "advanced": ["models/advanced/simple_mft/model.yml", "models/advanced/hub75_screen/model.yml"],
        }
        for section, paths in featured.items():
            with self.subTest(section=section):
                for relative in paths:
                    content = (ROOT / relative).read_text()
                    self.assertIn("featured: true", content)


    def test_homepage_explains_the_cad_library_not_the_ci_pipeline(self):
        home = (SITE / "layouts/home.html").read_text()
        self.assertIn("SCPF CAD models for SolidCraft", home)
        self.assertIn("practical SCPF reference", home)
        self.assertIn("generated SolidCraft commands", home)
        self.assertIn("Reusable parts designed to be imported", home)
        self.assertNotIn("Model descriptions come from local", home)
        self.assertNotIn("accepted CAD-CI results", home)

    def test_model_page_keeps_expected_public_content(self):
        page = (SITE / "layouts/models/single.html").read_text()
        for value in ("Construction stages","Python source","model.yml","Forge commands","SolidCraft model","STEP","Build provenance","No build evidence in this scope","extra_views"):
            self.assertIn(value, page)

    def test_site_reads_only_prepared_build_scope(self):
        mounts = (SITE / "config/_default/module.toml").read_text()
        adapter = (SITE / "content/models/_content.gotmpl").read_text()
        workflow = (ROOT / ".github/workflows/cad.yml").read_text()
        self.assertIn('source = "../prepared-scope"', mounts)
        self.assertIn('target = "assets/build"', mounts)
        self.assertIn('build/models/%s/%s/models/%s', adapter)
        self.assertIn("steps.cad_ci.outputs.prepared_scope", workflow)
        self.assertIn('"target" "model.sc"', adapter)
        self.assertIn('"target" "model.step"', adapter)
        self.assertIn('"mediaType" "application/octet-stream"', adapter)
        self.assertIn('"value" .Content', adapter)
        self.assertNotIn('"value" .)', adapter)
        page = (SITE / "layouts/models/single.html").read_text()
        self.assertIn('.Resources.Get "model.sc"', page)
        self.assertIn('.Resources.Get "model.step"', page)
        self.assertNotIn("resources.Copy", page)
        self.assertNotIn("scripts/ci/build-results.py", workflow)

    def test_stable_visual_baseline_is_retained_for_comparison(self):
        baseline = (SITE / "results.css").read_text()
        current = (SITE / "assets/css/custom.css").read_text()
        for value in ("#102d57","#244f80","#195eb8","#dbe3ef"):
            self.assertIn(value, baseline)
            self.assertIn(value, current)

if __name__ == "__main__":
    unittest.main()
