import subprocess
import sys
from pathlib import Path


def test_cli_demo_generates_catalog(tmp_path: Path) -> None:
    result = subprocess.run(
        [sys.executable, "-m", "trace_aviary.cli", "demo", "--output-dir", str(tmp_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "Adjusted Rand Index" in result.stdout
    assert (tmp_path / "incident_catalog.json").exists()
    catalog = (tmp_path / "incident_catalog.json").read_text(encoding="utf-8")
    assert "reproduction_hypothesis" in catalog
