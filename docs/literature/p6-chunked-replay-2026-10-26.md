# Chunked P6 certificate replay — bounded literature gate (2026-10-26)

**Decision: proceed with a narrowed experiment.** Extend the merged six-event `rt-route-stream/v2-p6` *whole-envelope* receipt into a separately versioned, **incremental** frame protocol. The target is exact bounded validation with early rejection, canonical sequence/coverage commitments and a terminal seal; it is **not** authenticated transport, a formal streaming proof or a neural-training audit.

## 1. Proposed experiment and finite scope

Accept six declared deterministic F5^8 affine update operations (the established `F5-affine-vector-update/v1` language). Encode one canonical header, at most 1800 adjacent-swap records distributed into groups of 1–32, then a terminal seal. Bind successive chunks by SHA-256 digests over canonical compact-ASCII-JSON records, with the first predecessor the header digest. A verifier receives *bytes incrementally* and **recomputes** every candidate edge at its actual prefix against an independently supplied trusted update-specification SHA-256. It rejects missing/duplicated/reordered/out-of-scope chunks and does not emit an accepted global result until a valid terminal seal and true end-of-stream.

Optional requested P6 cells may be constructed **after** sealed receipt verification, and admitted only from individually checked geometric-and-semantic swap edges. The source already has a genuinely lazy ordered-partition P6 cell constructor. The representation budget (max frames, max bytes, per-chunk size, face-cell cap) is independent of the coherence rank and tensor-direction rank.

## 2. Primary prior art / standards (read 2026-10-26)

| Source | Relevant location and what was consulted | Boundary here |
| --- | --- | --- |
| N. Williams, RFC 7464, *JSON Text Sequences* (2015) | §§1–3, https://www.rfc-editor.org/rfc/rfc7464 | The standard uses **RS 0x1e + JSON + LF**, unlike this **custom canonical JSON-line** protocol. Do **not** claim RFC 7464 conformance. Its §3 notes sequence parsing/canonicalization ambiguities, motivating exact byte re-encoding. |
| B. Laurie et al., RFC 9162, *Certificate Transparency Version 2.0* (2021) | §2.1 Merkle trees and §4 log format, https://www.rfc-editor.org/rfc/rfc9162 | CT uses Merkle consistency and signed timestamps. This pilot uses only a **linear SHA-256 hash chain**; it provides neither CT append-only transparency proofs nor signatures/author identity. |
| A. Mazurkiewicz, *Concurrent Program Schemes and Their Interpretations* (1977) | DAIMI PB-78, publication abstract, https://doi.org/10.7146/dpb.v6i78.7691 | Classical trace-reordering independence is a semantic hypothesis. A passed RT spread gate is *not* a proof that two update orders commute. |
| A. Hatcher, *Algebraic Topology* (2002) | §2.2 cellular homology; earlier dated P6 gate, https://pi.math.cornell.edu/~hatcher/AT/AT-doublepage.pdf | Certified P6 cell filling is separate from transport integrity; classical chain boundary identities are not claimed new. |

Previous bounded gate: `docs/literature/p6-receipt-v2-2026-10-26.md`. This is literature clearance, not a priority search, complete independent proof review or novelty finding.

## 3. Hypotheses, trust assumptions, falsifiers

- Header pins exactly the same update semantics/coordinate guards as `rt-route-stream/v2-p6`. The caller provides `expected_spec_sha256` **independently** from the untrusted stream.
- Serialized bytes: **one canonical ASCII JSON object plus terminal LF per frame**, sorted keys and compact separators. The stream format is custom `rt-route-chunks/v1-p6`; it is **not** RFC 7464, JSON Lines standardization, a transport session, or the existing `rt-route-stream/v2-p6` full envelope.
- Each chunk carries a strict sequence number, prior hash, a bounded record list and the digest of its own canonical content. The terminal seal covers the final hash, exact chunk and edge totals, and independently accumulated verdict counts. Reordering, omission, duplication, truncation, extra frames, malformed frames, forged residuals with recomputed chain digests, invalid trusted pin and over-budget input must all fail.
- **No provisional acceptance:** a verifier may compute in bounded memory but returns no verdict until it sees the correctly linked terminal seal **and EOF**. An empty requested-only audit is allowed but must not be presented as complete.
- Only after verified closure may the consumer request a P6 face and its signed boundary closure. A four-edge requested-only receipt may authorize its particular square; it must never authorize the full P6 top cell. Geometry is necessary but not sufficient: complete **vector effect equality** is separately checked at each shared prefix.
- Lower-level operation identity, binary provenance, Ed25519/HMAC keys, authenticated sender, replay-nonce freshness, hardware optimizer state, probabilistic route distribution and sound finite-field abstraction of floating-point training are **not established**.

## 4. Decision

**Proceed with a narrowed consumer experiment**, adding `experiments/rt/chunked_replay_p6.py`, contract-labelled deterministic tests and a dated experiment report. No modification to v1/v2 envelope or schema, shared finite-math kernels, vendored files, the claim ledger, or generated surfaces. Fail closed if hosted checks disagree. Promotion to an authenticated streaming protocol would require explicit key/identity, application replay protection and bounded delivery-state contracts.
