# CAD-CI items

These folders are consumer-owned work items for the released CAD-CI graph, not
another CI framework. Root `cad-ci.yml` discovers them through `ci/*`.

| Directory | Purpose |
| --- | --- |
| `forge-package/` | Build the exact Forge wheel from `dependencies.repos`. |
| `scpc-package/` | Build the exact SCPC wheel from `dependencies.repos`. |
| `cad-verification-package/` | Build the exact released verification wheel. |
| `repository-tests/` | Run retained repository regressions once. |
| `model-build-batch/` | Build selected CAD variants in one SolidCraft runtime batch. |

Generic planning, SCons execution, build-store mutation and Pages publication
remain in released CAD-CI. Model-specific data stays beside the model.
