# 0049 — remove the FlexBenchDog logo Slot workaround

Issue: #348

## Context

The accepted FlexBenchDog BrainBox mark has nine visible 0.6 mm-wide ribs and
a 0.6 mm recess depth. PR #347 deliberately implemented each rib as a separate
native Slot profile because the then-consumed Forge release could not lower
`Polygon2D` through the attached/explicit Sketch path.

Forge #747 is now released and consumed in Forge v0.13.2. The compatibility
construction is no longer needed.

## Decision

Preserve the accepted visible logo construction while replacing only its
profile representation:

- keep the same nine centreline segments;
- keep the 0.6 mm line width and 0.6 mm recess depth;
- convert each centreline to one square-ended four-vertex `Polygon2D` strip;
- extend each strip half a line width beyond both centreline endpoints so
  neighbouring ribs overlap cleanly at cube vertices;
- keep one attached top-face Sketch and one cut per rib;
- keep SCPF and the independently authored SCPC command model geometrically
  equivalent;
- remove the TEMPORARY #348 / Forge #747 Slot-workaround comments.

The already accepted full-length Cone taper from #327, Ø22 × 1.5 mm collar,
45° seat, R0.5 slot-corner fillets, slot dimensions and chamfers are unchanged.

## Verification

- SCPF emits nine closed four-point `sketch.line` profiles for the logo;
- neither SCPF nor SCPC emits a logo `sketch.slot.center_to_center`;
- all polygon coordinates match the nine preserved centreline constructions;
- nine independent 0.6 mm negative cuts remain;
- SCPF and SCPC polygon coordinates agree numerically;
- native SolidCraft build, semantic verification, STEP/STL/images and
  independent Forge/SCPC geometry comparison remain green;
- inspect the generated primary/top-visible render before merge and verify that
  the three projected cube faces remain open.
