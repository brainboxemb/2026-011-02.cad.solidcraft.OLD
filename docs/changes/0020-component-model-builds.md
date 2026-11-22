# 0020 — Build the reusable component variants through the shared batch

Issue #174. Builds on the accepted one-runtime architecture from PR #184.

## Scope

Enable the FlexBenchDog and GuideRail physical model roots. Their local
`ci.yml` files retain only id, shared template and process.

GuideRail owns **two** catalog variants (Festool and Makita), each with its
own model-local dimensions and body volume. The reference values come from
the previous accepted SolidCraft measurements and are not official
manufacturer specifications. FlexBenchDog has a separate SCPC command source
that must build and match the Forge-produced SolidCraft model.

## Verification gate

11 physical model roots (12 variants) must pass in one shared batch and
produce editable SolidCraft files, STEP, images and checked geometry. The
five remaining physical model roots stay disabled. There is no new generic
selector, per-model Docker startup, website redesign or Pages publication.

All checks must pass before this PR can be merged into `dev-ci`.
