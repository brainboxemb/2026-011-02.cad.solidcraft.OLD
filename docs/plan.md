# CAD repository plan

This file contains only unfinished work and its priority.

Historical results, merged work, run IDs and completed migrations do not belong
here. Use GitHub issues/PRs, change records and the changelog for that history.

The repository owns product/project CAD models and their repository-specific
verification and presentation. Reusable Forge behavior belongs in
`lib.py.solidcraft.forge`; generic CAD-CI belongs in `lib.py.cad.ci` /
`tool.cad.ci`; generic verification belongs in
`lib.py.cad.verification`; runtime packaging belongs in
`docker.cad.solidcraft`.

## Working branches

- `main` — stable integration.
- `dev-cad` — model/API/presentation work.
- `dev-ci` — CI/publication integration.

Development branches may accumulate several accepted changes. Promote to
`main` only at a useful stable checkpoint, not after every PR.

## Now

### 1. Finish the three already-implemented model changes

Do not start a new broad model project while these technically completed changes
are still waiting for final review.

- **#348 / PR #426 — FlexBenchDog logo cleanup**
  - Polygon2D implementation is built and verified.
  - Remaining work: inspect the final logo render and either accept it or fix a
    concrete visible mismatch.
  - Do not reopen the old Slot construction unless the visible geometry is
    actually wrong.

- **#362 / PR #429 — CornerBracket arm-tip wedges**
  - Wedge geometry is implemented and technically green.
  - Remaining work: inspect horizontal/vertical tip views and accept or correct
    concrete geometry.
  - Preserve the already accepted arm profile and recessed fixing-seat geometry.

- **#373 / PR #430 — HUB75 rear-bay contours**
  - Rear bay contour, rail step and recess work is implemented and technically
    green.
  - Remaining work: inspect the rear view against the preserved reference and
    accept or correct concrete geometry.

The missing convenient PR-render path is a CI/tooling problem. It must not
cause unrelated CAD development to invent a local publication system.

## Next

### Continue actual CAD model work

After the three current model PRs have their visual review, continue model work
before repository metadata cleanup.

Priority order:

1. finish #348 / PR #426 if the logo render is correct;
2. finish #362 / PR #429 if the arm-tip views are correct;
3. finish #373 / PR #430 if the rear-bay render matches the reference;
4. continue #375 / PR #390 as far as standalone panel geometry permits;
5. as soon as #388 is unblocked upstream, return immediately to the complete
   `hub75-screen` assembly and final five-panel acceptance.

Do not substitute repository metadata/site work for available CAD model work.

### HUB75 detailed-panel completion after #373

The reusable detailed HUB75 panel remains the owner of panel-side mechanical
interfaces.

- **#374** mounting tubes/bushings/locator pins is already implemented
  standalone; no new work unless upstream placement behavior requires a
  correction.
- **#375 / PR #390** connector envelopes remains parked until #388 is resolved
  well enough to validate the complete assembly.
- **#371** remains the tracking issue for these detailed-panel children.

Do not duplicate detailed panel dimensions into the wooden enclosure.

### Model metadata contract — #205

Repository metadata cleanup, not CAD model work.

Keep separate from the parallel model stream. Execute only when the CAD Forge
pin actually contains the accepted canonical metadata contract; do not copy a
newer Forge validator locally.

### CAD-CI consumer migration — #288

Keep this on `dev-ci`, separate from model work.

The current shared-tool interface is being reconsidered in `tool.cad.ci`.
Do not patch the historical CAD workflow locally while that contract is still
being corrected.

When the shared interface is stable and externally accepted:

1. migrate the CAD repository to it;
2. remove obsolete local generic orchestration;
3. prove normal PR, branch and manual execution from the released shared path.

### Full-catalog build and verification — #172

A deliberate complete repository build is still required.

Do not fake it by editing model process flags or changing source merely to
trigger selection. Use the released shared CI mechanism once that route is
clear and working.

## Blocked

### #388 — HUB75 component-local Cylinder placement

Five panel occurrences are placed correctly, but the detailed component can
leave joined Cylinder-derived rear features in world/component-definition
space.

Forge #753 now contains a merged native reproducer. Exact Forge dev-cad run
`45361627528` passes on SolidCraft 0.45.0 and its generated preview shows the
simple Box + one joined Cylinder copied/rotated case correctly: no loose source
Cylinder is visible.

Therefore #388 is **not** reproduced by the simplest generic Cylinder-join
occurrence case. The owner-layer reproducer must preserve more of the real
Hub75Panel feature history until the smallest failing difference is known.
SolidCraft #21098 / PR #21145 remains a relevant lead, but is not yet proven to
be the exact CAD #388 defect.

No CAD-local transform or placement workaround.

Consequences:

- #375 final five-panel acceptance waits here;
- #382 stable CAD checkpoint remains paused;
- enclosure work that depends on trustworthy detailed rear geometry also waits.

### #367 — native exploded HUB75 assembly view

Blocked on reusable Forge explode support (#751).

Do not bake exploded offsets into the normal assembled model.

### #135 / PR #141 — Bolted Flange circular pattern

Blocked on Forge #347 for the intended applied-feature pattern source.

Keep parked; do not replace the intended native relationship with a loop
workaround.

### PR #169 — latch

Keep parked until its required Forge API baseline is available. Do not mix latch
work into the current HUB75/model-cleanup sequence.

## Later

These are valid ideas but are not current priorities.

- **#417 — HUB75 display-case paths/model ids/public slugs.**
  Compatibility migration only after the model family and current build
  contracts are stable.

- **#20 — multiple verified model views.**
  The existing `extra_views` mechanism is sufficient for current review work;
  a broader gallery can wait.

- **#21 — interactive SolidCraft viewer.**
  Product/site enhancement, not a current model blocker.

- **#365 — glazing retention, pressure and sealing.**
  Do not start yet. The physical retention/sealing design has not been agreed,
  and guessed hardware/pressure geometry would create rework.

- **#366 — HUB75 rear mechanical/electrical enclosure interfaces.**
  Resume only after the reusable panel-side interfaces are trustworthy.

- **#7 / #8 / #371 — tracking issues.**
  Use their focused child issues for implementation; do not create broad
  catch-all PRs from the trackers.

## Priority rules

Use these rules when choosing new work:

1. Finish an already-implemented, technically green model change before
   starting another model slice.
2. Prefer independent CAD work while an upstream Forge/SolidCraft/CI issue is
   blocked.
3. Do not create CAD-local workarounds for generic Forge, SolidCraft or CAD-CI
   defects.
4. Do not promote `dev-cad` or `dev-ci` to `main` merely because one PR
   turned green.
5. Do not put completed work, run logs, old SHAs or historical migration notes
   back into this plan.
6. Reconcile this file when priorities change materially, not after every
   individual CI run.
