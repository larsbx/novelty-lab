# RT rank-lift pilot: P3 versus additive cube (2026-10-26)

**Authority:** bounded, non-authoritative exact experiment. **Literature gate:** [rank-lift-route-complexes-2026-10-26](../literature/rank-lift-route-complexes-2026-10-26.md). No new theorem or claim status.

## Question

Can a spread-controlled audit represent **more than pairwise diamonds** without conflating (a) coherence dimension, (b) tensor-direction rank, and (c) the number of cells materialized? The first controlled specimen compares two distinct models of three influences, with a parameterized rank-two direction check.

## Independent knobs

- **Shape:** order-sensitive permutohedral `P3` versus frozen-additive three-cube. The **hexagon is a two-dimensional face**; the cube has a three-dimensional filling. A three-dimensional permutohedron requires **four** influence labels (`P4`), not three.
- **Gate:** explicitly chosen subset of `F5`. Three pairwise orthogonal non-null, norm-one directions have spreads `(1,1,1)`. Gate `{1}` permits the formal coherence fixture; gate `{0}` refuses it. These are not ordered thresholds.
- **Direction:** rank-one projective spreads from the existing split quadratic oracle, plus a rank-two Grassmann pairing based on mixed `2×2` Gram determinants. It is **not** a general tensor map or a guarantee of training equivalence.
- **Instantiation:** the specimen materializes only the six permutation vertices / cube faces needed to check boundaries. This is an implementation budget, not a mathematical bound on permissible ranks.

## Reproduction

From repository root:

```sh
python -m experiments.rt.rank_lift_pilot
python -m unittest discover -s tests -p 'test_rt_rank_lift_pilot.py' -v
```

Both use exact `int` arithmetic modulo `5`, no random seed, no floating point, no infinite limits. The driver emits a self-labelled **bounded-experiment** JSON summary. The assertions cover `∂1∂2=0` for the hexagon and `∂2∂3=0` for the oriented cube, guard acceptance/rejection, null refusal, and basis independence for the rank-two interface.

## Interpretation and negative controls

The bare hexagon cycle has one `H1` generator; an attached hexagonal 2-cell fills it. The cube's six oriented square faces form a 2-cycle; its top 3-cell fills that cycle. These are standard polyhedral facts, not findings about LLM training dynamics. Spread=1 means quadratic orthogonality, **not** operational commutation. For actual state-dependent training micro-updates, the caller must separately certify endpoint equalities or declared residual bounds before a rewrite claims computational equivalence.

The reported Grassmann direction uses `s_2(U,W)=1-det(B_{UW})²/[det(B_{UU})det(B_{WW})]` with denominator guards. It is invariant under basis changes, but neither a metric nor an ordered notion of closeness over `F5`.

**Known limitations:** no `P4` 3-dimensional permutohedral cell, no general `R`-coherence, no persistent-homology claims, no source-model training, no observed probabilities, no API coupling with the upstream Mojo kernels. On-demand face enumeration and tensor-to-direction adapters remain separately testable extensions.

## Next bounded experiments

1. Construct the **full `P4` face-incidence** and verify its `∂2∂3=0` using a correct truncated-octahedron cell structure, including square and hexagonal 2-faces.
2. Add a finite, typed `DirectionModel` adapter that can select a projective vector or `Gr(k,V)` without coupling geometric rank to coherence depth.
3. Attach endpoint-equality/residual witnesses to **state-dependent** micro-updates, then compare geometry-passed swaps with actual effect-equality failures.
4. Only after those controls, try selectively materialized rank-`R` audit certificates over real training traces represented by an explicitly declared exact quantization/projection. A finite-field projection does not by itself prove floating-model equivalence.
