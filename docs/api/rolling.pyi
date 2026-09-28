"""Design stubs only. These functions are not installed or implemented."""
from typing import Any
from numpy.random import Generator
from pandas import Series

def max_modulus(x: Any, window: int, p: int = 2) -> Series:
    """Return causal within-window root moduli with the full original index and a declared warm-up prefix.

    Requires: finite 1D; ordered unique index; consecutive PeriodIndex; window>=5; p=2 initially.
    Raises: ValueError, RollingFitError, NotImplementedOrderError.
    Planned checks: test_rolling_prefix_invariance,test_rolling_future_perturbation,test_rolling_failed_endpoint.
    Acceptance mapping: AT-1; AT-6; AT-7; causal contract.
    """
    ...

