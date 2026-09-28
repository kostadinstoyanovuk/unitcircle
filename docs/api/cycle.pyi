"""Design stubs only. These functions are not installed or implemented."""
from typing import Any
from numpy.random import Generator
from pandas import Series
from ._types import CycleTestResult

def complex_root_test(x: Any, *, selection: Any, alpha: float = 0.05, rng: Generator | None = None) -> CycleTestResult:
    """Apply only the C3.TEST-selected complex-root test, identified by its frozen calibration record.

    Requires: finite series; 0<alpha<1; valid selection; Generator for a stochastic selected method.
    Raises: ValueError, PendingMethodError.
    Planned checks: test_complex_test_selection_required,test_complex_test_reduced_calibration.
    Acceptance mapping: AT-9; AT-17; AT-18; C3.TEST DR-3.
    """
    ...

def spectral_peak_test(x: Any, *, selection: Any, alpha: float = 0.05, rng: Generator | None = None) -> CycleTestResult:
    """Apply only the separately selected interior-peak test, respecting its kink and calibration domain.

    Requires: finite series; 0<alpha<1; valid selection; Generator where required.
    Raises: ValueError, PendingMethodError.
    Planned checks: test_spectral_test_selection_required,test_spectral_test_kink_policy.
    Acceptance mapping: AT-10; C3.TEST DR-3.
    """
    ...

