# Universal interval-intersection hypergraph bound: complete finite-order derivation

**Status: written mathematical proof, pending independent review.** This is a
self-contained rederivation of Appendix A of Chao–Dong–Liu–Shu–Wang,
*arXiv:2604.20815v1* (2026-04-22), with an explicit finite-linear-order and
tied-endpoint argument, and an elementary refinement replacing the published
coefficient \(t\) by \(t-1\). Neither the main asymptotic theorem nor its
induction architecture is new. The coefficient refinement is **not** a
novelty claim or an independently reviewed theorem. Literature gate:
[2026-10-29](../literature/hypergraph-intersections-2026-10-29.md).

## Definitions and main statement

Let \(L\) be a nonempty finite totally ordered set. An **interval** is
\([a,b]_L=\{x\in L:a\le x\le b\}\), with \(a\le b\). Intervals may be
singletons. Each family \(A_i\) consists of \(n_i\ge1\) labelled intervals;
equal geometric intervals remain distinct vertices with their own labels.

An edge is an index tuple \((I_1,\ldots,I_r)\in\prod_i A_i\) for which
\(\bigcap_i I_i\ne\varnothing\). The hypergraph is
\(K^{(r)}_{t,\ldots,t}\)-free if no \(t\) distinct labels in **each** part
have all their \(t^r\) choices as edges.

Write
\[
\Sigma_r(n_1,\ldots,n_r)=\sum_{k=1}^r\prod_{i\ne k}n_i.
\]

**Theorem (finite-order universal interval bound).**
For \(r\ge2\), \(t\ge2\), all positive \((n_1,\ldots,n_r)\), and all labelled
families of closed intervals on \(L\), if the intersection hypergraph \(H\) is
\(K^{(r)}_{t,\ldots,t}\)-free, then
\[
\boxed{e(H)\le4^{\,r-1}(t-1)\Sigma_r(n_1,\ldots,n_r).}\tag{U}
\]
In particular, \(e(H)<4^{r-1}t\Sigma_r\), the published preprint bound.
The statement is uniform in the order size, ties, degenerate intervals,
family sizes and multiplicities. It is **one-dimensional**; it is not a
linear-in-\(\Sigma_r\) statement for arbitrary higher-dimensional boxes.

### Lemma 1 (point–interval incidence)

Let \(P\) have \(m\ge1\) labelled vertices at positions in \(L\), and \(B\)
have \(n\ge1\) labelled intervals. If their containment graph is
\(K_{s,t}\)-free, with \(s\ge1\) on the \(P\)-side and \(t\ge1\) on the
interval side, then
\[
 e(P,B)\le m(t-1)+3n(s-1). \tag{1}
\]

**Proof.** Sort the \(m\) point *labels* in nondecreasing order of their
positions, breaking ties arbitrarily and permanently. For each interval
\(J\in B\), the positions of the point labels contained in \(J\) form a
consecutive run of indices (possibly empty). This remains true with repeated
positions because equal positions are either all in \(J\) or all out.

Partition the sorted labels into \(q=\lfloor m/s\rfloor\) full consecutive
blocks of exactly \(s\) labels and one last residual block of size
\(u=m-qs<s\) (omit the residual if empty).

For each full block, at most \(t-1\) intervals of \(B\) contain **all**
its \(s\) labels; otherwise those labels and any \(t\) intervals containing
them give \(K_{s,t}\). These full-block incidences contribute at most
\(q s(t-1)\).

An interval that meets but does not completely contain a full block
contributes at most \(s-1\) incidences to that block. Because its covered
point indices form a single run, it can **partially meet at most two full
blocks**: a partial block must contain the start or the end of that run.
Therefore, summed over all intervals, partial incidences to full blocks
are at most \(2n(s-1)\). Finally, the residual block contributes at most
\(un\le n(s-1)\).

Consequently
\[
 e(P,B)\le qs(t-1)+2n(s-1)+un
 \le m(t-1)+3n(s-1).
\]
No argument about interiors of geometric intervals is needed, so ties and
singleton intervals are harmless. \(\square\)

### Lemma 2 (interval–interval incidence)

Let \(A,B\) have \(m,n\ge1\) labelled intervals. If their intersection graph
is \(K_{s,t}\)-free (\(s,t\ge1\) from the respective sides), then
\[
 \boxed{e(A,B)\le4\bigl(m(t-1)+n(s-1)\bigr).}\tag{2}
\]
In particular, \(e(A,B)<4(mt+ns)\).

**Proof.** Replace each interval of \(A\) by its two **tagged endpoint
occurrences**, retaining two occurrences even when the interval is a
singleton. This forms \(2m\) labelled points. The endpoint–\(B\)
containment graph \(G_A\) is \(K_{2s-1,t}\)-free: any \(2s-1\) distinct
endpoint occurrences originate from at least \(s\) distinct \(A\)-labels,
and if they all lie in \(t\) fixed \(B\)-intervals, these give the forbidden
\(K_{s,t}\). Applying (1) with \(m_{\rm point}=2m\) yields
\[
 e(G_A)\le2m(t-1)+3n(2s-2)
         =2m(t-1)+6n(s-1).
\]
Similarly the graph \(G_B\) of \(2n\) tagged \(B\)-endpoints versus \(m\)
\(A\)-intervals is \(K_{2t-1,s}\)-free, so
\[
 e(G_B)\le2n(s-1)+6m(t-1).
\]

Every intersection \((I,J)\in A\times B\) contributes at least **two**
tagged endpoint-containment incidences across \(G_A,G_B\): the maximum
of its two left endpoints and the minimum of its two right endpoints
both lie in the intersection and are endpoint *occurrences*.
If the two coincide geometrically, their left/right endpoint tags are
still distinct. Conversely every endpoint-containment incidence belongs
to exactly one original pair. Therefore
\[
 2e(A,B)\le e(G_A)+e(G_B)
 \le8m(t-1)+8n(s-1),
\]
which is (2). \(\square\)

### Lemma 3 (Helly-2 over a linear order)

A finite family of closed intervals has nonempty total intersection if
and only if every pair intersects.

**Proof.** The intersection is
\([\max \ell(I),\min u(I)]_L\), and if this is empty, the interval attaining
the maximum lower endpoint and the interval attaining the minimum upper
endpoint are disjoint. The proof also applies to singletons and ties.
\(\square\)

For boxes in a product of finite linear orders, pairwise intersection
implies common intersection coordinatewise. The following induction,
however, needs the *one-dimensional* Lemma 2.

## Proof of theorem (U), by induction on the part count

**Base \(r=2\).** Lemma 2 with \(s=t\) gives
\[
 e(H)\le4(t-1)(n_1+n_2)=4^{2-1}(t-1)\Sigma_2.
\]

**Step \(r-1\to r\), \(r\ge3\).** Assume (U) for \(r-1\) interval
families with arbitrary positive part sizes and parameter \(t\).
Form a tagged family \(C\) of intervals: for every labelled
\((r-1)\)-tuple \(\alpha=(I_1,\ldots,I_{r-1})\) with nonempty intersection,
keep the pair
\[
  (\alpha,J_\alpha),\qquad J_\alpha=\bigcap_{i<r}I_i.
\]
Even if \(J_\alpha=J_\beta\), different tags \(\alpha\ne\beta\) are different
vertices of \(C\). Let \(M=|C|\le\prod_{i<r}n_i\).
Build an ordinary bipartite interval intersection graph \(G\) between
\(C\) and \(A_r\).

The maps \((\alpha,I_r)\mapsto(I_1,\ldots,I_r)\) and its inverse prove
\[
 e(G)=e(H). \tag{3}
\]

Set the integer threshold
\[
 T=4^{r-2}(t-1)\Sigma_{r-1}(n_1,\ldots,n_{r-1}). \tag{4}
\]

**Claim: \(G\) has no \(K_{T,t}\).**
Suppose instead that \(T\) distinct tagged intersections \(J_{\alpha}\)
meet each of \(t\) fixed \(A_r\)-intervals \(D_1,\ldots,D_t\).
For each \(i<r\), let \(A_i'\subseteq A_i\) be the set of original
*labels* appearing in the chosen \(T\) tuples, and write
\(n_i'=|A_i'|\le n_i\). The \((r-1)\)-partite intersection hypergraph
\(H'\) on these restricted parts contains all \(T\) selected distinct
tuple edges. Thus
\[
 e(H')\ge T
 \ge4^{r-2}(t-1)\Sigma_{r-1}(n'_1,\ldots,n'_{r-1}), \tag{5}
\]
by coordinatewise monotonicity of \(\Sigma_{r-1}\).

The induction hypothesis, in contrapositive form, now implies that
\(H'\) contains a \(K^{(r-1)}_{t,\ldots,t}\). Choose its \(t\) labelled
intervals in each first part, denoting these subsets \(A_i^*\).

Every interval in \(A_i^*\) lies in at least one selected tagged
intersection \(J_\alpha\). As each selected \(J_\alpha\) meets every
\(D_j\), that interval also meets each \(D_j\). Furthermore, any two
intervals chosen from distinct among the first \(r-1\) parts meet,
because the selected \(K^{(r-1)}_{t,\ldots,t}\) is complete.
Given any one chosen interval from *each* part, all chosen intervals
are therefore pairwise intersecting. Lemma 3 makes their entire
intersection nonempty, so \(A_1^*,\ldots,A_{r-1}^*,\{D_1,\ldots,D_t\}\)
form \(K^{(r)}_{t,\ldots,t}\) in \(H\): contradiction. The claim follows.

Apply Lemma 2 to \(G\) with \(s=T\) and \(t\) on the last family:
\[
\begin{aligned}
 e(H)&=e(G)
  \le4\bigl(M(t-1)+n_r(T-1)\bigr)\\
 &\le4(t-1)\prod_{i<r}n_i
    +4^{r-1}(t-1)n_r\Sigma_{r-1}(n_1,\ldots,n_{r-1})\\
 &\le4^{r-1}(t-1)
    \left(\prod_{i<r}n_i+n_r\Sigma_{r-1}\right)\\
 &=4^{r-1}(t-1)\Sigma_r,
\end{aligned}
\]
where the penultimate inequality uses \(4\le4^{r-1}\), and the
identity is the exact decomposition
\[
\Sigma_r=\prod_{i<r}n_i+n_r\Sigma_{r-1}.
\]
This closes the induction. \(\blacksquare\)

**Quantifier audit.** Every constant is independent of the order \(L\),
its cardinality, all endpoint positions, and every \(n_i\). The statement
allows duplicate labelled intervals and degenerate/singleton intervals.
For \(r=1\), the analogous bound \(e(H)\le t-1\) is immediate from
\(K_t^{(1)}\)-freeness. The proof is finite-combinatorial throughout.

## Sharp dependence on unequal part sizes (fixed \(r,t\))

For each \(k\) choose a two-vertex order with \(x<y\); place every
interval in the other \(r-1\) families at \(\{x\}\). In part \(k\),
put exactly \(q=\min(n_k,t-1)\) intervals at \(\{x\}\) and the other
\(n_k-q\) at \(\{y\}\). Then the hypergraph is
\(K^{(r)}_{t,\ldots,t}\)-free and has exactly
\[
 q\prod_{j\ne k}n_j
\]
edges. Choosing \(k\) with smallest \(n_k\) gives
\[
 e(H)\ge\prod_{j\ne k}n_j\ge\frac1r\Sigma_r.
\]
Consequently the extremal order, for fixed \(r,t\) over arbitrary
sufficiently rich finite orders, is \(\Theta_{r,t}(\Sigma_r)\) **even
for very unbalanced part sizes**. This is a simple construction,
not an independent novelty claim.

## Limits, audit observations, and replication

1. **No universal \(d>1\) linear analogue.** Full-dimensional boxes
   have a sharp extra \((\log n/\log\log n)^{d-1}\) in the balanced case
   (Chan–Keller–Smorodinsky, SoCG 2025). Helly-2 survives in products,
   but Lemma 2 does not apply to rectangle–rectangle incidence graphs.
2. **Not the rejected \(\Sigma\)-potential approach.** We use
   \(\Sigma_{r-1}(\mathbf n')\le\Sigma_{r-1}(\mathbf n)\) only for
   restricted *part sizes*, never claim potential contraction under
   separator splits.
3. **Not \(\Lambda^{(k)}\) induction.** The charged left-endpoint
   witness identity is valid, but is not needed for this proof.
4. **Source repair (Proposition A.2).** Applying the point–interval
   lemma to \(2m\) and \(2n\) endpoints, not \(m,n\), gives corrected
   point-incidence factors.
5. **Source repair (Proposition A.3).** The inductive threshold is
   \(4^{r-2}t\Sigma_{r-1}\) in the published version (or
   \(4^{r-2}(t-1)\Sigma_{r-1}\) above); the paper's later
   \(4^{r-1}\)-threshold comparison does not follow as written.
6. The step from \(t\) to \(t-1\) here is the direct integer refinement
   of the same block-counting proof and should not be represented as a
   novel extremal exponent or independently refereed improvement.

**Reproduce finite controls:**

    python3 -m unittest discover -s tests -p 'test_ordered_intersection.py' -v
    python3 -m unittest discover -s tests -p 'test_interval_universal_base.py' -v

The controls cover finite configurations only; the displayed proofs are
mathematical text **pending an independent proof audit**.
