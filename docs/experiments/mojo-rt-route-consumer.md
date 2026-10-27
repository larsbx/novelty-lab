# Pinned native RT route consumer — 2026-10-27

Consumer increment for [issue #52](https://github.com/larsbx/novelty-lab/issues/52),
limited to accepted upstream [#84](https://github.com/larsbx/finite-math-kernels/pull/84)
at `3bb94d317b8f0712591b33f9657cf3a0e54207cd`.

This reuses the reviewed bounded experiment and literature decisions in
`docs/literature/rt-route-stream-replay-2026-10-26.md` and
`docs/literature/rank-lift-route-complexes-2026-10-26.md`. It adds differential
consumer acceptance for that contract, not a new theorem-facing diagnostic
or promoted lemma.

## Reproduction and evidence

```sh
python -m unittest discover -s tests -p 'test_mojo_rt*estate.py' -v
scripts/verify_all.sh python
pixi run --manifest-path experiments/rt/pixi.toml conformance
```

The native `routes` task builds `route_smoke.mojo` once in a temporary directory,
then checks four Python-oracle cases. Each checks all 720 route endpoints and
1,800 unique canonically oriented adjacent swaps, including prefix-local
residuals, geometry and operational admission. The shared arithmetic is
exclusively vendored Mojo; the Python fixture adapter calls existing oracles.

Local source audit: **37/37** vendored files byte-identical to their immutable
upstream revisions, including the unchanged historical policy packages.
The new RT route source and its selected dependencies come only from #84's
merge. Re-running supported pin/digest tools checks recorded source identity.

Local execution on October 27:

| Gate | Observed result |
| --- | --- |
| Full `scripts/verify_all.sh python` | all gates passed: registries, vendor/estate pins, generated ledger, governance/coverage, unit suite, all census checks/replays and paper tables |
| Focused RT/Gram/route tests | 8 tests passed |
| Focused Python route consumer tests | 4 tests passed, including CLI execution from Pixi's working directory |
| Pinned native Pixi `conformance` | passed: prior 48 scalar vectors, 18 batch expectations, Gram/reflection/MAX smoke, and the route comparisons below |
| Native route cases | all 720 endpoints and 1,800 swaps per case passed for rank-one translations, scalar coupling, null defect and rank-two translations |
| Native refusal checks | altered residual, prefix, admission; duplicated context; truncated fixture all refused |
| TLC | both `MCNoveltyLedgerImports` and `MCNoveltyLedgerOpen` passed using v1.7.4 with the workflow's verified SHA-256 |
| Lean locally | skipped: `lake` unavailable; hosted Lean required before merge |

Both state-dependent rank-one cases produced 1,800 geometric passes but only
1,680 equal effects and admissions. The null-defect case had exactly 120
nonzero norm-zero residuals, all refused. Both translation cases admitted all
1,800 swaps. These are native results matching each row of the existing Python
oracle, not just matching aggregate expectations.

The first local compiler invocation was blocked by automatic review because of
toolchain telemetry. Verification completed with the compiler's documented
`MODULAR_TELEMETRY_ENABLED=0` opt-out, now set in the Pixi environment for local
and hosted runs. This changes no mathematical or acceptance guard.

## Remaining integration requirements (issue #52 stays open)

- Accept upstream #85 separately with its own actual CI evidence, then select
  immutable source modules and dependencies and regenerate consumer pins.
- Compare native P3/P4/P5/P6 signed integer incidences against existing Python;
  check sparse nine-cell square closure, exact `boundary²=0` and P6 f-vector
  `(720,1800,1560,540,62,1)`. P6 has dimension five; the six-additive cube has
  dimension six.
- Integrate higher-cell admission only with independently replayed exact
  prefix-local edge equality and recursively closed signed boundaries.
- If porting receipts, specify a separate canonical encoding and transport
  contract and add actual Mojo executables/tests for JSON, SHA-256, trusted
  program pins, chunk linking/seals and bounded streaming. Current v1/v2
  receipts and chunk transport remain consumer Python code.
- Continue to distinguish arithmetic conformance, compiled execution, Lean
  support, TLC dependency models and mathematical proof. No optimizer or
  real-valued training soundness follows from this bounded finite-field run.

No ledger claim, proof status or authority plane changes in this increment.
