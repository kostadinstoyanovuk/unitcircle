"""Design stubs only. These functions are not installed or implemented."""
from typing import Any
from numpy.random import Generator
from pandas import Series
from ._types import ARFit, PeakResult

def fit_ols(x: Any, p: int = 2) -> ARFit:
    """Fit intercept-inclusive least squares using only within-sample lags; retain unstable estimates and indexed residuals.

    Requires: finite 1D; n>=2*p+1; identifiable lags; p=2 initially.
    Raises: ValueError, EstimationError, NotImplementedOrderError.
    Planned checks: test_ols_frozen_reference,test_ols_rank_failure,test_ols_series_residual_index.
    Acceptance mapping: AT-1; AT-3; AT-4.
    """
    ...

def fit_yw(x: Any, p: int = 2) -> ARFit:
    """Fit demeaned Yule-Walker using one full-sample energy denominator for every lag.

    Requires: finite nonconstant 1D; n>=2*p+1; nonsingular system; p=2 initially.
    Raises: ValueError, EstimationError, NotImplementedOrderError.
    Planned checks: test_yw_common_denominator,test_yw_frozen_reference.
    Acceptance mapping: AT-2.
    """
    ...

def roots(phi: Any) -> tuple[complex, ...]:
    """Return companion-polynomial roots with the existing AR(2) ordering and cancellation-resistant real calculation.

    Requires: finite 1D coefficients; length=2 initially; no arithmetic overflow.
    Raises: ValueError, NumericalError, NotImplementedOrderError.
    Planned checks: test_roots_analytic,test_roots_polynomial_residual,test_legacy_two_argument_wrapper.
    Acceptance mapping: AT-1; AT-6.
    """
    ...

def modulus(phi: Any) -> float:
    """Return the largest companion-root modulus without clipping at the unit circle.

    Requires: same coefficient checks as roots.
    Raises: ValueError, NumericalError, NotImplementedOrderError.
    Planned checks: test_modulus_complex_identity,test_modulus_companion.
    Acceptance mapping: AT-6; AT-12.
    """
    ...

def period(phi: Any) -> float | None:
    """Return the AR(2) complex-pair period in sampling intervals, or None for real roots.

    Requires: finite AR(2) coefficients; period does not imply stability.
    Raises: ValueError, NumericalError, NotImplementedOrderError.
    Planned checks: test_period_sunspot_reference,test_period_real_and_repeated_roots.
    Acceptance mapping: AT-1; AT-2; AT-3.
    """
    ...

def half_life(phi: Any) -> float | None:
    """Return the modulus-envelope decay half-life; zero at zero modulus and None at or beyond one.

    Requires: finite AR(2) coefficients; no negative decay times.
    Raises: ValueError, NumericalError, NotImplementedOrderError.
    Planned checks: test_half_life_zero_unit_explosive.
    Acceptance mapping: AT-1.
    """
    ...

def in_triangle(phi1: float, phi2: float) -> bool:
    """Classify the strict open AR(2) stability triangle, without tolerance-based projection.

    Requires: two finite real scalars.
    Raises: ValueError.
    Planned checks: test_triangle_root_agreement,test_triangle_equalities.
    Acceptance mapping: AT-7.
    """
    ...

def spectral_peak(phi1: float, phi2: float) -> PeakResult | None:
    """Return the interior spectral-peak diagnostic for a stable AR(2), or None outside stability.

    Requires: two finite real scalars; strict stability for a defined diagnostic.
    Raises: ValueError, NumericalError.
    Planned checks: test_peak_numerical_grid,test_complex_without_peak,test_peak_unstable_undefined.
    Acceptance mapping: AT-10.
    """
    ...

