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

The accepted public presentation layer is **Hugo 0.169.0 + Hextra v0.13.0**.
Hextra supplies the common documentation shell and theme primitives. The CAD
repository owns its product-specific page composition, navigation choices,
layouts/partials and engineering visual treatment.

Active styling is maintained in `site/assets/css/custom.css`.
`site/results.css` is retained only as the pre-Hugo visual comparison
baseline and is not loaded as the current styling contract.

Existing model pages at `/models/<slug>/` keep the accepted information
hierarchy: identity/status, preview and files, construction stages, SCPF source,
generated SolidCraft commands, optional SCPC comparison, SolidCraft Web/native
actions, verification/provenance and optional background/reference content.
The homepage and Basic / Components / Advanced category routes remain stable.

Forge's site renderer is not adopted merely because Forge and CAD share
infrastructure. A deliberate public-site redesign is separate product work and
must not be hidden inside CI, metadata or evidence changes.

## Retirement boundary

The legacy custom Python HTML generator and the old CAD-local generic
planner/selector/build-store/publisher are retired. Generic planning, SCons
execution, durable build-scope handling and Pages publication belong to the
released CAD-CI stack.

This repository retains only CAD-owned responsibilities such as model source,
model-local expectations/adapters, catalog validation, model presentation data,
Hugo layouts/content and CAD-specific styling. Do not restore complete page
HTML in Python strings or create a second site renderer beside Hugo.

## Website data flow: model.yml -> Hugo/Hextra -> Pages

The accepted site data flow is:

```text
models/<category>/<root>/model.yml
models/<category>/<root>/page.md                 (optional)
accepted prepared build-scope evidence
        |
        v
scripts/ci/model_catalog.py                      (load/validate; no second catalog)
        |
        v
Hugo 0.169.0 content adapter + CAD layouts/partials
Hextra v0.13.0 + site/assets/css/custom.css
        |
        v
homepage + category pages + /models/<slug>/ + downloads/actions
        |
        v
released CAD-CI Pages publisher
```

`model.yml` owns model/page metadata. Optional `page.md` owns additional
background/reference prose without redefining identity, build state or
verification facts. Build provenance, generated commands, saved native output
and verification state come only from the accepted prepared build scope.

A model's optional supplementary views remain declarative model metadata and
are rendered generically. Shared Hugo code must not grow model-slug-specific
branches for normal model presentation.

The catalog loader validates local source paths, ordering, duplicate YAML keys,
optional SCPC/component sources, declared dependencies and multi-variant
ownership. It does not infer source SHA or verification state from YAML.

Presentation-only metadata/content changes must not invalidate unchanged
SolidCraft geometry. They may select a site refresh while the accepted CAD
output is reused. The final Pages provenance must still identify the exact
source lane and source commit that produced the published site.

Historical change record `0023-hugo-blowfish-site.md` remains historical
evidence of the earlier Hugo/Blowfish migration stage; the accepted Hextra
architecture is recorded by change record 0026.
