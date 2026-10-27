# Pinned Mojo rational-trigonometry kernels from the estate

**Scope:** reusable exact split-eight-space rational trigonometry. **Status:** immutable source snapshot vendored for code reuse; see the dated consumer evidence below. No research claim is promoted.

**Current Mojo source:** `larsbx/finite-math-kernels`, merged [PR #84](https://github.com/larsbx/finite-math-kernels/pull/84), immutable commit `3bb94d317b8f0712591b33f9657cf3a0e54207cd`. Earlier release reviews below retain their historical pins.

## Authority boundary

Reusable exact finite-field, tensor and projective mathematics is **Mojo-owned in finite-math-kernels**. This repository must not maintain a second generalized field-operations implementation. In this consumer:

- `vendor/mojo/finite_exact` supplies `ExactField`, `FpField[p]` and their exact number substrate;
- `vendor/mojo/projective_limits` supplies hyperbolic norm/polarization, guarded spreads, reflections, one-inversion spread batches and their scalar reference path;
- `vendor/mojo/projective_limits/rt_route.mojo` supplies affine eight-vector steps, whole-vector swap residual/equality, guarded ray/rank-two geometry and prefix-local certificate admission;
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

The native Mojo code is a reproducible source dependency under `vendor/mojo`. A separate **Mojo/MAX consumer CI** workflow uses the isolated toolchain manifest `experiments/rt/pixi.toml` (matching the source revision's compiler/MAX versions). Run its complete native gate with:

```sh
pixi run --manifest-path experiments/rt/pixi.toml conformance
```

`experiments/rt/replay_vectors.mojo` checks all 48 fixture rows directly against the vendored scalar operations, then checks all 18 spread rows against the batched implementation, including null-lane refusals. The replay requires 16 rows per prime (3, 5 and 7), checks each operation's row shape, and refuses unknown primes, unknown operations, incorrect results and incomplete corpora. It contains fixture decoding and assertions, with no local mathematical implementation. `experiments/rt/smoke.mojo` additionally executes reflection transport and the MAX CPU shell census. The workflow replays the same immutable fixture through the independent Python oracle before running native conformance, and changes to either the fixture or its consumers trigger it.

These observed results are separate from Python/Lean/TLA proof-state gates; finite conformance is not a field-generic mathematical proof.

`scripts/verify_all.sh python` checks vendored digests, derived estate pin, local Python tests and the 48-vector replay. It does **not** assert independent Lean proofs of the classical formulas, or performance improvements beyond the proved arithmetic operation counts. Python's existing consumer certificate-acceptance authority is unchanged; an estate decision record would be required to change it.

## October 24 source and integration review

Upstream PR #78 and consumer PRs #39 and #40 are already merged. The reviewed upstream release is `194780a6d314c972c7d066d3da2cae8e21231cba`, whose PR integration head `954abe57593858fde4df8987024c1da106002fc1` passed all four upstream workflows. PR #40's final head passed the consumer Python, Lean, TLC, estate policy and Mojo/MAX workflows. This supersedes their earlier descriptions of checks still running.

The source audit compared all 35 vendored files with their recorded immutable upstream revisions, including the historical Python governance packages. Each was byte-identical. The fixture also matched its upstream bytes. Running the existing vendoring checker and `tools/estate_pins.py --write` reproduced the committed digests without changes; there is no reason to move the accepted pin merely to repeat the integration.

The mathematical source review checked the following under the documented characteristic-not-two hypothesis:

- The doubled pairing is exactly `N(x+y)-N(x)-N(y)`; the spread ratio is invariant under nonzero rescaling of either ray.
- Expanding `N(x-t*a)` with `t=B2(x,a)/N(a)` gives the reflection isometry. For equal nonzero norms `c`, the exceptional transport case has `N(x+v)=4*c`, so both reflection normals used there are non-null.
- A nonzero first four-coordinate block defines a surjective linear functional with `q^3` elements per fiber, giving the shell cardinality `q^3*(q^4-1)`.
- The backward batch-inversion invariant recovers each reciprocal from one inversion of the prefix product. Null lanes use neutral denominators internally and remain rejected outputs.
- Prime-field residues are reduced at every operation, with modulus below `2^31`, so residue products fit in signed 64-bit arithmetic. The MAX census caps its inputs at one million, making its integer counts exact and independent of worker partition.

This is an agent source review of classical derivations and implementation contracts, not a recorded independent proof review or a claim-ledger promotion. Algorithmic operation-count savings, exact finite computation, mathematical proof and measured performance remain separate evidence classes. No benchmark or GPU acceleration is established.

The integration audit found that PR #40's native consumer gate exercised only a small smoke, while all 48 vectors ran only through Python in this repository. The direct native replay above closes that coverage gap. Local execution passed the 48 scalar rows, the 18 batch expectations and the MAX smoke; a compiled replay also refused fixtures with a wrong expected value, an unknown prime, or a missing row. The committed fixture was not modified for these negative checks.

## Future extensions without duplicate kernels

For Grassmannians, Aschbacher geometric subgroups, tensor stabilizers, Cayley multiplication and spread-controlled 2-complexes, first specify a narrow exact reusable mathematical primitive, implement it once **upstream in Mojo**, and add an independent downstream test/verification consumer only where needed. Existing N2 `cayley-dickson/v1` is deliberately not overwritten. A proposed new theorem requires a separate literature stop/go note before promotion.

**No manually maintained mathematical implementation is authoritative merely because it exists in this consumer.**

## Gram/exterior geometry extension (pinned)

The estate's [Gram geometry contract](https://github.com/larsbx/finite-math-kernels/blob/734f60a04a6cf8a68fab74367acc6b33d0e02cd9/docs/theorems/gram-minor-rt-contract.md) and exact `projective_limits.gram_geometry` module were introduced here at `734f60a04a6cf8a68fab74367acc6b33d0e02cd9`. The current pin above preserves those module bytes and the 18-case fixture unchanged.

The new reusable kernel supplies 2x2 and 3x3 Gram determinants, guarded normalized Gram ratios, and **56 coordinate 3-minors** to decide when three vectors lie in a genuine 2-plane, rather than incorrectly inferring planarity from a degenerate Gram matrix. The corpus `tests/fixtures/gram_geometry_v1.txt` is byte-identical to the upstream 18-case fixture and is replayed by the **independent** Python consumer test, while `experiments/rt/smoke.mojo` exercises the pinned Mojo implementation directly. It includes a non-planar 3-space with Gram determinant zero (isotropic radical) and a line tangent to the absolute whose ordinary two-reference-point cross-ratio is not defined.

No mathematical claim is promoted. The statement `Gram determinant zero ⇒ rank≤2` is **false** over the split form; the exterior-minor API is the faithful guard. The consumer retains its pre-existing claim governance and Cayley–Dickson model; the shared numerical implementation remains upstream in Mojo.

## October 27 RT route consumer increment

The three existing Mojo packages are re-pinned together at the accepted #84
merge. Only the public `projective_limits/rt_route.mojo` is added, with the
already selected transitive dependencies. Sources are copied from the commit,
re-pinned with `vendor/vendoring/check_vendored_sync.py pin`, and the estate
digest is regenerated with `tools/estate_pins.py --write`. No `finite_graph`
package or unmerged #85 source is imported. Historical Python policy package
pins remain as recorded.

`experiments/rt/route_vectors.py` adapts the **existing**
`event_stream_v2_p6.sample_spec` and `event_stream_v1.compute_record` oracle to
temporary differential fixtures. It adds no field arithmetic. The native
`route_smoke.mojo` replays each actual common prefix and calls upstream
`affine_step8`, `swap_residual8`, `swap_equal8`, ray/Gram spreads and
`certified_swap8`. It compares each eight-coordinate residual, spread and
admission against Python, and checks all 720 whole-route endpoints. Four
cases each exhaust all 1,800 adjacent swaps:

| Update model | Direction rank | Geometric passes | Exact equal effects / admitted | Nonzero null residuals |
| --- | ---: | ---: | ---: | ---: |
| translations | 1 | 1,800 | 1,800 | 0 |
| scalar_coupled | 1 | 1,800 | 1,680 | 0 |
| null_defect | 1 | 1,800 | 1,680 | 120 |
| translations | 2 | 1,800 | 1,800 | 0 |

These are the exact oracle expectations, checked by the Python tests; actual
native execution evidence is recorded in
[`docs/experiments/mojo-rt-route-consumer.md`](../experiments/mojo-rt-route-consumer.md).
The native gate also refuses altered prefix/residual/admission expectations,
duplicate contexts and truncated fixtures. Fixture bytes are temporary test
inputs, not a new canonical receipt encoding or an authenticated transport.

Run `pixi run --manifest-path experiments/rt/pixi.toml conformance` for the
native replay together with the prior vector and MAX shell gates. The existing
Mojo/MAX workflow runs all four-case comparisons and native negative checks;
the Python suite independently cross-checks fixture coverage and pilot census
agreement. Lean, TLC and estate-policy jobs continue to verify their existing
proof, dependency and provenance contracts; they do not thereby prove the
Mojo compiler or the geometry-to-effect implication.

Geometric admissibility alone never admits an operational edge. Exact
whole-vector equality at the actual prefix is also required. Higher cells
still require all signed boundary certificates, under the existing Python
consumer. P6 signed incidence, sparse square closure, full f-vector and
`boundary²=0` native integration remain separate tasks under issue #52 after
upstream #85 acceptance. Canonical JSON, SHA-256, chunk seals and receipt
replay remain Python-owned. No full P6 port, generic permutohedral theorem,
optimizer equivalence or finite-field-to-real training result is asserted.
