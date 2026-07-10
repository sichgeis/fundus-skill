#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def main() -> int:
    if len(sys.argv) != 4:
        print(
            "usage: verify_release_consistency.py <source-manifest> <plugin-build-dir> <marketplace-dir>",
            file=sys.stderr,
        )
        return 2

    source_manifest_path = Path(sys.argv[1]).resolve()
    plugin_root = Path(sys.argv[2]).resolve()
    marketplace_root = Path(sys.argv[3]).resolve()
    plugin_name = load_json(source_manifest_path)["name"]

    versions = {
        "source_manifest": load_json(source_manifest_path)["version"],
        "built_manifest": load_json(plugin_root / ".codex-plugin" / "plugin.json")["version"],
        "marketplace_metadata": load_json(
            marketplace_root / ".agents" / "plugins" / "marketplace.json"
        )["plugins"][0]["version"],
        "marketplace_manifest": load_json(
            marketplace_root / "plugins" / plugin_name / ".codex-plugin" / "plugin.json"
        )["version"],
    }
    if len(set(versions.values())) != 1:
        print(json.dumps({"ok": False, "versions": versions}, indent=2), file=sys.stderr)
        return 1
    print(json.dumps({"ok": True, "version": next(iter(versions.values())), "sources": versions}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
