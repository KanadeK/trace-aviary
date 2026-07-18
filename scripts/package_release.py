from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.1.0"
SLUG = "trace-aviary"


def main() -> None:
    subprocess.run([sys.executable, "-m", "build"], cwd=ROOT, check=True)
    release_dir = ROOT / "dist-release"
    release_dir.mkdir(exist_ok=True)
    for artifact in (ROOT / "dist").glob("*"):
        target = release_dir / artifact.name
        shutil.copy2(artifact, target)
    sample_target = release_dir / f"{SLUG}-{VERSION}-synthetic-logs.jsonl"
    shutil.copy2(ROOT / "examples" / "synthetic_logs.jsonl", sample_target)
    compose_target = release_dir / f"{SLUG}-{VERSION}-docker-compose.yml"
    shutil.copy2(ROOT / "docker-compose.yml", compose_target)
    checksums = []
    for artifact in sorted(release_dir.iterdir()):
        if artifact.name == "SHA256SUMS.txt" or artifact.is_dir():
            continue
        digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
        checksums.append(f"{digest}  {artifact.name}")
    (release_dir / "SHA256SUMS.txt").write_text("\n".join(checksums) + "\n", encoding="utf-8")
    print(f"Packaged {len(checksums)} release artifacts in {release_dir}")


if __name__ == "__main__":
    main()
