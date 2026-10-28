# RT-invariant tensor route auditing — cross-disciplinary literature context (2026-10-28)

**Status:** edited research-context survey, **not** an accepted proof, novel-result finding, or permission to certify real-model training.  
**Scope:** odd-characteristic finite quadratic spaces, spread-controlled route complexes, semilinear/tensor refinements, deterministic replay, homology-based leader selection, and possible training-dynamics consumers.  
**Provenance:** adapted from the 2026-10-28 Deep Research report *RT and Tensor Route-Auditing Literature Review*, cross-checked against this repository's dated literature gates. The original report is exploratory; statements and bibliography below have been tightened, with known incorrect or unsupported claims explicitly withheld. This is **not a complete priority search** or independent review of every cited proof.

## 1. Program and evidence boundary

The prospective interface is a finite quadratic space \((V,Q)\) over \(\mathbb F_q\), \(q\) odd. Write \(B_2(x,y)=Q(x+y)-Q(x)-Q(y)\). On non-null rays, define
\[
s([x],[y])=1-\frac{B_2(x,y)^2}{4Q(x)Q(y)}
=\frac{\det\begin{psmallmatrix}Q(x)&B_2(x,y)/2\\B_2(x,y)/2&Q(y)\end{psmallmatrix}}{Q(x)Q(y)}.
\]
This is a **rational invariant on the guarded locus**, not a distance or ordered angle. Its projective interpretation comes from a Cayley–Klein absolute quadric; tangent intersections require special handling. For a \(\sigma\)-semilinear similitude, the correct law is \(s(gx,gy)=\sigma(s(x,y))\); Boolean gates must be stable under the invoked field automorphisms. There is no order-compatible finite-field threshold.

Three independent research layers should not be collapsed:

1. **Established algebraic geometry:** quadratic/polar forms, Gram minors, split Cayley identities, and semilinear group actions.
2. **Exact finite route semantics:** a specified finite update vocabulary, actual prefix states, equality of whole-vector swapped endpoints, signed incidence and replay-certified cells. This repository already has bounded P3–P6 consumer experiments.
3. **Proposed applications:** probabilistic scheduling, optimizer equivalence, actual neural-network/LLM training verification, learned tensor restraints and their relationship to outcome quality. These require additional operational and abstraction theorems.

A finite-field conformance check is not automatically a symbolic identity over all fields: \(X^p-X\) is a standard counterexample. A certificate from an untrusted producer is not provenance without a separately trusted specification pin or authentication.

## 2. Quadratic RT, Cayley–Klein, and higher-frame invariants

**Nearest foundations:** Wildberger's higher-dimensional rational trigonometry and the older Cayley–Klein projective absolute, alongside standard quadratic-form/Witt theory [R1–R3]. Spread is best calculated as a \(2\times2\) Gram determinant rather than by constructing quadratic splitting fields or evaluating cross-ratios. In projective reconstruction, two distinct absolute intersections are required by the ordinary cross-ratio definition; tangent and coincident degeneracies are not covered by the same formula.

**Essential falsifier:** the triple-spread polynomial is **planar**. Three pairwise orthogonal non-null directions have spreads \((1,1,1)\), making its claimed unrestricted 8D form false. The algebraic higher-rank defect candidate is
\[
\mathcal T=(s_1+s_2+s_3)^2-2\sum_i s_i^2-4s_1s_2s_3
=\frac{D(4uvw-D)}{A^2B^2C^2},
\]
where \(A=Q(x),B=Q(y),C=Q(z)\); \(u=B_2(x,y)/2,v=B_2(y,z)/2,w=B_2(z,x)/2\); and \(D\) is the corresponding \(3\times3\) Gram determinant. It follows by direct expansion, reduces to the planar law when \(D=0\), and is not promoted as a novel theorem without a closer prior-art search. Nonplanar configurations can also make \(\mathcal T=0\).

**Higher-frame direction:** Plücker/exterior-power geometry uses \(\det(X^\top M Y)\) for rank-\(k\) subspaces with guarded nondegenerate self-Gram matrices. The normalized determinant ratio is basis-independent, but is only one invariant and is **not** a complete subspace-orbit classifier. A richer guarded matrix invariant is the characteristic polynomial of \(G_U^{-1}G_{UW}G_W^{-1}G_{WU}\); even this needs stated group, field and orbit hypotheses before claiming completeness. Characteristic 3 and small-characteristic polarization also require separate care for cubic/quartic proposals.

**Bounded local authority:** [split Cayley RT foundation](../foundations/split-cayley-rt.md) and [Gram-minor contract upstream](https://github.com/larsbx/finite-math-kernels/blob/main/docs/theorems/gram-minor-rt-contract.md).

## 3. Composition algebras, triality and tensor stabilizers

**Nearest foundations:** Schafer and Springer–Veldkamp [R4–R5]. A split Cayley algebra is an eight-dimensional unital composition algebra; norm multiplicativity, alternative multiplication, Artin's two-generator associativity, Moufang identities, triality and \(G_2\) are classical subjects. The Zorn matrix convention with norm \(N(\alpha,a;b,\beta)=\alpha\beta-a\cdot b\) requires **opposite signs on the two cross-product terms**. The earlier same-positive-sign formula fails composition. This repository distinguishes its pinned Cayley–Dickson N2 convention from a separate quadratic RT oracle.

An additional multiplication tensor \(m:V\otimes V\to V\), or other low-degree tensors, refines symmetry from \(\mathrm{Stab}(Q)\) to \(\mathrm{Stab}(Q,m)\). For the compatible split Cayley algebra this produces a \(G_2\)-type automorphism group. **This does not imply that all tensor-stabilizer subgroups are maximal or exceptional**. For dimensions beyond 8, drop the insistence that a unital composition product with multiplicative nondegenerate quadratic norm exists on the same module. Clifford/Spin, other algebra-with-involution structures, tensor stabilizers, triality/isotopes, Jordan cubic norm, Freudenthal quartic norm and incidence approaches are different branches, not a single forced ladder.

**Status:** imported classical results; do not restore the invalid in-thread associator push proof or assert a generic four-dimensional nondegenerate quaternion slice for every pair.

## 4. Semilinear and Aschbacher context

For \(\mathbb F_{p^k}\), \(\Gamma L(V)\) allows Frobenius-semilinear transformations; for prime fields the field-automorphism contribution is trivial. Stabilizers of subspaces, extension-field structures, tensor products, repeated tensor factors, subfield forms and classical forms correspond to recognizable *geometric types* in Aschbacher's theory of subgroups of finite classical groups [R6]. The full classification contains a further almost-simple class. Aschbacher is a **classification of finite-group subgroup types**, not a machine that assigns a unique class or proves maximality for every chosen tensor.

This branch needs **no real-number computational substrate**, although published theory may invoke algebraic closures, representation theory and classification results. It is sound to construct finite linear-algebraic examples without claiming independent finite-only proofs of the entire classification.

Research target: for each chosen tensor package, specify the ambient \(\mathrm{GL}\), \(\mathrm{GO}\), or semilinear group, calculate its actual stabilizer/normalizer in small examples, then state precisely which Aschbacher containment theorem applies.

## 5. Directed routes, polygraphs, permutohedra and coherence

**Closest prior work:** Mazurkiewicz traces, Aalbersberg–Rozenberg partial commutations, Godefroid partial-order reduction, Postnikov permutohedra, Hatcher cellular homology and Guiraud–Malbos higher rewriting/coherence [R7–R12]. These already provide the concepts of local interchange, formal generators/relations, finite cell incidence, coherence among rewrites and semantically justified independence.

A **formal additive square** has identical endpoints by commutativity of fixed vector addition. A **state-dependent swap** generally does not:
\[
\kappa_{ij}(a)=U_j(U_i(a))-U_i(U_j(a)).
\]
Geometric spread acceptance alone never establishes \(\kappa_{ij}(a)=0\). Exact reroute 2-cells need actual endpoint equality at the same prefix. A nonzero comparison defect can be recorded with a distinct connecting-edge/comparison certificate, without declaring computational equivalence. A nonzero **isotropic** defect is still a failure of equality.

The higher coherence shape must be correct: three labels give a two-dimensional permutohedral hexagon \(P_3\), four labels a three-dimensional \(P_4\), six labels a five-dimensional \(P_6\). An additive cube is a distinct object. Tensor-direction rank, influence count, cell dimension and materialization budget are independent parameters.

**Current repository evidence:** [P6 exact pilot](../experiments/rt-p6-lift-pilot.md) constructs the 4683-cell \(P_6\) reference and records 120 geometric-positive/effect-negative swaps in each of two state-dependent fixtures. It is bounded finite-field evidence, not a training audit.

## 6. Homology, persistent (co)homology and inverse leader placement

**Nearest foundations:** Hatcher [R11], persistent topology and compressed-annotation cohomology [R13–R14], and standard greedy set cover [R15]. A policy class \([z]\in H_1(K;F)\) is excluded from the unpinned subcomplex \(U(S)\) exactly when
\[
[z]\notin \operatorname{im}\bigl(H_1(U(S);F)\to H_1(K;F)\bigr).
\]
This is basis-independent and decided by finite field linear algebra. A residual class can be accompanied by a lifted cycle witness in \(U(S)\); hitting a *single representative* need not eliminate the entire class. Hitting-set greedy approximation applies to the fixed finite witness family, **not** to the stronger invariant class-cover objective.

Cellular \(\partial_1\partial_2=0\) proves chain consistency, not operational interchangeability. \(H_1\) is the abelianized obstruction; nontrivial \(\pi_1\) and path-groupoid equality require their own verifier. Sparse persistent cohomology is a useful heuristic tool; no unconditional support-minimality of its chosen cocycles is assumed.

## 7. Probabilistic routes and neural training

**Closest constructions:** partial-order reduction/trace theory [R7–R9], stochastic and probabilistic audit literature, and equivariant neural architectures [R16–R17]. Route choice may be stochastic while a **specified exact update** is replayable deterministically. Exact equality of local updates, geometric admissibility of RT guards, and route-probability balance are separate claims.

For two choices \(i,j\) at state \(a\), a necessary local equality of the two probability products is
\[
p(i\mid a)\,p(j\mid U_i(a))=
p(j\mid a)\,p(i\mid U_j(a)).
\]
It does not follow from spread or from equal update endpoints. Full probabilistic route-class invariance requires more than one local balance equation.

A polynomial update \(P\) has a telescoping divided-difference factorization
\[
P(x)-P(y)=J_P(x,y)(x-y),
\]
with polynomial \(J_P\) constructible without limits. This is a standard algebraic technique, not automatically a new result. Sparse/structured tensor factorization of such defect transport may be an interesting implementation direction.

For actual LLM optimization, model state must include optimizer moments, data ordering, randomness and relevant execution details. A finite-field simulator or projection certifies **its own exact abstraction** only. Without a separately proved faithful encoding or error/behavioral relation, it does not certify floating-point training, model convergence, accuracy, security or robustness. Merkle hashes bind records but do not authenticate untrusted training without separately trusted pins/signatures and replay semantics.

Equivariant CNNs demonstrate the broader principle of constraining weights by group symmetry [R16], but provide no validation of an \(O(V,Q)\)- or \(G_2\)-constrained LLM training design.

## 8. Finite algebraic synchronization (Kuramoto analogy)

The classical Kuramoto model is a continuous phase/sine-coupled system. A cone-valued finite-field coupled map with spread gates is a **Kuramoto-inspired finite synchronization model**, not a derivation of the original differential equation. The finite field has no canonical ordering or analytic small-angle interpretation. A deterministic non-null repair using lexicographically ordered perturbations need not commute with \(\Gamma GO\); equivariance of the spread kernel is not equivariance of the entire update pipeline.

Recommended test: separate the symmetries of the invariant, eligibility gate, drift, couplings, update and repair. State the largest group common to all these operations before claiming equivariant dynamics.

## 9. Research decisions and prioritized falsifiers

| Candidate | Current disposition | Next mathematically meaningful check |
| --- | --- | --- |
| Gram spread, semilinear covariance, two-reflection transport | **Established / local conformance** | Extend verified rank-\(k\) invariants; guard all denominator inverses |
| Triple-spread defect | **Proceed narrowly**; straightforward expansion, novelty unassessed | Compare with classical Gram/Fricke and higher-dimensional RT sources; classify zero-defect nonplanar triples |
| Split Cayley / triality tensor package | **Import/redirect** | Pin correct multiplication convention and exact stabilizer hypotheses |
| Aschbacher tensor-structure families | **Study as taxonomy** | Do not infer maximality or finite-only global proof |
| State-dependent rerouting and higher cells | **Existing bounded work** | Independent trusted replay, exact prefix effects, coherent boundary closure |
| Persistent inverse leader | **Proceed with verifier** | Distinguish witness hitting from inclusion-map class elimination |
| Finite Kuramoto-like coupling | **Exploratory model** | Repair equivariance and gate-policy meaning |
| Probabilistic route balance / LLM training | **Defer claims of soundness** | State a concrete stochastic operational semantics; prove faithful training abstraction |
| Cubic/quartic RT-style ratios | **Definitions only** | Check polarization in small characteristic and prove nontrivial laws before naming a theory |

**False or overstrong claims to retain as negative controls:** unrestricted triple-spread in 8D; same-sign Zorn cross products; rank-\(k\) single determinant as complete orientation invariant; spread pass implies commuting updates; null residual norm implies zero residual; one witness-hit implies class coverage; sampled results imply generic polynomial identity; cross-ratio with distinct absolute intersections at tangency; and float-to-\(\mathbb F_q\) equivalence without a transfer theorem.

**Decision:** **redirect** this synthesis to a **context-only survey** and **proceed with narrowed targets** already cleared by the repository's dated RT/P4–P6 literature notes. Before implementing new theorem-facing tensor, probabilistic, or real-training claims, run separate 3–6-primary-source gates and exact negative controls. Do not change proof ledger, candidate status, vendored arithmetic, or acceptance authority on the basis of this literature review.

## Annotated primary and near-primary reference map

The locators below were checked in prior repository gates or identified in the current research review; **full source proofs were not independently re-read in this commit**. The list is a bibliographic map, not proof by citation.

- **[R1]** N. J. Wildberger, *Rational Trigonometry in Higher Dimensions and a Diagonal Rule*, KoG 21 (2017), Theorems 4–5: planar RT hypothesis boundary. https://master.grad.hr/hdgg/kog_stranica/kog21/KoG21.pdf
- **[R2]** T. Y. Lam, *Introduction to Quadratic Forms over Fields* (2005): Witt theory, Gram forms and finite-field classification. https://bookstore.ams.org/gsm-67
- **[R3]** A. Cayley / F. Klein, projective-absolute and cross-ratio geometry: historical construction (consult original work before fixing an exact theorem citation). General orientation: https://en.wikipedia.org/wiki/Cayley%E2%80%93Klein_metric
- **[R4]** R. D. Schafer, *An Introduction to Nonassociative Algebras* (1966), ch. III: alternativity, Artin and Moufang. https://www.math.uci.edu/~brusso/Schaferbook.pdf
- **[R5]** T. A. Springer and F. D. Veldkamp, *Octonions, Jordan Algebras and Exceptional Groups* (2000), chs. 1–3: composition, automorphisms and triality. https://doi.org/10.1007/978-3-662-12622-6
- **[R6]** P. B. Kleidman and M. W. Liebeck, *The Subgroup Structure of the Finite Classical Groups* (1990), chs. 1–4: Aschbacher geometric families and maximality boundaries. https://doi.org/10.1017/CBO9780511629235
- **[R7]** A. Mazurkiewicz, *Concurrent Program Schemes and their Interpretations* (1977), DAIMI PB-78: trace/independence precursor. https://doi.org/10.7146/dpb.v6i78.7691
- **[R8]** I. J. J. Aalbersberg and G. Rozenberg, *Theory of traces*, TCS 60 (1988), 1–82: partial commutations. https://doi.org/10.1016/0304-3975(88)90051-5
- **[R9]** P. Godefroid, *Partial-Order Methods for the Verification of Concurrent Systems* (1996), LNCS 1032, chs. 3–4: semantic independence before reduction. https://doi.org/10.1007/3-540-60761-7
- **[R10]** A. Postnikov, *Permutohedra, Associahedra, and Beyond* (2009), props. 2.5–2.6: ordered-partition faces. https://math.mit.edu/~apost/papers/permutohedron_full.pdf
- **[R11]** A. Hatcher, *Algebraic Topology* (2002), §2.2: cellular homology and boundary closure. https://pi.math.cornell.edu/~hatcher/AT/AT-doublepage.pdf
- **[R12]** Y. Guiraud and P. Malbos, *Higher-dimensional normalisation strategies for acyclicity* (2012): polygraphic coherence. https://doi.org/10.1016/j.aim.2012.05.010
- **[R13]** H. Edelsbrunner and J. Harer, *Computational Topology: An Introduction* (2010): finite homology/persistence matrix computations. https://doi.org/10.1090/mbk/069
- **[R14]** J.-D. Boissonnat et al., *The Compressed Annotation Matrix: An Efficient Data Structure for Computing Persistent Cohomology* (2013): annotations and computation. https://arxiv.org/abs/1304.6813
- **[R15]** V. V. Vazirani, *Approximation Algorithms* (2001/2003), ch. 2: greedy set cover and its limited guarantee. https://www.springer.com/gp/book/9783540653677
- **[R16]** T. S. Cohen and M. Welling, *Group Equivariant Convolutional Networks*, ICML 2016: symmetry-based weight sharing and equivariance, not training-route proof. https://proceedings.mlr.press/v48/cohenc16.html
- **[R17]** S. Annamalai et al., *To Shuffle or not to Shuffle: Auditing DP-SGD with Shuffling* (arXiv 2411.10614, subsequent 2026 venue): privacy audit affected by sampling/shuffling; distinct from exact operational reroute verification. https://arxiv.org/abs/2411.10614

## Repository-specific continuity

Existing literature gates: [split-Cayley/RT](../literature/split-cayley-rt-foundations-2026-10-24.md), [rank-lift](../literature/rank-lift-route-complexes-2026-10-26.md), [state-dependent effects](../literature/state-dependent-rt-coherence-2026-10-26.md), [permutation coherence](../literature/p4-permutohedral-coherence-2026-10-26.md), and [receipt replay](../literature/rt-route-stream-replay-2026-10-26.md). Shared exact Mojo RT and tensor kernels remain owned by [finite-math-kernels](https://github.com/larsbx/finite-math-kernels/blob/main/docs/rt-route-kernels-mojo.md). This survey modifies **no** kernel, model, generated artifact, experimental data, claim registry or publication table.
