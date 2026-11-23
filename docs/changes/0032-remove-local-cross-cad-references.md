# 0032 — Remove local cross-CAD reference implementations

Issue: #206

## Problem

The product CAD repository still carried eight alternative implementation
sources under the CSG Cube and Plate model roots:

- CadQuery;
- MicroCAD;
- PythonSCAD;
- vcad.

Those files were comparison/reference implementations rather than product CAD
inputs. Cross-CAD API qualification and reference implementations belong to
Forge, while this repository owns the actual SCPF/SCPC product models.

## Decision

Remove the four reference implementation directories from both model roots.

Do not replace them with another local reference matrix. The model READMEs
point cross-CAD comparison ownership to Forge and continue to document the
supported SCPF/SCPC sources and model-specific regression evidence.

No `model.yml`, geometry source, CAD execution contract or public model route
changes as part of this cleanup.

## Verification

Repository ownership tests assert that the four reference implementation
directories do not exist below either model root.

Normal repository/CAD CI must remain green. After merge, durable `dev-cad`
build and Pages publication must source-match the accepted lane.
