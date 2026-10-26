# State-dependent permutation-route audit — bounded literature gate (2026-10-26)

**Decision: proceed with a narrowed target.** Extend the merged P4 RT coherence specimen with **exact local effect certificates for state-dependent transformations** over F5. No theorem promotion, novelty, actual LLM training audit, or probabilistic soundness claim.

## 1. Proposed experiment

Retain the existing combinatorial P4 (24 orderings and 36 adjacent-swap edges), RT spread and direction interface. Give each influence a deterministic map U_i: F5^8 → F5^8. For every adjacent-transposition edge, evaluate the actual prefix state A, both local composites U_j(U_i(A)) and U_i(U_j(A)), their **vector residual**, and spreads of the transported displacement directions. Define separate predicates:

- **geometric admissibility:** both opposite-direction spreads defined and members of an explicit field gate S⊆F5;
- **exact computational equivalence:** the full residual **vector** is zero;
- **certified swap:** geometric AND exact computational checks succeed.

Admit a P4 two-face only when every boundary swap is certified, and admit the top 3-cell only when every 2-face is certified. A verifier recomputes claimed certificates against the declared state-dependent maps. Exhaustively check the 36 adjacent-swap contexts of one P4 fixture and reject forged records. This is a finite **consumer experiment**, not a second shared algebra library.

## 2. Closest primary literature and boundaries (checked 2026-10-26)

| Work | Locator and access depth | Relevant result / boundary |
| --- | --- | --- |
| A. Mazurkiewicz, *Concurrent Program Schemes and their Interpretations* (1977), DAIMI PB-78, abstract and publication record, https://doi.org/10.7146/dpb.v6i78.7691 | Primary scheme/trace construction, original abstract checked. | Partial-order traces record permissible reordering. The experiment does **not** assume an arbitrary geometric gate supplies a valid independence relation. |
| I. J. J. Aalbersberg and G. Rozenberg, *Theory of traces* (1988), *TCS* 60(1), pp. 1–82, abstract, https://doi.org/10.1016/0304-3975(88)90051-5 | Partial-commutation structure, abstract checked. | Classical global trace-independence must be distinguished from **state-dependent, prefix-conditioned** effect equalities. |
| P. Godefroid, *Partial-Order Methods for the Verification of Concurrent Systems* (1996), LNCS 1032, contents §3–§4 / publisher overview, https://doi.org/10.1007/3-540-60761-7 | Methods for reducing interleavings subject to valid independence, contents checked. | Certificate replays are not a claimed partial-order-reduction completeness result, and all 24 permutations are computed in this pilot. |
| Y. Guiraud and P. Malbos, *Higher-dimensional normalisation strategies for acyclicity* (2012), *Adv. Math.* 231, pp. 2294–2351, abstract, https://doi.org/10.1016/j.aim.2012.05.010 | Higher-dimensional rewriting/coherence literature, abstract checked. | Filling a P4 3-cell is separate from declaring pairwise geometric eligibility. No general coherence theorem follows from the pilot. |
| Prior repository `docs/literature/p4-permutohedral-coherence-2026-10-26.md`, §§1–6 | P4 combinatorial/RT literature gate already reviewed | Face counts and chain differential are inherited, not reproved as novel. |

These are **bounded literature checks**, not a proof-by-citation or priority search. Full original proof texts of the works above were not independently verified here.

## 3. Terminology

- `geometric_pass`: spreads satisfy a predeclared field subset gate; **not** semantic equality.
- `effect_equal`: vector endpoints after the two *local* orders agree exactly in F5^8; **not** merely equal norm/spread and not just final equality after a potentially non-injective suffix.
- `certified_swap`: both tests pass, with an exact prefix/endpoint witness and deterministic replay.
- `face_admitted`: all boundary swap certificates pass. `top_admitted`: all face witnesses admitted and existing P4 `∂2∂3=0` test passes.
- `tensor direction rank`, `permutation coherence rank`, `cell dimension` and `materialization budget` remain independent.

## 4. Hypotheses and negative controls

- F5, exact modular arithmetic, no real-valued order, no roots, and spread division only under non-null guards.
- Frozen translations U_i(x)=x+d_i commute exactly. A **state-dependent** update U_0(x)=x+(1+x_1)d_0 and U_1(x)=x+d_1 does **not** commute, although all transported directions remain projectively parallel and every geometric gate `{0}` passes.
- Null-residual counterexample U_0(x)=x+d_0+x_1 e_0: residual equals a nonzero *null vector* on some swapped routes. A scalar norm-zero test would accept falsely; the verifier must compare all coordinates.
- A suffix after a swap may collapse differing local endpoints. Certificates compare endpoints **before** the suffix; endpoint equality at the whole-word level is insufficient alone.
- Any forged residual or spread in a certificate must fail exact replay.
- Partial face admission cannot justify the top 3-cell. Do not infer tensor-model optimization quality, training accuracy, approximate numerical error or probabilistic guarantees.

## 5. Decision

**Proceed with narrowed experiment** in `experiments/rt/state_dependent_coherence_pilot.py` plus focused `GUARDS_CONTRACT` tests and a bounded report. Reuse existing independent RT oracle and P4 combinatorics; do not copy kernels into `kernel/` or edit vendor/ledger/generated authority. A separate upstream interface proof will be needed before general tensor-route certification or floating-model equivalence claims.
