
> **Website- en modelgegevens (CAD #189):** volg Forge's
> `examples/*/model.yml`: in CAD staat de bron voor elke titel,
> omschrijving, parameteruitleg, bouwstap, waarschuwing, bron-/variantrelatie
> en extra afbeelding naast het model in `models/<groep>/<model>/model.yml`.
> De Python `model_catalog.py` is uitsluitend een lezer/validator.
> Hugo + Hextra onder `site/` leest dezelfde `model.yml` direct via een
> content adapter; voeg geen gegenereerde Markdown-catalogus of Python
> HTML-renderer toe.
> `ci.yml` is alleen voor uitvoering; `verification/verify.py` is optioneel en
> alleen voor zinvolle geometrische/semantische controles. Een model moet wel
> echt in SolidCraft bouwen; voeg geen kunstmatige verificatie toe om CI groen
> te krijgen. Voeg niet opnieuw een Python-dictionary met
> modelbeschrijvingen of model-specifieke HTML-condities toe. Bewaak de
> huidige website en URLs; wijzig metadata zonder geometrische herbouw.
>
# CAD repository instructions

> **Active CI architecture (issue #174):** the repository uses the exact
> released `tool.cad.ci` action, one SCons graph, one shared SolidCraft
> model-build batch and Hugo/Hextra publication from prepared durable scopes.
> `build/main`, `build/dev-cad`, `build/dev-ci` and their matching Pages scopes
> are source-lane-owned. Do not recreate the retired local planner, selector,
> build store, publisher or Python HTML generator.
>
> **Model build gate:** 14 physical roots / 16 variants currently build in the
> shared runtime. `hub75-display2` and `hub75-wood-frame` stay disabled only
> for Forge #679. Do not add CAD-local naming workarounds. Semantic
> `verification/verify.py` is optional; a processed model must at least build
> and produce the required saved outputs.
>
> **Generic CAD-CI requests go through Forge first:** track the common
> scan/plan/build-batch requirement under
> `brainboxemb/lib.py.solidcraft.forge#661`. Forge decides shared behavior
> and acceptance; the generic CI owner implements/releases it; Forge
> qualifies the release; only then does this repository adopt it. Do not
> change `lib.py.cad.ci` directly as a workaround for this CAD repository,
> and do not create another CI planner here.
>
This repository contains product and project CAD models built with SCPF/SCPC.
Forge itself belongs in `brainboxemb/lib.py.solidcraft.forge`; do not work
around a Forge API/compiler problem in a product model.

## Handoff

The canonical session handoff is `docs/handoff.md`, following the shared
`brainboxemb/meta.cad.solidcraft/templates/docs/handoff.md` structure.
Treat it only as an entrypoint: inspect current GitHub state, then read
`AGENTS.md` and `docs/plan.md`. Keep volatile SHAs, release/runtime pins and
active issue/PR state in the plan/GitHub rather than duplicating them in the
handoff.

## Development-lane cadence

`dev-cad` and `dev-ci` are working/integration lanes. They may accumulate
multiple accepted logical changes while related work continues. Do not promote
an accepted development PR to `main` merely because it is green.

Promote a development lane to `main` only at a deliberate stable checkpoint,
such as a coherent feature set, the end of a work block/day, a release point,
or when another lane genuinely needs that stable change. Keep the normal
history-preserving permanent-lane merge rules when that checkpoint is chosen.

Pure repository-instruction and documentation-only corrections in
`AGENTS.md` and `docs/*` may be committed directly to `main` when they do
not depend on an unmerged code/model change. Documentation that is part of a
logical code/model change stays with that issue, branch and PR.

Synchronize `main` back into `dev-cad` or `dev-ci` when the stable change
is actually needed there; do not perform a synchronization cycle as a ritual
after every development merge.

## Write simply

Use normal engineering language. Use the names that exist in the code and in
SolidCraft. Avoid architecture jargon and invented terms.

## Model naming and scope

- Put reusable physical parts in `models/components/<name>/`.
- Put complete designs and assemblies in `models/advanced/<name>/`.
- Put small standalone examples in `models/basic/<name>/`.
- Prefer generic component names when the geometry represents a generic part.
  Brand names belong in the source/reference documentation when appropriate.
- A component owns its local geometry. The assembly owns placement.
- Lower-case class attributes are editable native CAD parameters.
- UPPER_CASE values are fixed model constants.
- A leading underscore is a Forge/build-time input, not a native parameter.

Do not commit third-party STEP/STL/CAD reference files unless their licence and
project need explicitly require it. Prefer source links and reproduce only the
geometry needed by our own model.

## Change records

For structural library, public-model API, CI/publication or reusable-component
behavior changes, create the GitHub issue and the numbered
`docs/changes/NNNN-short-name.md` record before implementation.

- Use the next four-digit number from `docs/changes/README.md`.
- One record describes one design decision and links its issue.
- Record the problem, decision/contract and verification.
- Update the index in the same change.
- Do not use `CHANGELOG.md` as a substitute for the design/change record.
- Small content-only documentation corrections that do not change a repository
  contract do not need a new numbered record.

## Add a new model

A new model is not complete when only `model.py` exists. Check every item
below before opening or merging the PR.

1. **Source**
   - Add the SCPF source under the correct `models/.../<name>/scpf/model.py`.
   - Add a README when dimensions, source measurements, assumptions or scope
     need explanation.
   - Keep the model small enough to understand from its own source.

2. **Model metadata**
   - Add or update `models/<group>/<model>/model.yml`.
   - Put title, description, parameters, stages, warnings, source relations,
     variants and presentation-only extra views there.
   - `scripts/ci/model_catalog.py` only validates/normalizes these files for
     CAD-side consumers; do not add a second handwritten model list.

3. **Regression tests**
   - Add a focused test file under `tests/` for the important geometry and
     parameter behaviour.
   - For reusable components, include the class/path in
     `tests/test_cad_models.py:test_reusable_component_sources_own_component_decorator`.
   - Test dimensions and relationships from generated commands; do not merely
     assert that constants exist in the source.

4. **Normal CAD CI**
   - Models are compiled from the central catalog; do not add a slug to the
     workflow YAML.
   - The normal model regression and static-site smoke tests must pass.

5. **SolidCraft build and optional semantic verification**
   - Every processed model must build in the shared SolidCraft batch and
     produce its required saved model, STEP and preview outputs.
   - Add `verification/verify.py` only when a stable physical/semantic
     expectation is useful; do not invent checks merely to satisfy CI.
   - Optional snapshot camera and extra-view settings belong in the physical
     model-root `check.py`; verification logic does not.
   - Do not add model semantics or per-model execution loops to workflow YAML.

6. **Results site**
   - Site title, description, parameters, stages and section belong in local
     `model.yml`.
   - Hugo creates `/models/<slug>/` from
     `site/content/models/_content.gotmpl`.
   - Accepted build evidence is read-only input from the prepared
     `tool.cad.ci` scope; missing evidence must remain missing/pending.
   - Keep presentation in Hugo/Hextra layouts and CAD-owned CSS, not Python HTML.

7. **Repository model index**
   - Add a concise entry to `models/README.md` when the model is a reusable
     component or an important advanced model.

8. **Finish**
   - Run/inspect both the ordinary CAD CI and native SolidCraft CI.
   - Do not call the model complete while one of those checks is failing.
   - Keep one logical model change in one branch/PR.

## Targeted CI and publication

Build selection, tool versions and publication state are separate concerns.

### Reuse the released central SolidCraft runtime

Normal CAD CI uses the released runtime owned by
`brainboxemb/docker.cad.solidcraft`.

- This repository does not own a Dockerfile or image-build workflow.
- `ci/toolchain.json` pins one immutable
  `ghcr.io/brainboxemb/cad-solidcraft:vX.Y.Z` release and its expected
  SolidCraft version.
- SCPF and SCPC remain exact consumer pins in `dependencies.repos`; CI checks
  those sources out under `ext/` and exposes them to the container through
  `PYTHONPATH`.
- A Forge or Commands pin change must not rebuild the central runtime.
- A SolidCraft/runtime dependency change is made in
  `docker.cad.solidcraft`, released there, then adopted here by changing the
  immutable runtime pin.
- Do not use mutable runtime tags such as `:edge` or `:latest` for
  qualification.
- Record the central runtime reference plus exact SCPF, SCPC and SolidCraft
  versions in each model's verification metadata.
- Model selection and runtime selection remain independent. Use explicit
  `all` mode only when the complete model library is deliberately qualified.

### Select only the models that need work

- Normal model work uses targeted builds. A change to one model should compile,
  test and native-build that model only.
- Model/item selection and dependency closure come from released CAD-CI using
  `cad-ci.yml` + item `ci.yml`; do not reimplement them in CAD Python or
  workflow YAML.
- Shared component dependencies must be declared in the catalog so a component
  change selects its actual dependants.
- Adding a new model should normally build only that model.
- Changing `dependencies.repos` or the configured SolidCraft version does not
  automatically mean "build the whole catalog".
- Use an explicit full-build mode when deliberately testing every model against
  a new Forge revision/release or SolidCraft version.
- Keep explicit modes for changed models, named model(s), and all models.
- Keep **selection inputs** separate from **native verification inputs**:
  `model_input_paths()` may include model-root README/check metadata so those
  changes select the owning model/page, while `verification_input_paths()`
  contains only geometry/source inputs and declared geometry dependencies.
  Documentation/site metadata must never invalidate an unchanged native CAD
  verification. A `check.py` change still selects and reruns its model.
- Public verification wording must be literal:
  **Native verified** means a real SolidCraft `.sc` exists and its stored
  verification fingerprint matches the current geometry/source inputs.
  An older retained screenshot must be labelled as an older render that is not
  current verification; a command-only model must say native output is not
  verified. SolidCraft Web links and `.sc` downloads are user actions, not
  evidence of verification.

### Keep build output separate from Pages

Use `build` as the durable store of verified model build results.
The build item path is the catalog source-file path without the `.py` suffix.
This makes every item unique and prevents one item directory from being the
parent of another. Do not flatten model output to a slug-only directory.
`gh-pages` is generated publication output, not the source of truth for CAD
verification.

The output branch has two states:

- `pr/<number>/<model-root>/` for branch/PR staging output;
- `main/<model-root>/` for accepted output from a successful `main` build.

Each model output directory contains its own `verification.json` with the CAD
source commit, Forge revision/release, SolidCraft version, workflow run and
native file format that actually produced that model.

The canonical primary native screenshot is `native/model.png`. Legacy
`native/native.png` must be normalized during migration/publication rather
than supported as a second permanent site input. Extra views such as
`front.png` and `rear.png` keep their model-specific names.

Do not describe an unchanged model as verified against a newer Forge,
SolidCraft or CAD revision merely because another model was rebuilt.

### Preview/staging rules

- Every PR/branch writes only to its own preview namespace.
- A preview must never overwrite `build/main/`.
- Build and validate candidate output before publishing the preview.
- Preview Pages are generated from the branch catalog/source, that preview's
  freshly built models and stable output for unchanged models where needed.
- A failed preview build must not replace the previous preview or any stable
  output.
- Preview namespaces may be cleaned up after a PR closes or merges.

### Stable promotion rules

- Only a successful accepted `main` build may update stable model output.
- Build selected models into a temporary/candidate directory first.
- Run all selected-model checks against that candidate.
- Only after every required check is green, replace those selected model
  directories in `build/main/`.
- Preserve every unchanged stable model directory byte-for-byte.
- Regenerate the stable site from the current catalog plus the complete stable
  output set and publish that assembled site to the root of `gh-pages`.
- A failed main build must never partially update stable output or the stable
  Pages root.
- `build` and `gh-pages` may have legitimate concurrent writers, such as
  stable promotion and closed-PR cleanup. Publish with normal non-force pushes;
  on a non-fast-forward, fetch the target branch, rebase the prepared generated
  commit, and retry a bounded number of times. Never force-push generated
  branches or discard the other writer's change.
- Docker CAD output and host publication have different ownership boundaries.
  Stable Pages must be built and tested in a host-owned temporary directory,
  not below the container-owned `output/` tree. Do not repair this with broad
  chmod/chown operations.

### Site/catalog scaling

- Model pages stay at `/models/<slug>/`.
- Generate category pages from the central catalog, for example
  `/models/basic/`, `/models/components/` and `/models/advanced/`.
- The home page is a compact view of the six most recently changed model
  roots, derived from Git history at site-build time.
- Do not maintain a second hand-written home-page list or a hand-maintained
  `updated` field in `model.yml`.
- Category pages, home page and navigation may be regenerated cheaply even when
  no model geometry needs rebuilding.

See issue #129 for the current CI/publication implementation work.

## When a model exposes a Forge problem

Do not add a CAD-specific workaround just to get the model green.

1. Confirm the expected behaviour from the current Forge API/docs.
2. Reproduce the problem with the smallest useful Forge unit test.
3. Fix Forge in its own issue/PR.
4. Cover sibling API variants when the same underlying behaviour applies.
5. Merge the Forge fix through its normal CI.
6. Pin the CAD repository to the exact qualified Forge commit when the fix has
   not yet reached a normal release.
7. Re-run the downstream CAD native verification.

A downstream product model is evidence for a Forge bug, not the place where the
Forge bug should be hidden.

## Workflow structure

Expose one normal user-facing workflow:

- `cad.yml` — the complete CAD pipeline: select, cheap checks, native checks,
  candidate build, preview/stable publication and closed-PR cleanup.

The SolidCraft image is built and released only in
`brainboxemb/docker.cad.solidcraft`. This consumer repository must not add a
local image-build workflow. Do not split normal CAD operation into separate
native, publish or cleanup workflows merely because those are separate
implementation phases.

Workflow YAML owns triggers, permissions and the thin released-action/Hugo
handoff. Released CAD-CI owns generic checkout, selection, dependency closure,
SCons execution and durable publication. CAD Python below `scripts/ci/` is
limited to the adapters documented in `scripts/ci/README.md`.

The normal development flow is:

`source change -> released CAD-CI plan/SCons -> repository tests + shared model batch -> durable build scope -> Hugo -> released Pages publisher`

A deliberate full-library run uses the same commands with explicit `all`
selection; it is not a separate CI implementation.

## Merge policy

The repository needs both squash merges and normal merge commits, so the
GitHub merge method must not be chosen manually. Use the owner-only
`/merge` comment on the pull request.

Merge mechanics and branch lifecycle are owned by released `tool.cad.ci`.
`.github/workflows/merge-policy.yml` is only a thin caller of the exact
externally accepted reusable merge-policy workflow. Do not add a CAD-local
merge decision table or GitHub merge implementation.

Configured repository policy:

- short-lived feature/fix/documentation/CI branches: **squash merge**;
- exact `dev-cad -> main` and `dev-ci -> main`: **normal merge commit**;
- exact `main -> dev-cad` and `main -> dev-ci`: **normal history-preserving
  synchronization**;
- promoted long-lived lanes are retained/advanced by the shared policy;
- only allow-listed short-lived branch prefixes may be deleted after merge;
- `main`, `dev-cad`, `dev-ci`, `build`, `gh-pages` and backup refs are never
  cleanup targets.

The shared policy requires the exact current PR-head validation to be green and
filters its own issue-comment command runs from that gate. It explicitly
dispatches `cad.yml` for accepted durable refs because policy merges use
`GITHUB_TOKEN`.

Do not use GitHub's merge buttons or auto-merge as an alternative. Repository
settings must permit both merge methods because the correct method depends on
the PR head/base pair; `/merge` is the supported merge entrypoint.

## Git workflow

Prepare the complete logical patch before pushing when practical. Avoid a
separate commit/workflow run for every small file edit. If CI exposes several
related failures, collect them and make one bundled follow-up fix.

Do not mix unrelated model work into an existing PR merely because that branch
is already open.
