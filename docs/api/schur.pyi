"""Design stubs only. These functions are not installed or implemented."""
from typing import Any
from numpy.random import Generator
from pandas import Series

def schur_cohn_stable(coeffs: Any) -> bool:
    """Test strict disc stability of ascending finite complex coefficients, without claiming an exact certificate.

    Requires: nonempty 1D coefficients; nonzero leading coefficient; finite intermediate arithmetic.
    Raises: ValueError, NumericalError.
    Planned checks: test_schur_constant_zero_boundary,test_schur_random_root_agreement,test_schur_overflow_visible.
    Acceptance mapping: AT-8.
    """
    ...

