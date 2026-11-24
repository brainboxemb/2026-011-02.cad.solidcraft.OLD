#!/usr/bin/env python3
"""Build the exact CAD-pinned Forge source as one reusable CI dependency."""

import hashlib
import json
import os
from pathlib import Path
import re
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


def expected_solidcraft_version(root=ROOT):
    """Read the one CAD-owned SolidCraft version contract."""
    path = root / "ci/toolchain.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    version = data.get("solidcraft")
    if not isinstance(version, str) or not version.strip():
        raise RuntimeError("ci/toolchain.json must declare solidcraft")
    return version.strip()


def forge_tested_solidcraft_version(source):
    """Read Forge's package-level tested SolidCraft contract."""
    text = (source / "scpf/version.py").read_text(encoding="utf-8")
    match = re.search(
        r'(?m)^TESTED_SOLIDCRAFT_VERSION\s*=\s*["\']([^"\']+)["\']\s*$',
        text,
    )
    if match is None:
        raise RuntimeError("pinned Forge does not declare TESTED_SOLIDCRAFT_VERSION")
    return match.group(1)


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

    expected_solidcraft = expected_solidcraft_version()
    forge_solidcraft = forge_tested_solidcraft_version(source)
    if forge_solidcraft != expected_solidcraft:
        raise RuntimeError(
            "pinned Forge supports SolidCraft "
            f"{forge_solidcraft}, CAD toolchain expects {expected_solidcraft}"
        )

    wheel = wheels[0]
    provenance = {
        "schema": 1,
        "repository": url,
        "commit": revision,
        "version": wheel_version(wheel),
        "solidcraft": expected_solidcraft,
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
