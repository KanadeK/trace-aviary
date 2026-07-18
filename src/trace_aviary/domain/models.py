from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class LogEvent:
    raw: str
    message: str
    timestamp: datetime | None = None
    level: str | None = None
    source: str | None = None
    stack: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    expected_root: str | None = None

    @property
    def text(self) -> str:
        parts = [self.message]
        if self.stack:
            parts.append(self.stack)
        return "\n".join(part for part in parts if part).strip()


@dataclass(frozen=True)
class IncidentCluster:
    cluster_id: int
    species: str
    sample_count: int
    representative: LogEvent
    common_tokens: tuple[str, ...]
    first_seen: datetime | None
    last_seen: datetime | None
    time_buckets: dict[str, int]
    reproduction_hypothesis: str
    sample_indexes: tuple[int, ...]


@dataclass(frozen=True)
class AnalysisResult:
    clusters: tuple[IncidentCluster, ...]
    total_events: int
    noise_events: int
    generated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
