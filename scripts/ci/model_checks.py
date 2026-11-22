"""Load optional model-owned snapshot presentation settings.

CI selection and CAD verification do not live here. A physical model root may
provide check.py solely for snapshot camera/extra-view metadata. Semantic
geometry checks belong in verification/verify.py when they are useful.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

from model_catalog import MODELS

ROOT = Path(__file__).resolve().parents[2]


def model_root(slug: str) -> Path:
    """Return models/<section>/<folder> for one catalog variant."""

    source = Path(MODELS[slug]["source"])
    if len(source.parts) < 3 or source.parts[0] != "models":
        raise ValueError(f"{slug}: invalid model source path {source}")
    return ROOT.joinpath(*source.parts[:3])


def check_path(slug: str) -> Path:
    """Return the optional presentation-settings module for a model root."""

    return model_root(slug) / "check.py"


def load_check(slug: str):
    """Load model-root check.py, returning None when no settings are needed."""

    path = check_path(slug)
    if not path.is_file():
        return None
    spec = importlib.util.spec_from_file_location(
        f"cad_model_check_{slug.replace('-', '_')}",
        path,
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"{slug}: cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def snapshot_camera(slug: str) -> dict | None:
    """Return one optional SolidCraft snapshot camera."""

    module = load_check(slug)
    if module is None:
        return None
    value = getattr(module, "SNAPSHOT_CAMERA", None)
    return value if isinstance(value, dict) else None


def extra_snapshots(slug: str) -> tuple[dict, ...]:
    """Return optional additional named snapshots for the website."""

    module = load_check(slug)
    if module is None:
        return ()
    return tuple(getattr(module, "EXTRA_SNAPSHOTS", ()))
