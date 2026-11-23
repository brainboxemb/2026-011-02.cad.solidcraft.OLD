# Change 0045 — temporary hub75-panel repository-test gate

Issue: #412

## Problem

CAD #408 temporarily sets the detailed `hub75-panel` model root to
`process: false` because Forge #796 breaks symbolic placed-Cylinder anchor
arithmetic on Forge v0.13.1.

The shared CAD model-build batch respects that process gate, but
`tests/test_hub75_panel.py` directly compiles the detailed model in several
repository tests. Those tests therefore still execute the intentionally
disabled model and block Forge v0.13.1 adoption.

## Decision

Repository tests that require direct compilation of the detailed
`hub75-panel` root derive their temporary skip state from that root's existing
`ci.yml process` value.

Static/source tests, HUB75 screen tests and generic component-copy tests remain
active.

There is no second release/version switch and no exception handling in model
source. When `process: true` is restored, the gated tests run automatically
again.

## Verification

- repository-contract tests remain green;
- with `hub75-panel process: false`, only direct detailed-panel compilation
  tests are skipped;
- all other HUB75-panel test coverage remains active;
- removing the process gate restores the tests without another code change;
- Forge #796 remains the owner of the compiler defect.
