import Std

/-!
# Conditional local-swap congruence for exact route auditing

A verified equality at the actual prefix state implies equality after an
identical deterministic suffix. The state type is unrestricted and may
contain complete model/optimizer/RNG state. This proof does NOT infer
operational independence from RT spread, Gram rank, or a hash receipt.
-/

namespace NoveltyLab.RouteAudit

universe u v

variable {State : Type u} {Event : Type v}

/-- Execute a finite list of ordered events with the provided total step map. -/
def execute (step : Event → State → State) (start : State)
    (events : List Event) : State :=
  events.foldl (fun state event => step event state) start

theorem execute_append (step : Event → State → State) (start : State)
    (prefix suffix : List Event) :
    execute step start (prefix ++ suffix) =
      execute step (execute step start prefix) suffix := by
  simp [execute, List.foldl_append]

/-- An exact equality of two locally swapped events at the *actual prefix*
is sufficient to preserve every common deterministic suffix. No cancellation
or injectivity of the suffix is needed for this forward implication. -/
theorem exact_swap_preserves_suffix (step : Event → State → State)
    (start : State) (prefix suffix : List Event) (a b : Event)
    (h : step b (step a (execute step start prefix)) =
         step a (step b (execute step start prefix))) :
    execute step start (prefix ++ [a, b] ++ suffix) =
      execute step start (prefix ++ [b, a] ++ suffix) := by
  calc
    execute step start (prefix ++ [a, b] ++ suffix) =
        execute step (step b (step a (execute step start prefix))) suffix := by
          simp [execute_append, execute]
    _ = execute step (step a (step b (execute step start prefix))) suffix := by
          rw [h]
    _ = execute step start (prefix ++ [b, a] ++ suffix) := by
          simp [execute_append, execute]

/-- A deterministic observer of the complete state inherits a locally
certified swap equality; this is not a stronger equality than the premise. -/
theorem exact_swap_preserves_observer (step : Event → State → State)
    (start : State) (prefix suffix : List Event) (a b : Event)
    {Observation : Type} (observe : State → Observation)
    (h : step b (step a (execute step start prefix)) =
         step a (step b (execute step start prefix))) :
    observe (execute step start (prefix ++ [a, b] ++ suffix)) =
      observe (execute step start (prefix ++ [b, a] ++ suffix)) := by
  exact congrArg observe
    (exact_swap_preserves_suffix step start prefix suffix a b h)

end NoveltyLab.RouteAudit
