"""Exact rational two-example optimizer-order toy, never an LLM benchmark."""
from fractions import Fraction as Q


def sgd_step(w, target, eta=Q(1,2)):
    return w - eta*(w-target)


def momentum_step(state, target, eta=Q(1,2), mu=Q(1,2)):
    w, m = state
    grad = w-target
    next_m = mu*m+grad
    return w-eta*next_m, next_m


def run():
    sgd_ab = sgd_step(sgd_step(Q(0), Q(0)), Q(2))
    sgd_ba = sgd_step(sgd_step(Q(0), Q(2)), Q(0))
    def loss(w):
        return (w-Q(0))**2 + (w-Q(2))**2
    state = (Q(0), Q(0))
    mom_ab = momentum_step(momentum_step(state, Q(0)), Q(2))
    mom_ba = momentum_step(momentum_step(state, Q(2)), Q(0))
    next_ab = momentum_step(mom_ab, Q(0))
    next_ba = momentum_step(mom_ba, Q(0))
    if not (sgd_ab == Q(1) and sgd_ba == Q(1,2)
            and loss(sgd_ab) == Q(2) and loss(sgd_ba) == Q(5,2)
            and mom_ab == (Q(1),Q(-2)) and mom_ba == (Q(1),Q(0))
            and next_ab[0] != next_ba[0]):
        raise AssertionError("optimizer-order fixture mismatch")
    return {"discipline": "machine-learning-optimization", "status": "bounded-toy",
            "numeric_domain": "Q", "examples": 2, "eta": "1/2",
            "sgd_order_ab_weight": str(sgd_ab), "sgd_order_ba_weight": str(sgd_ba),
            "sgd_loss_ab": str(loss(sgd_ab)), "sgd_loss_ba": str(loss(sgd_ba)),
            "momentum_same_weight": mom_ab[0] == mom_ba[0],
            "momentum_distinct_full_state": mom_ab != mom_ba,
            "third_step_divergence": next_ab[0] != next_ba[0],
            "scope": "two scalar rational gradient examples; no floating-point/generalization claims"}
