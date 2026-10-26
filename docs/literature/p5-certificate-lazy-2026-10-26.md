# Certificate-demanded P5 boundary closures — bounded literature gate (2026-10-26)

**Decision:** **proceed with a narrowed experiment**. Add an actual on-demand consumer-specific P5 cellular face constructor that materializes only the requested cell(s) and their recursively required boundaries. Reuse the exact incidence and independently pinned F5 receipt verifier merged in PRs #46–47. Do not promote novelty, mathematical theorem status, or a general-purpose finite-math kernel.

## 1. Proposed finite experiment

The existing `experiments/rt/p5_full_coherence.py` constructs **all 541 cells** (120,240,150,30,1) before selecting them. Contrast its complete reference with a lazy P5 cache driven by independently replayed RT/effect certificates. Required finite controls: one square closure (4,4,1,0,0), one hexagon (6,6,1,0,0), one P4 facet (24,36,14,1,0), and the P5 top cell (120,240,150,30,1). Verify exactly matching signed coefficients for every instantiated incidence and integer d²=0. Enforce an **atomic budget** so a rejected request leaves the existing cache unchanged. Admit faces only after **all** immediate lower facets have been certified, and distinguish requested-only receipts from completeness.

## 2. Closest primary literature (checked 2026-10-26)

| Work | Locator | Transferred construction and boundary |
| --- | --- | --- |
| A. Postnikov, *Permutohedra, Associahedra, and Beyond* (2009) | Propositions 2.5–2.6 and ordered set partitions, https://math.mit.edu/~apost/papers/permutohedron_full.pdf | Face-poset combinatorics standard; no new permutohedral theorem. |
| A. Hatcher, *Algebraic Topology* (2002) | §2.2 cellular homology, https://pi.math.cornell.edu/~hatcher/AT/AT-doublepage.pdf | Boundary closure and d²=0 are classical properties; finite computation checks implementation orientation. |
| P. Godefroid, *Partial-Order Methods for the Verification of Concurrent Systems* (1996) | Chapters 3–4, https://doi.org/10.1007/3-540-60761-7 | State-dependent commutations need validated independence. Sparse observed traces are **not** complete verification. |
| A. Mazurkiewicz, *Concurrent Program Schemes and their Interpretations* (1977) | DAIMI PB-78, https://doi.org/10.7146/dpb.v6i78.7691 | Trace independence does not follow from projective RT spread gates alone. |

The closest original works are already scoped by `docs/literature/p5-full-coherence-2026-10-26.md` and `docs/literature/rt-route-stream-replay-2026-10-26.md`. These locators were consulted/reused; a full priority search and line-by-line proof verification are **not** claimed.

## 3. Exact hypotheses and negative controls

- Fix the same ordered-partition P5 on labels 0..4 as the existing reference. The only math functions used for a requested face are the **existing** exact `facets` and `incidence` computations; they are imported rather than reimplemented or moved to the canonical kernel.
- An unrequested cell is **not** instantiated, even if it is a face elsewhere in abstract P5. A higher cell is only present when all its lower faces are included; no incomplete cell is ever returned.
- Forged receipts, wrong trusted spec pins, and requested-only traces presented as complete fail closed under the already versioned `rt-route-stream/v1` verifier.
- A request with a cell-count budget smaller than its boundary closure must fail *without mutating the cache*. Falsify the implementation by stripping one required face or reversing one signed incidence.
- A geometric-positive but effect-negative swap does **not** authorize a higher face.
- **Distinct levels:** coherence rank five, maximal cell dimension four, tensor-direction rank one or two, materialization budget arbitrary. Materialization savings demonstrate a bounded representation count, **not** a measured runtime gain or new theorem.

## 4. Decision

**Proceed, narrowed** in the repository's non-authoritative experiments + regression tests + dated report. Independent full P5 cross-check remains the acceptance oracle. No edits to vendor/, upstream math kernels, theorem ledger, or generated surfaces. Do not assert general rank-R, probabilistic route equivalence, float-to-F5 soundness, or model-training correctness.
