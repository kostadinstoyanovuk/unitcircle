"""Installed-package smoke checks with independent algebraic expectations."""

import unittest

from unitcircle import roots


class RootSmokeTest(unittest.TestCase):
    def test_required_companion_roots(self):
        actual = roots(0.3, 0.1)
        for value, expected in zip(actual, (0.5, -0.2), strict=True):
            self.assertAlmostEqual(value, expected, places=14)
            self.assertAlmostEqual(value**2 - 0.3 * value - 0.1, 0, places=14)

    def test_complex_and_degenerate_cases(self):
        self.assertEqual(roots(0, -1), (1j, -1j))
        self.assertEqual(roots(0, 0), (0j, 0j))

    def test_nonfinite_rejected(self):
        for bad in (float("nan"), float("inf"), -float("inf")):
            with self.assertRaises(ValueError):
                roots(bad, 0)


if __name__ == "__main__":
    unittest.main()
