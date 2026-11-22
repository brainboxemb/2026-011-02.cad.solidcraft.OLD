# Accepted CAD website baseline before CI migration

This captures the existing public CAD Pages presentation so changing the
execution engine cannot silently change the website. It is a **comparison
baseline**, not a proposal to use Forge website templates.

- `gh-pages` snapshot: `55f5eae59879c6d37bd1b58b0eed0bc8f1a86775`.
- `build` branch snapshot:
  `bc90c5516fe42645d15a3e2b1057ad1b62e18a70`.
- Stable URL: https://brainboxemb.github.io/2026-011-02.cad.solidcraft/
- Existing CSS source: `site/results.css` (do not replace with Forge CSS).
- Homepage title: `Models · SolidCraft CAD projects`.
- Homepage H1: `CAD models, from readable code to native geometry`.
- Model-page example title: `SamplePlate · SolidCraft CAD projects`.

## Public structure to retain

- Homepage sections: Getting started, Model catalog, Verification status,
  Basic Models, Components, Advanced Models.
- Category routes: `/models/basic/`, `/models/components/` and
  `/models/advanced/`.
- Every model route: `/models/<catalog-slug>/`, with source and output links.
  Slugs are derived from `scripts/ci/model_catalog.py`, never maintained in
  a second hard-coded navigation list.
- Representative model page sections: Model preview, Files, Construction
  stages, Open this model in SolidCraft Web, Python model and Native
  SolidCraft command sequence (SCPF). SCPC-equipped models also show their
  independent command/source presentation.
- Current warnings, validation wording, available downloads, diagrams,
  thumbnail/supplementary renders and responsive CSS remain recognizable.

## Acceptance

M0 tests protect source-level route/content contracts; existing
`tests/test_site_generation.py` proves HTML can be generated from mock
CAD evidence without running native SolidCraft. This is **not** a visual
comparison of the newly published website.

At M4/M5 compare actual HTML, links, screenshots and page rendering against
this accepted `gh-pages` snapshot before promoting the new site. At least one
basic model, one HUB75 assembly and one SCPC-equipped model are mandatory
checks, along with homepage, all category pages and narrow-screen layout.

If a visible difference is a design choice rather than necessary build-data
migration, keep the existing site and open a separate website change.

## Model-content parity gate (CAD #189)

The migration to local model.yml files must preserve the **18 original
entries and their order**, section cards, titles, taglines, descriptions,
parameters, stages, warnings, featured flags and source associations.
The frozen source-content CRC is asserted in
`tests/test_model_metadata.py`, and the generated site is tested by
`tests/test_site_generation.py`. Supplementary MFT and HUB75 views are
declared in local metadata and rendered through the same visual layout.
A new `model.yml` download link is additive and intentional.

