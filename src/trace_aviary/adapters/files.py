from __future__ import annotations

from pathlib import Path

from trace_aviary.domain.models import LogEvent
from trace_aviary.domain.parsing import parse_files, parse_records


def read_events(paths: list[Path]) -> list[LogEvent]:
    return parse_files(paths)


def read_text_events(text: str) -> list[LogEvent]:
    return parse_records(text)
