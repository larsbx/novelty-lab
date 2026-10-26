# Experiment IX — incremental, hash-chained exact P6 route replay (2026-10-26)

**Status:** bounded consumer experiment, pending hosted acceptance. **Literature gate:** [P6 chunked replay](../literature/p6-chunked-replay-2026-10-26.md). Builds on the merged exact six-influence `rt-route-stream/v2-p6` receipt and the independently checked P6 signed-cell constructor.

## What changes, and what does not

Previous receipts were one canonical JSON object containing all 1800 swap records. The new **`rt-route-chunks/v1-p6`** format is a distinct streaming-oriented protocol: a canonical header, consecutive bounded chunks, and exactly one terminal seal, each its own **ASCII JSON object followed by LF**. It is **not** the RFC 7464 Record-Separator format, and it does not mutate or reinterpret the existing complete-envelope format.

- **Producer** `emit_frames(spec, requests="all", chunk_size=24)` yields frames rather than building an entire in-memory list of record objects. Chunk length must be an integer 1–32.
- **Verifier** `verify_frames(frames, expected_spec_sha256, requested_faces=(), max_cells=None)` consumes **one byte frame at a time**, exact-replaying its claimed prefix-state and both update orders from an independently pinned versioned six-event specification.
- Every chunk commits to its previous digest, sequence number and canonical list of records. The **header digest anchors** the chain to spec, complete/requested coverage, chunk size and expected count. The **seal** commits to the final chunk digest, exact totals and derived geometry/effect summary.
- A verifier returns an accepted result **only after the correct terminal seal and EOF**. Missing, extra, duplicated, reordered or truncated frames, a forged record with all chain hashes recomputed, an incorrect external spec pin, a lying summary, noncanonical JSON bytes or exceeded finite limits fail closed.
- A successful receipt is only **conditionally verified against a separately provided exact program pin**. SHA-256 neither signs it nor identifies its author. There is no replay-nonce freshness, channel authentication or fault-tolerant transport here.

Wire structural schema: `schemas/rt-route-chunks-v1-p6.json`. It reuses exact field-spec and event-record schema definitions from `schemas/rt-route-stream-v2-p6.json`; full replay supplies the stronger semantic validation.

## Independent parameters and budgets

| Parameter | Current finite pilot |
| --- | --- |
| Permutation coherence rank | 6 influence labels, exactly 720 word routes |
| Potential adjacent-swap edges | 1,800 |
| Highest P6 CW dimension | 5 |
| Direction rank | 1 non-null ray or 2-plane Gram ratio |
| Chunk cardinality | 1–32 exact records |
| Max frame bytes | 256,000 |
| Max cumulative bytes | 16,000,000 |
| Max frames | 1,802 (header + 1,800 one-record chunks + seal) |
| P6 materialization | Exact on-demand face closure with independent max-cells cap |

The verifier keeps only a current chunk of record dictionaries, a bounded canonical edge index and the admitted **edge IDs** needed to justify any later face. This is incremental **verification of records**, not a formal claim of constant memory independent of the bounded 1,800-edge universe. Record generation itself remains finitely bounded by the exact F5 toy program.

## Negative controls and intended exact fixture

| Mode | Edges examined | Geometric pass | Whole-vector admitted |
| --- | ---: | ---: | ---: |
| Frozen translations | 1,800 | 1,800 | 1,800 |
| State-coupled | 1,800 | 1,800 | 1,680 |
| Four requested frozen square-boundary swaps | 4 | 4 | 4 |
| Empty requested-only audit | 0 | 0 | 0 |

The state-dependent model has 120 **geometry-positive but computationally invalid** swaps. The complete frozen model should seal with **75 chunks** at chunk size 24, plus header and seal; coupled model should seal with **95 chunks** at chunk size 19. These are bounded regression expectations, not results about actual neural training.

A requested-only, four-edge receipt can independently certify exactly the requested P6 square and its 9-cell boundary closure, but can never certify the entire P6 top five-cell. All cells are admitted based on **complete, exact per-edge computational equality**, not on spread alone. Terminal seal correctness and chain linkage do not replace that effect check.

## Reproduce

From the repository root:

```sh
python -m experiments.rt.chunked_replay_p6
python -m unittest discover -s tests -p 'test_rt_p6_chunked_replay.py' -v
```

For real byte-frame input, use `verify_frames(iterable_of_bytes, trusted_sha256)`; the expected SHA-256 must come from a **trusted source outside the untrusted frames**. A result obtained without the valid seal plus EOF is neither complete nor accepted.

## Scope and next proof/computation obligations

This is an **exact bounded six-operation F5 experiment**. It does **not** certify a probabilistic optimizer, a real LLM computation, a model's numerical convergence, approximate-error bounds, or authorship. It does not provide Ed25519 signatures, hardware binding or durable multi-party audit logs. Transport-level timeouts, persistent checkpoints, replay/session nonces and signer trust policies are future separately gated work. No claim of cryptographic transparency or Merkle inclusion/consistency proof is made from a linear hash chain.
