# Pure mathematics — quadratic, projective and tensor invariants

**Discipline:** algebra, rational trigonometry, finite geometry, multilinear algebra, finite groups.  
**Status:** a mixture of known theorems, elementary derived identities, and separate open candidates. Mathematical claims are not graded by how much application software has been tested.

## Questions and subjects

- Quadratic form \(Q\) and bilinear polarization \(B_2\), with odd characteristic; guarded projective spread \(1-B_2(x,y)^2/(4Q(x)Q(y))\).
- Gram determinants, exterior minors and actual span rank, finite-field orthogonal/similitude/semilinear group actions.
- Split Cayley composition algebras (including consistent multiplication signs); alternativity, Moufang, Artin, triality and automorphism stabilizers.
- Grassmannian and tensor orbit invariants: **trace cross/spread and det-cross already occur in Wildberger**, so they are prior art; full characteristic-polynomial packages may provide additional invariants without automatically classifying every orbit.
- Possible Clifford, Jordan, Freudenthal and higher-degree tensor directions are *independent candidates* and need field/hypothesis-specific definitions.

## What constitutes mathematical evidence

A theorem requires an unambiguous claim with quantified hypotheses and a proof, or a cited theorem whose hypotheses have been checked against the new use. A machine-checked formalization can strengthen confidence but is not mandatory for every mathematical statement; exact finite tests are excellent counterexample/regression evidence yet do **not** establish a field-generic polynomial identity. Symbolic coefficient identities are different from testing polynomial functions on every element of one finite field.

The elementary guarded three-ray defect
\[
(ABC)^2 T = D(4uvw-D)
\]
is an algebraic consequence of the Gram determinant definition and has an upstream [written derivation](https://github.com/larsbx/finite-math-kernels/blob/main/docs/theorems/three-ray-gram-defect.md) plus exact kernels. A nonplanar triple can have \(T=0\), so the defect is **not** a planarity predicate; exterior minors decide rank. The planar triple-spread theorem is classical and retains its rank-two restriction. Distinguish an algebraic proof from verified compilation of the corresponding software and from a novelty determination.

## Out of scope

No claim here concerns stochastic route distributions, optimizer semantics, software deployment, inference accuracy, or LLM training. Those subjects may *use* a mathematically well-defined invariant without needing to settle every classification question in finite-group or exceptional-algebra theory.

**Sources:** [quadratic RT dossier](../../foundations/split-cayley-rt.md); [cross-disciplinary source map](../rt-tensor-route-auditing-context-2026-10-28.md); [upstream Gram contract](https://github.com/larsbx/finite-math-kernels/blob/main/docs/theorems/gram-minor-rt-contract.md).
