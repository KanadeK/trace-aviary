from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from trace_aviary.domain.analysis import analyze_events
from trace_aviary.domain.models import AnalysisResult, IncidentCluster, LogEvent


def build_catalog(events: list[LogEvent], n_clusters: int | None = None) -> AnalysisResult:
    return analyze_events(events, n_clusters=n_clusters)


def catalog_to_dict(result: AnalysisResult) -> dict[str, Any]:
    return {
        "total_events": result.total_events,
        "noise_events": result.noise_events,
        "generated_at": result.generated_at.isoformat(),
        "clusters": [_cluster_to_dict(cluster) for cluster in result.clusters],
    }


def write_catalog(result: AnalysisResult, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.suffix.lower() in {".md", ".markdown"}:
        output.write_text(catalog_to_markdown(result), encoding="utf-8")
    else:
        output.write_text(json.dumps(catalog_to_dict(result), indent=2), encoding="utf-8")


def catalog_to_markdown(result: AnalysisResult) -> str:
    lines = [
        "# Incident Catalog",
        "",
        f"- Total events: {result.total_events}",
        f"- Clusters: {len(result.clusters)}",
        f"- Generated at: {result.generated_at.isoformat()}",
        "",
    ]
    for cluster in result.clusters:
        lines.extend(
            [
                f"## {cluster.species}",
                "",
                f"- Samples: {cluster.sample_count}",
                f"- Common tokens: {', '.join(cluster.common_tokens) or 'n/a'}",
                f"- First seen: {cluster.first_seen.isoformat() if cluster.first_seen else 'n/a'}",
                f"- Last seen: {cluster.last_seen.isoformat() if cluster.last_seen else 'n/a'}",
                f"- Reproduction hypothesis: {cluster.reproduction_hypothesis}",
                "",
                "Representative sample:",
                "",
                "```text",
                cluster.representative.text[:2000],
                "```",
                "",
            ]
        )
    return "\n".join(lines)


def _cluster_to_dict(cluster: IncidentCluster) -> dict[str, Any]:
    data = asdict(cluster)
    representative = data["representative"]
    if representative.get("timestamp") is not None:
        representative["timestamp"] = representative["timestamp"].isoformat()
    if data["first_seen"] is not None:
        data["first_seen"] = data["first_seen"].isoformat()
    if data["last_seen"] is not None:
        data["last_seen"] = data["last_seen"].isoformat()
    return data
