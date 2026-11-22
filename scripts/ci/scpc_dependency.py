#!/usr/bin/env python3
"""Build SCPC from its pinned revision as a shared CAD-CI dependency.

Only this item checks out SCPC. Individual model jobs consume the finished
wheel, so parallel SolidCraft builds never race while cloning a repository.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile

from bootstrap_cad_ci import dependency, ensure_checkout


ROOT = Path(__file__).resolve().parents[2]


def wheel_version(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        matches = [entry for entry in archive.namelist()
                   if entry.endswith(".dist-info/METADATA")]
        if len(matches) != 1:
            raise RuntimeError("SCPC wheel must contain one METADATA file")
        metadata = archive.read(matches[0]).decode("utf-8")
    for line in metadata.splitlines():
        if line.startswith("Version: "):
            return line.removeprefix("Version: ").strip()
    raise RuntimeError("SCPC wheel version missing")


def main() -> int:
    raw = os.environ.get("CAD_CI_OUTPUT", "").strip()
    if not raw:
        raise RuntimeError("CAD_CI_OUTPUT is required")
    output = Path(raw).resolve()
    dist = output / "dist"
    dist.mkdir(parents=True, exist_ok=True)

    url, wanted = dependency("scpc")
    actual = ensure_checkout("scpc")
    if actual != wanted:
        raise RuntimeError("SCPC checkout differs from pinned source")
    subprocess.run(
        [
            sys.executable, "-m", "pip", "wheel", "--no-deps",
            "--wheel-dir", str(dist), str(ROOT / "ext/scpc"),
        ],
        cwd=ROOT,
        check=True,
    )
    wheels = tuple(dist.glob("scpc-*.whl"))
    if len(wheels) != 1:
        raise RuntimeError(f"expected one SCPC wheel, got {len(wheels)}")
    wheel = wheels[0]
    (output / "provenance.json").write_text(
        json.dumps(
            {
                "schema": 1,
                "repository": url,
                "commit": actual,
                "version": wheel_version(wheel),
                "wheel": wheel.name,
                "sha256": hashlib.sha256(wheel.read_bytes()).hexdigest(),
            },
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )
    print(f"Prepared SCPC {wheel_version(wheel)} {actual}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
