# Machine learning packet L1 — optimizer order on exact rational toy states

**Authority:** bounded, non-authoritative consumer research in `experiments/rt/field_pilots/`; original cross-disciplinary partition [here](../../surveys/fields/README.md). **Literature stop/go:** [bounded field-pilot gate](../../literature/rt-field-bounded-pilots-2026-10-28.md). **Governance:** `AGENTS.md`, `docs/calibration.md`, `docs/verification.md`. No novelty/theorem/status promotion.

**Question:** Can update order influence loss or optimizer future behavior even when immediate parameter weights coincide?

**Object:** two exact scalar squared-loss examples with targets 0 and 2 and two deterministic orders, learning rate 1/2. Compare ordinary SGD and a separate momentum rule `m'=m/2+(w-target)`, `w'=w-m'/2` with full state `(w,m)`.

**Hypotheses and controls:** SGD on initial `w=0` yields weights 1 vs 1/2 and total unnormalized squared losses 2 vs 5/2. Momentum yields **the same weight 1** after both orders, but different states `(1,-2)` and `(1,0)`, which diverge on the next example. Thus comparing weights only can conceal operational order dependence.

**Literature:** optimization background (Bottou–Curtis–Nocedal), [bounded gate](../../literature/rt-field-bounded-pilots-2026-10-28.md). The rule is a specified rational toy, not a claim about a production optimizer or convergence distribution.

**Procedure:** `machine_learning.run()` checks the exact algebraic targets; all results are reproducible and require no random seed or external dataset.

**Reproduce:** `python -m experiments.rt.field_pilots` and `test_machine_learning_full_optimizer_state_matters`.

**Claim ceiling:** deterministic two-sample toy observations, not speed, stability, accuracy, statistical significance, or behavior of a neural network.

**Next falsifier:** choose a real optimizer implementation and a small named synthetic dataset, record full optimizer state and precision/device, specify loss/accuracy/cost metrics and replications. Keep any field-to-floating representation theorem as a distinct bridge task.
