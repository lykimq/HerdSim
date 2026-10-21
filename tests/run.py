"""Guards to run before a campaign: tests and benchmarks.

    uv run python -m tests.run test    unit, invariant and reproducibility tests
    uv run python -m tests.run bench   miniature real campaigns, read for sense

The Makefile exposes both. Campaigns start from cli/campaign.py.
"""

from __future__ import annotations

import os

# One BLAS thread per process, as in campaigns, so the speed the bench prints matches a campaign.
# Must be set before NumPy is imported.
for _var in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_var] = "1"

import argparse  # noqa: E402

import pytest  # noqa: E402


def run_tests() -> int:
    return int(pytest.main(["tests", "-q"]))


def run_bench() -> int:
    return int(pytest.main(["tests", "-q", "-m", "bench", "-rP"]))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("verb", choices=("test", "bench"))
    verb = parser.parse_args().verb
    code = run_tests() if verb == "test" else run_bench()
    raise SystemExit(code)


if __name__ == "__main__":
    main()
