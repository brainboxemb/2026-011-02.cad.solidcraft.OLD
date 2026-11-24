# 0052 — refine detailed HUB75 rear bay contours

Issue: #373

## Context

The detailed Hub75Panel already owns the measured outer envelope, full rear
taper, mounting tubes, reinforcement interfaces and locator pins. Its four
rear electronics-bay cuts were still square-cornered rectangles, while the
preserved v1.2 OpenSCAD/STEP reference defines rounded and stepped bay edges
plus shallow recessed rail strips.

Forge v0.13.2 provides attached connected line/arc profiles, so this geometry
can be represented directly without overlapping closed-profile workarounds.

## Decision

Restore the rear-frame contour directly from the v1.2 reference:

- four separate connected profiles in the existing one rear-facing bay Sketch;
- R5 reference inner corners, scaled to the measured 159.70 × 319.71 mm panel;
- 10.75 mm normal end rail;
- 7.75 mm central narrow rail;
- 30 mm narrow section;
- nominal 3 mm 45-degree transitions;
- three 20 mm separator ribs whose adjacent reliefs leave the preserved
  approximately 14 mm central stepped section;
- one deep bay cut that still stops at `front_depth`.

Add the STEP-derived rear rail surface treatment as a separate shallow feature:

- 0.80 mm recess depth;
- two side-rail rounded strips;
- two end-rail rounded strips;
- three stepped crossbar strips inset by the reference 1.5 mm border;
- reinforcement cylinders are joined after this cut, preserving their Ø14
  rear-face footprints.

## Boundaries

Do not change:

- measured front envelope;
- outer taper;
- six mounting-tube centres/bores;
- six reinforcement interfaces;
- two locator pins;
- front mask / PCB stack;
- local component axes.

CAD #388 remains the separate reusable-component Cylinder/occurrence blocker;
this contour change must not work around it.

## Acceptance

- the one rear-bay Sketch contains four closed connected line/arc contours;
- the bay geometry lowers to 48 connected lines and 16 true circular arcs;
- the shallow recess owns four rounded-rectangle strips plus three closed
  stepped crossbar polygons and one 0.80 mm negative cut;
- mounting cylinders/holes remain 14 / 24;
- native `hub75-panel` build and rear image generation succeed;
- final rear-view visual acceptance uses exact PR render evidence when generic
  CAD-CI review artifacts are available through tool.cad.ci #181.
