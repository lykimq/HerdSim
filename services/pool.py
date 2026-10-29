"""Worker pool shared by calibration and campaign batches.

Workers start from a fork server, not by forking the parent: forking a process that
already runs threads can deadlock, and fresh workers read the single-thread BLAS settings
from the environment at import.
"""

from __future__ import annotations

import multiprocessing
import os
from concurrent.futures import ProcessPoolExecutor

THREAD_LIMIT_VARS = (
    "OPENBLAS_NUM_THREADS",
    "OMP_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
)

def _init_worker() -> None:
    for var in THREAD_LIMIT_VARS:
        os.environ[var] = "1"

# Ensure environment is set in the parent process before starting any forkserver or workers
for _var in THREAD_LIMIT_VARS:
    os.environ[_var] = "1"


def worker_pool(workers: int) -> ProcessPoolExecutor:
    for _var in THREAD_LIMIT_VARS:
        os.environ[_var] = "1"
    return ProcessPoolExecutor(
        max_workers=max(1, workers),
        mp_context=multiprocessing.get_context("forkserver"),
        initializer=_init_worker,
    )
