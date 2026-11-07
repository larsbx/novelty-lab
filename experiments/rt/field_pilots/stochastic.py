"""Exact rational two-step scheduler comparison; not a Kuramoto equation."""
from fractions import Fraction as Q


def weights(first, after_a, after_b):
    if first != Q(1,2):
        raise ValueError("fixture first choice distribution requires half/half")
    if not (Q(0) <= after_a <= Q(1) and Q(0) <= after_b <= Q(1)):
        raise ValueError("conditional transition probability outside [0,1]")
    return first*after_a, (Q(1)-first)*after_b


def as_fraction(value):
    return f"{value.numerator}/{value.denominator}"


def run():
    balanced = weights(Q(1,2), Q(1), Q(1))
    biased = weights(Q(1,2), Q(3,4), Q(1,4))
    if not (balanced == (Q(1,2), Q(1,2))
            and biased == (Q(3,8), Q(1,8))):
        raise AssertionError("finite rational schedule counterbalance invalid")
    return {"discipline": "stochastic-processes-control", "status": "bounded-experiment",
            "probability_domain": "Q>=0",
            "balanced_path_weights": tuple(map(as_fraction, balanced)),
            "biased_path_weights": tuple(map(as_fraction, biased)),
            "balanced": balanced[0] == balanced[1],
            "biased": biased[0] != biased[1],
            "two_step_complete_paths_probability": as_fraction(sum(biased)),
            "other_probability_mass": as_fraction(Q(1)-sum(biased)),
            "scope": "two local paths and stopping mass, no global Markov equivalence"}
