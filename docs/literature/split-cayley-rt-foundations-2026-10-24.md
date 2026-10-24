# Split Cayley / rational-trigonometry foundations — bounded literature gate (2026-10-24)

**Status:** literature gate only; no novelty or proof promotion.  
**Decision:** **proceed with a narrowed target**: exact split-quadratic-space RT contracts, their guarded polynomial equivalents, an explicit two-reflection transport routine, and negative controls for over-broad geometric assertions. Keep Cayley multiplication, Artin/Moufang, tensor generalizations and spread-controlled 2-complexes as separately gated research.

## 1. Proposed claim or experiment

For a split nondegenerate quadratic space \((V,N)\) of dimension eight over \(\mathbb F_p\), odd prime \(p\), implement the doubled polarization \(B_2\), affine quadrance \(Q(x,y)=N(y-x)\), guarded projective spread
\[
s([x],[y])=1-\frac{B_2(x,y)^2}{4N(x)N(y)}
\]
and an exact norm-shell transport from \(N(x)=N(v)=a\ne0\) using at most two non-null reflections. The triple-spread formula is **not** claimed for arbitrary triples in dimension eight: it requires an appropriate two-dimensional span. No float, ordering on \(\mathbb F_p\), or undefined inverse is admitted.

This work is a **contract/conformance foundation**, not a new RT theorem.

## 2. Sources (2026-10-24)

| Primary reference | Locator and access depth | What is used / boundary |
|---|---|---|
| R. D. Schafer, *An Introduction to Nonassociative Algebras* (1966) | Chapter III, **Alternative Algebras**, displayed Moufang identities (7)–(9), and **Theorem of Artin** (accessible book PDF/text). | Artin and Moufang are classical consequences of alternativity, not new results; proofs must use valid associator identities, not the false \([x,y,z]x=[x,y,zx]\). |
| T. A. Springer and F. D. Veldkamp, *Octonions, Jordan Algebras and Exceptional Groups* (2000) | **Composition Algebras**, pp. 1–23; **Automorphism Group**, pp. 25–36; **Triality**, pp. 37–67. Chapter ranges confirmed from publisher contents; no full chapter proof inspection claimed. | Distinguish split Cayley structure from underlying quadratic geometry; verify normalization and Zorn signs before borrowing multiplication tables. |
| N. J. Wildberger, *Rational Trigonometry in Higher Dimensions and a Diagonal Rule* (KoG 21, 2017) | Theorem 4 (**Cross law**) and Theorem 5 (**Triple spread formula**) identifiable from indexed article excerpt; full-page verification pending. | The cited triple spread relation is for a planar triangle. Its unrestricted extension to three independent rays in dimension eight is false. |
| P. B. Kleidman and M. W. Liebeck, *The Subgroup Structure of the Finite Classical Groups* (1990) | Preface and Chapter 1 discussion of Aschbacher's geometrically defined subgroups; publisher preview inspected, not a complete maximal-subgroup proof. | Aschbacher classes classify structural subgroup possibilities; a tensor stabilizer is not automatically maximal or in any asserted class. |

Accessible reference locators (not evidence of a complete literature search):
- https://www.math.uci.edu/~brusso/Schaferbook.pdf
- https://doi.org/10.1007/978-3-662-12622-6
- https://master.grad.hr/hdgg/kog_stranica/kog21/KoG21.pdf
- https://doi.org/10.1017/CBO9780511629235

## 3. Terminology

*Quadratic* requires both homogeneity and bilinearity of polarization. *Split* means Witt index four, not merely isotropic. *Ray* is a one-dimensional subspace; subtraction is defined on affine vectors, **not** on projective rays. *Spread* is a guarded rational invariant. *Finite-domain checking* is not equivalent to proving a formal polynomial identity over all fields. *Cayley algebra* is an 8D unital composition algebra; the legacy N2 census uses its own pinned `cayley-dickson/v1` convention.

## 4. Hypothesis and model boundaries

- Field: \(\mathbb F_p\), prime \(p\ge3\) in the executable contract; generic written statements use \(\operatorname{char}F\ne2\).
- Model: \(V=\mathbb F_p^8\) with \(N(x)=2\sum_{i=0}^3x_i x_{i+4}\); this **quadratic RT** model does not replace the canonical N2 multiplication model.
- Reflection \(r_a(x)=x-B_2(x,a)N(a)^{-1}a\) only if \(N(a)\ne0\).
- The RT 2-plane restriction is essential for triple spread. A null vector need not be zero.
- For semilinear \(g\), spread is generally **Frobenius covariant** \(s(gx,gy)=\sigma(s(x,y))\), not fixed as an element of the field.
- Characteristic three causes special polarization issues for cubic forms; quartic candidate invariants cannot be assumed separation metrics.
- Existing octonionic N2 ledger and paper claims are **not** changed or promoted in this gate.

## 5. Negative controls / falsifiers

1. **Non-coplanar triple:** three pairwise orthogonal non-null directions have spreads \(1,1,1\), violating the putative unrestricted triple spread polynomial (values 9 vs 10).
2. **Null spread guard:** nonzero \(x\) with \(N(x)=0\) yields no projective spread with \(x\) as a denominator.
3. **Same norm, null difference:** the one-reflection formula using \(x-v\) is undefined; the two-reflection fallback must use \(x+v\) and \(v\).
4. **Finite-domain vs polynomial:** \(t^p-t\) vanishes at every \(t\in\mathbb F_p\) but is not the zero polynomial.
5. **Cayley-model normalization:** any Zorn table must independently satisfy composition and alternativity; do not import the previously circulated same-sign cross-term table.
6. **Cross-ratio tangencies:** the unmodified two-distinct-absolute-points cross-ratio need not exist when the spanned projective line is tangent to the absolute, even if both input directions are non-null.

## 6. Decision

**Proceed, narrowed** to an exact **quadratic RT foundation** and its counterexample suite. Derive proofs symbolically in the dossier, keep executable checks as implementation conformance only, and do not conflate these with original theorems. **Redirect** new Cayley multiplication tests to the pinned N2 algebra contract and a separate multiplication-sign audit. **Defer** cubic/quartic, Aschbacher, tensor-weight, and 2-complex novelty claims until their own exact definitions, counterexamples and nearest-prior-art gates exist.

This note is bounded to four sources; it is **not** a priority search, proof review, novelty finding, or verification of the cited sources' complete arguments.
