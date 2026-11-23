# 0034 — FlexBenchDog MFT stop collar

Issue: #331

## Problem

The current FlexBenchDog uses a plain Ø24 × 3 mm cylindrical rim. The intended
MFT design uses a much smaller shaped stop collar that seats on the small 45°
mouth chamfer of a nominal Ø20 dog hole.

## Decision

Use a Ø22 × 1.5 mm collar envelope at the worktop datum and chamfer only its
lower outside edge by 1.0 mm.

The Ø22-to-Ø20 radial difference is exactly 1.0 mm, so a 1.0 mm standard edge
chamfer creates the required 45° seat:

- Z=0 underside reaches Ø20 and meets the shaft;
- Z=0..1.0 is the 45° seat;
- Z=1.0..1.5 retains a 0.5 mm straight Ø22 outer land.

The upper Ø20 working cylinder therefore starts at Z=1.5 and is 18.5 mm high,
preserving the existing Z=20 top datum.

This is model-specific geometry. No new Forge primitive or local compiler
workaround is introduced.

## Verification

SCPF and SCPC both create the same Ø22 × 1.5 mm collar, select the lower outside
edge for a 1.0 mm chamfer, and start the upper Ø20 section at Z=1.5.

Focused regression checks prove the collar dimensions/profile and keep the
overall 20 mm above-worktop extent unchanged. Durable rendering is reviewed
after merge.
