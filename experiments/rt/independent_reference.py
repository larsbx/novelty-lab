"""Independent Python RT oracle for differential conformance; no Cayley multiplication.

The norm is N(x) = 2 * sum(x[i] * x[i+4], i=0..3), giving a
hyperbolic 8-space with B2(e_i, f_j) = 2 delta_ij. This module is a
reference-only oracle for a classical contract, not a novelty or proof claim.
"""

def _prime_odd(p):
    if type(p) is not int or p < 3 or p % 2 == 0:
        return False
    i = 3
    while i * i <= p:
        if p % i == 0:
            return False
        i += 2
    return True


class SplitQuadratic8:
    """Finite-field quadratic geometry with total norms and guarded ratios."""

    def __init__(self, p):
        if not _prime_odd(p):
            raise ValueError("base field must be an odd prime field")
        self.p = p

    def vector(self, x):
        if len(x) != 8 or any(type(a) is not int for a in x):
            raise ValueError("expected eight integral field coordinates")
        return tuple(a % self.p for a in x)

    def add(self, x, y):
        x, y = self.vector(x), self.vector(y)
        return tuple((a + b) % self.p for a, b in zip(x, y))

    def sub(self, x, y):
        x, y = self.vector(x), self.vector(y)
        return tuple((a - b) % self.p for a, b in zip(x, y))

    def scalar(self, a, x):
        if type(a) is not int:
            raise ValueError("scalar must be an integral field coordinate")
        x = self.vector(x)
        return tuple((a * b) % self.p for b in x)

    def norm(self, x):
        x = self.vector(x)
        return (2 * sum(x[i] * x[i + 4] for i in range(4))) % self.p

    def polar(self, x, y):
        # Explicit polarization; also matches 2 * mixed hyperbolic pairing.
        return (self.norm(self.add(x, y)) - self.norm(x) - self.norm(y)) % self.p

    def quadrance(self, x, y):
        return self.norm(self.sub(y, x))

    def spread(self, x, y):
        """A projective spread or None on the null locus (no field order)."""
        nx, ny = self.norm(x), self.norm(y)
        if nx == 0 or ny == 0:
            return None
        den = (4 * nx * ny) % self.p
        assert den != 0  # Guaranteed by primality and p != 2.
        return (1 - self.polar(x, y) ** 2 * pow(den, -1, self.p)) % self.p

    def reflection(self, x, a):
        """Apply the orthogonal reflection, refusing a null normal."""
        na = self.norm(a)
        if na == 0:
            raise ValueError("reflection normal is null")
        factor = (self.polar(x, a) * pow(na, -1, self.p)) % self.p
        return self.sub(x, self.scalar(factor, a))

    def transport_normals(self, x, v):
        """Normals for <=2 reflections sending x to v, when norms agree != 0.

        The first normal applies first. The exceptional null difference
        is handled deterministically by x+v followed by v; no search.
        """
        x, v = self.vector(x), self.vector(v)
        if self.norm(x) == 0 or self.norm(x) != self.norm(v):
            raise ValueError("norm shell must agree and be nonzero")
        delta = self.sub(x, v)
        if self.norm(delta) != 0:
            return (delta,)
        return (self.add(x, v), v)

    def transport(self, x, v):
        result = self.vector(x)
        for normal in self.transport_normals(x, v):
            result = self.reflection(result, normal)
        if result != self.vector(v):
            raise AssertionError("transport invariant violated")
        return result

    def canonical_norm_vector(self, a):
        a = a % self.p
        if a == 0:
            raise ValueError("canonical shell here requires nonzero norm")
        x = [0] * 8
        x[0] = 1
        x[4] = a * pow(2, -1, self.p) % self.p
        return tuple(x)


def triple_spread_defect(s1, s2, s3, p):
    """Polynomial defect; zero is expected ONLY for planar triples."""
    return ((s1 + s2 + s3) ** 2 - 2 * (s1 * s1 + s2 * s2 + s3 * s3)
            - 4 * s1 * s2 * s3) % p
