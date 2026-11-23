# 0041 — Rounded FlexBenchDog central slot corners

Issue: #333

## Problem

The two rectangular flex-slot cuts create four sharp vertical material edges
around the central cross. The supplied underside reference shows those four
corners softly rounded.

Using native sketch Slot profiles would round the slot end caps, not these four
material-side corners, and would therefore solve the wrong geometry.

## Decision

Keep the existing perpendicular 1.5 mm × 16 mm rectangular cuts and their
4 mm solid root.

After both cuts, fillet exactly the four vertical material edges at the central
cross with an explicit `slot_corner_radius` parameter. The initial reviewed
value is R0.5 mm.

The edge picks are at ±slot_width/2 in X/Y and halfway through the slot height
(Z=-12 for the current 20 mm insertion / 16 mm slot).

This changes only the corner relief; slot width, slot length and root length
remain unchanged.

## Verification

SCPF and independent SCPC sources both emit one four-edge fillet feature.
Regression checks preserve the two rectangular slot cuts and require four
selected inner edges. Durable rendering is reviewed against the supplied
underside reference before final acceptance.
