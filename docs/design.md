# unitcircle: public API and extraction design

Status: review-ready design candidate for C5.1; not an implemented or released API. Owner: Kostadin Stoyanov. Date: 28 September 2026.

This document implements the design obligation on working-plan pages 18–19: a signature, input contract, return type, error contract, docstring stub and named acceptance test for every function in the module table. The companion `api/` directory contains signature/docstring stubs; `api-contracts.json` is the machine-readable coverage inventory. Named tests are specifications for future implementation, not claims of passing tests.

## 1. Source and release boundaries

Research reference: `unit-circle@6f9400ea4aba29c3b515f6ab13659efcff572a3f`. Existing package: `unitcircle@55b3c906aa1da28cf384eba296ea20918c40e65d`. Formal reference: `schur-cohn@a907f9910b7736340bd98e31947fdef1747e7149`.

The research snapshot provides implemented AR(2), causal rolling fits, retrospective episodes, fitted-null surrogates, the H1 test, a square-root Kalman filter and a floating-point Schur recursion. It does not contain a frozen H1 empirical result, a completed E3 model or Paper II's selected tests. Extraction may be prepared now, but comparison with `core-v1`, E3 and C3.TEST cannot be marked complete before those reference artifacts exist.

Move the reference algorithms rather than recreating them. First demonstrate unchanged numerical outputs and random-number consumption. Optimisation, broader order support and altered numerical checks are separately recorded changes. Maintain the scientific reference even if an alternative implementation later becomes faster. No release changes registered methods retroactively.

The currently installed top-level `unitcircle.roots(phi1, phi2)` remains compatible. The planned module API `unitcircle.ar.roots(phi)` takes a coefficient sequence. Keep the existing two-argument entry point as a documented wrapper; do not silently change its calling convention during extraction. A development version is distinct from v1.0.

## 2. Common data contracts

- Univariate data: a real one-dimensional numeric sequence or pandas Series, converted to a private float64 array. Reject complex, missing or non-finite observations, wrong dimensions, and silent coercions that lose information. Do not fill, interpolate, sort, drop or rescale the returned data automatically.
- Coefficients: AR order is `(phi_1, ..., phi_p)` in the companion polynomial `z^p - phi_1 z^(p-1) - ... - phi_p`. Polynomial coefficient input for Schur is a separate convention: ascending `(a_0, ..., a_n)`, with a nonzero final coefficient.
- Time: copy the Series index into time-aligned results. Arrays receive a RangeIndex. Reject duplicate or non-increasing labels. A PeriodIndex must have consecutive periods. A generic DatetimeIndex is not assumed to prove regular sampling; document the caller's sampling interval. No function sorts an index on the caller's behalf.
- Estimator parameters are not time series. ARFit has no parameter time index, but its residuals retain the input labels starting at position `p`. Root diagnostics use sampling intervals; converting to years is an explicit caller choice.
- Integer parameters reject booleans. Initially only `p=2` is validated for the extracted research path. Other orders raise `NotImplementedOrderError` until a separately tested extension exists. Signatures retain `p` so this limitation is explicit rather than accidental.
- `rng` must be an explicitly supplied numpy Generator. Create it once from the appropriate registered stream outside the numerical function. Do not use global random state, silently replace the generator, seed inside a loop, retry a failed draw, or consume random numbers during input validation.
- Return containers are frozen dataclasses. Numeric arrays and labelled residuals are owned copies; array write flags alone are not claimed as deep immutability. Accessors return copies where needed. Input data and global random state remain unchanged. The supplied generator advances by the documented successful or failed attempt sequence.
- Undefined scientific quantities use `None` with a reason/status, never zero, a fabricated p-value or a disappearing row. NaN is permitted only as the declared leading warm-up region of aligned rolling results.

## 3. Result types

| Type | Required fields and interpretation |
|---|---|
| ARFit | method; coefficient tuple; intercept; observation count; regression-row count; residual tuple plus indexed residual_series; RootSummary |
| RootSummary | companion roots; maximum modulus; stability; AR(2) discriminant/complex-pair flag; period; half-life; PeakResult or undefined reason |
| PeakResult | has_interior_peak; angular frequency or None, in radians per sample; stable-model requirement |
| EpisodeSet | index; tuple of episodes with zero-based onset/end positions and all constituent negative runs; labels derived from the retained index |
| SurrogateBatch | attempt numbers/statuses; paths for successful attempts; original index; fitted null identity; centred residual definition; initial values; RNG states before/after; failures |
| CSDResult | status; observed S; every episode change; eligible/ineligible onsets; requested/attempted/retained/no-episode/failed counts; exceedances; p-value; p-grid; attempt records; null model; settings and RNG states |
| FilterResult | indexed filtered states; prediction errors/variances; log-likelihood; burn count and initial-condition metadata |
| TVPFit | selected model identifier; estimated parameters; optimiser/convergence diagnostics; filter result; causal fitted-coefficient root path; optimisation bounds and initialisation |
| CycleTestResult | cycle definition; selected test/version and calibration identity; statistic; p-value if estimable; rejection at explicit alpha; estimator; diagnostics and RNG metadata |
| PlotResult | Matplotlib Figure and Axes; plotted-data provenance and any excluded/undefined points, without writing a file automatically |

Do not put an arbitrary fitted cycle's period into a field that promises a single AR(2) conjugate-pair period. General-order diagnostics need their own design before support is enabled.

## 4. Function contracts

The exact signatures and one-paragraph docstring stubs are in `api/`. Type aliases and result names there refer to this document. The inventory records one or more future test names and source/dependency status for every entry.

### unitcircle.ar

`fit_ols(x, p=2) -> ARFit`: require at least `2*p+1` finite observations in the initial extraction (five for AR(2)), identifiable lag columns and a full-rank centred lag design. Include an intercept; use the first p values only as lags. Retain unstable estimates. Centre/scale lag columns exactly as the reference and recover the intercept from means. ValueError covers invalid data; The proposed EstimationError covers singularity, non-finite calculation or solver failure; the initial extraction retains the reference ValueError until that taxonomy is adopted. AT-1, AT-3 and AT-4 pin coefficients and invariance; named checks also cover index alignment, residual reconstruction and input preservation. Supporting arbitrary p must not be confused with currently validated p=2.

`fit_yw(x, p=2) -> ARFit`: remove the selected interval mean; for lag k use `sum(x[t]*x[t+k])/sum(x[t]^2)` on demeaned values, with the same full-sample denominator for every lag. Return `mean(x)*(1-sum(phi))` as intercept and conditional residuals without automatically recentering them. Reject constant data and singular systems. AT-2 pins the result; named checks distinguish this estimator from adjusted lag-dependent denominators.

`roots(phi) -> tuple[complex, ...]`: companion roots, never reciprocal lag roots. For AR(2), preserve the reference's cancellation-resistant real-root calculation and place the positive imaginary part first for a complex pair. For real roots retain the existing package's magnitude-first ordering; tests must cover equal magnitudes and signed zero before documenting a stronger tie guarantee. Reject non-finite coefficients and overflow. AT-1/AT-6 plus analytic roots and residual-in-polynomial checks pin the implementation. Only order 2 is supported initially.

`modulus(phi) -> float`: maximum absolute companion root; uses the same root calculation. No clipping at one. AT-6 and AT-12 pin it.

`period(phi) -> float | None`: for a strictly nonreal AR(2) pair, `2*pi/atan2(sqrt(-D), phi1)`, with `D=phi1^2+4*phi2`. Negative real and repeated real roots have no complex-pair period. A finite period can describe an unstable oscillation; report stability separately. AT-1/AT-2/AT-3 and real-root edge cases pin it.

`half_life(phi) -> float | None`: envelope decay `log(2)/(-log(M))` for `0<M<1`; zero at M=0 by the reference convention; None for M>=1. Never report an explosive model's negative decay time. AT-1 and explicit zero/unit/explosive cases pin it.

`in_triangle(phi1, phi2) -> bool`: strict inequalities `phi1+phi2<1`, `phi2-phi1<1`, `phi2>-1`. Validate finite real scalars; no tolerance changes this definition. AT-7 compares against roots away from the registered edge margin; deterministic boundary tests cover equality.

`spectral_peak(phi1, phi2) -> PeakResult | None`: only defined for a strictly stable model. An interior peak requires `phi2<0` and `abs(phi1)*(1-phi2)<-4*phi2`; its frequency is `acos(phi1*(phi2-1)/(4*phi2))`. Clamp only roundoff in the inverse-cosine argument, not the decision inequality. An unstable model returns None; an endpoint peak returns `has_interior_peak=False`. AT-10 and `(1,-0.3)` distinguish spectral peaks from complex roots.

### unitcircle.rolling

`max_modulus(x, window, p=2) -> Series`: integer window at least five for AR(2). At position t fit exactly `x[t-window+1:t+1]`, using `window-p` regression outcomes within that window. Preserve the entire input index with the first `window-1` values NaN. A shorter series is all warm-up. A failure after warm-up raises RollingFitError identifying its endpoint; no skipped or repaired windows. Prefix-invariance, future-perturbation, endpoint and frozen-reference comparisons pin causality. AT-1/AT-6/AT-7 pin the underlying method.

### unitcircle.recession

`episodes(g, rule='two_negative', merge=8) -> EpisodeSet`: currently only that rule; merge a nonnegative integer. A run requires at least two strictly negative observations; zero breaks it. Qualifying runs merge when the next onset minus the last qualifying run's end is at most merge. Keep the first onset of a chained episode. Isolated negative observations never move the merging clock. Positions are zero-based, endpoints inclusive, labels retained. These are retrospective episodes; the first negative quarter is not an onset observable without future confirmation. Deterministic rule, gap, chaining, zero and index checks pin this function; there is no separate original numbered acceptance test for episode boundaries.

### unitcircle.surrogate

`ar_surrogates(x, B, rng, p=2, *, innovation='residual') -> SurrogateBatch`: positive integer B, explicit Generator and a strictly stable identifiable full-sample AR(2) null. Preserve the first two observed values; draw the remaining innovations from mean-centred fitted residuals with replacement. `innovation='wild'` uses the reference's independent random signs and residual ordering. There is no burn-in or stationarity projection in the reference H1 null. Retain exactly B attempted paths with failures visible; numerical failure does not create a replacement draw. ValueError handles options; NullModelError handles an unusable fitted null. AT-13 pins long-series recovery; seed/state and initial-condition checks pin extraction. This lower-level path generator does not itself decide whether a path contains an eligible episode.

`var_surrogates(X, B, rng, p=1) -> SurrogateBatch`: reserved contract for E2, not an implemented current method. Require a finite two-dimensional array or DataFrame with aligned, unique ordered rows and named columns. Proposed residual resampling uses whole residual vectors to preserve contemporaneous dependence, with full companion stability and fixed initial p vectors. The exact intercept, estimator, initialisation and random sequence must be fixed in E2's registered design before implementation. Raise PendingMethodError until that design exists. E2 frozen-output reproduction and AT-12 are dependencies, not current pass claims.

### unitcircle.test

`csd_test(g, window, lookback, B, rng, onsets='endogenous', *, merge=8, innovation='residual') -> CSDResult`: uses the established episode and rolling contracts; defaults must not replace a supplied registered setting. Supported onset modes are endogenous and the reference fixed-date diagnostic; translate argument names to the reference's `onset_mode` and `innovation_mode` explicitly. The observed change is `M[t_r-1]-M[t_r-lookback-1]`; never use onset-quarter values. No eligible observed episodes gives a non-estimable result, not zero. Recompute episodes inside each endogenous surrogate. Only no-eligible-episode surrogates may be excluded from the retained denominator; computational failures invalidate p and remain recorded. Apply the registered empty and small-retained-sample rules unchanged from prereg/H1.md. For a defined comparison use `(1 + count(S_b >= S))/(B_retained+1)`, including ties. AT-14 pins arithmetic, AT-15/AT-16 calibration, and fixed-seed reference checks pin extraction. Do not rerun full registered experiments merely to populate a fast development test suite.

### unitcircle.statespace

`kalman_filter(y, Z, T, Q, H, a1, P1, *, burn=0) -> FilterResult`: univariate finite y of length n, finite Z of shape `(n,m)`, finite T/Q/P1 of shape `(m,m)`, a1 of length m, finite H>0, symmetric positive-semidefinite covariance inputs, and integer `0<=burn<n`. Match Series/DataFrame labels before matrix conversion where labels are supplied; do not silently align and drop rows. The first returned state is the measurement update from a1/P1; transition follows each update. Burn excludes initial likelihood terms, not observations or filtering. Preserve the corrected square-root algorithm; a large finite initial covariance is approximate diffuse initialisation, not an exact diffuse filter. AT-11 and the retained version-1 failure/version-2 correction pin numerical requirements. Additional shape/symmetry/finite checks are explicit wrapper validation and require tests; they are not evidence that the reference already enforces them.

`tvp_ar_mle(x, p=2, *, specification) -> TVPFit`: reserved E3 contract. `specification` must identify the frozen observation model, time-varying coefficient/intercept structure, initialisation, optimisation bounds and method, observation/state variances and causal filtering convention. Insufficient, unregistered or unsupported specifications raise PendingMethodError. Record optimiser failure explicitly; never substitute a converged-looking estimate. A filtered path conditional on full-sample estimated hyperparameters must not be described as a real-time forecast experiment. AT-11 plus E3's frozen estimates/path pin future validation.

### unitcircle.cycle

`complex_root_test(x, *, selection, alpha=0.05, rng=None) -> CycleTestResult` and `spectral_peak_test(x, *, selection, alpha=0.05, rng=None) -> CycleTestResult`: reserved public interfaces for the eventual separate C3.TEST recommendations. `selection` identifies the frozen test, estimator, supported domain, calibration record and bootstrap settings. Reject an absent or unvalidated selection with PendingMethodError. Alpha must lie strictly between zero and one; a stochastic selected method requires an explicit Generator, while a deterministic method must not consume it. Test candidates remain internal until DR-3 selects a valid procedure. No valid candidate is an allowed research outcome, so v1.0 must not manufacture one; record the resulting release-scope decision. AT-9/AT-10/AT-17/AT-18 support the theory, while C3.TEST's size/power criteria decide acceptance. Handle the spectral-statistic kink separately; do not import a smooth gradient formula at zero without justification.

### unitcircle.schur

`schur_cohn_stable(coeffs) -> bool`: finite nonempty ascending complex coefficients, with nonzero leading coefficient. A nonzero constant is stable; the zero polynomial or trailing leading-zero representation raises ValueError. Use the fixed-vector-degree reciprocal and Schur transform, including a zero constant coefficient; equality of endpoint norms fails strict stability. AT-8 and deterministic constant/linear/boundary/repeated-root cases pin it. The initial version is floating point, not a formal certificate. Extraction must explicitly detect non-finite intermediate arithmetic and raise NumericalError; treating overflow as stable is unacceptable. Compare any added scaling scheme separately with the unscaled reference and exact small examples. Formal rational checking remains a separate verified interface, not an inferred property of a float boolean.

### unitcircle.plot

`triangle(*, ax=None) -> PlotResult`: draw the strict stability region and labelled boundary with the established companion convention. The picture does not decide stability. Accept a Matplotlib Axes or create one, return both figure/axes, and perform no show/save/network operation.

`argand(roots, *, ax=None) -> PlotResult`: finite one-dimensional complex roots; draw the unit circle and equal aspect ratio. Accept roots, not undocumented coefficients; label plotted data and avoid inferring stationarity for an entire stochastic model from a picture.

`root_path(path, *, ax=None) -> PlotResult`: validated indexed sequence of root sets, preserving chronology; explicitly represent missing warm-up segments and never connect across undefined intervals. Connect corresponding roots only where a documented tracking rule or stored root identities exist; sorting independently at each time can swap paths. Without tracking information, render ordered-time points without claiming continuous root identities. Plot metadata, labels, input preservation and artist-coordinate checks pin these functions; visual review remains required for publication figures.

## 5. Error taxonomy and compatibility

`InputError`, `EstimationError`, `RollingFitError` and `NullModelError` may subclass ValueError so established caller handling survives. `NumericalError` subclasses FloatingPointError. `NotImplementedOrderError` and `PendingMethodError` subclass NotImplementedError. Do not convert an internal programming exception into an apparently scientific non-result. Attempt-level numerical failures are recorded by the same boundary used in the reference, with the original error context retained.

This is a proposed public taxonomy. Existing research exceptions and tuple/dataclass fields must be mapped explicitly. Any intentional change to previously accepted inputs requires a compatibility note and a targeted test. A named stub is not exported from the installed development package until its implementation and supported scope are verified.

## 6. Extraction order and checks

| Stage | Work | Evidence required before acceptance |
|---|---|---|
| C5.1 | Review these contracts and stubs against the plan and reference code | Every function covered; unresolved E2/E3/C3 contracts clearly gated |
| C5.2 | Transfer AR and rolling implementations with compatibility wrapper | AT-1–AT-4/AT-6/AT-7; independent analytic/property cases; frozen core-v1 numbers to 1e-10 |
| C5.3 | Transfer episode, surrogate and test code without changing draw order | AT-5/AT-13–AT-16 evidence; original attempt accounting and full RNG-state agreement; frozen H1 reproduction |
| C5.4 | Transfer square-root filter; implement only frozen E3 specification | AT-11, analytic state-space fixtures, E3 output comparison |
| C5.5 | Expose only selected C3 tests; extract Schur recursion with numerical safeguards | Reduced-R C3 size table within prescribed Monte Carlo uncertainty; AT-8 and exact edge cases |
| C5.6 | Build docs and one runnable worked example per module | All public examples execute; documentation site build |
| C5.7 | Release against the full plan checklist | Three supported Python versions; >=90% core coverage; clean install; citation, licence, version and archive DOI verified |

Use small deterministic and artificial checks in routine development. Reuse stored registered evidence for scientific acceptance. An expensive recomputation needs an explicit reproducibility purpose and a new labelled output directory. Do not modify the running validation environment to install package test tools. A fast implementation that changes RNG order cannot claim bitwise reproduction: retain the reference and report the separately evaluated Monte Carlo comparison required by the plan.

The plan specifies MIT for the eventual code release and CC BY 4.0 for the registration snapshot; neither grants permission to relicense third-party data. Keep SILSO's separate attribution and licence requirements. Resolve the existing package README's undecided licensing statement through an explicit release decision rather than silently changing it in this design delivery.

## 7. Review and open decisions

The source map is complete for current AR(2)/H1/foundations components. The following remain acceptance dependencies: core-v1 does not yet exist; E2 and E3 contracts require their registered designs; C3.TEST may select a different method or no valid method; arbitrary AR order and root tracking need separately validated implementations. C5.1 is delivered as a reviewable candidate, not as proof of M6 completion. No empirical results, programme gates, package versions or public repositories are changed by this document.
