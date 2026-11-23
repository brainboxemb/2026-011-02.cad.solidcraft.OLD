# 0039 — Wooden HUB75 frame iteration 2 lower compartment

Issue: #154

## Problem

The preserved PR #156 contains the intended iteration-2 product geometry, but
its branch predates the current model.yml/ci.yml catalog and contains stale
catalog/CI-era edits. Re-merging that branch would restore obsolete
infrastructure.

## Decision

Add `models/advanced/hub75_wood_frame_iter2/` as a new independent physical
model root. Keep the existing `hub75-display2` root; this refresh does not
rename or delete it.

The public model slug is `hub75-wood-frame-iter2`, owned by the root
`ci.yml`.

Retain only the product-CAD work from PR #156:

- 12 mm bottom board;
- 70 mm clear lower storage compartment;
- two 12 mm vertical dividers with 30 / 40 / 30 clear-bay proportions;
- 12 mm intermediate shelf;
- unchanged 844 × 362 mm display opening beginning at Z=94 mm;
- full 120 mm side-wall depth;
- 30 mm wide R15 side hand slots with 20 mm rear clearance;
- 9 mm inset rear board starting at Z=82 mm with open 50 mm R20 side cutouts;
- five existing HUB75 panel positions and eight corner brackets;
- all display-dependent Z placement derived from the lower-compartment
  parameter rather than fixed occurrence offsets.

`lower_compartment_height` remains an editable model parameter.

## Current qualification gate

The closed Forge #679 naming fix is not yet present in a released Forge version
consumed by this repository. Therefore this new root is registered with
`process: false`.

That is not native acceptance. Repository tests may validate the authored
command plan and model-owned expectations, but #154 remains incomplete until
the model can run through the normal released SolidCraft build and saved-design
mutation path.

## Verification

- focused regression coverage from the preserved model branch is retained;
- catalog metadata and root counts use the current model.yml architecture;
- no old Python catalog, mutation registry or local CI implementation is
  restored;
- after a qualifying Forge release is adopted, enable processing and require
  the normal targeted native build plus `lower_compartment_height=90 mm`
  saved-design mutation before closing #154.
