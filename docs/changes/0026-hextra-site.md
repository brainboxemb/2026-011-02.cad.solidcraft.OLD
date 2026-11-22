# 0026 — Accepted Hugo + Hextra CAD site

Issue: #251
Parent migration: #191

## Problem

The first Hugo migration design used Blowfish as the presentation candidate.
That architecture removed the custom Python HTML generator, but the accepted
site subsequently moved to Hextra while retaining CAD-owned layouts, content
contracts and visual identity.

The live repository and stable Pages now use:

- Hugo 0.169.0;
- Hextra v0.13.0, pinned by `site/go.mod`;
- CAD-owned layouts/partials below `site/layouts/`;
- CAD-owned active styling in `site/assets/css/custom.css`;
- model-owned `model.yml` metadata and optional `page.md` content;
- accepted CAD-CI build evidence mounted read-only into Hugo;
- released CAD-CI publication for stable and development-lane Pages scopes.

Durable requirements/design/AGENTS text still described Blowfish, so it no
longer matched the promoted stable implementation.

## Decision

The accepted CAD website presentation layer is **Hugo 0.169.0 + Hextra
v0.13.0**.

Hextra provides the common documentation shell and theme primitives. The CAD
repository continues to own the product-specific page composition, model
presentation, navigation choices and engineering visual treatment.

`site/results.css` remains only as the pre-Hugo visual comparison baseline. It
is not the active stylesheet. Current styling is maintained in
`site/assets/css/custom.css`.

The legacy Python HTML generator is retired and must not return. Site Python may
prepare/validate data where genuinely necessary, but authored page composition
belongs to Hugo layouts/content rather than Python HTML strings.

Historical change record 0023 remains unchanged as evidence of the earlier
Hugo/Blowfish migration stage.

## Site contract

The website data flow is:

```text
models/<section>/<model>/model.yml
models/<section>/<model>/page.md        (optional)
accepted build/<scope> evidence
              |
              v
Hugo 0.169.0 + Hextra v0.13.0
site/layouts/ + site/assets/css/custom.css
              |
              v
homepage + category pages + /models/<slug>/ + downloads/actions
              |
              v
released CAD-CI Pages publisher
```

The following remain repository contracts:

- `model.yml` is the model-page metadata source; do not add a second catalog;
- optional `page.md` adds background/reference prose but does not redefine
  model identity or build/verification facts;
- source code shown on model pages is read from the declared repository source;
- generated commands and native outputs come from accepted build evidence;
- verification labels must remain provenance-backed;
- SCPF is primary technical source; SCPC is optional secondary comparison;
- existing model/category routes remain stable;
- no model-specific slug branches in shared Hugo templates;
- Hugo does not select/build CAD or mutate accepted build evidence;
- the CAD site is not replaced by Forge's site renderer merely because both
  repositories share CI infrastructure.

## Verification

The complete accepted Hextra lane was promoted by PR #249.

Promotion evidence:

- exact head before promotion:
  `88fc6641d9eccf4ad853ac2592aef51e5b4452b9`;
- promotion validation run 45044936849 used `full_run: true`;
- SCons reported 19 targets built, 0 errors;
- normal two-parent promotion merge:
  `b2f7cac32ebc045a3ec25e9e4d4988d76aaaf680`;
- shared merge policy advanced both `main` and `dev-ci` to that merge;
- stable `build/main`, public Pages, `build/dev-ci` and Pages `/dev-ci/`
  all source-match the promoted merge;
- implementation issues #211-#217 and #227 were closed from that stable
  evidence.

The final documentation-only #251 PR must leave all repository/site tests green
and publish a stable main scope matching its exact merge commit before parent
#191 closes.
