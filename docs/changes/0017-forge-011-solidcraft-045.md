# 0017 — Qualify released Forge 0.11 with SolidCraft 0.45

Status: qualification pending

Issue: #172

## Goal

Adopt the already released Forge v0.11.0 and SolidCraft 0.45.0 in the
product CAD repository after the central runtime migration (#170/#171).

## Exact inputs

- Forge v0.11.0: annotated release tag targeting
  `9258d54079981604b6dd777a4c4face897c190fe`;
- central runtime `ghcr.io/brainboxemb/cad-solidcraft:v0.3.4`;
- runtime engine version `SolidCraft 0.45.0`;
- SCPC and tool.cad.ci consumer pins remain unchanged.

## Contract

- `dependencies.repos` is the source of truth for exact SCPF/SCPC/tool pins.
- `ci/toolchain.json` pins the released central runtime and the qualified
  engine version. No consumer Dockerfile or runtime rebuild.
- The Forge source itself declares `TESTED_SOLIDCRAFT_VERSION = "0.45.0"`.
  Native CI fails if that and the runtime disagree.
- Verification evidence records actual source commit, Forge release, exact
  commands commit, SolidCraft version and runtime image.
- Updating the toolchain pins does not automatically mark every retained
  model natively verified against 0.45.0. Only completed native builds may
  carry the new provenance.

## Consumer compatibility findings

The first Forge 0.11 / SolidCraft 0.45 PR run found two obsolete consumer
API usages:

- `sample_plate` used removed `Shape.repeat_linear()`. Replace it with one
  explicit `Holes` sketch source cut and a native rectangular feature
  pattern, keeping width-driven pitch and feature history. Update the
  model catalog to describe the resulting three sketches and pattern.
- `corner_bracket/scpf/reference.py` is an archived, historical 42-command
  hole experiment and uses removed `Hole(countersink_*)` options.
  Preserve the reference verbatim; test its historical content as an archive
  instead of pretending it still compiles under modern Forge.
  The production CornerBracket remains the separate hole-free component.

## Verification plan

1. Run the ordinary PR pipeline against the released inputs and fix any
   diagnosed compatibility problems in the owning upstream repository.
2. Run explicit full catalog qualification after initial selected smoke; do
   not silently change normal model selection rules.
3. Compare native design/STEP/measurements, record any blocked models, and
   promote only successfully qualified results.

No Forge or central runtime release is created by this consumer change:
both artifacts already exist.
