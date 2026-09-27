"""Low-overhead structured latency logging for request diagnostics."""
from __future__ import annotations

import logging
import time
from contextlib import contextmanager
from collections.abc import Iterator


logger = logging.getLogger("aarohan.latency")


def elapsed_ms(start: float) -> int:
    """Return monotonic elapsed time rounded to whole milliseconds."""

    return round((time.perf_counter() - start) * 1000)


def log_latency(operation: str, stage: str, duration_ms: int, **fields: object) -> None:
    """Emit a single safe timing line without request or model content."""

    details = " ".join(f"{key}={value}" for key, value in fields.items())
    suffix = f" {details}" if details else ""
    logger.info("[LATENCY] %s %s_ms=%d%s", operation, stage, duration_ms, suffix)


@contextmanager
def timed(operation: str, stage: str, **fields: object) -> Iterator[None]:
    """Measure and log a named stage even when it raises an exception."""

    start = time.perf_counter()
    try:
        yield
    finally:
        log_latency(operation, stage, elapsed_ms(start), **fields)
