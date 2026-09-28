# unitcircle

Development package for autoregressive roots and time-series stability.

Version `0.0.2.dev0` adds `unitcircle.ar` (AR(2) OLS, Yule-Walker and root
diagnostics) and `unitcircle.rolling.max_modulus`. The existing top-level
`unitcircle.roots(phi1, phi2)` remains compatible. Only AR order two is supported.

## Installation and checks

Use Python 3.12.14 in an isolated environment, install `requirements-dev.lock`,
then install this package with `pip install --no-build-isolation .`.
Run `python -m unittest discover -s tests -v`.

The first extraction checkpoint has 16 passing installed-package tests.
It matches the preserved research reference exactly on 14 fit comparisons and
seven rolling paths; see [extraction evidence](evidence/AR_EXTRACTION.md).
These are bounded transfer checks, not a completed scientific release.

## Example

```python
from unitcircle.ar import fit_ols, roots
from unitcircle.rolling import max_modulus

x = [1.2, -0.7, 0.4, 1.1, -1.3, 0.2, 0.9, -0.4, 1.5, -0.8, 0.3]
fit = fit_ols(x)
print(fit.coefficients)
print(fit.residual_series)  # labels start at the third observation
print(roots((0.3, 0.1)))
print(max_modulus(x, window=6))  # first five observations are warm-up
```

Residual numerical values remain tuples; residual_index and residual_series
return copies. Period and half-life are measured in sampling intervals. Roots
use the companion convention; undefined diagnostics remain None. Rolling
calculations use trailing windows and reject failed fits rather than skip them.

[Design](docs/design.md) describes the broader candidate API. Its later methods
are not implemented or exported by this checkpoint. The present errors retain
the reference ValueError classes rather than introduce the proposed future
exception taxonomy. No `core-v1` comparison or M6 completion is claimed.
Project licensing remains undecided pending the release decision.
