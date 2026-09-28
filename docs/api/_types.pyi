"""Result-shape design stubs; see docs/design.md for ownership and semantics."""
from typing import Any
from dataclasses import dataclass

@dataclass(frozen=True)
class PeakResult:
    has_interior_peak: bool
    frequency: float | None

@dataclass(frozen=True)
class RootSummary:
    roots: tuple[complex, ...]
    modulus: float
    stable: bool
    discriminant: float | None
    complex_pair: bool | None
    period: float | None
    half_life: float | None
    peak: PeakResult | None
    undefined_reason: str | None

@dataclass(frozen=True)
class ARFit:
    method: str
    coefficients: tuple[float, ...]
    intercept: float
    n_observations: int
    n_regression_rows: int
    residuals: Any
    diagnostics: RootSummary

@dataclass(frozen=True)
class EpisodeSet:
    index: Any
    episodes: tuple[Any, ...]

@dataclass(frozen=True)
class SurrogateBatch:
    attempts: tuple[Any, ...]
    index: Any
    null_model: Any
    initial_values: Any
    rng_before: dict[str, Any]
    rng_after: dict[str, Any]

@dataclass(frozen=True)
class CSDResult:
    status: str
    observed: Any
    p_value: float | None
    requested: int
    attempted: int
    retained: int
    no_episode: int
    failed: int
    exceedances: int | None
    p_grid_spacing: float | None
    attempts: tuple[Any, ...]
    null_model: Any
    settings: dict[str, Any]
    rng_before: dict[str, Any]
    rng_after: dict[str, Any]

@dataclass(frozen=True)
class FilterResult:
    filtered_states: Any
    prediction_errors: Any
    prediction_variances: Any
    loglik: float
    burn: int
    initialisation: dict[str, Any]

@dataclass(frozen=True)
class TVPFit:
    specification: Any
    parameters: Any
    optimisation: Any
    filter_result: FilterResult
    root_path: Any

@dataclass(frozen=True)
class CycleTestResult:
    definition: str
    selection: Any
    statistic: float | None
    p_value: float | None
    reject: bool | None
    alpha: float
    status: str
    diagnostics: Any
    rng_before: dict[str, Any] | None
    rng_after: dict[str, Any] | None

@dataclass(frozen=True)
class PlotResult:
    figure: Any
    axes: Any
    provenance: dict[str, Any]

