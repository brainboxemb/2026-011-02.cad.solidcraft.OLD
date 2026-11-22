# CAD repository CI design

**Target architecture** — same released mechanisms and branch topology as
`lib.py.solidcraft.forge`, with only CAD-specific producer and site content
remaining here. This document does not claim the old pipeline has already been
replaced.

## Reference stack

- `tool.cad.ci 0.17.0`:
  `d88d6e189c12edb5a30158c068145c099c17a019`;
- its exact `lib.py.cad.ci 0.9.3`:
  `74486c441f1f2b170ff3dc06e0edcaf662fbec6b`;
- central `cad-solidcraft:v0.3.4` (SolidCraft 0.45.0);
- Forge `v0.11.0` at exact source
  `9258d54079981604b6dd777a4c4face897c190fe`;
- released CAD verification package: exact dependency to be selected and
  owner-layer-qualified before cutover; do not build it into Docker.

The exact adopted moving pins will live in repository configuration, not be
duplicated in custom workflow branching logic.

## Technical pipeline

```text
PR or source-lane push
    -> thin workflow / Forge's exact tool.cad.ci root action
        -> released generic CAD-CI + one SCons graph
            -> root cad-ci.yml, model-root ci.yml
            -> checks for selected items
            -> CAD-owned Forge/SCPC producer(s)
            -> released CAD-verification runner
            -> model-local expected results
            -> build/<item>/.cad-ci + saved model + checks + screenshots

source-lane push only
    -> released build fetch/prepare/update/publish commands
    -> complete accepted build scope
    -> CAD site generator (read-only evidence consumer)
    -> released Pages publisher (scope-preserving)
```

The host launches the immutable SolidCraft runtime once per model-build
batch, not once per model item. Python dependencies and model-specific
scripts remain separate inputs. A change to a test or model does not rebuild a Docker image.

## Shared scan → plan → build execution

The accepted reference is Forge's `ci/model-verification-batch/ci.yml`,
`scripts/model_verification_batch.py` and the `copy: dependency` step in
`forge-model-declarative`. The CAD repository must follow that **existing
pattern**, not create its own selector, scheduler or per-model Docker runner.

```text
one Git/CAD-CI scan
    -> discover all model items from category globs
    -> released tool.cad.ci plans changed items and dependencies
    -> ONE SCons graph
        -> prepare pinned Forge, SCPC and verification packages once
        -> one model-build batch: gather commands before starting runtime
        -> one SolidCraft runtime startup for the batch
        -> build/check each selected model, keep per-model evidence
        -> model items copy their outputs from the batch dependency
    -> optional complete build/Pages publication from accepted results
```

The library remains the sole authority for `process`, changed-path
selection, dependency closure and target freshness. The CAD consumer may
provide a catalog-to-build-source adapter and per-model expected results,
but **not** a parallel planning mechanism or manually extended root item list.

### Efficiency and correctness acceptance

- Root `cad-ci.yml` uses generic discovery globs, not a list amended every
  time another model is migrated. Keep the existing 16 physical roots and 18
  catalog variants accounted for. Individual `ci.yml` files stay minimal.
- Do not start Docker in a model-item action. A shared batch prepares all
  selected commands and starts the released SolidCraft runtime **once** for
  that batch; the batch reports success/failure separately for each model.
- Model items use released CAD-CI `copy: dependency` to materialize their
  own outputs from the batch, as Forge does.
- Preserve the independent SCPC geometry comparison for the five applicable
  catalog variants; do not build its dependency wheel per model.
- Regular development PRs use the released selective planner. A full run
  is reserved for explicit full checks or promotion into `main`.
- Measure actual selected/build counts, single-pull/container-start count,
  runtime and stored evidence. Do not infer success from a green workflow
  without each model's own saved result.
- Forge's current batch has a granularity trade-off: an input change may
  invalidate the whole batch. Measure it; if per-model selectivity is needed,
  improve the **released generic ownership layer** first rather than
  embedding another change planner in CAD-specific Python.
- The site remains a separate consumer of complete build evidence; no
  redesign or URL change is authorized by this correction.

**Current dev-ci implementation:** released CAD-CI scans/plans one SCons
graph; `model-build-batch` launches the SolidCraft runtime once and model
items project their output with released `copy: dependency`. Fourteen
physical roots / sixteen variants are active. The two remaining advanced
assemblies are disabled only by Forge #679. Repository regressions are one
normal CAD-CI item, not a separate orchestration layer.

## Model item shape

Current repository discovery has **16** physical `models/**/ci.yml` roots.
The website/catalog has **18** model variants. Preserve that mapping; do not
create a second catalog just for generic CI.

Desired item contract:

```yaml
id: sample-plate
template: cad-model-build
process: true
# model-local source/tests/verification inputs plus declared cross-model needs
```

Root `cad-ci.yml` will hold the shared template and explicit runtime
variables; the exact template syntax must be validated against the released
tool/library contracts. A model-specific `verification/verify.py` is optional. Every processed model
must build successfully in SolidCraft and produce its saved design/build
artifacts; when useful semantic expectations exist, the released verification
library applies the local definition and writes separate verification evidence.
SCPC models keep an independent comparison and therefore require such a
semantic definition.

This is an illustrative contract, not a ready-to-run YAML drop-in. The
migration must test it against the pinned released stack before replacing
working model `ci.yml` steps.

## Pull request and promotion

```text
feature PR -> dev-cad       changed/dependency-selected checks; no generated writes
CI PR      -> dev-ci        changed/dependency-selected checks; no generated writes
dev-cad PR -> main          full processed model and infrastructure checks
dev-ci PR  -> main          full processed model and infrastructure checks
```

Permanent-lane promotion and stable-to-lane synchronization are normal merge
commits; short-lived work squashes. CAD consumes the same exact released
`tool.cad.ci` reusable merge-policy workflow as Forge and supplies only its
stable/lane refs, permanent generated refs, temporary cleanup prefixes and
`cad.yml` integration workflow. Merge mechanics, check filtering and branch
lifecycle are not reimplemented in this repository.

## Persistent branch output

```text
main push    -> run -> build/main    -> Pages /
dev-cad push -> run -> build/dev-cad -> Pages /dev-cad/
dev-ci push  -> run -> build/dev-ci  -> Pages /dev-ci/
```

On a named lane's first publication, prepare its complete item set.
On later pushes, use the last accepted `build/<lane>/build.json` source
commit as the incremental base. Do not derive this from `github.event.before`
for branch recreation. Publication uses released `update-main` or
`update-named`, source-SHA checks, branch-specific Pages output and bounded
non-force retry. Keep existing stable URLs during the cutover.

## Rebuild semantics

**The fact that a workflow succeeded does not establish that every model was
regenerated.** Build acceptance needs item-scoped evidence.

- Normal model edit: selected model, declared dependants, or relevant shared
  items; unchanged accepted output may be reused when signatures match.
- Forge/SCPC/native-verification or runtime version change: those exact pins
  must be declared as model inputs/dependencies; affected models are
  re-executed rather than silently inheriting old evidence.
- Development-lane to main promotion and deliberate toolchain-wide acceptance:
  run all processed items and check actual executed/native artifacts.
- Pages-only edit: rebuild site, not geometry, from the accepted complete scope.

An explicit full run must actually execute all model steps whose native
evidence is missing or invalid for that toolchain. A full *selection* alone
cannot be used to claim execution if SCons reused valid results.

## Website preservation boundary

The CAD website uses Hugo **0.169.0** with Hextra **v0.13.0** as the shared
documentation shell. The repository retains its own CAD presentation in
`site/assets/css/custom.css`; it does not adopt Forge's renderer or copy
Forge's page templates. `site/results.css` is retained only as a historical
pre-Hugo comparison baseline and is not a second active style authority.

Hugo reads local `model.yml` files directly for model content and reads
accepted build/verification results only from the prepared complete build
scope. Existing model routes at `/models/<slug>/` remain the public contract.

### CAD visual component contract

Model-detail pages use a small semantic presentation system:

- **standard content panel** — neutral 1 px border, common radius/padding,
  no accent edge; used for ordinary grouped content such as Preview, Files,
  Background and Verification;
- **primary action panel** — the same standard panel with one blue accent line
  at the **top**; reserved for the user-facing `Open in SolidCraft Web`
  action;
- **semantic notice/warning** — a left accent edge is reserved for notice or
  warning semantics; warnings use the red warning color;
- **code/generated-output section** — no white outer panel; heading and helper
  text lead directly to the dark code surface, and generated commands may use
  the native collapsed disclosure.

Accent-edge direction therefore has meaning: normal content never gains a blue
left or top edge merely for decoration.

CAD prose uses the accepted sans-serif CAD typography with normal body weight
and neutral tracking. Ordinary panel/section headings use medium weight and
neutral tracking. Markdown-rendered Background content must follow the same
CAD typography rather than reverting to Hextra prose styling.

Regression checks compare representative basic, component and advanced model
pages, including desktop/narrow layouts, source/command blocks, preview/files,
Background, verification and downloads. Retained screenshots must never be
presented as newly verified output.

## Retirement boundary

Currently the CAD repository still has local orchestration in
`build_plan.py`, `select_models.py`, `pipeline_ci.py`, `cad_ci.py`,
`native_ci.py` and `publish_ci.py`. Model-specific build adapters remain. The custom Python site renderer does
not: after the accepted Hugo/Hextra cut-over it was removed with the obsolete
planner/runtime/publisher code.

No rewrite of the CAD website's layout or content is authorized merely to
match Forge's CI design.

## Website data flow: model.yml → validated catalog → shared renderer

The original CAD website was generated directly from an approximately
28 KB handwritten Python `MODELS` dictionary. Forge already uses
`examples/<model>/model.yml` for model titles, descriptions and stages.

The CAD version is:

```text
models/<category>/<root>/model.yml  (source of website model content)
models/<category>/<root>/ci.yml     (build identity and participation)
models/<category>/<root>/verification/verify.py (optional semantic expectations)
        |
        v
scripts/ci/model_catalog.py (load/validate; no hard-coded model list)
        |
        +-- existing build selectors / model dependencies (compatible API)
        +-- site/content/models/_content.gotmpl
        +-- site/layouts/models/* + Hextra
                |
                v
homepage + category pages + /models/<slug>/ + model/build downloads
```

A model's optional `extra_views` declaration contains a title, a
caption, and view items of kinds `url` (external HTTPS reference),
`asset` (checked-in model asset), or `build` (saved SolidCraft
screenshot). The shared renderer checks availability and verification,
copies assets, and uses the original `panel-views` layout. No model slug
should appear in dedicated view-generation conditionals.

The loader verifies local source paths, section, page ordering, duplicate
YAML keys, optional SCPC/component sources, referenced CAD dependencies,
required public text, and multi-variant ownership. Source SHA/verification
evidence is **not** inferred from YAML. The existing geometry-only
fingerprint excludes `model.yml`, while site selection includes it.

The site stays static HTML/CSS. PyYAML is a **build-time dependency**,
not a browser dependency or a new general-purpose CI subsystem. Accepted
Pages baselines must be compared before any public cut-over.

