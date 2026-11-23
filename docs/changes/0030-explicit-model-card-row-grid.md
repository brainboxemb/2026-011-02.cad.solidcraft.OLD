# 0030 — Explicit model-card row grid

Issue: #303

## Problem

The outer four/two/one model grid from #297 was correct, but the card itself
still used flex-column flow. Fixed or minimum heights on title/tagline/parameter
elements did not prevent a two-line title from moving later content on the
published `dev-ci` category page.

## Decision

Keep one shared `cad/model-card.html` partial, but make the card internals an
explicit named CSS grid:

- fixed preview row;
- optional section row;
- fixed two-line title row;
- optional updated row;
- fixed two-line tagline row;
- fixed two-line parameters row;
- flexible spacer;
- final status row.

The partial adds capability classes only for the optional section/updated rows.
No route-specific card implementation is introduced.

The preview no longer depends on negative margins. The card owns its outer
image row directly and text/status rows use normal horizontal insets.

## Verification

Repository tests assert the named-row contract and reject the old flex-flow
alignment mechanism.

Durable Chrome proof adds `components-overview.png` so the exact reported
`/dev-ci/models/components/` route is inspected alongside Home and Models.

## Scope

Presentation only. Model metadata, geometry, CAD execution and generic CAD-CI
behavior are unchanged.
