"""Model catalog derived exclusively from model-owned model.yml files.

Forge uses the same model.yml convention for site-facing metadata. This
module preserves the existing CAD API while eliminating the independent
hand-written Python catalog. The website reads these model files via MODELS;
ci.yml continues to own build execution, not presentation.
"""

from __future__ import annotations

from pathlib import Path
import argparse
import re

import yaml


ROOT = Path(__file__).resolve().parents[2]
SLUG_RE = re.compile(r"^[a-z][a-z0-9-]+$")

SECTION_INFO = {
    "basic": (
        "Basic Models",
        "Small, transparent models used to develop and verify SCPF features.",
    ),
    "components": (
        "Components",
        "Reusable physical parts compiled directly from the same source assemblies import.",
    ),
    "advanced": (
        "Advanced Models",
        "Full designs and nested native assemblies built from reusable components.",
    ),
}


def _require_text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label}: expected non-empty text")
    return value


def _path_from_model(root, value, label, *, directory_ok=False):
    """Resolve a local model-relative path or an explicit repo-relative path."""

    text = _require_text(value, label)
    if text.startswith("/") or "\\" in text:
        raise ValueError(f"{label}: expected a repository-relative POSIX path")
    path = Path(text) if text.startswith("models/") else root / text
    if ".." in path.parts:
        raise ValueError(f"{label}: parent traversal is not allowed")
    absolute = (ROOT / path).resolve()
    if not absolute.is_relative_to(ROOT.resolve()):
        raise ValueError(f"{label}: source path escaped the CAD repository")
    if directory_ok:
        if not absolute.exists():
            raise ValueError(f"{label}: declared input does not exist: {path}")
    elif not absolute.is_file():
        raise ValueError(f"{label}: declared source does not exist: {path}")
    return path.as_posix() + (
        "/" if directory_ok and text.endswith("/") else ""
    )


def _model_entry(slug, info, section, root, path):
    label = f"{path} [{slug}]"
    if not SLUG_RE.fullmatch(slug):
        raise ValueError(f"{label}: invalid model slug")
    if not isinstance(info, dict):
        raise ValueError(f"{label}: expected a YAML mapping")

    required = ("priority", "title", "tagline", "description",
                "parameters", "diagram", "stages", "source")
    optional = ("scpc_source", "component_source",
                "component_definition_primary", "extra_inputs",
                "dependencies", "warning", "build", "snapshot_required",
                "featured", "extra_views", "allow_stale_preview")
    unknown = set(info) - set(required) - set(optional)
    if unknown:
        raise ValueError(f"{label}: unknown metadata keys {sorted(unknown)}")
    for key in required:
        if key not in info:
            raise ValueError(f"{label}: missing {key}")
    priority = info["priority"]
    if type(priority) is not int or priority < 0:
        raise ValueError(f"{label}: priority must be a nonnegative integer")

    entry = {"section": section}
    for key in ("title", "tagline", "description", "parameters", "diagram"):
        entry[key] = _require_text(info[key], f"{label}.{key}")
    stages = info["stages"]
    if not isinstance(stages, list) or not stages:
        raise ValueError(f"{label}.stages: expected non-empty list")
    entry["stages"] = [
        _require_text(value, f"{label}.stages") for value in stages
    ]

    entry["source"] = _path_from_model(
        root, info["source"], f"{label}.source"
    )
    if "scpc_source" in info:
        entry["scpc_source"] = _path_from_model(
            root, info["scpc_source"], f"{label}.scpc_source"
        )
    if "component_source" in info:
        entry["component_source"] = _path_from_model(
            root, info["component_source"], f"{label}.component_source"
        )
    for key in ("extra_inputs", "dependencies"):
        if key in info:
            raw = info[key]
            if not isinstance(raw, list) or not all(
                isinstance(v, str) and v for v in raw
            ):
                raise ValueError(f"{label}.{key}: expected list of strings")
            entry[key] = (
                tuple(_path_from_model(
                    root, v, f"{label}.{key}", directory_ok=True,
                ) for v in raw)
                if key == "extra_inputs"
                else tuple(raw)
            )
    if "warning" in info:
        warning = info["warning"]
        if not isinstance(warning, dict) or set(warning) != {"title", "body"}:
            raise ValueError(f"{label}.warning: expected title and body")
        entry["warning"] = {
            key: _require_text(warning[key], f"{label}.warning.{key}")
            for key in ("title", "body")
        }
    if "extra_views" in info:
        views = info["extra_views"]
        if not isinstance(views, dict) or set(views) - {
            "title", "note", "verified_only", "items"
        }:
            raise ValueError(f"{label}.extra_views: invalid fields")
        title = _require_text(views.get("title"), f"{label}.extra_views.title")
        items = views.get("items")
        if not isinstance(items, list) or not items:
            raise ValueError(f"{label}.extra_views.items: expected non-empty list")
        normalized = []
        for view in items:
            if not isinstance(view, dict) or set(view) != {
                "kind", "src", "alt", "caption"
            }:
                raise ValueError(f"{label}: invalid supplementary view")
            kind = view["kind"]
            if kind not in ("url", "asset", "build"):
                raise ValueError(f"{label}: invalid view kind {kind!r}")
            source = _require_text(view["src"], f"{label}.extra_views.src")
            if kind == "url":
                if not source.startswith("https://"):
                    raise ValueError(f"{label}: external view must use HTTPS")
            else:
                if Path(source).name != source or source in (".", ".."):
                    raise ValueError(f"{label}: view file must be a local filename")
                if kind == "asset":
                    _path_from_model(root, source, f"{label}.extra_views.asset")
            normalized.append({
                "kind": kind,
                "src": source,
                "alt": _require_text(view["alt"], f"{label}.extra_views.alt"),
                "caption": _require_text(
                    view["caption"], f"{label}.extra_views.caption"
                ),
            })
        verified_only = views.get("verified_only", False)
        if type(verified_only) is not bool:
            raise ValueError(f"{label}.extra_views.verified_only: expected boolean")
        entry["extra_views"] = {
            "title": title,
            "note": _require_text(views["note"], f"{label}.extra_views.note")
            if "note" in views else "",
            "verified_only": verified_only,
            "items": normalized,
        }

    for key in ("component_definition_primary", "featured",
                "allow_stale_preview"):
        if key in info:
            if type(info[key]) is not bool:
                raise ValueError(f"{label}.{key}: expected boolean")
            entry[key] = info[key]

    # These old API keys remain available for the current result publisher.
    for new, old in (
        ("build", "native"),
        ("snapshot_required", "native_snapshot_required"),
    ):
        if new in info and type(info[new]) is not bool:
            raise ValueError(f"{label}.{new}: expected boolean")
        entry[old] = info.get(new, False)
    return priority, entry


class _UniqueKeysLoader(yaml.SafeLoader):
    """Reject duplicate YAML mapping keys instead of silently losing data."""


def _construct_unique_map(loader, node):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=True)
        if key in result:
            raise ValueError(f"duplicate YAML key: {key!r}")
        result[key] = loader.construct_object(value_node, deep=True)
    return result


_UniqueKeysLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_map,
)


def load_models(root=ROOT):
    """Read, validate and order every CAD model without a second catalog."""

    catalog = []
    seen = set()
    priorities = set()
    files = sorted(root.glob("models/*/*/model.yml"))
    ci_files = sorted(root.glob("models/*/*/ci.yml"))
    if {p.parent for p in files} != {p.parent for p in ci_files}:
        raise ValueError("every physical CAD model root needs exactly one model.yml and ci.yml")

    for path in files:
        model_root = path.parent.relative_to(root)
        section = model_root.parts[1]
        if section not in SECTION_INFO:
            raise ValueError(f"{path}: unknown model section")
        document = yaml.load(path.read_text(encoding="utf-8"), Loader=_UniqueKeysLoader)
        if not isinstance(document, dict):
            raise ValueError(f"{path}: expected model.yml mapping")
        if document.get("section") != section:
            raise ValueError(f"{path}: section differs from model folder")

        ci_file = path.parent / "ci.yml"
        ci = yaml.load(ci_file.read_text(encoding="utf-8"), Loader=_UniqueKeysLoader)
        if not isinstance(ci, dict):
            raise ValueError(f"{ci_file}: expected a mapping")
        owner = _require_text(ci.get("id"), f"{ci_file}.id")

        if "variants" in document:
            if set(document) != {"section", "variants"}:
                raise ValueError(f"{path}: unsupported root fields alongside variants")
            variants = document["variants"]
            if not isinstance(variants, dict) or len(variants) < 2:
                raise ValueError(f"{path}: variants requires 2+ catalog models")
            if owner not in variants:
                raise ValueError(f"{path}: CI owner is absent from variants")
        else:
            variants = {owner: {k: v for k, v in document.items()
                                if k != "section"}}

        for slug, info in variants.items():
            if slug in seen:
                raise ValueError(f"duplicate model slug: {slug}")
            seen.add(slug)
            priority, entry = _model_entry(slug, info, section, model_root, path)
            if (section, priority) in priorities:
                raise ValueError(f"{path}: duplicate section priority {priority}")
            priorities.add((section, priority))
            catalog.append((list(SECTION_INFO).index(section), priority, slug, entry))

    catalog.sort(key=lambda row: (row[0], row[1], row[2]))
    table = {slug: entry for _, _, slug, entry in catalog}
    for slug, entry in table.items():
        for dependency in entry.get("dependencies", ()):
            if dependency not in table:
                raise ValueError(f"{slug}: unknown dependency {dependency}")
            if dependency == slug:
                raise ValueError(f"{slug}: model cannot depend on itself")
    return table


MODELS = load_models()


SOURCES = {slug: model["source"] for slug, model in MODELS.items()}
COMMAND_SOURCES = {
    slug: model["scpc_source"]
    for slug, model in MODELS.items()
    if model.get("scpc_source")
}
COMPONENT_SOURCES = {
    slug: model["component_source"]
    for slug, model in MODELS.items()
    if model.get("component_source")
}
COMPONENT_DEFINITION_PRIMARY = frozenset(
    slug
    for slug, model in MODELS.items()
    if model.get("component_definition_primary")
)
SECTIONS = {
    key: (
        title,
        description,
        tuple(
            slug
            for slug, model in MODELS.items()
            if model["section"] == key
        ),
    )
    for key, (title, description) in SECTION_INFO.items()
}


def _model_root(path):
    """Return the model/package root before a language directory."""
    value = Path(path).as_posix()
    for marker in ("/scpf/", "/scpc/"):
        if marker in value:
            return value.split(marker, 1)[0] + "/"
    return str(Path(value).parent.as_posix()) + "/"


def model_build_path(slug):
    """Return the source-file path without .py as this build item's directory."""
    if slug not in MODELS:
        raise ValueError(f"unknown model: {slug}")
    return Path(MODELS[slug]["source"]).with_suffix("")


def direct_input_paths(slug):
    """Geometry/source paths whose change directly affects one catalog model.

    These paths propagate through declared model dependencies.
    Model-root metadata is intentionally kept separate so README or snapshot
    settings changes do not rebuild dependent assemblies.
    """
    model = MODELS[slug]
    paths = {model["source"]}
    if model.get("scpc_source"):
        paths.add(model["scpc_source"])
    if model.get("component_source"):
        paths.add(model["component_source"])
    paths.update(model.get("extra_inputs", ()))
    return tuple(sorted(paths))


def model_metadata_paths(slug):
    """Model-root metadata that affects only the owning model."""
    root = _model_root(MODELS[slug]["source"])
    # model.yml is website metadata. It must not enter geometry fingerprints.
    # model_build_path/source geometry lives outside the metadata-only list.
    physical = Path(*Path(MODELS[slug]["source"]).parts[:3]).as_posix() + "/"
    return (
        physical + "model.yml",
        physical + "README.md",
        physical + "check.py",
    )


def model_dependencies(slug):
    """Catalog-model dependencies used by change selection."""
    return tuple(MODELS[slug].get("dependencies", ()))


def dependency_closure(slug):
    """Return slug plus all declared catalog dependencies."""
    result = []
    seen = set()

    def visit(current):
        if current in seen:
            return
        if current not in MODELS:
            raise ValueError(f"unknown model dependency: {current}")
        seen.add(current)
        result.append(current)
        for dependency in model_dependencies(current):
            visit(dependency)

    visit(slug)
    return tuple(result)


def verification_input_paths(slug):
    """Geometry/source paths that define one model's native CAD result."""
    paths = set()
    for dependency in dependency_closure(slug):
        paths.update(direct_input_paths(dependency))
    return tuple(sorted(paths))


def model_input_paths(slug):
    """All paths whose change should select one model for rebuild/publication.

    Native verification is based only on verification_input_paths(). Model-root
    README/check metadata belongs to selection, not to the geometry fingerprint.
    """
    paths = set(verification_input_paths(slug))
    paths.update(model_metadata_paths(slug))
    return tuple(sorted(paths))


def model_slugs(kind="scpf"):
    if kind == "scpf":
        return tuple(MODELS)
    if kind == "scpc":
        return tuple(COMMAND_SOURCES)
    if kind == "native":
        return tuple(
            slug for slug, model in MODELS.items()
            if model.get("native")
        )
    if kind == "native-snapshot-required":
        return tuple(
            slug for slug, model in MODELS.items()
            if model.get("native_snapshot_required")
        )
    raise ValueError(f"unknown model selection: {kind}")


def source_path(root, slug, language="scpf"):
    if language == "scpf":
        return Path(root) / SOURCES[slug]
    if language == "scpc":
        return Path(root) / COMMAND_SOURCES[slug]
    raise ValueError("language must be scpf or scpc")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("slug", nargs="?")
    parser.add_argument("language", nargs="?", choices=("scpf", "scpc"), default="scpf")
    parser.add_argument(
        "--list",
        dest="list_kind",
        choices=("scpf", "scpc", "native", "native-snapshot-required"),
    )
    parser.add_argument(
        "--count",
        dest="count_kind",
        choices=("scpf", "scpc", "native", "native-snapshot-required"),
    )
    args = parser.parse_args()

    if args.list_kind:
        print(" ".join(model_slugs(args.list_kind)))
        return
    if args.count_kind:
        print(len(model_slugs(args.count_kind)))
        return
    if not args.slug:
        parser.error("provide a model slug or --list/--count")

    table = SOURCES if args.language == "scpf" else COMMAND_SOURCES
    if args.slug not in table:
        raise SystemExit(f"Unknown {args.language} model: {args.slug}")
    print(table[args.slug])


if __name__ == "__main__":
    main()
