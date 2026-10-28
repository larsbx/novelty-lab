# Algebraic topology packet H1 — homologous alternative cycles survive witness hitting

**Authority:** bounded, non-authoritative consumer research in `experiments/rt/field_pilots/`; original cross-disciplinary partition [here](../../surveys/fields/README.md). **Literature stop/go:** [bounded field-pilot gate](../../literature/rt-field-bounded-pilots-2026-10-28.md). **Governance:** `AGENTS.md`, `docs/calibration.md`, `docs/verification.md`. No novelty/theorem/status promotion.

**Question:** Does hitting one explicitly exhibited cycle eliminate the homology class it represents? **Not generally.**

**Object/field:** 3-square cylindrical cell complex over `F5`, with top and bottom triangular edge cycles and three joining edges. Boundary of each oriented side face is `t_i - b_i + v_(i+1) - v_i`.

**Hypotheses:** both loops are cycles; their difference is the sum of all three 2-face boundaries; neither loop is itself in `im(partial_2)`, verified by exhausting `5^3=125` combinations of the three faces. Removing one top edge hits the top witness, but the bottom witness remains in the surviving subcomplex and is nontrivial in the original complex. This models the gap between witness-hit and inclusion-induced class coverage.

**Literature:** Hatcher §2.2 as pinned in [P4/Gram rank-lift gate](../../literature/rank-lift-route-complexes-2026-10-26.md) and the [bounded pilot gate](../../literature/rt-field-bounded-pilots-2026-10-28.md). This is a textbook-style finite cylinder, not a new homology algorithm.

**Procedure:** `topology.run()` independently checks all oriented face boundaries, cycle closures, finite image membership and survival of the bottom support. No generic sparse homology library is added under the consumer plane.

**Reproduce:** `python -m experiments.rt.field_pilots`, `test_topology_witness_hit_is_not_class_elimination`.

**Claim ceiling:** one 9-edge, 3-face exact counterexample, not the complexity or completeness of the inverse-leader solver.

**Next falsifier:** parameterize a small deletion family and compute the exact inclusion-induced map rank before announcing class coverage. Distinguish `H1` from nonabelian `pi1` route claims.
