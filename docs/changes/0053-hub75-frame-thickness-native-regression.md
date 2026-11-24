# 0053 — add Hub75DisplayCase frame-thickness native regression

Issue: #91

## Context

Obsolete PR #83 contained one useful regression: changing
`frame_wood_thickness` from 12 mm to 18 mm must move the wooden frame and all
eight CornerBracket occurrences together. Its AnchorTopology implementation and
workflow-local jq checks no longer match the repository architecture.

The current Hub75DisplayCase already uses associative explicit placements. The
remaining task is durable native verification, not a geometry rewrite.

## Decision

Add model-owned declarative SolidCraft verification to
`hub75_wood_frame`:

- baseline `frame_wood_thickness = 12 mm`;
- saved-design mutation through native `parameters.change` to 18 mm;
- verify all five wooden Board body envelopes;
- verify all eight CornerBracket body envelopes;
- use the shared `SolidCraftBodyGroupExpectation` /
  `SolidCraftSavedDesign` layer;
- keep bounds tolerance at 0.001 mm.

## Native regression geometry

At 18 mm:

- side-board outside planes move to X=±440 mm;
- roof top moves to Z=398 mm;
- the rear board grows to 880 mm width / 380 mm height;
- four bottom brackets remain Z=-12..60;
- four top brackets move to Z=338..410;
- bracket outer reach moves to X=±452 mm;
- front/rear bracket Y envelopes remain 0..24 and 76..100 mm.

These are the useful native checks preserved from #83, now expressed as model
verification data rather than workflow-local jq.

## Boundary

No SCPF geometry, placement or reusable CornerBracket implementation changes
belong to this issue. #77 remains the broader opening-width/opening-height and
orientation acceptance slice.
