# 0040 — Compact model-detail facts

Issue: #344

## Problem

`model.yml.parameters` is descriptive technical prose. The model-detail
template rendered it as a rounded status pill beside the SolidCraft status and
command count.

That worked for short values but made FlexBenchDog produce a very long blue
status badge, reducing scanability and making descriptive dimensions look like
build state.

## Decision

Keep `.cad-model-statusbar` for compact generated/status facts only:

- SolidCraft build/verification status;
- generated command count when available.

Render the model-owned `parameters` text below the normal model description
as `Key dimensions`. It remains visible near the preview but is ordinary
readable prose, not a status badge.

The rule is generic. There is no FlexBenchDog-specific template branch.

## Verification

Repository tests require the parameters value to be absent from the status-bar
markup and present in the preview content. Durable browser proof adds a
FlexBenchDog overview screenshot alongside the existing Plate and Simple MFT
captures so both short and long parameter text are visually covered.
