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

**Explicit website constraint:** Preserve the current CAD Pages appearance,
home/category/model navigation, model screenshots and source presentation,
public model routes, downloads and truthful result labels in broad terms.
Forge's CI design is being adopted, not Forge's website layout. The existing
site generator and CSS remain the presentation baseline; comparison of
representative old/new pages is a cutover requirement. A redesign requires a
separate change.

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

## Staged development-lane evidence

- PR #177: permanent source lanes and site/catalog contract tests.
- PR #178: released CAD-CI built the Plate model on SolidCraft 0.45.0 (run
  45008030428). The Forge and verification wheels were built separately.
- Next PR: remove the Plate-only bridge and let one model-independent
  producer read the authoritative catalog for Plate and Vent Plate, including
  SCPC source models. This remains development-only, without stable Pages
  changes or a full-catalog acceptance claim.

- The two-model trial identified a parallel checkout race on SCPC. The fix
  is one pinned shared `scpc-package` dependency wheel, matching how Forge's
  wheel is prepared; model tasks only consume that existing wheel.
  The new shared template is named `cad-model-build`. User-facing text says
  model build/verification/results. Existing saved output folder names remain
  compatible until site migration. See Forge terminology issue #659.

- PR #180: five physical models built and checked by the released CAD-CI
  runner, with Forge and SCPC comparisons where present (8 targets, all pass).
- Next batch: Bracket, CSG Cube and two plastic enclosures. Basic shape,
  body and sketch expectations are checked first. Existing specialized
  construction-history, material and detailed geometric checks still need
  equivalent declarative coverage before claiming full check parity.
