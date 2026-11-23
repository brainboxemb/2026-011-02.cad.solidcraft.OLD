# CAD CI adapters

Only narrow CAD-owned adapters live here. Generic selection, dependency
closure, SCons scheduling, reuse, durable build scopes and Pages publication
belong to released `tool.cad.ci` / `lib.py.cad.ci`.

| File | Responsibility |
| --- | --- |
| `bootstrap_cad_ci.py` | Read exact Forge/SCPC source pins and prepare those source checkouts. |
| `forge_dependency.py` | Build one pinned Forge wheel + provenance. |
| `scpc_dependency.py` | Build one pinned SCPC wheel + provenance. |
| `verification_package.py` | Build the exact released CAD-verification wheel. |
| `repository_tests.py` | Expose shared dependency wheels and run repository tests once. |
| `model_catalog.py` | Load and validate model-owned `model.yml`. |
| `model_history.py` | Derive physical model-root last-modified timestamps from Git for Hugo presentation only. |
| `model_checks.py` | Load optional model-root snapshot presentation settings. |
| `model_build_batch.py` | Generate model commands and start one shared SolidCraft runtime batch. |
| `model_verify.py` | Save models, export STEP plus optional model-root STL from the accepted SolidCraft design, run optional semantic checks, render snapshots and write provenance. |
| `capture_site_layout.sh` | Render generated Plate/Simple-MFT Pages in headless Chrome and retain visual regression screenshots before publication. |

Do not add a changed-files planner, model scheduler, cache/store implementation,
Pages publisher or Python HTML generator here.


## Model history presentation input

`model_history.py` writes the generated `site/data/cad/model_history.json`
used by Hugo's content adapter to set page `Lastmod` values.

The manifest is deliberately narrow: it contains only the source commit and a
`category/root -> Git author timestamp` map. It does not copy titles,
descriptions, categories, build state or variant definitions from
`model.yml`, so it is not a second model catalog.

Generate it from a full Git checkout before running Hugo:

```bash
python scripts/ci/model_history.py \
  --output site/data/cad/model_history.json \
  --expected-source "$(git rev-parse HEAD)"
```

Variants owned by the same physical model root share that root's last-modified
timestamp.
