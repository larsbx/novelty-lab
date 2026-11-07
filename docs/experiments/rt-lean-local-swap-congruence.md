# Proof obligation: prefix-local swap preserves deterministic suffix (Lean, 2026-10-26)

This proof closes one precise semantics obligation of the RT route-auditing research. It is **conditional** on an independently replayed exact *whole-state* local equality; it does not derive equality from RT geometry or hashes.

## Formal statement

For any types State and Event, any total deterministic transition function `step : Event → State → State`, finite prefix `p`, finite suffix `s` and events `a,b`:

```
step b (step a (execute step x p))
= step a (step b (execute step x p))
--------------------------------------------------
execute step x (p ++ [a,b] ++ s)
= execute step x (p ++ [b,a] ++ s)
```

The proof is pure finite List.foldl algebra, specifically `List.foldl_append`, and substitution under a common suffix. It does not use limits, convergence, field order, infinite route search, or complex analysis. This is a general mathematical theorem about deterministic function composition (not a novel theorem); the implementation in `NoveltyLab/RouteAudit.lean` is a Lean-checkable record of the exact premise needed for **sound admission of an effect-certified swap**. It works for high-dimensional tensor states and for a *complete optimizer/RNG state* if that is the declared State.

An observer projection of the complete state inherits the equality by congruence. The converse is **not** established: a noninjective suffix or observer can hide unequal local states, so endpoint-only/audit-observable agreement is weaker than the premise.

## What this does not establish

- RT spread or Grassmann k-plane agreement **does not imply** the required local effect equality.
- No automatic commuting property for state-dependent updates.
- No static P_R or CW attachment homology theorem; signed face incidence is a separate proof/check.
- No differential/ODE/Kuramoto synchronization theorem, no floating-point model equivalence, no proof that F5 approximates an actual LLM training run.
- No cryptographic sender attestation or authenticated transport.

**Acceptance:** the existing Lean oracle pipeline must compile the new `RouteAudit.lean` module by importing it in `Main.lean`; no claimed formal acceptance before hosted check reports success.
