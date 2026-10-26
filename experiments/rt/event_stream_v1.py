"""Exact F5 P4/P5 route receipt audit. Consumer experiment; no provenance signatures.

Cell dimension, influence count, tensor direction rank and materialization
are independent. Checks are exact in F5, not claims about floating models.
"""
import hashlib
import itertools
import json

from experiments.rt.p4_coherence_pilot import DirectionModel, P4
from experiments.rt.rank_lift_pilot import F

VERSION = "rt-route-stream/v1"
ZERO = (0,) * 8


def encode(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True, allow_nan=False) + "\n").encode("ascii")


def digest(value):
    return hashlib.sha256(encode(value)).hexdigest()


def _exact_int(value, lo, hi):
    return type(value) is int and lo <= value <= hi


def _vector(values):
    if type(values) is not list or len(values) != 8 or not all(
            _exact_int(x, 0, 4) for x in values):
        raise ValueError("field vector must be eight canonical F5 coordinates")
    return tuple(values)


def validate(spec):
    """Fail closed on unknown operations, fields, order, or coordinates."""
    if type(spec) is not dict or set(spec) != {
            "field", "initial", "updates", "direction_rank", "gate"}:
        raise ValueError("unknown or missing specification field")
    if type(spec["field"]) is not int or spec["field"] != 5:
        raise ValueError("only F5 is supported by this bounded experiment")
    _vector(spec["initial"])
    updates = spec["updates"]
    if type(updates) is not list or not 3 <= len(updates) <= 5:
        raise ValueError("rank must be between three and five influences")
    for i, update in enumerate(updates):
        if type(update) is not dict or set(update) != {
                "id", "offset", "gain", "probe", "shear"}:
            raise ValueError("unknown update operation")
        if type(update["id"]) is not int or update["id"] != i:
            raise ValueError("update IDs must be in canonical order")
        if not _exact_int(update["gain"], 0, 4) or not _exact_int(
                update["probe"], 0, 7):
            raise ValueError("invalid gain/probe")
        offset = _vector(update["offset"])
        _vector(update["shear"])
        if F.norm(offset) == 0:
            raise ValueError("offset direction is null")
    if type(spec["direction_rank"]) is not int or spec["direction_rank"] not in (1, 2):
        raise ValueError("direction rank must be one or two")
    gate = spec["gate"]
    if type(gate) is not list or not gate or gate != sorted(set(gate)) or not all(
            _exact_int(x, 0, 4) for x in gate):
        raise ValueError("gate must be sorted nonempty canonical F5 subset")
    return spec


def directions():
    """Five pairwise orthogonal anisotropic directions in split F5^8."""
    half = pow(2, -1, 5)
    rows = []
    for i in range(4):
        v = [0] * 8
        v[i], v[i + 4] = 1, half
        rows.append(tuple(v))
    w = [0] * 8
    w[0], w[4] = 1, (-half) % 5
    rows.append(tuple(w))
    assert all(F.norm(v) for v in rows)
    return rows


def sample_spec(n=5, mode="translations", rank=1):
    if type(n) is not int or not 3 <= n <= 5:
        raise ValueError("sample rank outside bounded experiment")
    if mode not in ("translations", "coupled", "null_defect"):
        raise ValueError("invalid sample mode")
    if rank not in (1, 2):
        raise ValueError("invalid direction rank")
    offsets = directions()[:n]
    null_v = (1,) + (0,) * 7
    updates = []
    for i, d in enumerate(offsets):
        updates.append({"id": i, "offset": list(d),
                        "gain": int(i == 0 and mode == "coupled"),
                        "probe": 1,
                        "shear": list(null_v if i == 0 and mode == "null_defect"
                                      else ZERO)})
    return validate({"field": 5, "initial": list(ZERO), "updates": updates,
                     "direction_rank": rank,
                     "gate": [0, 3] if mode == "null_defect" else [0]})


def step(x, update):
    coefficient = (1 + update["gain"] * x[update["probe"]]) % 5
    return F.add(F.add(x, F.scalar(coefficient, update["offset"])),
                 F.scalar(x[update["probe"]], update["shear"]))


def route(word, spec):
    x = tuple(spec["initial"])
    for label in word:
        x = step(x, spec["updates"][label])
    return x


def edge_key(a, b):
    return min((a, b), (b, a))


def all_edges(n):
    """Every adjacent swap in the bounded n! permutation graph."""
    edges = set()
    for p in itertools.permutations(range(n)):
        for k in range(n - 1):
            q = p[:k] + (p[k + 1], p[k]) + p[k + 2:]
            edges.add(edge_key(p, q))
    return tuple(sorted(edges))


def checked_requests(n, requests):
    edges = all_edges(n)
    if requests == "all":
        return edges
    if type(requests) is not list:
        raise ValueError("requests must be 'all' or canonical explicit edges")
    parsed = []
    for e in requests:
        if type(e) is not list or len(e) != 2:
            raise ValueError("invalid edge request")
        a, b = e
        if any(type(p) is not list or len(p) != n or not all(
                _exact_int(i, 0, n - 1) for i in p) for p in (a, b)):
            raise ValueError("invalid permutation")
        parsed.append((tuple(a), tuple(b)))
    if tuple(parsed) != tuple(sorted(set(parsed))) or any(e not in edges for e in parsed):
        raise ValueError("edge requests must be unique and canonical")
    return tuple(parsed)


def _subtract(a, b):
    return F.add(a, F.scalar(-1, b))


def compute_record(spec, edge):
    a, b = edge
    positions = [k for k in range(len(a) - 1)
                 if a[:k] + (a[k + 1], a[k]) + a[k + 2:] == b]
    if len(positions) != 1:
        raise ValueError("not an adjacent swap")
    k = positions[0]
    i, j = a[k], a[k + 1]
    prefix = route(a[:k], spec)
    ia = step(prefix, spec["updates"][i])
    jb = step(prefix, spec["updates"][j])
    ab = step(ia, spec["updates"][j])
    ba = step(jb, spec["updates"][i])
    da, db = _subtract(ia, prefix), _subtract(jb, prefix)
    da_after = _subtract(ba, jb)
    db_after = _subtract(ab, ia)
    offsets = [tuple(u["offset"]) for u in spec["updates"]]
    model = DirectionModel("ray" if spec["direction_rank"] == 1 else "grassmann",
                           (0,) if spec["direction_rank"] == 1 else (0, 1))

    def frame(delta, label):
        if spec["direction_rank"] == 1:
            return (delta,)
        return (delta, offsets[(label + 1) % len(offsets)])

    spreads = [model.spread(frame(da, i), frame(da_after, i)),
               model.spread(frame(db, j), frame(db_after, j))]
    residual = _subtract(ab, ba)
    geom = all(s is not None and s in spec["gate"] for s in spreads)
    equal = residual == ZERO
    return {"source": list(a), "target": list(b), "position": k,
            "prefix": list(prefix), "after_a": list(ia), "after_b": list(jb),
            "after_ab": list(ab), "after_ba": list(ba),
            "directions": [list(x) for x in (da, da_after, db, db_after)],
            "spreads": spreads, "residual": list(residual),
            "geometric_pass": geom, "effect_equal": equal, "admitted": geom and equal}


def summary(spec, requests, records):
    n = len(spec["updates"])
    audited = {(tuple(r["source"]), tuple(r["target"])) for r in records}
    admitted = {edge_key(tuple(r["source"]), tuple(r["target"]))
                for r in records if r["admitted"]}
    faces = None
    top = None
    if n == 4:
        poly = P4()
        faces = sum(set(boundary).issubset(admitted)
                    for boundary in poly.face_boundaries.values())
        top = faces == len(poly.cells[2]) and poly.d2d3_zero()
    return {"coherence_labels": n, "direction_rank": spec["direction_rank"],
            "potential_edges": len(all_edges(n)), "audited_edges": len(audited),
            "admitted_edges": len(admitted),
            "geometric_edges": sum(r["geometric_pass"] for r in records),
            "blocked_effect_edges": sum(r["geometric_pass"] and not r["effect_equal"]
                                        for r in records),
            "nonzero_null_residuals": sum(r["residual"] != list(ZERO)
                                          and F.norm(r["residual"]) == 0 for r in records),
            "P4_admitted_faces": faces, "P4_top_cell": top,
            "scope": "complete" if requests == "all" else "requested-only"}


def make_envelope(spec, requests="all"):
    validate(spec)
    edges = checked_requests(len(spec["updates"]), requests)
    records = [compute_record(spec, edge) for edge in edges]
    envelope = {"schema_version": VERSION, "spec": spec,
                "spec_sha256": digest(spec), "requests": requests,
                "records": records, "records_sha256": digest(records),
                "summary": summary(spec, requests, records)}
    return encode(envelope)


def verify_envelope(payload, expected_spec_sha256):
    """Replay untrusted bytes against a separately pinned spec digest."""
    if type(payload) is not bytes or len(payload) > 2_000_000:
        raise ValueError("invalid/oversized audit payload")
    try:
        envelope = json.loads(payload.decode("ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("non-JSON or non-ASCII payload") from exc
    if payload != encode(envelope):
        raise ValueError("noncanonical JSON")
    if type(envelope) is not dict or set(envelope) != {
            "schema_version", "spec", "spec_sha256", "requests", "records",
            "records_sha256", "summary"} or envelope["schema_version"] != VERSION:
        raise ValueError("unknown certificate format")
    validate(envelope["spec"])
    if (type(expected_spec_sha256) is not str or
            digest(envelope["spec"]) != expected_spec_sha256 or
            envelope["spec_sha256"] != expected_spec_sha256):
        raise ValueError("untrusted program specification")
    edges = checked_requests(len(envelope["spec"]["updates"]), envelope["requests"])
    if type(envelope["records"]) is not list or len(envelope["records"]) != len(edges):
        raise ValueError("incomplete record set")
    expected = [compute_record(envelope["spec"], edge) for edge in edges]
    if envelope["records"] != expected or envelope["records_sha256"] != digest(expected):
        raise ValueError("certificate replay failed")
    for record in expected:
        if record["admitted"] and route(record["source"], envelope["spec"]) != route(
                record["target"], envelope["spec"]):
            raise ValueError("certified local equality failed full-route replay")
    result = summary(envelope["spec"], envelope["requests"], expected)
    if envelope["summary"] != result:
        raise ValueError("false summary")
    return result


def pilot():
    full = sample_spec(5, "translations", 1)
    coupled = sample_spec(5, "coupled", 1)
    null_defect = sample_spec(5, "null_defect", 1)
    rank2 = sample_spec(4, "translations", 2)
    runs = {}
    for key, spec in (("frozen_R5", full), ("coupled_R5", coupled),
                      ("null_R5", null_defect), ("grassmann_R4", rank2)):
        payload = make_envelope(spec)
        runs[key] = verify_envelope(payload, digest(spec))
    if (runs["frozen_R5"]["admitted_edges"] != 240 or
            runs["coupled_R5"]["blocked_effect_edges"] != 24 or
            runs["null_R5"]["nonzero_null_residuals"] != 24 or
            not runs["grassmann_R4"]["P4_top_cell"]):
        raise AssertionError("bounded program failed its negative controls")
    sparse = [[list(a), list(b)] for a, b in all_edges(5)[:2]]
    runs["sparse_R5"] = verify_envelope(make_envelope(full, sparse), digest(full))
    return {"status": "bounded-experiment", "version": VERSION, "runs": runs,
            "note": "hashes are not signatures; finite F5 only"}


if __name__ == "__main__":
    print(json.dumps(pilot(), sort_keys=True))
