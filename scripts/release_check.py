from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.1.0"


def run(command: list[str]) -> str:
    if command and command[0] == "git":
        command = ["git", "-c", f"safe.directory={ROOT.as_posix()}", *command[1:]]
    return subprocess.check_output(command, cwd=ROOT, text=True, stderr=subprocess.STDOUT)


def main() -> None:
    status = run(["git", "status", "--short"])
    if status.strip():
        raise SystemExit(f"working tree is not clean:\n{status}")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    if f"## v{VERSION}" not in changelog:
        raise SystemExit("CHANGELOG is missing v0.1.0")
    if not (ROOT / "dist-release" / "SHA256SUMS.txt").exists():
        raise SystemExit("dist-release/SHA256SUMS.txt is missing")
    scanned_files = [
        path
        for path in ROOT.rglob("*")
        if path.is_file() and path.suffix in {".py", ".md", ".toml", ".yml", ".yaml"}
    ]
    scan = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore") for path in scanned_files
    )
    secret_pattern = (
        r"(?i)(api[_-]?key|token|secret|password)\s*=\s*['\"]?[A-Za-z0-9._~+/=-]{12,}"
    )
    if re.search(secret_pattern, scan):
        raise SystemExit("potential secret pattern found")
    blocked_markers = [
        "TO" + "DO",
        "FIX" + "ME",
        "Not" + "Implemented",
        "lorem" + " ipsum",
        "coming" + " soon",
    ]
    blocked_markers.append("place" + "holder")
    if re.search("|".join(re.escape(marker) for marker in blocked_markers), scan, re.I):
        raise SystemExit("empty-shell marker found")
    authors = run(["git", "log", "--format=%an <%ae>"]).splitlines()
    unexpected = [author for author in set(authors) if not author.startswith("KanadeK <")]
    if unexpected:
        raise SystemExit(f"unexpected commit authors: {unexpected}")
    subprocess.run([sys.executable, "scripts/verify.py"], cwd=ROOT, check=True)
    print("release check passed")


if __name__ == "__main__":
    main()
