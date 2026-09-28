"""Causal within-window AR(2) root moduli with preserved observation labels."""
from .ar import _validate_order
from ._reference.rolling import RollingFitError
from ._reference.rolling import max_modulus as _reference_max_modulus

__all__ = ["max_modulus", "RollingFitError"]


def max_modulus(x, window: int, p: int = 2):
    """Return the root-modulus Series for fits ending at each observation.

    The window includes its first two lag-only observations and must contain
    at least five finite observations. The first window-1 outputs are NaN;
    a series shorter than the window has only warm-up output. A failed fit
    after warm-up raises RollingFitError with its endpoint, never a silent
    missing row. Supply ordered, unique labels and consecutive PeriodIndex
    periods. Only p=2 is implemented. No future observation enters a fit.
    """
    _validate_order(p)
    return _reference_max_modulus(x, window)
