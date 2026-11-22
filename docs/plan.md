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

Current stable integration commit:

`4b4ed80188c0de49cb33d4796e243644a7ae8374`

Accepted stable state:

- released CAD-CI owns generic selection, execution and durable publication;
- the shared model build uses one SolidCraft runtime;
- stable `build/main` is source-matched to `4b4ed801...`;
- stable Pages provenance is source-matched to `4b4ed801...`;
- Hugo + Blowfish publishes the CAD catalog from model metadata plus accepted
  build evidence;
- 14 physical model roots / 16 catalog variants build through the accepted
  shared path;
- `hub75-display2` and `hub75-wood-frame` remain disabled only for Forge
  #679; do not add CAD-side naming workarounds;
- runtime baseline: `ghcr.io/brainboxemb/cad-solidcraft:v0.3.4`,
  SolidCraft `0.45.0`;
- Forge baseline: released SCPF `0.11.0` at
  `9258d54079981604b6dd777a4c4face897c190fe`;
- stable pre-cut-over Pages remain backed up at
  `backup/gh-pages-before-174-2026-11-22`;
- the legacy stable build scope is backed up at
  `backup/build-before-174-2026-11-22`.

The shared plan structure is defined by
`brainboxemb/meta.cad.solidcraft/templates/docs/plan.md`.

## Lane rule

- `main` is stable integration only.
- `dev-cad` owns product CAD/model work.
- `dev-ci` owns CAD-CI/runtime/publication integration.
- Short-lived branches target the appropriate lane and are squash-merged.
- Exact `dev-cad -> main` and `dev-ci -> main` promotions use the repository
  `/merge` policy and therefore normal merge commits.
- Before new work starts on a long-lived lane, synchronize it from current
  `main` without flattening its history.
- Generic CI/verification/runtime changes are implemented and released in their
  owner repositories before adoption here.

## Active workstreams

### WS1 — finish migration reconciliation and reactivate dev-cad

Owner/lane: repository-wide governance, then `dev-cad`.

Status:

- the #174 `dev-ci -> main` promotion is complete;
- stable `build/main` and stable Pages are green after the new durable-scope
  bootstrap;
- `dev-ci` has no accepted source work beyond the promoted baseline;
- `dev-cad` is still behind the current stable main and must be synchronized
  before product CAD work resumes.

Next gate:

1. merge this plan/handoff reconciliation;
2. close/rewrite migration issues only from recorded acceptance evidence;
3. synchronize `dev-cad` from current `main` with a normal history-preserving
   merge;
4. re-evaluate the existing `dev-cad` feature PRs against the synchronized
   lane before continuing them.

PR #188 is a stale #174 governance draft and should be reassessed/closed rather
than merged into the now-promoted `dev-ci` lane.

### WS2 — normalize model-description ownership

Owner/lane: shared contract in Forge/meta; CAD adoption in `dev-cad` after lane
reactivation.

- #204 removes the derived SCPC command count from model metadata.
- #205 adopts the canonical shared `model.yml` contract and is blocked on
  Forge #703/shared contract completion.
- #206 removes Forge-owned cross-CAD reference implementations from this product
  repository.

Do not solve #205 by creating another CAD-local schema or validator.

### WS3 — resume product CAD work

Owner/lane: `dev-cad`.

Existing product work remains parked until WS1 has synchronized the lane.

- PR #156 / #154 — lower storage compartment;
- PR #141 / #135 — Bolted Flange circular pattern, blocked on Forge #347;
- PR #169 — latch design draft, with Forge dependencies;
- other geometry/viewer/verification issues remain later work as classified
  below.

## Open issue assignment

| Issue | Lane/owner | Status | Next action |
| --- | --- | --- | --- |
| #206 Remove Forge reference implementations | dev-cad | **next** | Remove local CadQuery/MicroCAD/PythonSCAD/VCAD reference sources after lane sync; retain Forge as reference owner. |
| #205 Canonical shared model.yml contract | shared + dev-cad | **blocked** | Wait for Forge #703/shared contract, then migrate CAD without a copied schema. |
| #204 Remove SCPC command counts from model.yml | dev-cad | **next** | Remove the five hand-maintained counts and reject the field in CAD metadata. |
| #191 Hugo/Blowfish CAD site migration | repository | **effectively complete but still open** | Reconcile final acceptance evidence against stable Pages and close or rewrite remaining follow-up scope. |
| #174 Released CAD-CI/publication migration | repository | **effectively complete but still open** | Record final stable build/Pages evidence after this documentation reconciliation, then close. |
| #189 Per-model model.yml website catalog | repository | **effectively complete but still open** | Keep the completed distributed catalog; track schema correction separately in #205 and then close/rewrite #189. |
| #172 Full-catalog Forge/SolidCraft qualification | dev-cad | **blocked** | Re-enable and qualify the two remaining models after Forge #679; do not add a local workaround. |
| #168 Verification terminology cleanup | cross-repo | **later** | Revisit only after current ownership/model-metadata cleanup is stable. |
| #154 HUB75 lower storage compartment | dev-cad | **later** | Rebase/reassess PR #156 after dev-cad synchronization. |
| #155 CAD-CI lifecycle migration to tool.cad.ci v0.2.0 | repository | **probably obsolete** | Reconcile against completed #174/released current CAD-CI architecture and close/rewrite. |
| #142 HUB75Display2 | dev-cad | **blocked** | Resume native qualification after Forge #679. |
| #135 Bolted Flange circular pattern | dev-cad | **blocked** | Keep PR #141 parked until Forge #347 supports the intended seed feature. |
| #91 Frame-thickness native regression | dev-cad | **later** | Resume with the relevant HUB75 frame work. |
| #77 CornerBracket placement/associativity | dev-cad | **later** | Resume with CornerBracket/HUB75 component work. |
| #34 SCPC alongside SCPF | dev-cad | **later** | Reassess the remaining migration scope against the current five SCPC-backed models before extending it. |
| #21 Interactive SolidCraft viewer | site/product | **later** | Resume only after core model/qualification work is stable. |
| #7 Complete HUB75 screen assembly | dev-cad | **later** | Resume after the relevant reusable model/API blockers are cleared. |
| #20 Multiple verified model views | site/product | **later** | Keep deferred until complex model geometry and verification are stable. |
| #14 Incremental CAD builds / Moon evaluation | CI | **probably obsolete** | Reassess against the released selective CAD-CI/shared-batch architecture before retaining any Moon-specific scope. |
| #8 CornerBracket exact geometry | dev-cad | **later** | Resume as focused geometry work after lane synchronization. |

## Recently completed

- #230 normalized `docs/handoff.md` against the shared meta template: one copyable handoff message, durable repository boundaries, and no duplicated volatile plan/status snapshot.
- #201 retired the legacy local CAD-CI Python orchestration.
- `dev-ci` was synchronized with `main` without flattening lane history.
- PR #203 promoted `dev-ci -> main` through the repository policy as a normal
  merge commit.
- stable `build/main` was bootstrapped from the accepted named-scope contract
  and then accepted by the released CAD-CI publisher.
- stable Hugo/Blowfish Pages now publish from the accepted `main` scope.
- `meta.cad.solidcraft` now owns the shared SolidCraft/CAD plan/template
  convention, and this repository handoff links to it.

## Next release/checkpoint

The next repository checkpoint is not another CI migration.

It is:

1. close the completed #174 migration from exact stable evidence;
2. synchronize/reactivate `dev-cad`;
3. qualify the synchronized lane;
4. choose one existing product CAD work item as the next active model change.

Do not start several parked product PRs in parallel before the lane is
synchronized and their current relevance has been reassessed.
