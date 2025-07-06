#!/usr/bin/env python3
"""Check that all apt package names in config/packages.yaml exist."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import List

from ruamel.yaml import YAML

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "packages.yaml"
TODO_PATH = Path(__file__).resolve().parent.parent / "TODO.md"

yaml = YAML(typ="safe")


def load_packages() -> List[str]:
    if not CONFIG_PATH.exists():
        return []
    with open(CONFIG_PATH, "r") as f:
        data = yaml.load(f) or {}
    packages = []
    for item in data.get("packages", []):
        name = None
        override = None
        if isinstance(item, str):
            name = item
        elif isinstance(item, dict):
            if "name" in item:
                name = item.get("name")
                override = item.get("apt-override")
            elif len(item) == 1:
                name, meta = next(iter(item.items()))
                if isinstance(meta, dict):
                    override = meta.get("apt-override")
        if name:
            packages.append(override if override else name)
    return packages


def apt_exists(pkg: str) -> bool:
    result = subprocess.run([
        "apt-cache",
        "show",
        pkg,
    ], capture_output=True, text=True)
    return "Package:" in result.stdout


def append_todo(pkg: str) -> None:
    line = f"- [ ] Add apt installation method for {pkg}\n"
    if TODO_PATH.exists():
        with open(TODO_PATH, "r+") as f:
            contents = f.read()
            if line.strip() not in contents:
                f.write(line)
    else:
        with open(TODO_PATH, "w") as f:
            f.write("# TODO\n" + line)


def main() -> int:
    missing: List[str] = []
    for pkg in load_packages():
        if not apt_exists(pkg):
            print(f"Missing apt package: {pkg}")
            append_todo(pkg)
            missing.append(pkg)
    if missing:
        print(f"\n{len(missing)} package(s) missing from apt")
        return 1
    print("All packages present in apt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
