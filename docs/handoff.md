# Handoff — CAD repository

Repository: `brainboxemb/2026-011-02.cad.solidcraft`.

Read `docs/plan.md` first. It is the source of truth for unfinished work.

Shared SolidCraft/CAD conventions and document templates live in
`brainboxemb/meta.cad.solidcraft`. Use
`templates/docs/plan.md` there as the structural reference for this
repository's plan; keep CAD-specific work and status in this repository.

## Current state

- Permanent source lanes: `main`, `dev-cad`, `dev-ci`.
- Short-lived work is squash-merged into a dev lane.
- `dev-cad` / `dev-ci` promotion to `main` uses a normal merge commit
  through the owner-only `/merge` policy.
- Generic execution/publication is owned by the released
  `tool.cad.ci` / `lib.py.cad.ci` stack.
- Model/site metadata is owned by the 16 local `model.yml` files, representing
  18 published variants.
- Hugo + Blowfish builds the CAD site from those files plus accepted build
  evidence.
- 14 physical model roots / 16 variants build through the shared SolidCraft
  batch. `hub75-display2` and `hub75-wood-frame` remain disabled only for
  Forge #679; do not add CAD-side naming workarounds.
- Durable `build/dev-ci` and Pages `/dev-ci/` publication are proven and
  isolated from stable Pages.
- Stable pre-cut-over Pages are backed up at
  `backup/gh-pages-before-174-2026-11-22`.

## Active workstream

There is one active workstream: finish the `dev-ci` stabilization and promote
that accepted lane to `main`.

Do not start new CAD features, an `examples/` cleanup, new site/theme work, or
unrelated CI refactors until that promotion is complete.

Relevant tracking: #174 (CI/publication migration), #172 (full qualification),
#191 (site migration/history).

After promotion, synchronize/reactivate `dev-cad` and return to product CAD
work.
