# Benchmark

Environment: local development workstation, Python 3.12, deterministic 500-event synthetic sample.

Command:

```bash
python -m trace_aviary.cli demo
```

Expected v0.1.0 behavior: parse 500 JSONL events, cluster five root causes, export JSON and Markdown catalogs, and report an Adjusted Rand Index near 1.0 in a few seconds on a typical laptop.
