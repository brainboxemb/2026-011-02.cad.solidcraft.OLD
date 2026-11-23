# 0038 — FlexBenchDog independent logo rib cuts

Issue: #332

## Problem

PR #341 used the correct nine centerlines of the BrainBox wireframe cube, but
placed nine intersecting closed Slot profiles in one Sketch. Their intersections
created additional enclosed sketch regions. The resulting recess visually
removed a filled six-sided face instead of only engraving the cube ribs.

An initial correction attempt used Polygon2D rib strips. CAD CI rejected that
approach because the released Forge v0.11.0 consumed by this repository does
not support Polygon2D in this attached-Sketch route.

That missing generic capability is tracked upstream as Forge #747. CAD #348
tracks removal of the temporary per-rib Slot workaround after the Forge fix is
released and adopted here.

## Decision

Keep the nine accepted cube centerlines, 0.6 mm line width and 0.6 mm recess
depth.

Use the already supported native Slot profile, but put **exactly one rib in
each Sketch**. Each of the nine Sketches is extruded as its own 0.6 mm cut.

This retains the intended rounded line engraving while preventing intersections
between closed profiles from generating selectable cube-face regions.

SCPF and independent SCPC use the same nine centerlines and the same
one-Sketch/one-Slot/one-cut construction.

## Verification

Regression tests require:

- nine separately named top-logo Sketches;
- exactly one 0.6 mm Slot profile per rib Sketch;
- nine independent 0.6 mm negative cuts;
- no polygon/sketch.line workaround;
- identical SCPF/SCPC Slot geometry.

The PR render must be visually inspected before merge. A green command-plan
test alone is not sufficient acceptance for this logo correction.
