from pathlib import Path

from trace_aviary.adapters.samples import write_synthetic
from trace_aviary.adapters.sqlite import load_latest, save_result
from trace_aviary.domain.parsing import parse_files
from trace_aviary.services.catalog import build_catalog, write_catalog


def test_catalog_export_and_sqlite_roundtrip(tmp_path: Path) -> None:
    sample = tmp_path / "sample.jsonl"
    write_synthetic(sample, count=50)
    result = build_catalog(parse_files([sample]), n_clusters=5)
    output = tmp_path / "catalog.json"
    write_catalog(result, output)
    assert "reproduction_hypothesis" in output.read_text(encoding="utf-8")
    db_path = tmp_path / "catalogs.sqlite"
    save_result(db_path, result)
    latest = load_latest(db_path)
    assert latest is not None
    assert latest["total_events"] == 50
