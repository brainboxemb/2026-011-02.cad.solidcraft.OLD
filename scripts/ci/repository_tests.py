#!/usr/bin/env python3
"""Run CAD repository regressions inside the released CAD-CI graph.

Released CAD-CI owns selection, dependency ordering and SCons. This adapter
only exposes already-built dependency wheels and invokes unittest once.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]


def dependency_wheel(name: str, pattern: str) -> Path:
    """Return exactly one wheel produced by a declared CAD-CI dependency."""

    raw = os.environ.get("CAD_CI_DEPENDENCIES_JSON", "")
    if not raw:
        raise RuntimeError("CAD_CI_DEPENDENCIES_JSON is required")
    entry = json.loads(raw).get(name)
    if not isinstance(entry, dict) or not entry.get("output_root"):
        raise RuntimeError(f"required dependency missing: {name}")
    matches = tuple((Path(entry["output_root"]) / "dist").glob(pattern))
    if len(matches) != 1:
        raise RuntimeError(
            f"expected one {name} wheel matching {pattern}, found {len(matches)}"
        )
    return matches[0].resolve()


def main() -> int:
    """Run all retained tests and write one inspectable result."""

    output_text = os.environ.get("CAD_CI_OUTPUT", "").strip()
    if not output_text:
        raise RuntimeError("CAD_CI_OUTPUT is required")
    output = Path(output_text).resolve()
    output.mkdir(parents=True, exist_ok=True)

    wheels = (
        dependency_wheel("forge-package", "scpf-*.whl"),
        dependency_wheel("scpc-package", "scpc-*.whl"),
        dependency_wheel(
            "cad-verification-package",
            "brainboxemb_cad_verification_lib-*.whl",
        ),
    )
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join(
        [*(str(path) for path in wheels), str(ROOT), env.get("PYTHONPATH", "")]
    ).rstrip(os.pathsep)

    command = [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]
    completed = subprocess.run(command, cwd=ROOT, env=env, check=False)
    result = {
        "schema": 1,
        "command": command,
        "status": "pass" if completed.returncode == 0 else "fail",
        "returncode": completed.returncode,
        "dependency_wheels": [path.name for path in wheels],
    }
    (output / "result.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
