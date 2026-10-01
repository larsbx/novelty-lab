# Lean oracle layer

The oracle is deliberately independent of the Python Cayley–Dickson
implementation.

## Inputs encoded in Lean

- modulus (p=3);
- an explicit (8\times8\times8) multiplication tensor;
- the basis quadruple ((e_0,e_1,e_2,e_4)).

## Checks

1. The tensor is dimensionally well formed.
2. (e_0) acts as a two-sided identity on all eight basis vectors.
3. The five pentagon edge terms are recomputed from the tensor.
4. The total boundary is zero.
5. The witness is nonflat: its third edge is (e_7) and its fifth edge is
   (-e_7).

The oracle proves neither that 3 is prime nor that an arbitrary submitted
tensor is a composition algebra. It independently establishes the exact
finite calculation for the committed tensor. Future certificate layers should
add primality, norm composition, alternativity, and tensor provenance checks.

## Self-check suite (`NoveltyLab/SelfCheck.lean`)

`lake exe oracle-selfcheck` prints every named check, and CI runs it after the
build. The suite contains:

- the scalar sanity case;
- the 𝔽₃ witness above, plus a check that each of its edges is the
  difference of the two parenthesizations it joins;
- the generated 𝔽₅ fixture (`NoveltyLab/Fixture.lean`, written by
  `experiments/n2/lean_fixture.py` from `experiments/n2/pentagon.py`).

The fixture holds a second 8×8×8 Cayley–Dickson tensor and three quadruples.
Two of them have all five edges nonzero. For each case the suite requires:

- the boundary closes;
- the edges equal the values Python computed;
- each edge equals its vertex difference;
- negating any nonzero edge breaks the boundary;
- in discriminating cases, moving the outer factor of [a,b,c]d or a[b,c,d]
  to the other side breaks the boundary.

Six mutations of `Oracle.lean` (edge signs, factor order, argument order,
a globally negated associator, a transposed tensor) were each confirmed to
fail the suite. See `docs/theorems/pentagon-boundary.md`.
