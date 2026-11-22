#!/usr/bin/env python3
"""Resolve the released central SolidCraft runtime and consumer library pins."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import tomllib

from bootstrap_cad_ci import dependency


ROOT = Path(__file__).resolve().parents[2]
TOOLCHAIN = ROOT / "ci" / "toolchain.json"
_RELEASE_IMAGE = re.compile(
    r"^ghcr\.io/brainboxemb/cad-solidcraft:v\d+\.\d+\.\d+$"
)


def load_toolchain(root: Path = ROOT) -> dict:
    """Read and validate the immutable central runtime selection."""

    data = json.loads((root / "ci" / "toolchain.json").read_text(encoding="utf-8"))
    if data.get("schema") != 2:
        raise ValueError("unsupported CAD toolchain schema")

    reference = str(data.get("runtime_image", ""))
    if not _RELEASE_IMAGE.fullmatch(reference):
        raise ValueError(
            "runtime_image must be an immutable released "
            "ghcr.io/brainboxemb/cad-solidcraft:vX.Y.Z reference"
        )

    solidcraft = str(data.get("solidcraft", ""))
    if not re.fullmatch(r"\d+\.\d+\.\d+", solidcraft):
        raise ValueError("solidcraft must be an exact X.Y.Z version")
    return data


def scpf_release(root: Path = ROOT) -> str:
    """Read the package version from the exact checked-out Forge source."""

    path = root / "ext" / "scpf" / "scpf" / "pyproject.toml"
    if not path.is_file():
        raise FileNotFoundError(
            "missing ext/scpf checkout; run scripts/ci/bootstrap_cad_ci.py first"
        )
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    version = data.get("project", {}).get("version")
    if not isinstance(version, str) or not version:
        raise ValueError("SCPF pyproject.toml has no project.version")
    return version


def metadata(root: Path = ROOT) -> dict[str, str]:
    """Return runtime and exact consumer dependency provenance."""

    data = load_toolchain(root)
    _, scpf_sha = dependency("scpf", root)
    _, scpc_sha = dependency("scpc", root)
    return {
        "reference": data["runtime_image"],
        "solidcraft": data["solidcraft"],
        "scpf_sha": scpf_sha,
        "scpc_sha": scpc_sha,
        "scpf_release": scpf_release(root),
    }


def write_github_output(path: Path, values: dict[str, str]) -> None:
    """Append resolved values using the GitHub Actions output-file format."""

    with path.open("a", encoding="utf-8") as handle:
        for key, value in values.items():
            handle.write(f"{key}={value}\n")


def main() -> int:
    """Print resolved runtime metadata and optionally expose Actions outputs."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--github-output", type=Path)
    args = parser.parse_args()

    values = metadata()
    for key, value in values.items():
        print(f"{key}={value}")
    if args.github_output:
        write_github_output(args.github_output, values)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
