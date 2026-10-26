# Experiment IV: canonical P4/P5 RT route streams and pinned replay (2026-10-26)

**Authority:** bounded experiment, non-authoritative. **Literature stop/go:** [rt-route-stream-replay](../literature/rt-route-stream-replay-2026-10-26.md). Builds on the merged [P4 state-dependent audit experiment](rt-state-dependent-coherence-pilot.md). No theorem, novelty, proof-record, or actual LLM correctness promotion.

## Narrowed question

Can an **external serialized receipt** be checked exactly against a *separately trusted update program digest* across a bounded family of coherence sizes and independent tensor-direction ranks? This consumer pilot implements the first **finite parameterized n=3..5 stream** with explicit local update effects and guarded RT spreads. The P4 face incidence is inherited from the preceding experiment; n=5 is an **edge-only** Cayley graph audit, **not** a constructed P5 CW complex.

### Orthogonal parameters

- **Influence/coherence rank:** n in {3,4,5}, with n! words; complete edge audit has n!(n-1)/2 adjacent-swap witnesses.
- **Direction rank:** 1 (guarded rays) or 2 (nondegenerate Grassmann 2-frames), chosen separately. Higher k needs its own upstream-owned exact kernel.
- **Materialization:** all edges, or a caller-selected canonical sorted list of edges. Requested-only receipts must not claim complete coverage.
- **Cell dimension:** only when n=4 are existing P4 two-faces/top 3-cell admitted, and only from *complete boundary certificates*. In n=5, no higher faces are claimed.

### Mathematical update contract

States are exact vectors in `F5^8` and need not be non-null. Each event `i` is declared by a canonical offset `b_i`, scalar gain `g_i`, probe index `p_i` and shear `h_i`:

```text
U_i(x) = x + (1 + g_i*x[p_i])*b_i + x[p_i]*h_i   in F5^8
```

Only the RT-observed **displacements** require non-null guards. The verifier checks both execution orders at the actual common prefix state. The proof obligation is **whole-vector equality**, not zero quadratic norm or matching projective spread.

### Certificate format

Wire schema: [schemas/rt-route-stream-v1.json](../../schemas/rt-route-stream-v1.json).
The receipt contains `schema_version`, exact `spec`, independently checkable `spec_sha256`, canonical requested edges (`all` or sorted edge pairs), every prefix and local endpoint, transported directions, spreads, residual vector, **separate geometry/effect/admission booleans**, a canonical `records_sha256`, and a derived summary. Canonical representation: ASCII JSON, keys sorted, compact separators, exactly one final LF; digest SHA-256 includes that LF.

**Trust boundary:** `verify_envelope(payload_bytes, expected_spec_sha256)` must be passed an **expected program digest from a source independent of the receipt**. It validates all input types/guards, the exact request set, reconstructs all records from the declared program, checks canonical serialization, verifies both digests, and independently checks full-route equality for each admitted local swap. An attacker who simply rewrites the JSON and recomputes receipt hash still fails replay. An attacker who changes the specification and its hash fails a separately trusted pin. **SHA-256 is neither a digital signature nor evidence of who authored a receipt.** No update authority, signature verification or remote identity system is implemented.

### Reproduction

```sh
python -m experiments.rt.event_stream_v1
python -m unittest discover -s tests -p 'test_rt_event_stream_v1.py' -v
```

For a saved receipt `receipt.json` and an expected SHA from a separate trusted record:

```python
from pathlib import Path
from experiments.rt.event_stream_v1 import verify_envelope

trusted_sha256 = "..."  # NEVER copy this from receipt.json
result = verify_envelope(Path("receipt.json").read_bytes(), trusted_sha256)
print(result)
```

### Bounded F5 observations (deterministic local replay)

| Experiment | Potential adjacent swaps | Geometric passes | Computationally admitted | Effect failures | Higher P4 filling |
| --- | ---: | ---: | ---: | ---: | --- |
| n=5 frozen translations | 240 | 240 | 240 | 0 | **not modeled** |
| n=5 state-coupled update | 240 | 240 | 216 | 24 | **not modeled** |
| n=5 null-vector effect defect | 240 | 240 | 216 | 24 | **not modeled** |
| n=4 translations, rank-2 directions | 36 | 36 | 36 | 0 | 14 faces; **admitted** |
| n=5 two requested swaps | 240 potential | 2 checked | 2 | 0 | **not modeled** |

A state-dependent update can keep transported directions projectively parallel (`spread=0`) while changing the actual endpoint. The null-defect control has **24 nonzero vector residuals with quadratic norm zero**. Sparse edge selection is a budget on evidence, not a mathematical limit on the lift.

### Known limits and follow-on work

This is an **independently replayed certificate of a bounded exact toy field model**, not a finite-field reduction of arbitrary float-based training. Nothing establishes LLM loss, convergence, stochastic route distribution, or approximate error bounds. The P5 complex (higher permutohedral faces, explicit `∂²=0`, higher-rank coherence) is **not** implemented here, just its adjacency graph and local effect checks. Production audit requires a pinned model specification, authenticated provenance separate from hashing, resource-safe batch streaming, kernel reuse through `finite-math-kernels`, and a sound abstraction relation for actual optimizer state.
