from __future__ import annotations

import html
import shutil
from pathlib import Path

from trace_aviary.adapters.files import read_events
from trace_aviary.services.catalog import build_catalog

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    site = ROOT / "site"
    site.mkdir(exist_ok=True)
    events = read_events([ROOT / "examples" / "synthetic_logs.jsonl"])
    result = build_catalog(events, n_clusters=5)
    cards = []
    for cluster in result.clusters:
        cards.append(
            f"<article><h2>{html.escape(cluster.species)}</h2>"
            f"<p>{cluster.sample_count} samples</p>"
            f"<p>{html.escape(cluster.reproduction_hypothesis)}</p>"
            f"<pre>{html.escape(cluster.representative.text)}</pre></article>"
        )
    page = "\n".join(
        [
            "<!doctype html><html><head><meta charset='utf-8'>",
            "<meta name='viewport' content='width=device-width, initial-scale=1'>",
            "<title>Trace Aviary Demo</title>",
            "<link rel='stylesheet' href='style.css'></head><body>",
            "<header><p class='eyebrow'>Trace Aviary v0.1.0</p>",
            "<h1>Deterministic incident species demo</h1></header>",
            "<main><section class='summary'>",
            f"<strong>{result.total_events}</strong><span>events</span>",
            f"<strong>{len(result.clusters)}</strong><span>clusters</span>",
            f"</section><section class='clusters'>{''.join(cards)}</section></main>",
            "</body></html>",
        ]
    )
    (site / "index.html").write_text(page, encoding="utf-8")
    shutil.copy2(ROOT / "src" / "trace_aviary" / "static" / "style.css", site / "style.css")


if __name__ == "__main__":
    main()
