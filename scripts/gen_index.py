#!/usr/bin/env python3
from pathlib import Path
import json
import datetime
import re

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT = REPO_ROOT / "index.json"
ROOTS = ["core", "extra", "multilib"]

# kata kunci umum → alias
KEYWORD_ALIASES = {
    "browser": ["browser", "web", "firefox", "chrome"],
    "linux": ["kernel", "linux"],
    "studio": ["studio", "ide"],
    "note": ["note", "markdown", "knowledge"],
}

def parse_template(path: Path):
    meta = {}
    for line in path.read_text(errors="ignore").splitlines():
        if "=" not in line or line.strip().startswith("#"):
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip().strip('"')
        if k in ("pkgname", "version", "short_desc"):
            meta[k] = v
        elif k == "revision":
            try:
                meta[k] = int(v)
            except ValueError:
                meta[k] = 1
    return meta


def base_alias(pkgname: str):
    """
    linux6.13-zen → linux
    xorg-minimal → xorg
    """
    name = re.sub(r"\d+(\.\d+)*", "", pkgname)
    return name.split("-")[0]


index = {
    "generated_at": datetime.datetime.now(
        datetime.timezone.utc
    ).isoformat(),
    "packages": {},
    "aliases": {},
}

def add_alias(alias, pkg):
    index["aliases"].setdefault(alias, set()).add(pkg)


# --- scan repo ---
for root in ROOTS:
    rootdir = REPO_ROOT / root
    if not rootdir.exists():
        continue

    for tpl in rootdir.rglob("template"):
        meta = parse_template(tpl)
        if "pkgname" not in meta:
            continue

        pkg = meta["pkgname"]

        index["packages"][pkg] = {
            "category": root,
            "path": str(tpl.parent.relative_to(REPO_ROOT)),
            "version": meta.get("version", ""),
            "revision": meta.get("revision", 1),
            "short_desc": meta.get("short_desc", ""),
        }

        # 1️⃣ base alias (linux, xorg, obsidian)
        add_alias(base_alias(pkg), pkg)

        # 2️⃣ exact name alias
        add_alias(pkg, pkg)

        # 3️⃣ keyword alias dari description
        desc = meta.get("short_desc", "").lower()
        for alias, keys in KEYWORD_ALIASES.items():
            for k in keys:
                if k in desc:
                    add_alias(alias, pkg)

# convert set → sorted list
index["aliases"] = {
    k: sorted(v) for k, v in index["aliases"].items()
}

# write output
with open(OUTPUT, "w") as f:
    json.dump(index, f, indent=2)

print(f"[OK] index.json generated ({len(index['packages'])} packages)")

