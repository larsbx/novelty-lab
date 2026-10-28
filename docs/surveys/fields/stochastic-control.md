# Probability, finite dynamical systems and control

**Disciplines:** finite stochastic processes, probability/Markov chains, algebraic finite-state dynamics, network/control modeling. These can have conditional mathematical theorems, exact finite calculations, simulations and empirical model-comparison claims; do not treat them as identical evidence classes.

## Separate probabilistic and algebraic dynamics

A scheduling law over a finite state space can be specified using **rational** nonnegative transition probabilities with normalization in \(\mathbb Q\). This is distinct from field-valued coupling coefficients in \(\mathbb F_q\), which have no compatible order and do not inherently define probabilities.

For a two-step swap \(i,j\) at state \(a\), the local probability comparison
\[
p(i\mid a)\,p(j\mid U_i(a)) \stackrel{?}{=}
p(j\mid a)\,p(i\mid U_j(a))
\]
is independent of computational endpoint equality and independent of geometric spread. Proving this equality for an edge does not alone establish equality of global route-class measures or long-horizon Markov behavior; conditioning, normalization, path multiplicities and context extension require explicit treatment.

A finite-field phase model using a norm-one conic or a discrete map may be **Kuramoto-inspired**, but without a faithful phase/signed-coupling correspondence it is not the continuous-time sine-coupled Kuramoto equation. The symmetric spread value loses orientation/sign information; an oriented alternating form or other extra tensor is needed if direction of interaction matters. A lexicographic repair map is generally not equivariant under all orthogonal transformations.

## Suitable evidence

- A statement about a declared finite Markov chain can be proved by exact matrix calculations or exhaustive enumeration.
- A dynamical law can be studied by periodic orbit counts, reachability, invariant subsets, algebraic identities and finite combinatorics.
- A control or synchronization interpretation must declare a measurable goal; no "attraction" or "small error" can be inferred from an unordered finite-field scalar.
- Simulation can establish bounded behavior in the sampled/complete finite domain, not a universal convergence or robustness theorem.

This domain can progress independently of higher-rank Cayley algebra classification and of unbuilt ML deployment infrastructure. It connects to the exact route interpreter only through a **specified sampling/transition interface**.

**Source:** [cross-disciplinary context](../rt-tensor-route-auditing-context-2026-10-28.md).
