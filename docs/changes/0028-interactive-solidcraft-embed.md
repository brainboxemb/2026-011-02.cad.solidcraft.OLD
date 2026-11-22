# 0028 — Interactive SolidCraft model embed

Issue: #21

## Goal

Allow a published CAD model to be inspected interactively from its Hugo detail
page without introducing a custom model viewer or a second CAD runtime.

## Upstream contract

SolidCraft's official web application supports:

- `?open=<encoded HTTPS .sc URL>` for opening a hosted design;
- `?embed&open=<...>` for an embedded viewport/timeline/browser-tree view.

The CAD site consumes that supported upstream API. It does not mirror,
repackage or script the SolidCraft application.

## Presentation contract

The calm model-detail hierarchy from change 0027 remains authoritative.

The interactive viewer is therefore:

- optional and available only when the published model has `model.sc`;
- collapsed by default;
- placed directly below the existing **Open in SolidCraft Web** section;
- labelled as an external SolidCraft application;
- loaded with a responsive 16:9 frame and `loading="lazy"`;
- accompanied by the existing full-app link as the primary escape path.

The default Plate/Simple-MFT page screenshots continue to capture the closed
state. The embed must not add another always-visible dashboard panel.

## URL ownership

The embedded app URL is generated from the model's published absolute
`.Permalink`:

```text
https://docs.solidcraft.io/app/?embed&open=<url-encoded published model.sc URL>
```

The same published `.sc` file is used by the existing **Open in SolidCraft
Web** link. No duplicate or temporary model copy is introduced.

## Verification

Before acceptance:

- repository tests assert the embed is generated only inside the
  `model.sc` resource branch;
- generated HTML contains `?embed&open=` and the encoded published model URL;
- the iframe is collapsed by default and marked `loading="lazy"`;
- Plate and Simple MFT rendered screenshots remain visually stable in their
  default closed state;
- the published `.sc` URL remains HTTPS-accessible and usable by the official
  SolidCraft web application.

This is a Hugo presentation feature only. It does not change CAD geometry,
model verification or the SolidCraft document format.
