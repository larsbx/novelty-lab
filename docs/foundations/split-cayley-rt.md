# Split Cayley RT foundations: scope, proofs and falsifiers

**Research state:** a narrowed classical-foundation contract; **no new theorem promoted**, no existing N1–N5 status changed.  
**Gate:** [bounded literature audit](../literature/split-cayley-rt-foundations-2026-10-24.md).  
**Executable:** [exact quadratic kernel](../../experiments/rt/independent_reference.py) and [negative-control tests](../../tests/test_rt_foundations.py).

This file is an **audit dossier**, not an independent proof review or a novelty claim. It separates elementary calculations, established imported theorems, disproved formulations and open extensions.

## 1. Algebraic foundation

For a field \(F\) with \(\operatorname{char}F\ne2\), let \(V\) be a finite-dimensional vector space and \(N:V\to F\) a quadratic form (homogeneous of degree two **and** with bilinear polarization)
\[
B_2(x,y)=N(x+y)-N(x)-N(y).
\]
The affine quadrance is \(Q(x,y)=N(y-x)\). For **non-null** vectors \(N(x)N(y)\ne0\), projective spread on rays is
\[
s([x],[y])=1-\frac{B_2(x,y)^2}{4N(x)N(y)}.
\]
**Equivalent polynomial certificate on the guard:** \(4N(x)N(y)(1-s)=B_2(x,y)^2\). Clearing denominators without retaining the guard is not logically equivalent.

The independent Python reference model is \(F=\mathbb F_p\) (odd prime), \(V=F^8\),
\[
N(x)=2\sum_{i=0}^{3}x_i x_{i+4}.
\]
In the basis \(e_i,f_i\), this yields \(N(e_i)=N(f_i)=0\) and \(B_2(e_i,f_j)=2\delta_{ij}\). Thus this model is split, Witt index four. It is *only quadratic-space code*, separate from the repository's existing pinned N2 `cayley-dickson/v1` multiplication model.

**Well-definedness:** when \(x'=\lambda x\), \(y'=\mu y\), \(\lambda,\mu\in F^\times\), polarization and homogeneity scale the numerator and denominator by the same \(\lambda^2\mu^2\). Hence spread is independent of ray representatives.

**Caution:** a finite field has no compatible order. A threshold like \(s\le\epsilon\) is not part of this kernel; finite-field acceptance families must be supplied as nested predicates/sets with their own provenance.

## 2. A complete algebraic transport argument (classical construction)

For \(N(a)\ne0\) define the reflection
\[
r_a(x)=x-\frac{B_2(x,a)}{N(a)}a.
\]
Set \(t=B_2(x,a)/N(a)\). The polarization formula gives
\[
N(x-ta)=N(x)+t^2N(a)-tB_2(x,a)=N(x).
\]
The reflector is linear, maps \(a\) to \(-a\), and fixes \(a^\perp\).

**Two-reflection norm-shell transport (written proof, pending independent review):** Given \(N(u)=N(v)=c\ne0\), if \(N(u-v)\ne0\) then
\[
r_{u-v}(u)=v
\]
because \(B_2(u,u-v)=N(u-v)\). Otherwise the parallelogram identity shows
\[
N(u+v)+N(u-v)=4c\implies N(u+v)=4c\ne0.
\]
Then \(r_{u+v}(u)=-v\) and \(r_v(-v)=v\). Thus \(r_v\circ r_{u+v}\) transports \(u\) to \(v\) using only non-null normals. This argument needs **no search**, generic-point selection, or field ordering. It also works for non-split nondegenerate forms whenever the two nonzero-norm vectors exist.

The implementation returns the ordered sequence of normals and rejects null or mismatched norm shells. The conformance test replays the transport **over every vector of norm one in \(\mathbb F_3^8\)**. This exact finite check is independent evidence of implementation behavior, not a proof of the field-generic statement.

## 3. Essential negative control: triple spread requires planarity

The familiar polynomial
\[
(s_1+s_2+s_3)^2=2(s_1^2+s_2^2+s_3^2)+4s_1s_2s_3
\]
must not be asserted for arbitrary triples of directions in \(F^8\). Its planar use has an explicit rank-two hypothesis (directions contained in a two-dimensional vector subspace; all denominators nonzero).

For three mutually orthogonal, non-null rays, the spreads are \((1,1,1)\). The left side evaluates to \(9\) and the right to \(10\); the identity fails over **every** field, including odd finite fields. The tests check a planar instance and this non-planar counterexample over \(\mathbb F_3\), \(\mathbb F_5\), and \(\mathbb F_7\).

## 4. Cayley layer: do not reuse an unverified Zorn table

The previous circulated Zorn product with **the same positive cross-product sign in both off-diagonal slots** contradicts norm composition. With standard \(e_i\in F^3\), set
\[
x=(0,e_1;e_2,0),\quad y=(0,e_2;e_1,0).
\]
Their norms are zero; that old table gives \(xy=(1,-e_3;e_3,1)\), whose norm is \(2\ne0\). Thus it cannot be used as a composition algebra in odd characteristic.

A consistent product convention uses an **opposite sign** on one of the cross terms; its identities must be validated as a separate contract in the existing N2 model before any theorem-facing table is adopted. This branch does **not** create a competing octonion multiplication implementation.

## 5. Classical results and invalid derivations

| Item | Current treatment | Reason |
|---|---|---|
| Quadratic polarization, guarded spread, reflection | Elementary algebraic calculations; executable conformance | Definitions plus direct identities |
| Two-reflection transport | Written proof; pending independent review | All inverses guarded, explicit case split |
| Moufang identities | **Imported** from alternative-algebra theory | Earlier in-thread associator push lemma was false |
| Artin's two-generator associativity | **Imported** | Alternating trilinearity alone does not reduce associators of arbitrary words |
| Every two generators span a nondegenerate quaternion 4-space | **Rejected as universal** | Degenerate/smaller subalgebras are possible |
| Triple spread on arbitrary 8D triples | **Refuted** | Orthogonal-triple counterexample |
| \(G_2\) stabilizer of compatible Cayley multiplication | Classical, imported, model/hypothesis-sensitive | Not deduced by RT alone |
| Aschbacher classification of tensor stabilizers | Classification framework, **not** automatic maximality | Exact class and normalizer require separate proof |
| Cubic/quartic projective ratios | Candidates | Scale-invariance does not itself give RT laws |
| Spread-controlled 2-complex | Separate candidate | Need exact attachment predicate, planar/ordered-field or finite acceptance semantics, and prior-art gate |

Any group-normalizer claim must distinguish linear/isometric from semilinear covariance: if \(g\) induces \(\sigma\in\mathrm{Aut}(F)\), projective spread generally satisfies \(s(gx,gy)=\sigma(s(x,y))\), not numerical equality in \(F\).

## 6. Proof, computation and novelty are separate

The suite checks selected concrete formulas and exhaustive finite shells. It **does not** certify a proof over all fields, complete Cayley multiplication, Artin/Moufang, performance of structured tensor weights, or mathematical novelty. A polynomial function can vanish at every point of a finite field without being the zero polynomial (\(X^p-X\) is the standard falsifier). Generic identities need symbolic coefficient proofs or exact imported theorems.

## 7. Next foundation work, without forcing a single interpretation

1. Verify and pin the canonical N2 multiplication convention; add sign-falsifier witnesses **using the existing shared primitive**, never a second multiplication table.
2. Replace the false associator push argument with a source-matched Moufang derivation; independently review the Artin induction and its exact hypotheses.
3. Treat planar RT identities as dimension-independent **rank-two-restricted** laws; investigate higher-dimensional Gram-minor relations separately.
4. Study projective Cayley–Klein reconstruction only on a domain accounting for tangent absolute intersections.
5. Define the semilinear action with Frobenius covariance before claiming invariant finite-field threshold sets.
6. Explore tensor stabilizers, Aschbacher families, and higher-degree forms as **candidate directions**, not consequences of the present RT proof.
7. Develop the spread-controlled 2-complex in a separate workstream: interpretation-neutral cells with explicit eligibility, and ordered-field vs finite-field acceptance policies.

No N2 manuscript, ledger record, generated data, vendor pin, or mathematical status is changed by this foundation branch.
