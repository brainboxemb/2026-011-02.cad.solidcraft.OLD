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
- `dev-cad`: `f975ff4f60af2e719399635fdb5153dc1f052c18`;
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

Current CAD runtime baseline is SolidCraft 0.45.0. CAD #405 / PR #406 has adopted
released Forge v0.13.1 at exact commit
`17a4e1d0e2edf0124d40daf5425891fdf65c24be`. The release contains Forge
#679, #703, #746, #747, #749 and #750. CAD #408 and #412 are merged and keep
only the detailed `hub75-panel` execution path temporarily gated for Forge
#796; that upstream defect therefore does not block qualification of unrelated
models. Forge #753 / CAD #388 remains a separate owner-layer blocker.

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
- #327 / draft PR #328: Forge #746 is in v0.13.1. After #405 is accepted,
  refresh the branch from current `dev-cad`, replace the old 2 mm-tip
  experiment with the intended full-length Ø20.0 -> Ø20.2 native Cone, and
  require native build/verification before making the PR ready.

### 2. Keep temporary capability workarounds explicit

- #348 -> Forge #747: attached/explicit Sketch `Polygon2D` lowering is in
  v0.13.1. After #405, replace the temporary one-Slot-per-Sketch logo
  construction while preserving the accepted visible geometry.
- #362 -> Forge #750: locally rotated standalone Sketch cutters are in v0.13.1.
  After #405, implement the final CornerBracket arm-tip triangular wedge and
  remove the TEMPORARY markers only with the completed geometry.
- #8: PR #360 restored the preserved 11-point arm profile and exact four-part
  recessed M5 fixing seats. The remaining arm-tip wedge becomes actionable
  through #362 after #405.

Do not add CAD-local compiler, transform or command workarounds for these
generic Forge gaps.

### 3. HUB75 iteration 2 refresh

- #154 is represented by current draft PR #349; old PR #156 is closed as
  superseded.
- The refreshed root is `models/advanced/hub75_wood_frame_iter2/` and keeps
  only current product-CAD geometry plus current `model.yml` / `ci.yml`
  ownership.
- Forge #679 naming and #749 model-local import isolation are both in v0.13.1.
  After #405, refresh PR #349 from current `dev-cad` and enable its intended
  native processing. No CAD-local `sys.modules` cleanup is allowed.
- Keep PR #349 draft until the normal native build plus saved-design
  lower-compartment mutation pass succeeds on the adopted release.

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

## Forge v0.13.1 adoption gate

CAD #408 and #412 are merged. Only the detailed `hub75-panel` root is
temporarily `process: false` for Forge #796, and only its direct
Forge-dependent repository tests follow that same process gate. Screen,
static/source and generic component tests remain active.

CAD #405 therefore adopts Forge v0.13.1 for the remaining active roots instead
of holding the whole repository on v0.11.0. This is an execution gate, not a
geometry rollback or compiler workaround. Re-enable `hub75-panel` after Forge
#796 is fixed, released and adopted.

## Forge v0.13.1 follow-ups

The current `hub75-wood-frame` root remains `process: false` until #405 is
accepted, but Forge #679 is present in v0.13.1. After #405, re-enable that root
under #378 and then continue native saved-design acceptance for:

- #91 frame-thickness mutation moving all eight CornerBrackets;
- #77 CornerBracket placement/associativity under dimension changes;
- #142 Hub75DisplayCase v2 native qualification;
- the remaining catalog qualification work in #172.

These become actionable after #405 is merged and #378 proves the existing
wooden HUB75 root on the adopted v0.13.1 baseline.

## Other open work

| Issue | Owner/lane | Status | Next action |
| --- | --- | --- | --- |
| #416 HUB75 display-case product/class names | dev-cad | **now** | Rename only the public product titles and top-level classes to `Hub75DisplayCase` / `Hub75DisplayCaseV2`; preserve paths and slugs. |
| #417 HUB75 display-case paths/slugs | dev-cad/site | **later / compatibility migration** | After both models are green, migrate source roots/model ids/public slugs with explicit redirects/aliases for existing URLs. |
| #412 hub75-panel repository-test process gate | dev-cad | **merged / temporary gate active** | Direct detailed-panel compilation tests follow the existing `ci.yml process` state and auto-restore when the model is re-enabled. |
| #408 Temporary hub75-panel process gate | dev-cad + Forge | **merged / temporary gate active** | `hub75-panel` stays disabled only for Forge #796; re-enable after the upstream fix is released/adopted. |
| #8 CornerBracket exact geometry | dev-cad | **actionable after #405 via #362** | Preserve PR #360 geometry; add the final rotated wedge with released Forge #750 support. |
| #362 CornerBracket arm-tip wedge | dev-cad | **actionable after #405** | Implement the final rotated wedge using v0.13.1 and remove the temporary markers with the completed geometry. |
| #154 HUB75 lower compartment | dev-cad | **resume after #405 / draft PR #349** | Refresh on current dev-cad, enable native processing and complete the saved-design lower-compartment mutation acceptance. |
| #345 STL output + GitHub viewer | dev-cad / SolidCraft runtime | **complete / PR #401** | Accepted on durable dev-cad run #45211961040; direct .sc → STL export and scope-matched GitHub viewer link are live. |
| #348 FlexBenchDog logo cleanup | dev-cad | **actionable after #405** | Replace temporary per-rib Slot Sketches with the released Polygon2D path while preserving accepted geometry. |

| #327 FlexBenchDog Cone taper | dev-cad | **resume after #405 / draft PR #328** | Refresh the branch and implement the intended full-length native Cone before making the PR ready. |
| #288 CAD-CI workflow/config migration | dev-ci / tool.cad.ci | **later / separate** | Reassess against the current released tool.cad.ci owner baseline before implementation. |
| #205 canonical model.yml contract | dev-cad | **actionable after #405 / separate migration** | Forge #703 is in v0.13.1; move CAD-only fields to their owning layers in its own focused change. |
| #172 full-catalog native qualification | dev-cad + Forge | **blocked on temporary disabled roots** | Qualify the active catalog on v0.13.1; final full-catalog acceptance waits for `hub75-panel`/#796 and the intentionally disabled HUB75 roots to be re-enabled. |
| #142 Hub75DisplayCase v2 | dev-cad | **actionable after #405/#378** | Resume native qualification after the existing wooden HUB75 root is green on v0.13.1. |
| #135 Bolted Flange circular pattern | dev-cad + Forge | **blocked on Forge #347** | Keep PR #141 parked until the intended applied-feature seed is supported. |
| #91 frame-thickness native regression | dev-cad | **actionable after #405/#378** | Run the saved-design mutation once hub75-wood-frame is processable on v0.13.1. |
| #77 CornerBracket placement/associativity | dev-cad | **actionable after #405/#378** | Validate all eight bracket occurrences on the re-enabled current HUB75 root. |
| #21 interactive SolidCraft viewer | site/product | **later** | Revisit after current model/output contracts stabilize. |
| #20 multiple verified model views | site/product | **later / partially enabled** | Build on generic extra_views; broader responsive gallery contract remains open. |
| #365 HUB75 glazing retention/seal | dev-cad | **next design slice** | Define the physical glazing stack, contact/clearance, retention and sealing before modelling guessed hardware. |
| #371 Detailed HUB75 panel completion | tracking | **tracking only** | Reusable-panel work is split into #373 rear-frame contour, #374 mounting interfaces and #375 connector envelopes. |
| #373 HUB75 rear-frame bay contours | dev-cad + Forge | **blocked on Forge #796 process gate** | Forge #747 is available, but native acceptance of this detailed panel waits until `hub75-panel` is re-enabled after #796. |
| #374 HUB75 mounting tubes/bushings/locator pins | dev-cad + Forge/SolidCraft | **standalone merged / process gate #796; assembly gate #388** | Re-run standalone native acceptance after #796; keep final five-panel acceptance blocked on #388. |
| #375 HUB75 connector envelopes | dev-cad | **implemented / draft PR #390; blocked on #796 and #388 before merge** | Keep the measured connector geometry; refresh standalone acceptance after #796 and final assembly acceptance after #388. |
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
- PR #141 — draft Bolted Flange circular pattern; blocked on Forge #347.

PR #349 (#154) and PR #328 (#327) stop being Forge-release-blocked once #405
is accepted; refresh each within its existing issue before resuming geometry.

## Next checkpoint

1. complete #416 so the two current wooden enclosure products/classes are
   named `Hub75DisplayCase` and `Hub75DisplayCaseV2` while paths/slugs stay
   stable under #417;
2. re-enable the existing v1 `hub75-wood-frame` under #378 and require a real
   native build on the accepted Forge v0.13.1 baseline;
3. after v1 is green, re-enable/qualify #142 Hub75DisplayCase v2;
4. refresh #154 / PR #349, then resume #327, #348 and #362 as independent
   model slices unlocked by v0.13.1;
5. continue #77/#91 after #378; keep #373/#374/#375 behind the temporary
   `hub75-panel`/#796 gate and #388 on its separate owner path;
6. defer #417 path/model-id/public-slug migration until both display-case
   models are green and the redirect/compatibility contract is explicit;
7. do not promote `dev-cad -> main` until the deliberate stable checkpoint
   criteria are met.
