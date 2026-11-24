# 0056 — Adopt Forge v0.15.0 for HUB75 replay-context acceptance

Issue: #388

## Problem

CAD already adopted Forge v0.14.0 together with immutable runtime v0.3.5 /
SolidCraft 0.48.1, but the source-matched durable five-panel `hub75-screen`
render still showed detached component-local Cylinder/tool geometry.

Forge #753 subsequently isolated the remaining defect to headless replay
transport: after a save/reopen checkpoint, Forge restored active Sketch context
but not the active reusable component context. Later joined features could
therefore change the correct component body while their visible feature/tool
history remained in root/world presentation context.

## Owner fix

Forge v0.15.0 is published at exact source:

`efc88bfcaf452051d721347f2e5ca561decad654`

Annotated tag `v0.15.0` resolves exactly to that commit. The release keeps the
already-qualified runtime unchanged:

- `ghcr.io/brainboxemb/cad-solidcraft:v0.3.5`;
- SolidCraft 0.48.1.

Forge #753 now restores active component context before any active-Sketch
restore when a headless replay phase continues after save/reopen. The retained
Forge owner preview is visually clean.

Temporary CAD qualification run `45396787004` rebuilt the full 16-root graph
on the accepted Forge fix, including a native PASS for `hub75-screen`, without
any CAD geometry change.

## Decision

Adopt only the exact Forge v0.15.0 source revision in `dependencies.repos`
and the matching exact-pin repository contract.

Do not change:

- HUB75 model geometry;
- occurrence placement;
- Cylinder definitions;
- runtime image;
- SolidCraft version;
- render visibility/hiding behavior.

## Final acceptance

After merge, the normal durable dev-cad output must:

1. source-match the adoption merge;
2. build the full affected CAD graph successfully;
3. produce the normal `hub75-screen/model.png`;
4. show exactly the five intended panel occurrences;
5. contain no detached mounting-tube, reinforcement-cylinder, locator-pin or
   other component-local Cylinder/tool geometry above/below the screen or at
   the component-definition origin.

Only that released-source durable render closes #388 and provides the final
downstream acceptance needed to close Forge #753.
