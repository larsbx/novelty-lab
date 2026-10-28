# Theoretical CS packet T1 — permitted P4 rewrites versus actual effects

**Authority:** bounded, non-authoritative consumer research in `experiments/rt/field_pilots/`; original cross-disciplinary partition [here](../../surveys/fields/README.md). **Literature stop/go:** [bounded field-pilot gate](../../literature/rt-field-bounded-pilots-2026-10-28.md). **Governance:** `AGENTS.md`, `docs/calibration.md`, `docs/verification.md`. No novelty/theorem/status promotion.

**Question:** How many geometrically eligible adjacent swaps remain executable when influence maps depend on prefix state?

**Object:** existing exact P4 order complex (24 permutation vertices, 36 adjacent swap edges, 14 2-faces, 1 top 3-cell) and the `F5^8` state-dependent update vocabulary. The formal face differential is separate from `U_j(U_i(a)) == U_i(U_j(a))` at the actual prefix.

**Hypothesis/negative control:** frozen translations certify all 36 swaps and the top cell. The existing scalar-coupled specimen admits geometric spread for all 36 but **only 30** effect equalities. The null residual variant has 6 rejected nonzero norm-zero residuals. Geometric-only admission must never create a computational-equivalence face.

**Literature:** [state-dependent coherence gate](../../literature/state-dependent-rt-coherence-2026-10-26.md), [P4 primary-source gate](../../literature/p4-permutohedral-coherence-2026-10-26.md), [bounded field pilot gate](../../literature/rt-field-bounded-pilots-2026-10-28.md). Trace independence (Mazurkiewicz/Godefroid) and higher rewrite coherence are not claimed anew.

**Procedure:** reuse `P4.d1d2_zero`, `d2d3_zero`, and `state_dependent_coherence_pilot.audit` without a second general incidence implementation. The **new prefix-stability falsifier** uses U0(x)=x+(2+x1²)d0 and U1(x)=x+d1: over F5 they commute at a prefix with x1=2, but not at the origin x1=0, even though both transported projective direction spreads equal zero and are non-null. This is a bounded prefix-conditioned witness, not a general confluence theorem.

**Reproduce:** `python -m experiments.rt.field_pilots` and the `test_theoretical_cs_geometry_does_not_authorize_swap` contract test.

**Claim ceiling:** finite P4 re-evaluation of existing semantics; no general confluence or contextual equivalence theorem.

**Next falsifier:** search a finite prefix-dependent update family for an exact local equality that fails under the intended *extended state* semantics, or prove a conditional context-stability lemma with explicit hypotheses.
