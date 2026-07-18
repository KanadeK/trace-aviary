from __future__ import annotations

import re

SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|token|secret|password)=([A-Za-z0-9._~+/=-]{8,})"),
    re.compile(r"(?i)(authorization:\s*bearer\s+)([A-Za-z0-9._~+/=-]{8,})"),
]

NORMALIZATION_RULES: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"\b\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?\b"), "<time>"),
    (re.compile(r"[A-Za-z]:\\(?:[^\\\s]+\\)*([^\\\s:]+\.py)"), r"<path>/\1"),
    (re.compile(r"/(?:[\w.-]+/)+([\w.-]+\.(?:py|js|ts|java|go|rb|php))"), r"<path>/\1"),
    (
        re.compile(
            r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
            re.I,
        ),
        "<uuid>",
    ),
    (re.compile(r"\b(?:req|request|trace|span|session)[_-]?[a-z0-9]{6,}\b", re.I), "<id>"),
    (re.compile(r"\b0x[0-9a-f]+\b", re.I), "<hex>"),
    (re.compile(r"(?<![A-Za-z])\d+(?:\.\d+)?(?![A-Za-z])"), "<num>"),
    (re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b"), "<email>"),
)


def mask_secrets(text: str) -> str:
    masked = text
    for pattern in SECRET_PATTERNS:
        masked = pattern.sub(lambda match: f"{match.group(1)}=<redacted>", masked)
    return masked


def normalize_text(text: str) -> str:
    normalized = mask_secrets(text)
    for pattern, replacement in NORMALIZATION_RULES:
        normalized = pattern.sub(replacement, normalized)
    normalized = re.sub(r"['\"]", "", normalized)
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.strip().lower()


def tokenize(text: str) -> tuple[str, ...]:
    normalized = normalize_text(text)
    return tuple(
        token
        for token in re.findall(r"[a-z][a-z0-9_./<>-]{2,}", normalized)
        if token not in {"the", "and", "for", "with", "from", "this", "that"}
    )
