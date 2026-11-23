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
- `main` and `dev-ci` currently point to
  `f4469205f9bcef118c169135c0ac5dffaea9837c`.
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
- `dev-cad` is also diverged from `main`, retains unique product-CAD
  history, and still publishes the older Blowfish site. It must not be rebased
  or recreated; synchronize current stable history into it only after the
  `dev-ci` work is promoted.
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

Status: **now — #278 reopened for the approved replacement**.

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

Current port branch:

`issue/278-approved-exp-baseline`

Required order:

1. port the approved EXP hierarchy without extra redesign;
2. record actual `SOLIDCRAFT_VERSION` in model provenance and show it in the
   status badge;
3. require repository tests + CAD-CI PR validation;
4. inspect the CAD-owned Plate/Simple-MFT Chrome screenshot artifact;
5. merge through `/merge` to `dev-ci`;
6. verify durable `build/dev-ci` and Pages `/dev-ci/` source-match;
7. only then promote exact `dev-ci -> main`.

Do not mix #21 or #288 into this replacement.

### WS2 — synchronize dev-cad and reassess parked product work

Owner/lane: repository governance + `dev-cad`.

Status: **next after #278 is durably accepted**.

After the accepted #278 site work is reconciled:

1. open exact `main -> dev-cad`;
2. merge only through `/merge` as a history-preserving permanent-ref merge;
3. require durable `build/dev-cad` and Pages `/dev-cad/` to source-match the
   synchronized lane;
4. reassess PR #141, PR #156 and PR #169 against the new `dev-cad` head;
5. choose one coherent product-CAD work item at a time.

Product/model work stays parked until this synchronization is accepted.

### WS3 — normalize model-description ownership

Owner/lane: shared owner repositories first; CAD adoption in `dev-cad` after
WS2.

- #204 removes the hand-maintained SCPC command count from model metadata.
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
| #278 Calm generic model-detail presentation | dev-ci | **now / reopened** | Port user-approved EXP #29/run #89 framed/source-first baseline; review CAD screenshots before merge. |
| #288 tool.cad.ci v0.25.0 workflow/config migration | dev-ci / CI | **later / separate** | Do not mix with #278; reassess after the current site presentation checkpoint. |
| #250 Shared changelog template/history | documentation | **later** | Reassess after permanent lanes are coherent; do not interrupt WS1/WS2. |
| #206 Remove Forge reference implementations | dev-cad | **next after WS2** | Remove local cross-CAD reference sources/assumptions without changing product geometry. |
| #205 Canonical shared model.yml contract | shared + dev-cad | **blocked** | Wait for an actually reusable/adoptable shared contract; do not copy Forge's site-local validator. |
| #204 Remove SCPC command counts from model.yml | dev-cad | **next after WS2** | Remove the handwritten counts and derive displayed/check counts from generated output. |
| #172 Full-catalog Forge/SolidCraft qualification | dev-cad | **blocked** | Re-enable the two remaining roots after the required Forge fix reaches the CAD-consumed baseline. |
| #168 Verification terminology cleanup | cross-repo | **later** | Revisit after lane and model-ownership cleanup are stable. |
| #154 HUB75 lower storage compartment | dev-cad | **later** | Reassess PR #156 after the exact `main -> dev-cad` synchronization. |
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

Complete the approved #278 replacement on `dev-ci`, inspect the CAD-owned
Plate/Simple-MFT screenshots, and verify durable build/Pages provenance. Only
then promote exact `dev-ci -> main`. Keep #21 and #288 separate.
