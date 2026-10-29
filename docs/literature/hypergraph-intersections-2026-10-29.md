# Interval and box intersection hypergraphs: stop/go (2026-10-29)

**Proposed claim or experiment.** Work over finite linear orders; each part is a *labelled multiset* of closed intervals, with repeated geometric intervals retaining distinct vertex labels. For part sizes \(n_1,\ldots,n_r>0\), write \(\Sigma_r=\sum_{i=1}^r\prod_{j\ne i}n_j\). A \(K_{t,\ldots,t}^{(r)}\)-free interval intersection hypergraph has fewer than \(4^{r-1}t\Sigma_r\) hyperedges (an **imported literature theorem**, not a locally certified proof). Test exact labelled-intersection, endpoint tie-breaking and Helly-2 interfaces; do **not** claim the older proposed \(\Theta(\Sigma_r\log^{d-1}n)\) box estimate is sharp.

## Sources (primary, checked 2026-10-29)

1. **Chao, Dong, Liu, Shu and Wang**, *A dichotomy for hypergraph Zarankiewicz problems on axis-parallel boxes*, arXiv:2604.20815v1 (2026-04-22), Appendix A, Propositions A.1–A.3 and Lemma 4.7: \(e(H)<4^{r-1}t\Sigma_r\) for interval families, even when part sizes differ. Exact locator: https://arxiv.org/html/2604.20815 . The authors' non-2-coherence dichotomy concerns direction-restricted boxes, not every full-box instance.
2. **Chan, Keller and Smorodinsky**, *On Zarankiewicz's Problem for Intersection Hypergraphs of Geometric Objects*, SoCG 2025, Theorem 1.1/§2 (DOI https://doi.org/10.4230/LIPIcs.SoCG.2025.33 ): balanced, full-dimensional box upper bound \(O_{r,d,t}(n^{r-1}(\log n/\log\log n)^{d-1})\), with matching order for fixed parameters. The earlier \(\log^{d-1}n\) sharpness conjecture is therefore false for fixed \(d>1\).
3. **Chan and Har-Peled**, *On the Number of Incidences When Avoiding an Induced Biclique in Geometric Settings*, Discrete Comput. Geom. 73 (2025), pp. 466–489 (DOI https://doi.org/10.1007/s00454-024-00648-8 ; arXiv:2112.14829): points versus axis-parallel boxes, with a \(O(kn(\log n/\log\log n)^{d-1})\) bound under a forbidden biclique. This is an incidence specialization, not a full \(r\)-partite intersection theorem.
4. **Mustafa and Pach**, *On the Zarankiewicz problem for intersection hypergraphs*, J. Combin. Theory Ser. A 141 (2016), pp. 1–7, cited in Chao et al. §1: historical hypergraph intersection precedent. Citation scope not independently checked beyond bibliographic metadata in the primary 2026 work; do not use for an exact bound without reading the original paper.

**Search trail:** title queries for “intersection hypergraph Zarankiewicz”, “interval intersection hypergraph unbalanced”, “point box incidences biclique” and “box hypergraph log log”, followed by inspection of the three accessible primary results.

## Terminology

*Intersection hypergraph*, *complete multipartite forbidden hypergraph*, *tagged (multiset) intersections*, *lopsided \(K_{s,t}\)-free incidence graph*, *Helly number two*, *direction set* and *2-coherence*.

## Hypotheses and transfer

- Finite-order endpoints suffice for the exact combinatorial interfaces: interval intersection, counts of labelled tuples, monotonicity of \(\Sigma_r\), and coordinatewise Helly-2. No floating-point predicates are needed.
- Endpoint coincidences and repeated geometric intervals require tags and deterministic tie handling. A geometrically deduplicated intersection family does not preserve hyperedges.
- The full-box SoCG result assumes equal-size parts for the displayed sharp formula; do **not** transfer that formula to arbitrary unbalanced \((n_i)\) without a new proof.
- The cited 2026 interval result is a **preprint proof**. Reproducing its finite combinatorial interfaces here does not independently verify its complete induction.

## Negative controls

- Three identical intervals in distinct parts give one hyperedge but three uncharged maximum-left-endpoint witnesses.
- A naive tensor grouping can contain auxiliary \(K_{2,2}\) without original \(K_{2,2,2}\).
- The local separator proposal \(\Sigma_r(H^-)+\Sigma_r(H^+)\le\Sigma_r(H)\) was rejected in earlier project work; its original counterexample scripts were not located, so the exact old witness must still be imported before a stronger claim.
- Apparent textual errors in arXiv:2604.20815v1 Appendix A: Proposition A.2 undercounts the doubled endpoint multiset in two displayed intermediate bounds; Proposition A.3 writes \(4^{r-1}\) where the defined threshold \(T\) only guarantees \(4^{r-2}\). Correcting the algebra appears to preserve the final stated theorem. These are **audit candidates**, not author-confirmed errata.

## Decision: redirect

The general \(O_r(t\Sigma_r)\) interval result and the balanced full-box log/loglog behavior are *prior art*. Continue with a narrowed **artifact contribution**: independent exact finite-order conformance checks and, subsequently, a formal proof of the 2026 induction with labelled multisets. Investigate unbalanced full-dimensional boxes only with an explicit new problem statement and a further prior-art gate. **No novelty promotion, ledger theorem promotion or universal-bound assertion is made by these tests.**
