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

- `main`: `6be947fd47333389513e64a73ae19649eb80796a`;
- `dev-cad`: `75d8fb377e37766fc59fcf1abaa7cc18bfec1069`;
- `dev-ci`: `c3d46976c8810487b74a802faf1009cb8608e4b0`.

Stable `main` includes the accepted #344/#350 model-detail presentation and
`dev-cad` now carries that stable baseline through exact history-preserving
merge `200c902f976ff6809692cc344379bbdc10dcbd13`. Durable dev-cad run
#45202180938 is green; both `build/dev-cad` and `/dev-cad/` Pages source-match
that exact merge. The long model parameter prose is normal **Key dimensions**
text rather than a status badge, and the #385 FlexBenchDog primary-camera fix
remains intact. `dev-ci` retains the same accepted site implementation at its
last synchronized stable head.

Development lanes are working/integration lanes. Multiple accepted logical
changes may accumulate there. Do **not** promote to `main` after every green
feature PR. Promote only at a deliberate stable checkpoint such as a coherent
feature batch, end of work block/day, release point, or genuine cross-lane
dependency.

Pure repository-instruction/documentation corrections in `AGENTS.md` and
`docs/*` may go directly to `main` when independent of unmerged code/model
work. Documentation belonging to a code/model change stays with that issue,
branch and PR.

Current CAD runtime baseline is SolidCraft 0.45.0 and stable `dev-cad` still
consumes released Forge v0.11.0. Forge v0.13.1 is published at exact commit
`17a4e1d0e2edf0124d40daf5425891fdf65c24be`; CAD #405 is the focused
baseline-adoption issue. Its first validation exposed Forge #796 in the existing
detailed `hub75-panel` root. CAD #407 therefore temporarily disables only that
root before #405 is refreshed. No panel geometry changes. Once #405 is accepted,
Forge #679/#703/#746/#747/#749/#750 become CAD-consumable while #796 continues
upstream independently.

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
- #327 / draft PR #328: Forge #746 is released in v0.13.1. Keep the draft
  parked only until #405 adopts that baseline, then refresh it and complete the
  intended full-length native Cone taper.

### 2. Keep temporary capability workarounds explicit

- #348 -> Forge #747: attached/explicit Sketch `Polygon2D` lowering is
  released in v0.13.1. Preserve the temporary construction until #405 adopts
  the baseline, then replace it in its own focused slice without changing the
  accepted visible logo.
- #362 -> Forge #750: locally rotated standalone Sketch cutters are released in
  v0.13.1. After #405, resume the final CornerBracket arm-tip triangular wedge
  and remove the TEMPORARY markers only with the completed geometry.
- #8: PR #360 restored the preserved 11-point arm profile and exact four-part
  recessed M5 fixing seats. Its remaining arm-tip wedge is actionable through
  #362 after #405.

Do not add CAD-local compiler, transform or command workarounds for these
generic Forge gaps.

### 3. HUB75 iteration 2 refresh

- #154 is represented by current draft PR #349; old PR #156 is closed as
  superseded.
- The refreshed root is `models/advanced/hub75_wood_frame_iter2/` and keeps
  only current product-CAD geometry plus current `model.yml` / `ci.yml`
  ownership.
- Forge #679 naming and #749 model-local import isolation are both released in
  v0.13.1. Keep PR #349 draft until #405 adopts that baseline; no CAD-local
  `sys.modules` cleanup is allowed.
- After #405, refresh PR #349 on current `dev-cad`, enable its intended native
  processing and require the normal build plus saved-design lower-compartment
  mutation before making it ready.

### 4. STL publication

- #345 established direct saved-design STL export through the pinned
  SolidCraft 0.45.0 CLI; #403 narrows that output to an explicit model-root
  request instead of exporting every processed model.
- Model roots request STL in execution config with:
  `artifacts: [stl]`. The default is no STL.
- FlexBenchDog currently requests STL. Models such as Plate keep `.sc`, STEP
  and preview output without an STL mesh.
- The site remains evidence-driven: STL download and GitHub viewer links appear
  only when the durable build scope actually contains `model.stl`.
- STEP remains the interchange CAD export. There is no STEP-to-STL conversion
  and Forge #748 is not required for this output path.

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

## Forge-adoption follow-ups

The current `hub75-wood-frame` root remains `process: false` on the stable
v0.11 baseline. Forge #679 is released in v0.13.1, so after #407 and #405 the
root can be re-enabled under #378 without a CAD-local workaround. Then proceed
with:

- #91 frame-thickness mutation moving all eight CornerBrackets;
- #77 CornerBracket placement/associativity under dimension changes;
- #142 HUB75Display2 native qualification;
- the independent portions of #172 full-catalog qualification.

CAD #407 temporarily adds `hub75-panel` to the disabled set because Forge #796
breaks its symbolic Cylinder anchor arithmetic on v0.13.1. That temporary gate
does not block unrelated models or the v0.13.1 capabilities needed by
#154/#327/#348/#362. Final all-roots #172 acceptance still requires #796 to be
fixed, released and the panel root re-enabled.

## Other open work

| Issue | Owner/lane | Status | Next action |
| --- | --- | --- | --- |
| #407 temporary hub75-panel gate | dev-cad + Forge | **now / Forge #796** | Disable only `hub75-panel` before #405; re-enable immediately after a released Forge #796 fix is adopted. |
| #405 Forge v0.13.1 adoption | dev-cad | **next after #407** | Refresh from the new dev-cad head, adopt exact v0.13.1, and require normal PR validation with the temporary panel gate in place. |
| #8 CornerBracket exact geometry | dev-cad + Forge | **after #405 via #362** | Preserve PR #360 geometry; add the final rotated wedge with released Forge #750 support. |
| #362 CornerBracket arm-tip wedge | dev-cad | **after #405** | Implement the final rotated wedge and remove the temporary markers with the completed geometry. |
| #154 HUB75 lower compartment | dev-cad | **after #405 / draft PR #349** | Refresh on current dev-cad, enable native processing and complete the saved-design lower-compartment mutation acceptance. |
| #345 STL output + GitHub viewer | dev-cad / SolidCraft runtime | **complete / PR #401** | Accepted on durable dev-cad run #45211961040. |
| #348 FlexBenchDog logo cleanup | dev-cad | **after #405** | Replace temporary per-rib Slot Sketches with released Polygon2D attached-Sketch support while preserving accepted geometry. |
| #327 FlexBenchDog Cone taper | dev-cad | **after #405 / draft PR #328** | Refresh on current dev-cad and implement the intended full-length native Cone taper. |
| #288 CAD-CI workflow/config migration | dev-ci / tool.cad.ci | **later / separate** | Reassess against the current released tool.cad.ci owner baseline before implementation. |
| #205 canonical model.yml contract | dev-cad | **after #405 / separate migration** | Forge #703 is released in v0.13.1; migrate CAD-only fields to their owning layers separately. |
| #172 full-catalog native qualification | dev-cad + Forge | **partially after #405; final blocked on #796** | Qualify independent roots first; final all-roots acceptance waits for `hub75-panel` to be restored. |
| #142 HUB75Display2 | dev-cad | **after #378** | Resume native qualification after the existing wooden HUB75 root is re-enabled and green. |
| #135 Bolted Flange circular pattern | dev-cad + Forge | **blocked on Forge #347** | Keep PR #141 parked until the intended applied-feature seed is supported. |
| #91 frame-thickness native regression | dev-cad | **after #378** | Run the saved-design mutation on the re-enabled wooden HUB75 root. |
| #77 CornerBracket placement/associativity | dev-cad | **after #378** | Validate all eight bracket occurrences on the re-enabled current HUB75 root. |
| #21 interactive SolidCraft viewer | site/product | **later** | Revisit after current model/output contracts stabilize. |
| #20 multiple verified model views | site/product | **later / partially enabled** | Build on generic extra_views; broader responsive gallery contract remains open. |
| #365 HUB75 glazing retention/seal | dev-cad | **later design slice** | Do not model guessed hardware; revisit only when the physical glazing stack is intentionally defined. |
| #371 Detailed HUB75 panel completion | tracking | **tracking only** | Reusable-panel work is split into #373/#374/#375. |
| #373 HUB75 rear-frame bay contours | dev-cad + Forge | **implementation after #405; native acceptance blocked on #796** | Use released Polygon2D support; do not claim native root acceptance while the panel is temporarily gated. |
| #374 HUB75 mounting tubes/bushings/locator pins | dev-cad + Forge/SolidCraft | **standalone merged / assembly acceptance blocked on #388; root gated by #796** | Keep accepted geometry; no local workaround for #796 or #388. |
| #375 HUB75 connector envelopes | dev-cad | **implemented / draft PR #390; blocked on #388 before merge** | Keep PR #390 draft until reusable-component assembly output is clean. |
| #388 HUB75 component-local Cylinder placement regression | dev-cad + Forge/SolidCraft | **blocked on owner-layer qualification** | Forge #753 / draft PR #754 owns the reusable reproducer; no CAD-local workaround. |
| #382 Stable-to-dev-cad synchronization / CAD checkpoint | repository governance | **Phase A complete; Phase B blocked on #388** | Do not promote `dev-cad -> main` while #388 remains open. |
| #366 HUB75 rear/electrical interfaces | dev-cad | **blocked on reusable panel children** | After #371 children are accepted, model only enclosure-side clearance/access/cable consequences. |
| #367 HUB75 exploded view | dev-cad + Forge | **blocked on Forge #751** | Resume only after the reusable exploded-view wrapper is released. |
| #7 complete HUB75 screen assembly | tracking | **tracking only** | Continue through focused child issues; do not create one broad implementation PR. |

## Completed / retired in this batch

- #344 complete and stable: compact model-detail facts are promoted on `main`
  and synchronized into `dev-cad` through #382 Phase A.
- #385 complete: FlexBenchDog primary preview camera restored without changing
  the dedicated underside review camera.
- #345 complete: PR #401 publishes direct SolidCraft STL output and a
  scope-matched durable GitHub STL viewer link without a Forge dependency.
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

1. merge #407 so only `hub75-panel` is temporarily gated for Forge #796;
2. refresh #405 from the resulting `dev-cad` head, adopt exact Forge v0.13.1
   and require normal PR validation to be green;
3. after #405, re-enable the existing `hub75-wood-frame` under #378 and require
   a real native build plus source-matched dev-cad output;
4. resume #154 / draft PR #349, then #327/#348/#362 as independent focused
   model slices;
5. continue #77/#91 and then #142; progress independent portions of #172 while
   final all-roots qualification waits for Forge #796;
6. fix #796 upstream in parallel and re-enable `hub75-panel` immediately after
   a released Forge fix is adopted;
7. keep #388 on its Forge #753/SolidCraft owner path. It still blocks final
   #374 assembly acceptance, PR #390/#375 and `dev-cad -> main`, but it does
   not block the unrelated model work above.
