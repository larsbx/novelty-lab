# Theoretical computer science and algebraic topology — routes, rewrites and classes

**Discipline:** semantics of rewriting systems, automata/concurrency traces, polygraphs, cellular homology, algorithmic complexity. These subjects include provable theorems, decidable finite problems and implemented algorithms, but the standards differ between them.

## Separate mathematical/computational objects

**Formal permutation object.** Ordered influence labels yield vertices and adjacent-transposition edges. Permutohedral square/hexagonal cells and their higher-dimensional incidences can be built as finite combinatorics. The cellular chain identity \(\partial^2=0\) verifies incidence consistency, not execution semantics.

**Operational transition object.** A program step \(U_i:S\to S\) acts on an *entire state*, potentially including optimizer buffers, randomness and data-stream position. A local swap of \(i,j\) is effect-equivalent at prefix \(a\) only if \(U_j(U_i(a))=U_i(U_j(a))\) in the declared state equality. If endpoints differ, a comparison edge must be separately typed; it is not automatically a computational commutation 2-cell.

**Homology object.** Over \(\mathbb F_p\), \(H_1(K)=\ker\partial_1/\operatorname{im}\partial_2\). A class \([z]\) is excluded from an unpinned subcomplex \(U(S)\) when it is not in \(\operatorname{im}(H_1(U(S))\to H_1(K))\). Witness support hitting is a *finite optimization proxy*: removing one representative need not remove the class. \(H_1\) cannot replace all nonabelian path-\(\pi_1\) semantics.

## Evidence appropriate to this field

A formal theorem of confluence, trace independence, chain exactness or algorithmic complexity needs a specified rewrite/transition system and proof of that statement. For a **particular finite \(P_6\) instance**, exhaustive signed incidence, boundary closure and exact finite-field rank checks can establish a scoped computational fact without proving a general polygraphic coherence theorem. For particular update maps, exact endpoint replay certifies their behavior in the tested domain and not every possible implementation.

The existing [P6 pilot](../../experiments/rt-p6-lift-pilot.md) compares valid geometric gates with failed effect equality. That counterexample is sufficient to forbid an inference from geometry to semantic commutation, without contesting the underlying algebraic RT theorem.

## Open questions local to the field

For state-dependent maps, characterize which prefix-conditioned independence relations are stable under scheduling/context extension. Develop a typed comparison-complex construction when endpoints differ, avoiding accidental quotienting. Study algorithmic complexity of incremental homology and inclusion-map verification under static constraints. These are **separate research questions**; a proof in one does not promote the others.

**Nearest references:** Mazurkiewicz traces; Aalbersberg–Rozenberg; Godefroid; Postnikov; Hatcher; Guiraud–Malbos, with locators in the [source map](../rt-tensor-route-auditing-context-2026-10-28.md).
