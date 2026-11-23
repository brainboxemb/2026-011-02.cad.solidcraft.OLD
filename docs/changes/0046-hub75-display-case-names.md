# Change 0046 — align HUB75 display-case product names

Issue: #416

## Decision

Use one product family name for the two current wooden HUB75 enclosure models:

- v1 product title and top-level class: `Hub75DisplayCase`;
- v2 product title: `Hub75DisplayCase v2`;
- v2 top-level class: `Hub75DisplayCaseV2`.

These names describe the models as display cases rather than generic boxes and
make the v1/v2 relationship explicit.

## Compatibility boundary

This change deliberately keeps repository-facing identifiers stable:

- `models/advanced/hub75_wood_frame/` / `hub75-wood-frame`;
- `models/advanced/hub75-display2/` / `hub75-display2`.

CAD #417 owns the later path/model-id/public-slug migration together with the
required URL compatibility/redirect contract.

## Scope

- rename product titles, top-level classes and active model-owned documentation;
- update direct tests and parameter-override entrypoints that name the classes;
- no geometry, parameter, placement, process-gate, path, id or slug change.

## Verification

- default and parameter-override model compilation still uses the same geometry;
- v1/v2 class-name contracts match the new product family;
- normal repository/CAD validation remains green.
