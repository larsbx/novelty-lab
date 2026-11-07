# N7 projective arithmetic literature gate

## Proposed claim or experiment

Compare incidence support, integral fixed-output orbit counts, and framed
partial operations over F₇², with a projective-plane incidence replay over F₃³.
Adjoin a singleton orbit for vector zero. Count ordered pairs at one output
vector. Use F₇[u]/(u² − 3) for the separate multiplicative action.

## Sources

Read on 2026-11-07.

- [Krasner, *A class of hyperrings and hyperfields*](https://www.emis.de/journals/HOA/IJMMS/6/307.pdf),
  pp. 307–311, gives the quotient hyperfield construction for a field and a
  subgroup of its multiplicative group.
- [Connes and Consani, *The hyperring of adèle classes*](https://math.jhu.edu/~kc/papers/JNT2.pdf),
  Proposition 3.1 and §3.1, pp. 170–173, recover a projective line by adding
  the endpoints to the sum of distinct points and discuss finite extensions
  of the Krasner hyperfield.
- [Evdokimov and Ponomarenko, *Normal cyclotomic schemes over a finite
  commutative ring*](https://arxiv.org/abs/math/0608469),
  §1, p. 1, identify the translation scheme defined by differences lying in
  multiplicative-subgroup orbits. For fixed endpoints 0 and z, an intermediate
  point t with differences t and z − t in the specified orbits counts exactly
  one ordered pair summing to z. These intersection numbers match N7's
  fixed-output convention.
- [Wildberger, *Finite commutative hypergroups and applications*](https://web.maths.unsw.edu.au/~norman/papers/FiniteHypergroupsSurvey.pdf),
  §§2–3, discusses structure constants and the normalization used for orbit
  convolutions. The integral orbit-sum basis and the probability normalization
  use different coefficients.
- [Gallier, *Basics of projective geometry*](https://www.cis.upenn.edu/~jean/gma-v2-chap5.pdf),
  §5.4, pp. 114–115, and §5.5, pp. 124–125, give the three-point projective-line frame, affine
  chart, and common-scale ambiguity of associated bases. The candidate's
  homogeneous polynomial pairs extend ordinary affine formulas as partial
  operations under its explicit undefined-output convention.

## Terminology

Quotient hyperfield, cyclotomic translation scheme, intersection numbers,
orbit sums, homogeneous coordinates, and projective frame.

## Hypotheses

The quotient construction uses the nonzero scalars as a multiplicative
subgroup. The line-minus-endpoints rule with the stated self-sum uses q > 2.
The translation-scheme comparison fixes a single difference z. Framed
coordinates require three distinct points. Frame covariance transports the
three marks together with the operands.

## Negative controls

Raw output-orbit totals multiply each fixed-output coefficient by the size of
its output orbit. Substituting those totals in integral orbit-sum composition
is a different normalization. A zero multiplier collapses all support to one
class and may coalesce multiple coefficients. At q = 2, a repeated nonzero
input has only the zero outcome. A homogeneous pair (0,0) has no projective
class.

## Decision

**Proceed with a narrowed target.** Build an independent exact comparison
and reproducible negative controls over the declared finite fixtures, with
explicit Lean obligations for the general statements. Keep the candidate
classification. The comparison above identifies classical antecedents and
leaves broader prior-art clearance for the shared replay artifact open.
