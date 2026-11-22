# Handoff — CAD repository

Work in `brainboxemb/2026-011-02.cad.solidcraft`.
Primary migration: #174. Website renderer: #191. Full Forge 0.11 /
SolidCraft 0.45 qualification: #172.

## Current state

- Source lanes: `main`, `dev-cad`, `dev-ci`.
- Short-lived PRs squash into a dev lane. Direct dev-lane -> main promotion
  uses a normal merge commit through the owner-only `/merge` policy.
- Generic execution/publication comes from released `tool.cad.ci` /
  `lib.py.cad.ci`; do not recreate it in CAD Python.
- 14 physical roots / 16 variants build through one shared SolidCraft runtime.
  `hub75-display2` and `hub75-wood-frame` remain `process:false` only
  because Forge #679 must namespace repeated component-local feature names.
- Every physical model root owns `model.yml`; it is the human/site metadata
  source. `model_catalog.py` only validates/adapts it.

## Website

#191 selected Hugo + Blowfish. The isolated
`exp.2026-015.hugo-cad-site` build used the real CAD metadata, generated 32
pages, and passed route/content checks.

Target data flow:

```text
models/*/*/model.yml
    -> Hugo data mount (model.yml only)
    -> content/models/_content.gotmpl
    -> /models/<slug>/

prepared tool.cad.ci scope
    -> Hugo assets/build
    -> build state, images and downloads

Hugo/Blowfish
    -> generated-site
    -> cad_ci_tool publish pages
```

The pre-cut-over stable Pages tip is backed up permanently:
`backup/gh-pages-before-174-2026-11-22` =
`55f5eae59879c6d37bd1b58b0eed0bc8f1a86775`.

## Continue

1. Get the Hugo/Blowfish site green on the existing CAD `/dev-ci/` Pages
   subtree; do not touch the stable root.
2. Compare routes, images, downloads, warnings and mobile/desktop structure
   against the backup/stable site.
3. Remove unreachable legacy Python planner/selector/publisher/HTML-renderer
   code immediately after that acceptance.
4. Do not work around Forge #679 in CAD geometry.
5. Then return the main workstream to CAD model development.

Forge #674 tracks moving merge/lane governance into shared tooling. Forge #661
tracks shared CAD-CI architecture/selectivity.
