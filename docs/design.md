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

**Current implementation is not accepted as the target.** On `dev-ci`
the present `cad-model-build` runs `scripts/ci/model_verify.py` once per
model, doing a `docker pull` and `docker run` for every model. The
development PR also uses `full_run: true`, and root `cad-ci.yml` grows
one manual item path at a time. These choices are a performance and
ownership regression compared with Forge and must be replaced before
onboarding the remaining models.

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

Source promotions are made as normal merge commits; feature PRs squash.
Reuse Forge's owner-controlled merge-policy structure, adjusted only for this
repository and with a rule against deleting long-lived lanes.

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

Unlike the generic CI, the CAD website is **not** being migrated to Forge's
site design. Keep the existing `scripts/ci/build-results.py`,
`site/results.css` and model catalog as the baseline presentation, adapting
only their input-reading boundary to the prepared complete build scope.

In particular, existing model pages at `/models/<slug>/` must continue
to show their own title, explanation, construction stages, source and
commands, visual preview, verification status and relevant downloads. Keep
home and category pages, their navigation, and the established Basic /
Components / Advanced grouping.

During the transition, generate an old-site baseline and a new-site candidate
from equivalent accepted CAD output, then compare:

1. Homepage and the three category index pages, including CSS/layout and
   navigation on desktop and narrow screens.
2. A basic model, a complex HUB75 assembly and a model with an independent
   SCPC source, including preview images, commands, source links and
   downloads.
3. All existing `/models/<slug>/` routes and internal links, with the
   current model catalog as the route authority.
4. Correct source/version/status information; retained old screenshots must
   not be presented as newly verified output.

Keep changes to the page's composition minimal. If the new evidence format
cannot be rendered without a visible layout change, treat that as an explicit
migration blocker instead of silently redesigning the site.

## Retirement boundary

Currently the CAD repository still has local orchestration in
`build_plan.py`, `select_models.py`, `pipeline_ci.py`, `cad_ci.py`,
`native_ci.py` and `publish_ci.py`. Model-specific tools and the site
generator can remain, but generic planner/runtime/publisher behavior must
be retired only after the released replacements are proven.

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
        +-- scripts/ci/build-results.py (one static page template + views)
                |
                v
homepage + category pages + /models/<slug>/ + model.yml downloads
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

