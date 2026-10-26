"""Worker pool factory using forkserver.

Uses Python's forkserver context rather than standard fork to avoid deadlocks
with multi-threaded BLAS libraries (NumPy/OpenBLAS) and ensure workers start clean.
"""

from __future__ import annotations

import multiprocessing
from concurrent.futures import ProcessPoolExecutor


def worker_pool(workers: int) -> ProcessPoolExecutor:
    """Create a ProcessPoolExecutor using the forkserver start method."""
    return ProcessPoolExecutor(
        max_workers=max(1, workers), mp_context=multiprocessing.get_context("forkserver")
    )
