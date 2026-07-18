# Architecture

Trace Aviary separates deterministic incident analysis from I/O:

- `trace_aviary.domain`: pure parsing, normalization, models, and clustering logic.
- `trace_aviary.adapters`: files, SQLite persistence, and deterministic sample generation.
- `trace_aviary.services`: catalog construction and export orchestration.
- `trace_aviary.cli`: command-line entry points.
- `trace_aviary.api`: FastAPI web interface over the same service layer.

The core does not call external APIs and fixes random seeds for repeatable clustering. The bundled sample data contains synthetic records only.
