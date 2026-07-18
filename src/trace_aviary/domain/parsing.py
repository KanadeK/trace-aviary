from __future__ import annotations

import json
from collections.abc import Iterable
from datetime import datetime
from pathlib import Path
from typing import Any

from trace_aviary.domain.models import LogEvent
from trace_aviary.domain.normalization import mask_secrets


def parse_timestamp(value: Any) -> datetime | None:
    if value in (None, ""):
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, int | float):
        return datetime.fromtimestamp(float(value))
    if isinstance(value, str):
        candidate = value.replace("Z", "+00:00")
        try:
            return datetime.fromisoformat(candidate)
        except ValueError:
            return None
    return None


def _event_from_mapping(item: dict[str, Any], raw: str) -> LogEvent:
    exception = item.get("exception")
    stack = item.get("stack") or item.get("stacktrace") or item.get("traceback")
    if isinstance(exception, dict):
        values = exception.get("values")
        if isinstance(values, list) and values:
            first = values[0]
            if isinstance(first, dict):
                stack = stack or _sentry_frames_to_stack(first)
                message = first.get("value") or item.get("message") or item.get("title") or raw
            else:
                message = item.get("message") or raw
        else:
            message = item.get("message") or raw
    else:
        message = (
            item.get("message")
            or item.get("msg")
            or item.get("event")
            or item.get("title")
            or raw
        )

    return LogEvent(
        raw=mask_secrets(raw),
        message=str(message),
        timestamp=parse_timestamp(
            item.get("timestamp") or item.get("time") or item.get("datetime")
        ),
        level=str(item["level"]) if item.get("level") else None,
        source=str(item["logger"]) if item.get("logger") else item.get("service"),
        stack=str(stack) if stack else None,
        metadata={
            k: v
            for k, v in item.items()
            if k not in {"message", "msg", "stack", "stacktrace"}
        },
        expected_root=str(item["root_cause"]) if item.get("root_cause") else None,
    )


def _sentry_frames_to_stack(exception: dict[str, Any]) -> str | None:
    stacktrace = exception.get("stacktrace")
    if not isinstance(stacktrace, dict):
        return None
    frames = stacktrace.get("frames")
    if not isinstance(frames, list):
        return None
    rendered: list[str] = []
    for frame in frames:
        if not isinstance(frame, dict):
            continue
        filename = frame.get("filename") or "<unknown>"
        function = frame.get("function") or "<module>"
        line = frame.get("lineno") or "?"
        rendered.append(f'  File "{filename}", line {line}, in {function}')
    return "\n".join(rendered)


def parse_records(text: str) -> list[LogEvent]:
    stripped = text.strip()
    if not stripped:
        return []
    if stripped.startswith("{") or stripped.startswith("["):
        try:
            parsed = json.loads(stripped)
        except json.JSONDecodeError:
            parsed = None
        if isinstance(parsed, list):
            return [
                _event_from_mapping(item, json.dumps(item, sort_keys=True))
                for item in parsed
                if isinstance(item, dict)
            ]
        if isinstance(parsed, dict):
            if isinstance(parsed.get("events"), list):
                return [
                    _event_from_mapping(item, json.dumps(item, sort_keys=True))
                    for item in parsed["events"]
                    if isinstance(item, dict)
                ]
            return [_event_from_mapping(parsed, stripped)]

    events: list[LogEvent] = []
    for line in stripped.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            events.append(LogEvent(raw=mask_secrets(line), message=line))
        else:
            if isinstance(item, dict):
                events.append(_event_from_mapping(item, line))
            else:
                events.append(LogEvent(raw=mask_secrets(line), message=str(item)))
    return events


def parse_files(paths: Iterable[Path]) -> list[LogEvent]:
    events: list[LogEvent] = []
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(path)
        events.extend(parse_records(path.read_text(encoding="utf-8")))
    return events
