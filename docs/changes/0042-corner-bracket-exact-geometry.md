# 0042 — CornerBracket exact relief and fixing geometry

Issue: #8

## Problem

The active shared CornerBracket diverged from the preserved OpenSCAD model in
two important ways.

First, the 0.6 mm arm-tip print relief had been removed from the 2D L profile
and approximated as one chamfer along each full 24 mm extrusion edge. That is
not the same topology as the original tip bevel.

Second, the live reusable bracket had all mounting holes removed after earlier
native warnings. The archived design shows that a screw-head seat is not one
large countersink: it contains a flat cylindrical recess before the 90-degree
transition and has separate shallow edge relief at both faces.

## Decision

Keep the core 24 mm width, 12 mm wall and 60 mm arm lengths.

Restore the two 0.6 mm tip reliefs directly in the XZ polygon, matching
OpenSCAD `base_profile_2d()`. Remove the former full-width tip-edge chamfer.

For each of the four M5 fixing positions (24 mm and 42 mm on both arms), build
the seat from four explicit native operations:

1. Ø10.4 × 1.0 mm cylindrical head recess from the outside face;
2. a 90° countersink beginning 1.0 mm inside the wall and transitioning from
   Ø10.4 to the Ø5.4 clearance bore;
3. Ø10.8 × 0.2 mm flat outside edge relief;
4. Ø5.8 × 0.2 mm flat inside edge relief.

This preserves the flat-bottom head seat instead of pretending a larger
countersink is equivalent.

SCPF and independent SCPC both describe the same 42-command default model.

## Arm-tip wedge acceptance

OpenSCAD also applies a small local `arm_tip_relief_wedge()` correction where
the broad-face relief meets the diagonal side chamfer. The restored 2D profile
removes the known incorrect full-width tip chamfer first.

Native render inspection is required before #8 can close. If a remaining local
triangular remnant still requires an arbitrary rotated wedge/cutter capability
that released Forge cannot express, create or reuse the generic Forge owner
issue. Do not introduce a CAD-local transform workaround.

## Verification

- exact 11-point named profile;
- 19 model parameters;
- 16 native hole commands (four per fixing position);
- two remaining chamfer features plus the R4 fillet;
- 42 commands in both SCPF and independent SCPC;
- native SolidCraft build and semantic verification;
- rendered image inspection for the two arm-tip junctions and all four fixing
  seats.
