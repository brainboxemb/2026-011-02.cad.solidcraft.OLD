# 0033 — FlexBenchDog full-length native Cone taper

Issue: #327

## Problem

The accepted FlexBenchDog still approximates the insertion fit with a straight
Ø20 × 20 mm cylinder plus a separate Ø20.2 × 2 mm cylindrical free-tip
overlay. That stepped construction predates reusable joined-Cone support.

An old draft attempted a 2 mm Cone but also carried obsolete Ø24 × 3 mm collar
geometry. It must not be rebased wholesale.

## Decision

Start from the current accepted FlexBenchDog and change only the insertion
profile:

- keep insertion extent Z=-20..0;
- use one native joined Cone/frustum for the complete 20 mm insertion;
- free end at Z=-20: Ø20.2;
- worktop end at Z=0: Ø20.0;
- remove the straight insert cylinder and secondary tip feature;
- keep the Ø22 × 1.5 mm stop collar and 1 mm 45° seat unchanged;
- keep the 16 mm crossing slots and 4 mm solid flex root unchanged;
- keep the R0.5 inner slot-corner fillets unchanged;
- keep the current recessed nine-rib BrainBox logo unchanged;
- keep SCPF and the independent SCPC command model physically equivalent.

Forge #746 is released and consumed in the current Forge v0.13.2 baseline, so
no CAD-local compiler workaround is required.

## Verification

- SCPF emits exactly one `solid.cone` for the insertion and no insertion
  `solid.cylinder`;
- SCPC emits the same full-length native Cone contract independently;
- cone base is Z=-20, height 20, bottom diameter Ø20.2 and top diameter Ø20.0;
- body envelope remains -20..+20 mm in Z and ±11 mm in X/Y;
- collar, slots, R0.5 fillets and top logo remain unchanged;
- native SolidCraft build and independent SCPC verification are green.
