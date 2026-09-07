"""FastAPI application entry point for HerdSim."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import algorithms, benchmarks, metrics, netlogo, scenarios, simulations, websocket

app = FastAPI(
    title="HerdSim API",
    description="Herding agent-based model simulation platform",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(algorithms.router, prefix="/api/algorithms", tags=["algorithms"])
app.include_router(scenarios.router, prefix="/api/scenarios", tags=["scenarios"])
app.include_router(simulations.router, prefix="/api/simulations", tags=["simulations"])
app.include_router(metrics.router, prefix="/api/metrics", tags=["metrics"])
app.include_router(benchmarks.router, prefix="/api/benchmarks", tags=["benchmarks"])
app.include_router(netlogo.router, prefix="/api/netlogo", tags=["netlogo"])
app.include_router(websocket.router, tags=["websocket"])


@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}
