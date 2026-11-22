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

### Owner decision before more model migration

**Forge issue #661 is the entry point** for the shared scan/plan/batch
requirements and any generic `lib.py.cad.ci` / `tool.cad.ci`
enhancements. Do not implement these requests directly in those repositories
from the CAD consumer, and do not build a second CAD-specific scheduler.
Forge owns acceptance; the appropriate library/tool makes its own released
implementation and Forge qualifies that version. Only then adopt it here.

## Ownership and registration correction — now

Forge is the central reusable CAD library, not the owner of generic CI architecture.

- Forge owns the reusable CAD API, compiler/lowering, modelling semantics and Forge-owned examples/expectations.
- `lib.py.cad.ci` / `tool.cad.ci` own generic CAD-CI discovery, selection, execution and durable build/publication mechanics.
- `lib.py.cad.verification` owns generic CAD/model verification mechanics.
- `docker.cad.solidcraft` owns the immutable SolidCraft runtime.
- This product CAD repository owns its product models, model variants, model-to-model dependencies, presentation metadata and product catalog.
- `scripts/ci/model_catalog.py` may remain the single product-model registration source for the CAD site/domain, but it must not become a second generic CI planner or be required by generic CAD-CI item discovery.
- Distributed model-root `ci.yml` items are the generic CI participation boundary. Generic discovery/selection must not depend on Forge or on a central product catalog.
- A product model that exposes missing reusable CAD modelling capability raises a Forge CAD-library requirement; a product-model registration change remains local to this repository.

Forge #661 is therefore only a Forge consumer/selectivity validation. It is not a governance gate for generic CAD-CI and must not block unrelated model onboarding when the released stack already satisfies this repository's requirements.

### Open issue assessment — 2026-11-22

| Issue | Status | Current interpretation |
| --- | --- | --- |
| #174 CAD-CI/publication migration | **now** | Continue the staged migration; also remove stale wording that makes Forge the generic CI governor. |
| #172 full-catalog Forge 0.11 / SolidCraft 0.45 verification | **blocked** | Complete after the remaining model roots are on the shared build path and the full-run gate exists. |
| #168 verification terminology | **later** | Coordinate with Forge #659 after the active architecture/ownership correction. |
| #155 tool.cad.ci v0.2.0 migration | **probably obsolete** | Superseded by #174 and much newer released tool/lib versions; preserve useful history, then close or rewrite residual scope. |
| #154 lower storage compartment | **now** | Independent CAD work; active PR #156 belongs on `dev-cad`, not directly on `main`. |
| #142 HUB75Display2 parallel model | **effectively complete but still open** | Model/catalog structure exists; final current-runtime/full-catalog evidence is covered by #174/#172. |
| #135 bolted-flange circular pattern | **blocked** | Explicitly blocked by Forge CAD-library issue #347. |
| #91 frame wood-thickness regression | **later** | Resume with the relevant frame model verification work. |
| #77 CornerBracket placement/associativity | **later** | Keep as focused model-quality work; not a CI architecture gate. |
| #34 SCPC alongside SCPF | **effectively complete but still open** | SCPC library and multiple independent comparisons exist; reconcile remaining acceptance after #174 migration. |
| #21 interactive SolidCraft viewer | **later** | Presentation feature, independent of current migration. |
| #20 multiple verified image views | **later** | Presentation/verification enhancement after stable publication cut-over. |
| #14 incremental builds / Moon evaluation | **probably obsolete** | Released CAD-CI now owns changed/dependency selection, caching and build-store semantics; do not introduce Moon or a second planner. |
| #8 CornerBracket exact geometry | **later** | CAD geometry refinement, independent of CI migration. |
| #7 HUB75 screen completion | **later** | Product-model roadmap item, independent of generic CI ownership. |

## Architecture correction — shared build-batch accepted for nine models

**PR #184 passed and was squash-merged into `dev-ci` on 2026-11-22.**
The resulting source SHA is
`670960db48c80317a37f72bc1ea0a62a09595090`.

The existing Forge batch/copy design was applied as follows:
- Reuse the accepted Forge `model-verification-batch` / `copy: dependency`
  architecture with one SolidCraft runtime launch for the batch.
- Discover model roots through generic globs; each of the 16 model
  `ci.yml` files has only id/template/process. Keep the 7 not yet built by
  the new route `process: false`.
- Build the existing nine accepted model roots as the first batch and retain
  separate model files, STEP, images, checks and independent SCPC comparisons.
- Use the released Forge-accepted `tool.cad.ci 0.17.1` /
  `lib.py.cad.ci 0.10.0` stack with `copy: dependency`.
- Regular development PRs use selective CAD-CI planning. The batch may
  still rebuild all `process: true` models if any batch input changes; this
  is an existing Forge trade-off and its selectivity is tracked by Forge #661.
- Do not change stable `main`, generated publication or the CAD website.

**Proof:** 13/13 SCons targets succeeded; 9/9 SolidCraft models passed
their checks, including the 4 independent Forge/SCPC comparisons.
The shared batch used exactly one Docker run, total 29.843 seconds
(including 8.791 seconds image pull), and CAD-CI copied each model's
build results through the released `copy: dependency` feature.

**Still open:** docs-only/no-model selective run, detailed checks that were
deferred in the nine-model proof, remaining 7 roots/2 additional variants,
full catalog acceptance (#172), independent development build/Pages scopes
and site comparison. The public CAD website and `main` remain unchanged.
A compact new-chat handoff is available at `docs/handoff.md`.

## Next component batch — accepted on dev-ci

**PR #186 is groen getest en met squash gemerged** als
`75ea0fb6db0459872255b7f51e9ae506b9ed7f4c`.

- Enabled the reusable `flex-bench-dog` and `guide-rail` model roots in
  the **existing shared SolidCraft build batch**, not separate jobs.
- GuideRail owns Festool/Makita as two catalog variants with their own
  measured envelopes and volumes, but only one three-line `ci.yml`.
- FlexBenchDog retains a second independent SCPC implementation.
- **Verified:** 11 physical roots / 12 variants built and checked with
  exactly one Docker run, including both GuideRail variants and
  FlexBenchDog's independent SCPC comparison. 15/15 SCons targets passed;
  the shared batch total was 31.760 seconds, of which 7.434 seconds
  came from pulling the image.
- The remaining five roots stay disabled until separately checked.
- Docs-only PR #185 demonstrated **zero selected CAD targets**; no model
  build, Docker pull or SolidCraft runtime startup occurred.
- No change to the public CAD website or the accepted `main` pipeline.

## Previous architecture review — obsolete per-model execution

**Historical reason for #184 (resolved for nine active model roots):**
The preceding prototype started Docker separately for each model, forced
a complete run on every development PR and had a manually growing list.
PR #184 replaced those mechanisms with one shared batch, model globs and
the released `copy:` feature. Do not reintroduce the old behavior.

Before further model onboarding:

1. Use Forge's released `tool.cad.ci` scan/plan/SCons approach without a
   second CAD-specific planner.
2. Replace per-model Docker starts with one shared model-build batch,
   including the existing independent SCPC comparisons, and expose results
   through released `copy: dependency` semantics.
3. Replace the hand-maintained selected-model list by category globs
   and `process` settings; prevent unused old `ci.yml` steps from
   accidentally becoming active during staged transition.
4. Make normal dev-PR runs selective; retain full builds for deliberate
   promotion and Forge/SolidCraft upgrade checks.
5. Demonstrate two-model change, no-op change, full-catalog trigger,
   independent geometry check, and one runtime startup per batch. Record
   timing and actual model result files.
6. Keep the existing CAD website/publication untouched until complete
   source, result, route and page comparison passes.

The unmerged `ci/174-component-models-batch` is **not** a completed
migration step. No further model onboarding should be merged on the old
per-model runner. Refer to issue #174 for the detailed audit.

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

Status: **nine model roots pass the shared build-batch, seven remain disabled;
detailed check parity and website/build publication remain outstanding**.
PR #178 at `a4329d0791803572184b8ebf163adea737f7a372`
passed a real Plate build with released tool.cad.ci 0.17.0 /
lib.py.cad.ci 0.9.3, verification 0.15.0, Forge 0.11.0 and central
SolidCraft 0.45.0. The next stage uses one model-independent producer, adds Vent Plate,
and compares separate Forge/SCPC SolidCraft results. SCPC is prepared
once as a shared dependency to prevent simultaneous checkout conflicts;
all other roots remain outside the staged graph until checked. This is not full-catalog acceptance.

- Reuse Forge's accepted released
  `tool.cad.ci 0.17.1` / `lib.py.cad.ci 0.10.0` stack (accepted for
  shared `copy:` output).
- Add the released CAD verification package as an **external** separately
  pinned dependency; never add it to the central Docker.
- Align `cad-ci.yml` runtime variables, templates, item discovery,
  `process`, watches, dependencies and output contracts with Forge.
- Test that every current model variant is accounted for and that a single
  source change selects only its declared affected items.
- SCons/released library must be the only owners of selection/reuse.

### M2 — Native verification and consumer step migration

Status: **nine model roots pass one SolidCraft build batch; remaining
seven physical model roots still require migration and checks**.
The Plate model was built successfully by released CAD-CI. The next
stage converts Plate and Vent Plate to one model-independent producer, builds
and checks Forge and independent SCPC SolidCraft models and checks that their body
bounds and volume agree. Other model roots remain on the old main pipeline.

- Convert one representative basic model to model-local declarative
  verification and released `lib.py.cad.verification`, including native
  SolidCraft output and accurate provenance.
- Cover a model with independent SCPC output and a complex assembly.
- Only after the shared-batch architecture gate is green, convert the
  remaining model roots in reviewable groups, preserving
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
