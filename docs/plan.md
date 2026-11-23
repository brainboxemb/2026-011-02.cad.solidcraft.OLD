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

Current CAD runtime baseline is SolidCraft 0.45.0. CAD #405 is adopting
released Forge v0.13.1 at exact commit
`17a4e1d0e2edf0124d40daf5425891fdf65c24be`, which contains #679, #703,
#746, #747, #749 and #750. Adoption run #45263158238 exposed Forge #796 in
the existing detailed `hub75-panel`. CAD #407 therefore temporarily marks only
that model root `process: false`; its geometry stays unchanged and the gate is
removed after a released Forge fix is adopted. This temporary model gate does
not block accepting v0.13.1 for the other CAD roots. Forge #753 / CAD #388 is
separate and remains an owner-layer blocker.

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
- #327 / draft PR #328: Forge #746 is released in v0.13.1. Resume the
  full-length native Cone taper after #405 accepts the baseline; Forge #796 is
  isolated to the temporarily disabled `hub75-panel` root through #407.

### 2. Keep temporary capability workarounds explicit

- #348 -> Forge #747: attached/explicit Sketch `Polygon2D` lowering exists in v0.13.1, but the
  repository cannot adopt that baseline until #405 / Forge #796 is resolved.
  Keep the temporary construction until the patched release is accepted.
- #362 -> Forge #750: locally rotated standalone Sketch cutters exist in v0.13.1, but CAD adoption
  is blocked by #405 / Forge #796. Keep the TEMPORARY markers until the patched
  release is accepted, then resume the final arm-tip wedge.
- #8: PR #360 restored the preserved 11-point arm profile and exact four-part
  recessed M5 fixing seats. The remaining arm-tip wedge becomes actionable through #362 after #405.

Do not add CAD-local compiler, transform or command workarounds for these
generic Forge gaps.

### 3. HUB75 iteration 2 refresh

- #154 is represented by current draft PR #349; old PR #156 is closed as
  superseded.
- The refreshed root is `models/advanced/hub75_wood_frame_iter2/` and keeps
  only current product-CAD geometry plus current `model.yml` / `ci.yml`
  ownership.
- Forge #679 naming and #749 model-local import isolation are present in
  v0.13.1, but CAD #405 cannot yet accept that release because of Forge #796.
  Keep PR #349 draft; no CAD-local `sys.modules` or primitive workaround is
  allowed.
- After a patched Forge release is accepted, refresh #154 / PR #349 on the
  current lane and require the normal native build plus saved-design
  lower-compartment mutation before marking it ready.

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

## Released capability follow-ups awaiting accepted Forge adoption

Forge v0.13.1 contains the previously missing #679 naming fix and #749
model-local import isolation, but candidate adoption failed on Forge #796.
Therefore do **not** re-enable `hub75-wood-frame` yet. After #796 is fixed,
released and #405 is green, #378 becomes the first model-specific follow-up.
After that native root is green, the current saved-design placement/mutation
work can proceed:

- #91 frame-thickness mutation moving all eight CornerBrackets;
- #77 CornerBracket placement/associativity under dimension changes;
- #142 HUB75Display2 native qualification;
- the remaining full-catalog acceptance in #172.

Forge v0.13.1 also contains #746/#747/#750. Those capabilities will unblock
#327, #348, #362 and the clean Polygon2D path for #373 after a patched Forge
release containing them and #796 is accepted under #405. These are independent
of #388.

CAD #388 remains blocked on Forge #753 / applicable SolidCraft component-local
Cylinder ownership. It continues to block final five-panel assembly acceptance,
PR #390 / #375 and the reverse `dev-cad -> main` checkpoint, but it must not
freeze unrelated model work.

## Other open work

| Issue | Owner/lane | Status | Next action |
| --- | --- | --- | --- |
| #407 temporary hub75-panel gate | dev-cad + Forge | **temporary / Forge #796** | Keep only `hub75-panel` disabled while #796 is unresolved; re-enable immediately after a released Forge fix is adopted. |
| #8 CornerBracket exact geometry | dev-cad + Forge | **actionable via #362 after #405** | Preserve PR #360 geometry; add the final rotated wedge using released Forge v0.13.1 support. |
| #362 CornerBracket arm-tip wedge | dev-cad | **unblocked by Forge v0.13.1 after #405** | Implement the final rotated wedge in a focused branch/PR and remove the temporary markers with the completed geometry. |
| #154 HUB75 lower compartment | dev-cad | **resume draft PR #349 after #405** | Refresh on the accepted v0.13.1 baseline, enable the intended native processing and complete the saved-design lower-compartment mutation acceptance. |
| #345 STL output + GitHub viewer | dev-cad / SolidCraft runtime | **complete / PR #401** | Accepted on durable dev-cad run #45211961040; direct .sc → STL export and scope-matched GitHub viewer link are live. |
| #348 FlexBenchDog logo cleanup | dev-cad | **unblocked by Forge v0.13.1 after #405** | Replace temporary per-rib Slot Sketches with the released Polygon2D attached-Sketch path while preserving accepted geometry. |
| #327 FlexBenchDog Cone taper | dev-cad | **resume draft PR #328 after #405** | Refresh on v0.13.1 and complete the full-length native Cone build/verification before making the PR ready. |
| #288 CAD-CI workflow/config migration | dev-ci / tool.cad.ci | **later / separate** | Reassess against the current released tool.cad.ci owner baseline before implementation. |
| #205 canonical model.yml contract | dev-cad | **unblocked after #405** | Forge #703 is released in v0.13.1; migrate CAD-only fields to their owning layers in its own focused work. |
| #172 full-catalog native qualification | dev-cad + Forge | **partially actionable; final gate includes #796** | Re-enable and qualify independent roots now; final all-roots acceptance waits until `hub75-panel` is restored after Forge #796. |
| #142 HUB75Display2 | dev-cad | **actionable after #378** | Resume native qualification after the existing wooden HUB75 root is re-enabled and green; treat any #796 exposure as owner-layer evidence, not a local workaround. |
| #135 Bolted Flange circular pattern | dev-cad + Forge | **blocked on Forge #347** | Keep PR #141 parked until the intended applied-feature seed is supported. |
| #91 frame-thickness native regression | dev-cad | **actionable after #378** | Run the saved-design mutation once `hub75-wood-frame` is re-enabled on the accepted Forge baseline. |
| #77 CornerBracket placement/associativity | dev-cad | **actionable after #378** | Validate all eight bracket occurrences on the re-enabled current HUB75 root. |
| #21 interactive SolidCraft viewer | site/product | **later** | Revisit after current model/output contracts stabilize. |
| #20 multiple verified model views | site/product | **later / partially enabled** | Build on generic extra_views; broader responsive gallery contract remains open. |
| #365 HUB75 glazing retention/seal | dev-cad | **next design slice** | Define the physical glazing stack, contact/clearance, retention and sealing before modelling guessed hardware. |
| #371 Detailed HUB75 panel completion | tracking | **tracking only** | Reusable-panel work is split into #373 rear-frame contour, #374 mounting interfaces and #375 connector envelopes. |
| #373 HUB75 rear-frame bay contours | dev-cad + Forge | **implementation unblocked; native acceptance waits on #796** | Use the released clean Polygon2D path; do not add overlapping-profile workarounds, and do not claim native acceptance while `hub75-panel` is temporarily gated. |
| #374 HUB75 mounting tubes/bushings/locator pins | dev-cad + Forge/SolidCraft | **standalone merged / assembly acceptance blocked on #388; root also gated by #796** | Keep the accepted geometry; do not use #796 or #388 as justification for CAD-local primitive/placement workarounds. |
| #375 HUB75 connector envelopes | dev-cad | **implemented / draft PR #390; blocked on #388 before merge** | Keep PR #390 draft until reusable-component assembly output is clean; #407 only gates the standalone root build. |
| #388 HUB75 component-local Cylinder placement regression | dev-cad + Forge/SolidCraft | **blocked on owner-layer qualification** | Five panel bodies are placed correctly, but the 14 native Cylinder join features can appear detached. Forge #753 / draft PR #754 owns the minimal rotated-component reproducer. SolidCraft 0.45 issue #21098 / PR #21145 is the primary runtime hypothesis, not yet proven or released. |
| #382 Stable-to-dev-cad synchronization / CAD checkpoint | repository governance | **Phase A complete; Phase B blocked on #388** | Exact `main -> dev-cad` merge `200c902f976ff6809692cc344379bbdc10dcbd13` is green and source-matched in build/Pages. Do not promote `dev-cad -> main` while #388 remains open. |
| #366 HUB75 rear/electrical interfaces | dev-cad | **blocked on reusable panel children** | After #371 children are accepted, model only enclosure-side clearance/access/cable consequences; do not duplicate panel dimensions. |
| #367 HUB75 exploded view | dev-cad + Forge | **blocked on Forge #751** | SolidCraft 0.45 has native `explode.create/show`; Forge #751 owns the reusable wrapper/qualification, then CAD publishes through generic extra views. |
| #7 complete HUB75 screen assembly | tracking | **tracking only** | Remaining work is split across #8/#77/#91/#365/#366/#367 plus #20/#21; do not create one broad #7 implementation PR. |

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

- PR #169 — draft latch design; keep parked until its required Forge API
  baseline is available.
- PR #141 — Bolted Flange circular pattern; blocked on Forge #347.

PR #349 (#154) and PR #328 (#327) have their required Forge capabilities in
v0.13.1. Resume them after #405 is accepted; #407 isolates the unrelated
`hub75-panel` regression while Forge #796 is fixed upstream.

## Next checkpoint

1. merge #407 into the #405 adoption branch so only `hub75-panel` is
   temporarily disabled for Forge #796; do not change its geometry;
2. require #405 validation to be green on exact Forge v0.13.1, then merge the
   dependency adoption into `dev-cad`;
3. re-enable the existing `hub75-wood-frame` under #378 and require a real
   native build plus source-matched dev-cad output;
4. resume #154 / draft PR #349, then the independent #327/#348/#362/#373
   slices in their own issue/branch/PR order;
5. fix Forge #796 upstream in parallel; after a released Forge fix is adopted,
   restore `hub75-panel` to `process: true` and remove #407's temporary gate;
6. after #378 is green, continue #77/#91 and then #142/full-catalog #172 as
   appropriate;
7. keep #388 on its Forge #753/SolidCraft owner path. It still blocks final
   #374 assembly acceptance, PR #390/#375 and `dev-cad -> main`, but not the
   unrelated model work after #405.
