# 0016 — Reuse the released central SolidCraft runtime

Status: implementation

Issue: #170

## Problem

This CAD repository still owned `docker/cad/Dockerfile` and
`.github/workflows/image.yml` even though reusable SolidCraft runtimes are now
owned and released by `brainboxemb/docker.cad.solidcraft`.

The local image also baked the exact SCPF and SCPC consumer revisions into the
image. A Forge or Commands pin update therefore caused another Docker build
without changing the SolidCraft engine/runtime itself.

## Decision

Use the released central SolidCraft runtime and keep consumer Python libraries
outside that image.

- pin `ghcr.io/brainboxemb/cad-solidcraft:v0.3.2`;
- preserve the existing SolidCraft 0.42.0 qualification baseline;
- keep exact SCPF, SCPC and tool.cad.ci revisions in `dependencies.repos`;
- check out all three under `ext/` before the CAD run;
- mount the repository into the runtime and expose SCPF/SCPC through
  `PYTHONPATH`;
- pass exact SCPF/SCPC provenance into native verification metadata;
- remove the local Dockerfile, local image workflow and image-publication race
  helper.

A Forge/Commands pin change no longer creates a Docker image. A SolidCraft or
runtime-composition change is released in `docker.cad.solidcraft` first and
then adopted here through a new immutable runtime tag.

## Verification

- the runtime resolver accepts only released
  `ghcr.io/brainboxemb/cad-solidcraft:vX.Y.Z` references;
- exact dependency checkout tests cover SCPF, SCPC and tool.cad.ci pins;
- the normal CAD workflow pulls the released runtime directly;
- native verification continues to check Forge's tested SolidCraft version and
  records runtime image, SolidCraft, SCPF release/commit and SCPC commit.
