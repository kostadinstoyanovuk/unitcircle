# AR(2) extraction checkpoint

Development checkpoint C5.2a, 28 September 2026. No scientific gate changes.

The installed development package passed 16 unittest checks, including direct
intercept-inclusive least squares, an independently solved Yule-Walker system,
analytic root cases, signed-zero compatibility, input/index handling and rolling
prefix/future-perturbation causality.

`ar-extraction-verification.json` records 14 exact estimator comparisons and
seven exact rolling-path comparisons against research commit
6f9400ea4aba29c3b515f6ab13659efcff572a3f. Coefficients, intercepts, residuals,
counts and all root diagnostics match exactly. Inputs are three artificial
fixtures and four intervals from already-acquired SILSO data, verified against
its existing manifest. No data files are added to this package.

The numerical reference files in src/unitcircle/_reference are byte-identical
to their source checkout. They are kept together so rolling imports the same
preserved estimator. Public wrappers add order validation and copied residual
labels; estimator arithmetic is unchanged. A legacy docstring was corrected
to describe signed-zero tie ordering; that algorithm is unchanged.

Repeat the transfer verification with:

```text
python tools/verify_ar_extraction.py --reference PATH_TO_RESEARCH_CHECKOUT --output evidence/ar-extraction-verification.json
```

Use an unchanged checkout at the recorded source commit. The command reads only
reference source, its data manifest and the two specified SILSO files. It does
not execute any registered experiment or acquire UK observations.

Core-v1 comparisons, broader-order support, remaining module extraction,
release licensing and M6 acceptance remain pending. This checkpoint is local;
no hosted-check or public-release result is claimed.
