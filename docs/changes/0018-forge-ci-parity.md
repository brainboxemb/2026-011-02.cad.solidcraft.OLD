# 0018 — Align CAD CI architecture with Forge

Status: design approved for staged migration; implementation incomplete

Issue: #174

## Context

CAD uses central SolidCraft Docker and has adopted Forge 0.11.0 but still
duplicates generic model selection, orchestration, verification and publishing.
The main run succeeded without rebuilding every model when the engine pins
changed. Adding one more custom trigger would perpetuate the duplicated CI.

Forge already uses the released `tool.cad.ci` root action, one SCons graph,
released verification, immutable runtime roles, permanent source lanes and
isolated generated build/Pages scopes.

## Decision

Migrate the **infrastructure** to Forge's released architecture; do not
reimplement it. Keep the product model catalog, SCPF/SCPC sources, model
expectations, result-page content and renders in this CAD repository.

Full target: `main`/`dev-cad`/`dev-ci` source lanes with corresponding
complete build scopes and Pages root/subtrees, exact released tools, SCons
selection and native verification package ownership.

Normal PRs remain selective and do not publish durable preview output.
Promotion and version-upgrade acceptance requires complete processed model
execution with version-matched native evidence.

## Migration and verification

See `docs/plan.md` for staged implementation, ownership, rollback/cutover
gates and acceptance requirements. The current `cad.yml` and
`scripts/ci/pipeline_ci.py` remain operational until the released replacement
is proven; this record does not authorize premature deletion or changes to
already accepted build/Pages data.

Do not close #172 on the basis of an ordinary selected-model run.
