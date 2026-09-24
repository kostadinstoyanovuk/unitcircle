# Local verification, 2026-09-24

Run from this repository, using Python 3.12.14:

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements-dev.lock
.venv/Scripts/python.exe -m pip install --no-build-isolation .
.venv/Scripts/python.exe -m unittest discover -s tests -v
.venv/Scripts/python.exe -m pip freeze --all
```

All commands completed successfully. The package wheel was built and installed
into this repository's separate environment. Three tests passed. The source uses
a `src/` layout, so these tests import the installed package, not an implicit
working-directory module. Logs and interpreter/version records accompany this file.
These records describe local verification. Current hosted checks are available
through the repository's package workflow. Source metadata snapshots pin the
workflow actions and build backend; the provenance list also points to Lean
sources archived in the separate `schur-cohn/evidence` directory.
