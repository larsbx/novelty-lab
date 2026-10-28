"""Exact failure of naïve F5-to-integer effect-equality transfer."""


def add_five(x):
    return x+5


def double(x):
    return 2*x


def run():
    x=1
    left=double(add_five(x))
    right=add_five(double(x))
    if not (left == 12 and right == 7 and left != right and left % 5 == right % 5):
        raise AssertionError("nonfaithful reduction control failed")
    return {"discipline": "cross-field-abstraction", "status": "refutation-of-naive-transfer",
            "source_domain": "Z", "target_domain": "F5",
            "integer_ab": left, "integer_ba": right,
            "integer_effect_equal": False,
            "field_effect_equal": left % 5 == right % 5,
            "nonzero_integer_defect": left-right,
            "defect_reduced_to_zero": (left-right) % 5 == 0,
            "scope": "one explicit noninjective projection; no real training transfer"}
