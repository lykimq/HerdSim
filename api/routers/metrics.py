"""API router for metric discovery and session export."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse, PlainTextResponse, Response

from api.session_manager import session_manager
from metrics.registry import metric_registry

router = APIRouter()


@router.get("")
@router.get("/")
def list_metrics():
    """List all registered evaluation metrics."""
    return metric_registry.list_all()


@router.get("/export/{session_id}")
def export_session_metrics(
    session_id: str,
    format: str = Query(default="json", pattern="^(json|csv|md)$"),
):
    """Export recorded metrics for a simulation session."""
    try:
        session = session_manager.get_session(session_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    summary = session.runner.recorder.get_summary()
    df = session.runner.recorder.to_dataframe()

    if format == "json":
        return JSONResponse(
            {
                "session_id": session_id,
                "summary": summary,
                "history": df.to_dict(orient="records"),
            }
        )

    if format == "csv":
        return Response(
            content=df.to_csv(index=False),
            media_type="text/csv",
            headers={
                "Content-Disposition": f'attachment; filename="herdsim_{session_id}.csv"'
            },
        )

    lines = [
        f"# HerdSim Export ({session_id})",
        "",
        f"- ticks: {summary.get('ticks', 0)}",
        f"- final_tick: {summary.get('final_tick', 0)}",
        "",
        "## Final Metrics",
    ]
    for key, value in summary.get("final_metrics", {}).items():
        lines.append(f"- {key}: {value}")
    return PlainTextResponse("\n".join(lines) + "\n", media_type="text/markdown")
