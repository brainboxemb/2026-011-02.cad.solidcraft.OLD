#!/usr/bin/env python3
"""Produce CAD-owned models; delegate scheduling and checking to released tools.

lib.py.cad.ci owns selected items, their dependency graph and output reuse.
lib.py.cad.verification owns SolidCraft checks. This producer only compiles
the selected model source and replays it in the released SolidCraft runtime.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import runpy
import subprocess
import sys

from bootstrap_cad_ci import dependency
from model_catalog import COMMAND_SOURCES, MODELS, source_path
from model_checks import command_check


ROOT = Path(__file__).resolve().parents[2]


def selected_models() -> tuple[str, ...]:
    """Find source variants from the authoritative catalog, never a CI list."""

    raw = os.environ.get("CAD_CI_ITEM_PATH", "").strip()
    if not raw:
        raise RuntimeError("CAD_CI_ITEM_PATH is required")
    item = Path(raw)
    if not item.is_absolute():
        item = ROOT / item
    relative = item.resolve().relative_to(ROOT.resolve())
    if len(relative.parts) != 3 or relative.parts[0] != "models":
        raise RuntimeError(f"not a physical model root: {relative}")

    models = tuple(
        slug for slug, meta in MODELS.items()
        if Path(*Path(meta["source"]).parts[:3]) == relative
    )
    if not models:
        raise RuntimeError(f"no catalog variants owned by {relative}")
    name = os.environ.get("CAD_CI_ITEM", "").strip()
    if not name or name != models[0]:
        raise RuntimeError(
            f"item identity mismatch: expected {models[0]!r}, found {name!r}"
        )
    return models


def output_root() -> Path:
    value = os.environ.get("CAD_CI_OUTPUT", "").strip()
    if not value:
        raise RuntimeError("CAD_CI_OUTPUT is required")
    return Path(value).resolve()


def dependency_wheel(name: str, pattern: str) -> Path:
    value = os.environ.get("CAD_CI_DEPENDENCIES_JSON", "")
    if not value:
        raise RuntimeError("CAD_CI_DEPENDENCIES_JSON is required")
    entry = json.loads(value).get(name)
    if not isinstance(entry, dict) or not entry.get("output_root"):
        raise RuntimeError(f"required dependency missing: {name}")
    files = tuple((Path(entry["output_root"]) / "dist").glob(pattern))
    if len(files) != 1:
        raise RuntimeError(
            f"expected exactly one {name} wheel, found {len(files)}"
        )
    return files[0].resolve()


def compile_scpc(slug: str, target: Path, scpc_wheel: Path) -> str:
    """Compile SCPC using the finished shared dependency wheel.

    Model jobs never checkout shared SCPC sources, so parallel builds cannot
    conflict with one another.
    """

    _, wanted = dependency("scpc")
    metadata = json.loads(
        (scpc_wheel.parent.parent / "provenance.json").read_text(encoding="utf-8")
    )
    if metadata.get("commit") != wanted:
        raise RuntimeError("SCPC wheel provenance differs from pinned source")
    target.parent.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    current = env.get("PYTHONPATH", "")
    source = str(scpc_wheel)
    env["PYTHONPATH"] = source if not current else source + os.pathsep + current
    subprocess.run(
        [
            sys.executable, "-m", "scpc", str(source_path(ROOT, slug, "scpc")),
            "--out", str(target),
        ],
        env=env, cwd=ROOT, check=True,
    )
    value = json.loads(target.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not value.get("commands"):
        raise RuntimeError(f"{slug}: SCPC produced no commands")
    return wanted

def run_host() -> int:
    slugs = selected_models()
    output = output_root()
    output.mkdir(parents=True, exist_ok=True)

    forge = dependency_wheel("forge-package", "scpf-*.whl")
    verifier = dependency_wheel(
        "cad-verification-package", "brainboxemb_cad_verification_lib-*.whl"
    )
    if str(forge) not in sys.path:
        sys.path.insert(0, str(forge))
    from scpf.runner import run_script

    scpc_wheel = (
        dependency_wheel("scpc-package", "scpc-*.whl")
        if any(slug in COMMAND_SOURCES for slug in slugs)
        else None
    )
    rows = []
    for slug in slugs:
        commands = output / "generated" / slug / "scpf" / "solidcraft.json"
        commands.parent.mkdir(parents=True, exist_ok=True)
        document = run_script(source_path(ROOT, slug))
        if not isinstance(document, dict) or not document.get("commands"):
            raise RuntimeError(f"{slug}: Forge returned no CAD commands")
        commands.write_text(
            json.dumps(document, indent=2) + "\n", encoding="utf-8"
        )
        command_check(slug, commands)

        verification = ROOT / Path(*Path(MODELS[slug]["source"]).parts[:3])
        verification = verification / "verification" / "verify.py"
        if not verification.is_file():
            raise RuntimeError(f"{slug}: missing model-local verification definition")

        scpc = None
        scpc_sha = None
        if slug in COMMAND_SOURCES:
            scpc = output / "generated" / slug / "scpc" / "solidcraft.json"
            if scpc_wheel is None:
                raise RuntimeError("SCPC wheel missing for independent source")
            scpc_sha = compile_scpc(slug, scpc, scpc_wheel)

        rows.append({
            "slug": slug,
            "forge_commands": f"/output/generated/{slug}/scpf/solidcraft.json",
            "scpc_commands": (
                f"/output/generated/{slug}/scpc/solidcraft.json" if scpc else None
            ),
            "definition": str(verification.relative_to(ROOT)),
            "scpc_sha": scpc_sha,
        })

    image = os.environ.get("FORGE_RUNTIME_IMAGE", "").strip()
    if not image.startswith("ghcr.io/brainboxemb/cad-solidcraft:v"):
        raise RuntimeError("released central SolidCraft runtime is required")
    _, forge_sha = dependency("scpf")
    manifest = {
        "schema": 1,
        "item": os.environ["CAD_CI_ITEM"],
        "runtime_image": image,
        "forge_sha": forge_sha,
        "models": rows,
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    subprocess.run(["docker", "pull", image], check=True)
    subprocess.run(
        [
            "docker", "run", "--rm", "--pull=never",
            "-e", "PYTHONPATH=/verification-wheel/" + verifier.name
                   + ":/forge-wheel/" + forge.name,
            "-e", "SOLIDCRAFT_GPU=cpu",
            "-v", f"{ROOT}:/workspace:ro",
            "-v", f"{output}:/output",
            "-v", f"{forge.parent}:/forge-wheel:ro",
            "-v", f"{verifier.parent}:/verification-wheel:ro",
            "-w", "/workspace", image,
            "python", "/workspace/scripts/ci/model_verify.py",
            "--inside-runtime",
        ],
        cwd=ROOT,
        check=True,
    )
    return 0


def compare_independent_geometry(forge_file: Path, scpc_file: Path) -> dict:
    """Use released numeric comparisons for two independently built shapes."""

    from cad_verification import compare_bounds, compare_scalar, require_equal

    forge = json.loads(forge_file.read_text(encoding="utf-8"))
    scpc = json.loads(scpc_file.read_text(encoding="utf-8"))
    count = require_equal(
        forge["body_count"], scpc["body_count"],
        label="Forge/SCPC body count",
    )
    left = forge["bodies"]
    right = scpc["bodies"]
    if len(left) != 1 or len(right) != 1:
        raise RuntimeError(
            "multi-body independent comparisons require a model-local matcher"
        )
    bounds = compare_bounds(
        left[0]["bbox"]["min"], left[0]["bbox"]["max"],
        right[0]["bbox"]["min"], right[0]["bbox"]["max"],
        0.005, label="Forge/SCPC bounds",
    )
    volume = compare_scalar(
        left[0]["volume_mm3"], right[0]["volume_mm3"],
        0.05, label="Forge/SCPC volume (mm³)",
    )
    return {
        "schema": 1,
        "status": "pass",
        "body_count": count,
        "bounds": bounds,
        "volume": volume,
    }


def run_inside_runtime() -> int:
    from cad_verification import SolidCraftVerification, run_solidcraft_verification
    from scpf.headless import run_document

    output = Path("/output")
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("schema") != 1 or not manifest.get("models"):
        raise RuntimeError("model producer manifest has no selected variants")

    for row in manifest["models"]:
        slug = row["slug"]
        definition = runpy.run_path(
            str(Path("/workspace") / row["definition"])
        ).get("VERIFICATION")
        if not isinstance(definition, SolidCraftVerification):
            raise RuntimeError(f"{slug}: invalid SolidCraftVerification definition")
        root = output / "models" / slug
        native = root / "native"
        native.mkdir(parents=True, exist_ok=True)
        saved = native / "model.sc"
        commands = json.loads(Path(row["forge_commands"]).read_text(encoding="utf-8"))
        run_document(
            commands,
            save=saved,
            export=native / "model.step",
            results_out=native / "results.json",
            replay_log_out=native / "replay-log.json",
            work_dir=native / "replay_work",
        )
        report = run_solidcraft_verification(saved, root / "verification", definition)
        if report["status"] != "pass":
            print(json.dumps(report, indent=2, default=str), flush=True)
            return 1

        subprocess.run(
            [
                "solidcraft-cli", "snapshot", str(saved),
                "--out", str(root / "model.png"), "--no-grid", "--no-axes",
            ],
            check=True,
        )
        for expected in (saved, native / "model.step", root / "model.png"):
            if not expected.is_file() or not expected.stat().st_size:
                raise RuntimeError(f"{slug}: missing required artifact {expected}")

        comparison = None
        if row.get("scpc_commands"):
            native_scpc = root / "scpc" / "native"
            native_scpc.mkdir(parents=True, exist_ok=True)
            scpc_saved = native_scpc / "model.sc"
            scpc_doc = json.loads(
                Path(row["scpc_commands"]).read_text(encoding="utf-8")
            )
            run_document(
                scpc_doc,
                save=scpc_saved,
                export=native_scpc / "model.step",
                results_out=native_scpc / "results.json",
                replay_log_out=native_scpc / "replay-log.json",
                work_dir=native_scpc / "replay_work",
            )
            scpc_report = run_solidcraft_verification(
                scpc_saved, root / "scpc" / "verification", definition
            )
            if scpc_report["status"] != "pass":
                print(json.dumps(scpc_report, indent=2, default=str), flush=True)
                return 1
            comparison = compare_independent_geometry(
                root / "verification" / "baseline" / "measurements.json",
                root / "scpc" / "verification" / "baseline" / "measurements.json",
            )
            (root / "scpc" / "comparison.json").write_text(
                json.dumps(comparison, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )

        (root / "provenance.json").write_text(
            json.dumps(
                {
                    "schema": 1,
                    "model": slug,
                    "runtime_image": manifest["runtime_image"],
                    "forge_sha": manifest["forge_sha"],
                    "scpc_sha": row["scpc_sha"],
                    "solidcraft_verified": True,
                    "independent_scpc_compared": comparison is not None,
                },
                indent=2,
                sort_keys=True,
            ) + "\n",
            encoding="utf-8",
        )
        print(
            f"{slug}: SolidCraft model built, STEP/preview saved, checks PASS"
            + ("; independent SCPC geometry comparison PASS" if comparison else ""),
            flush=True,
        )
    return 0


if __name__ == "__main__":
    if sys.argv[1:] == ["--inside-runtime"]:
        raise SystemExit(run_inside_runtime())
    if len(sys.argv) != 1:
        raise SystemExit("only --inside-runtime is supported")
    raise SystemExit(run_host())
