# CAD repository requirements

This document defines the target CI and publication contract for
`2026-011-02.cad.solidcraft`. Migration tracking is in `docs/plan.md`;
historical decisions are in `docs/changes/`.

## Ownership

The accepted Forge CI stack is the reference design, not another
implementation to copy into this repository.

- `tool.cad.ci` is the only generic runner/CLI/workflow surface.
- `lib.py.cad.ci` owns changed-path selection, dependency closure, SCons
  execution, up-to-date decisions, result reuse, complete build manifests,
  generated-branch publication and retry.
- Released `lib.py.cad.verification` owns general native SolidCraft evaluation,
  mutations, checks and machine-readable evidence.
- `docker.cad.solidcraft` owns the immutable SolidCraft runtime; this
  repository may only select its released image.
- Forge and SCPC own their Python APIs; this repository pins exact released
  source revisions and owns CAD model content.
- This repository owns model-specific expectations, SCPF/SCPC model production,
  comparison intent, website prose, catalog presentation and presentation
  images.

Do not create a second CAD-specific generic selector, SCons scheduler,
verification engine, build-store implementation or Pages publisher.

## Same source lanes and generated scopes as Forge

Permanent source branches: `main`, `dev-cad`, `dev-ci`.

- Short-lived CAD/model PRs target `dev-cad`.
- CI/publishing migration PRs target `dev-ci`.
- Feature/fix PRs are **squash-merged** into the corresponding dev lane.
- Lane-to-`main` promotions use a **normal merge commit** through the
  owner-controlled merge policy, not squash; the long-lived lane is retained.
- PRs validate without writing durable model output.
- Pushes to a long-lived branch may publish only their own generated scope:
  `build/main`, `build/dev-cad`, `build/dev-ci` and Pages root,
  `dev-cad/`, `dev-ci/`.
- A generated-branch writer may not overwrite sibling scopes or force-push.
- Preserve the current stable site and model URLs through the migration.

## Workflow and model ownership

- The workflow invokes the **exact released** `tool.cad.ci` root action,
  as Forge does, including a tested bounded `jobs` value.
- Root `cad-ci.yml` declares runtime variables, templates and item discovery.
- Each model-root `ci.yml` declares participation, source watches, dependency
  edges, steps and expected outputs. One physical model root may own multiple
  website/catalog variants.
- A model-specific change selects only the affected model and its declared
  dependants; SCons decides whether a selected action needs to run.
- A source-level change to Forge/SCPC/verifier/runtime that changes model
  semantics invalidates the affected outputs. A deliberate full model check
  is required for runtime or Forge version promotions.
- Promotion PRs from `dev-cad`/`dev-ci` into `main` run all processed CI
  items, including their actual SolidCraft model execution; unit tests alone
  are not model acceptance.
- Documentation-only changes that cannot change technical outputs avoid
  expensive model runs under the same narrow Forge-style PR classifier.
- A model is reported as built against a new toolchain only when its own
  saved native design, STEP/results and checks were produced under that
  toolchain. Merely refreshing the website or command JSON does not count.

## Verification and results

- Keep the semantic checks declarative beside their models; do not bury model
  expectations inside the GitHub workflow, general Python runners or HTML.
- Preserve SCPC-versus-Forge comparison where the model has an independent
  SCPC source.
- Native output must contain the editable `.sc`, STEP where supported,
  measurements/check results, required renders and exact input/version
  provenance. Required artifacts missing or empty fail that model.
- Never relabel retained old results as newly checked after a library or
  runtime update.
- Publication consumes a **complete** accepted build scope and produces one
  validated site; it does not regenerate or mutate CAD geometry.

## Adoption gates

Before removing the current working workflow, prove: all 16 current model-root
CI items and their 18 catalog variants are represented; selective
single-model execution; full-model execution on promotion/version upgrade;
matching output/verification provenance; independent stable/dev scopes;
and site-generation acceptance. Do not change model geometry to disguise a
missing generic CI feature.
