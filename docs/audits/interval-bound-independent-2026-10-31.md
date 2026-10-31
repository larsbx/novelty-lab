# Independent audit of the interval-hypergraph bound (2026-10-31)

## Verdict and scope

**Audited revision:** `f4e1fd884ec8541bf6a622a07e2a51dcbaacbea4` of
`larsbx/novelty-lab`, in particular
[`interval-hypergraph-universal-bound.md`](../proofs/interval-hypergraph-universal-bound.md).
The mathematical reconstruction below found **no defect in the proposed
`4^(r-1)(t-1) Sigma_r` bound** under its stated hypotheses. The integer
`t-1` refinement survives this independent audit. This is an independently
reconstructed written argument, with supporting Lean lemmas and finite tests;
it is not a human referee report or an end-to-end Lean certification.
No ledger promotion or novelty finding is made.

The merged proof's block estimate, doubled endpoint lift, strict threshold,
tagged carrier and coefficient comparison all survive scrutiny. A separate
sliding-window reconstruction is stronger: it gives point incidence
`e <= m(t-1)+n(s-1)`, interval incidence
`e <= 2[m(t-1)+n(s-1)]`, and hence the written corollary

\[
 e(H)\le 2^{r-1}(t-1)\Sigma_r.
\]

This corollary is recorded separately, **pending further independent review**;
the merged theorem is not replaced. Constant sharpness and priority for either
refinement have not been established. Attribution for the induction remains
Chao–Dong–Liu–Shu–Wang, Appendix A, and its cited antecedents.
The [literature gate](../literature/interval-bound-audit-2026-10-31.md) records
exact reading coverage and excludes a higher-dimensional claim.

## Hypotheses fixed before counting

All geometric intervals are nonempty and closed in a nonempty finite linear
order. Families are indexed lists of vertices: geometry need not be injective
in the labels. Forbidden cliques use distinct labels **within each part**.
No pair of intervals within the same part is required to meet. The theorem
assumes `r>=2, t>=2, n_i>=1`; the incidence lemmas allow `s,t>=1`.
Empty incidence parts are harmless and are also tested.

Rank the underlying order in the naturals. This preserves membership,
intersection, endpoint equality, singleton intervals and all labels; no
continuity, perturbation, thickening or analysis is needed. Sort point labels
by rank, breaking ties permanently. A containing interval sees a consecutive
run of these labels: equal positions are all included or all excluded.

## 1. Independently reconstructed point incidence

Write the sorted point labels as `0,...,m-1`. For interval label `j`, its
neighbor set is a possibly empty half-open index run `[a_j,b_j)`, with
`0<=a_j<=b_j<=m`. This is an index interval, not a change to the closed
geometric convention. Put `d_j=b_j-a_j`.

Fix `s>=1`. Split the incidences in each run into its first at most `s-1`
indices and its remaining indices. Each remaining incidence at index `i`
certifies that the interval covers the `s` **distinct labels**
`i+1-s,...,i`. Thus at most `t-1` interval labels can be charged to a fixed
such window, since otherwise that window and `t` labels form `K_{s,t}`.
An incidence is charged once, to its own ending index. Consequently, with
`w=max(0,m-s+1)`, double counting gives the exact identity and bound

\[
\begin{aligned}
 e &=\sum_j\min(d_j,s-1)+\sum_j\max(0,d_j-s+1),\\
 \sum_j\max(0,d_j-s+1)
   &=\sum_{i=s-1}^{m-1}\#\{j:a_j+s-1\le i<b_j\}\le w(t-1),\\
 e &\le n(s-1)+w(t-1)\le n(s-1)+m(t-1).\tag{P}
\end{aligned}
\]

An empty summation is zero. If `s>m`, every run has length at most `s-1`
and the window term vanishes. If `s=1`, each individual point has at most
`t-1` neighbors. If `t=1`, each interval has fewer than `s` point labels.
None of these cases permits replacing labels with distinct coordinates.

**Comparison with the merged block proof.** Partitioning labels into full
`s`-blocks and a residual block is also valid. A consecutive run has at most
two partially covered full blocks; each contributes at most `s-1`, and the
residual has at most `s-1` labels. Full blocks have at most `t-1` containing
intervals. Hence `qs(t-1)+2n(s-1)+un <= m(t-1)+3n(s-1)`.
This counts indices rather than geometric interiors, so repeated endpoints
cause no missing boundary incidence. Formula (P) independently implies that
weaker estimate and explains exactly where `t-1` enters.

## 2. Independently reconstructed interval incidence

Give every interval two occurrences `(family,label,left)` and
`(family,label,right)`, even for a singleton. Let `G_A` be the containment
graph of the `2m` A-occurrences against the B-labels.

Any `2s-1` distinct A-occurrences come from at least `s` A-labels: fewer
labels supply at most `2(s-1)` occurrences. If `t` B-labels contain all
those occurrences, each of these `s` A-labels meets every one of those
B-labels. Therefore `G_A` is `K_{2s-1,t}`-free. The symmetric statement
makes `G_B` `K_{2t-1,s}`-free.

For an intersecting pair `(A,B)`, choose an occurrence attaining the maximum
left endpoint and an occurrence attaining the minimum right endpoint.
Each lies in the other interval. The two occurrences have different
left/right tags, even if they coincide as positions, and each endpoint
incidence belongs to exactly one original pair. Thus

\[
 2e\le e(G_A)+e(G_B).\tag{E}
\]

Applying the **merged** point bound to the two lifted graphs gives

\[
\begin{aligned}
 e(G_A)&\le2m(t-1)+6n(s-1),\\
 e(G_B)&\le2n(s-1)+6m(t-1),\\
 2e&\le8m(t-1)+8n(s-1).
\end{aligned}
\]

Division by two is exactly the claimed `4[m(t-1)+n(s-1)]`.
There is no hidden lost factor from endpoint doubling. Applying (P) instead
replaces the two sixes by twos and yields independently

\[
 e\le2[m(t-1)+n(s-1)].\tag{I}
\]

Equation (E) is an inequality, not an equality: equal intervals give four
occurrences per intersecting pair. Deduplicating singleton endpoints can
make even (E) false. The threshold `2s-1` cannot be lowered mechanically to
`2s-2`; an explicit counterexample is recorded below.

## 3. Helly and the tagged-intersection induction

For a nonempty finite family of intervals, let `x` be its largest lower
endpoint. Pairwise intersection implies each upper endpoint is at least
`x`: compare the interval attaining `x` with the interval having that upper
endpoint. Hence all intervals contain `x`. Repeated labels and equal
endpoints affect neither the comparison nor attainment. This is Helly-2.

To audit the induction without depending on the source's coefficient, write
`c` for either `4` (merged lemmas) or `2` (P and I). The base is
`e <= c(t-1)(n_1+n_2)`.

Assume the `(r-1)`-part bound for arbitrary positive sizes. Make one auxiliary
vertex for **each distinct label tuple** in the first `r-1` parts whose
intersection is nonempty, carrying the tuple itself as tag and its clipped
intersection as interval. There are `M<=p=prod_{i<r} n_i` vertices.
The map `((i_1,...,i_{r-1}),i_r) <-> (i_1,...,i_r)` is a bijection
between auxiliary edges and original edges. Equal clipped intervals still
have different tags, so multiplicities are preserved exactly. If `M=0`,
there are no edges and no incidence lemma needs a nonempty first family.

Put

\[
 B=c^{r-2}(t-1)\Sigma_{r-1}(n_1,\ldots,n_{r-1}),\qquad T=B+1.
\]

Suppose `T` tags all meet the same `t` last-part labels `D_j`. In each first
part restrict to the **set of original labels appearing in those tags**;
do not clone a label once per appearance. These sets have positive sizes
`n_i'<=n_i`. The restricted prefix hypergraph has at least `T` distinct
edges, so

\[
 e(H')\ge T>B\ge c^{r-2}(t-1)\Sigma_{r-1}(n'_1,\ldots,n'_{r-1}).
\]

The last inequality holds term by term: each product has nonnegative factors
and each restricted factor is at most its original counterpart. The
contrapositive induction hypothesis forces a prefix `K_{t,...,t}`.
This clique need not consist of the selected tags. **Every interval label
in its parts nevertheless occurs in a selected tag.** Since that tag's
clipped intersection is a subset of the original interval and meets every
`D_j`, the original interval meets every `D_j`.

Now take one interval from each of the chosen first-part subsets and one
`D_j`. Any two chosen first-part intervals meet, because they can be
completed to an edge of the prefix clique. Each meets `D_j` by the previous
paragraph. Helly-2 gives a common point for this particular tuple. Repeating
for all choices proves a full original `K_{t,...,t}`, a contradiction.
We never require two `D_j` intervals or two labels in one first part to meet.
Thus the auxiliary graph is `K_{T,t}`-free.

**Threshold audit.** The induction hypothesis is non-strict. `e(H')>=B`
would not contradict `e(H')<=B`. The required deduction is supplied by
`T=B+1`. There is no evidence here that `B` is a sharp geometric threshold;
only that a smaller threshold cannot be justified from that inequality alone.

## 4. Every final coefficient comparison

Write `a=t-1>=1`, `z=n_r`, `S=Sigma_{r-1}` and `p=prod_{i<r} n_i`.
The bipartite lemma and the corrected threshold give, successively,

\[
\begin{aligned}
 e(H)&=e(G)\\
 &\le c[M a+z(T-1)] &&\text{incidence with }s=T\\
 &\le c[p a+zB] &&M\le p,\ a\ge0\\
 &=cpa+c^{r-1}azS &&T-1=B=c^{r-2}aS\\
 &\le c^{r-1}a(p+zS) &&c\le c^{r-1}\ (r\ge3,\ c\ge1)\\
 &=c^{r-1}(t-1)\Sigma_r.
\end{aligned}
\]

The last identity partitions the omitted-index terms: omitting the last
index gives `p`; all other omissions give `zS`. No balanced-size assumption
or division by a part size occurs. The Lean theorem `coefficient_step`
checks the comparison for arbitrary nonnegative `a,p,z,S,c` and `C>=1`,
with `C=c^(r-2)`. The original proof uses `c=4`; the separate strengthened
corollary uses `c=2`.

## 5. Boundary cases and rejected stronger claims

- **One part smaller than t.** If `n_k<=t-1`, the hypergraph is automatically
  forbidden-clique-free and `e<=prod n_i <= (t-1) prod_{i!=k} n_i
  <= (t-1) Sigma_r`. This also covers arbitrarily unbalanced sizes.
- **One-point order.** All intervals are equal singletons. The full labelled
  product is a clique iff every part has at least `t` labels. Otherwise the
  preceding trivial bound applies. Equality of geometry does not delete edges.
- **Endpoint ties.** Sorted point runs include all equal positions; an
  interval may start/end between blocks of equal labels only if all labels
  at that position are included. The index argument never requires this
  extra restriction and therefore remains sound.
- **Point additive term cannot disappear.** One point label at 0 and two
  interval labels `[0,0]` are `K_{2,2}`-free but have `2>m(t-1)=1` edges.
- **Endpoint threshold cannot become `2s-2`.** Take
  `A=([0,0],[1,1])`, `B=([0,0],[0,0])`, `s=t=2`. The original graph is
  `K_{2,2}`-free, but the two occurrences of A's first singleton and both
  B-labels form an endpoint `K_{2,2}`.
- **Geometric deduplication is unsound.** Two labelled `[0,0]` in A and one
  in B give two edges. Geometrically deduplicating each side's endpoints
  gives one A-endpoint incidence and two B-endpoint incidences: their sum
  is 3, smaller than twice the edge count, 4. Two equal labels in each of two prefix
  parts also give four tags with identical clipped geometry.
- **Unchanged tensor threshold is false.** Prefix parts of sizes `(1,2)`
  and last part of size 2, all at `[0,0]`, have auxiliary `K_{2,2}` but no
  original `K_{2,2,2}`. Grouping does not preserve the small forbidden clique.
- **Exactly two endpoints per pair is false.** `A=B=[0,1]` gives four
  endpoint incidences. The needed lower bound remains valid.

The executable search rediscovers the missing-additive-term and lowered
endpoint-threshold counterexamples, rather than merely asserting fixtures.
Other fixtures pin the multiplicity and tensor failures. No counterexample
to (P), (I), or the original theorem was found in the domains below. This
negative search result has precisely those finite domains, not universal scope.

## 6. Independent finite evidence

`tests/test_interval_bound_audit.py` does not import the merged oracle or
its predicates. It uses integer endpoints, bitmask neighbor sets and exact
label tuples. Within each family, enumeration uses nondecreasing multisets:
this removes only label permutations, which preserve incidence counts,
cliques, endpoint lifts and all tested inequalities. **Repeated entries
remain separate labels.**

| Domain | Configurations | Forbidden-free parameter checks |
| --- | ---: | ---: |
| Point multisets on 3 positions, m=0..5, n=0..3, s=1..6, t=1..4 | 4,704 | 88,790 |
| Two interval multisets on 3 positions, m,n=0..3, s,t=1..4 | 7,056 | 79,780 |
| 2-position hypergraphs, sizes (2,2,2), (1,3,8), (2,2,2,2), t=2,3 | 2,862 | 5,503 |
| 2-position interval pairs, sizes (9,9), (2,25), (25,2), s,t=2,3 | 7,237 | 8,910 |

The hypergraph enumeration additionally checks the exact tagged edge
bijection and, for **every pair of last-part labels**, checks that every
prefix clique in the associated restricted carrier extends to both labels.
This exercises the geometric lifting argument even when the generous
universal edge bound itself is vacuous on tiny configurations.
A separate larger pair census uses sizes `(9,9),(2,25),(25,2)` on 2 positions,
with `s,t=2,3`. Its receipt includes the number of forbidden-free checks in
which the complete graph exceeds the original bound, explicitly identifying
nonvacuous counting tests (18 such checks). In total there are 21,859
configurations and 182,983 forbidden-free parameter checks.
The million/billion-scale arithmetic fixtures
check the exact recurrence without constructing huge graphs.

Reproduce all counts and search witnesses:

```sh
python experiments/interval_bound_audit.py
python -m unittest discover -s tests -p test_interval_bound_audit.py -v
```

The exact UTF-8 JSON receipt produced by that driver has SHA-256
`e84f9b17b0e23e1b7ed7989206839dda4f51b9a0691beb1643fcd92cdb7e0a8c`.
Recompute with `python experiments/interval_bound_audit.py | sha256sum`.

This is a deterministic finite evidence receipt, not a certificate for all
orders, all sizes or all r. No ledger `finite-domain` record or generated
data file is created by this audit.

## 7. Formal coverage and remaining obligations

`NoveltyLab/IntervalBound.lean` imports only `Std` under the repository's
pinned Lean 4.24.0. Importing it from `Main.lean` makes the standard build
check it. There are no `sorry`, added axioms, analytic objects or dependencies
on the new Python tests.

| Lean theorem | What the kernel checks |
| --- | --- |
| `meets_iff`, `endpoint_witnesses`, `endpoint_tags_distinct` | Cross-endpoint intersection criterion and distinct left/right witnesses |
| `helly`, `finite_helly`, `helly_extend` | Finite list Helly-2, its explicit `Fin N` specialization, and extension by one interval |
| `contains_clip`, `tagged_edge_iff` | Exact clipped-intersection membership and the triple-edge interface |
| `count_run`, `sumN_swap`, `point_run_bound` | Consecutive-run counts, finite double counting, and (P) from explicit per-window capacity |
| `window_contained` | A charged late incidence contains all s consecutive labels |
| `endpoint_pigeonhole` | 2s-1 occurrences force at least s labels given capacity two per label |
| `strict_threshold`, `coefficient_step` | Strict threshold and the last coefficient inequality |

**Not yet formalized end to end:** converting sorted point-coordinate
containment neighborhoods to index runs; extracting `t` distinct neighbors from a
cardinality exceeding `t-1`; deriving the per-window capacity directly from
an abstract `K_{s,t}`-free graph; the global sum of tagged endpoint counts;
and the arbitrary-r carrier cardinality, clique restriction and induction.
The point-run bound's capacity hypothesis is explicit and independently
justified in section 1, not disguised as a formal proof of that extraction.
The clipping theorem proves the triple interface; iteration to arbitrary
prefix length is written mathematics, not an existing Lean theorem here.
The `FiniteInterval N` model uses endpoints in `Fin N` explicitly, and
`finite_helly` produces a witness in that finite order. The ranking
isomorphism for an arbitrary finite-order type is not formalized in this file.

A separate `#print axioms` inspection of `point_run_bound`, `helly_extend`,
`tagged_edge_iff`, `coefficient_step` and `endpoint_pigeonhole` reported only
Lean's standard `propext`, `Classical.choice`, and/or `Quot.sound`, with no
`sorryAx` or user-added axiom.

These are precise remaining formalization tasks, not missing hypotheses in
the written proof. A full Lean theorem will need those links. Successful CI
or finite enumeration cannot substitute for them.

## Repository validation

Local gates completed successfully:

- `scripts/verify_all.sh python`: PASS, including all regressions, committed
  census replays, governance coverage and generated paper-table checks.
- `scripts/verify_all.sh lean`: PASS on pinned Lean 4.24.0, including the
  ordinary build, self-check, mutation suite and F3 export comparison.
- `scripts/verify_all.sh tla`: PASS with workflow-pinned TLC v1.7.4; the
  downloaded JAR's SHA-256 was checked against the workflow pin.
- The exact pinned estate layout audit: PASS after SHA-256 verification.
- The six focused independent interval tests: PASS, including a final replay
  after tightening the deduplicated-endpoint negative control to count both
  endpoint graphs; the receipt hash above was reproduced.

The local sandbox required an external executable-path lookup compatibility
wrapper for Lean (`/proc/<pid>/exe` lookup), supplying paths only. The pinned
Lean compiler, libraries and proof kernel were unchanged; no workaround is
committed. Hosted CI uses the ordinary repository workflows. Local success
is not a claim about the status of any later hosted run.

## Additional lower-bound check

The merged unequal-size lower construction is valid too. With a smallest
part k, q=min(n_k,t-1)>=1 labels at x and the others at y, exactly
q*prod(other sizes) tuples intersect. Any t labels in part k include one at
y (or there are fewer than t labels), while all other parts are at x, so
there is no forbidden clique. Omitting the smallest size maximizes the
product of the remaining sizes; therefore Sigma_r is at most r times that
product, and the displayed lower estimate follows. This concerns order of
growth, not a sharp leading constant.

## Attribution and status

The universal linear order and induction architecture are prior art, as
recorded in the merged note and October 29 literature audit. The independently
established written `t-1` refinement is a constant-level refinement of the
same elementary combinatorics. The further sliding-window improvement is
also recorded without any priority or novelty assertion. Neither the audit
nor its Lean fragment establishes a bound for arbitrary higher-dimensional
boxes. No external authors were contacted and no author-confirmed erratum
is claimed.
