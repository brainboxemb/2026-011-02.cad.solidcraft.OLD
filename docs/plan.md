# CAD repository plan

This file is the source of truth for **unfinished work** in
`2026-011-02.cad.solidcraft`.

Detailed implementation history belongs in `docs/changes/` and GitHub issues,
not in this plan.

## Current focus — stabilize and promote dev-ci

**There is one active workstream: finish the #174 dev-ci migration and promote
that accepted lane to main.**

Do not start or expand unrelated work until this section is complete.

### 1. Finish the existing cleanup PR

Active PR: **#201 — Retire legacy CAD CI Python orchestration**.

Required outcome:

- keep only CAD-owned adapters and model-specific checks;
- remove superseded local planner/selector/publisher/HTML-generation code;
- retain broad repository regression coverage through the released CAD-CI graph;
- keep every retained `ci/*` item and `scripts/ci/*` adapter documented;
- no CAD geometry changes;
- no stable Pages cut-over in this PR.

### 2. Qualify the resulting dev-ci lane

After #201 is merged into `dev-ci`:

- run the normal durable `dev-ci` workflow;
- require green released CAD-CI checks;
- verify `build/dev-ci` is complete and source-matched;
- verify Pages publication changes only the `/dev-ci/` subtree;
- compare routes, downloads, warnings, images and representative desktop/mobile
  pages against the stable-site backup;
- do not relabel missing or old evidence as current.

Known external blocker:

- `hub75-display2` and `hub75-wood-frame` remain `process:false` while
  Forge #679 is unresolved. Do not add CAD-side naming workarounds.

### 3. Make repository documentation coherent before promotion

Before `dev-ci -> main`:

- `docs/plan.md` must describe only current unfinished work;
- `docs/handoff.md` is a **repository-level entrypoint**, not a dev-ci-owned
  document. A lane-only copy is transitional and must not be treated as the
  canonical handoff;
- the final promoted main tree must contain the current handoff;
- add a small `docs/README.md` only if needed to make document roles obvious;
- do not start a broad documentation reorganization during this stabilization
  pass.

### 4. Promote dev-ci to main

Promotion is the exit gate for this workstream.

Before promotion:

- synchronize the long-lived lane with the current `main` without flattening
  lane history;
- all required checks must be green on the exact promotion head;
- use the owner-controlled merge policy;
- `dev-ci -> main` uses a normal merge commit, not squash;
- retain the long-lived `dev-ci` branch;
- verify stable build/Pages output after promotion.

After promotion:

- `main` must expose the current `model.yml` catalog and repository handoff;
- `docs/plan.md` on main must match the actual repository state;
- close or rewrite #174/#172 only from recorded acceptance evidence.

## Frozen until the dev-ci promotion is complete

Do **not** start or expand these while the current focus is active:

- new CAD model work or model onboarding;
- `examples/` cleanup/audit;
- additional website redesign or theme work;
- new Forge/CAD-CI enhancements unless an existing external blocker requires
  owner-repository work;
- general branch cleanup unrelated to the promotion;
- terminology refactors;
- new verification coverage that is not required for the current cut-over.

Existing CAD feature PRs may remain open, but they are not the active workstream.

## Accepted state already proven

The following is background, not active work:

- permanent source lanes `main`, `dev-cad`, `dev-ci` exist;
- released CAD-CI is the generic planner/executor/publisher;
- the shared model batch uses one SolidCraft runtime;
- 14 physical model roots / 16 catalog variants build through the accepted
  shared path;
- model metadata is distributed across 16 model-owned `model.yml` files,
  representing 18 published variants;
- Hugo/Blowfish reads the model metadata directly;
- durable `build/dev-ci` and `/dev-ci/` publication have been proven;
- the stable pre-cut-over Pages tip is backed up at
  `backup/gh-pages-before-174-2026-11-22`.

Do not reopen these architecture decisions during the stabilization pass unless
new evidence proves the accepted implementation incorrect.

## Next work after stabilization

Once `dev-ci` is promoted and main is coherent again:

1. synchronize and reactivate `dev-cad`;
2. reassess the existing CAD feature PRs;
3. resume product CAD work;
4. only then audit retained `examples/` and old branches as a separate cleanup
   task.
