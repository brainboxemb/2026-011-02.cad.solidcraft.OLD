# 0051 — complete CornerBracket arm-tip relief wedges

Issue: #362

## Context

The accepted CornerBracket already preserves:

- the 11-point OpenSCAD arm profile;
- the two 0.6 mm tip-relief diagonals;
- the R4 inside fillet;
- the ordinary 2 mm outside side chamfer;
- the continuous broad-face elephant-foot relief;
- the exact four-part recessed M5 fixing seats.

The preserved OpenSCAD `arm_tip_relief_cuts()` also subtracts four small
triangular prisms where the broad-face relief meets the arm-tip side chamfers.
Those local 45-degree cutters were deliberately deferred until reusable Forge
support existed.

Forge #750 / PR #771 is now released and consumed through Forge v0.13.2 as
rotated explicit Sketch frames.

## Decision

Port `arm_tip_relief_cuts()` literally:

- one triangular profile:
  `[-elephant_foot_relief-1,-1], [1,-1], [1,elephant_foot_relief+1]`;
- prism length:
  `side_edge_chamfer * sqrt(2) + 2`;
- horizontal positive-side frame:
  rotation `(90, 0, 45)`;
- vertical positive-side frame:
  rotation `(0, 45, 90)`;
- mirrored negative-side cutters use reflected local Sketch frames and
  negative extrusion direction, preserving the exact mirror without
  hand-expanded world geometry;
- subtract all four cutters after the broad-face relief and before the M5 seats.

The two `tip_*` profile segments remain excluded from the ordinary 2 mm
side-chamfer selector.

## Verification

- default SCPF command plan contains four rotated arm-tip Sketch cutters;
- SCPF/SCPC use equal origins, local axes, prism lengths and mirror directions;
- the existing 11-point profile, two chamfers and sixteen native hole features
  remain unchanged;
- dedicated `horizontal-tip.png` and `vertical-tip.png` review views are
  model-owned;
- native SolidCraft build and independent Forge/SCPC geometry comparison must
  pass;
- visual acceptance of the exact PR images remains required before closing #8
  and #362. CAD-CI review-artifact transport is tracked upstream as
  `tool.cad.ci#181`.
