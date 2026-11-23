# CAD repository plan

This file is the current source of truth for unfinished work in
`2026-011-02.cad.solidcraft`.

This repository owns product CAD models, model-specific expectations and the
published CAD catalog. Shared SolidCraft/CAD repository conventions come from
`brainboxemb/meta.cad.solidcraft`; Forge owns reusable modelling API/compiler
behavior; generic CI, verification and runtime behavior remain in their owner
repositories.

## Current accepted baseline

Permanent source lanes:

```text
main
dev-cad
dev-ci
```

Accepted repository state:

- `main` is stable integration. Its durable `build/main` scope and public
  Pages are source-matched to the current stable source; verify the live
  provenance before every synchronization/promotion rather than copying a
  stale SHA into a handoff.
- The public site uses Hugo **0.169.0** with Hextra **v0.13.0**.
- The Hextra migration and final migration documentation are complete. The
  post-migration `dev-ci` work has since normalized catalog/model-page
  presentation and changed the landing page to show Git-derived recently
  updated models.
- `main` currently consumes released `tool.cad.ci 0.18.0`
  (`b62f9d0b169aa201a3c66c3166f364396b2d71bc`) for CAD execution and
  `tool.cad.ci 0.20.1`
  (`eb64a46b243db00e8dbb4b78b6643a2a7efa3fb9`) for merge policy.
- #316 / PRs #317 and #318 made all catalog overview routes use the same
  section-bearing card geometry and promoted that correction to stable.
- #204 is complete. PR #315 promoted the accepted removal of handwritten
  `scpc_command_count` metadata to stable `main`.
- `main` is currently
  `5712fce7d62a958156cdc85e3b12d57a6372b23e`; durable `build/main` and
  public Pages source-match that commit (run #349).
- `dev-ci` remains on the accepted site-integration baseline
  `57c45499c02e3a70b30382488827fa5f87239088`; no active site work is
  required before the current product-CAD work.
- #310 / PR #311 synchronized stable history into `dev-cad` as the normal
  history-preserving merge commit
  `4e6f36f946cdb560fa2349f8559419f66ba577fc`.
- Durable `build/dev-cad` and Pages `/dev-cad/` source-match
  `4e6f36f946cdb560fa2349f8559419f66ba577fc` (run #353); the synchronized
  development site now uses Hugo/Hextra like stable.
- #206 / PR #326 removed the local cross-CAD reference implementations.
- #331 / PR #334 replaced the old Ø24 × 3 mm band with the shaped Ø22 × 1.5 mm
  MFT stop collar.
- #333 / PR #338 added the R0.5 four-edge inner-corner relief. Durable run
  #373 proved that geometry. #333 remains open only for underside-view visual
  acceptance because the standard catalog camera does not expose the central
  cross clearly.
- #332 / PR #341 preserved the intended nine BrainBox cube centerlines but its
  one-Sketch/nine-Slot construction was visually rejected: intersecting closed
  profiles produced a filled six-sided cut. #332 remains active for the
  independent-rib correction; PR #341 is not an accepted visual baseline.
- The presentation from change 0027 was later visually rejected; Pages was
  temporarily switched back to the preserved pre-change publication while the
  replacement was worked out in EXP.
- EXP issue #29 / PR #31 is the user-approved replacement baseline. EXP main
  commit `b0ed2dc474affc9bc0591ff60c5e95ce12a31b25` and run #92
  (`45134031122`) prove the approved framed/source-first layout, including the
  SolidCraft version badge, before this CAD port.
- The synchronized `dev-ci` lane consumes released `tool.cad.ci 0.21.0`
  (`b1474f6be66dc0236f2a5c2555af07a100447255`) for CAD execution and merge
  policy. The later tool.cad.ci lifecycle migration is tracked separately in
  #288 and is not part of the current site presentation work.
- `dev-cad` retains its unique product-CAD history and now also contains the
  current stable history through the accepted permanent-lane merge. Do not
  rebase or recreate the lane.
- Runtime baseline is
  `ghcr.io/brainboxemb/cad-solidcraft:v0.3.4` with SolidCraft `0.45.0`.
- There are 16 physical model roots and 18 published model variants. Fourteen
  physical model roots are processed; `hub75-display2` and
  `hub75-wood-frame` remain blocked on their Forge-side naming/API
  qualification.
- `model.yml` remains model-owned website description data. Generated facts
  such as command counts, build status and Git last-modified timestamps do not
  belong in handwritten model metadata.

The shared plan structure is defined by
`brainboxemb/meta.cad.solidcraft/templates/docs/plan.md`.

## Lane rule

- `main` is stable integration only.
- `dev-cad` owns product CAD/model work.
- `dev-ci` owns CAD-CI/runtime/publication/site integration.
- Short-lived branches target the appropriate lane and are squash-merged.
- Exact `main -> dev-cad|dev-ci` synchronization uses a normal merge commit.
- Exact `dev-cad|dev-ci -> main` promotion uses a normal merge commit.
- Permanent-ref synchronization and promotion use the owner-only repository
  `/merge` policy; do not use GitHub merge buttons as an alternative.
- Generic CI/verification/runtime changes are implemented and released in
  their owner repositories before adoption here.
- Reconcile this plan after each permanent-lane synchronization/promotion or
  other change that materially alters the accepted baseline.

## Active workstreams

### WS1 — port the user-approved EXP model-detail baseline

Owner/lane: `dev-ci`.

Status: **promoted and accepted, including #303 row alignment and #316 identical catalog-card geometry**.

The earlier 0027 presentation was technically green but visually rejected.
The restored backup publication was then used as the baseline in EXP issue #29.

User-approved reference:

- EXP PR #31;
- EXP run #92 (`45134031122`);
- framed panel hierarchy retained;
- SCPF source visible by default;
- Background and reference section labels added;
- Background bullets restored;
- Construction-stage spacing tightened;
- generated commands collapsed;
- no standalone numeric section labels.

Accepted CAD evidence:

- PRs #293/#294 ported and corrected the approved framed model-detail baseline;
- #297 / PRs #299/#300/#301 established the shared four/two/one model-card grid;
- #303 / PR #304 replaced flex-flow card internals with explicit named rows;
- #316 / PR #317 made `/models/` use the same section-bearing card geometry as
  Basic/Components/Advanced category pages;
- PR #318 promoted the accepted #316 correction through the permanent-lane
  merge policy;
- `main` and `dev-ci` are synchronized at
  `6bf67ab733293868f349c820fc1dcc6a44abadf0`;
- stable run #341 (`45146269640`) and dev-ci run #342 (`45146273209`) are green;
- stable screenshot artifact `model-layouts-main` is artifact `14804840316`;
- dev-ci screenshot artifact `model-layouts-dev-ci` is artifact `14804067733`;
- `models-overview.png` and `basic-overview.png` were visually compared and
  show identical Basic card geometry;
- `build/main`, public Pages, `build/dev-ci` and Pages `/dev-ci/` all
  source-match the synchronized lane;
- public Pages build commit is
  `480d4f7d1a98acfaf6409b6e041e89beff7fc828`;
- dev-ci Pages build commit is
  `d9ba40d1664cb51aea1941f394d8582bcf319222`;
- published Plate and Simple MFT provenance record SolidCraft `0.45.0`.

Required next order:

- none; WS1 is accepted and stable;
- keep #21 and #288 separate from any future site work.

### WS2 — synchronize dev-cad and reassess parked product work

Owner/lane: repository governance + `dev-cad`.

Status: **completed**.

Accepted evidence:

- #314 / PR #315 promoted the already accepted #204 metadata contract to
  current stable `main`;
- #321 / PR #322 converged the remaining stable model metadata and plan before
  the permanent lane merge;
- all former conflict files were byte-identical between `main` and
  `dev-cad` before synchronization;
- #310 / PR #311 merged `main -> dev-cad` using the repository policy as a
  normal history-preserving merge commit;
- synchronized `dev-cad` is
  `4e6f36f946cdb560fa2349f8559419f66ba577fc`;
- durable run #353 (`45149024946`) is green;
- `build/dev-cad` and Pages `/dev-cad/` source-match the synchronized lane;
- Pages build commit is
  `bd4dfdcf4e6c0b5a74b9c7635c66e6f0128a52c8`;
- screenshot artifact `model-layouts-dev-cad` is artifact `14804679663`.

Parked product reassessment:

- PR #141 / #135 remains blocked on Forge #347;
- PR #169 remains blocked: Forge #349 is open, and the completed sheet/profile
  fixes are newer than the CAD-consumed Forge v0.11.0 release;
- PR #156 / #154 has no current upstream blocker, but its old branch is
  substantially behind the synchronized lane and still contains stale
  catalog/CI-era edits. Preserve the model work and refresh it deliberately
  when its turn arrives.

### WS3 — normalize model-description ownership

Owner/lane: shared owner repositories first; CAD adoption in `dev-cad` after
WS2.

- #204 is complete: handwritten SCPC command counts are removed and rejected
  as model metadata.
- #205 adopts a genuinely reusable canonical model-description contract.
  Forge #703 is closed, but current Forge `main` still exposes its validator
  as site-local `site/example_metadata.py`; do not copy that validator into
  CAD. Resume only when an adoptable shared contract is actually available.
- #206 removes cross-CAD reference implementations that belong to Forge.

Keep these as focused ownership cleanups. Do not create another CAD-local
schema, planner or reference framework.

## Open issue assignment

| Issue | Lane/owner | Status | Next action |
| --- | --- | --- | --- |
| #278 Model-detail presentation replacement | dev-ci | **promoted / accepted** | Framed model-detail baseline plus #297/#303 catalog corrections are stable; no further action in this workstream. |
| #288 tool.cad.ci v0.25.0 workflow/config migration | dev-ci / CI | **later / separate** | Do not mix with #278; reassess after the current site presentation checkpoint. |
| #250 Shared changelog template/history | documentation | **later** | Reassess after permanent lanes are coherent; do not interrupt WS1/WS2. |
| #205 Canonical shared model.yml contract | shared + dev-cad | **blocked** | Wait for an actually reusable/adoptable shared contract; do not copy Forge's site-local validator. |
| #172 Full-catalog Forge/SolidCraft qualification | dev-cad | **blocked** | Re-enable the two remaining roots after the required Forge fix reaches the CAD-consumed baseline. |
| #168 Verification terminology cleanup | cross-repo | **later** | Revisit after lane and model-ownership cleanup are stable. |
| #333 FlexBenchDog rounded central slot corners | dev-cad | **implemented / visual pending** | PR #338 and durable run #373 prove the R0.5 four-edge fillet; keep open because the standard upper-oblique render does not expose the central underside cross clearly enough for visual acceptance. |
| #332 FlexBenchDog BrainBox cube-wireframe logo | dev-cad | **correction now** | Keep the accepted nine centerlines, put each 0.6 mm Slot rib in its own Sketch/cut, and visually verify that all three cube faces remain open. |
| #348 FlexBenchDog logo workaround cleanup | Forge + dev-cad | **blocked** | Keep the temporary one-Slot-per-Sketch implementation until Forge #747 adds Polygon2D support for explicit/attached Sketch compilation and that support reaches the CAD-consumed release. |
| #327 FlexBenchDog full-length native Cone taper | dev-cad | **blocked** | PR #328 proved native Cone exists, but Forge #746 must add Cone join/cut feature compilation and reach a CAD-consumable release/pin. |
| #154 HUB75 lower storage compartment | dev-cad | **next after #332** | Refresh PR #156 against current dev-cad and retain only the product/model work; drop stale catalog/CI-era edits. |
| #142 HUB75Display2 | dev-cad | **blocked** | Resume qualification after the required Forge naming fix reaches the CAD baseline. |
| #135 Bolted Flange circular pattern | dev-cad | **blocked** | Keep PR #141 parked until Forge #347 supports the intended applied feature seed. |
| #91 Frame-thickness native regression | dev-cad | **later** | Resume with relevant HUB75 frame work. |
| #77 CornerBracket placement/associativity | dev-cad | **later** | Resume with CornerBracket/HUB75 component work. |
| #34 SCPC alongside SCPF | dev-cad | **later** | Reassess remaining scope against current supported SCPC-backed models before extending it. |
| #21 Interactive SolidCraft viewer | site/product | **later** | Resume only after lane synchronization and current product work are stable. |
| #20 Multiple verified model views | site/product | **later** | Keep deferred until complex model geometry and verification are stable. |
| #14 Incremental CAD builds / Moon evaluation | CI | **probably obsolete** | Reassess against released selective CAD-CI/SCons; retain only an unmet requirement if one still exists. |
| #8 CornerBracket exact geometry | dev-cad | **later** | Resume as focused geometry work after WS2. |
| #7 Complete HUB75 screen assembly | dev-cad | **later** | Resume after relevant reusable model/API blockers are cleared. |

Parked open product PRs:

- PR #141 — Bolted Flange circular pattern;
- PR #156 — HUB75 lower storage compartment;
- PR #169 — latch design draft.

## Recently completed

- #333 / PR #338 implemented the R0.5 four-edge fillet around the FlexBenchDog
  central cross. PR and durable CAD verification are green at
  `b68e3670e5278bda9dcd5de32aafc4772cb7c269`; only the explicit underside
  visual acceptance remains open.
- #331 / PR #334 shaped the FlexBenchDog stop collar as a Ø22 × 1.5 mm MFT
  seat with a 1.0 mm 45° underside chamfer back to Ø20. Durable run #368 and
  both dev-cad publication scopes source-match
  `086678bd0ce9280f14603df66231da75ec3b5a56`.
- #310 / PR #311 completed the permanent history-preserving `main -> dev-cad`
  synchronization. Run #353 and both durable dev-cad publication scopes
  source-match `4e6f36f946cdb560fa2349f8559419f66ba577fc`.
- #204 / #314 / PR #315 removed handwritten SCPC command counts from model
  metadata on stable; #321 / PR #322 completed the final metadata convergence
  required for the lane merge.
- #316 / PRs #317/#318 made catalog card geometry identical between `/models/`
  and category pages and promoted the accepted layout to stable.
- #297 / PRs #299, #300 and #301 established one shared four/two/one model-card
  grid on Home and Models, fixed preview/text slots, and added durable
  Home/Models screenshot proof. Run #309 is the visually accepted dev-ci
  baseline.
- #253 reconciled this plan from current branch/build/Pages evidence after the
  Hextra migration and subsequent `dev-ci` work.
- #274 / PR #280 replaced repeated homepage category blocks with six
  Git-derived recently updated model cards; durable `dev-ci` Pages are
  source-matched to `73d3268b2f3fd647d8c73f52559718f8378440fc`.
- #257 established the model-detail typography baseline. The first #278/0027
  layout was technically validated but later visually rejected; change 0028
  records the user-approved EXP replacement now being ported.
- #273 simplified the all-model catalog so category context is not repeated in
  multiple visual layers.
- #263/#267/#269 completed the remaining construction-stage typography,
  library Pages-link and Hugo/Hextra footer refinements.
- #191/#251 completed the Hugo/Hextra migration and final migration
  documentation.
- PR #254 adopted externally accepted `tool.cad.ci 0.21.0` on `dev-ci`.

Historical implementation detail belongs in issues and `docs/changes/`, not
in this plan.

## Next checkpoint

Complete the #332 visual correction before returning to #154:

1. retain the nine BrainBox cube centerlines and 0.6 mm line width;
2. replace the rejected one-Sketch/nine-Slot implementation from PR #341 with
   nine independent Sketches containing one native Slot rib each;
3. cut every rib 0.6 mm deep while leaving the three projected cube faces as
   material;
4. compare SCPF and independent SCPC Slot/cut geometry;
5. inspect the PR top-view/perspective render and merge only when it visibly
   reads as the supplied wireframe cube;
6. then continue the clean #154 refresh from current `dev-cad`.

Keep #333 open only for explicit underside-view visual acceptance of R0.5.
Keep #348 blocked on Forge #747; the per-rib Slot sketches are explicitly
temporary compatibility code, not the desired final logo construction.
Keep #327 / PR #328 draft and parked on Forge #746. Keep PR #141 parked on
Forge #347. Keep PR #169 draft/parked until its required Forge API is available
in a CAD-consumable release. Keep #21 and #288 separate.
