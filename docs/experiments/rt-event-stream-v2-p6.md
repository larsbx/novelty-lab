# Experiment VIII — externally replayable six-influence RT receipts (v2-p6)

**Status:** bounded exact F5 consumer experiment, pending hosted acceptance. **Literature gate:** [p6-receipt-v2-2026-10-26](../literature/p6-receipt-v2-2026-10-26.md). Built on the P6 signed-cell and exact-effect specimen under PR #49 and the merged P5/v1 receipt experiment. No mathematical theorem, novel topology, or LLM-training guarantee is promoted.

## Problem closed

Version 1 of the external receipt protocol accepts **only 3–5 influences**. The six-influence P6 experiment had an exact *internal* route computation but lacked an independently pinned externally replayable receipt. This experiment adds **version 2, exclusively for six influences** without weakening or silently modifying v1.

**Wire schema:** `schemas/rt-route-stream-v2-p6.json`. **Executable:** `experiments/rt/event_stream_v2_p6.py`.

Each spec explicitly identifies exactly six F5^8 affine transformations of the form:

```
U_i(x) = x + (1 + gain_i*x[probe_i])*offset_i + x[probe_i]*shear_i
```

Each transformation has fully specified field-coordinate vectors, gain and probe. The spec has an exact `semantics` version, initial state, `direction_rank` of 1 or 2, and a **sorted set of allowable spread values**, never an ordering/threshold on F5.

The envelope includes `schema_version=rt-route-stream/v2-p6`, embedded specification and digest, either complete `all` or sorted explicit adjacent-swap requests, the exact prefix-state and both-order effect records, direction/spread/residual vectors, separate geometric/effect/admission bits, a records digest, and a derived summary.

## Replay trust boundary

`verify_receipt(payload_bytes, expected_spec_sha256, requested_faces=(), max_cells=None)` requires the **expected program pin to originate outside the receipt**. The verifier rejects malformed field coordinates, wrong cardinality, unknown update language, noncanonical request ordering, modified records even if the attacker recomputes their record checksum, and an otherwise internally consistent but independently unpinned program.

The verifier independently executes each swap at its actual shared prefix and checks full vectors, not `Q(residual)` or merely the final effect after a possibly collapsing suffix. When a P6 face is requested, it constructs only the needed signed boundary closure, checks exact `∂²=0`, and admits it only if every recursively required swap is computationally equal **and** geometrically allowed. A requested-only receipt has no global-top-cell authority.

A SHA-256 digest is an integrity fingerprint and conditional pin, **not** an origin signature; interpreter code identity, authenticated receipts, transport, privacy and real optimizer state are outside this fixture.

## Bounded acceptance comparisons

| Exact F5 experiment | Swaps examined | Geometric passes | Effect-certified swaps | Effect-negative |
| --- | ---: | ---: | ---: | ---: |
| Six frozen affine translations | 1800 | 1800 | **1800** | 0 |
| Scalar-coupled state-dependent update | 1800 | 1800 | **1680** | 120 |
| Nonzero-null effect defect | 1800 | 1800 | **1680** | 120 |
| Four externally requested P6 square-boundary edges | 4 | 4 | 4 | 0 |

The null-defect case has **120 nonzero residual vectors of zero quadratic norm**; no residual can pass by checking its norm alone. An independently pinned rank-two, full-swap receipt can admit the 5-dimensional P6 top cell and its **(720,1800,1560,540,62,1)** signed closure; four requested square edges can admit their **(4,4,1,0,0,0)** closure but never the top cell.

These are **bounded expected contract outcomes** to be checked by hosted regression, not a general algebraic theorem or a random/sample survey.

## Reproduction

```sh
python -m experiments.rt.event_stream_v2_p6
python -m unittest discover -s tests -p 'test_rt_event_stream_v2_p6.py' -v
```

For external receipts, independently acquire/pin `expected_spec_sha256` before loading the receipt. Supply that pin explicitly to the replay API; never extract it from the untrusted same envelope.

## Explicit nonclaims and follow-on obligations

- **v1 unchanged.** It still rejects six-event specifications.
- **No general k/R.** Coherence labels fixed at six, geometry rank limited to 1 or 2, and finite P6 cell dimension five. Sparse materialization is a distinct budget.
- **No real-training bridge.** An F5 update experiment does not prove an abstraction relation to float optimizers, LLM weights or stochastic model behavior.
- **No authenticated provenance.** SHA-256 is not a signature. Independent interpreter verification and adversarial limits beyond bounded input are distinct tasks.
- **No incremental streaming transport.** An envelope may include all 1800 records in memory, even if only a subset is requested; subsequent streaming transport must preserve canonical framing and independent replay.

Next proof/computation obligations: version independently replayable, bounded streaming chunks with sequence/coverage commitments; prove replay composition over chunks; add complete optimizer/RNG state to each transition; and only then research sound exact abstraction of finite hardware arithmetic.
