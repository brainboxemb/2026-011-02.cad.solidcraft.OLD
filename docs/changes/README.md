# Change design records

Structural CAD-library changes are recorded here before or together with implementation.

Naming:

```text
NNNN-short-change-name.md
```

Rules:

- four-digit, monotonically increasing number;
- one design/change per document;
- link the matching GitHub issue;
- describe the problem, decision, repository/API/CI contract and verification;
- implementation follows the recorded decision;
- later changes add a new record instead of rewriting an older decision.

Current records:

- [0001-targeted-model-builds.md](0001-targeted-model-builds.md) — targeted model selection, per-model verified output and incremental publication (#129).
- [0002-tested-ci-orchestration.md](0002-tested-ci-orchestration.md) — move selection, model checks and publication policy out of workflow YAML into tested Python (#134).
- [0003-reusable-cad-ci-image.md](0003-reusable-cad-ci-image.md) — build and reuse one immutable CAD/SolidCraft/SCPF/SCPC CI toolchain image (#136).
- [0004-concurrent-generated-publication.md](0004-concurrent-generated-publication.md) — retry generated-branch publication safely when CAD cleanup or promotion races (#138).
- [0005-host-owned-stable-pages-workspace.md](0005-host-owned-stable-pages-workspace.md) — build/test stable Pages in a host-owned temporary workspace (#139).
- [0006-canonical-native-screenshot-filename.md](0006-canonical-native-screenshot-filename.md) — normalize migrated primary screenshots to `native/model.png` before stable Pages generation (#140).
- [0007-parallel-hub75-display2.md](0007-parallel-hub75-display2.md) — add HUB75Display2 as a separately evolvable advanced model alongside the existing wooden display (#142).
- [0008-model-root-input-selection.md](0008-model-root-input-selection.md) — select model-root README/check metadata without propagating it through geometry dependencies (#144).
- [0009-model-page-warnings.md](0009-model-page-warnings.md) — render optional model-specific warnings from catalog metadata on result pages (#147).
- [0010-stable-catalog-growth.md](0010-stable-catalog-growth.md) — support adding a new catalog model to an existing modern stable build (#150).
- [0011-native-verification-status.md](0011-native-verification-status.md) — separate geometry verification fingerprints from page metadata and explain public verification states (#152).
- [0012-tool-cad-ci-migration.md](0012-tool-cad-ci-migration.md) — migrate generic CAD CI planning, build-store and Pages lifecycle to released `tool.cad.ci` (#155).
- [0013-tool-cad-ci-native-packaging.md](0013-tool-cad-ci-native-packaging.md) — package verified native results inside model-root tool.cad.ci items.
- [0014-tool-cad-ci-publication.md](0014-tool-cad-ci-publication.md) — move durable build and Pages publication to tool.cad.ci.
- [0015-remove-legacy-publication.md](0015-remove-legacy-publication.md) — remove superseded CAD publication/store code after the cutover.
- [0016-central-solidcraft-runtime.md](0016-central-solidcraft-runtime.md) — reuse the released central SolidCraft runtime instead of a consumer-owned Docker image (#170).
- [0017-forge-011-solidcraft-045.md](0017-forge-011-solidcraft-045.md) — adopt released Forge 0.11.0 and central SolidCraft 0.45.0 in CAD verification (#172).

- [0018-forge-ci-parity.md](0018-forge-ci-parity.md) — migrate CAD CI to Forge's released tooling, source lanes and generated scopes (#174).

- [0019-shared-build-batch.md](0019-shared-build-batch.md) — Forge-compatible shared model-build batch; one runtime start (#174).

- [0020-component-model-builds.md](0020-component-model-builds.md) — shared SolidCraft build for GuideRail variants and FlexBenchDog (#174).

- [0021-model-metadata.md](0021-model-metadata.md) — local model.yml drives CAD website metadata and views (#189).

- [0022-build-vs-semantic-verification.md](0022-build-vs-semantic-verification.md) — require real model builds while keeping semantic verification optional (#174).

- [0023-hugo-blowfish-site.md](0023-hugo-blowfish-site.md) — direct model.yml → Hugo/Blowfish site generation with prepared CAD-CI evidence (#191, #174).
