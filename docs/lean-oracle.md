# Lean oracle layer

The oracle independently replays the committed eight-dimensional model over
(mathbb F_3) from an explicit multiplication tensor.

## Executed checks

The CI job builds the Lean project and runs `lake exe oracle-selfcheck`.
The executable checks:

1. trial-division primality of 3;
2. tensor dimensions and the two-sided basis identity;
3. alternativity through antisymmetry of the trilinear associator on every
   basis triple;
4. norm composition through all diagonal and polarized cross coefficients of
   (L_x^T L_x=N(x)I), with (N(x)=sum_i x_i^2);
5. the nonflat pentagon witness ((e_0,e_1,e_2,e_4)), whose third and fifth
   edges are (e_7) and (-e_7);
6. the closed total pentagon boundary.

Python independently reconstructs the tensor by three scalar
Cayley–Dickson doublings. Its canonical SHA-256 digest is
`747ace028b8a34fb95f5b7c39e99f3004e39ad4fb3401a7caa3b6e3a4e2e2f4b`,
also recorded by the Lean model.

## Boundary

This is an executable finite certificate, not a kernel-level Lean proof that
the Boolean checker implies Mathlib's abstract composition-algebra classes.
That soundness theorem is the next formalization layer.
