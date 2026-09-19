"""API router for multi-seed scientific benchmarks."""

from __future__ import annotations

import json
from typing import Any, Optional

import pandas as pd
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import PlainTextResponse, Response, StreamingResponse
from pydantic import BaseModel, Field

from services.experiments.defs import benchmark_definitions_payload
from services.experiments.report import build_report_package, report_to_csv, report_to_markdown
from services.experiments.runner import (
    iter_one_trial,
    run_benchmark,
    summarize_rows,
)
from services.experiments.sweep import expand_factor_grid, parse_factor_specs

router = APIRouter()

# In-memory last benchmark for export convenience.
_LAST_BENCHMARK: dict | None = None
_LAST_REQUEST: dict | None = None


def _request_meta(req: BenchmarkRequest, sweep_payload: list[dict[str, Any]] | None) -> dict:
    return {
        "instruments": list(req.instruments),
        "scenario_id": req.scenario_id,
        "preset": req.preset,
        "seeds": list(req.seeds),
        "num_sheep": req.num_sheep,
        "num_shepherds": req.num_shepherds,
        "algorithm_params": req.algorithm_params,
        "sweep": sweep_payload,
    }


class SweepParam(BaseModel):
    key: str
    values: list[float | int | str] = Field(min_length=1)


class BenchmarkRequest(BaseModel):
    instruments: list[str] = Field(default_factory=lambda: ["strombom", "kubo"])
    scenario_id: str = "drive_to_goal"
    seeds: list[int] = Field(default_factory=lambda: [1, 2, 3, 4, 5])
    preset: str = Field(default="paper", pattern="^(paper|scenario|custom)$")
    num_sheep: Optional[int] = Field(default=None, ge=1, le=200)
    num_shepherds: Optional[int] = Field(default=None, ge=1, le=10)
    algorithm_params: Optional[dict[str, Any]] = None
    sweep: Optional[list[SweepParam]] = None


def _validate_request(req: BenchmarkRequest) -> list[dict[str, Any]]:
    if not req.seeds:
        raise HTTPException(status_code=400, detail="seeds required")
    try:
        specs = parse_factor_specs(
            [item.model_dump() for item in req.sweep] if req.sweep else None
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if specs:
        keys = {str(item["key"]) for item in specs}
        if req.instruments:
            if len(req.instruments) != 1:
                raise HTTPException(
                    status_code=400,
                    detail="Param sweep with an instrument requires exactly one instrument",
                )
        elif "sheep_model" not in keys or "dog_controller" not in keys:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Factor grids without an instrument require sheep_model "
                    "and dog_controller factors"
                ),
            )
    elif not req.instruments:
        raise HTTPException(status_code=400, detail="instruments required")
    return specs


@router.post("/run")
def benchmark_run(
    req: BenchmarkRequest,
    stream: bool = Query(
        default=False,
        description="If true, stream NDJSON progress events then a final done payload.",
    ),
):
    global _LAST_BENCHMARK
    specs = _validate_request(req)
    sweep_payload = [s for s in specs] if specs else None

    if not stream:
        try:
                payload = run_benchmark(
                instruments=req.instruments,
                scenario_id=req.scenario_id,
                seeds=req.seeds,
                preset=req.preset,
                num_sheep=req.num_sheep,
                num_shepherds=req.num_shepherds,
                algorithm_params=req.algorithm_params,
                sweep=sweep_payload,
            )
        except (KeyError, ValueError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        meta = _request_meta(req, sweep_payload)
        payload["experiment"] = meta
        _LAST_BENCHMARK = payload
        _LAST_REQUEST = meta
        return payload

    def event_stream():
        global _LAST_BENCHMARK, _LAST_REQUEST
        try:
            rows = []
            param_sets = expand_factor_grid(specs)
            instrument_loop = list(req.instruments) if req.instruments else [None]
            total = len(instrument_loop) * len(req.seeds) * len(param_sets)
            index = 0
            for instrument in instrument_loop:
                for params in param_sets:
                    for seed in req.seeds:
                        index += 1
                        for event in iter_one_trial(
                            instrument=instrument,
                            scenario_id=req.scenario_id,
                            seed=seed,
                            preset=req.preset,
                            num_sheep=req.num_sheep,
                            num_shepherds=req.num_shepherds,
                            algorithm_params=req.algorithm_params,
                            sweep_params=params or None,
                            index=index,
                            total=total,
                        ):
                            if event["type"] == "trial":
                                rows.append(event["row"])
                            yield json.dumps(event) + "\n"
            meta = _request_meta(req, sweep_payload)
            payload = {
                "rows": rows,
                "summary": summarize_rows(pd.DataFrame(rows)),
                "experiment": meta,
            }
            _LAST_BENCHMARK = payload
            _LAST_REQUEST = meta
            yield json.dumps({"type": "done", **payload}) + "\n"
        except (KeyError, ValueError) as exc:
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
        return build_report_package(_LAST_BENCHMARK, request=_LAST_REQUEST)
    if format == "csv":
        return Response(
            content=report_to_csv(_LAST_BENCHMARK, request=_LAST_REQUEST),
            media_type="text/csv",
            headers={
                "Content-Disposition": 'attachment; filename="herdsim_benchmark.csv"'
            },
        )
    return PlainTextResponse(
        report_to_markdown(_LAST_BENCHMARK, request=_LAST_REQUEST),
        media_type="text/markdown",
    )
