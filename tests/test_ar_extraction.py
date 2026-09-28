"""Independent acceptance checks for the extracted AR(2) public API."""

import unittest

import numpy as np
import pandas as pd

from unitcircle import roots as legacy_roots
from unitcircle.ar import (
    fit_ols,
    fit_yw,
    half_life,
    in_triangle,
    modulus,
    period,
    roots,
    spectral_peak,
)
from unitcircle.rolling import max_modulus


class ARFitReferenceChecks(unittest.TestCase):
    def setUp(self):
        # Fixed, non-generated observations keep these estimator checks
        # reproducible and independent of an assumed AR data-generating model.
        self.x = np.array(
            [1.2, -0.7, 0.4, 1.1, -1.3, 0.2, 0.9, -0.4, 1.5, -0.8, 0.3],
            dtype=float,
        )

    def test_ols_matches_independent_intercept_inclusive_least_squares(self):
        design = np.column_stack(
            (np.ones(len(self.x) - 2), self.x[1:-1], self.x[:-2])
        )
        expected, _, rank, _ = np.linalg.lstsq(design, self.x[2:], rcond=None)
        self.assertEqual(rank, 3)

        result = fit_ols(self.x, p=2)

        np.testing.assert_allclose(
            [result.intercept, *result.coefficients], expected, rtol=1e-12, atol=1e-12
        )
        expected_residuals = self.x[2:] - design @ expected
        np.testing.assert_allclose(result.residuals, expected_residuals, atol=1e-12)
        self.assertIsInstance(result.residuals, tuple)

    def test_yule_walker_matches_independent_toeplitz_solve(self):
        centered = self.x - self.x.mean()
        denominator = centered @ centered
        r1 = centered[1:] @ centered[:-1] / denominator
        r2 = centered[2:] @ centered[:-2] / denominator
        expected_phi = np.linalg.solve(
            np.array([[1.0, r1], [r1, 1.0]]), np.array([r1, r2])
        )
        expected_intercept = self.x.mean() * (1 - expected_phi.sum())

        result = fit_yw(self.x, p=2)

        np.testing.assert_allclose(result.coefficients, expected_phi, rtol=1e-12, atol=1e-12)
        self.assertAlmostEqual(result.intercept, expected_intercept, places=12)
        expected_residuals = (
            self.x[2:]
            - expected_intercept
            - expected_phi[0] * self.x[1:-1]
            - expected_phi[1] * self.x[:-2]
        )
        np.testing.assert_allclose(result.residuals, expected_residuals, atol=1e-12)


class AnalyticDiagnosticChecks(unittest.TestCase):
    def test_roots_modulus_period_and_half_life_on_known_coefficients(self):
        real = roots((0.3, 0.1))
        np.testing.assert_allclose(real, (0.5, -0.2), atol=1e-14)
        self.assertAlmostEqual(modulus((0.3, 0.1)), 0.5, places=14)
        self.assertIsNone(period((0.3, 0.1)))
        self.assertAlmostEqual(half_life((0.3, 0.1)), np.log(2) / -np.log(0.5))

        oscillatory = roots((0.0, -0.25))
        np.testing.assert_allclose(oscillatory, (0.5j, -0.5j), atol=1e-14)
        self.assertAlmostEqual(modulus((0.0, -0.25)), 0.5)
        self.assertAlmostEqual(period((0.0, -0.25)), 4.0)
        self.assertAlmostEqual(half_life((0.0, -0.25)), 1.0)

        self.assertEqual(roots((0.0, 0.0)), (0j, 0j))
        self.assertEqual(half_life((0.0, 0.0)), 0.0)
        self.assertIsNone(half_life((0.0, -1.0)))

    def test_signed_zero_real_root_order_matches_legacy_entry_point(self):
        expected = legacy_roots(-0.0, 0.25)
        self.assertEqual(expected, (-0.5 + 0j, 0.5 + 0j))
        self.assertEqual(roots((-0.0, 0.25)), expected)

    def test_stability_boundaries_and_spectrum_peak_classification(self):
        self.assertTrue(in_triangle(0.3, 0.1))
        self.assertFalse(in_triangle(1.0, 0.0))
        self.assertFalse(in_triangle(0.0, -1.0))

        peak = spectral_peak(0.1, -0.8)
        self.assertIsNotNone(peak)
        self.assertTrue(peak.has_interior_peak)
        self.assertAlmostEqual(
            peak.frequency,
            np.arccos(0.1 * (-0.8 - 1) / (4 * -0.8)),
            places=12,
        )
        no_peak = spectral_peak(0.3, 0.1)
        self.assertFalse(no_peak.has_interior_peak)
        self.assertIsNone(no_peak.frequency)
        complex_without_peak = spectral_peak(1.0, -0.3)
        self.assertFalse(complex_without_peak.has_interior_peak)
        self.assertIsNone(complex_without_peak.frequency)
        self.assertIsNone(spectral_peak(1.0, 0.0))

    def test_legacy_top_level_roots_entry_point_remains_available(self):
        np.testing.assert_allclose(legacy_roots(0.3, 0.1), (0.5, -0.2), atol=1e-14)


class InputAndIndexChecks(unittest.TestCase):
    def setUp(self):
        self.x = np.array([1.2, -0.7, 0.4, 1.1, -1.3, 0.2, 0.9, -0.4, 1.5, -0.8, 0.3])

    def test_nonfinite_observations_are_rejected(self):
        for bad in (np.nan, np.inf, -np.inf):
            values = self.x.copy()
            values[4] = bad
            with self.subTest(value=bad):
                with self.assertRaises(ValueError):
                    fit_ols(values, p=2)
                with self.assertRaises(ValueError):
                    fit_yw(values, p=2)
                with self.assertRaises(ValueError):
                    max_modulus(values, window=6, p=2)

    def test_rank_deficient_ols_is_rejected(self):
        alternating = np.array([-1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0])
        with self.assertRaises(ValueError):
            fit_ols(alternating, p=2)

    def test_only_ar2_order_is_supported_and_p_is_validated(self):
        for function, args, kwargs in (
            (fit_ols, (self.x,), {}),
            (fit_yw, (self.x,), {}),
            (max_modulus, (self.x,), {"window": 6}),
        ):
            with self.subTest(function=function.__name__):
                with self.assertRaises(NotImplementedError):
                    function(*args, p=1, **kwargs)
                for invalid in (True, False, 0, -2, 2.0, "2"):
                    with self.subTest(p=invalid):
                        with self.assertRaises(ValueError):
                            function(*args, p=invalid, **kwargs)

    def test_time_indexes_must_be_ordered_unique_and_consecutive(self):
        valid = pd.period_range("2000Q1", periods=len(self.x), freq="Q")
        self.assertEqual(len(fit_ols(pd.Series(self.x, index=valid)).residuals), len(self.x) - 2)
        self.assertEqual(len(max_modulus(pd.Series(self.x, index=valid), window=6).dropna()), len(self.x) - 5)

        invalid_indexes = (
            valid[::-1],
            valid.delete(4).insert(4, valid[3]),
            valid.delete(4),
        )
        for index in invalid_indexes:
            values = self.x if len(index) == len(self.x) else self.x[:-1]
            series = pd.Series(values, index=index)
            with self.subTest(index=index):
                with self.assertRaises(ValueError):
                    fit_ols(series, p=2)
                with self.assertRaises(ValueError):
                    max_modulus(series, window=5, p=2)

    def test_fit_copies_residual_index_and_returns_fresh_residual_series(self):
        index = pd.period_range("2004-01-01", periods=len(self.x), freq="M")
        values = pd.Series(self.x, index=index, name="observed")
        result = fit_ols(values, p=2)

        self.assertIsInstance(result.residual_index, pd.Index)
        self.assertTrue(result.residual_index.equals(index[2:]))
        self.assertIsNot(result.residual_index, values.index)
        first = result.residual_series
        second = result.residual_series
        self.assertIsInstance(first, pd.Series)
        self.assertIsNot(first, second)
        self.assertTrue(first.index.equals(index[2:]))
        self.assertEqual(len(first), len(result.residuals))
        first.iloc[0] = 12345.0
        self.assertNotEqual(result.residual_series.iloc[0], 12345.0)


class RollingCausalityChecks(unittest.TestCase):
    def test_short_input_is_all_warmup_and_singular_fit_reports_endpoint(self):
        short = pd.Series(
            [0.3, -0.2, 0.7, 1.1],
            index=pd.period_range("2012Q1", periods=4, freq="Q"),
        )
        warmup = max_modulus(short, window=5, p=2)
        self.assertTrue(warmup.isna().all())
        self.assertTrue(warmup.index.equals(short.index))

        singular = pd.Series(
            [-1.0, 1.0, -1.0, 1.0, -1.0],
            index=pd.period_range("2012Q1", periods=5, freq="Q"),
        )
        with self.assertRaisesRegex(ValueError, r"position 4.*label"):
            max_modulus(singular, window=5, p=2)

    def test_prefix_and_future_perturbations_do_not_change_past_modulus(self):
        values = pd.Series(
            [0.7, -0.1, 1.2, 0.3, -0.8, 0.4, 1.1, -0.5, 0.2, 0.9,
             -0.3, 1.4, -0.6, 0.5, 0.1, -1.0, 0.8, 0.6, -0.2, 1.3],
            index=pd.period_range("2010Q1", periods=20, freq="Q"),
        )
        cut, window = 13, 6

        prefix_path = max_modulus(values.iloc[:cut], window=window, p=2)
        full_path = max_modulus(values, window=window, p=2).iloc[:cut]
        perturbed = values.copy()
        perturbed.iloc[cut:] = [100.0, -90.0, 80.0, -70.0, 60.0, -50.0, 40.0]
        perturbed_path = max_modulus(perturbed, window=window, p=2).iloc[:cut]

        pd.testing.assert_series_equal(prefix_path, full_path)
        pd.testing.assert_series_equal(prefix_path, perturbed_path)


if __name__ == "__main__":
    unittest.main()
