# 0037 — Development-lane promotion cadence

Issue: #346

## Problem

The repository already defined the mechanics for permanent-lane merges, but it
did not state when a working lane should be promoted. That made it too easy to
treat every accepted `dev-cad` or `dev-ci` PR as a reason for an immediate
`dev-* -> main -> dev-*` cycle, causing unnecessary full validation and
publication work.

## Decision

`dev-cad` and `dev-ci` are real working/integration lanes. Multiple logical
changes may be accepted into the owning lane before promotion.

Promotion to `main` is deliberate and checkpoint-based, not per-PR. Suitable
checkpoints include a coherent feature set, the end of a work block/day, a
release point, or a genuine cross-lane dependency. Existing merge mechanics do
not change: short-lived issue branches are still squash-merged into their
owning lane and permanent-lane promotions/synchronizations remain normal
history-preserving merges.

Pure repository-instruction and documentation-only corrections in
`AGENTS.md` and `docs/*` may be committed directly to `main` when they are
independent of unmerged code/model work. Documentation that belongs to a
logical code/model change remains part of that issue, branch and PR.

## Verification

The rule is stated consistently in `AGENTS.md`, `docs/plan.md` and the
session handoff. No CI or merge-policy implementation changes are required.
