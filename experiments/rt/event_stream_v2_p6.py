"""Independently pinned canonical v2 receipts for EXACTLY six F5 influences.

The version-one stream still rejects six events. This is a bounded
consumer-specific audit; no signature or floating-model guarantee.
An exact affine update program and every local prefix are explicitly replayed.
"""

import json

from experiments.rt import event_stream_v1 as v1
from experiments.rt.p6_lift_pilot import (
    DemandP6, DIRECTIONS, LABELS, NULL_E0, N, ORIGIN,
)

VERSION = "rt-route-stream/v2-p6"
LANGUAGE = "F5-affine-vector-update/v1"
MAX_RECEIPT_BYTES = 12_000_000


def validate_spec(spec):
    """Strict independent validation; never trust the spec's own digest."""
    if type(spec) is not dict or set(spec) != {
            "field", "initial", "updates", "direction_rank", "gate", "semantics"}:
        raise ValueError("malformed six-influence update spec")
    if type(spec["field"]) is not int or spec["field"] != 5:
        raise ValueError("unsupported exact field")
    if type(spec["semantics"]) is not str or spec["semantics"] != LANGUAGE:
        raise ValueError("unrecognized update interpretation")
    v1._vector(spec["initial"])
    updates = spec["updates"]
    if type(updates) is not list or len(updates) != N:
        raise ValueError("v2 requires exactly six canonical updates")
    for i, update in enumerate(updates):
        if type(update) is not dict or set(update) != {
                "id", "offset", "gain", "probe", "shear"}:
            raise ValueError("malformed update")
        if type(update["id"]) is not int or update["id"] != i:
            raise ValueError("updates must have canonical order")
        v1._vector(update["offset"])
        v1._vector(update["shear"])
        if v1.F.norm(update["offset"]) == 0:
            raise ValueError("null reference offset")
        if (type(update["probe"]) is not int or not 0 <= update["probe"] < 8 or
                type(update["gain"]) is not int or
                not 0 <= update["gain"] < 5):
            raise ValueError("invalid probe or gain")
    if (type(spec["direction_rank"]) is not int or
            spec["direction_rank"] not in (1, 2)):
        raise ValueError("unrecognized tensor direction rank")
    gate = spec["gate"]
    if (type(gate) is not list or not gate or
            gate != sorted(set(gate)) or
            any(type(s) is not int or not 0 <= s < 5 for s in gate)):
        raise ValueError("invalid finite-field gate")
    return spec


def sample_spec(mode="translations", direction_rank=1):
    """Explicit typed program; never reinterpret a v1 three-to-five input."""
    if mode not in ("translations", "scalar_coupled", "null_defect"):
        raise ValueError("unknown exact model")
    updates = []
    for i in LABELS:
        updates.append({
            "id": i, "offset": list(DIRECTIONS[i]), "probe": 1,
            "gain": int(mode == "scalar_coupled" and i == 0),
            "shear": list(NULL_E0 if mode == "null_defect" and i == 0
                          else ORIGIN),
        })
    return validate_spec({
        "field": 5, "initial": list(ORIGIN), "updates": updates,
        "direction_rank": direction_rank,
        "gate": [0, 3] if mode == "null_defect" else [0],
        "semantics": LANGUAGE,
    })


def summary(spec, requests, records):
    return {
        "labels": N,
        "direction_rank": spec["direction_rank"],
        "potential_swaps": len(v1.all_edges(N)),
        "audited_swaps": len(records),
        "geometric_passes": sum(r["geometric_pass"] for r in records),
        "effect_equal": sum(r["effect_equal"] for r in records),
        "admitted_swaps": sum(r["admitted"] for r in records),
        "blocked_effects": sum(r["geometric_pass"] and not r["effect_equal"]
                               for r in records),
        "nonzero_null_residuals": sum(
            r["residual"] != list(ORIGIN) and
            v1.F.norm(r["residual"]) == 0 for r in records),
        "scope": "complete" if requests == "all" else "requested-only",
    }


def create_receipt(spec, requests="all"):
    validate_spec(spec)
    edges = v1.checked_requests(N, requests)
    records = [v1.compute_record(spec, edge) for edge in edges]
    receipt = {
        "schema_version": VERSION, "spec": spec,
        "spec_sha256": v1.digest(spec), "requests": requests,
        "records": records, "records_sha256": v1.digest(records),
        "summary": summary(spec, requests, records),
    }
    payload = v1.encode(receipt)
    if len(payload) > MAX_RECEIPT_BYTES:
        raise ValueError("receipt exceeds finite byte budget")
    return payload


def verify_receipt(payload, expected_spec_sha256, requested_faces=(),
                   max_cells=None):
    """Deterministically replay, then optionally materialize P6 face closure.

    expected_spec_sha256 MUST come from a trusted channel independent of the
    receipt; integrity hashes are not signatures.
    """
    if type(payload) is not bytes or len(payload) > MAX_RECEIPT_BYTES:
        raise ValueError("invalid or over-budget byte payload")
    try:
        document = json.loads(payload.decode("ascii"))
    except (UnicodeError, ValueError) as exc:
        raise ValueError("invalid canonical ASCII JSON") from exc
    try:
        canonical = v1.encode(document)
    except (TypeError, ValueError) as exc:
        raise ValueError("invalid canonical JSON structure") from exc
    if canonical != payload:
        raise ValueError("noncanonical JSON bytes")
    if type(document) is not dict or set(document) != {
            "schema_version", "spec", "spec_sha256", "requests", "records",
            "records_sha256", "summary"} or document["schema_version"] != VERSION:
        raise ValueError("invalid route-stream v2 envelope")
    spec = validate_spec(document["spec"])
    if (type(expected_spec_sha256) is not str or
            v1.digest(spec) != expected_spec_sha256 or
            document["spec_sha256"] != expected_spec_sha256):
        raise ValueError("untrusted or altered program pin")
    edges = v1.checked_requests(N, document["requests"])
    records = document["records"]
    if type(records) is not list or len(records) != len(edges):
        raise ValueError("incomplete route record list")
    expected = [v1.compute_record(spec, edge) for edge in edges]
    if records != expected or document["records_sha256"] != v1.digest(expected):
        raise ValueError("exact route certificate replay failed")
    for record in expected:
        if record["admitted"] and v1.route(record["source"], spec) != v1.route(
                record["target"], spec):
            raise ValueError("invalid admitted full route")
    result = summary(spec, document["requests"], expected)
    if document["summary"] != result:
        raise ValueError("false claimed audit summary")

    if type(requested_faces) not in (tuple, list):
        raise ValueError("requested faces must be a sequence")
    if requested_faces:
        cache = DemandP6()
        materialized = cache.request(requested_faces, max_cells=max_cells)
        if cache.chain_defects():
            raise ValueError("bad cellular face boundary")
        certified = {
            tuple(sorted((tuple(r["source"]), tuple(r["target"]))))
            for r in expected if r["admitted"]
        }
        profile = cache.admitted_profile(certified)
        # The full top is admitted only by complete boundary closure;
        # requested-only receipts never have that authority.
        result = dict(result)
        result["face_witness"] = {
            "materialized": materialized["cells_by_dimension"],
            "admitted": profile["admitted_cells"],
            "betti_F5": profile["betti_F5"],
            "requested_admitted": all(
                # A requested face cannot be admitted if any of its facets
                # are not in the admitted signed closure.
                _face_admitted(f, cache, certified) for f in requested_faces),
            "top_admitted": cache.counts() == (
                720, 1800, 1560, 540, 62, 1) and
                profile["admitted_cells"] == cache.counts() and
                result["scope"] == "complete",
        }
    return result


def _face_admitted(face, cache, certified):
    """Exact recursively closed certificate check for a given face."""
    if face not in cache.boundaries:
        return False
    if len(face) == N:
        return True
    if len(face) == N - 1:
        pair = sorted(tuple(block[0] for block in v)
                      for v in cache.boundaries[face])
        return tuple(pair) in certified
    return all(_face_admitted(f, cache, certified)
               for f in cache.boundaries[face])


def experiment():
    complete = {}
    for name in ("translations", "scalar_coupled", "null_defect"):
        spec = sample_spec(name)
        complete[name] = verify_receipt(
            create_receipt(spec), v1.digest(spec))
    spec2 = sample_spec("translations", 2)
    top = (LABELS,)
    rank2 = verify_receipt(create_receipt(spec2), v1.digest(spec2),
                           requested_faces=(top,))
    tiny = sample_spec()
    two = [[list(a), list(b)] for a, b in v1.all_edges(N)[:2]]
    sparse = verify_receipt(create_receipt(tiny, two), v1.digest(tiny),
                            requested_faces=(top,))
    if (complete["translations"]["admitted_swaps"] != 1800 or
            complete["scalar_coupled"]["blocked_effects"] != 120 or
            complete["null_defect"]["nonzero_null_residuals"] != 120 or
            not rank2["face_witness"]["top_admitted"] or
            sparse["face_witness"]["top_admitted"]):
        raise AssertionError("six-event v2 bounded controls failed")
    return {
        "status": "bounded-experiment", "schema_version": VERSION,
        "full": complete,
        "grassmann_rank2_top": rank2["face_witness"],
        "requested_only_top": sparse["face_witness"],
        "trust": "digest checked against external pin; not authenticated origin",
    }


if __name__ == "__main__":
    print(json.dumps(experiment(), sort_keys=True))
