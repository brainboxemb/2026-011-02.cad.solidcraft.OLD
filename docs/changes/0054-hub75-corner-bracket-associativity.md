# 0054 — validate Hub75DisplayCase CornerBracket associativity

Issue: #77

## Context

The Hub75DisplayCase v1 assembly already places one reusable CornerBracket
definition eight times with explicit associative occurrence placements.

Repository command-contract tests already prove that:

- all eight bracket X placements retain `opening_width` and
  `frame_wood_thickness`;
- the four upper bracket Z placements retain `opening_height`;
- the four lower brackets remain at the bottom datum;
- four rear brackets retain `cabinet_depth`;
- the four corner orientations use the intended Y-axis quarter turns.

Issue #91 separately added native 12→18 mm frame-thickness verification. The
remaining #77 gap is native acceptance for opening-width/opening-height
changes.

## Decision

Add two model-owned SolidCraft saved-design regressions without changing SCPF
geometry:

- `opening_width = 1000 mm`;
- `opening_height = 400 mm`.

Each saved design verifies all eight CornerBracket body envelopes at 0.001 mm
bounds tolerance.

The envelope pattern is intentionally asymmetric around each placement datum,
so the checks prove both position and the four intended handedness/orientation
states:

- top-left: local X extends inward/right and local Z extends downward;
- top-right: local X extends inward/left and local Z extends downward;
- bottom-right: local X extends inward/left and local Z extends upward;
- bottom-left: local X extends inward/right and local Z extends upward.

Front/rear Y envelopes remain 0..24 mm and 76..100 mm.

## Expected native mutations

At `opening_width = 1000 mm` with 12 mm frame wood:

- bracket placement datum X becomes ±512 mm;
- left bracket envelopes become X=-524..-452 mm;
- right bracket envelopes become X=452..524 mm;
- Z and Y envelopes remain unchanged.

At `opening_height = 400 mm`:

- upper bracket placement datum Z becomes 424 mm;
- upper bracket envelopes become Z=364..436 mm;
- the four lower bracket envelopes remain Z=-12..60 mm;
- X and Y envelopes remain unchanged.

No CornerBracket geometry or assembly placement formula changes belong to this
issue.
