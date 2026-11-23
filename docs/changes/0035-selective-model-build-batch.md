# 0035 — Selective shared model-build batch

Issue: #335

## Problem

The repository-level CAD-CI graph was selective, but once one model selected the
shared `model-build-batch`, that producer rebuilt all processed CAD models.

FlexBenchDog PR #334 run #367 proved the mismatch with `full_run=false`:
one model child output was selected, while the shared SolidCraft batch built all
16 active published variants. The shared batch took 54.675 s, including
45.061 s in SolidCraft.

## Decision

Adopt the already released/Forge-qualified CAD-CI
`selection_context: direct_dependents` contract on the batch step.

The CAD-specific batch adapter consumes
`CAD_CI_ACTIVE_DEPENDENTS_JSON`, validates the direct model item IDs against
the already configured process:true model roots, and prepares only those roots
and their owned catalog variants.

The Git/path selection remains entirely in released CAD-CI. The consumer does
not add a second planner, fingerprint engine or changed-path implementation.

An empty direct-dependent list produces an empty successful batch result and
does not pull or start the SolidCraft runtime.

## Acceptance

A one-model proof must show only that physical model root in the batch manifest
and SolidCraft summary, with one container start. Full-run/shared changes must
still select all affected direct model dependents. Docs/no-model work remains
batch-free.

Run #367 is the before measurement; the accepted one-model proof is recorded in
#335 after this change validates on dev-ci.
