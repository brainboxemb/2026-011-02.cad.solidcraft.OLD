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

Current heads before #421:

- `main`: `6be947fd47333389513e64a73ae19649eb80796a`;
- `dev-cad`: `e7149d2b402c4ba30835c6b56aeb5373205ef496`;
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

Current CAD runtime baseline is SolidCraft 0.45.0. CAD #421 adopts released
Forge v0.13.2 at exact commit
`ea5710a5d2d33b0633b93c5da95dd5b74f126aa4`. v0.13.2 contains the
v0.13.1 capability batch plus Forge #796's symbolic placed-primitive hotfix.
The temporary #408/#412 detailed `hub75-panel` gate is therefore removed and
the model plus its direct repository tests run normally again. Forge #753 /
CAD #388 remains a separate owner-layer blocker.

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

### 3. Hub75DisplayCase v2 consolidation

- #142 created `hub75-display2` as a temporary v1-geometry comparison baseline.
- #154 then added the actual v2 lower-compartment geometry under
  `hub75_wood_frame_iter2`.
- Those are the same product evolution, not two physical products. #427
  consolidates the complete #154 geometry, tests and 70→90 mm saved-design
  verification into the canonical `hub75-display2` root.
- After #427 the wooden enclosure family contains only
  `Hub75DisplayCase` (v1) and `Hub75DisplayCase v2`; no
  `WoodenHub75BoxIter2` catalog/root remains.

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

## Forge v0.13.2 detailed-panel adoption

CAD #421 / PR #423 adopted exact Forge v0.13.2 and restored `hub75-panel`
to `process: true`. Durable run #45271789698 selected all 16 existing
physical roots, built `hub75-panel` natively, and finished green. Forge #796
is therefore no longer a CAD execution blocker; the direct detailed-panel
repository tests from #412 run normally again because they derive their state
from the model's `ci.yml`.

The temporary #408/#412 gate is retired without a panel-geometry change.
Forge #753 / CAD #388 remains separate and still owns the component-local
Cylinder/occurrence problem.

## Forge v0.13.x follow-ups

The current accepted Forge baseline is v0.13.2. CAD #378 / PR #419 proved
Hub75DisplayCase v1, CAD #142 / PR #420 proved Hub75DisplayCase v2, and
CAD #421 / PR #423 restored the detailed `hub75-panel`.

Current released-capability follow-ups include:

- #427 is complete: #154 geometry is consolidated into the one canonical
  Hub75DisplayCase v2 root;
- #91 frame-thickness native mutation is implemented and green in draft PR
  #431; finalize its clean-head run/merge;
- #77 remains the next Hub75DisplayCase v1 associativity slice for opening
  width/height and orientation;
- #327 is complete; #348 and #362 are technically green draft PRs waiting only
  on exact PR render evidence through tool.cad.ci #181;
- #373 is technically green in draft PR #430 and likewise waits only on exact
  rear-view PR render evidence; #374 is already merged standalone and #375
  remains parked behind #388 for final assembly acceptance;
- the remaining catalog qualification work in #172.

## Other open work

| Issue | Owner/lane | Status | Next action |
| --- | --- | --- | --- |
| #378 Hub75DisplayCase native re-enable | dev-cad | **complete / PR #419** | v1 selected and passed native SolidCraft build on Forge v0.13.1 with STEP and image output. |
| #416 HUB75 display-case product/class names | dev-cad | **complete / PR #418** | Product/class names are `Hub75DisplayCase` / `Hub75DisplayCaseV2`; paths and slugs remain intentionally stable under #417. |
| #417 HUB75 display-case paths/slugs | dev-cad/site | **later / compatibility migration** | After both models are green, migrate source roots/model ids/public slugs with explicit redirects/aliases for existing URLs. |
| #422 lower-compartment case naming | dev-cad/site | **obsolete through #427** | The lower-compartment model is Hub75DisplayCase v2; no third product needs a name. Close after #427 merges. |
| #421 Forge v0.13.2 + detailed hub75-panel re-enable | dev-cad | **complete / PR #423** | Durable run #45271789698 selected all 16 existing roots and built detailed `hub75-panel` successfully on exact v0.13.2. |
| #412 hub75-panel repository-test process gate | dev-cad | **complete / gate retired** | Tests continue deriving from `ci.yml`; with `process:true` they run normally on v0.13.2. |
| #408 Temporary hub75-panel process gate | dev-cad + Forge | **complete / gate retired** | Forge #796 is fixed in v0.13.2 and the detailed root is active again. |
| #8 CornerBracket exact geometry | dev-cad | **actionable after #405 via #362** | Preserve PR #360 geometry; add the final rotated wedge with released Forge #750 support. |
| #362 CornerBracket arm-tip wedge | dev-cad | **draft PR #429 / technical green** | Four OpenSCAD arm-tip wedges are native/SCPC green; keep draft only for exact horizontal/vertical tip render review through tool.cad.ci #181. |
| #154 lower-compartment HUB75 geometry | dev-cad | **complete / consolidated by #427** | Geometry and 70→90 mm verification live in canonical `hub75-display2`; no separate Iter2 root remains. |
| #345 STL output + GitHub viewer | dev-cad / SolidCraft runtime | **complete / PR #401** | Accepted on durable dev-cad run #45211961040; direct .sc → STL export and scope-matched GitHub viewer link are live. |
| #348 FlexBenchDog logo cleanup | dev-cad | **draft PR #426 / technical green** | Polygon2D cleanup is native/SCPC green; keep draft only for exact logo render review through tool.cad.ci #181. |

| #327 FlexBenchDog Cone taper | dev-cad | **complete / PR #328** | Full-length native Cone is merged and durable-green; #348 remains a separate logo-construction cleanup. |
| #288 CAD-CI workflow/config migration | dev-ci / tool.cad.ci | **later / separate** | Reassess against the current released tool.cad.ci owner baseline before implementation. |
| #205 canonical model.yml contract | dev-cad | **actionable after #405 / separate migration** | Forge #703 is in v0.13.1; move CAD-only fields to their owning layers in its own focused change. |
| #172 full-catalog native qualification | dev-cad + Forge | **active** | Requalify the corrected 16-root / 18-variant catalog after #427; do not count #154 as a separate root. |
| #142 Hub75DisplayCase v2 baseline | dev-cad | **complete / corrected by #427** | `hub75-display2` is the single canonical v2 root and contains the accepted #154 lower-compartment geometry. |
| #135 Bolted Flange circular pattern | dev-cad + Forge | **blocked on Forge #347** | Keep PR #141 parked until the intended applied-feature seed is supported. |
| #91 frame-thickness native regression | dev-cad | **complete / PR #431** | Native 12→18 mm saved-design verification is merged on dev-cad and checks exact five-Board and eight-CornerBracket envelopes at 0.001 mm tolerance. |
| #77 CornerBracket placement/associativity | dev-cad | **now / branch active** | Add native 844→1000 mm opening-width and 362→400 mm opening-height saved-design acceptance for all eight bracket occurrences and orientation/handedness, without geometry changes. |
| #21 interactive SolidCraft viewer | site/product | **later** | Revisit after current model/output contracts stabilize. |
| #20 multiple verified model views | site/product | **later / partially enabled** | Build on generic extra_views; broader responsive gallery contract remains open. |
| #365 HUB75 glazing retention/seal | dev-cad | **next design slice** | Define the physical glazing stack, contact/clearance, retention and sealing before modelling guessed hardware. |
| #371 Detailed HUB75 panel completion | tracking | **tracking only** | Reusable-panel work is split into #373 rear-frame contour, #374 mounting interfaces and #375 connector envelopes. |
| #373 HUB75 rear-frame bay contours | dev-cad + Forge | **draft PR #430 / technical green** | R5/stepped bay contours plus 0.8 mm rail recess are native-green; keep draft only for exact rear-view render review through tool.cad.ci #181. |
| #374 HUB75 mounting tubes/bushings/locator pins | dev-cad + Forge/SolidCraft | **standalone merged / assembly gate #388** | Re-run standalone native acceptance on v0.13.2; keep final five-panel acceptance blocked on #388. |
| #375 HUB75 connector envelopes | dev-cad | **implemented / draft PR #390; blocked on #388 before merge** | Refresh standalone acceptance on v0.13.2; final assembly acceptance remains blocked on #388. |
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

#427 / PR #428 has consolidated the proven #154 lower-compartment geometry
into canonical `hub75-display2`. #327 / PR #328 is complete. Draft PRs
#426/#348, #429/#362 and #430/#373 are technically green and wait only on the
shared exact-PR render evidence gap tracked by tool.cad.ci #181.

## Next checkpoint

1. finish #91 / PR #431: squash to one logical commit, re-run the already-green
   native 12→18 mm five-Board/eight-CornerBracket verification, then merge;
2. implement #77 separately with native opening-width/opening-height saved
   designs and explicit eight-bracket orientation/handedness acceptance;
3. keep #426/#348, #429/#362 and #430/#373 draft on the common exact-render
   review gate; fix that generically in tool.cad.ci #181, never per consumer;
4. keep #374 as already merged standalone and #375/PR #390 parked behind #388
   for final five-panel assembly acceptance;
5. continue the remaining independent model slices after #77;
6. keep #417 as the later HUB75 path/slug compatibility migration;
7. do not promote `dev-cad -> main` until the deliberate stable checkpoint
   criteria are met.
