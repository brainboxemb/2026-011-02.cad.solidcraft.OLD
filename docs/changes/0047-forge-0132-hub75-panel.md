# Change 0047 — adopt Forge v0.13.2 and restore detailed hub75-panel

Issue: #421

## Problem

Forge v0.13.1 adoption exposed Forge #796 in the existing detailed
`hub75-panel`: symbolic placed-Cylinder anchor arithmetic could mix a native
string expression with a Forge `Expression`.

CAD #408 temporarily set the model root to `process: false`; CAD #412 made
only the direct detailed-panel repository tests follow that same process state.

Forge v0.13.2 fixes #796 at exact release commit
`ea5710a5d2d33b0633b93c5da95dd5b74f126aa4`.

## Decision

Adopt exact Forge v0.13.2 as the CAD source dependency and restore
`models/components/hub75_panel/ci.yml` to `process: true`.

Keep the #412 test mechanism: tests that directly compile the detailed panel
continue to derive their enabled state from the model root's `ci.yml`.
Restoring normal processing therefore restores those tests automatically; no
second release/version switch is introduced.

Do not change panel geometry and do not add a CAD-local compiler workaround.

Forge #753 / CAD #388 remains a separate component-local
Cylinder/occurrence problem and is not resolved by this change.

## Verification

- dependency bootstrap pins exact Forge v0.13.2;
- the shared model-batch contract reports all 16 physical roots active;
- direct detailed-panel repository tests execute instead of being skipped;
- the former Forge #796 `str + Expression` failure does not recur;
- `hub75-panel` completes a real SolidCraft build and required saved outputs;
- #408 and #412 can close after the accepted merge.
