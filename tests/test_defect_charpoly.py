import random
import unittest

from support import load

R = load("experiments/n2/rank_law.py", "rank_law_charpoly")
C = R.C
GUARDS_CLAIM = "DefectCharacteristicPolynomial"
GUARDS_CONTRACT = "QuaternionDoubling right-multiplication form of Delta on Q-perp in the cayley-dickson/v1 octonion model"


def rand(ell, rng):
    return tuple(rng.randrange(ell) for _ in range(C.DIM))


def sub(u, v, ell):
    return tuple((s - t) % ell for s, t in zip(u, v))


def polymul(a, b, ell):
    out = [0] * (len(a) + len(b) - 1)
    for i, s in enumerate(a):
        for j, t in enumerate(b):
            out[i + j] = (out[i + j] + s * t) % ell
    return tuple(out)


def predicted(nu, nc, ell):
    """(Y - nu)^4 (Y^2 - (2 nu - N(c)) Y + nu^2)^2, coefficients low -> high."""
    out = (1,)
    for f in [((-nu) % ell, 1)] * 4 + [(nu * nu % ell, (nc - 2 * nu) % ell, 1)] * 2:
        out = polymul(out, f, ell)
    return out


def pairs(ell, rng, count):
    """Random pairs, a fifth of them with y = a + b x so that dim Q <= 2 is covered."""
    for i in range(count):
        x, y = rand(ell, rng), rand(ell, rng)
        if i % 5 == 0:
            a, b = rng.randrange(ell), rng.randrange(1, ell)
            y = tuple((b * s + a * (k == 0)) % ell for k, s in enumerate(x))
        yield x, y


class TestCharpolyHelper(unittest.TestCase):
    def test_against_a_companion_matrix(self):
        ell = 7
        coeffs = (3, 0, 5, 1, 6, 2, 0, 4)                    # monic degree 8: c0 + c1 Y + ... + Y^8
        companion = [[0] * 8 for _ in range(8)]
        for i in range(1, 8):
            companion[i][i - 1] = 1
        for i in range(8):
            companion[i][7] = -coeffs[i] % ell
        self.assertEqual(C.charpoly(companion, ell), coeffs + (1,))


class TestGramIdentity(unittest.TestCase):
    def test_gram_determinant_is_squared_commutator_norm(self):
        """det Gram_B(1, x, y, xy) = N(xy - yx)^2 for all x, y."""
        for ell in (3, 5, 7, 11):
            rng = random.Random(ell)
            for x, y in pairs(ell, rng, 300):
                xy = C.mul(x, y, ell)
                q = [C.BASIS[0], x, y, xy]
                gram = C.echelon([[R.bilinear(u, v, ell) for v in q] for u in q], ell)[1]
                commutator = C.norm(sub(xy, C.mul(y, x, ell), ell), ell)
                self.assertEqual(gram, commutator * commutator % ell)


class TestCharacteristicPolynomial(unittest.TestCase):
    def test_polynomial_identity_on_all_strata(self):
        """det(Y - L_x L_y L_conj(xy)) = (Y - nu)^4 (Y^2 - (2 nu - N(c)) Y + nu^2)^2, nu = N(x)N(y), c = xy - yx."""
        for ell in (3, 5, 7, 11, 13):
            rng = random.Random(100 + ell)
            for x, y in pairs(ell, rng, 250):
                xy = C.mul(x, y, ell)
                m = C.matmul(C.matmul(C.left(x, ell), C.left(y, ell), ell), C.left(C.conj(xy, ell), ell), ell)
                nu = C.norm(x, ell) * C.norm(y, ell) % ell
                nc = C.norm(sub(xy, C.mul(y, x, ell), ell), ell)
                self.assertEqual(C.charpoly(m, ell), predicted(nu, nc, ell))

    def test_dim_three_pairs_over_f3(self):
        """The middle stratum, rare under random sampling, from the exhaustive projective enumeration over F_3."""
        ell, found = 3, 0
        points = R.projective_pure(ell)
        for i, x in enumerate(points):
            for y in points[i + 1:i + 40]:
                xy = C.mul(x, y, ell)
                if C.rank([C.BASIS[0], x, y, xy], ell) != 3:
                    continue
                found += 1
                self.assertEqual(C.norm(sub(xy, C.mul(y, x, ell), ell), ell), 0)
                if C.norm(x, ell) and C.norm(y, ell):
                    d, _ = C.defect(x, y, ell)
                    self.assertEqual(C.charpoly(d, ell), predicted(1, 0, ell))
        self.assertGreater(found, 50)


class TestRightMultiplicationForm(unittest.TestCase):
    def test_delta_on_q_perp_is_right_multiplication_by_g(self):
        """For nondegenerate Q and v in Q-perp with N(v) != 0: Delta(uv) = (u g) v, g = (xy)^-1 (yx)."""
        for ell in (3, 5, 7):
            rng, done = random.Random(ell), 0
            while done < 25:
                x, y = rand(ell, rng), rand(ell, rng)
                xy = C.mul(x, y, ell)
                q = [C.BASIS[0], x, y, xy]
                nu = C.norm(x, ell) * C.norm(y, ell) % ell
                if not nu or C.rank(q, ell) != 4 or not R.gram_nondegenerate(q, ell):
                    continue
                perp = R.orthogonal_complement(q, ell)
                v = next((w for w in perp if C.norm(w, ell)), None)
                if v is None:
                    continue
                done += 1
                g = tuple(t * pow(nu, -1, ell) % ell for t in C.mul(C.conj(xy, ell), C.mul(y, x, ell), ell))
                d, _ = C.defect(x, y, ell)
                for _ in range(4):
                    coeffs = [rng.randrange(ell) for _ in q]
                    u = tuple(sum(a * b[i] for a, b in zip(coeffs, q)) % ell for i in range(C.DIM))
                    uv = C.mul(u, v, ell)
                    self.assertEqual(C.apply(d, uv, ell), C.mul(C.mul(u, g, ell), v, ell))


if __name__ == "__main__":
    unittest.main()
