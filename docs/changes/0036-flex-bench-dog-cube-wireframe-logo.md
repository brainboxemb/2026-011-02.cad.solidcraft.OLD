# 0036 — FlexBenchDog cube-wireframe logo

Issue: #332

## Problem

The current FlexBenchDog cuts one filled 8 × 8 mm square into the top face.
That is not the intended BrainBox mark.

The preserved historical branch
`feature/refine-conical-flex-bench-dog` contains the exact intended logo and
is the source of truth for this change.

## Decision

Replace the filled square with nine recessed 0.6 mm-wide native Slot strokes:

- six segments form the outer isometric cube/box perimeter;
- three spokes run from the centre to the top and lower-right/lower-left
  vertices;
- recess depth remains 0.6 mm.

Exact centreline endpoints:

```text
( 0.0,  4.0) -> ( 3.5,  2.0)
( 3.5,  2.0) -> ( 3.5, -2.0)
( 3.5, -2.0) -> ( 0.0, -4.0)
( 0.0, -4.0) -> (-3.5, -2.0)
(-3.5, -2.0) -> (-3.5,  2.0)
(-3.5,  2.0) -> ( 0.0,  4.0)
( 0.0,  0.0) -> ( 0.0,  4.0)
( 0.0,  0.0) -> ( 3.5, -2.0)
( 0.0,  0.0) -> (-3.5, -2.0)
```

SCPF uses `SlotCenterToCenter2D`; SCPC uses
`sketch.slot.center_to_center`. No filled polygon or replacement square is
retained.

## Verification

Focused tests compare all nine exact endpoints, require 0.6 mm stroke width
and 0.6 mm negative cut depth, and reject the historical filled 8 × 8 mm
rectangle. SCPF and SCPC contracts must match and full CAD verification must
remain green.
