# 0043 — SolidCraft STL publication

Issue: #345

## Problem

The CAD build already saves the accepted editable `model.sc`, exports STEP and
renders previews, but it does not publish an STL mesh. The earlier plan treated
this as a Forge capability gap.

That ownership was incorrect. The pinned SolidCraft 0.45.0 CLI can open the
saved design and export STL directly:

```sh
solidcraft-cli run --in model.sc --out model.stl --quality fine
```

Forge has already completed its job when the accepted `.sc` exists.

## Decision

The CAD model-build adapter exports `native/model.stl` directly from the
accepted saved SolidCraft design with the pinned runtime's CLI and `fine`
mesh quality.

STEP remains the interchange CAD export. STL is an additional printable/viewable
mesh artifact. There is no STEP-to-STL conversion and no Forge STL API in this
path.

The results site copies `model.stl` from the prepared durable build scope into
the model page bundle. When the resource exists, the Files panel exposes both a
download and a GitHub viewer link to:

```text
build/<scope>/models/<section>/<root>/models/<slug>/native/model.stl
```

The link uses the same published scope as the page. If STL is absent, neither
STL link is rendered.

## Contract

- `model.sc` remains the editable SolidCraft design.
- `model.step` remains the interchange CAD export.
- `model.stl` is generated from `model.sc` by SolidCraft itself.
- the STL must be non-empty for a successful processed model build;
- durable Pages publication requires the STL for the representative Plate
  model;
- no Forge/compiler or generic CAD-CI behavior is added for this export.

## Verification

- repository tests assert the direct `solidcraft-cli run --in ... --out
  model.stl --quality fine` path and required-output gate;
- site tests assert prepared-scope copying, conditional STL links and the
  scope-matched `build`-branch viewer URL;
- normal CAD CI performs the real SolidCraft export in the pinned 0.45.0
  runtime and must publish a non-empty `model.stl`.
