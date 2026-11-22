# 0021 — Local model.yml is the CAD website source of truth

Issue: #189; parent migration #174.

## Observation

The CAD repository had no model.yml files. An approximately 28 KB Python
catalog maintained all 18 model descriptions, and the site generator used
model-specific branches for MFT and HUB75 images. Forge already uses a
per-model model.yml contract.

## Decision

- Introduce 16 `models/*/*/model.yml` files with the same public model
  vocabulary as Forge (section, priority, title, tagline, description,
  parameters, stages); record the two multi-variant roots in one YAML file
  each.
- Keep `ci.yml` and `verification/verify.py` strictly about execution
  and geometric checks. `model_catalog.py` is now a validator/loader that
  preserves its previous consumer API and model ordering.
- Convert Simple MFT and Hub75Panel view declarations to model-owned data.
  Keep the existing static HTML/CSS layout and category/model URLs.
- Publish a model's `model.yml` next to its public code and outputs.
- `model.yml` participates in site selection but not geometry fingerprints;
  documentation should not cause a costly SolidCraft build.
- PyYAML is required only while building/testing the static website.
- Leave stable Pages unchanged until new build/Pages lanes and full
  catalogue acceptance are ready.

## Evidence required

16 files / 18 variants, all sources and warnings intact, original catalog
content/order CRC, unchanged website routes and representative images;
metadata-only runs without model builds; no model-specific view HTML code.

