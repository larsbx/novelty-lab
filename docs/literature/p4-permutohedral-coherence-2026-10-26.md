# P4 permutohedral incidence and tensor-direction adapter — bounded gate (2026-10-26)

**Decision: proceed with a narrowed target.** Implement a finite **P4** combinatorial incidence/check experiment and a rank-1/rank-2 consumer direction adapter. No universal coherence theorem, full rank-R implementation, neural-training equivalence, or novel mathematical discovery is asserted.

## 1. Proposed claim or experiment

Extend the preceding `P3` vs additive cube specimen to the **3-dimensional permutohedron on 4 influence labels**, with 24 permutation vertices, 36 adjacent-swap edges, 8 hexagonal and 6 square two-faces, and a single 3-cell. Derive the incidence maps using the face poset of ordered set partitions; check `∂1∂2=0` and `∂2∂3=0` exactly over integer coefficients. Independently select rank-one projective or rank-two Grassmann directions through a typed experimental consumer interface using existing exact `F5` RT oracle functions. Include a geometric-gate-pass / semantic-order-failure negative control.

## 2. Sources (consulted 2026-10-26)

| Primary work | Locator, reading depth | Closest theorem / boundary |
| --- | --- | --- |
| Alexander Postnikov, *Permutohedra, Associahedra, and Beyond* (IMRN 2009) | **Proposition 2.6** and preceding Proposition 2.5, full author-hosted paper PDF inspected (p. 6). https://math.mit.edu/~apost/papers/permutohedron_full.pdf | Faces indexed by ordered partitions and edges by adjacent transpositions. Classical results: the face enumeration is not new. Original geometric model is over real polytopes; this experiment uses their *finite combinatorial incidence*, not real arithmetic as an executable substrate. |
| Allen Hatcher, *Algebraic Topology* (2002) | **§2.2 Cellular Homology**, particularly cellular boundary maps and their composition. https://pi.math.cornell.edu/~hatcher/AT/AT-doublepage.pdf | The CW chain condition is classical. This experiment independently checks signed orientation on a finite face poset, not a new homology theorem. |
| Postnikov, Reiner, Williams, *Faces of Generalized Permutohedra* (Documenta Math. 13, 2008) | Abstract and bibliographic summary checked (open-access publisher entry), https://doi.org/10.4171/DM/248 | A broad existing combinatorial face framework; no novelty inference from producing `P4` cells. |
| N. J. Wildberger, *Rational Trigonometry in Higher Dimensions and a Diagonal Rule* (KoG 21, 2017) | Prior bounded `split-cayley-rt-foundations-2026-10-24.md` locator Theorems 4–5, not rechecked in full this turn. | Spread is a guarded quadratic invariant; the triple spread formula does not apply to arbitrary independent high-dimensional directions. |

## 3. Terminology

**Coherence rank = influence labels (4)**; **CW cell dimension = 3**; **tensor-direction rank = 1 or 2**; **materialization budget = specified face boundary closures**. These four are independent. `P4` is combinatorially a truncated octahedron, with square and hexagonal faces. `∂3` may be oriented by propagating incidence signs over its closed shell; this is not an arbitrary braid identity about state-dependent update functions.

## 4. Hypotheses and transfer limits

- Combinatorial `P4` face poset is computed with finite tuples of integers (not projective rays); its integer signed incidences are checked by cancellation.
- `F_5^8` is used only for RT gate/Grassmann checks, through the existing independent consumer oracle. No generic new finite-field or determinant engine; upstream `finite-math-kernels` remains authoritative for shared kernels.
- A gate `{1}` approves pairwise spreads 1 among four pairwise orthogonal non-null directions; **orthogonality does not prove commutation of two operators**.
- Coherence means a **permitted formal cell**; actual semantic equality of state-dependent update compositions requires independent endpoint/effect certificates.
- `DirectionModel(kind,indices)` offers precisely `ray/1` and `grassmann/2`. Arbitrary `k`, tensor extraction, and general `R` remain outside this bounded experiment.
- An upper 3-cell is only materialized when all of its 14 oriented 2-faces have been included. Sparse instantiation is a budget, not a mathematical dimensional restriction.

## 5. Negative controls

1. Flip one 2-face orientation in `∂3`: then `∂2∂3 != 0`.
2. Demand a nonexistent face: sparse closure rejects.
3. Gate `{0}` rejects all four direction pairs even though `{1}` accepts them; spread gates use a subset rather than an ordering of `F5`.
4. Null ray and degenerate Grassmann basis are rejected.
5. Change a Grassmann basis: ratio remains invariant when defined.
6. Distinct noncommuting maps `x -> x+v` and `x -> 2x` produce different endpoints although the geometric fixture passes.

## 6. Decision

**Proceed with a narrowed target**: add `experiments/rt/p4_coherence_pilot.py`, a contract-guarded test suite and a dated bounded report, without changing proof ledger/status, canonical `kernel/`, vendored Mojo sources, or existing P3 experiment. Require CI/verification gates for merge. This clears a small finite experiment only; it does not establish mathematical novelty, training correctness, or a general coherence calculus.
