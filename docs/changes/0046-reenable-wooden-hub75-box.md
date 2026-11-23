# Change 0046 — re-enable existing WoodenHub75Box

Issue: #378

## Problem

The existing `hub75-wood-frame` root was disabled while Forge #679 prevented
repeated component-local feature names from replaying in SolidCraft. The first
PR #379 correctly selected the model but failed on released Forge v0.11.0 with
a duplicate `Profile` feature name.

CAD #405 has now adopted Forge v0.13.1, which contains the generic #679 fix.

## Decision

Re-enable only `models/advanced/hub75_wood_frame` by restoring
`process: true`.

Do not change model geometry, do not enable iteration 2 in this issue, and do
not add a CAD-local naming workaround.

The detailed `hub75-panel` root remains independently gated by #408/#412 for
Forge #796.

## Verification

- normal PR selection includes `hub75-wood-frame`;
- native SolidCraft replay no longer fails on duplicate `Profile` names;
- required saved model, STEP and preview outputs are produced;
- the active/blocked-root repository contract reflects only the intentional
  remaining gates;
- the merged dev-cad lane build source-matches the re-enabled root.
