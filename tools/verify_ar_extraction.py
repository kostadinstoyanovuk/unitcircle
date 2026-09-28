"""Compare an installed package with an immutable, locally available reference.

This bounded transfer check uses artificial observations and already-acquired
SILSO files. It does not execute registered experiments or access UK data.
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import importlib
import json
from pathlib import Path
import subprocess
import sys
import types

import numpy as np
import pandas as pd
import unitcircle
from unitcircle import ar, rolling

REFERENCE_COMMIT = "6f9400ea4aba29c3b515f6ab13659efcff572a3f"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.reference.resolve()
    commit = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    if commit != REFERENCE_COMMIT:
        raise ValueError("Reference checkout does not match the recorded extraction commit")
    source_root = root / "src" / "uc_core"
    preserved = Path(ar.__file__).parent / "_reference"
    source_hashes = {}
    for name in ("ar.py", "rolling.py"):
        source = source_root / name
        blob = subprocess.check_output(["git", "-C", str(root), "show", f"{commit}:src/uc_core/{name}"])
        if source.read_bytes().replace(b"\r\n", b"\n") != blob.replace(b"\r\n", b"\n"):
            raise ValueError(f"Reference source has uncommitted changes: {name}")
        if source.read_bytes() != (preserved / name).read_bytes():
            raise ValueError(f"Preserved source differs from the reference: {name}")
        source_hashes[name] = digest(source)

    # Import just these reference modules; do not load unrelated analysis code.
    package = types.ModuleType("_transfer_reference")
    package.__path__ = [str(source_root)]
    sys.modules[package.__name__] = package
    ref_ar = importlib.import_module("_transfer_reference.ar")
    ref_rolling = importlib.import_module("_transfer_reference.rolling")
    rng = np.random.default_rng(20260928)
    artificial = rng.normal(size=256)
    fixtures = {"artificial": artificial, "artificial_affine": artificial / .6 + 5,
                "artificial_short": artificial[:12]}
    manifest = pd.read_csv(root / "DATA_MANIFEST.csv")
    data_hashes = {}
    for name, separator in (("yearssn.dat", None), ("SN_y_tot_V2.0.csv", ";")):
        path = root / "data" / "raw" / name
        relative = "data/raw/" + name
        rows = manifest[manifest["file"] == relative]
        if len(rows) != 1 or digest(path) != rows.iloc[0]["sha256"]:
            raise ValueError(f"Existing data manifest does not verify {name}")
        data_hashes[relative] = digest(path)
        parsed = np.loadtxt(path, delimiter=separator, usecols=(0, 1))
        years = np.floor(parsed[:, 0]).astype(int)
        for start, end in ((1749, 1924), (1925, 2008)):
            selected = (years >= start) & (years <= end)
            if not np.array_equal(years[selected], np.arange(start, end + 1)):
                raise ValueError("Incomplete sunspot reference interval")
            fixtures[f"{name}:{start}-{end}"] = parsed[selected, 1]

    comparisons = []
    for name, values in fixtures.items():
        for method in ("fit_ols", "fit_yw"):
            expected = getattr(ref_ar, method)(values)
            actual = getattr(ar, method)(values)
            for attr in ("method", "coefficients", "intercept", "n_observations",
                         "n_regression_rows", "residuals"):
                if getattr(actual, attr) != getattr(expected, attr):
                    raise AssertionError(f"{name} {method} differs in {attr}")
            if dataclasses.asdict(actual.diagnostics) != dataclasses.asdict(expected.diagnostics):
                raise AssertionError(f"{name} {method} diagnostics differ")
            comparisons.append({"fixture": name, "method": method, "equality": "exact"})
        labelled = pd.Series(values, index=pd.period_range("1700", periods=len(values), freq="Y"))
        pd.testing.assert_series_equal(rolling.max_modulus(labelled, 40),
                                       ref_rolling.max_modulus(labelled, 40), check_exact=True)

    result = {"status": "passed", "scope": "bounded installed-package transfer verification",
              "reference_commit": commit, "package_version": unitcircle.__version__,
              "package_location": str(Path(unitcircle.__file__).resolve()),
              "numpy_version": np.__version__, "pandas_version": pd.__version__,
              "preserved_source_sha256": source_hashes, "input_data_sha256": data_hashes,
              "data_attribution": "WDC-SILSO, Royal Observatory of Belgium; existing manifest CC BY-NC 4.0",
              "fit_comparisons": comparisons, "rolling_comparisons": len(fixtures),
              "core_v1_comparison": "pending: core-v1 does not yet exist",
              "registered_experiments_executed": False, "uk_data_accessed": False,
              "release_accepted": False}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Passed {len(comparisons)} exact fit comparisons and {len(fixtures)} exact rolling comparisons")


if __name__ == "__main__":
    main()
