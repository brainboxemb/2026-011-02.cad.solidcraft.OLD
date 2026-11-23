# 0031 — Identical catalog card geometry

Issue: #316

## Problem

The shared model-card partial was still invoked in two different catalog modes.
Category routes used `showSection=true`, while `/models/` used
`showSection=false`. That removed the blue section row only on the all-model
page and produced a visibly different vertical card structure for the same
model.

The user identified `/dev-ci/models/basic/` as the intended reference and
reported the remaining mismatch on `/dev-ci/models/`.

## Decision

All catalog overview routes use the same section-bearing card geometry:

- `/models/`;
- `/models/basic/`;
- `/models/components/`;
- `/models/advanced/`.

The blue BASIC / COMPONENTS / ADVANCED row remains visible on every catalog
card. Home continues to use the same shared partial with its additional Updated
metadata row.

No route-specific CSS or duplicate card template is introduced.

## Verification

Repository tests require both the all-model list and category list to invoke
the shared partial with `showSection=true`.

Durable Chrome proof adds `basic-overview.png` so the same Basic cards can be
visually compared directly with the Basic section in `models-overview.png`.

## Scope

Presentation only. Model metadata, geometry, CAD execution and generic CAD-CI
behavior are unchanged.

## Accepted evidence

- PR #317 merged the implementation to `dev-ci`.
- Accepted dev-ci implementation commit:
  `3ae614b0c64a937ef4db92837cf60e288875f857`.
- Dev-ci run #339 (`45145735379`) was green; artifact `14803314793`
  contained both `models-overview.png` and `basic-overview.png`, which were
  visually compared and showed identical Basic card geometry.
- PR #318 promoted the correction through the permanent-lane merge policy.
- `main` and `dev-ci` are synchronized at
  `6bf67ab733293868f349c820fc1dcc6a44abadf0`.
- Stable run #341 (`45146269640`) and dev-ci run #342 (`45146273209`) are green.
- Stable artifact: `model-layouts-main` / `14804840316`.
- Dev-ci artifact: `model-layouts-dev-ci` / `14804067733`.
- Durable build and Pages provenance on both lanes source-match
  `6bf67ab733293868f349c820fc1dcc6a44abadf0`.
