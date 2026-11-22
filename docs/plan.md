# CAD repository migration plan

Source of truth for the **unfinished** Forge-compatible CI migration:
[issue #174](https://github.com/brainboxemb/2026-011-02.cad.solidcraft/issues/174).
Permanent target requirements/design are in `docs/requirements.md` and
`docs/design.md`. Keep implementation history in numbered
`docs/changes/` records.

## Current accepted state — 2026-11-22

- PR #171 / commit `f615379bb2e8cb44e300dc87f9edf0983c6ea6cb`:
  CAD Docker moved to released central runtime.
- PR #173 / commit `ecda73518f465adbfb4678fc6a11803d40cabe97`:
  Forge 0.11.0 and SolidCraft 0.45.0 pins accepted.
- Main CAD run `45005747810` is green under the **old hybrid CI**.
- That run completed 184 unit tests, executed native SolidCraft for
  `sample-plate` and `corner-bracket`, and ran generic item
  compile/compare/package for two additional HUB75 roots.
  It did **not** build all CAD models in SolidCraft.
- #172 remains open: full-catalog Forge 0.11 / SolidCraft 0.45
  verification is not demonstrated.
- The repository has 16 physical model-root `ci.yml` items mapping to
  18 catalog variants. Permanent `dev-cad` and `dev-ci` branches were
  created at source commit `67e635e4bf6b0d3e371cf44d57e0f950255ddb34`.
  Their generated build/Pages scopes are **not yet published**.
  Build output and Pages remain main/PR oriented until M4.
- `cad-ci.yml` already exists, but generic execution is wrapped in
  `scripts/ci/pipeline_ci.py`. The workflow uses an older pinned
  `tool.cad.ci` and has separate project-specific selectors and publisher.

**Do not claim the Forge CI migration is completed by the successful runtime
upgrade or by a green selected-model run.**

## Work order

### M0 — Inventory and safe starting point

Status: **in progress** — source branches created, initial catalog/route
contract is being implemented on `dev-ci`; complete old/new Pages visual
comparison remains outstanding.

- Inventory all model-root items, 18 catalog variants, cross-model geometry
  dependencies, native/SCPC comparison flags and required saved artifacts.
- Capture stable build and Pages URLs/provenance before changes.
- Capture representative current CAD pages/screenshots and navigation:
  homepage, Basic/Components/Advanced, a simple model, a complex HUB75 model,
  and a model with independent SCPC; preserve their visual hierarchy,
  model-specific content and links as the comparison baseline.
- Keep all active model PRs isolated from the CI migration.
- Record the old code to retire versus CAD-specific content to retain.
- Define acceptance tests before any cutover.
- Enforce the 16-root/18-variant/5-SCPC-source inventory, model-root ownership,
  branch merge rules and website route/layout source contract with fast
  pre-cutover tests. Execute the existing site generator tests on development
  PRs without launching Docker.

### M1 — Released tooling and declarative model graph

Status: **five models accepted; next four-model batch in progress**.
PR #178 at `a4329d0791803572184b8ebf163adea737f7a372`
passed a real Plate build with released tool.cad.ci 0.17.0 /
lib.py.cad.ci 0.9.3, verification 0.15.0, Forge 0.11.0 and central
SolidCraft 0.45.0. The next stage uses one model-independent producer, adds Vent Plate,
and compares separate Forge/SCPC SolidCraft results. SCPC is prepared
once as a shared dependency to prevent simultaneous checkout conflicts;
all other roots remain outside the staged graph until checked. This is not full-catalog acceptance.

- Pin exactly Forge's accepted released
  `tool.cad.ci 0.17.0` /`lib.py.cad.ci 0.9.3` stack.
- Add the released CAD verification package as an **external** separately
  pinned dependency; never add it to the central Docker.
- Align `cad-ci.yml` runtime variables, templates, item discovery,
  `process`, watches, dependencies and output contracts with Forge.
- Test that every current model variant is accounted for and that a single
  source change selects only its declared affected items.
- SCons/released library must be the only owners of selection/reuse.

### M2 — Native verification and consumer step migration

Status: **five models built and checked; four further models in trial**.
The Plate model was built successfully by released CAD-CI. The next
stage converts Plate and Vent Plate to one model-independent producer, builds
and checks Forge and independent SCPC SolidCraft models and checks that their body
bounds and volume agree. Other model roots remain on the old main pipeline.

- Convert one representative basic model to model-local declarative
  verification and released `lib.py.cad.verification`, including native
  SolidCraft output and accurate provenance.
- Cover a model with independent SCPC output and a complex assembly.
- Convert the remaining model roots in reviewable groups, preserving
  geometry and current accepted result details.
- Keep model-specific expected outcomes and optional snapshots in CAD;
  remove generic JSON/schema/mutation/checker duplication only when parity
  has been demonstrated.

### M3 — Exact Forge workflow and long-lived lanes

Status: **not started** — development branches already exist, but the old
main workflow and publication path remain accepted until M1/M2 are complete.

- Use the exact released root `tool.cad.ci` action for PR and integration
  runs, not the existing `pipeline_ci.py` wrapper.
- Adapt Forge's thin workflow, docs-only PR classifier and explicit
  `jobs=2` *after* verifying CAD's own runner capacity.
- Introduce permanent `dev-cad` and `dev-ci`, owner-controlled merge
  policy, feature squash and lane→main merge discipline.
- Promotion PRs into main request a complete processed-model run.
- Keep PR verification-only, without new PR build/Pages publication.

### M4 — Durable build and Pages scopes

Status: **not started**.

- Publish complete accepted build scopes at `main`, `dev-cad`,
  `dev-ci` using released build-store CLI, preserving siblings.
- Publish stable Pages root and development subtrees using released Pages
  CLI, with source SHA/provenance checks and no force-push.
- Site generator consumes exact prepared complete scope without executing CAD.
  Reuse the existing CAD website layout/style/source presentation; do not swap
  in Forge's website generator or redesign the model page.
- Generate a site candidate and compare it with the accepted stable CAD site
  for navigation, page structure, model images, source, command sequence,
  downloads, URLs and verification labels before changing stable Pages.
- Ensure a docs-only Pages update is fast and cannot invalidate native CAD.

### M5 — End-to-end qualification and cutover

Status: **not started**.

- Run one selected model, one cross-model dependency, SCPC comparison,
  the full 16-item/18-variant model set, and all required native checks.
- Prove a Forge/SolidCraft pin change invalidates every affected native
  model; validate every model's saved `.sc`, STEP, measurements and
  screenshots, not just the page update or command compilation.
- Complete #172 using real result evidence; no relabeling old outputs.
- Test independent build/Pages publication on both dev lanes and on main.
- Verify existing `/models/<slug>/` links and category URLs; visually compare
  homepage/category/model examples on desktop and narrow screens. Reject a
  visible website regression even if the CI/build checks are green.
- Retire obsolete CAD selectors, wrapped generic execution and publisher
  only after acceptance; update tests, AGENTS and documentation to the
  new active architecture.
- Merge the migration into `main` only after source and generated scopes
  have been checked. Close #174 only at completion.

## Git workflow and release discipline

While the lane topology is being introduced, documentation-only changes can
use a short-lived PR to `main` with **squash**. After lanes exist, CI work
targets `dev-ci` and CAD model work targets `dev-cad`. Promotions use
normal merge commits by the owner-controlled policy. Avoid many tiny commits;
finish logical changes as one reviewed PR with tested output.

The exact Forge/central Docker versions already exist. This migration does
not create another Forge release or rebuild the Docker image.
