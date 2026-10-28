# Cross-field bridge contracts — no automatic transfer of verification

**Purpose:** specify **additional obligations only when one discipline makes claims about another**. These bridges are optional; no field must prove every downstream application before it can finish its own result.

## Typed claim interface

A bridge record should state:

| Field | Meaning |
| --- | --- |
| source claim | precise upstream object, hypotheses, evidence and version |
| target claim | precise statement that depends on it, in the target discipline |
| representation map | specified translation/encoding and guards, including information loss |
| transfer assertion | exact equality, simulation, refinement, statistical relation, or other explicit claim |
| proof/test obligation | evidence required for **that transfer**, not generic "verified" |
| failure case | a falsifier demonstrating what would break the transfer |
| accepted evidence | separate source and target references or artifacts |
| limitations | coverage, approximation, trust and novelty limits |

## Four essential bridges

### B1 — Algebraic identity → executable kernel

Source: a proved guarded spread/Gram identity. Target: a concrete field-typed implementation. Transfer obligation: the arithmetic model, input domain, rejected/null handling, overflow/representation semantics and implemented formula correspond to the source. Mojo tests and independent Python conformance support an implementation claim; an all-input code correctness theorem would require its own proof.

### B2 — Formal rewrite cell → operational route equivalence

Source: a legal combinatorial square, hexagon or higher cell. Target: two concrete state-dependent computations may be exchanged. Transfer obligation: evaluate both update orders at the same complete prefix state, verify **whole endpoint equality** and applicable geometric guards, and justify any stability under later contexts. A valid formal incidence alone is insufficient.

### B3 — Finite state replay → probability law / provenance

Source: a recorded finite sequence of valid transitions. Target: assertion that the trace was drawn from a specified stochastic process, or produced by an authenticated party. Transfer obligation: externally grounded sampling law and measure calculations for probability; independent trusted pin/signature/run provenance for origin. A Merkle root proves integrity of committed bytes, not these target claims.

### B4 — Finite surrogate → actual ML training

Source: exact finite-field or rational-state simulation. Target: claims about floating-point weights, training outcome, model predictions or safety. Transfer obligation: faithful state/transition encoding, explicit abstraction/refinement semantics or bounded error propagation, plus application-relevant empirical validation. **No default transfer theorem exists**.

## Evidence independence

Declare bridge status as **unspecified, defined, tested-on-domain, proved-under-assumptions, or refuted**. This is a local research vocabulary rather than a change to the existing governed claim ledger. Mathematical results keep their independent proof status; verified CS executions retain their declared test coverage; empirical results retain their statistical protocol. A failed bridge invalidates the *derived cross-field assertion*, not necessarily the source-domain result.

**Do not use a single scalar "verified" label across disciplines**; always say *what*, *under which model*, *by which method*, *with what scope*.

For prior sources and completed bounded experiments, see the [cross-disciplinary survey](../rt-tensor-route-auditing-context-2026-10-28.md).
