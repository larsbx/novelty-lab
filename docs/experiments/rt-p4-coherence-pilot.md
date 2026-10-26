# RT rank-lift experiment II: P4 incidence and direction-adapter pilot (2026-10-26)

**Status:** bounded, non-authoritative exact experiment; no theorem or novelty promotion. **Literature gate:** [P4 permutohedral coherence](../literature/p4-permutohedral-coherence-2026-10-26.md). Extends [P3 versus cube](rt-rank-lift-pilot.md).

## Question and distinctions

The initial rank-three-influence experiment contained a **two-dimensional P3 hexagonal face**, alongside a **three-dimensional cubical coherence cell** for additive, frozen contributions. The present experiment realizes a genuine **three-dimensional permutohedron P4** with four influences. Neither coherence rank nor CW cell dimension determines the tensor direction's Grassmann rank, and face materialization is a separate budget.

## Exact specimen

Run from the repository root:

```sh
python -m experiments.rt.p4_coherence_pilot
python -m unittest discover -s tests -p 'test_rt_p4_coherence_pilot.py' -v
```

The driver constructs the `P4` face poset from ordered set partitions of four labels, expands each face to its incident permutations, orients square/hexagonal polygon cycles, and propagates an orientation across the 14-face 3-cell shell. It verifies integer `∂1∂2=0` and `∂2∂3=0`.

Expected exact counts:

| CW dimension | Cells | Detail |
| --- | ---: | --- |
| 0 | 24 | all permutations of 4 labels |
| 1 | 36 | adjacent swaps |
| 2 | 14 | 8 hexagons and 6 squares |
| 3 | 1 | oriented polyhedral filling |

A selected square with boundary closure occupies four vertices/four edges/one two-face. The whole top-cell witness requires all 14 faces and their boundaries. **This pilot constructs the full P4 as a reference before selecting faces.** Sparse subset extraction here is not yet a lazy construction or a demonstrated asymptotic speed improvement.

The adapter `DirectionModel(kind, indices)` selects either a rank-one ray or a rank-two Grassmann frame from a finite bundle, and delegates spread calculation to the existing F5 quadratic experiment. The four designated non-null orthogonal directions have all six pairwise spreads equal to 1; gate `{1}` accepts, gate `{0}` rejects. A distinct pair of nondegenerate rank-two frames is used to test the Grassmann ratio.

## Negative controls and semantic boundary

- Flipping the orientation of one facet breaks `∂2∂3=0`.
- Unknown faces, null directions, repeated Grassmann basis elements and malformed adapters are rejected.
- **Geometric passage does not imply update commutation.** The explicit field maps `U(x)=x+v` and `T(x)=2x` satisfy `T(U(0))=2v ≠ v=U(T(0))` although the declared orthogonal direction fixture passes its geometric spread gate.
- `P4` is a combinatorial CW model; the code does **not** use a real-number geometry, even though prior literature provides its geometric proof. No model-training trajectory or probabilistic claim is checked.

## Follow-on proof and implementation obligations

The next step is to attach **effect-equality or exact residual certificates** to state-dependent micro-updates, so geometry-gated swaps are never mistaken for semantic equivalence. A genuinely certificate-lazy face boundary service and a general parameterizable `DirectionModel` with Grassmann rank `k` are separate upstream-kernel and consumer-interface tasks; do not implement generic determinants or finite-field arithmetic a second time here. Only afterward extend to `P5`/rank-`R` combinatorial complexes and probabilistic route auditing.

The experiment is deliberately modest: it checks one complete finite incidence object and typed direction adapters, not generic higher-rank tensor dynamics.
