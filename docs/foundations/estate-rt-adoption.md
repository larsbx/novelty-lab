# Estate integration: split quadratic RT

**Status:** integration staged; **not adopted as a pinned dependency yet**.  
**Upstream owner:** [finite-math-kernels PR #78](https://github.com/larsbx/finite-math-kernels/pull/78), `feature/quadratic-rt-8d-exact`.  
**Consumer foundation:** [novelty-lab PR #38](https://github.com/larsbx/novelty-lab/pull/38), merged.  
**Policy:** `AGENTS.md`, `ARCHITECTURE.md`, `vendored.toml`, `ESTATE.toml`. Do not hand-edit pinned vendor copies or claim a passing Mojo gate without its CI result.

## Authority and code-reuse boundary

The estate already provides the canonical exact arithmetic and projective rational-trigonometry machinery, rather than starting from a new finite-field arithmetic implementation:

| Mathematical dependency | Shared owner / API | Consumer status |
| --- | --- | --- |
| Prime fields, canonical residue and checked scalar inverse | `finite-math-kernels/kernel/finite_exact/fp.mojo`: `Fp[p]`, `FpField[p]` | Existing shared kernel; Mojo-pinned upstream |
| Exact field abstraction (also \(\mathbb Q\)) | `finite_exact.field.ExactField`, `QField` | Existing shared kernel |
| Projective points with rejected \([0:0]\) and zero-denominator refusal | `projective_limits.line.P1Over` | Existing shared projective machinery, specialized to \(\mathbb P^1\) |
| Rotor spread, projective group laws, spread polynomials | `projective_limits.rotor`, `projective_limits.spread_polynomial` | Existing shared 2D RT |
| Split eight-space norm, doubled polarization, guarded projective spread, reflections and norm-shell transport | `projective_limits.hyperbolic_rt` | **Proposed shared kernel in upstream PR #78**; not yet merged/vendor-pinned |
| Cayley multiplication and defect witnesses | `experiments/n2/defect_census.py` + repository N2 pinned `cayley-dickson/v1` | Existing independent N2 model; not superseded by quadratic RT |

The existing local `kernel/rt_foundations.py` was introduced before identifying the upstream extension point. It is a **temporary consumer-specific Python conformance implementation**, not an estate-owned reusable numeric primitive. It must not be generalized as a competing field library or presented as if it calls the shared Mojo implementation. When upstream PR #78 has passing tests and a pinned version, the consumer must reclassify or remove the duplicate quadratic arithmetic under a **separate boundary-first PR**, maintaining the tests as independent Python differential oracles if needed. Because `AGENTS.md` currently assigns Python the consumer's canonical acceptance role and Mojo no role here, any change to *acceptance authority* needs the repository's decision-record process; importing a shared computational oracle alone cannot silently change this policy.

## Adoption gates (fail closed)

1. **Upstream validation:** run and pass the pinned Mojo suite `pixi run test-projective-limits`, including `test_hyperbolic_rt.mojo`; independently review its field-generic boundary. Tests over F3/F5/F7 and the F3 norm-one shell check implementation conformance only.
2. **Cross-language conformance:** pin a published set of exact contract vectors (valid rays, null rays, two-reflection exceptional cases, planar triple spread and the independent 8D counterexample), and compare shared Mojo with an independent Python oracle. Do not derive expected values from the same implementation.
3. **Vendor with provenance:** use `vendor/vendoring/check_vendored_sync.py` and the existing estate `tools/estate_pins.py` generator. Never hand-edit vendored files, pinned digests, or a generated surface. The shared Mojo package's transitive imports (`finite_exact.field`, `finite_exact.fp`, `finite_exact.rat_q`, etc.) must be vendored consistently.
4. **Decide consumer authority:** `novelty-lab` is presently Python canonical, Lean/TLA+ supporting; an external Mojo runtime is not automatically a replacement for Python acceptance. An upstream field kernel may be a pinned, independently tested **oracle** without changing the existing governance.
5. **Remove duplicate authority:** after cross-checks, keep at most an explicitly labelled independent Python oracle or a thin adapter. No locally replicated group-wide finite field arithmetic, projective spread polynomial engine, or unguarded inverse.
6. **Run full verification:** `scripts/verify_all.sh`, estate audit and the upstream Mojo gate; record PASS/FAIL/SKIP without interpreting a skip as a pass.

## Scope and non-promotions

This integration does **not** establish new RT, Moufang, Artin, tensor, Aschbacher or spread-complex theorems, nor prove novelty. No N1–N5 ledger or N2 candidate status changes. The research extensions remain dossier-level questions. A field-generic polynomial identity must still be proved symbolically; finite-field enumeration alone cannot certify it.

## Recommended next edit after upstream passes

- Pin `projective_limits.hyperbolic_rt` at the accepted immutable upstream commit and add contract vectors.
- Reconcile the temporary Python kernel with the common exact arithmetic boundary while preserving independent oracle testability.
- Delete or demote redundant primitive implementations in a narrowly scoped follow-up, without changing generated files or claim status.
