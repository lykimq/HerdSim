"""API router for multi-seed scientific benchmarks."""

from __future__ import annotations

import json
from typing import Optional

import pandas as pd
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import PlainTextResponse, Response, StreamingResponse
from pydantic import BaseModel, Field

from api.benchmark_defs import benchmark_definitions_payload
from api.benchmark_runner import (
    iter_one_trial,
    run_benchmark,
    summarize_rows,
    summary_to_csv,
    summary_to_markdown,
)

router = APIRouter()

# In-memory last benchmark for export convenience.
_LAST_BENCHMARK: dict | None = None


class BenchmarkRequest(BaseModel):
    algorithm_ids: list[str] = Field(default_factory=lambda: ["strombom", "kubo"])
    scenario_id: str = "drive_to_goal"
    seeds: list[int] = Field(default_factory=lambda: [1, 2, 3, 4, 5])
    preset: str = Field(default="paper", pattern="^(paper|scenario|custom)$")
    num_sheep: Optional[int] = Field(default=None, ge=1, le=200)
    num_shepherds: Optional[int] = Field(default=None, ge=1, le=10)


def _validate_request(req: BenchmarkRequest) -> None:
    if not req.algorithm_ids:
        raise HTTPException(status_code=400, detail="algorithm_ids required")
    if not req.seeds:
        raise HTTPException(status_code=400, detail="seeds required")


@router.post("/run")
def benchmark_run(
    req: BenchmarkRequest,
    stream: bool = Query(
        default=False,
        description="If true, stream NDJSON progress events then a final done payload.",
    ),
):
    global _LAST_BENCHMARK
    _validate_request(req)

    if not stream:
        try:
            payload = run_benchmark(
                algorithm_ids=req.algorithm_ids,
                scenario_id=req.scenario_id,
                seeds=req.seeds,
                preset=req.preset,
                num_sheep=req.num_sheep,
                num_shepherds=req.num_shepherds,
            )
        except KeyError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        _LAST_BENCHMARK = payload
        return payload

    def event_stream():
        global _LAST_BENCHMARK
        try:
            rows = []
            total = len(req.algorithm_ids) * len(req.seeds)
            index = 0
            for algorithm_id in req.algorithm_ids:
                for seed in req.seeds:
                    index += 1
                    for event in iter_one_trial(
                        algorithm_id=algorithm_id,
                        scenario_id=req.scenario_id,
                        seed=seed,
                        preset=req.preset,
                        num_sheep=req.num_sheep,
                        num_shepherds=req.num_shepherds,
                        index=index,
                        total=total,
                    ):
                        if event["type"] == "trial":
                            rows.append(event["row"])
                        yield json.dumps(event) + "\n"
            payload = {
                "rows": rows,
                "summary": summarize_rows(pd.DataFrame(rows)),
            }
            _LAST_BENCHMARK = payload
            yield json.dumps({"type": "done", **payload}) + "\n"
        except KeyError as exc:
            yield json.dumps({"type": "error", "message": str(exc)}) + "\n"
        except Exception as exc:  # noqa: BLE001 - surface failures to the UI stream
            yield json.dumps({"type": "error", "message": str(exc)}) + "\n"

    return StreamingResponse(event_stream(), media_type="application/x-ndjson")


@router.get("/definitions")
def benchmark_definitions():
    """Definitions for summary-table metrics and CSV trial columns."""
    return benchmark_definitions_payload()


@router.get("/last")
def benchmark_last():
    if _LAST_BENCHMARK is None:
        raise HTTPException(status_code=404, detail="No benchmark has been run yet")
    return _LAST_BENCHMARK


@router.get("/export")
def benchmark_export(format: str = Query(default="json", pattern="^(json|csv|md)$")):
    if _LAST_BENCHMARK is None:
        raise HTTPException(status_code=404, detail="No benchmark has been run yet")
    if format == "json":
        return _LAST_BENCHMARK
    if format == "csv":
        return Response(
            content=summary_to_csv(_LAST_BENCHMARK),
            media_type="text/csv",
            headers={
                "Content-Disposition": 'attachment; filename="herdsim_benchmark.csv"'
            },
        )
    return PlainTextResponse(
        summary_to_markdown(_LAST_BENCHMARK), media_type="text/markdown"
    )
