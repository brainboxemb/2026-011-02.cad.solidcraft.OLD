# 0048 — qualify the lower-compartment HUB75 case on Forge v0.13.2

Issue: #154

## Context

Change record #0039 introduced the independent lower-compartment model root but
left it at `process: false` because the then-consumed Forge baseline did not
contain the required #679/#749 fixes.

The repository now consumes Forge v0.13.2. Hub75DisplayCase,
Hub75DisplayCase v2 and the restored detailed `hub75-panel` all pass native
SolidCraft builds on that baseline.

## Decision

Refresh the existing #154 / PR #349 product-CAD slice onto current `dev-cad`
without carrying its stale repository-infrastructure history.

- keep the #0039 geometry and independent model root;
- set `hub75-wood-frame-iter2` to `process: true`;
- keep using `Hub75PanelBasic`; this model remains independent of detailed
  panel internals even though Forge v0.13.2 has restored that root;
- keep rear-board hand cutouts at fixed 50 mm depth / R20 product constants,
  rather than exposing them accidentally as native parameters;
- add model-owned declarative SolidCraft verification;
- verify the baseline `lower_compartment_height = 70 mm`;
- mutate the saved native design with SolidCraft `parameters.change` to
  `lower_compartment_height = 90 mm`;
- verify the mutated saved design reports 90 mm after native rebuild.

## Naming boundary

The existing `hub75_wood_frame_iter2` / `WoodenHub75BoxIter2` /
`hub75-wood-frame-iter2` identifiers stay unchanged in this geometry
qualification. CAD #422 owns the distinct final product/class name, coordinated
with the path/id/slug compatibility work in #417.

## Acceptance

- repository regression contracts account for 17 physical roots and 19 catalog
  variants;
- all 17 physical roots are active on the current Forge v0.13.2 baseline;
- the targeted native build selects `hub75-wood-frame-iter2`;
- native SolidCraft replay succeeds and saves STEP/image/design output;
- semantic verification passes baseline and the 70 → 90 mm saved-design
  mutation;
- no CAD-local Forge/compiler/import workaround is introduced.
