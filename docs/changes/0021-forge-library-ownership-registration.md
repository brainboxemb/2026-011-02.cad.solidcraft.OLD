# 0021 — Forge CAD-library ownership and product registration boundary

Issue: #174

## Problem

Migration documentation had drifted into saying that generic CAD-CI requests must
be decided by Forge first. That makes Forge look like the owner of CI architecture,
while Forge's actual central role is the reusable CAD library. The CAD repository
also has a legitimate product `model_catalog.py`, which risks being confused with
generic CI item discovery.

## Decision

- Forge is the central reusable CAD library: API, compiler/lowering, modelling
  semantics and reusable CAD capabilities.
- `lib.py.cad.ci` / `tool.cad.ci` own generic CAD-CI behavior.
- `lib.py.cad.verification` owns generic verification behavior.
- `docker.cad.solidcraft` owns the immutable SolidCraft runtime.
- This repository owns product models and one product catalog for model identity,
  variants, product dependencies and site/presentation metadata.
- Generic CAD-CI discovers executable physical items through distributed `ci.yml`
  declarations; it does not depend on the product catalog and Forge is not a
  cross-repository model registry.
- A downstream request for a reusable modelling/API/compiler capability belongs
  in Forge. A product-model registration change stays here.
- Forge #661 is consumer acceptance evidence for shared-batch selectivity only.
  A demonstrated generic CI gap becomes an issue/change in the actual CAD-CI
  owner repository before consumers adopt the resulting release.

## Verification

- `AGENTS.md`, requirements, design, plan and handoff use the same ownership rule.
- Adding a physical model root requires a small `ci.yml` and product catalog entry
  only where product variants/site metadata require it; no workflow slug list or
  Forge registration is introduced.
- No consumer-local changed-path planner, scheduler or generic cache is added.
