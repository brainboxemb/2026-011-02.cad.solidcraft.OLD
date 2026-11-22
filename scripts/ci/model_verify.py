#!/usr/bin/env python3
"""Check a prepared CAD model batch inside one SolidCraft runtime.

The released CAD-CI library owns discovery and SCons scheduling. The
consumer-specific batch adapter collects model sources and delegates physical
checks to the separately released CAD verification library.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import runpy
import subprocess
import sys

from bootstrap_cad_ci import dependency
from model_catalog import COMMAND_SOURCES, source_path
from model_checks import extra_snapshots, snapshot_camera


ROOT = Path(__file__).resolve().parents[2]


def dependency_wheel(name: str, pattern: str) -> Path:
    value = os.environ.get("CAD_CI_DEPENDENCIES_JSON", "")
    if not value:
        raise RuntimeError("CAD_CI_DEPENDENCIES_JSON is required")
    entry = json.loads(value).get(name)
    if not isinstance(entry, dict) or not entry.get("output_root"):
        raise RuntimeError(f"required dependency missing: {name}")
    files = tuple((Path(entry["output_root"]) / "dist").glob(pattern))
    if len(files) != 1:
        raise RuntimeError(f"expected one {name} wheel, found {len(files)}")
    return files[0].resolve()


def compile_scpc(slug: str, target: Path, scpc_wheel: Path) -> str:
    """Compile an independent SCPC source from the shared pinned wheel."""

    _, expected = dependency("scpc")
    evidence = json.loads(
        (scpc_wheel.parent.parent / "provenance.json").read_text(encoding="utf-8")
    )
    if evidence.get("commit") != expected:
        raise RuntimeError("SCPC wheel differs from dependencies.repos")
    target.parent.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    previous = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(scpc_wheel) + (
        os.pathsep + previous if previous else ""
    )
    subprocess.run(
        [
            sys.executable, "-m", "scpc",
            str(source_path(ROOT, slug, "scpc")), "--out", str(target),
        ],
        env=env, cwd=ROOT, check=True,
    )
    document = json.loads(target.read_text(encoding="utf-8"))
    if not isinstance(document, dict) or not document.get("commands"):
        raise RuntimeError(f"{slug}: SCPC produced no SolidCraft commands")
    return expected


def compare_independent_geometry(forge_file: Path, scpc_file: Path) -> dict:
    """Compare separately built Forge/SCPC models using released checkers."""

    from cad_verification import compare_bounds, compare_scalar, require_equal

    forge = json.loads(forge_file.read_text(encoding="utf-8"))
    scpc = json.loads(scpc_file.read_text(encoding="utf-8"))
    count = require_equal(
        forge["body_count"], scpc["body_count"],
        label="Forge/SCPC body count",
    )
    left, right = forge["bodies"], scpc["bodies"]
    if len(left) != 1 or len(right) != 1:
        raise RuntimeError(
            "multi-body Forge/SCPC comparison requires a model-specific matcher"
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


def _build_one(row: dict, batch: dict) -> str:
    """Build one model and run optional model-owned semantic verification."""

    from cad_verification import SolidCraftVerification, run_solidcraft_verification
    from scpf.headless import run_document

    slug = row["slug"]
    definition = None
    definition_path = row.get("definition")
    if definition_path:
        definitions = runpy.run_path(str(Path("/workspace") / definition_path))
        by_variant = definitions.get("VERIFICATIONS")
        if by_variant is not None:
            if not isinstance(by_variant, dict):
                raise RuntimeError(f"{slug}: VERIFICATIONS must be a mapping")
            definition = by_variant.get(slug)
        else:
            definition = definitions.get("VERIFICATION")
        if not isinstance(definition, SolidCraftVerification):
            raise RuntimeError(f"{slug}: invalid model verification definition")
        if definition.verification_id != slug:
            raise RuntimeError(f"{slug}: verification identity mismatch")

    root = Path("/output/items") / row["item_path"] / "models" / slug
    saved_dir = root / "native"  # Compatibility output path; do not rename here.
    saved_dir.mkdir(parents=True, exist_ok=True)
    saved = saved_dir / "model.sc"

    commands = json.loads(Path(row["forge_commands"]).read_text(encoding="utf-8"))
    run_document(
        commands,
        save=saved,
        export=saved_dir / "model.step",
        results_out=saved_dir / "results.json",
        replay_log_out=saved_dir / "replay-log.json",
        work_dir=saved_dir / "replay_work",
    )

    semantic_status = "not-configured"
    if definition is not None:
        report = run_solidcraft_verification(
            saved, root / "verification", definition
        )
        if report["status"] != "pass":
            raise RuntimeError(f"{slug}: SolidCraft checks failed: {report}")
        semantic_status = "pass"

    def render_snapshot(target: Path, camera: dict | None = None) -> None:
        """Render one required snapshot with optional model-owned framing."""

        command = [
            "solidcraft-cli", "snapshot", str(saved),
            "--out", str(target), "--no-grid", "--no-axes",
        ]
        if camera:
            command.extend(
                ["--camera", json.dumps(camera, separators=(",", ":"))]
            )
        subprocess.run(command, check=True)
        if not target.is_file() or not target.stat().st_size:
            raise RuntimeError(f"{slug}: snapshot is missing or empty: {target}")

    primary_snapshot = root / "model.png"
    render_snapshot(primary_snapshot, snapshot_camera(slug))
    for spec in extra_snapshots(slug):
        name = spec.get("name")
        if (
            not isinstance(name, str)
            or Path(name).name != name
            or name in {".", ".."}
        ):
            raise RuntimeError(f"{slug}: invalid extra snapshot name {name!r}")
        render_snapshot(saved_dir / name, spec.get("camera"))

    for path in (saved, saved_dir / "model.step", primary_snapshot):
        if not path.is_file() or not path.stat().st_size:
            raise RuntimeError(f"{slug}: required build result missing: {path}")

    comparison = None
    if row.get("scpc_commands"):
        if definition is None:
            raise RuntimeError(
                f"{slug}: independent SCPC comparison requires "
                "model-owned semantic verification"
            )
        scpc_dir = root / "scpc" / "native"
        scpc_dir.mkdir(parents=True, exist_ok=True)
        scpc_saved = scpc_dir / "model.sc"
        scpc_doc = json.loads(
            Path(row["scpc_commands"]).read_text(encoding="utf-8")
        )
        run_document(
            scpc_doc,
            save=scpc_saved,
            export=scpc_dir / "model.step",
            results_out=scpc_dir / "results.json",
            replay_log_out=scpc_dir / "replay-log.json",
            work_dir=scpc_dir / "replay_work",
        )
        scpc_report = run_solidcraft_verification(
            scpc_saved, root / "scpc" / "verification", definition
        )
        if scpc_report["status"] != "pass":
            raise RuntimeError(f"{slug}: independent SCPC checks failed")
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
                "runtime_image": batch["runtime_image"],
                "forge_sha": batch["forge_sha"],
                "scpc_sha": row.get("scpc_sha"),
                "solidcraft_built": True,
                # Compatibility field for existing consumers. Build-only
                # models must never be presented as semantically verified.
                "solidcraft_verified": semantic_status == "pass",
                "semantic_verification": semantic_status,
                "independent_scpc_compared": comparison is not None,
                "source_sha": batch["source_sha"],
            },
            indent=2,
            sort_keys=True,
        ) + "\n", encoding="utf-8",
    )
    print(
        f"{slug}: SolidCraft build PASS; semantic verification "
        f"{semantic_status}; STEP and image saved"
        + ("; independent Forge/SCPC geometry agrees" if comparison else ""),
        flush=True,
    )
    return semantic_status


def run_inside_runtime(manifest_path: Path) -> int:
    """Build all prepared models, collecting errors instead of stopping early."""

    import traceback

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    rows = manifest.get("models")
    if not isinstance(rows, list) or not rows:
        raise RuntimeError("model-build batch has no configured models")

    results = []
    for row in rows:
        slug = row["slug"]
        try:
            if row.get("compile_error"):
                raise RuntimeError(
                    f"SolidCraft command generation failed: {row['compile_error']}"
                )
            semantic_status = _build_one(row, manifest)
            results.append(
                {
                    "model": slug,
                    "status": "pass",
                    "semantic_verification": semantic_status,
                    "error": None,
                }
            )
        except Exception as exc:
            error = "".join(
                traceback.format_exception_only(type(exc), exc)
            ).strip()
            print(f"{slug}: SolidCraft build/check ERROR: {error}", flush=True)
            results.append(
                {
                    "model": slug,
                    "status": "fail",
                    "semantic_verification": (
                        "configured" if row.get("definition") else "not-configured"
                    ),
                    "error": error,
                }
            )

    failed = any(item["status"] != "pass" for item in results)
    report = {
        "schema": 1,
        "source_sha": manifest["source_sha"],
        "status": "fail" if failed else "pass",
        "model_count": len(results),
        "models": results,
    }
    (manifest_path.parent / "batch-report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        "SolidCraft build batch: " + ", ".join(
            f"{item['model']}={item['status']}" for item in results
        ), flush=True,
    )
    return 1 if failed else 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inside-runtime", action="store_true")
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    if not args.inside_runtime or args.manifest is None:
        parser.error("--inside-runtime and --manifest are required")
    raise SystemExit(run_inside_runtime(args.manifest))
