# 0022 — Reuse Hugo rather than build a CAD website engine

Issues: #191, #189 and #174.

## Problem

The accepted Python-catalog-to-model.yml migration in PR #190 corrected
**where** content lives, but not **how** the static website is generated.
`scripts/ci/build-results.py` still directly composes roughly 41 KB of
HTML in Python. The subsequent idea of wrapping those strings in a private
`string.Template` layer would amount to another bespoke static-site engine.

## Decision

Reuse **Hugo**, which is already deployed for the organization's Notes
website. Hugo owns content-to-page generation, layouts, partials, menus,
routing and static assets. Model content remains in local `model.yml`;
CAD-CI owns build evidence and durable Pages publishing. A narrow
evidence adapter may expose accepted model results to Hugo, but it must
neither generate HTML nor select/rebuild CAD models.

Hugo's built-in content adapters and data mounts are the preferred way
to create the 18 existing model routes from the 16 local model files.
Prove the exact tool version and variant handling before implementation.
The existing CAD CSS/HTML hierarchy, page design, routes and downloads
remain the acceptance reference; **do not transplant the Notes theme**.

## Cut-over gate

Do not remove the legacy generator or publish new main Pages until the
candidate has passed route, content, link, asset, provenance and visual
comparisons. Docs-only edits and metadata-only edits must not start
SolidCraft or rebuild the runtime container.

