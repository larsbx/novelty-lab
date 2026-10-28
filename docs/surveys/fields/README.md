# Field-separated research map — quadratic RT, route rewriting, and training audits

**Type:** navigation and evidence-boundary guide; **not** a global verification policy, theorem, or claim promotion.  
**Date:** 2026-10-28. **Source context:** [cross-disciplinary literature review](../rt-tensor-route-auditing-context-2026-10-28.md) and its [bounded gate](../../literature/rt-tensor-route-audit-context-2026-10-28.md).

This program contains different disciplines, not one escalating proof ladder. **Proof, formal verification, conformance testing, experiments, statistical inference and engineering deployment answer different questions.** The purpose of this index is to let each field develop independently while requiring explicit interfaces when one field makes claims about another.

| Field | Own subject | Typical defensible evidence | Not implied |
| --- | --- | --- | --- |
| [Pure mathematics and invariant theory](mathematics.md) | finite quadratic spaces, Cayley algebras, Gram forms, exterior/tensor invariants | algebraic proof under stated hypotheses; reviewed citations; exact counterexamples | software implementation correctness or practical model improvement |
| [Theoretical CS and algebraic topology](theoretical-cs-topology.md) | formal rewriting, directed routes, polygraphs, permutohedral cells, \(H_1\)/\(\pi_1\), complexity | theorem under formal semantics, exact finite incidence, certified combinatorial constructions | agreement of concrete state-dependent programs |
| [Software systems, verification and security](systems-verification.md) | update interpreter, replay, typed guards, receipts, hashes, toolchains, provenance | test/replay results, model checking with bounded scope, refinement proof if available, independently trusted pins/signatures | universal correctness from finite tests; authenticated origin from a hash alone |
| [Stochastic processes and finite control](stochastic-control.md) | finite-state scheduling, probability, synchronization-like finite dynamics, control-policy choices | exact transition calculations, conditional probabilistic theorems, finite simulation where claims are bounded | ordinary continuous Kuramoto dynamics or long-run behavior without a theorem |
| [Machine learning and empirical training](machine-learning.md) | optimizer order, measured performance, reproduction, generalization and robustness | transparent experimental design, hardware/software provenance, statistical reporting and independent replication | a training-performance theorem from a finite-field surrogate |
| [Interdisciplinary interface contracts](bridges.md) | transfers between the above representations | separate bridge statement with explicit assumptions and targeted evidence | importing the strongest verification label from either side |

## Independent promotion and reporting

Every claim states **field, object, scope, method, evidence and limitations**. A classical mathematical statement may be proved and cited while a corresponding Mojo function remains untested; conversely, a finite-route program may pass exhaustive regression for a fixed implementation without proving a general theorem. Neither conclusion is internally contradictory. A CS correctness theorem is possible and valuable when a formal specification is fixed; **CS is not categorically unprovable**. Empirical ML hypotheses generally require observations, not a forced mathematical proof.

This map does **not** change repository governance in [calibration](../../calibration.md) or [verification](../../verification.md); those existing authority rules continue to govern any claim actually promoted into their respective registries. It prevents **cross-field inference without a bridge**, not progress within an individual field.

## Integration examples

- A correct Gram identity does not validate an algorithm implementing it. The integration claim needs a field-arithmetic model plus implementation conformance or a refinement theorem.
- A permutohedral 2-cell is a valid formal boundary without proving that two optimizer calls commute. Operational equivalence requires replay at the **same prefix state**, all relevant optimizer state included, and equality of complete endpoints.
- A stored exact schedule trace can be verified independently of whether it was sampled from an asserted probability law. Distribution claims need a separate probabilistic model and evidence.
- A passing finite \(\mathbb F_q\) training-proxy run validates the proxy under its declared semantics, not floating-point neural training unless a transfer/abstraction theorem is separately supplied.
- A successful homology witness-hit operation destroys that witness, not automatically all cycles representing the same \(H_1\) class.

## Ownership and next deliverables

The **reusable exact arithmetic/geometric algorithms** belong to [finite-math-kernels](https://github.com/larsbx/finite-math-kernels) under its existing Mojo/provenance policy. **Finite route experiments, receipts and bounded model comparisons** stay in this repository's non-authoritative experimental plane. **Empirical model training** requires separate experimental protocol and data; it is not absorbed into the mathematics ledger by default. Interdisciplinary output should link a precise interface statement and evidence from each relevant owner.

Proposed next independent outputs: a mathematical theorem/negative-control dossier for a selected tensor invariant; a theoretical-CS formal-rewrite soundness specification; a systems replay-conformance matrix; a finite Markov/synchronization experiment; and only then an optional ML measurement protocol. None is a prerequisite for unrelated claims in other fields.
