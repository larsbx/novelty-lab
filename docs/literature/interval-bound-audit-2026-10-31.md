# Independent interval-bound audit stop/go (2026-10-31)

## Proposed claim or experiment

Audit the merged proof of `e <= 4^(r-1)(t-1) Sigma_r` for labelled
closed intervals on a finite linear order, including singleton intervals.
Independently derive the incidence lemmas, search finite counterexamples,
and formalize finite counting and order interfaces. Also examine the stronger
sliding-window point bound `e <= m(t-1)+n(s-1)`; novelty is not a target.

## Sources (primary, read 2026-10-31)

1. Chao–Dong–Liu–Shu–Wang, arXiv:2604.20815v1, Appendix A,
   Propositions A.1–A.3, https://arxiv.org/html/2604.20815v1 .
   Full appendix read. It supplies the closest induction architecture;
   multisets are explicit. A.2 applies A.1 to doubled endpoint families but
   writes undoubled leading terms. A.3's displayed comparison has exponent
   r-1 although its threshold uses r-2. These are textual discrepancies,
   not author-confirmed errata. Neither invalidates the corrected local proof.
2. Chan–Keller–Smorodinsky, SoCG 2025, abstract and publication record,
   https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2025.33 .
   Sharp full-box asymptotic has the log/loglog factor for dimension >1.
   This source is used to exclude a higher-dimensional linear generalization,
   not to supply a constant in the audited one-dimensional proof.
3. Chan–Har-Peled, arXiv:2112.14829v4, abstract,
   https://arxiv.org/abs/2112.14829 . Point–box forbidden-biclique incidence
   bounds; Appendix A of source 1 identifies its Lemma 2.1 as antecedent.
   Only the abstract and source 1's attribution were read here; do not claim
   a full inspection of Lemma 2.1 or priority for the sliding-window refinement.

Retrieval: direct primary URLs above. Firecrawl retrieval was unavailable
(`Unknown tool`); the web reader supplied the sources. Reuse the October 29
literature gate for the broader problem. This is a bounded attribution check,
not an exhaustive priority search.

## Terminology

Convex point neighborhoods, labelled multisets, consecutive windows,
lopsided forbidden bicliques, tagged intersections, finite Helly-2.

## Hypotheses

Labels survive all lifts; interval neighborhoods in sorted point labels are
consecutive runs, even with tied positions. Endpoints are included. Nonempty
finite orders are equivalent by ranking to initial segments of the naturals.
The interval-incidence lemma cannot be transferred to boxes in dimension >1.

## Negative controls

Dropping the additive term in point incidence, geometrically deduplicating
endpoints, claiming exactly two endpoint incidences per edge, replacing
`T=B+1` by `B` merely because `e<=B`, and transferring a small forbidden
biclique unchanged through tensor grouping are not justified.

## Decision: proceed with a narrowed target

Add a separately reproducible audit and supporting Lean proofs, without
promoting any ledger record or asserting novelty. Keep the original theorem
and provenance intact. A stronger coefficient derived in the audit remains
separate from formal coverage of the full hypergraph theorem.
