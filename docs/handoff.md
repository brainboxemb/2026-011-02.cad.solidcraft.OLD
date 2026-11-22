# Handoff — CAD repository

Work in `brainboxemb/2026-011-02.cad.solidcraft`.
Primary migration: #174. Website renderer: #191. Full Forge 0.11 /
SolidCraft 0.45 qualification: #172.

## Current state

- Source lanes: `main`, `dev-cad`, `dev-ci`.
- Short-lived PRs squash into a dev lane. Direct dev-lane -> main promotion
  uses a normal merge commit through the owner-only `/merge` policy.
- Generic execution/publication comes from the exact released
  `tool.cad.ci` / `lib.py.cad.ci` stack; do not recreate it in CAD Python.
- 14 physical roots / 16 variants build through one shared SolidCraft runtime.
  `hub75-display2` and `hub75-wood-frame` remain `process:false` only
  because Forge #679 must namespace repeated component-local feature names.
- Every physical model root owns `model.yml`; `model_catalog.py` only
  validates/adapts it.

## Durable build and website proof

Hugo 0.169.0 + Blowfish v3.10.0 reads model.yml directly and accepted build
evidence from the prepared CAD-CI scope.

The dev-ci end-to-end path is proven:

```text
released CAD-CI -> build/dev-ci -> prepared scope
                 -> Hugo/Blowfish -> gh-pages/dev-ci/
```

After PR #200 the durable run published model pages plus model.yml, PNG,
SolidCraft .sc, STEP, command JSON and provenance. Comparing current Pages
with the pre-cut-over backup found 150 new files, all under `dev-ci/`, and
zero changes outside that subtree.

Stable pre-cut-over Pages remain backed up at:

`backup/gh-pages-before-174-2026-11-22` =
`55f5eae59879c6d37bd1b58b0eed0bc8f1a86775`.

## Continue

1. Finish #174 legacy cleanup: keep useful model regressions in one declarative
   `ci/repository-tests` item and remove retired local orchestration.
2. Keep `ci/README.md` and `scripts/ci/README.md` authoritative for every
   retained consumer-owned CI item/adapter.
3. Compare dev-ci visuals/routes against stable/backup before stable cut-over.
4. Do not work around Forge #679 in CAD geometry.
5. Then return the main workstream to CAD model development.

Forge #674 tracks moving merge/lane governance into shared tooling. Forge #661
tracks shared CAD-CI architecture/selectivity.
