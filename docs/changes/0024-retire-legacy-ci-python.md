# 0024 — Retire legacy CAD CI Python orchestration

Issue: #174

## Problem

The released CAD-CI action, shared SolidCraft batch and Hugo/Blowfish Pages
path are accepted on `dev-ci`, but the repository still contained the old
Python planner, selector, native runner, build-store publisher and HTML
generator. Their tests and stale documentation made those files look like
active architecture and risked recreating a second CI framework.

The old pipeline also ran broad Python model regressions, so deleting it without
a replacement inside the released graph would lose useful coverage.

## Decision

- Generic planning, SCons execution, durable build scopes and Pages publication
  remain exclusively in released `tool.cad.ci` / `lib.py.cad.ci`.
- One declarative `ci/repository-tests` item runs retained Python regressions
  with the same shared Forge, SCPC and CAD-verification dependencies.
- Only narrow CAD-owned package/catalog/test/model-batch adapters remain below
  `scripts/ci/`; both that directory and every `ci/*` item are documented.
- The superseded local planner, selector, native wrapper, output store,
  publisher and Python HTML renderer are removed together with tests that only
  covered those retired implementations.
- Model semantic verification remains optional in `verification/verify.py`.
- Snapshot framing remains model-owned. Physical model-root `check.py` files
  contain only camera/extra-view presentation settings used by the shared
  builder.
- The obsolete `cad-ci` source checkout is removed from
  `dependencies.repos`; the workflow already pins the released action.

## Verification

The change is accepted when repository contract tests and
`ci/repository-tests` pass, model builds still use one shared SolidCraft
runtime, the workflow contains no retired orchestration reference, and durable
`dev-ci` build/Pages publication continues through released CAD-CI only.
