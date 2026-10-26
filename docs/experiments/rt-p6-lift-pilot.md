# Experiment VII — demanded P6 (six influences) and exact coherence comparison

**Date:** 2026-10-26. **Authority:** bounded, non-authoritative exact consumer experiment. **Literature gate:** [p6-lift-2026-10-26](../literature/p6-lift-2026-10-26.md). This extends the merged P5 certificate-demanded implementation without modifying shared finite-field kernels or claiming novelty.

## Constructed object

The complete permutation coherence object on six influences is the **five-dimensional permutohedron P6**, not a six-dimensional cell. Its (independently counted by Stirling recurrence and exactly instantiated) CW face vector is **(720,1800,1560,540,62,1)**, totaling 4683 cells. The different **six-dimensional additive cube** has vector **(64,192,240,160,60,12,1)**, totaling 729 cells. Coherence labels, CW dimension, tensor-direction rank and materialization budget remain orthogonal.

| Shape | Dimension | CW cells by dimension | Semantic interpretation |
| --- | ---: | --- | --- |
| P3 | 2 | 6,6,1 | Three-order permutohedral hexagon |
| P4 | 3 | 24,36,14,1 | Four-influence permutation coherence |
| P5 | 4 | 120,240,150,30,1 | Five-influence 4-cell |
| **P6** | **5** | **720,1800,1560,540,62,1** | Six-influence 5-cell |
| **Six-cube** | **6** | **64,192,240,160,60,12,1** | Frozen-additive subset coherence |

A face is an ordered partition of six labels; only its immediate block-splitting facets are generated, recursively. Signed boundaries use **exact integer** outward-first doubled-barycenter incidence with the orientation conventions of P5. The P6 routine reconstructs all **541 signed cells of a canonical P5 facet** and compares their coefficients against the independent existing P5 reference. It checks exact integer **∂(∂c)=0** for every materialized face, including the P6 top 5-cell. It computes **F5 cellular ranks/Betti** using the existing bounded exact rank oracle from the P5 consumer experiment rather than introducing a second shared arithmetic implementation.

## Actual on-demand construction

Unlike the eager P5 census followed by extraction, this constructor materializes **only** the cells required by a requested face and its recursively necessary boundaries, with an atomic `max_cells` cap.

| Demand | P6 cells instantiated | Relative to full 4683 |
| --- | ---: | ---: |
| Single square | **9** | 520.3× fewer cells |
| Single hexagon | **13** | 360.2× fewer cells |
| Single P5 facet | **541** | 8.66× fewer cells |
| Entire top | **4683** | No savings, as required |

A failed budget does not mutate the cache; a repeated request instantiates zero additional cells. These are **cell-count comparisons**, not memory or runtime benchmarks.

## Actual six-event state-dependent effect tests

A six-event deterministic internal F5^8 vocabulary is evaluated at every **shared prefix** of every **adjacent swap in all 720 permutations** (1800 distinct edges). There are six non-null directions; they are **not all mutually orthogonal**. At every edge, the geometric gate uses RT projective spread of the **transported update displacement** (rank 1 or guarded rank 2), while effect equality compares complete field vectors.

| Update mode | Geometric passes | Effect-equal edges | Admitted 2-faces | 3-faces | 4-faces | 5-cell |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Frozen translations | 1800 | **1800** | 1560 | 540 | 62 | **Yes** |
| Scalar state-coupled | 1800 | **1680** | 1320 | 390 | 32 | **No** |
| Nonzero null residual | 1800 | **1680** | 1320 | 390 | 32 | **No** |
| Frozen, Grassmann rank 2 | 1800 | **1800** | 1560 | 540 | 62 | **Yes** |

The state-dependent models have **120 geometry-positive but effect-invalid swaps**, removing 240 potential 2-face attachments, 150 three-faces, 30 four-faces and the top 5-cell from the *certified* subcomplex. In the null-defect mode, all 120 failing swaps have **nonzero residual vectors with quadratic norm zero**. Checking the quadratic norm alone therefore remains unsound.

### Homology comparison over F5

| Certified subcomplex | Differential ranks d1…d5 | Betti b0…b5 |
| --- | --- | --- |
| Fully admitted translations | (719,1081,479,61,1) | **(1,0,0,0,0,0)** |
| State-dependent / null-defect | (718,962,358,32,0) | **(2,0,0,0,0,0)** |

The 120 forbidden swaps split the six-event rewrite graph into **two certified-commutation components**; geometric gates by themselves would have conflated them. Both directions of every local swap are tested before a common suffix, so later non-injective updates cannot conceal an invalid local rewrite.

## Reproduction

Run from repository root:

```sh
python -m experiments.rt.p6_lift_pilot
python -m unittest discover -s tests -p 'test_rt_p6_lift_pilot.py' -v
```

The driver is deterministic, bounded, and uses no floating arithmetic, unguarded divisions or random sampling. Negative controls test malformed faces, budget atomicity, a reversed top incidence (∂² failure), the 120 state-dependent swaps, nonzero null residuals, and the explicit fact that the **version-one external route receipt only accepts 3–5 events**.

## Scope of the certificate

This is a **finite internal six-event exact experiment**. It does *not* change the externally versioned `rt-route-stream/v1` schema or pretend that a five-label receipt can certify a six-label update sequence. No signed receipt provenance, true neural/optimizer trace, arbitrary rank-R permutohedron, finite-field-to-float proof, statistical learning conclusion or performance claim is established. A next contract will need **explicitly versioned six-event externally replayable records** and an upstream-provenance-verified tensor-direction adapter before extending to real model data.
