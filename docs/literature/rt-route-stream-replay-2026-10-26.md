# Canonical external RT-route receipt replay — bounded literature gate (2026-10-26)

**Decision: proceed with a narrowed consumer experiment**, not a theorem or novel trace theory.

## 1. Question and scope
After the state-dependent P4 swap-audit experiment, can independently supplied, canonical JSON receipts be replayed against a **separately pinned exact update specification** while keeping (i) geometric spread eligibility, (ii) whole-vector effect equality, (iii) coherence-cell admission, and (iv) materialization budget separate? Test 3–5 influences over the existing split F5^8 oracle. No general P5 cellular 3/4-faces and no proof about floating-point training.

## 2. Primary sources and closest prior art

Sources below follow the dated verification of the prior gate `docs/literature/state-dependent-rt-coherence-2026-10-26.md`. Their original complete proofs were **not re-read for this note**, and the comparison is bounded.

| Source | Locator | Transfer / boundary |
| --- | --- | --- |
| A. Mazurkiewicz, *Concurrent Program Schemes and their Interpretations* (1977) | DAIMI PB-78, abstract/publication record, https://doi.org/10.7146/dpb.v6i78.7691 | Classical trace reordering requires valid independence. Geometric agreement does not create independence. |
| I. J. J. Aalbersberg and G. Rozenberg, *Theory of traces* (1988) | TCS 60(1), pp. 1–82, https://doi.org/10.1016/0304-3975(88)90051-5 | Global partial commutation differs from prefix-dependent tested effects. |
| P. Godefroid, *Partial-Order Methods for the Verification of Concurrent Systems* (1996) | LNCS 1032, chapters 3–4, https://doi.org/10.1007/3-540-60761-7 | This experiment exhaustively checks up to 5! routes rather than asserting a complete partial-order-reduction algorithm. |
| A. Postnikov, *Permutohedra, Associahedra, and Beyond* (2009) | Propositions 2.5–2.6, https://math.mit.edu/~apost/papers/permutohedron_full.pdf | The P4 face poset is imported from the preceding local experiment. No general P5 face incidence is implemented. |
| N. J. Wildberger, *Rational Trigonometry in Higher Dimensions and a Diagonal Rule* (2017) | Theorems 4–5, prior RT foundation literature gate | Spread is guarded. No unrestricted triple-spread or metric claim in high dimensions. |

## 3. Terminology and hypotheses

A **trusted pin** is the expected SHA-256 digest of the update specification, supplied **independently** to the verifier. A receipt digest is an integrity checksum, **not** a signature or proof of origin. A **complete trace** enumerates all adjacent swap edges for a bounded n=3,4,5; a **requested-only** trace certifies strictly its listed edges. Shape rank (n), tensor direction rank (1 or 2), and materialization policy are orthogonal.

The program is an explicit, finite linear-affine update vocabulary `U_i(x)=x+(1+g_i x[p_i]) b_i+x[p_i]h_i` on F5^8. No arbitrary executable code is accepted as a receipt. Every local pair replays at the *actual shared prefix*, before any shared suffix. For n=4 only, existing P4 face boundaries may be promoted when all boundary edges are certified. For n=5, no higher faces are claimed.

## 4. Falsifiers and negative controls

- Two modes, all geometric spread gates pass but the state-dependent mode has nonzero exact swap residuals.
- A null yet nonzero residual vector must not count as zero effect.
- A forged residual still fails even if a malicious producer recomputes the receipt digest.
- Altering the program and recomputing **both** receipt and program hashes must fail against the independent trusted pin.
- Noncanonical JSON, unsupported field, duplicate/unsorted requests, incomplete complete traces, bogus summaries, bad frame guards, and malformed update specifications fail closed.
- Sparse requested edges may admit a single P4 face but never the P4 top cell without full boundary closure.
- No claim about actual training traces, signed provenance, probabilistic correctness, or equivalence under floating/quantized projection.

## 5. Decision

**Proceed, narrowed** to a versioned `schemas/rt-route-stream-v1.json`, a non-authoritative `experiments/rt/event_stream_v1.py`, contract-labelled deterministic tests, and a report. No edits to `kernel/`, `vendor/`, generated ledgers, or theorem status. Run repository full CI; merging without full check completion must not be represented as evidence of that check.
