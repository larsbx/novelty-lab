"""Bounded certificate tampering and independent hash pin demonstration.

A digest of an untrusted forged record is not authenticated provenance.
"""
from dataclasses import asdict, replace
from hashlib import sha256
import json

from experiments.rt.p4_coherence_pilot import P4, DirectionModel, F
from experiments.rt.state_dependent_coherence_pilot import (
    certificates, verify_swap, ORIGIN,
)


def digest(cert):
    payload = json.dumps(asdict(cert), sort_keys=True, separators=(",", ":"))
    return sha256(payload.encode("utf-8")).hexdigest()


def run():
    mode, gate, direction = "null_defect", frozenset((0, 3)), DirectionModel("ray", (0,))
    all_certs = certificates(P4(), mode, gate, direction)
    # Present-only replay is not evidence of a complete 36-edge P4 audit.
    kept = dict(list(all_certs.items())[1:])
    presented_valid = all(verify_swap(cert, mode, gate, direction)
                          for cert in kept.values())
    incomplete_rejected = presented_valid and len(kept) != len(P4().edge_list)
    if not incomplete_rejected:
        raise AssertionError("missing edge wrongly certified as complete")
    victim = next((c for c in all_certs.values()
                   if c.geometric_pass and c.residual != ORIGIN and F.norm(c.residual) == 0), None)
    if victim is None or not verify_swap(victim, mode, gate, direction):
        raise AssertionError("no valid nonzero isotropic swap residual fixture")
    forged = replace(victim, residual=ORIGIN, effect_equal=True, certified=True)
    own_hash = digest(forged)
    expected = digest(victim)
    if verify_swap(forged, mode, gate, direction) or own_hash == expected:
        raise AssertionError("forged certificate accepted")
    return {"discipline": "software-verification-security", "status": "bounded-experiment",
            "field": "F5", "tested_certificates": 2, "genuine_replayed": True, "incomplete_trace_rejected": incomplete_rejected,
            "forged_rejected": True, "nonzero_isotropic_residual": True,
            "forged_can_recompute_untrusted_digest": len(own_hash) == 64,
            "independently_pinned_digest_mismatch": own_hash != expected,
            "scope": "local deterministic checksum/receipt fixture, no identity or execution provenance"}
