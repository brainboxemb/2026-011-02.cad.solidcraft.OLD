# CAD repository requirements

This document defines the target CI and publication contract for
`2026-011-02.cad.solidcraft`. Migration tracking is in `docs/plan.md`;
historical decisions are in `docs/changes/`.

## Ownership

The accepted Forge CI stack is the reference design, not another
implementation to copy into this repository.

- `tool.cad.ci` is the only generic runner/CLI/workflow surface.
- `lib.py.cad.ci` owns changed-path selection, dependency closure, SCons
  execution, up-to-date decisions, result reuse, complete build manifests,
  generated-branch publication and retry.
- Released `lib.py.cad.verification` owns general native SolidCraft evaluation,
  mutations, checks and machine-readable evidence.
- `docker.cad.solidcraft` owns the immutable SolidCraft runtime; this
  repository may only select its released image.
- Forge and SCPC own their Python APIs; this repository pins exact released
  source revisions and owns CAD model content.
- This repository owns model-specific expectations, SCPF/SCPC model production,
  comparison intent, website prose, catalog presentation and presentation
  images.

Do not create a second CAD-specific generic selector, SCons scheduler,
verification engine, build-store implementation or Pages publisher.

## Generic CI requests: Forge owns the decision

Generic changes requested by this CAD consumer do **not** go directly into
`lib.py.cad.ci` or `tool.cad.ci`. Start with a Forge issue explaining
the problem, expected behavior, acceptance tests and performance impact.
Forge decides the shared requirements and design. The appropriate generic
owner repository implements and releases the change independently, after
which Forge qualifies and selects its release. This CAD repository then
adopts the same released stack.

The scan → plan → shared model-build-batch requirement is tracked by
`brainboxemb/lib.py.solidcraft.forge#661`. Do not introduce local
selection/scheduling/cache logic while waiting for a generic answer.
Do not move the stable CAD site to Forge's page layout.

## Same source lanes and generated scopes as Forge

Permanent source branches: `main`, `dev-cad`, `dev-ci`.

- Short-lived CAD/model PRs target `dev-cad`.
- CI/publishing migration PRs target `dev-ci`.
- Feature/fix PRs are **squash-merged** into the corresponding dev lane.
- Lane-to-`main` promotions use a **normal merge commit** through the
  owner-controlled merge policy, not squash; the long-lived lane is retained.
- PRs validate without writing durable model output.
- Pushes to a long-lived branch may publish only their own generated scope:
  `build/main`, `build/dev-cad`, `build/dev-ci` and Pages root,
  `dev-cad/`, `dev-ci/`.
- A generated-branch writer may not overwrite sibling scopes or force-push.
- Preserve the current stable site and model URLs through the migration.

## Workflow and model ownership

- The workflow invokes the **exact released** `tool.cad.ci` root action,
  as Forge does, including a tested bounded `jobs` value.
- Root `cad-ci.yml` declares runtime variables, templates and item discovery.
- Each model-root `ci.yml` stays small (identity, template, participation and
  genuinely local overrides). Common dependency/build/output policy belongs
  in the root template; one physical root may own multiple catalog variants.
- A model-specific change selects only the affected model and its declared
  dependants; SCons decides whether a selected action needs to run.
- A source-level change to Forge/SCPC/verifier/runtime that changes model
  semantics invalidates the affected outputs. A deliberate full model check
  is required for runtime or Forge version promotions.
- Promotion PRs from `dev-cad`/`dev-ci` into `main` run all processed CI
  items, including their actual SolidCraft model execution; unit tests alone
  are not model acceptance.
- Documentation-only changes that cannot change technical outputs avoid
  expensive model runs under the same narrow Forge-style PR classifier.
- A model is reported as built against a new toolchain only when its own
  saved native design, STEP/results and checks were produced under that
  toolchain. Merely refreshing the website or command JSON does not count.

## Build batch and scan contract

- Reuse the **Forge pattern**: CAD-CI discovers all items and owns the
  changed-path/dependency plan; one released SCons run executes the plan.
- Prepare shared Forge/SCPC/checker dependencies once. One shared build-batch
  item collects the affected model commands and runs SolidCraft with **one
  container startup**, writing separate verification evidence per model.
- Model items use the existing released `copy: dependency` mechanism to
  expose their own results; they do not each launch Docker.
- Item discovery uses category globs and declarative `process`, not a
  growing manually edited list of model paths.
- Ordinary development PRs remain selective. A complete model check is
  required for toolchain upgrades and deliberate lane-to-main promotion.
- Measure plan count, model-build count, shared dependency runs, image pulls,
  container starts and total elapsed time. Do not claim the architecture is
  completed just because isolated model builds succeed.
- If the released batch model cannot preserve the required selectivity,
  resolve that with Forge/CAD-CI's published generic architecture first,
  not a new second scheduler within the CAD repository.

## Verification and results

- Keep the semantic checks declarative beside their models; do not bury model
  expectations inside the GitHub workflow, general Python runners or HTML.
- Preserve SCPC-versus-Forge comparison where the model has an independent
  SCPC source.
- Native output must contain the editable `.sc`, STEP where supported,
  measurements/check results, required renders and exact input/version
  provenance. Required artifacts missing or empty fail that model.
- Never relabel retained old results as newly checked after a library or
  runtime update.
- Publication consumes a **complete** accepted build scope and produces one
  validated site; it does not regenerate or mutate CAD geometry.

## Public CAD website continuity

The **CI implementation may change, but the visible CAD website must remain
recognizably the same**. Forge's workflow/tooling architecture is the reference;
Forge's website layout is **not** a replacement template for this site's UI.

Preserve these user-visible contracts in the stable Pages root:

- Current home-page presentation, visual style and curated model overview.
- The existing Basic Models, Components and Advanced Models navigation and
  category pages.
- The current model page hierarchy: model title and explanation, model
  preview/screenshots, construction stages, actual Forge/SCPC source (where
  applicable), native command sequence, downloads/links and verification
  information.
- Existing model slugs and public routes, including
  `/models/<slug>/` and `/models/basic/`, `/models/components/`,
  `/models/advanced/`; avoid broken external or internal links.
- Model-specific diagrams, supplementary screenshots, warnings and the
  distinction between newly checked models and older retained output.
- The present `site/results.css` visual identity and responsive layout in
  broad terms. Pixel-perfect equality is not required, but major navigation,
  information, or layout changes are **not** part of this CI migration.

The existing CAD site generator remains consumer-owned and is adapted only
where the new build evidence format requires it; it must not be replaced by
Forge's site generator as a side effect of CI modernization.

Before publishing the new stable site, compare generated old and new versions
of the homepage, all three category indexes, representative simple and
advanced model pages, and a model containing both Forge and SCPC sources.
Check visual structure, source availability, links, native result/downloads
and meaningful verification labels. A regression in these public behaviours
blocks publication even when all model builds pass.

Any deliberate website redesign is a separate, explicitly scoped change with
its own review and acceptance criteria.

## Adoption gates

Before removing the current working workflow, prove: all 16 current model-root
CI items and their 18 catalog variants are represented; selective
single-model execution; full-model execution on promotion/version upgrade;
matching output/verification provenance; independent stable/dev scopes;
and website appearance/content/link parity acceptance. Do not change model geometry to disguise a
missing generic CI feature.

## Model-owned content and website data

- Every one of the 16 physical model roots owns a `model.yml`, following
  the established Forge example metadata vocabulary: section, priority,
  title, tagline, description, parameters, and stages. CAD-specific source,
  diagram, warning, and optional variant/reused-component fields live there
  too.
- The two physical model roots with multiple catalog variants (GuideRail and
  Simple MFT) declare those variants **inside one local `model.yml`**.
- `scripts/ci/model_catalog.py` validates/discovers the local YAML; it
  must not maintain a competing handwritten list of models.
- `ci.yml` declares build execution only, while `verification/verify.py`
  declares physical checks. The static site renderer consumes model-owned
  metadata, build results, source code and verification evidence.
- A presentation-only metadata change must not change SolidCraft geometry
  fingerprints or trigger a SolidCraft rebuild. Metadata must still select
  site refresh when publishing from the accepted build output.
- Common page/layout rendering remains shared. Model-specific supplementary
  views are described in `model.yml` and rendered generically, not in
  slug-specific branches inside the HTML generator.
- Do not change the existing website design, routes, warnings, published
  assets, or source/download behavior without a separate explicit decision.

