# 0027 — Calm generic model-detail presentation

Issue: #278
Reference experiment: `brainboxemb/exp.2026-015.hugo-cad-site`

## Problem

The accepted Hextra CAD site accumulated several independent model-detail
presentation rules after migration. Preview, Files, Background, SolidCraft Web,
technical source, generated commands and build evidence no longer formed one
clear information hierarchy.

The visible regressions included:

- Construction-stage typography drifting away from ordinary CAD prose;
- preview geometry being coupled to heading height;
- large standalone section ordinals around technical sections;
- SCPF source expanding by default and dominating the page;
- build/provenance values presented as dashboard-like mini-cards;
- Simple MFT requiring presentation treatment that differed from simpler model
  pages.

The EXP repository was used to resolve the presentation question before making
another consumer-site change.

## Decision

Adopt the calm generic model-detail contract proven in the EXP repository.

Accepted EXP evidence:

- Hextra v0.13.0;
- EXP main after PR #27:
  `fcbb9ba4fb22856f016dd2f129c5bb3d07b84b7b`;
- accepted live proof run #80:
  `45069974361`;
- Plate and Simple MFT rendered through one generic model-detail template;
- headless-browser screenshots retained by CI.

The CAD site keeps its existing routes and model-owned data. This change is a
presentation consolidation, not another site migration.

## Model-detail contract

### Overview

A model page begins with:

1. the existing model hero;
2. a compact facts row derived from generated evidence/model metadata;
3. two neutral overview panels:
   - Model preview;
   - Files + Construction stages.

Preview image geometry is independent from heading height. Construction stages
use the normal CAD prose font, body weight and line-height.

### Document sections

Below the overview, ordinary content uses document sections separated by subtle
rules instead of another layer of cards.

This includes:

- Open in SolidCraft Web;
- optional Background;
- optional extra/reference views;
- SCPF source;
- generated SolidCraft commands;
- optional SCPC source/comparison;
- build and verification;
- source/download links.

Warnings remain semantic notices and keep warning-specific treatment.

### Technical disclosure

- SCPF source is collapsed by default.
- SCPC source is collapsed by default when present.
- Generated SolidCraft commands are collapsed by default.
- Standalone section ordinals are not part of the presentation.
- Command-step numbering remains inside the expanded generated-command list.

### Build evidence

Build/provenance evidence is a quiet definition list:

- field name left;
- value right;
- subtle row separators;
- monospace only for technical identifiers;
- responsive one-column rows on narrow screens.

It is not a dashboard/card grid.

### Rich model content

The shared model template renders optional model-owned Background and
`extra_views` without model-slug-specific presentation branches.

External reference images may be mapped to a repository-owned/cache-owned local
copy when publication must not depend on a mutable third-party request. That
mapping is presentation data only and does not redefine model geometry or
verification state.

## Visual verification

The CAD repository owns the durable regression proof.

CI renders at least:

- Plate overview;
- Plate full page;
- Simple MFT overview;
- Simple MFT full page.

A headless Chrome/Chromium capture runs against the generated Hugo site before
publication. Screenshots are retained as workflow artifacts and missing local
rendered assets fail the proof.

The screenshots complement HTML/content assertions; they do not replace build
or provenance checks.

## Verification

Accepted production evidence:

- PR #290 repository-contract and CAD-CI validation passed in run #286
  (`45071139374`);
- PR #290 was squash-merged through the repository `/merge` policy into
  `dev-ci` at `74e46ea863cdd0a895cc80b175038c112e3025d4`;
- durable `dev-ci` run #287 (`45071251972`) completed successfully;
- the rendered-browser step captured and retained:
  - `plate-overview.png`;
  - `plate-full.png`;
  - `simple-mft-overview.png`;
  - `simple-mft-full.png`;
- visual artifact `model-layouts-dev-ci` (artifact 14772843173) was inspected
  after the durable build and matches the accepted calm hierarchy;
- `build/dev-ci` source-matches
  `74e46ea863cdd0a895cc80b175038c112e3025d4`;
- Pages `/dev-ci/` source-matches the same source commit and records build
  commit `e39f9bea675e6855af38280af16a9edfdf7bbdc1`;
- published Plate and Simple MFT HTML both contain the source/command
  disclosures and quiet provenance list, and neither contains the retired
  standalone section-index presentation;
- the published Simple MFT page retains its Reference and 2D expectation
  section.

The pre-change Pages state remains preserved at
`backup/gh-pages-before-278-2026-11-22`.

Do not port individual EXP CSS patches. The accepted unit is the generic
layout, content contract and rendered-browser proof together.
