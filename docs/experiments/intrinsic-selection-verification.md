# Intrinsic selection: replacement compatibility gate

**Status:** experimental result; exact finite artifact, no novel theorem or intrinsic selection promoted.

## Result and scope

For packing dimension 6 over F7, all eight distinct transported basis-defect
operators at the bridge Phi=I+J were checked. Identity passes. The seven
nonidentity operators fail both row-permutation quotient descent and the
replacement neighbor identity. Thus this tested defect subgroup cannot act
as a group of automorphisms of the declared unlabeled replacement graph.
This does not exclude all other bridge placements, or defect observables
that are decorations rather than graph automorphisms.

## Exact global test, not vertex sampling

Let Q=I+J, Sigma the row-permutation group, and S the eight replacement
matrices. A candidate B must satisfy B^T Q B=Q. Configurations W are
invertible and satisfy W^T Q W=R, for a specified nonempty fiber.

For W and P W to have equivalent images, B P W must equal P' B W for a
permutation P'. Cancel W: B P B^-1 must be a permutation matrix. Checking
the seven adjacent transpositions suffices: they generate Sigma, and finite
conjugation sends Sigma into itself only if it normalizes Sigma. This is
necessary and sufficient for the left-linear action to descend.

Replacement adjacency requires equality, with multiplicities, of the
row-permutation classes of B S_i W and S_j B W. Cancellation of invertible
W reduces this to equality of the multisets of classes of B S_i and S_j B.
The implementation compares sorted-row matrix keys and exact integer
multiplicities. With quotient descent, this identity is necessary and
sufficient for a bijective multigraph automorphism on the full fiber.

These are elementary proof outlines for reducing the global property to
matrix identities. They are not independently reviewed abstract theorems
or Lean proofs. Executable certificates recompute every identity over F7.

## Intrinsic uniqueness remains open

The candidate domain here is the explicit basis-defect list at one bridge,
not every admissible embedding and not the full graph automorphism group.
The identity survivor is not a selected octonionic placement.

To establish intrinsic selection, first define the placement equivalence
and a complete admissible domain. Then prove that the predicate is invariant
under all symmetries of the declared packing structure and that its survivor
set is a singleton. A fixed point under all symmetries is necessary for an
individual intrinsic choice, but does not by itself establish uniqueness.
Preservation of a canonical relational refinement follows from graph
preservation and is not an independent uniqueness test.

## Replay and controls

Run `python -m experiments.soddy.intrinsic_selection` for the deterministic
certificate census, and `python -m unittest tests/test_intrinsic_selection.py -v`.
Positive controls: identity, adjacent row permutations, scalar negation.
Negative controls: every nonidentity basis defect, modified certificates,
altered matrix entries, and changed multiplicities. Quotient failures are
replayed directly using equivalent inputs with inequivalent outputs.

The repository verification workflow discovers these tests; the existing
Lean oracle workflow is also required. A passing Lean workflow does not
certify this new oracle: Lean proofs of the reduction, matrix identities,
and intrinsic uniqueness remain pending.
