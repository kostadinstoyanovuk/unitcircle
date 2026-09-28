"""AR(2) fits and companion-root diagnostics extracted from the research code.

Only order two is currently supported. Parameters are never projected onto
the stationary region. Undefined diagnostics remain None.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import numpy as np
import pandas as pd

from ._reference import ar as _reference
from ._reference.ar import RootSummary
from ._reference.rolling import _observations_and_index

__all__ = ["ARFit", "RootSummary", "PeakResult", "fit_ols", "fit_yw",
           "roots", "modulus", "period", "half_life", "in_triangle", "spectral_peak"]


@dataclass(frozen=True)
class PeakResult:
    """Interior-peak status and angular frequency in radians per sample."""
    has_interior_peak: bool
    frequency: float | None


@dataclass(frozen=True)
class ARFit:
    """Immutable numerical fit with copied labels for conditional residuals.

    Residuals remain the reference tuple. residual_index and residual_series
    return copies so changing their metadata cannot change this fit.
    """
    method: str
    coefficients: tuple[float, float]
    intercept: float
    n_observations: int
    n_regression_rows: int
    residuals: tuple[float, ...]
    diagnostics: RootSummary
    _residual_index: pd.Index = field(repr=False, compare=False)

    @property
    def residual_index(self) -> pd.Index:
        return self._residual_index.copy(deep=True)

    @property
    def residual_series(self) -> pd.Series:
        return pd.Series(self.residuals, index=self.residual_index,
                         dtype=float, name="residual")


def _validate_order(p: int) -> None:
    if isinstance(p, (bool, np.bool_)) or not isinstance(p, (int, np.integer)) or p < 1:
        raise ValueError("p must be a positive integer")
    if p != 2:
        raise NotImplementedError("Only the research AR(2) extraction is supported")


def _fit(x, p, method) -> ARFit:
    _validate_order(p)
    values, index = _observations_and_index(x)
    fitted = method(values)
    return ARFit(fitted.method, fitted.coefficients, fitted.intercept,
                 fitted.n_observations, fitted.n_regression_rows,
                 fitted.residuals, fitted.diagnostics,
                 index[2:].copy(deep=True))


def fit_ols(x, p: int = 2) -> ARFit:
    """Fit intercept-inclusive least squares on within-sample AR(2) lags.

    Requires five finite real observations and identifiable lag columns.
    Series indexes must be unique and increasing, with consecutive periods
    for a PeriodIndex. Invalid data or singular fits raise ValueError;
    unsupported orders raise NotImplementedError. Unstable fits are retained.
    """
    return _fit(x, p, _reference.fit_ols)


def fit_yw(x, p: int = 2) -> ARFit:
    """Fit demeaned Yule-Walker using a common full-sample denominator.

    The implied intercept is mean(x)*(1-sum(phi)). Conditional residuals
    are not recentered. Input, index and order rules match fit_ols;
    constant input or a singular system raises ValueError.
    """
    return _fit(x, p, _reference.fit_yw)


def roots(phi) -> tuple[complex, complex]:
    """Return roots of z**2-phi[0]*z-phi[1], using the research ordering.

    A nonreal pair has its positive imaginary part first. Real roots use
    the cancellation-resistant ordering of the reference. Supply exactly
    two finite real coefficients; invalid input or overflow raises ValueError.
    The existing top-level unitcircle.roots(phi1, phi2) remains available.
    """
    return _reference.root_summary(phi).roots


def modulus(phi) -> float:
    """Return the maximum companion-root modulus without clipping at one."""
    return _reference.root_summary(phi).modulus


def period(phi) -> float | None:
    """Return the nonreal AR(2) pair's period in samples, or None for real roots.

    A period does not establish stability; negative real roots can alternate
    but have no complex-pair period under this convention.
    """
    return _reference.root_summary(phi).period


def half_life(phi) -> float | None:
    """Return envelope decay half-life, zero at modulus zero, None at M>=1."""
    return _reference.root_summary(phi).half_life


def in_triangle(phi1: float, phi2: float) -> bool:
    """Classify the strict open AR(2) stability triangle, without tolerance."""
    return _reference.in_triangle(phi1, phi2)


def spectral_peak(phi1: float, phi2: float) -> PeakResult | None:
    """Return the stationary interior-peak diagnostic, or None if unstable.

    Endpoint peaks are not interior. Frequency is in radians per sample.
    Complex roots alone do not imply an interior spectral peak.
    """
    summary = _reference.root_summary((phi1, phi2))
    if summary.spectral_peak is None:
        return None
    return PeakResult(summary.spectral_peak, summary.peak_frequency)
