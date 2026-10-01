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
