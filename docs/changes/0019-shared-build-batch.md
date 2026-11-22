# 0019 — One shared SolidCraft model-build batch

Issue: #174; generic architecture requirements are routed through Forge #661.

## Decision

Replace the CAD development lane's temporary one-Docker-start-per-model
implementation with the **already released Forge batch pattern**, not another
CAD-CI scheduler.

- Released CAD-CI discovers each item, resolves dependencies, and invokes
  one SCons graph.
- One `ci/model-build-batch` item consumes pinned Forge/SCPC/verification
  packages, prepares commands from the enabled model sources, then starts
  SolidCraft **once** to build/check all enabled models.
- A model's simple `ci.yml` declares only id, shared template, process.
  Its build outputs are copied from the batch through released
  `copy: dependency`, preserving model-specific files and checks.
- Model roots are discovered via the three section globs, not a manually
  extended item list. Nine previously exercised roots are enabled initially;
  seven are disabled until checked.
- One shared build has a known granularity trade-off: it may rebuild all
  enabled models when a batch input changes. Resolve any required generic
  selection improvement via Forge #661.

## Boundaries

Main workflow and public CAD Pages remain unchanged until all 16 roots /
18 catalog variants and independent SCPC comparisons have passed. Website
layout, images, source/download links and URLs are preserved. The internal
`native/` result folder is retained only for backwards compatibility;
newly written human-facing instructions use build/check/results terminology.

## Acceptance evidence

**Accepted first shared build: PR #184, squash-merged to `dev-ci` at
`670960db48c80317a37f72bc1ea0a62a09595090`.**

- 13/13 SCons targets built with zero errors: Forge, SCPC and verification
  package wheels; the single shared batch; nine model-output copies.
- All nine enabled SolidCraft models passed their checks; four available
  independent Forge/SCPC shapes agreed in bounds and volume.
- Exactly **one** Docker runtime startup for nine models. Batch total
  **29.843 seconds** (8.791 seconds image pull and 20.721 seconds
  inside the container).
- Seven untested physical model roots remain `process: false`; this
  is deliberately not full-catalog acceptance.
- `main` and public Pages were not changed by the PR.

Remaining acceptance work: A PR into `dev-ci` must prove one Docker run per batch, result projection
for each enabled model, separate failure evidence, complete build assets,
expected geometry and independent comparisons. Selective and full-run
behavior must be measured; no claim of full migration before tests pass.

See `docs/handoff.md` for a short new-chat transfer and
`docs/plan.md` for the active migration status.
