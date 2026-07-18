"""Trace Aviary public package API."""

__all__ = ["AnalysisResult", "IncidentCluster", "LogEvent", "analyze_events"]


def __getattr__(name: str) -> object:
    if name == "analyze_events":
        from trace_aviary.domain.analysis import analyze_events

        return analyze_events
    if name in {"AnalysisResult", "IncidentCluster", "LogEvent"}:
        from trace_aviary.domain import models

        return getattr(models, name)
    raise AttributeError(name)
