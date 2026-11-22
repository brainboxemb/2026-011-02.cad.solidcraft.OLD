#!/usr/bin/env python3
"""Plate-only bridge from released CAD-CI items to released CAD verification.

SCons controls selection. The released verification package controls generic
SolidCraft checks. This consumer script only produces one editable CAD model.
"""

import json
import os
from pathlib import Path
import runpy
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
MODEL = ROOT / "models/basic/plate/scpf/model.py"
DEFINITION = ROOT / "models/basic/plate/verification/verify.py"


def exact_wheel(item, pattern):
    context = json.loads(os.environ["CAD_CI_DEPENDENCIES_JSON"])
    dependency = context.get(item)
    if not isinstance(dependency, dict) or not dependency.get("output_root"):
        raise RuntimeError(f"missing CAD-CI dependency {item}")
    wheels = tuple((Path(dependency["output_root"]) / "dist").glob(pattern))
    if len(wheels) != 1:
        raise RuntimeError(f"expected one wheel for {item}, found {len(wheels)}")
    return wheels[0].resolve()


def inside():
    from cad_verification import SolidCraftVerification, run_solidcraft_verification
    from scpf.headless import run_document

    result = Path("/output/model_verify")
    native = result / "native"
    native.mkdir(parents=True, exist_ok=True)
    definition = runpy.run_path(str(DEFINITION)).get("VERIFICATION")
    if not isinstance(definition, SolidCraftVerification):
        raise RuntimeError("model-local VERIFICATION must be SolidCraftVerification")

    commands = json.loads(Path("/output/solidcraft.json").read_text(encoding="utf-8"))
    saved = native / "model.sc"
    run_document(
        commands,
        save=saved,
        export=native / "model.step",
        results_out=native / "results.json",
        replay_log_out=native / "replay-log.json",
        work_dir=native / "replay_work",
    )
    report = run_solidcraft_verification(saved, result, definition)
    if report["status"] != "pass":
        print(json.dumps(report, indent=2, default=str), flush=True)
        return 1
    subprocess.run(
        ["solidcraft-cli", "snapshot", str(saved),
         "--out", str(result / "model.png"), "--no-grid", "--no-axes"],
        check=True,
    )
    for path in (saved, native / "model.step", result / "model.png"):
        if not path.is_file() or not path.stat().st_size:
            raise RuntimeError(f"required SolidCraft output missing: {path}")
    print("plate: SolidCraft 0.45.0 model and checks PASS", flush=True)
    return 0


def host():
    if os.environ.get("CAD_CI_ITEM") != "plate":
        raise RuntimeError("pilot supports only the plate item")
    output = Path(os.environ["CAD_CI_OUTPUT"]).resolve()
    output.mkdir(parents=True, exist_ok=True)
    forge = exact_wheel("forge-package", "scpf-*.whl")
    verification = exact_wheel(
        "cad-verification-package", "brainboxemb_cad_verification_lib-*.whl"
    )

    sys.path.insert(0, str(forge))
    from scpf.runner import run_script

    document = run_script(MODEL)
    if not document.get("commands"):
        raise RuntimeError("Forge generated no commands")
    (output / "solidcraft.json").write_text(
        json.dumps(document, indent=2) + "\n",
        encoding="utf-8",
    )
    image = os.environ.get("FORGE_RUNTIME_IMAGE", "")
    if not image.startswith("ghcr.io/brainboxemb/cad-solidcraft:v"):
        raise RuntimeError("immutable released central Docker required")
    subprocess.run(["docker", "pull", image], check=True)
    subprocess.run(
        [
            "docker", "run", "--rm", "--pull=never",
            "-e", "PYTHONPATH=/verification-wheel/" + verification.name
                   + ":/forge-wheel/" + forge.name,
            "-e", "SOLIDCRAFT_GPU=cpu",
            "-v", f"{ROOT}:/workspace:ro",
            "-v", f"{output}:/output",
            "-v", f"{forge.parent}:/forge-wheel:ro",
            "-v", f"{verification.parent}:/verification-wheel:ro",
            "-w", "/workspace",
            image,
            "python", "/workspace/scripts/ci/model_verify_pilot.py",
            "--inside-runtime",
        ],
        cwd=ROOT,
        check=True,
    )
    return 0


if __name__ == "__main__":
    if sys.argv[1:] == ["--inside-runtime"]:
        raise SystemExit(inside())
    if len(sys.argv) != 1:
        raise SystemExit("only --inside-runtime is supported")
    raise SystemExit(host())
