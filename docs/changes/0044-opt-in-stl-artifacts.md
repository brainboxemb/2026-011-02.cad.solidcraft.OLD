# 0044 — Opt-in STL artifacts

Issue: #403

## Problem

PR #401 proved that the pinned SolidCraft runtime can export a saved `.sc`
directly to STL, but it made that export mandatory for every processed model.
That wastes runtime and durable storage for models where a printable mesh is
not useful.

## Decision

STL is an optional model-root build artifact.

A model root requests it in its execution-owned `ci.yml`:

```yaml
artifacts:
  - stl
```

The default artifact list is empty. The CAD batch validates the list and
currently supports only `stl`.

This configuration stays out of `model.yml`: model.yml remains
catalog/presentation metadata, while ci.yml owns execution/output behavior.

Initially only `models/components/flex_bench_dog` requests STL.

## Runtime contract

For a root that requests `stl`, the runtime exports:

```sh
solidcraft-cli run --in model.sc --out model.stl --quality fine
```

and requires the resulting file to be non-empty.

For a root without the request, no STL command runs and `model.stl` is not a
required or published result.

The existing site remains resource-driven, so STL download/viewer links appear
only when `model.stl` is actually present in the accepted durable scope.

## Verification

- selection tests prove FlexBenchDog requests STL and Plate does not;
- batch/source tests prove STL export and required-output checks are
  conditional on the artifact request;
- durable Pages checks require FlexBenchDog STL and explicitly require Plate
  STL to be absent;
- no Forge or generic CAD-CI change is involved.
