#!/usr/bin/env python3
"""Check out the exact external repositories used by this CAD repository."""

from __future__ import annotations

from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "dependencies.repos"
DEPENDENCIES = ("scpf", "scpc", "cad-ci")


def dependency(name: str, root: Path = ROOT) -> tuple[str, str]:
    """Return one exact Git URL and 40-character revision from the manifest."""

    text = (root / "dependencies.repos").read_text(encoding="utf-8")
    section = re.search(
        rf"(?ms)^  {re.escape(name)}:\s*\n(.*?)(?=^  [\w-]+:|\Z)",
        text,
    )
    if section is None:
        raise RuntimeError(f"dependencies.repos has no {name} entry")

    url = re.search(r"(?m)^    url:\s*(\S+)\s*$", section[1])
    sha = re.search(r"(?m)^    version:\s*([0-9a-f]{40})\s*$", section[1])
    if url is None or sha is None:
        raise RuntimeError(f"{name} requires a Git URL and exact commit SHA")
    return url[1], sha[1]


def _git(target: Path, *args: str, check: bool = True) -> str:
    """Run Git for one external checkout and return stripped stdout."""

    completed = subprocess.run(
        ["git", "-C", str(target), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and completed.returncode != 0:
        message = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(message or "git command failed")
    return completed.stdout.strip()


def ensure_checkout(
    name: str,
    root: Path = ROOT,
    *,
    target: Path | None = None,
) -> str:
    """Make one external checkout match dependencies.repos exactly."""

    url, wanted = dependency(name, root)
    target = target or (root / "ext" / name)
    target.parent.mkdir(parents=True, exist_ok=True)

    if (target / ".git").is_dir():
        current = _git(target, "rev-parse", "HEAD")
        if current != wanted:
            dirty = _git(target, "status", "--porcelain", "--untracked-files=no")
            if dirty:
                raise RuntimeError(
                    f"{name} has tracked local changes; preserve them before updating"
                )
            _git(target, "remote", "set-url", "origin", url)
            _git(target, "fetch", "origin", wanted)
            _git(
                target,
                "-c",
                "advice.detachedHead=false",
                "checkout",
                "--detach",
                wanted,
            )
    else:
        if target.exists():
            raise RuntimeError(
                f"{target} exists but is not a Git checkout; move it aside first"
            )
        subprocess.run(
            ["git", "clone", "--quiet", "--no-checkout", "--", url, str(target)],
            check=True,
        )
        _git(
            target,
            "-c",
            "advice.detachedHead=false",
            "checkout",
            "--detach",
            wanted,
        )

    actual = _git(target, "rev-parse", "HEAD")
    if actual != wanted:
        raise RuntimeError(
            f"{name} revision mismatch: expected {wanted}, found {actual}"
        )
    return actual


def ensure_dependencies(root: Path = ROOT) -> dict[str, str]:
    """Check out all exact consumer dependencies without installing them."""

    return {
        name: ensure_checkout(name, root)
        for name in DEPENDENCIES
    }


def main() -> int:
    """Prepare exact source checkouts for host tooling and container mounts."""

    for name, sha in ensure_dependencies().items():
        print(f"Ready: {name} at {sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
