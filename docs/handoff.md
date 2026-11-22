# Handoff — CAD repository

Repository: `brainboxemb/2026-011-02.cad.solidcraft`.

Read `docs/plan.md` first. It is the source of truth for unfinished work.

Shared SolidCraft/CAD conventions and document templates live in
`brainboxemb/meta.cad.solidcraft`. Use
`templates/docs/plan.md` there as the structural reference for this
repository's plan; keep CAD-specific work and status in this repository.

## Current state

- Stable `main`: `4b4ed80188c0de49cb33d4796e243644a7ae8374`.
- Permanent source lanes: `main`, `dev-cad`, `dev-ci`.
- Short-lived work is squash-merged into a dev lane.
- `dev-cad` / `dev-ci` promotion to `main` uses a normal merge commit
  through the owner-only `/merge` policy.
- The #174 `dev-ci -> main` migration promotion is complete.
- Stable `build/main` and stable Hugo/Blowfish Pages are source-matched to the
  current stable main.
- Generic execution/publication is owned by released
  `tool.cad.ci` / `lib.py.cad.ci`.
- Runtime baseline is `cad-solidcraft:v0.3.4` with SolidCraft `0.45.0`.
- 14 physical model roots / 16 variants build through the shared SolidCraft
  batch; two remain blocked only by Forge #679.
- Forge and CAD model-description schemas have drifted; #205 / Forge #703 own
  the correction. Do not extend the CAD-local schema meanwhile.
- Stable pre-cut-over generated state is retained on the backup build/Pages
  branches.

## Active workstream

One workstream is active:

1. reconcile/close the completed #174 migration from exact evidence;
2. synchronize `dev-cad` from current `main` without flattening history;
3. reassess the existing CAD feature PRs;
4. then resume one product CAD work item.

New model-metadata cleanup (#204/#205/#206) is recorded in the plan but must not
turn into another parallel migration before the lane is coherent.

PR #188 is an old #174 governance draft and should be reassessed rather than
merged into the already-promoted CI lane.
