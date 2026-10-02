import random
import unittest

from support import load

R = load("experiments/n2/rank_law.py", "rank_law_class")
C = R.C
GUARDS_CLAIM = "DefectClassIsClassical"


def rand(ell, rng):
    return tuple(rng.randrange(ell) for _ in range(C.DIM))


def gram_det(vectors, ell):
    return C.echelon([[R.bilinear(u, v, ell) for v in vectors] for u in vectors], ell)[1]


def commutator_norm(x, y, ell):
    return C.norm(tuple((a - b) % ell for a, b in zip(C.mul(x, y, ell), C.mul(y, x, ell))), ell)


class TestCommutatorNormIsGramData(unittest.TestCase):
    def test_twice_commutator_norm_is_gram_determinant_of_one_x_y(self):
        """2 N(xy - yx) = det Gram_B(1, x, y): tau is a function of the Gram matrix of (1, x, y)."""
        for ell in (3, 5, 7, 11, 13):
            rng = random.Random(ell)
            for _ in range(400):
                x, y = rand(ell, rng), rand(ell, rng)
                self.assertEqual(2 * commutator_norm(x, y, ell) % ell, gram_det([C.BASIS[0], x, y], ell))


class TestSemisimplicity(unittest.TestCase):
    def test_delta_is_annihilated_by_the_split_quadratic_for_tau_not_two(self):
        """For tau != +-2, (Delta - I)(Delta^2 - tau Delta + I) = 0, so Delta is semisimple and its
        similarity class is fixed by its characteristic polynomial."""
        for ell in (5, 7, 11, 13):
            rng, checked = random.Random(ell), 0
            while checked < 60:
                x, y = rand(ell, rng), rand(ell, rng)
                nu = C.norm(x, ell) * C.norm(y, ell) % ell
                if not nu:
                    continue
                tau = (2 - commutator_norm(x, y, ell) * pow(nu, -1, ell)) % ell
                if tau in (2, ell - 2):
                    continue
                checked += 1
                d, _ = C.defect(x, y, ell)
                n = C.DIM
                eye = [[int(i == j) for j in range(n)] for i in range(n)]
                d2 = C.matmul(d, d, ell)
                quad = [[(d2[i][j] - tau * d[i][j] + eye[i][j]) % ell for j in range(n)] for i in range(n)]
                lin = [[(d[i][j] - eye[i][j]) % ell for j in range(n)] for i in range(n)]
                self.assertFalse(any(any(r) for r in C.matmul(lin, quad, ell)))


if __name__ == "__main__":
    unittest.main()
