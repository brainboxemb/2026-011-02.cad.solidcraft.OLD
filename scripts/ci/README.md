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
| `model_checks.py` | Load optional model-root snapshot presentation settings. |
| `model_build_batch.py` | Generate model commands and start one shared SolidCraft runtime batch. |
| `model_verify.py` | Save models, run optional semantic checks, render snapshots and write provenance. |

Do not add a changed-files planner, model scheduler, cache/store implementation,
Pages publisher or Python HTML generator here.
