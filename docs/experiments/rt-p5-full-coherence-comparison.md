# Experiment V — full P5 coherence versus P4, P3, and the additive five-cube (2026-10-26)

**Status:** bounded, non-authoritative exact experiment. Literature gate: [p5-full-coherence-2026-10-26](../literature/p5-full-coherence-2026-10-26.md). Source: experiments/rt/p5_full_coherence.py; conformance: tests/test_rt_p5_full_coherence.py. This follows the earlier completed F5 external receipt replay in PR #46.

## What is constructed

Unlike the earlier five-influence **edge-only** receipt pilot, this experiment actually generates the complete, oriented, **four-dimensional** permutohedron P5 from ordered partitions, including its 30 3-dimensional facets and single 4-cell. A facet is formed by splitting one block into two ordered nonempty blocks. Signed incidence is determined by the exact integer determinant of the outward barycenter displacement plus a canonical tangent basis. All composition checks are integer exact, then the ranks and homology are checked by a separate bounded F5 elimination oracle.

| Shape | Dimension | Number of cells by dimension | Interpretation |
| --- | ---: | --- | --- |
| P3 (3 labels) | 2 | 6, 6, 1 | A hexagonal 2-cell; NOT a 3-cell |
| P4 (4 labels) | 3 | 24, 36, 14, 1 | 8 hexagons, 6 squares, oriented 3-cell |
| **P5 (5 labels)** | **4** | **120, 240, 150, 30, 1** | **90 squares, 60 hexagons, 10 P4 facets, 20 hexagonal prisms, 4-cell** |
| **Five-cube** (5 additive updates) | **5** | **32, 80, 80, 40, 10, 1** | Subset-addition coherence with five independent frozen influences; not a permutohedron |

The ranks of the P5 chain differentials over F5, for d1 through d4, are **119, 121, 29, 1**. The filled P5 Betti vector is **(1,0,0,0,0)**; its 3-dimensional boundary has Betti vector **(1,0,0,1)**. For **all** cells of positive dimension at least two, the signed integer d-after-d sum is zero. Flipping a single 3-facet orientation of the top 4-cell produces a nonzero 2/3-chain residue: the falsifier checks orientation soundness rather than relying on an untested assertion.

## Exact comparison with *independently verified* prior route receipts

The source first calls the existing rt-route-stream/v1 verifier with an independently supplied trusted update-specification SHA-256. Only the separately recomputed admitted adjacent-swap edges are used as permissions for higher-cell attachment. A k-face is admitted if, and only if, **all its immediate (k-1)-facets are admitted**. This recursively ensures entire boundary closure.

| F5 update model | Geometry passes (of 240) | Admitted edges | Admitted 2-faces | Admitted 3-faces | Admitted 4-cell |
| --- | ---: | ---: | ---: | ---: | --- |
| Frozen translations | 240 | 240 | 150 | 30 | **Yes** |
| Scalar state-coupled | 240 | 216 | 114 | 16 | **No** |
| Nonzero-null residual defect | 240 | 216 | 114 | 16 | **No** |
| Frozen translations, Grassmann direction rank 2 | 240 | 240 | 150 | 30 | **Yes** |
| Frozen translations, 2 requested edges only | 2 checked | 2 | 0 | 0 | **No** |

The 24 failing swaps do not disappear when lifting to 4-dimensional coherence: they prevent attachment of **36 two-faces, 14 three-faces, and the top four-cell**. The null-vector defect is a crucial negative control: Q(residual)=0 can hold with residual != 0, so a scalar quadratic norm is not an effect equality certificate.

**Separate knobs:** coherence rank is 5 influences, CW top dimension is 4, Grassmann direction rank can be 1 or 2, and materialized certificate scope is independently chosen. This is a demonstration of their non-equivalence, not an engineering speedup.

## Boundary closure and sparse instantiation

The program computes the full P5 finite reference complex, then extracts exact closure for selected requested cells. Representative closures (cell vector by dimension 0–4):

- one square: (4,4,1,0,0);
- one hexagon: (6,6,1,0,0);
- one P4 facet: (24,36,14,1,0);
- one hexagonal prism: (12,18,8,1,0);
- top 4-cell: (120,240,150,30,1).

This is **selection from an already constructed reference**, not lazy asymptotic generation. An actually on-demand cell constructor remains a separate implementation objective.

## Reproduce

Run from repository root:

    python -m experiments.rt.p5_full_coherence
    python -m unittest discover -s tests -p 'test_rt_p5_full_coherence.py' -v

Any claimed promotion fails closed if a trusted spec pin is incorrect, a receipt cannot be replayed, the face geometry is not a genuine P5 facet, or the boundary has an unattached edge. The exact mathematical statement is finite combinatorial conformance, not originality.

## Limits

No general P_R theorem, arbitrary tensor order, numerical approximation certification, signed receipt provenance, LLM training run, optimizer-state completeness proof, performance claim, or rigorous probabilistic route guarantee. P5 as a classical permutohedron and the finite homology computations are not novel. The admitted P5 is only the **formally certified subcomplex of a bounded field toy-update model**, not proof that projective RT geometry alone enforces computational commutation.
