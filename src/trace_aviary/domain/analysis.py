from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from datetime import datetime
from math import sqrt
from typing import Any, cast

import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

from trace_aviary.domain.models import AnalysisResult, IncidentCluster, LogEvent
from trace_aviary.domain.normalization import normalize_text


def choose_cluster_count(event_count: int, requested: int | None = None) -> int:
    if event_count <= 1:
        return max(event_count, 1)
    if requested is not None:
        return min(max(1, requested), event_count)
    return min(max(2, round(sqrt(event_count / 4))), 8, event_count)


def analyze_events(events: list[LogEvent], n_clusters: int | None = None) -> AnalysisResult:
    if not events:
        return AnalysisResult(clusters=(), total_events=0, noise_events=0)

    documents = [normalize_text(event.text) or "<empty>" for event in events]
    cluster_count = choose_cluster_count(len(events), n_clusters)
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1, max_df=1.0)
    matrix = vectorizer.fit_transform(documents)

    if cluster_count == 1:
        labels = np.zeros(len(events), dtype=int)
    else:
        model = KMeans(n_clusters=cluster_count, n_init=20, random_state=42)
        labels = model.fit_predict(matrix)

    feature_names = list(vectorizer.get_feature_names_out())
    clusters: list[IncidentCluster] = []
    for label in sorted(set(int(label) for label in labels)):
        indexes = tuple(index for index, value in enumerate(labels) if int(value) == label)
        centroid = matrix[list(indexes)].mean(axis=0)
        centroid_array = cast(np.ndarray[Any, Any], np.asarray(centroid).ravel())
        top_positions = [
            int(position) for position in np.argsort(centroid_array).tolist()[::-1][:10]
        ]
        common_tokens = tuple(
            feature_names[position]
            for position in top_positions
            if feature_names[position] and not feature_names[position].startswith("<")
        )[:8]
        representative_index = _representative_index(matrix, indexes, centroid_array)
        first_seen, last_seen, buckets = _time_summary(events[index] for index in indexes)
        species = _species_name(label, common_tokens)
        clusters.append(
            IncidentCluster(
                cluster_id=label,
                species=species,
                sample_count=len(indexes),
                representative=events[representative_index],
                common_tokens=common_tokens,
                first_seen=first_seen,
                last_seen=last_seen,
                time_buckets=buckets,
                reproduction_hypothesis=_hypothesis(common_tokens, events[representative_index]),
                sample_indexes=indexes,
            )
        )

    clusters.sort(key=lambda cluster: (-cluster.sample_count, cluster.cluster_id))
    return AnalysisResult(clusters=tuple(clusters), total_events=len(events), noise_events=0)


def _representative_index(
    matrix: Any, indexes: tuple[int, ...], centroid: np.ndarray[Any, Any]
) -> int:
    best_index = indexes[0]
    best_distance = float("inf")
    for index in indexes:
        row = np.asarray(matrix[index].todense()).ravel()
        distance = float(np.linalg.norm(row - centroid))
        if distance < best_distance:
            best_distance = distance
            best_index = index
    return best_index


def _time_summary(
    events: Iterable[LogEvent],
) -> tuple[datetime | None, datetime | None, dict[str, int]]:
    timestamps = [event.timestamp for event in events if event.timestamp is not None]
    if not timestamps:
        return None, None, {}
    buckets: dict[str, int] = defaultdict(int)
    for timestamp in timestamps:
        buckets[timestamp.strftime("%Y-%m-%dT%H:00:00")] += 1
    return min(timestamps), max(timestamps), dict(sorted(buckets.items()))


def _species_name(label: int, common_tokens: tuple[str, ...]) -> str:
    if not common_tokens:
        return f"incident-species-{label}"
    head = "-".join(common_tokens[:2]).replace("/", "-")[:42].strip("-")
    return f"{head or 'incident'}-{label}"


def _hypothesis(common_tokens: tuple[str, ...], representative: LogEvent) -> str:
    token_text = ", ".join(common_tokens[:5]) if common_tokens else "shared stack/message shape"
    source = f" in {representative.source}" if representative.source else ""
    return (
        f"Reproduce by replaying an input that reaches the representative failure path{source}; "
        f"vary dynamic IDs/timestamps while preserving these shared symptoms: {token_text}."
    )


def adjusted_rand_for_expected(events: list[LogEvent], result: AnalysisResult) -> float | None:
    from sklearn.metrics import adjusted_rand_score

    expected = [event.expected_root for event in events]
    if any(value is None for value in expected):
        return None
    predicted = [0] * len(events)
    for cluster in result.clusters:
        for index in cluster.sample_indexes:
            predicted[index] = cluster.cluster_id
    return float(adjusted_rand_score(expected, predicted))
