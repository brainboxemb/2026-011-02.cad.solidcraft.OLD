# 0025 — Adopt the released shared merge policy

Issue: #245

## Problem

The CAD repository still owns a copied merge-policy engine in
`.github/workflows/merge-policy.yml` plus `scripts/merge_policy.py`.

During exact `main -> dev-ci` synchronization PR #240, all normal PR checks
passed, but the local `/merge` workflow rejected its own command check:

```text
merge refused: checks are not green: merge=queued/none
```

The command workflow enumerates all check runs on the PR head and therefore
mistakes its own in-progress issue-comment job for an unmet PR validation gate.

This is generic repository merge behavior, not CAD model/site behavior.

Released `tool.cad.ci v0.20.1` at
`eb64a46b243db00e8dbb4b78b6643a2a7efa3fb9` already owns and externally
qualifies this behavior. Its reusable merge workflow filters issue-comment
command runs by Actions run identity and supports both permanent directions:

- `dev-cad|dev-ci -> main`: normal promotion merge;
- `main -> dev-cad|dev-ci`: normal history-preserving synchronization.

Forge already consumes that exact reusable workflow.

## Decision

CAD will stop owning merge-policy mechanics.

`.github/workflows/merge-policy.yml` becomes a thin repository-specific caller
of:

`brainboxemb/tool.cad.ci/.github/workflows/reusable-merge-policy.yml@eb64a46b243db00e8dbb4b78b6643a2a7efa3fb9`

CAD supplies only its configuration:

- stable ref: `main`;
- development lanes: `dev-cad`, `dev-ci`;
- additional permanent refs: `build`, `gh-pages`;
- temporary cleanup prefixes including CAD's `ci/` prefix;
- integration workflow: `cad.yml`.

The local `scripts/merge_policy.py` is removed rather than retained as a
second decision engine.

The normal CAD execution/publication action pin in `.github/workflows/cad.yml`
is outside this change.

## Contract

- `/merge` remains the only supported merge-method entrypoint.
- Short-lived work remains squash-merged.
- Exact permanent-lane promotion and synchronization use normal merge commits.
- Permanent source/generated/backup refs are never cleanup targets.
- The reusable owner workflow validates the exact current PR head and excludes
  its own issue-comment command runs from the required-check set.
- CAD owns only the lane/ref/prefix/workflow configuration needed by the shared
  policy.

## Verification

- repository tests assert that the wrapper pins the exact accepted 0.20.1 SHA
  and supplies the expected CAD configuration;
- repository tests assert that no local `scripts/merge_policy.py` remains;
- the ordinary CAD PR workflow must pass;
- existing exact PR #240 is revalidated against the resulting `main` head;
- #240 must merge only through `/merge`;
- the resulting `dev-ci` head must be a real normal merge with both permanent
  histories and must publish matching durable `build/dev-ci` and Pages
  provenance.
