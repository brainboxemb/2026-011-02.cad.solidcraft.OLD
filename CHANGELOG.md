# Changelog

Notable changes to `2026-011-02.cad.solidcraft`, newest first.

## [Unreleased]

### Public API and behavior

- **Changed:** Product CAD development is split across the permanent
  `dev-cad` and `dev-ci` working lanes. Accepted work may accumulate on a
  development lane and is promoted to `main` only at a deliberate stable
  checkpoint rather than after every individual PR.
- **Changed:** Model detail pages use model-owned `model.yml` content together
  with generated build/verification evidence. Long descriptive parameter prose
  is presented as readable key dimensions rather than as a status badge.
- **Added:** FlexBenchDog now has the reviewed MFT stop collar, four-segment
  flex stem with R0.5 inner-corner relief, and recessed BrainBox wireframe
  mark. Temporary compatibility constructions are explicitly tracked against
  their Forge owner issues rather than being treated as final API usage.
- **Changed:** CornerBracket restores the preserved 11-point arm profile and
  explicit recessed M5 fixing-seat construction. The remaining local arm-tip
  wedge is intentionally deferred to reusable Forge shape-transform support.

### Dependencies and compatibility

- **Changed:** Current accepted native CAD execution targets SolidCraft 0.45.0
  through the released CAD runtime image. Forge remains consumed through a
  pinned released version; newer Forge fixes are adopted only after a normal
  Forge release and CAD dependency-update qualification.
- **Changed:** Generic CAD-CI, verification and runtime behavior are consumed
  from their owner repositories rather than reimplemented in this product-CAD
  repository.

### Infrastructure and tooling

- **Changed:** CAD-CI uses released affected-item/SCons selection and a shared
  model build batch, so only selected model roots are prepared and executed.
  The retired Moon/GitHub-cache proposal is not part of the active
  architecture.
- **Changed:** Generated durable build state and GitHub Pages are maintained per
  permanent scope (`main`, `dev-cad`, `dev-ci`) with source provenance.
- **Added:** Model-owned optional extra snapshots can provide verified detail
  views without route-specific rendering logic.

### Internal implementation

- **Changed:** Product models own their source, metadata, optional presentation
  settings and model-specific verification data. Reusable modelling/compiler
  capability remains in Forge; generic orchestration remains in the CAD-CI
  owner layer.
- **Changed:** Independent SCPC command models coexist with SCPF models where a
  second implementation is useful for native geometry comparison. SCPC
  coverage is model-specific rather than a requirement that every catalog
  model have a duplicate implementation.

### Documentation

- **Added:** `AGENTS.md`, `docs/plan.md` and `docs/handoff.md` define the
  permanent-lane cadence, owner-repository boundaries and current-work
  protocol.
- **Added:** Numbered change records under `docs/changes/` preserve important
  model/architecture decisions without turning this changelog into a commit
  log.

## Historical release status

As of 2026-11-23 this repository has **no GitHub Releases and no Git tags**.
There is therefore no authoritative historical version boundary from which to
construct truthful `## [<version>] - YYYY-MM-DD` sections.

Earlier accepted CAD, CI and site changes remain traceable through Git history,
issues, pull requests and `docs/changes/`. This changelog deliberately does
not invent retrospective versions or treat arbitrary commits as releases.

If this product repository later adopts explicit release or accepted-checkpoint
boundaries, add them here using the real identifier and ISO date from the
corresponding repository evidence.
