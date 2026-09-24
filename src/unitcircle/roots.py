"""AR(2) companion roots for infrastructure checks."""

import math


def roots(phi1: float, phi2: float) -> tuple[complex, complex]:
    """Return roots of z**2 - phi1*z - phi2 for finite real coefficients.

    A conjugate pair has the positive imaginary part first. Real roots put
    the root with greater absolute value first (positive first on a tie).
    These are companion roots, not reciprocals of lag-polynomial roots.
    Floating-point arithmetic is used; this is not a certified root checker.
    """
    a, b = float(phi1), float(phi2)
    discriminant = a * a + 4 * b
    if not all(math.isfinite(v) for v in (a, b, discriminant)):
        raise ValueError("Finite coefficients and a finite discriminant are required")
    if discriminant < 0:
        imaginary = math.sqrt(-discriminant) / 2
        return complex(a / 2, imaginary), complex(a / 2, -imaginary)
    # Recover the smaller root from the product to reduce cancellation.
    large = (a + math.copysign(math.sqrt(discriminant), a)) / 2
    small = -b / large if large else 0.0
    return complex(large), complex(small)
