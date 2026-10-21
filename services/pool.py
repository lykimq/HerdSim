"""Worker pool shared by calibration and campaign batches.

Workers start from a fork server, not by forking the parent: forking a
process that already runs threads can deadlock, and fresh workers read the
single-thread BLAS settings from the environment at import.
"""

from __future__ import annotations

import multiprocessing
from concurrent.futures import ProcessPoolExecutor


def worker_pool(workers: int) -> ProcessPoolExecutor:
    return ProcessPoolExecutor(
        max_workers=max(1, workers), mp_context=multiprocessing.get_context("forkserver")
    )
