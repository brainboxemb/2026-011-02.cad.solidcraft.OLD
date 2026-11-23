# 0043 — HUB75 connector envelopes

Issue: #375

## Problem

The reusable detailed HUB75 panel already carries the measured rear mounting
interfaces, but it still omits the connector volumes that determine rear
clearance. Assemblies and enclosures must not duplicate those panel-local
positions and dimensions.

## Decision

The detailed `Hub75Panel` owns three fixed connector clearance features in its
local X/Y/Z axes:

- two IDC/HUB75 data-connector envelopes centered at local X=0 and
  Y=±113.5 mm, each 27.90 × 9.50 × 10.64 mm, starting at Z=2.63 mm;
- one power-connector clearance envelope derived from the preserved v1.2 visual
  reference position X=53 mm / long-axis coordinate 128 mm in the nominal
  160 × 320 mm reference raster. Those coordinates are scaled to the measured
  159.70 × 319.71 mm panel before centering, yielding local centres of about
  X=-26.9494 mm and Y=-31.9710 mm. The envelope is 13 × 20 × 7 mm and starts
  1 mm behind the PCB back face (Z=3 mm).

The IDC dimensions and front datum are preserved from the existing source
contract. The power connector remains explicitly approximate: its source
position and envelope are visual-reference values, not drawing dimensions.

These volumes are named native XY Sketch + join-Extrude features attached to
the reusable panel body so they remain explicit in the feature history. This
uses the released Forge v0.11 explicit-Sketch feature path; it does not depend
on newer standalone-Sketch boolean support. No enclosure dimensions or
assembly-world coordinates are introduced in this component.

## Contract

- Connector geometry is fixed product geometry, not editable model parameters.
- Local component axes remain X=panel width, Y=panel height, Z=front-to-rear.
- Assemblies consume the reusable component; they do not restate connector
  coordinates.
- The approximate power envelope must remain labelled as approximate in source
  and user-facing model documentation.

## Verification

Focused model regressions must verify:

- two named 27.90 × 9.50 × 10.64 data-envelope Sketch/Extrude features at
  Y=±113.5 mm, front Z=2.63 mm;
- one named 13 × 20 × 7 approximate power-envelope Sketch/Extrude feature at
  the transformed local center;
- no new editable parameters;
- the ordinary native SolidCraft build and rear snapshot complete on the
  pinned CAD stack.
