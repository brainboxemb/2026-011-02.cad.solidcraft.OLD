"""Derive model last-modified timestamps from Git history for Hugo.

This is presentation input only. It does not define model identity, titles,
categories or build participation; model.yml remains the sole model catalog.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]


def physical_model_roots(root=ROOT):
    """Return validated physical model roots as category/root keys."""
    models = {
        path.parent.relative_to(root / "models").as_posix()
        for path in root.glob("models/*/*/model.yml")
    }
    ci = {
        path.parent.relative_to(root / "models").as_posix()
        for path in root.glob("models/*/*/ci.yml")
    }
    if models != ci:
        raise ValueError("model-history roots must match model.yml/ci.yml ownership")
    if not models:
        raise ValueError("no physical CAD model roots found")
    return tuple(sorted(models))


def _git(root, *args):
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def git_head(root=ROOT):
    return _git(root, "rev-parse", "HEAD")


def git_lastmod(model_root, root=ROOT):
    """Return the Git author date of the latest change below one model root."""
    value = _git(
        root,
        "log",
        "-1",
        "--format=%aI",
        "--",
        f"models/{model_root}",
    )
    if not value:
        raise ValueError(f"no Git history found for models/{model_root}")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError(f"Git timestamp lacks timezone: {value}")
    return value


def build_manifest(
    root=ROOT,
    *,
    expected_source=None,
    source_commit=None,
    lastmod_resolver=git_lastmod,
):
    """Build the derived root->lastmod manifest."""
    source = source_commit or git_head(root)
    if expected_source and source != expected_source:
        raise ValueError(
            f"model-history source mismatch: expected {expected_source}, got {source}"
        )

    history = {}
    for model_root in physical_model_roots(root):
        history[model_root] = lastmod_resolver(model_root, root)

    return {
        "schema": 1,
        "source_commit": source,
        "roots": history,
    }


def write_manifest(path, manifest):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--expected-source")
    args = parser.parse_args()

    manifest = build_manifest(expected_source=args.expected_source)
    write_manifest(args.output, manifest)


if __name__ == "__main__":
    main()
