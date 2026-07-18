from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from trace_aviary.adapters.files import read_events
from trace_aviary.adapters.samples import write_synthetic
from trace_aviary.adapters.sqlite import save_result
from trace_aviary.domain.analysis import adjusted_rand_for_expected
from trace_aviary.domain.models import AnalysisResult
from trace_aviary.services.catalog import build_catalog, write_catalog

app = typer.Typer(help="Cluster logs and stack traces into incident species.")
console = Console()


@app.command()
def sample(
    output: Annotated[
        Path, typer.Option("--output", "-o")
    ] = Path("examples/synthetic_logs.jsonl"),
    count: Annotated[int, typer.Option(min=5)] = 500,
    seed: Annotated[int, typer.Option()] = 42,
) -> None:
    """Generate deterministic synthetic logs with five known root causes."""
    write_synthetic(output, count=count, seed=seed)
    console.print(f"Wrote {count} synthetic events to {output}")


@app.command()
def analyze(
    inputs: Annotated[list[Path], typer.Argument(exists=True, readable=True)],
    output: Annotated[
        Path, typer.Option("--output", "-o")
    ] = Path("dist-release/incident_catalog.json"),
    clusters: Annotated[int | None, typer.Option("--clusters", "-k")] = None,
    sqlite: Annotated[Path | None, typer.Option("--sqlite")] = None,
) -> None:
    """Parse logs, cluster incident species, and export a catalog."""
    events = read_events(inputs)
    result = build_catalog(events, n_clusters=clusters)
    write_catalog(result, output)
    if sqlite is not None:
        save_result(sqlite, result)
    _print_summary(result, adjusted_rand_for_expected(events, result))
    console.print(f"Catalog written to {output}")


@app.command()
def demo(
    output_dir: Annotated[Path, typer.Option("--output-dir")] = Path("dist-release/demo"),
) -> None:
    """Run the full deterministic demo using repository sample data."""
    sample_path = Path("examples/synthetic_logs.jsonl")
    if not sample_path.exists():
        write_synthetic(sample_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    events = read_events([sample_path])
    result = build_catalog(events, n_clusters=5)
    write_catalog(result, output_dir / "incident_catalog.json")
    write_catalog(result, output_dir / "incident_catalog.md")
    _print_summary(result, adjusted_rand_for_expected(events, result))


def _print_summary(result: AnalysisResult, ari: float | None) -> None:
    table = Table(title="Incident Species")
    table.add_column("Species")
    table.add_column("Samples", justify="right")
    table.add_column("Common tokens")
    for cluster in result.clusters:
        table.add_row(
            cluster.species,
            str(cluster.sample_count),
            ", ".join(cluster.common_tokens[:5]),
        )
    console.print(table)
    if ari is not None:
        console.print(f"Adjusted Rand Index against sample labels: {ari:.3f}")


if __name__ == "__main__":
    app()
