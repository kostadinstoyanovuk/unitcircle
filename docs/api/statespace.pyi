"""Design stubs only. These functions are not installed or implemented."""
from typing import Any
from numpy.random import Generator
from pandas import Series
from ._types import FilterResult, TVPFit

def kalman_filter(y: Any, Z: Any, T: Any, Q: Any, H: float, a1: Any, P1: Any, *, burn: int = 0) -> FilterResult:
    """Apply the reference square-root filter and prediction-error likelihood with explicit finite initial covariance.

    Requires: finite compatible dimensions; H>0; symmetric PSD Q/P1; matching labels; 0<=burn<n.
    Raises: ValueError, NumericalError.
    Planned checks: test_filter_diffuse_ols,test_filter_scalar_analytic,test_filter_shapes_covariances.
    Acceptance mapping: AT-11.
    """
    ...

def tvp_ar_mle(x: Any, p: int = 2, *, specification: Any) -> TVPFit:
    """Fit the frozen E3 time-varying model and retain convergence, initialisation and filtering diagnostics.

    Requires: finite series; supported order; complete frozen E3 specification.
    Raises: ValueError, EstimationError, PendingMethodError.
    Planned checks: test_tvp_frozen_e3_reference,test_tvp_nonconvergence_visible.
    Acceptance mapping: AT-11; frozen E3 outputs.
    """
    ...

