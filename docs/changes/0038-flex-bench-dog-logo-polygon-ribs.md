# 0038 — FlexBenchDog logo polygon ribs

Issue: #332

## Problem

PR #341 used the correct nine centerlines of the BrainBox wireframe cube, but
placed nine intersecting closed Slot profiles in one Sketch. Their intersections
created additional enclosed sketch regions. The resulting recess visually
removed a filled six-sided face instead of only engraving the cube ribs.

## Decision

Keep the nine accepted cube centerlines and the 0.6 mm line width / 0.6 mm
recess depth.

Do not represent the complete logo as intersecting closed profiles in one
Sketch. Convert every centreline to one narrow square-ended four-vertex
`Polygon2D` strip. Extend each end by half the line width so neighbouring rib
cuts overlap cleanly at a cube vertex.

Cut the nine rib polygons independently. This makes the intended material
removal explicit: only the nine visible ribs are recessed, while all three
projected cube faces remain material.

SCPF and SCPC use the same polygon-strip construction. The supplied BrainBox
logo image is the visual source of truth; the preserved centerline coordinates
remain the dimensional construction.

## Verification

Regression tests require:

- nine `sketch.line` closed quadrilateral profiles;
- nine independent logo cuts;
- no `sketch.slot.center_to_center` logo profiles;
- matching SCPF/SCPC polygon coordinates;
- 0.6 mm recess depth.

The PR render must be visually inspected before merge. A green command-plan
test alone is not sufficient acceptance for this logo correction.
