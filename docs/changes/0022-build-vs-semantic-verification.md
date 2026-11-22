# 0022 — Separate model build acceptance from optional semantic verification

Issue: #174

## Problem

The staged shared batch had 11 enabled physical model roots. The remaining
five were blocked because the CAD-specific batch adapter treated a local
`verification/verify.py` as mandatory. That made semantic assertions a
migration prerequisite even when a model had no useful, stable physical
contract to assert.

This conflated two different questions:

1. can the model actually be built by the accepted Forge/SolidCraft toolchain;
2. does this model benefit from additional model-specific semantic checks.

## Decision

Every model root that the accepted Forge/SolidCraft stack can currently build
participates in the same released CAD-CI shared batch. Two advanced assemblies
remain temporarily disabled because Forge #679 must first namespace repeated
component-local feature names; no CAD-local naming workaround is allowed.

For every processed model, build acceptance requires command generation and a
real SolidCraft build with non-empty saved-design, STEP and preview output plus
truthful provenance.

A local `verification/verify.py` is optional. If present, the released
`lib.py.cad.verification` contract runs and the provenance records semantic
verification as `pass`. If absent, the provenance records
`semantic_verification: not-configured` and compatibility field
`solidcraft_verified: false`.

Independent Forge/SCPC comparison remains semantic verification and therefore
requires a local verification definition.

## Boundaries

- No second planner, changed-file selector or per-model runtime is introduced.
- Missing semantic verification is not a build failure by itself.
- Build-only output must never be presented as semantically verified.
- Existing useful model verification definitions remain model-owned.
- Additional semantic checks are added because they improve engineering
  confidence, not to satisfy a catalog-coverage metric.

## Verification

Repository tests require the 14 currently buildable physical roots to be
`process: true`, explicitly name the two Forge #679 blockers, and allow only
the currently useful subset to own `verification/verify.py`. The shared batch still contains exactly one Docker
pull/run path and model items still project results through released
`copy: dependency` semantics.
