# unitcircle

Python package development for the Unit Circle Programme, which studies
autoregressive roots and time-series stability.

The current version, `0.0.1.dev0`, provides a small, installable foundation. Its
only public function is `roots(phi1, phi2)`, returning the roots of
`z^2 - phi1*z - phi2`. For example, `roots(0.3, 0.1)` returns `(0.5, -0.2)` to
floating-point precision. The function's docstring specifies root ordering and
numerical limits.

## Install and verify

The recorded environment uses Python 3.12.14. From the repository directory:

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements-dev.lock
.venv/Scripts/python.exe -m pip install --no-build-isolation .
.venv/Scripts/python.exe -m unittest discover -s tests -v
```

The [package workflow](https://github.com/kostadinstoyanovuk/unitcircle/actions/workflows/ci.yml)
repeats installation and the three smoke tests on pinned Python 3.12.14.
[Recorded verification](evidence/README.md) includes the local installation,
interpreter version, dependency versions and successful test output.

## Development scope

This is a development package, not a validated research release or version 1.0.
The real-root calculation uses the companion-polynomial convention and a
cancellation-resistant product calculation. The broader research implementation
has not yet been extracted into this package. A scientific release requires
extraction and cross-validation of the frozen research implementation at M6.

The research methods and programme records are maintained in
[unit-circle](https://github.com/kostadinstoyanovuk/unit-circle).
Project licensing remains undecided.
