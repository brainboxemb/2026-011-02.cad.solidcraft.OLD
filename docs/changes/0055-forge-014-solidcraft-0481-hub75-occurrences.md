# 0055 — Adopt Forge v0.14.0 and SolidCraft 0.48.1 for HUB75 occurrence acceptance

Issue: #388

## Problem

The detailed five-panel HUB75 screen is blocked by the owner-layer
component-local joined-Cylinder occurrence regression. The product model itself
is already correctly placed and must not grow a CAD-local geometry workaround.

The accepted CAD baseline still consumes Forge v0.13.2 and
`cad-solidcraft:v0.3.4` / SolidCraft 0.45.0, so it cannot prove the released
owner fix.

## Decision

Adopt the exact released owner baseline together:

- Forge v0.14.0 source
  `cd46d6797df319b9d13605c11568990113772700`;
- immutable `ghcr.io/brainboxemb/cad-solidcraft:v0.3.5`;
- SolidCraft 0.48.1.

Forge v0.14.0 permanently retains the generic component-local joined-Cylinder
regression and was released only after that case passed on runtime v0.3.5 /
SolidCraft 0.48.1.

This change updates consumer dependency/toolchain pins only. It does not alter
HUB75 geometry, placements, Cylinder definitions or render-specific hiding.

## Repository contract

- `dependencies.repos` owns the exact Forge source revision.
- `ci/toolchain.json` owns the immutable SolidCraft runtime and expected
  SolidCraft version.
- `cad-ci.yml` uses the same runtime/version for the shared CAD graph.
- the exact-pin repository test must match the new Forge source.
- dependency/runtime changes deliberately select the affected model graph; do
  not add a model-local selection workaround.

## Verification

Acceptance for #388 requires:

1. repository tests green on the exact pins;
2. shared SolidCraft build/verification green on runtime v0.3.5 / 0.48.1;
3. source-matched durable `hub75-screen` output;
4. five intended HUB75 panel occurrences only, with no loose mounting-tube,
   reinforcement-cylinder or locator-pin geometry at the component-definition
   origin;
5. no product-model geometry workaround in the diff.

After that evidence is durable, #388 can close and #375 / PR #390 can resume
its final five-panel connector acceptance.
