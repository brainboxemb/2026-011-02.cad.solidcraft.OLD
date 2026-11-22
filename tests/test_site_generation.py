"""Hugo/Hextra site ownership and route contracts."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"

class HugoSiteContractTests(unittest.TestCase):
    def test_theme_and_hugo_version_are_explicitly_pinned(self):
        self.assertIn("github.com/imfing/hextra v0.13.0", (SITE / "go.mod").read_text())
        self.assertIn('hugo-version: "0.169.0"', (ROOT / ".github/workflows/cad.yml").read_text())

    def test_model_yaml_is_mounted_without_python_sources(self):
        mounts = (SITE / "config/_default/module.toml").read_text()
        self.assertIn('path = "github.com/imfing/hextra"', mounts)
        self.assertNotIn("blowfish", mounts.lower())
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

    def test_homepage_uses_git_lastmod_instead_of_featured_categories(self):
        home = (SITE / "layouts/home.html").read_text()
        adapter = (SITE / "content/models/_content.gotmpl").read_text()
        card = (SITE / "layouts/partials/cad/model-card.html").read_text()
        workflow = (ROOT / ".github/workflows/cad.yml").read_text()
        self.assertIn("Recently updated models", home)
        self.assertIn("first 6 $models.ByLastmod.Reverse", home)
        self.assertNotIn("$categoryDescriptions", home)
        self.assertNotIn('index .Params.model "featured"', home)
        self.assertIn('"showUpdated" true', home)
        self.assertIn('"dates" (dict "lastmod" $lastmod)', adapter)
        self.assertIn('hugo.Data.cad.model_history', adapter)
        self.assertIn('class="cad-card-updated"', card)
        self.assertIn('fetch-depth: 0', workflow)
        self.assertEqual(workflow.count("scripts/ci/model_history.py"), 2)

    def test_homepage_links_scpf_and_scpc_libraries(self):
        home = (SITE / "layouts/home.html").read_text()
        self.assertIn("https://brainboxemb.github.io/lib.py.solidcraft.forge/", home)
        self.assertIn(">Forge / SCPF<", home)
        self.assertIn("https://brainboxemb.github.io/lib.py.solidcraft.cmd/", home)
        self.assertIn(">SCPC Commands<", home)
        self.assertNotIn("brainboxemb/tool.cad.ci", home)

    def test_homepage_featured_grid_uses_three_two_one_columns(self):
        css = (SITE / "assets/css/custom.css").read_text()
        self.assertIn(".cad-home .cad-model-grid{grid-template-columns:repeat(3,minmax(0,1fr))}", css)
        self.assertIn("@media(max-width:1000px) and (min-width:761px)", css)
        self.assertIn(".cad-home .cad-model-grid{grid-template-columns:repeat(2,minmax(0,1fr))}", css)
        self.assertIn(".cad-model-grid,.cad-reference-grid{grid-template-columns:1fr}", css)


    def test_model_detail_panel_styles_have_semantic_accent_edges(self):
        css = (SITE / "assets/css/custom.css").read_text()
        page = (SITE / "layouts/models/single.html").read_text()
        design = (ROOT / "docs/design.md").read_text()
        self.assertNotIn(".cad-background{border-left:", css)
        self.assertIn(".cad-panel-emphasis{border-top:3px solid var(--cad-accent)}", css)
        self.assertIn('class="cad-panel cad-panel-emphasis cad-web-open"', page)
        self.assertIn("border-left:4px solid #d32f2f", css)
        self.assertIn(".content blockquote{border:1px solid var(--cad-line)", css)
        self.assertIn("Hugo **0.169.0** with Hextra **v0.13.0**", design)
        self.assertIn("primary action panel", design)
        self.assertNotIn("Blowfish v3.10.0", design)

    def test_model_detail_typography_does_not_inherit_hextra_prose_tracking(self):
        css = (SITE / "assets/css/custom.css").read_text()
        self.assertNotIn(".content h1{letter-spacing:-.025em}", css)
        self.assertNotIn(".content h2{letter-spacing:-.016em}", css)
        self.assertNotIn(".content h3{letter-spacing:-.01em}", css)
        self.assertIn(".cad-panel h2{margin:0 0 .6rem;font-size:1.6rem;line-height:1.3;font-weight:600;letter-spacing:0}", css)
        self.assertIn(".cad-model-detail h2,", css)
        self.assertIn("font-weight:400;\n  letter-spacing:0;", css)

    def test_background_markdown_uses_the_same_quiet_cad_typography(self):
        css = (SITE / "assets/css/custom.css").read_text()
        self.assertIn(".cad-rich-text{max-width:78ch;font-size:1rem;line-height:1.52}", css)
        self.assertIn("font-size:1.05rem;\n  line-height:1.35;\n  font-weight:600;\n  letter-spacing:0;", css)
        self.assertIn(".cad-rich-text li::marker{color:var(--cad-accent)}", css)
        self.assertIn(".cad-background .subheading-anchor{display:none}", css)

    def test_cad_typography_matches_the_accepted_visual_baseline(self):
        css = (SITE / "assets/css/custom.css").read_text()
        self.assertIn(".cad-page-shell{", css)
        self.assertIn("font-size:1rem", css)
        self.assertIn('font-family:"Segoe UI",system-ui,-apple-system,BlinkMacSystemFont,sans-serif;', css)
        self.assertNotIn('font-family:Inter,"Segoe UI",system-ui', css)
        self.assertIn(".cad-page-shell h1,", css)
        self.assertIn(".cad-page-shell button{", css)
        self.assertIn("font-size:.76rem", css)
        self.assertIn("padding:4px 11px", css)
        self.assertIn(".hextra-max-navbar-width", css)
        self.assertIn("font-size:1.19rem!important", css)
        self.assertIn(".cad-hero h1{max-width:760px;margin:4px 0 15px;color:#fff;font-size:clamp(2rem,4.5vw,3rem);line-height:1.14;font-weight:600;letter-spacing:0}", css)
        self.assertIn("font-weight:600;\n  letter-spacing:0;", css)

    def test_optional_page_markdown_is_generic_model_content(self):
        mounts = (SITE / "config/_default/module.toml").read_text()
        adapter = (SITE / "content/models/_content.gotmpl").read_text()
        page = (SITE / "layouts/models/single.html").read_text()
        self.assertIn('"**/page.md"', mounts)
        self.assertIn('cad-source/%s/%s/page.md', adapter)
        self.assertIn('page.md', adapter)
        self.assertIn('.Resources.Get "page.md"', page)
        self.assertIn('$.RenderString .Content', page)
        self.assertNotIn('if eq .Params.cadSlug "simple-mft"', page)

    def test_external_reference_images_render_as_images(self):
        page = (SITE / "layouts/models/single.html").read_text()
        self.assertIn('strings.HasSuffix $lower ".jpg"', page)
        self.assertIn('class="cad-external-image"', page)
        self.assertIn('External reference', page)

    def test_simple_mft_background_has_one_public_source(self):
        background = (ROOT / "models/advanced/simple_mft/page.md").read_text()
        readme = (ROOT / "models/advanced/simple_mft/README.md").read_text()
        self.assertIn("CRAFTMAKER ProStation S30", background)
        self.assertIn("photo-derived", background)
        self.assertIn("[page.md](page.md)", readme)
        self.assertNotIn("## Photo-based slot estimate", readme)

    def test_scpc_is_optional_secondary_comparison_content(self):
        adapter = (SITE / "content/models/_content.gotmpl").read_text()
        page = (SITE / "layouts/models/single.html").read_text()
        self.assertIn('index $model "scpc_source"', adapter)
        self.assertIn('scpc-source.py', adapter)
        self.assertIn('.Resources.Get "scpc-source.py"', page)
        self.assertIn("SCPC command source", page)
        self.assertIn("It does not call SCPF", page)

    def test_solidcraft_model_can_open_in_external_solidcraft_web(self):
        page = (SITE / "layouts/models/single.html").read_text()
        self.assertIn('.Resources.Get "model.sc"', page)
        self.assertIn("https://docs.solidcraft.io/app/?open=", page)
        self.assertIn("urlquery $nativeURL", page)
        self.assertIn('target="_blank"', page)
        self.assertIn('rel="noopener noreferrer"', page)
        self.assertIn("Download model .sc", page)

    def test_verification_section_uses_only_build_provenance(self):
        page = (SITE / "layouts/models/single.html").read_text()
        self.assertIn("Build and verification", page)
        self.assertIn('index $prov "solidcraft_built"', page)
        self.assertIn('index $prov "solidcraft_verified"', page)
        self.assertIn('index $prov "semantic_verification"', page)
        self.assertIn('index $prov "runtime_image"', page)
        self.assertIn("No accepted build or verification evidence", page)


    def test_catalog_uses_sections_without_repeated_category_navigation(self):
        listing = (SITE / "layouts/models/list.html").read_text()
        css = (SITE / "assets/css/custom.css").read_text()
        self.assertNotIn('class="cad-category-grid"', listing)
        self.assertNotIn('class="cad-category-card"', listing)
        self.assertIn('class="cad-section cad-catalog-section"', listing)
        self.assertIn('slice "basic" "components" "advanced"', listing)
        card = (SITE / "layouts/partials/cad/model-card.html").read_text()
        self.assertIn('{{ if $showSection }}<span class="cad-card-section">', card)
        self.assertIn('"showSection" false', listing)
        self.assertIn(".cad-catalog-page .cad-model-grid{grid-template-columns:repeat(3,minmax(0,1fr))}", css)
        self.assertIn(".cad-catalog-page .cad-model-grid{grid-template-columns:repeat(2,minmax(0,1fr))}", css)
        self.assertIn("font-weight:600;", css)

    def test_cad_routes_use_one_shared_page_shell(self):
        home = (SITE / "layouts/home.html").read_text()
        listing = (SITE / "layouts/models/list.html").read_text()
        page = (SITE / "layouts/models/single.html").read_text()
        self.assertIn('class="cad-page-shell cad-home"', home)
        self.assertIn('class="cad-page-shell cad-catalog-page"', listing)
        self.assertIn('class="cad-page-shell cad-model-detail"', page)
        self.assertIn('class="cad-page-shell"', page)

    def test_scpf_code_uses_hextra_copy_control(self):
        page = (SITE / "layouts/models/single.html").read_text()
        partial = (SITE / "layouts/partials/cad/codeblock.html").read_text()
        params = (SITE / "config/_default/params.toml").read_text()
        self.assertIn('partial "cad/codeblock.html"', page)
        self.assertIn('components/codeblock-copy-button', partial)
        self.assertIn('[highlight.copy]', params)
        self.assertIn('display = "always"', params)

    def test_public_model_page_avoids_native_terminology(self):
        page = (SITE / "layouts/models/single.html").read_text()
        for value in ("Native verified", "Verified native", "SCPC native-command source", ">Native .sc<", "Native model", "Download native .sc", "saved native model", "native SolidCraft operations"):
            self.assertNotIn(value, page)

    def test_model_overview_restores_header_status_preview_and_files_layout(self):
        page = (SITE / "layouts/models/single.html").read_text()
        self.assertIn('class="cad-model-hero"', page)
        self.assertIn('class="cad-model-statusbar"', page)
        self.assertIn('class="cad-model-overview"', page)
        self.assertIn(">Model preview<", page)
        self.assertIn(">Files<", page)
        self.assertIn("Construction stages", page)
        self.assertIn('<ul class="cad-stages">', page)
        self.assertNotIn('<ol class="cad-stages">', page)
        self.assertIn('$commandCount = len .', page)
        self.assertIn('{{ $commandCount }} commands', page)
        self.assertNotIn("scpc_command_count", page)

    def test_model_page_prioritizes_use_and_context_before_technical_depth(self):
        page = (SITE / "layouts/models/single.html").read_text()
        self.assertLess(page.index("cad-web-open"), page.index("cad-source-section"))
        self.assertLess(page.index("cad-background"), page.index("cad-source-section"))
        self.assertLess(page.index('index $m "extra_views"'), page.index("cad-source-section"))

    def test_generated_solidcraft_commands_are_collapsed_by_default(self):
        page = (SITE / "layouts/models/single.html").read_text()
        self.assertIn('<details class="cad-code-section cad-commands-section cad-collapsible">', page)
        self.assertIn("<summary>", page)
        self.assertIn("Generated output", page)
        self.assertIn("SolidCraft commands", page)
        self.assertIn("generated operations · expand to inspect", page)
        self.assertNotIn('<details class="cad-code-section cad-commands-section cad-collapsible" open', page)
        self.assertIn('class="cad-command-sequence"', page)
        self.assertIn('class="cad-command-step"', page)
        self.assertIn('class="cad-command-json"', page)
        self.assertIn('transform.Remarshal "json"', page)
        self.assertNotIn('"label" "solidcraft.json"', page)
        self.assertNotIn('class="cad-command-list"', page)

    def test_model_overview_uses_balanced_columns_and_compact_preview(self):
        css = (SITE / "assets/css/custom.css").read_text()
        page = (SITE / "layouts/models/single.html").read_text()
        self.assertIn("grid-template-columns:repeat(2,minmax(0,1fr))", css)
        self.assertIn(".cad-preview-panel .cad-preview{\n  min-height:330px;", css)
        self.assertIn(".cad-preview-panel .cad-preview-link{\n  min-height:330px;", css)
        self.assertIn(".cad-collapsible[open]>summary:after{content:\"Collapse\"}", css)
        self.assertNotIn(".cad-command-list", css)
        self.assertIn(".cad-command-sequence{", css)
        self.assertIn(".cad-command-json{", css)
        self.assertIn("right:1.75rem!important", css)
        self.assertIn("padding:1rem 5.25rem 1rem 1.05rem!important;scrollbar-gutter:stable", css)
        self.assertIn(".cad-code-frame{\n  overflow:hidden;\n  margin-top:.9rem;\n  border:0;", css)
        self.assertNotIn("cad-panel cad-commands-panel", page)

    def test_model_page_keeps_expected_public_content(self):
        page = (SITE / "layouts/models/single.html").read_text()
        for value in ("SCPF source","SolidCraft commands","Construction stages","Python source","model.yml","Forge commands","SolidCraft model","STEP","Build provenance","No accepted build evidence","extra_views"):
            self.assertIn(value, page)

    def test_model_page_uses_declared_scpf_source_and_generated_commands(self):
        mounts = (SITE / "config/_default/module.toml").read_text()
        adapter = (SITE / "content/models/_content.gotmpl").read_text()
        page = (SITE / "layouts/models/single.html").read_text()
        self.assertIn('"**/*.py"', mounts)
        self.assertIn('$sourcePath := index $model "source"', adapter)
        self.assertIn("scpf-source.py", adapter)
        self.assertIn('.Resources.Get "scpf-source.py"', page)
        self.assertIn('partial "cad/codeblock.html"', page)
        self.assertIn('.Resources.Get "solidcraft.json"', page)
        self.assertIn('$commandsDoc := .Content | transform.Unmarshal', page)
        self.assertIn('index $commandsDoc "commands"', page)

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

    def test_footer_uses_hextra_extension_point_for_hugo_and_theme_credit(self):
        params = (SITE / "config/_default/params.toml").read_text()
        footer = (SITE / "layouts/_partials/custom/footer.html").read_text()
        self.assertIn("displayPoweredBy = false", params)
        self.assertIn("Built with", footer)
        self.assertIn("https://gohugo.io/", footer)
        self.assertIn("Theme:", footer)
        self.assertIn("https://imfing.github.io/hextra/", footer)
        self.assertNotIn("layouts/_partials/footer.html", footer)

    def test_stable_visual_baseline_is_retained_for_comparison(self):
        baseline = (SITE / "results.css").read_text()
        current = (SITE / "assets/css/custom.css").read_text()
        for value in ("#102d57","#244f80","#195eb8","#dbe3ef"):
            self.assertIn(value, baseline)
            self.assertIn(value, current)

if __name__ == "__main__":
    unittest.main()
