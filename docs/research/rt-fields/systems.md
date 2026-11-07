# Systems/security packet S1 — replay versus recalculated digest

**Authority:** bounded, non-authoritative consumer research in `experiments/rt/field_pilots/`; original cross-disciplinary partition [here](../../surveys/fields/README.md). **Literature stop/go:** [bounded field-pilot gate](../../literature/rt-field-bounded-pilots-2026-10-28.md). **Governance:** `AGENTS.md`, `docs/calibration.md`, `docs/verification.md`. No novelty/theorem/status promotion.

**Question:** Will a forged certificate that lies about an isotropic-but-nonzero swap residual pass the existing independent replay verifier? It must not.

**Object:** an existing `F5^8` null-defect P4 swap certificate, selected deterministically from the 36 contexts, then mutated by setting the nonzero residual to the zero vector and changing effect booleans. SHA-256 is applied to a deterministic local JSON test representation of the certificate.

**Hypothesis/negative controls:** original certificate passes deterministic recomputation; forged certificate fails despite the attacker being able to calculate a completely valid SHA-256 digest of the forged bytes. The independently pinned original digest also differs. A 35-of-36 requested-only trace also passes replay for every included record but is rejected if asserted to be a *complete* P4 audit. A hash is not a signature and cannot attest trusted execution.

**Literature:** [RT route receipt replay gate](../../literature/rt-route-stream-replay-2026-10-26.md), [bounded field pilot gate](../../literature/rt-field-bounded-pilots-2026-10-28.md); NIST FIPS 180-4 provides the hash algorithm, not the claimed provenance model.

**Procedure:** `systems.run()` reuses the existing certified-swap interpreter and `verify_swap`. The JSON hash is **local test representation** only, not a new signed or canonical external receipt format.

**Reproduce:** `python -m experiments.rt.field_pilots` and `test_systems_reject_forged_receipt_even_if_hash_recalculated`.

**Claim ceiling:** two deterministic test receipts and a forged-data rejection; no adversarial security proof, no signed identity, no trusted-execution result.

**Next falsifier:** independently pinned external stream parser with complete request completeness, version fencing, altered-program and truncated-stream controls. Keep transport/authentication separate from numeric kernel correctness.
