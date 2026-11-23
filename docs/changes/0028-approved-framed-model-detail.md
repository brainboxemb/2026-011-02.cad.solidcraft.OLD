# 0028 — User-approved framed model-detail baseline

Issue: #278
Approved experiment: `brainboxemb/exp.2026-015.hugo-cad-site#29`
Approved EXP PR: #31
Approved EXP main commit: `b0ed2dc474affc9bc0591ff60c5e95ce12a31b25`
Accepted visual proof: EXP run #92 (`45134031122`)

## Supersedes the presentation decision in 0027

Change 0027 records an intermediate model-detail redesign that was technically
validated but visually rejected after publication review.

This change keeps 0027 as history, but **supersedes its presentation contract**.
The restored pre-0027 CAD publication was used as the visual baseline in EXP,
then corrected incrementally and explicitly approved before this port.

## Approved hierarchy

The model-detail page keeps the familiar framed hierarchy:

- compact status badges below the hero;
- Model preview and Files/Construction stages as the paired top panels;
- Open in SolidCraft Web in a framed panel;
- optional Background in a framed panel;
- optional reference/extra views in a framed panel;
- SCPF source in a framed code section and visible by default;
- SCPC source in a framed code section and visible by default when present;
- generated SolidCraft commands in a framed disclosure, collapsed by default;
- build/verification evidence in a framed panel;
- source/download links in a framed panel.

Do not replace these panels with a free-form facts row or transparent
document-section layout.

## Section labels

Small blue labels provide a consistent hierarchy:

- `SolidCraft model` → Open in SolidCraft Web;
- `Model context` → Background;
- `Design reference` → reference/extra-view title;
- `Source` → SCPF source;
- `Generated output` → SolidCraft command sequence;
- `Independent comparison` → SCPC command source;
- `Accepted build evidence` → Build and verification.

Standalone large numeric section labels are not used.

## Source-first behavior

SCPF is the primary model source and is visible on initial page load. SCPC is
also visible when a comparison source exists.

Generated SolidCraft commands are secondary generated evidence and may remain
collapsed by default.

## Typography and spacing fixes

The approved EXP proof keeps the backup layout but corrects:

- Segoe UI/system sans for CAD prose and headings;
- normal body weight and neutral tracking;
- preview geometry independent from heading height;
- Background Markdown lists explicitly render list markers;
- Background list markers use the CAD accent color;
- Construction stages use tighter vertical rhythm:
  - line-height `1.42`;
  - item margin `0.12rem 0`;
- reference content retains the two-column visual comparison.

## SolidCraft build-version badge

The status badge shows the SolidCraft version that actually built the model.

Model provenance therefore includes:

```json
"solidcraft_version": "0.45.0"
```

The value comes from `SOLIDCRAFT_VERSION` inside the immutable runtime image,
not from a hardcoded Hugo value.

For runtime `ghcr.io/brainboxemb/cad-solidcraft:v0.3.4`, the immutable runtime
release pins SolidCraft `0.45.0`.

Badge forms:

- verified build: `SolidCraft 0.45.0 · verified`;
- built without semantic verification: `Built in SolidCraft 0.45.0`.

## Visual regression proof

The existing CAD-owned Chrome proof remains required before publication:

- Plate overview;
- Plate full page;
- Simple MFT overview;
- Simple MFT full page.

The CAD screenshots must match the user-approved EXP hierarchy from run #92 before #278 is
closed again.

## Port boundary

This change ports only the approved EXP model-detail baseline.

It does **not** include:
- the interactive SolidCraft iframe/viewer from #21;
- CAD-CI lifecycle work from #288;
- any new model or geometry work.


### Durable parity correction

The first durable CAD screenshot run after the approved port exposed two
presentation differences that were not visible in the EXP data adapter:

- the CAD codeblock partial had lost the dark technical code surface;
- the external-reference `open original` anchor inherited the image-link
  16:9 layout and rendered as a large empty tile.

The follow-up parity correction restores the approved dark code surface, keeps
`open original` as a normal inline link, and restores the model description
below the preview as shown in EXP.
