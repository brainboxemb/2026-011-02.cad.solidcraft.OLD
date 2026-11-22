#!/usr/bin/env python3
"""Compile enabled CAD models, then build/check them in one SolidCraft runtime.

This is the CAD-specific source adapter for Forge's existing shared batch
pattern. The released CAD-CI library handles item discovery, Git selection,
SCons planning, dependencies and materializing each model's build results.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import traceback

import yaml

from bootstrap_cad_ci import dependency
from model_catalog import COMMAND_SOURCES, MODELS, source_path
from model_checks import command_check
from model_verify import compile_scpc, dependency_wheel


ROOT = Path(__file__).resolve().parents[2]


def configured_model_roots() -> tuple[tuple[Path, tuple[str, ...]], ...]:
    """Read model-local process flags; no separate CI model allowlist."""

    roots: list[tuple[Path, tuple[str, ...]]] = []
    for config_path in sorted(ROOT.glob("models/*/*/ci.yml")):
        config = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        if config.get("process", True) is False:
            continue
        if config.get("template") != "cad-model-build":
            raise RuntimeError(f"{config_path}: not using shared build template")
        model_root = config_path.parent.relative_to(ROOT)
        variants = tuple(
            slug for slug, metadata in MODELS.items()
            if Path(*Path(metadata["source"]).parts[:3]) == model_root
        )
        if not variants:
            raise RuntimeError(f"{model_root}: missing catalog source variants")
        if config.get("id") != variants[0]:
            raise RuntimeError(
                f"{model_root}: id does not match catalog primary {variants[0]}"
            )
        roots.append((model_root, variants))
    if not roots:
        raise RuntimeError("no processed CAD model roots")
    return tuple(roots)


def source_sha() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True,
    ).strip()


def write_manifest(batch_output: Path, forge_wheel: Path, scpc_wheel: Path) -> Path:
    """Prepare every model before launching the SolidCraft container."""

    if str(forge_wheel) not in sys.path:
        sys.path.insert(0, str(forge_wheel))
    from scpf.runner import run_script

    rows = []
    for model_root, variants in configured_model_roots():
        item_output = batch_output / "items" / model_root
        item_output.mkdir(parents=True, exist_ok=True)
        (item_output / "generated").mkdir(exist_ok=True)
        (item_output / "models").mkdir(exist_ok=True)

        for slug in variants:
            error = None
            scpc_sha = None
            command_file = item_output / "generated" / slug / "scpf" / "solidcraft.json"
            scpc_file = item_output / "generated" / slug / "scpc" / "solidcraft.json"
            try:
                command_file.parent.mkdir(parents=True, exist_ok=True)
                document = run_script(source_path(ROOT, slug))
                if not isinstance(document, dict) or not document.get("commands"):
                    raise RuntimeError(f"{slug}: Forge generated no commands")
                command_file.write_text(
                    json.dumps(document, indent=2) + "\n",
                    encoding="utf-8",
                )
                command_check(slug, command_file)

                if slug in COMMAND_SOURCES:
                    scpc_sha = compile_scpc(slug, scpc_file, scpc_wheel)
                verification = ROOT / model_root / "verification" / "verify.py"
                if not verification.is_file():
                    raise RuntimeError(
                        f"{slug}: missing model-local verification/verify.py"
                    )
            except Exception as exc:
                error = "".join(
                    traceback.format_exception_only(type(exc), exc)
                ).strip()
                print(f"{slug}: command generation ERROR: {error}", flush=True)

            row = {
                "slug": slug,
                "item_path": model_root.as_posix(),
                "forge_commands": "/output/items/"
                + model_root.as_posix()
                + f"/generated/{slug}/scpf/solidcraft.json",
                "scpc_commands": (
                    "/output/items/" + model_root.as_posix()
                    + f"/generated/{slug}/scpc/solidcraft.json"
                    if slug in COMMAND_SOURCES else None
                ),
                "definition": (
                    model_root / "verification" / "verify.py"
                ).as_posix(),
                "scpc_sha": scpc_sha,
                "compile_error": error,
            }
            rows.append(row)

        # This becomes a model-local build output through CAD-CI copy:.
        (item_output / "manifest.json").write_text(
            json.dumps(
                {
                    "schema": 1,
                    "item_path": model_root.as_posix(),
                    "models": [row["slug"] for row in rows
                               if row["item_path"] == model_root.as_posix()],
                },
                indent=2,
                sort_keys=True,
            ) + "\n", encoding="utf-8",
        )

    image = os.environ.get("FORGE_RUNTIME_IMAGE", "").strip()
    if not image.startswith("ghcr.io/brainboxemb/cad-solidcraft:v"):
        raise RuntimeError("released central SolidCraft container required")
    _, forge_sha = dependency("scpf")
    batch = {
        "schema": 1,
        "source_sha": source_sha(),
        "runtime_image": image,
        "forge_sha": forge_sha,
        "models": rows,
    }
    path = batch_output / "manifest.json"
    path.write_text(
        json.dumps(batch, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        f"SolidCraft batch prepared: {len(roots_summary(rows))} model roots, "
        f"{len(rows)} model variants",
        flush=True,
    )
    return path


def roots_summary(rows: list[dict]) -> set[str]:
    return {row["item_path"] for row in rows}


def run_batch() -> int:
    """Start Docker once after collecting all models and their commands."""

    started = time.perf_counter()
    output_env = os.environ.get("CAD_CI_OUTPUT", "").strip()
    if not output_env:
        raise RuntimeError("CAD_CI_OUTPUT is required")
    output = Path(output_env).resolve()
    items = output / "items"
    if items.exists():
        shutil.rmtree(items)
    output.mkdir(parents=True, exist_ok=True)

    forge = dependency_wheel("forge-package", "scpf-*.whl")
    scpc = dependency_wheel("scpc-package", "scpc-*.whl")
    checks = dependency_wheel(
        "cad-verification-package", "brainboxemb_cad_verification_lib-*.whl",
    )
    compile_started = time.perf_counter()
    manifest_path = write_manifest(output, forge, scpc)
    print(
        f"CAD BUILD TIMING command_generation_s="
        f"{time.perf_counter() - compile_started:.3f}",
        flush=True,
    )

    image = json.loads(manifest_path.read_text())["runtime_image"]
    pull_started = time.perf_counter()
    subprocess.run(["docker", "pull", image], check=True)
    print(
        f"CAD BUILD TIMING image_pull_s="
        f"{time.perf_counter() - pull_started:.3f}",
        flush=True,
    )

    runtime_started = time.perf_counter()
    finished = subprocess.run(
        [
            "docker", "run", "--rm", "--pull=never",
            "-e", "PYTHONPATH=/cad-verification/" + checks.name
            + ":/forge-package/" + forge.name,
            "-e", "SOLIDCRAFT_GPU=cpu",
            "-v", f"{ROOT}:/workspace:ro",
            "-v", f"{output}:/output",
            "-v", f"{forge.parent}:/forge-package:ro",
            "-v", f"{checks.parent}:/cad-verification:ro",
            "-w", "/workspace",
            image,
            "python", "/workspace/scripts/ci/model_verify.py",
            "--inside-runtime", "--manifest", "/output/manifest.json",
        ],
        cwd=ROOT, check=False,
    )
    print(
        f"CAD BUILD TIMING container_s="
        f"{time.perf_counter() - runtime_started:.3f}",
        flush=True,
    )
    print(
        f"CAD BUILD TIMING total_s={time.perf_counter() - started:.3f}; "
        "docker_run_count=1",
        flush=True,
    )
    return finished.returncode


if __name__ == "__main__":
    if sys.argv[1:]:
        raise SystemExit("model_build_batch.py takes no positional arguments")
    raise SystemExit(run_batch())
