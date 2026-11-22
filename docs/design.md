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

The host launches the immutable SolidCraft runtime only for selected native
model actions. Python dependencies and model-specific scripts are separate
inputs. A change to a test or model does not rebuild a Docker image.

## Model item shape

Current repository discovery has **16** physical `models/**/ci.yml` roots.
The website/catalog has **18** model variants. Preserve that mapping; do not
create a second catalog just for generic CI.

Desired item contract:

```yaml
id: sample-plate
template: cad-model-native
process: true
# model-local source/tests/verification inputs plus declared cross-model needs
```

Root `cad-ci.yml` will hold the shared template and explicit runtime
variables; the exact template syntax must be validated against the released
tool/library contracts. The model-specific `verification/verify.py` will
define the expected native outcomes, while the generic verification library
will apply them and write evidence. SCPC models add an independent comparison
step with explicit outputs.

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

## Retirement boundary

Currently the CAD repository still has local orchestration in
`build_plan.py`, `select_models.py`, `pipeline_ci.py`, `cad_ci.py`,
`native_ci.py` and `publish_ci.py`. Model-specific tools and the site
generator can remain, but generic planner/runtime/publisher behavior must
be retired only after the released replacements are proven.

No rewrite of the CAD website's content or geometry is required merely to
match Forge's CI design.
