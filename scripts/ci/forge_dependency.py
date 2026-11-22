#!/usr/bin/env python3
"""Build the exact CAD-pinned Forge source as one reusable CI dependency."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile

from bootstrap_cad_ci import dependency, ensure_checkout


ROOT = Path(__file__).resolve().parents[2]


def wheel_version(path):
    with zipfile.ZipFile(path) as archive:
        names = [n for n in archive.namelist() if n.endswith(".dist-info/METADATA")]
        if len(names) != 1:
            raise RuntimeError("Forge wheel must contain one METADATA")
        metadata = archive.read(names[0]).decode("utf-8")
    for line in metadata.splitlines():
        if line.startswith("Version: "):
            return line.removeprefix("Version: ").strip()
    raise RuntimeError("Forge wheel version missing")


def main():
    raw = os.environ.get("CAD_CI_OUTPUT", "").strip()
    if not raw:
        raise RuntimeError("CAD_CI_OUTPUT is required")
    out = Path(raw).resolve()
    dist = out / "dist"
    dist.mkdir(parents=True, exist_ok=True)
    url, revision = dependency("scpf")
    if ensure_checkout("scpf") != revision:
        raise RuntimeError("Forge checkout does not match pinned revision")
    source = ROOT / "ext/scpf/scpf"
    subprocess.run(
        [sys.executable, "-m", "pip", "wheel", "--no-deps",
         "--wheel-dir", str(dist), str(source)],
        check=True, cwd=ROOT,
    )
    wheels = tuple(dist.glob("scpf-*.whl"))
    if len(wheels) != 1:
        raise RuntimeError(f"expected one Forge wheel, found {len(wheels)}")
    from_version = (source / "scpf/version.py").read_text(encoding="utf-8")
    if 'TESTED_SOLIDCRAFT_VERSION = "0.45.0"' not in from_version:
        raise RuntimeError("pinned Forge does not support SolidCraft 0.45.0")
    wheel = wheels[0]
    provenance = {
        "schema": 1,
        "repository": url,
        "commit": revision,
        "version": wheel_version(wheel),
        "solidcraft": "0.45.0",
        "wheel": wheel.name,
        "sha256": hashlib.sha256(wheel.read_bytes()).hexdigest(),
    }
    (out / "provenance.json").write_text(
        json.dumps(provenance, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Prepared exact Forge {provenance['version']} at {revision}", flush=True)


if __name__ == "__main__":
    main()
