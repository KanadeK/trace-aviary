from __future__ import annotations

from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from trace_aviary.adapters.files import read_text_events
from trace_aviary.adapters.samples import synthetic_jsonl
from trace_aviary.services.catalog import build_catalog, catalog_to_dict

PACKAGE_DIR = Path(__file__).parent

app = FastAPI(title="Trace Aviary", version="0.1.0")
app.mount("/static", StaticFiles(directory=PACKAGE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=PACKAGE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    events = read_text_events(synthetic_jsonl(count=80))
    result = build_catalog(events, n_clusters=5)
    return templates.TemplateResponse(
        request,
        "index.html",
        {"result": result, "catalog": catalog_to_dict(result), "sample_loaded": True},
    )


@app.post("/analyze", response_class=HTMLResponse)
async def analyze_upload(
    request: Request,
    file: Annotated[UploadFile | None, File()] = None,
    pasted: Annotated[str, Form()] = "",
    clusters: Annotated[int | None, Form()] = None,
) -> HTMLResponse:
    body = pasted
    if file is not None and file.filename:
        body = (await file.read()).decode("utf-8")
    events = read_text_events(body)
    result = build_catalog(events, n_clusters=clusters)
    return templates.TemplateResponse(
        request,
        "index.html",
        {"result": result, "catalog": catalog_to_dict(result), "sample_loaded": False},
    )


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}
