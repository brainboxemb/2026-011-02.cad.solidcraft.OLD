# 0050 — collapse duplicate HUB75 v2 roots

Issue: #427

## Problem

The repository accidentally represented one product evolution as two separate
advanced model roots:

- `hub75-display2` from #142 was only the initial v1-geometry comparison
  baseline for Hub75DisplayCase v2;
- `hub75_wood_frame_iter2` from #154 contained the actual v2
  lower-compartment geometry.

`WoodenHub75BoxIter2` is not a third enclosure product. It is
Hub75DisplayCase v2.

## Decision

Keep exactly two wooden HUB75 enclosure products:

1. Hub75DisplayCase v1 in `hub75_wood_frame`;
2. Hub75DisplayCase v2 in `hub75-display2`.

Move the complete accepted #154 geometry into `hub75-display2` and remove the
temporary separate `hub75_wood_frame_iter2` root.

## Preserved v2 geometry

The canonical v2 root keeps the 844 × 362 mm display opening, 70 mm editable
lower compartment, 12 mm intermediate shelf, 30/40/30 lower bays, 120 mm
cabinet depth, side hand slots, inset rear board, derived Z=94 mm display
datum, five HUB75 panels, eight CornerBrackets and the native 70→90 mm
`lower_compartment_height` saved-design verification.

## Repository effect

- class: `Hub75DisplayCaseV2`;
- public/root id remains `hub75-display2`;
- remove `hub75_wood_frame_iter2`;
- physical roots: 17 → 16;
- catalog variants: 19 → 18;
- all 16 physical roots remain active;
- no accepted #154 product geometry is discarded.
