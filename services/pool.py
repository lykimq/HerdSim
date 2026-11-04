"""Worker pool shared by calibration and campaign batches.

Workers start from a fork server, not by forking the parent: forking a process that
already runs threads can deadlock, and fresh workers read the single-thread BLAS settings
from the environment at import.
"""

from __future__ import annotations

import argparse
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


def limit_threads() -> None:
    for var in THREAD_LIMIT_VARS:
        os.environ[var] = "1"


def check_workers(workers: int) -> int:
    """``workers``, if at least 1: a batch queues ``workers`` times a few trials, so zero
    workers would queue nothing and a campaign would idle until its budget runs out."""
    if workers < 1:
        raise ValueError(f"workers must be at least 1, got {workers}")
    return workers


def worker_count(text: str) -> int:
    """argparse type of the --workers option of every command."""
    try:
        return check_workers(int(text))
    except ValueError as err:
        raise argparse.ArgumentTypeError(str(err)) from err


def worker_pool(workers: int) -> ProcessPoolExecutor:
    # Set in the parent too: the fork server reads its environment at start.
    limit_threads()
    return ProcessPoolExecutor(
        max_workers=check_workers(workers),
        mp_context=multiprocessing.get_context("forkserver"),
        initializer=limit_threads,
    )
