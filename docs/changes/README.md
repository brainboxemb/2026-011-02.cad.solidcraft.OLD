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

- [0024-retire-legacy-ci-python.md](0024-retire-legacy-ci-python.md) — remove superseded local CI/site orchestration after released dev-ci build/Pages acceptance (#174).
- [0025-shared-merge-policy.md](0025-shared-merge-policy.md) — consume the released tool.cad.ci merge policy instead of a CAD-local merge engine (#245).
- [0026-hextra-site.md](0026-hextra-site.md) — record Hugo 0.169.0 + Hextra v0.13.0 as the accepted CAD site architecture after #191 stable promotion (#251).

- [0027-calm-model-detail.md](0027-calm-model-detail.md) — adopt the EXP-proven calm generic model-detail layout and rendered-browser regression proof (#278).

- [0028-approved-framed-model-detail.md](0028-approved-framed-model-detail.md) — supersede the intermediate #278 redesign with the user-approved EXP #29 framed/source-first baseline.

- [0029-four-column-model-card-grid.md](0029-four-column-model-card-grid.md) — use one four/two/one model-card grid with bounded card text on Home and Models (#297).

- [0030-explicit-model-card-row-grid.md](0030-explicit-model-card-row-grid.md) — use explicit named card rows so one/two-line text cannot shift later content (#303).

- [0031-identical-catalog-card-geometry.md](0031-identical-catalog-card-geometry.md) — keep the section row on all catalog overview routes so category and all-model cards are identical (#316).

- [0035-selective-model-build-batch.md](0035-selective-model-build-batch.md) — make the shared SolidCraft batch honor CAD-CI direct-dependent model selection instead of rebuilding the full catalog (#335).

- [0037-development-lane-promotion-cadence.md](0037-development-lane-promotion-cadence.md) — let dev-cad/dev-ci accumulate work and promote only at deliberate stable checkpoints (#346).

- [0040-compact-model-detail-facts.md](0040-compact-model-detail-facts.md) — keep long model parameters out of the status badge row and render them as readable key-dimensions prose (#344).
- [0032-remove-local-cross-cad-references.md](0032-remove-local-cross-cad-references.md) — remove CadQuery/MicroCAD/PythonSCAD/vcad reference sources from the product CAD repository (#206).
- [0034-flex-bench-dog-mft-collar.md](0034-flex-bench-dog-mft-collar.md) — shape the FlexBenchDog stop collar as a Ø22 × 1.5 mm MFT seat with a 45° underside chamfer (#331).
- [0036-flex-bench-dog-cube-wireframe-logo.md](0036-flex-bench-dog-cube-wireframe-logo.md) — replace the filled top square with the nine-rib BrainBox cube wireframe construction (#332).
- [0038-flex-bench-dog-logo-polygon-ribs.md](0038-flex-bench-dog-logo-polygon-ribs.md) — isolate the nine BrainBox logo ribs into separate cuts; current Slot-per-Sketch construction is temporary pending Forge #747 (#332/#348).
- [0041-flex-bench-dog-rounded-slot-corners.md](0041-flex-bench-dog-rounded-slot-corners.md) — fillet the four vertical material corners around the FlexBenchDog central cross without changing slot dimensions (#333).
- [0042-corner-bracket-exact-geometry.md](0042-corner-bracket-exact-geometry.md) — restore the preserved arm-tip profile and exact four-part recessed M5 fixing-seat geometry in the shared CornerBracket (#8).
- [0043-solidcraft-stl-publication.md](0043-solidcraft-stl-publication.md) — export STL directly from the accepted saved SolidCraft design and publish the durable mesh/viewer link (#345).
- [0044-opt-in-stl-artifacts.md](0044-opt-in-stl-artifacts.md) — make STL export an explicit model-root artifact request instead of a universal CAD output (#403).
- [0045-temporary-hub75-panel-test-gate.md](0045-temporary-hub75-panel-test-gate.md) — make direct detailed-panel repository tests follow the temporary process gate for Forge #796 (#412).
- [0046-reenable-wooden-hub75-box.md](0046-reenable-wooden-hub75-box.md) — restore the existing WoodenHub75Box to the active SolidCraft build set on Forge v0.13.1 (#378).
