# Pinned Mojo rational-trigonometry kernels from the estate

**Scope:** reusable exact split-eight-space rational trigonometry. **Status:** immutable source snapshot vendored for code reuse; consumer verification depends on GitHub CI. No research claim is promoted.

**Source:** `larsbx/finite-math-kernels`, merged [PR #78](https://github.com/larsbx/finite-math-kernels/pull/78), immutable commit `194780a6d314c972c7d066d3da2cae8e21231cba`.

## Authority boundary

Reusable exact finite-field, tensor and projective mathematics is **Mojo-owned in finite-math-kernels**. This repository must not maintain a second generalized field-operations implementation. In this consumer:

- `vendor/mojo/finite_exact` supplies `ExactField`, `FpField[p]` and their exact number substrate;
- `vendor/mojo/projective_limits` supplies hyperbolic norm/polarization, guarded spreads, reflections, one-inversion spread batches and their scalar reference path;
- `vendor/mojo/parallel_fold` supplies MAX's deterministic CPU-thread-pool map-fold used by the exact shell census;
- `experiments/rt/independent_reference.py` is a **non-authoritative Python oracle**, not the canonical mathematical implementation;
- `tests/fixtures/hyperbolic_rt_v1.txt` is byte-identical to the upstream 48-case corpus at the pinned source commit; `tests/test_mojo_rt_estate.py` checks its SHA and replays every row through the independent Python oracle.

Only selected named modules and their transitive dependencies are vendored, not the upstream repository's entire implementation or CI toolchain. Each copied byte is SHA-256 pinned in `vendored.toml`. The existing Python policy and proof-record packages retain their earlier pins; new Mojo packages are all sourced from the single immutable revision above. The combined estate digest is derived by `tools/estate_pins.py` and checked in CI.

## Algorithm contract

The shared upstream source carries named theorem/guard statements and exact conformance:
- split hyperbolic norm \(N(x)=2\sum_{i=0}^{3}x_ix_{i+4}\) and doubled polarization;
- projective spread \(s=1-B_2(x,y)^2/[4N(x)N(y)]\), defined only for non-null rays;
- at most two guarded orthogonal reflections to transport vectors of equal nonzero norm;
- one-inversion exact batch spread using Montgomery's prefix/backward trick;
- deterministic MAX-backed CPU enumeration of norm-one shells: \(q^3(q^4-1)\) elements for the nonzero shell in the split eight-space.

The upstream implementation has a focused Mojo/MAX CI suite, full CI and independent dataset checks at its release commit. It makes **no** float/GPU numerical approximation or new-theorem/novelty claim.

## Consumer conformance and limits

The native Mojo code is made available as a reproducible source dependency under `vendor/mojo`. It is **not yet executed from novelty-lab's own CI** (which is Python/Lean/TLA+ based). Native Mojo computation and performance remain independently CI-checked upstream, not implicitly certified by the consumer's Python tests.

`scripts/verify_all.sh python` checks vendored digests, derived estate pin, local Python tests and the 48-vector replay. It does **not** assert independent Lean proofs of the classical formulas, or performance improvements beyond the proved arithmetic operation counts. Python's existing consumer certificate-acceptance authority is unchanged; an estate decision record would be required to change it.

## Future extensions without duplicate kernels

For Grassmannians, Aschbacher geometric subgroups, tensor stabilizers, Cayley multiplication and spread-controlled 2-complexes, first specify a narrow exact reusable mathematical primitive, implement it once **upstream in Mojo**, and add an independent downstream test/verification consumer only where needed. Existing N2 `cayley-dickson/v1` is deliberately not overwritten. A proposed new theorem requires a separate literature stop/go note before promotion.

**No manually maintained mathematical implementation is authoritative merely because it exists in this consumer.**
