# Software systems, verification and security — exact replay and evidence

**Discipline:** software engineering, formal methods, deterministic interpreters, verification tooling, records/provenance and security. A correct finite program does not require an all-encompassing mathematical proof of every surrounding research hypothesis.

## Own objects

The implementation has its own **typed update specification**, state encoding, finite arithmetic and guard semantics, synchronous/asynchronous schedule, deterministic replay, serialized certificate format, independently supplied trusted specification pin, and versioned acceptance tests. Operational equality of swapped updates requires checking all state components; a zero quadratic norm of the difference is insufficient.

**Security separates integrity from authenticity.** A Merkle root or SHA-256 digest can commit to bytes, but alone does not establish who generated them, whether the interpreter was trusted or whether the asserted run actually happened. Selective membership proofs are not evidence that *unopened* records were checked. Signed origin, threat model, and trusted measurement chain must be additional claims with distinct evidence.

## Verification classes are not interchangeable

| Question | Possible evidence | Limit |
| --- | --- | --- |
| Does an implementation match its declared finite specification on selected inputs? | deterministic unit/integration tests, differential oracles | limited test domain |
| Does a finite state machine satisfy an invariant within a declared bound? | exhaustive state exploration/model checking | bounded by model abstraction, reachability and state-space coverage |
| Does a concrete interpreter refine an abstract transition specification? | a refinement/functional-correctness proof | conditional on semantics, environment and proof assumptions |
| Does a serialized receipt replay exactly? | independent verifier with canonical parser and independently trusted spec | certifies the checked trace, not necessarily its origin |
| Did an authenticated actor produce a record? | signature verification under an independently trusted credential | provenance relative to the key/trust model, not physical execution |
| Does the real deployed service behave as modeled? | runtime telemetry, integration/security testing, verified deployment evidence | not implied by a model checker alone |

A full correctness theorem is possible for well-scoped CS systems, but successful tests are not *promoted to* such a theorem. Conversely, a useful engineering deliverable can be accepted with a disclosed test/operational assurance level, without waiting for a field-generic pure-math classification theorem.

## Existing boundaries and next testable work

The repository's [RT route replay report](../../experiments/rt-route-stream-replay-v1.md) and [P6 chunked replay](../../experiments/rt-p6-chunked-replay.md) are bounded exact consumers of a pinned finite state model. They do not authenticate human provenance or prove actual floating-point training equivalence. Future work should specify coverage, trusted pin transport, schema evolution, failure policy and replay resource limits **as systems requirements**, not as corollaries of spread identities.

**Source:** [cross-disciplinary context](../rt-tensor-route-auditing-context-2026-10-28.md).
