# Cross-discipline packet B1 — reduction modulo 5 is not a faithful effect-equality map

**Authority:** bounded, non-authoritative consumer research in `experiments/rt/field_pilots/`; original cross-disciplinary partition [here](../../surveys/fields/README.md). **Literature stop/go:** [bounded field-pilot gate](../../literature/rt-field-bounded-pilots-2026-10-28.md). **Governance:** `AGENTS.md`, `docs/calibration.md`, `docs/verification.md`. No novelty/theorem/status promotion.

**Question:** If two integer transitions have the same output in a finite field, may a software auditor infer equality of their integer (or floating-point) effects? **No** without an additional faithful-transfer hypothesis.

**Object:** exact integer functions `A(x)=x+5`, `B(x)=2x`, anchor `x=1`. Their two compositions are `B(A(1))=12` and `A(B(1))=7`: distinct integers, identical residues modulo 5, a nonzero integer defect of 5 mapping to zero.

**Hypothesis/negative control:** `bridges.run()` confirms source effect inequality, target residue equality and loss of the defect. No stochastic, analytic or real-training claims enter. This falsifies the implication “mod-p equality ⇒ source equality” in the absence of a bounded injective encoding.

**Literature:** [bounded field pilot gate](../../literature/rt-field-bounded-pilots-2026-10-28.md) and [cross-field interface contracts](../../surveys/fields/bridges.md), which require a separate representation map, transfer assertion, failed case and evidence.

**Reproduce:** `python -m experiments.rt.field_pilots`, `test_bridge_f5_equality_does_not_lift`.

**Claim ceiling:** one constructive counterexample; it does not refute *every* bounded encoding or faithfully simulated subset.

**Next falsifier:** construct a declared fixed-point interval/state encoder with a proof of injectivity over a bounded range and an explicit transition preservation theorem; reject executions that leave that range.
