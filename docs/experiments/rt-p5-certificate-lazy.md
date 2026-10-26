# Experiment VI — genuinely certificate-demanded P5 cell construction (2026-10-26)

**Status:** bounded, non-authoritative exact F5 consumer experiment; no theorem or mathematical novelty promotion. **Literature gate:** [p5-certificate-lazy-2026-10-26](../literature/p5-certificate-lazy-2026-10-26.md). The [full P5 experiment](rt-p5-full-coherence-comparison.md) is the independently constructed reference.

## Why this experiment

The earlier P5 prototype computed its entire 541-cell finite polytope (120 vertices, 240 edges, 150 two-faces, 30 three-faces, 1 four-cell) and **then** selected a requested closure. That was sparse selection, not actual on-demand construction. This experiment corrects the representation: a consumer only requests specific ordered-partition faces and recursively constructs those faces plus the signed codimension-one boundary closure. It reuses the **existing** exact `facets`, `incidence`, and finite-field receipt replay functions rather than creating a competing mathematical kernel.

A bounded, atomic cache refuses any request exceeding `max_cells`; a rejected request leaves both cached cells and incidence-computation counter unchanged. Repeating a request performs zero additional incidence calculations. The code separately computes exact integer `∂²` cancellation for *every instantiated cell* and compares each signed boundary against the existing eagerly constructed P5 oracle.

## Representative deterministic counts

| Request | Instantiated vertices | Edges | 2-faces | 3-faces | 4-cells | Total cells |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| One square | 4 | 4 | 1 | 0 | 0 | **9** |
| One hexagon | 6 | 6 | 1 | 0 | 0 | **13** |
| One P4 facet | 24 | 36 | 14 | 1 | 0 | **75** |
| One hexagonal-prism facet | 12 | 18 | 8 | 1 | 0 | **39** |
| Full P5 top | 120 | 240 | 150 | 30 | 1 | **541** |

A standalone square therefore requires constructing only 9 of 541 possible P5 cells, a **60.1× fewer cells** representation comparison for that demand. This is a deterministic materialization-count reduction, **not** a measured CPU or memory speedup and not a claim that the complete P5 is cheaper: its top-cell request correctly instantiates the whole 541-cell closure.

## Three independent contracts

1. **Geometry:** a declared finite-field spread predicate allows or forbids the observed update directions.
2. **Computation:** the source receipt verifier independently replays the update program, the actual shared-prefix state and both update orders, requiring **exact whole-vector effect equality**.
3. **Topology:** a higher ordered-partition face is promoted only if **each** lower facet is admitted; the cell never appears without its full boundary.

The caller must provide the expected update-specification SHA-256 from outside the untrusted receipt. Receipt hashes are integrity checks, not signatures. The verifier runs **before** materializing faces. A partial receipt cannot authorize the global P5 top cell, even if the target would be present as a combinatorial object.

Coherence rank remains 5, top CW dimension 4, RT tensor-direction rank is independently 1 or 2, and the cell/materialization budget is independent of all three.

## Reproduce

```sh
python -m experiments.rt.p5_certificate_lazy
python -m unittest discover -s tests -p 'test_rt_p5_certificate_lazy.py' -v
```

The eight new conformance tests check exact closure counts, independent eager/lazy oriented incidence equality, integer differential cancellation, atomic budget failure, cache reuse, forged/untrusted program pin refusal, full translations accepting P5, state-coupled/null-defect updates rejecting P5, and sparse receipt nonpromotion. These are exact finite-domain consumer checks, not a theorem proof over arbitrary fields.

## Limitations and next steps

- This is a **P5-bounded** consumer face constructor, not a generic unbounded rank-R topology kernel and not an upstream Mojo primitive. An independent upstream math-kernel interface and provenance pin would be required for production reuse.
- It performs on-demand **face incidence**, but the existing receipt format still generates all requested swap records in memory before serialization; genuine incremental transport/verification, signature authority, and quota-safe streaming remain distinct tasks.
- No probabilistic route selection, no LLM training data, no semantic float-vs-modular proof, and no convergence or model-quality result.
- Scaling the construction to P6 or larger should follow a fixed-budget experiment with an independent incidence oracle. It must not be conflated with increasing Grassmann tensor rank or automatically filling a general braid cell.
