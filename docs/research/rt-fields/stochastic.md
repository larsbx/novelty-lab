# Probability/control packet P1 — rational local balance is independent of exact effects

**Authority:** bounded, non-authoritative consumer research in `experiments/rt/field_pilots/`; original cross-disciplinary partition [here](../../surveys/fields/README.md). **Literature stop/go:** [bounded field-pilot gate](../../literature/rt-field-bounded-pilots-2026-10-28.md). **Governance:** `AGENTS.md`, `docs/calibration.md`, `docs/verification.md`. No novelty/theorem/status promotion.

**Question:** Does commuting deterministic state effect imply equal probabilities of the two local execution orders? **No.**

**Object:** two rational two-step schedule configurations. From initial state choose each of labels `a,b` with probability 1/2. The second-step choice uses declared conditional values; any unused conditional mass is an explicitly modelled STOP outcome (not silently discarded).

**Hypotheses:** with both second-choice conditional probabilities 1, complete-path weights are both 1/2. With conditional probabilities 3/4 after `a` and 1/4 after `b`, complete-path weights are 3/8 and 1/8 with remaining 1/2 STOP mass. This is a valid two-step toy law even when state effects are commuting translations.

**Literature:** finite Markov chains (Kemeny–Snell) and [bounded gate](../../literature/rt-field-bounded-pilots-2026-10-28.md). The `Fraction` probabilities are in ordered nonnegative rationals, not probability interpreted directly in `F5`.

**Procedure/controls:** `stochastic.run()` validates conditional ranges, computes both exact route weights and stop mass, and refuses an invalid >1 conditional probability. The reported result is algebraic finite arithmetic, not measured stochastic training.

**Reproduce:** `python -m experiments.rt.field_pilots`, `test_probability_locally_equal_versus_unequal_paths`.

**Claim ceiling:** one finite distribution comparison, neither global detailed balance nor stochastic bisimulation.

**Next falsifier:** enumerate every transition of a declared 3-state rational Markov kernel, check row normalization and exact short-horizon distribution consistency, then separately define what a route-class probability claim means.
