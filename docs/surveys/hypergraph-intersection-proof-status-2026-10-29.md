# Hypergraph intersections over finite products of linear orders

**Research status — 2026-10-29.** This is a source-comparison and test-interface packet, **not** a new extremal theorem or a formalization of the published proof. Literature gate: [2026-10-29 note](../literature/hypergraph-intersections-2026-10-29.md).

## Separating the claims

Let the \(i\)-th part contain \(n_i>0\) *labelled* closed intervals. Edges are index tuples whose intervals have nonempty common intersection. Define
\[
\Sigma_r(n_1,\dots,n_r)=\sum_{i=1}^r\prod_{j\neq i}n_j.
\]

| Claim | Evidence class | Status |
| --- | --- | --- |
| Three-family \(O(t^2\Sigma_3)\), plus the reported \((t^2+4t)\Sigma_3\) Theorem 4.7 | Earlier project report; original manuscript absent | **Unverified locally**; do not claim new proof |
| \(K_{t,\ldots,t}^{(r)}\)-free intervals satisfy \(e(H)<4^{r-1}t\Sigma_r\) | Chao et al., arXiv:2604.20815v1, Appendix A.3 | **Imported preprint theorem**, no local formal proof |
| \(\Sigma_r\) contracts under the proposed separator split | Earlier adversarial counterexamples | **Rejected approach**; original scripts not present |
| \(\sum_k \Lambda^{(k)}=|E(H)|\) for raw endpoint counts | Counterexample when tied maxima occur | **False without tie-breaking** |
| Charged maximum-left-endpoint identity | Elementary exact counting; tests enumerate finite cases | **Exact elementary identity**, not an extremal bound |
| Pairwise-intersecting boxes have nonempty joint intersection | Coordinatewise interval Helly-2 | **Elementary theorem**; finite cases checked |
| Full \(d\)-dimensional box sharp growth \(\Theta(\Sigma_r\log^{d-1}n)\) | Contradicted by balanced SoCG 2025 bounds | **Reject as a sharp conjecture** for fixed \(d>1\) |
| Unbalanced sharp full-dimensional box bound | Not established by the cited balanced theorem | **Open target pending narrower search** |

## Correcting the left-endpoint witness

For any intersecting interval tuple \(e=(I_1,\dots,I_r)\), put \(a(e)=\max_i \ell(I_i)\), and charge the tuple to the **least** index \(k\) for which \(\ell(I_k)=a(e)\). With \(a=\ell(I)\), define
\[
\Lambda_k^{\rm charged}
=\sum_{I\in A_k}
 \left(\prod_{j<k}\#\{J\in A_j:\ell(J)<a\leq u(J)\}\right)
 \left(\prod_{j>k}\#\{J\in A_j:\ell(J)\leq a\leq u(J)\}\right).
\]
For closed intervals this gives the exact combinatorial identity
\[
  |E(H)|=\sum_{k=1}^{r}\Lambda_k^{\rm charged}.
\]
Each factor counts exactly the intervals in that part which contain the anchor and respect the earliest-index winner rule. The uncharged version overcounts when two or more left endpoints tie (three equal intervals: raw sum 3 versus one hyperedge).

## Tagged multiset intersections and forbidden-clique pitfall

The intersection of a tuple from the first \(r-1\) parts is stored as \((\text{label tuple}, [\max\ell,\min u])\). Equal geometric intervals with different tuples remain different vertices in the auxiliary bipartite graph against part \(r\). There is an edge-preserving bijection from this auxiliary graph to the original hyperedges.

The auxiliary graph can contain a small complete bipartite graph even when the original complete multipartite configuration is absent. In particular, an auxiliary \(K_{2,2}\) does not force original \(K_{2,2,2}\). A sufficiently large threshold \(T\), the \((r-1)\)-partite induction hypothesis, and interval Helly-2 are essential.

For \(r\ge3\), the published induction sets
\[
T=4^{r-2}t\Sigma_{r-1}(n_1,\dots,n_{r-1}),
\]
shows the auxiliary bipartite graph is \(K_{T,t}\)-free, and applies the lopsided interval graph bound
\[
 e(G)<4(mt+ns).
\]
This yields
\[
e(H)<4\left(t\prod_{i<r}n_i+n_r T\right)
\leq4^{r-1}t\Sigma_r(n).
\]
The source v1 prints an incorrect exponent in one intermediate comparison \(T\ge4^{r-1}t\Sigma_{r-1}(n')\); its defined \(T\) only supplies \(4^{r-2}\), which is exactly what induction needs. Likewise Proposition A.2's doubled endpoint counts require corrected intermediate estimates. Treat these as proposed errata, not an independent source correction.

## Boxes and logarithmic status

An axis-parallel box over a finite product \(L_1\times\cdots\times L_d\) is a product of closed order intervals. Intersection commutes with Cartesian products, hence pairwise box intersection implies joint intersection because intervals have Helly number 2 in each coordinate. The usual maximum-left-endpoint anchor **does not** work for boxes in dimension \(\ge2\): different coordinates can attain their maxima in different boxes.

Chan–Keller–Smorodinsky (SoCG 2025) prove the balanced full-box growth, for fixed \(r,d,t\), of order
\[
 n^{r-1}\left(\frac{\log n}{\log\log n}\right)^{d-1},
\]
so the former conjecture with \(\log^{d-1}n\) is not sharp in this case. A binary-decomposition lemma alone does not prove the sharp recurrence. Unequal part sizes require a distinct statement and review.

## Reproducible checks and next proof interface

Run:

    python3 -m unittest tests.test_ordered_intersection -v

The test module (declared as a contract, **not** a ledger theorem) checks tagged-intersection bijection, witness tie-breaking for all enumerated small labelled families, one tensor collision, Helly-2 for all unordered triples of 36 finite 2D boxes, and small interval bounds. Exhausted finite cases say nothing about unbounded asymptotics.

Next formalization should separately certify:
1. Point–interval \(K_{s,t}\)-free incidence lemma \(e(G)<mt+3ns\), including endpoint ties.
2. Endpoint multiset reduction \(e(G)<4(mt+ns)\) with both endpoint sides counted with multiplicity.
3. Tagged intersection edge bijection and \(K_{T,t}\) exclusion by induction.
4. Coordinatewise Helly-2 and \(\Sigma_r\) monotonicity over finite linear orders.

Do **not** reintroduce the rejected \(\Sigma\)-potential contraction or promote any theorem status until an independent proof review is recorded.
