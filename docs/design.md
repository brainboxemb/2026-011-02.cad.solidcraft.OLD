# CAD repository CI design

**Accepted architecture** — reuse the released generic CAD-CI mechanisms and
permanent branch topology, with only CAD-specific model producers, repository
contracts and site content remaining here. The legacy local generic pipeline
and Python HTML site renderer are retired.

## Reference stack

- CAD execution/publication and repository merge policy use released
  `tool.cad.ci 0.21.0` at exact commit
  `b1474f6be66dc0236f2a5c2555af07a100447255`;
- that tool revision pins `lib.py.cad.ci 0.11.1` at exact commit
  `fa6bf244381dde609a0b04de673d774911c52fea`;
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

**Accepted implementation:** released CAD-CI scans/plans one SCons
graph; `model-build-batch` launches the SolidCraft runtime once and model
items project their output with released `copy: dependency`. All sixteen
physical roots / eighteen catalog variants are active on the current Forge
v0.13.2 baseline. Repository regressions are one normal CAD-CI item, not a
separate orchestration layer.

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

The accepted public presentation layer uses Hugo **0.169.0** with Hextra **v0.13.0**.
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

### CAD catalog model-card contract

Home and `/models/` use the same model-card component and the same responsive
grid:

- desktop: four equal columns;
- medium/tablet: two columns;
- narrow/mobile: one column.

Do not add route-specific Home or Catalog column overrides.

The card component owns its text geometry through explicit named CSS-grid rows,
not flex-flow plus minimum/fixed element heights. The preview occupies a fixed
row; section, title, tagline and technical parameters each occupy explicit rows;
Home may additionally insert the Updated row. A flexible spacer precedes the
final status row. One-line content therefore cannot move any later row.

All catalog overview routes use the same section-bearing card geometry:
`/models/`, `/models/basic/`, `/models/components/` and
`/models/advanced/` all render the blue BASIC / COMPONENTS / ADVANCED row.
Do not hide that row only on `/models/`; doing so creates a second card geometry.

Home shows eight recently updated models so the four-column desktop layout
starts with two complete rows.

The durable browser proof captures Home, Models, Basic and Components overview
screenshots in addition to the representative model-detail screenshots.

### CAD model-detail presentation contract

The accepted model-detail presentation is the user-approved framed baseline from
`exp.2026-015.hugo-cad-site` issue #29 / PR #31.

Change 0028 supersedes the intermediate presentation decision in change 0027.

#### Framed hierarchy

Model-detail pages preserve the established framed panel hierarchy:

- compact build/status badges below the hero, limited to short build/verification state and generated command count; longer model parameter prose belongs with the model description as normal readable content, not in a status pill;
- Model preview and Files/Construction stages in the paired top panels;
- Open in SolidCraft Web in a framed panel;
- optional Background in a framed panel;
- optional reference/extra views in a framed panel;
- SCPF source in a framed code section;
- generated SolidCraft commands in a framed disclosure;
- optional SCPC comparison in a framed code section;
- build/verification evidence in a framed panel;
- source/downloads in a framed panel.

Do not replace this hierarchy with a free-form facts row or transparent
document-section treatment.

#### Section labels

Small blue labels give consistent hierarchy without standalone numeric section
markers:

- `SolidCraft model` → Open in SolidCraft Web;
- `Model context` → Background;
- `Design reference` → reference/extra-view title;
- `Source` → SCPF source;
- `Generated output` → SolidCraft command sequence;
- `Independent comparison` → SCPC command source;
- `Accepted build evidence` → Build and verification.

#### Source-first behavior

SCPF source is primary content and remains visible on initial page load. SCPC
source is also visible when present.

Generated SolidCraft commands are secondary generated evidence and remain
collapsed by default.

#### Typography and list rhythm

CAD prose uses the Segoe UI/system sans stack with body weight 400 and neutral
tracking. Headings use weight 600.

Background Markdown lists explicitly retain their list markers and use the CAD
accent color.

Construction stages intentionally use a tighter rhythm than ordinary prose:

- line-height `1.42`;
- item margin `0.12rem 0`.

The preview owns its own aspect ratio and is never sized from heading height.

#### SolidCraft version evidence

Each model provenance record contains the actual SolidCraft version exposed by
the immutable runtime through `SOLIDCRAFT_VERSION`.

The status badge uses that provenance value:

- verified build: `SolidCraft <version> · verified`;
- built without semantic verification: `Built in SolidCraft <version>`.

The Hugo template does not hardcode a SolidCraft version.

#### Rendered visual regression proof

The durable CAD build renders representative pages in headless Chrome before
Pages publication and retains:

- Plate overview;
- Plate full page;
- Simple MFT overview;
- Simple MFT full page.

Missing local assets fail the capture. Screenshots complement build/provenance
checks and must be visually reviewed for presentation changes.

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

The landing page's "Recently updated models" ordering is presentation data
derived from Git history, not model metadata. `scripts/ci/model_history.py`
writes one generated `site/data/cad/model_history.json` containing only the
source commit and physical model-root timestamps. The Hugo content adapter maps
each root timestamp to page `dates.lastmod`; variants owned by the same
physical root therefore share that timestamp. `model.yml` remains the sole
model-description/catalog source and must not gain a hand-maintained
`updated` field.

`model.yml` owns model/page metadata. Optional `page.md` owns additional
background/reference prose without redefining identity, build state or
verification facts. Build provenance, generated commands, saved SolidCraft output
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
