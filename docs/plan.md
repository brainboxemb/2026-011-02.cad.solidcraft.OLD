# CAD repository plan

This file is the current source of truth for unfinished work in
`2026-011-02.cad.solidcraft`.

This repository owns product/project CAD models, model-specific expectations,
variants, dependencies and the published CAD catalog. Forge owns reusable CAD
API/compiler behaviour; generic CAD-CI belongs in `lib.py.cad.ci` /
`tool.cad.ci`; generic verification belongs in
`lib.py.cad.verification`; runtime packaging belongs in
`docker.cad.solidcraft`.

## Current repository state

Permanent source lanes:

```text
main
dev-cad
dev-ci
```

Current heads at this reconciliation:

- `main`: `c3d46976c8810487b74a802faf1009cb8608e4b0`;
- `dev-cad`: `b69e8170576a911581c4d8d58806ba92f1ac0b57`;
- `dev-ci`: `c3d46976c8810487b74a802faf1009cb8608e4b0`.

Stable `main` and `dev-ci` now include the accepted #344/#350 model-detail
presentation: long model parameter prose is normal **Key dimensions** text,
not a status badge. Stable run #45199498406 and dev-ci run #45199501975 are
green on the exact shared head.

Development lanes are working/integration lanes. Multiple accepted logical
changes may accumulate there. Do **not** promote to `main` after every green
feature PR. Promote only at a deliberate stable checkpoint such as a coherent
feature batch, end of work block/day, release point, or genuine cross-lane
dependency.

Pure repository-instruction/documentation corrections in `AGENTS.md` and
`docs/*` may go directly to `main` when independent of unmerged code/model
work. Documentation belonging to a code/model change stays with that issue,
branch and PR.

Current CAD runtime baseline is SolidCraft 0.45.0. The CAD repository still
consumes released Forge v0.11.0; several newer Forge fixes exist upstream but
are not yet available through a released CAD-consumable baseline.

## Current work order

### 1. Finish current FlexBenchDog visual acceptance

Primary lane: `dev-cad`.

- #332 is complete: the durable render after PR #347 visibly matches the open
  BrainBox wireframe cube. The current one-Slot-per-Sketch implementation is
  temporary only at the construction/API level; cleanup remains #348 / Forge
  #747 and must preserve the accepted visible geometry.
- #333 is complete: PR #338 supplied the R0.5 four-edge fillet and PRs
  #361/#368/#372 added, corrected and zoomed the model-owned underside view.
  Durable run #433 made the four equal rounded material-side corners clearly
  inspectable and they were visually accepted.
- #385 is complete: PR #386 removed the unintended primary-camera override
  introduced with the underside view. The primary FlexBenchDog preview again
  uses the shared/default camera while `underside.png` keeps its dedicated
  review camera. Durable dev-cad run #45196422598 is green at
  `b69e8170576a911581c4d8d58806ba92f1ac0b57`.
- #327 / draft PR #328: full-length native Cone taper remains blocked on Forge
  #746. Do not emulate Cone locally.

### 2. Keep temporary capability workarounds explicit

- #348 -> Forge #747: the FlexBenchDog one-Slot-per-Sketch logo construction is
  temporary until attached/explicit Sketch `Polygon2D` lowering is released.
  Both SCPF and SCPC sources carry explicit TEMPORARY comments.
- #362 -> Forge #750: the final CornerBracket arm-tip triangular wedge needs a
  reusable locally rotated standalone cutter. PR #363 adds explicit TEMPORARY
  comments to SCPF and SCPC; no geometry change.
- #8: PR #360 restored the preserved 11-point arm profile and exact four-part
  recessed M5 fixing seats. The remaining arm-tip wedge is exactly the #362 /
  Forge #750 blocker.

Do not add CAD-local compiler, transform or command workarounds for these
generic Forge gaps.

### 3. HUB75 iteration 2 refresh

- #154 is represented by current draft PR #349; old PR #156 is closed as
  superseded.
- The refreshed root is `models/advanced/hub75_wood_frame_iter2/` and keeps
  only current product-CAD geometry plus current `model.yml` / `ci.yml`
  ownership.
- Native processing stays disabled until the required Forge naming fix from
  #679 reaches a released CAD-consumable Forge version.
- Full repository execution also exposed Forge #749: `run_script()` must
  isolate project-local Python modules between independent model roots.
- No CAD-local `sys.modules` cleanup is allowed.
- Keep PR #349 draft until both generic blockers are released/adopted and the
  normal native build plus saved-design lower-compartment mutation pass.

### 4. STL publication

- #345 is blocked on Forge #748.
- Required final CAD behaviour remains: publish `model.stl` beside `.sc`,
  STEP and preview; expose STL as the practical mesh/view artifact; link the
  exact durable `build/<scope>/.../native/model.stl` so GitHub's STL viewer
  can be used.
- Do not add a CAD-local STEP-to-STL conversion. Forge/runtime must first
  qualify STL export from the accepted SolidCraft result.

### 5. Site lane

- #344 is complete and promoted to stable `main`: long model parameter prose
  is no longer a status badge; it is rendered as readable **Key dimensions**
  under the model description. #383 synchronized `main -> dev-ci`, restored
  the accepted documentation, and promoted exact `dev-ci -> main` through the
  permanent-lane merge policy.
- #278 is closed: the accepted EXP-derived model-detail hierarchy has been
  ported and accepted.
- Keep #288 as a separate CAD-CI consumer migration; do not mix it into model
  presentation work.
- #20 and #21 remain later product/site work. The current generic
  `extra_views` / `EXTRA_SNAPSHOTS` mechanism already proves model-owned
  multiple views, but #20's broader gallery contract is not yet complete.

## Blocked HUB75/native follow-ups

The current `hub75-wood-frame` root is still `process: false` while the
closed Forge #679 fix is absent from the released CAD-consumed Forge baseline.
Therefore do not claim native saved-design acceptance for:

- #91 frame-thickness mutation moving all eight CornerBrackets;
- #77 CornerBracket placement/associativity under dimension changes;
- #142 HUB75Display2 native qualification;
- the remaining full-catalog acceptance in #172.

These become actionable after a Forge release/adoption that contains the
required naming fix and any other applicable runner fixes.

## Other open work

| Issue | Owner/lane | Status | Next action |
| --- | --- | --- | --- |
| #8 CornerBracket exact geometry | dev-cad + Forge | **blocked on #362 / Forge #750** | Preserve PR #360 geometry; add final rotated wedge only after generic transform support is released. |
| #362 CornerBracket arm-tip wedge | dev-cad + Forge | **blocked on Forge #750** | PR #363 is merged; temporary markers are in both model sources. Geometry waits for released transform support. |
| #154 HUB75 lower compartment | dev-cad + Forge | **blocked / draft PR #349** | Wait for released #679 fix and Forge #749, then enable native processing and mutation acceptance. |
| #345 STL output + GitHub viewer | dev-ci/dev-cad + Forge | **blocked on Forge #748** | Adopt qualified STL export after upstream release; no STEP conversion workaround. |
| #348 FlexBenchDog logo cleanup | dev-cad + Forge | **blocked on Forge #747** | Replace temporary per-rib Slot Sketches after released Polygon2D attached-Sketch support. |

| #327 FlexBenchDog Cone taper | dev-cad + Forge | **blocked on Forge #746** | Resume draft PR #328 only after native Cone support is released/adopted. |
| #288 CAD-CI workflow/config migration | dev-ci / tool.cad.ci | **later / separate** | Reassess against the current released tool.cad.ci owner baseline before implementation. |
| #205 canonical model.yml contract | Forge release + dev-cad | **blocked on Forge release** | Forge PR #711 already provides reusable `scpf.model_metadata`; adopt it only after a qualified post-v0.11 Forge release, then move CAD-only fields to their owning layers. |
| #172 full-catalog native qualification | dev-cad + Forge | **blocked** | Re-enable remaining disabled roots after required Forge fixes reach the CAD baseline. |
| #142 HUB75Display2 | dev-cad + Forge | **blocked on released #679 fix** | Resume native qualification after Forge adoption. |
| #135 Bolted Flange circular pattern | dev-cad + Forge | **blocked on Forge #347** | Keep PR #141 parked until the intended applied-feature seed is supported. |
| #91 frame-thickness native regression | dev-cad + Forge | **blocked on released #679 fix** | Run current native saved-design mutation once hub75-wood-frame is processable. |
| #77 CornerBracket placement/associativity | dev-cad + Forge | **blocked on released #679 fix** | Validate eight bracket occurrences only on a processable current HUB75 root. |
| #21 interactive SolidCraft viewer | site/product | **later** | Revisit after current model/output contracts stabilize. |
| #20 multiple verified model views | site/product | **later / partially enabled** | Build on generic extra_views; broader responsive gallery contract remains open. |
| #365 HUB75 glazing retention/seal | dev-cad | **next design slice** | Define the physical glazing stack, contact/clearance, retention and sealing before modelling guessed hardware. |
| #371 Detailed HUB75 panel completion | tracking | **tracking only** | Reusable-panel work is split into #373 rear-frame contour, #374 mounting interfaces and #375 connector envelopes. |
| #373 HUB75 rear-frame bay contours | dev-cad + Forge | **blocked if clean Polygon2D is required** | Restore R5/stepped bay contours; do not use overlapping-profile workarounds instead of Forge #747. |
| #374 HUB75 mounting tubes/bushings/locator pins | dev-cad + Forge/SolidCraft | **standalone merged / assembly acceptance blocked on #388** | PR #376 is merged and the standalone detailed panel remains valid. Do not close final visual acceptance while the five-panel assembly leaves component-local Cylinder features detached. |
| #375 HUB75 connector envelopes | dev-cad | **implemented / draft PR #390 green; blocked on #388 before merge** | The two measured IDC envelopes and explicitly approximate power envelope build successfully in the standalone reusable panel on the released stack. Keep PR #390 draft until reusable-component assembly output is clean. |
| #388 HUB75 component-local Cylinder placement regression | dev-cad + Forge/SolidCraft | **blocked on owner-layer qualification** | Five panel bodies are placed correctly, but the 14 native Cylinder join features can appear detached. Forge #753 / draft PR #754 owns the minimal rotated-component reproducer. SolidCraft 0.45 issue #21098 / PR #21145 is the primary runtime hypothesis, not yet proven or released. |
| #382 Stable-to-dev-cad synchronization / CAD checkpoint | repository governance | **next: main -> dev-cad only; reverse promotion paused** | Bring the now-stable #344 site fix into dev-cad through an exact history-preserving merge, then require durable dev-cad green. Do not promote dev-cad back to main while #388 remains open. |
| #366 HUB75 rear/electrical interfaces | dev-cad | **blocked on reusable panel children** | After #371 children are accepted, model only enclosure-side clearance/access/cable consequences; do not duplicate panel dimensions. |
| #367 HUB75 exploded view | dev-cad + Forge | **blocked on Forge #751** | SolidCraft 0.45 has native `explode.create/show`; Forge #751 owns the reusable wrapper/qualification, then CAD publishes through generic extra views. |
| #7 complete HUB75 screen assembly | tracking | **tracking only** | Remaining work is split across #8/#77/#91/#365/#366/#367 plus #20/#21; do not create one broad #7 implementation PR. |

## Completed / retired in this batch

- #344 complete and stable: compact model-detail facts are on synchronized
  `main` / `dev-ci` at `c3d46976c8810487b74a802faf1009cb8608e4b0`.
- #385 complete: FlexBenchDog primary preview camera restored without changing
  the dedicated underside review camera.
- #278 closed: accepted model-detail presentation baseline.
- #34 closed: SCPC/SCPF repository split and representative parallel-model
  architecture are complete; future SCPC coverage is model-specific work.
- #14 closed as superseded: released CAD-CI/SCons selection now owns affected
  model selection; do not revive CAD-local Moon/GitHub-cache architecture.
- #250 complete: root `CHANGELOG.md` follows the shared template without inventing historical releases; the repository currently has no tags or GitHub Releases.
- #168 complete: active operator-facing documentation now uses explicit SolidCraft build/verification terminology; the site already enforced `Build and verification` / `SolidCraft verified` labels.
- #206 and #204 were already completed before this reconciliation.
- PR #156 is closed and superseded by #349.

## Parked pull requests

- PR #349 — draft HUB75 iteration-2 refresh; blocked as documented above.
- PR #328 — draft FlexBenchDog native Cone taper; blocked on Forge #746.
- PR #169 — draft latch design; keep parked until its required Forge API
  baseline is available.
- PR #141 — Bolted Flange circular pattern; blocked on Forge #347.

## Next checkpoint

1. complete #383 baseline reconciliation, then synchronize exact stable
   `main -> dev-cad` under #382 so the accepted Key-dimensions presentation is
   also visible on the dev-cad Pages scope;
2. verify the synchronized dev-cad durable build/Pages scope remains green and
   retains the restored FlexBenchDog primary camera;
3. resolve #388 through Forge #753 / the applicable SolidCraft owner fix; do not
   add a CAD-local primitive/placement workaround;
4. only after #388 is qualified, finish #374 assembly visual acceptance and
   merge the already-green draft #390 / #375 connector slice;
5. keep #365 as a design-decision slice and keep
   #154/#327/#345/#348/#362/#367 parked until their owner-layer Forge
   capabilities are released and adopted;
6. do not promote `dev-cad -> main` under #382 while #388 remains open.
