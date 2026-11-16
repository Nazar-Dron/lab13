import math
import sys
import unittest
from pathlib import Path

import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from function_model import evaluate, sample, chord_deviation


class TestVariant8(unittest.TestCase):
    def test_formula_control_a(self):
        self.assertAlmostEqual(evaluate(3*math.pi/4), -5/math.sqrt(3*math.pi/2), places=12)

    def test_formula_control_b(self):
        self.assertAlmostEqual(evaluate(5*math.pi/4), -5/math.sqrt(5*math.pi/2), places=12)

    def test_formula_control_c(self):
        self.assertAlmostEqual(evaluate(7*math.pi/4), 5/math.sqrt(7*math.pi/2), places=12)

    def test_bounds(self):
        for n in (1201, 2401):
            x, y = sample(n)
            self.assertEqual(len(x), n)
            self.assertEqual(len(y), n)
            self.assertEqual(float(x[0]), 1.0)
            self.assertEqual(float(x[-1]), 7.0)
            self.assertTrue(np.isfinite(y).all())

    def test_no_gaps(self):
        x, y = sample()
        self.assertFalse(np.isnan(y).any())
        self.assertTrue((x > 0).all())

    def test_bad_n(self):
        for n in (2, 0, -4, 10.0, True, "2401"):
            with self.subTest(n=n), self.assertRaises(ValueError):
                sample(n)

    def test_bad_domain(self):
        for value in (0.0, -1.0, 7.0001, np.nan, np.inf, -np.inf, "слово"):
            with self.subTest(value=str(value)), self.assertRaises(ValueError):
                evaluate(value)

    def test_boundary_scalar(self):
        self.assertAlmostEqual(evaluate(1.0), 5*math.sin(10)*math.sin(3), places=12)
        self.assertAlmostEqual(evaluate(7.0), 5*math.sin(70)*math.sin(21)/math.sqrt(7), places=12)

    def test_vector_matches_scalar(self):
        values = [1.0, 2.2, 4.7, 7.0]
        expected = [evaluate(v) for v in values]
        np.testing.assert_allclose(evaluate(np.array(values)), expected, atol=1e-13)

    def test_array_unchanged(self):
        x = np.array([1.0, 3.0, 7.0]); original = x.copy()
        evaluate(x)
        np.testing.assert_array_equal(x, original)

    def test_fine_grid_lower_deviation(self):
        x1, y1 = sample(1201)
        x2, y2 = sample(2401)
        err1, err2 = chord_deviation(x1, y1), chord_deviation(x2, y2)
        self.assertGreater(err1, 0)
        self.assertLess(err2, err1)

    def test_chord_bad_shapes(self):
        with self.assertRaises(ValueError):
            chord_deviation([1, 2], [1])

    def test_chord_bad_order(self):
        with self.assertRaises(ValueError):
            chord_deviation([2, 1], [1, 2])

    def test_immutable_result_valid(self):
        x, y = sample(2401)
        self.assertEqual(np.isfinite(y).sum(), 2401)
        self.assertEqual(len(x), 2401)


if __name__ == "__main__":
    unittest.main(verbosity=2)
