# Experiment III: state-dependent P4 semantic swap certificates (2026-10-26)

**Status:** bounded, non-authoritative exact F5 experiment. **Literature gate:** [state-dependent RT coherence](../literature/state-dependent-rt-coherence-2026-10-26.md). Depends on merged [P4 incidence and tensor-directions pilot](rt-p4-coherence-pilot.md).

## Question

Does a guarded spread-based direction agreement justify swapping two **state-dependent** tensor-update operations? **Not generally.** The experiment separates three properties:

1. **Geometric direction gate:** transported update displacements retain declared rank-one or rank-two RT relations.
2. **Computational effect equality:** in the actual prefix context, `U_b(U_a(A)) == U_a(U_b(A))` as **whole vectors** in F5^8.
3. **Higher-dimensional coherence authority:** allow a P4 face only if **each** of its boundary adjacent swaps has both certificates, and allow its top 3-cell only if every face is admitted and the P4 chain boundary remains valid.

These are independent tests; semantic effect equality is not inferred from geometric agreement.

## Reproduction

```sh
python -m experiments.rt.state_dependent_coherence_pilot
python -m unittest discover -s tests -p 'test_rt_state_dependent_coherence_pilot.py' -v
```

The tests require no randomness, floating point, normalization, roots or external runtime. The driver enumerates **all 36 adjacent-swap edges** among **all 24 permutations** of four influence labels and deterministically evaluates both two-step orders at the exact shared prefix state. It independently computes both transported-direction spreads, the full vector residual, local equalities, certified edges, admitted 2-faces, and the 3-cell admission. It also verifies every certificate by independent recomputation from its source permutation and the declared update definitions.

The underlying **training-audit state is V=F5^8**, not the Kuramoto cone; temporary training states may be null. The RT spread guard applies to update **directions**, which must be non-null, and the rank-two adapter must present nondegenerate Gram planes. This distinction permits the exact origin start in the experiment without dividing by `Q(origin)=0`.

## Three finite counterbalanced modes

| Mode | Geometric edges | Exact effect equalities | Certified edges | Full P4 top cell | Full-route effects |
| --- | ---: | ---: | ---: | --- | ---: |
| Four frozen translations `U_i(x)=x+d_i` | 36 | 36 | 36 | admitted | 1 |
| State-coupled `U_0(x)=x+(1+x_1)d_0`; other translations | 36 | 30 | 30 | rejected | 2 |
| Null defect `U_0(x)=x+d_0+x_1 e_0`; other translations | 36 | 30 | 30 | rejected | 2 |

The vectors `d_i` are four non-null, pairwise orthogonal norm-one directions in a split F5^8. The scalar-coupled case has **all geometric transported-direction spreads zero** on the declared gate `{0}`, even for six swaps that change the computation. For the null-defect mode gate `{0,3}`, six failures have **nonzero residual vector with norm zero**. This is the principal fail-closed negative control: checking only `Q(residual)=0` is unsound over split fields.

## Certificate and soundness boundary

A certificate identifies the source and target permutations, swapped position, exact prefix state, the first-step intermediate states, both two-step endpoints, four displacement directions, two guarded spreads, the vector residual, and the separate geometry/effect/admission booleans. Replay recomputes every field and refuses altered values.

When a local swap is effect-equal **at its actual prefix**, a shared deterministic suffix preserves equality of full route endpoints. Conversely, equal final endpoints **after a noninjective suffix** do not certify local equivalence; an explicit erasure counterexample is recorded. A connected component of the certified-swap graph therefore has a unique full-route endpoint for this bounded deterministic model. This is a straightforward finite induction, not a theorem of numerical stability.

A P4 3-cell is admitted only when all 14 faces are certified. A face needs all of its boundary edges; neither spread alone nor a subset of certified faces authorizes a global cell.

## Limits and next steps

The mode descriptions are **toy exact field-state update maps**; they are not an LLM optimizer, a statistical learning model, a Monte Carlo experiment, or a general statement about real-valued training. This pilot **does not** approximate floating-point updates, derive bounds from modular projections, or certify exact equality outside the finite tested prefixes. The existing consumer direction adapter is rank-one/rank-two only; higher k and tensor extraction remain separate upstream-defined mathematical primitives.

Next: version the certificate schema and support independent byte-replay from external audit records; lift geometry and effect checks to a bounded rank-R event stream; separate exact and approximate fixed-point/residue certificates before connecting to any real training workload. Preserve independent parameterizations of coherence shape, direction rank, and materialization depth.
