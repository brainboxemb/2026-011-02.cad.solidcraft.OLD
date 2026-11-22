# 0023 — Hugo + Blowfish CAD site

Issues: #191, #174

## Problem

Local `model.yml` fixed metadata ownership, but complete Pages were still
assembled by a large custom Python HTML generator. The CI migration needs a
presentation layer that consumes accepted build evidence without becoming a
second CAD runner, selector or publisher.

## Decision

Use Hugo 0.169.0 with Blowfish v3.10.0.

- Hugo mounts only model-owned `model.yml` into its data tree.
- `content/models/_content.gotmpl` creates all 18 model routes.
- Multi-variant roots remain one physical metadata file.
- The exact prepared CAD-CI scope is mounted read-only under Hugo assets.
- Missing evidence renders as missing/pending and is never inferred.
- CAD owns a small set of catalogue/model templates and CSS; Blowfish owns the
  generic theme shell.
- `cad_ci_tool publish pages` remains the only durable Pages writer.
- `/dev-ci/` is accepted before changing the stable root.

There is no generated Markdown catalogue and no Python HTML renderer in the
target architecture.

## Evidence

The isolated `exp.2026-015.hugo-cad-site` build used the real CAD metadata,
produced 32 Hugo pages, and passed ordinary/multi-variant/warning/
supplementary-view route checks.

## Acceptance

The CAD dev-ci integration must prove the existing model/category routes,
accepted model images and downloads, truthful build/verification labels, and
source/build provenance. Once accepted, the obsolete Python renderer is
removed rather than retained as a second site engine.
