# 0029 — Shared four-column model-card grid

Issue: #297

## Problem

Home and `/models/` used separate three-column overrides even though both
routes render the same model-card component.

At the accepted 1080 px content width this left cards unnecessarily wide. The
larger visible problem was text rhythm: title, tagline and technical parameters
wrapped freely, so cards in the same row developed different text heights.

## Decision

Home and `/models/` use one shared model-card grid contract:

- desktop: 4 equal columns;
- medium/tablet: 2 equal columns;
- narrow/mobile: 1 column;
- no route-specific Home/Catalog column overrides.

The card itself owns stable text geometry:

- image: fixed compact height, with the slot retained even when a model has no current preview image;
- title: fixed 2-line slot, clamped to 2 lines;
- tagline: fixed 2-line slot, clamped to 2 lines;
- technical parameters: fixed 2-line slot, clamped to 2 lines;
- status badge remains pinned at the bottom.

The metadata itself is not shortened or rewritten to solve presentation.

## Landing page

The landing page shows the 8 most recently updated models instead of 6. At the
desktop four-column width that produces two complete initial rows.

## Visual verification

The durable headless-Chrome proof is extended with:

- `home-overview.png`;
- `models-overview.png`;

in addition to the existing Plate and Simple MFT detail screenshots.

The `dev-ci -> main` promotion stays blocked until these two new screenshots
are reviewed.

## Scope

Presentation only. No model geometry, source metadata or CAD-CI lifecycle work
is part of this change.
