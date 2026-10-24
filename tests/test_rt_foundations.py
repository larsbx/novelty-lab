"""Exact RT foundations, guarded normalization, and planar counterexamples.

Checks the split hyperbolic norm, reflection transport and RT kernel by an
independent arithmetic replay. The 8D noncoplanar triple is a negative control.
"""

import itertools
import unittest

from kernel.rt_foundations import SplitQuadratic8, triple_spread_defect

GUARDS_CONTRACT = "Split Cayley RT quadratic-layer foundation: guards, reflections, planar triple-spread scope"


class TestRTFoundations(unittest.TestCase):
    def test_invalid_fields_and_vectors_fail_closed(self):
        for p in (0, 1, 2, 4, 9, 21):
            with self.assertRaises(ValueError):
                SplitQuadratic8(p)
        f = SplitQuadratic8(3)
        with self.assertRaises(ValueError):
            f.vector([0] * 7)
        with self.assertRaises(ValueError):
            f.vector([0] * 7 + [0.5])

    def test_polarization_and_spread_kernel(self):
        for p in (3, 5, 7):
            f = SplitQuadratic8(p)
            a = f.canonical_norm_vector(1)
            b = (0, 1, 0, 0, 0, pow(2, -1, p), 0, 0)
            self.assertEqual(f.norm(a), 1)
            self.assertEqual(f.norm(b), 1)
            self.assertEqual(f.polar(a, b), 0)
            self.assertEqual(f.spread(a, b), 1)
            self.assertEqual(f.spread(f.scalar(2, a), f.scalar(3, b)), 1 if p != 3 else None)
            # For p=3, scalar 3 gives a zero vector; its null guard fires.
            for x, y in ((a, b), (a, a), (a, f.add(a, b))):
                s = f.spread(x, y)
                if s is not None:
                    den = (4 * f.norm(x) * f.norm(y)) % p
                    self.assertEqual((den * (1 - s) - f.polar(x, y) ** 2) % p, 0)
            e = (1, 0, 0, 0, 0, 0, 0, 0)
            self.assertEqual(f.norm(e), 0)
            self.assertIsNone(f.spread(e, a))
            with self.assertRaises(ValueError):
                f.reflection(a, e)

    def test_triple_spread_requires_a_planar_span(self):
        for p in (3, 5, 7):
            f = SplitQuadratic8(p)
            x = f.canonical_norm_vector(1)
            y = (0, 1, 0, 0, 0, pow(2, -1, p), 0, 0)
            z = f.add(x, y)
            spreads = (f.spread(x, y), f.spread(y, z), f.spread(z, x))
            self.assertTrue(all(v is not None for v in spreads))
            self.assertEqual(triple_spread_defect(*spreads, p), 0)
            w = (0, 0, 1, 0, 0, 0, pow(2, -1, p), 0)
            all_right = (f.spread(x, y), f.spread(y, w), f.spread(w, x))
            self.assertEqual(all_right, (1, 1, 1))
            self.assertNotEqual(triple_spread_defect(*all_right, p), 0)

    def test_two_reflection_shell_transport_complete_over_f3(self):
        f = SplitQuadratic8(3)
        canonical = f.canonical_norm_vector(1)
        n_cases = 0
        n_fallback = 0
        for x in itertools.product(range(3), repeat=8):
            if f.norm(x) != 1:
                continue
            normals = f.transport_normals(x, canonical)
            self.assertTrue(1 <= len(normals) <= 2)
            self.assertTrue(all(f.norm(n) != 0 for n in normals))
            self.assertEqual(f.transport(x, canonical), canonical)
            n_fallback += (len(normals) == 2)
            n_cases += 1
        self.assertGreater(n_cases, 0)
        self.assertGreater(n_fallback, 0)
        with self.assertRaises(ValueError):
            f.transport((0,) * 8, canonical)


if __name__ == "__main__":
    unittest.main()
