from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from trace_aviary.domain.models import AnalysisResult
from trace_aviary.services.catalog import catalog_to_dict


def save_result(db_path: Path, result: AnalysisResult) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS catalogs ("
            "id INTEGER PRIMARY KEY, generated_at TEXT, payload TEXT NOT NULL)"
        )
        payload = catalog_to_dict(result)
        connection.execute(
            "INSERT INTO catalogs (generated_at, payload) VALUES (?, ?)",
            (payload["generated_at"], json.dumps(payload)),
        )


def load_latest(db_path: Path) -> dict[str, object] | None:
    with sqlite3.connect(db_path) as connection:
        row = connection.execute(
            "SELECT payload FROM catalogs ORDER BY id DESC LIMIT 1"
        ).fetchone()
    if row is None:
        return None
    payload = json.loads(str(row[0]))
    if not isinstance(payload, dict):
        raise ValueError("catalog payload is not a JSON object")
    return payload
