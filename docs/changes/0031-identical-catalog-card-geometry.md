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
