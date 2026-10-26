"""Canonical incremental six-event F5 route certificates (bounded consumer pilot).

Frame format: custom canonical ASCII JSON object + LF, NOT RFC 7464.
A header, sequenced SHA-256-chained record chunks, and a terminal seal.
Every record is independently replayed from a separately pinned update spec.
No verdict is returned before the terminal seal AND end-of-stream. Hashes are
not signatures, and no real-valued optimizer equivalence is claimed.
"""

import json

from experiments.rt import event_stream_v1 as v1
from experiments.rt import event_stream_v2_p6 as v2
from experiments.rt.p6_lift_pilot import DemandP6, LABELS, N

VERSION = "rt-route-chunks/v1-p6"
MAX_CHUNK_RECORDS = 32
MAX_FRAME_BYTES = 256_000
MAX_STREAM_BYTES = 16_000_000
MAX_FRAMES = 1802  # header + up to 1800 one-record chunks + seal

_HEADER_FIELDS = frozenset({
    "kind", "version", "spec", "spec_sha256", "requests",
    "chunk_size", "expected_edges",
})
_CHUNK_FIELDS = frozenset({
    "kind", "sequence", "previous_sha256", "records", "sha256",
})
_SEAL_FIELDS = frozenset({
    "kind", "chunks", "records", "previous_sha256", "summary", "sha256",
})


def _check_size(raw):
    if type(raw) is not bytes or not 0 < len(raw) <= MAX_FRAME_BYTES:
        raise ValueError("invalid or oversized canonical frame")
    return raw


def _parse(raw):
    raw = _check_size(raw)
    try:
        object_value = json.loads(raw.decode("ascii"))
        if v1.encode(object_value) != raw:
            raise ValueError("noncanonical JSON frame")
    except (UnicodeError, TypeError, ValueError, OverflowError) as exc:
        raise ValueError("invalid or noncanonical JSON frame") from exc
    if type(object_value) is not dict:
        raise ValueError("frame must be a JSON object")
    return object_value


def _frame(body):
    raw = v1.encode(body)
    return _check_size(raw)


def _sealed(body):
    """A frame's hash covers its canonical content WITHOUT its hash field."""
    return _frame({**body, "sha256": v1.digest(body)})


def _new_totals(spec, requests, edges_count):
    return {
        "labels": N,
        "direction_rank": spec["direction_rank"],
        "potential_swaps": len(v1.all_edges(N)),
        "audited_swaps": edges_count,
        "geometric_passes": 0,
        "effect_equal": 0,
        "admitted_swaps": 0,
        "blocked_effects": 0,
        "nonzero_null_residuals": 0,
        "scope": "complete" if requests == "all" else "requested-only",
    }


def _add_record(totals, record):
    totals["geometric_passes"] += int(record["geometric_pass"])
    totals["effect_equal"] += int(record["effect_equal"])
    totals["admitted_swaps"] += int(record["admitted"])
    totals["blocked_effects"] += int(
        record["geometric_pass"] and not record["effect_equal"])
    totals["nonzero_null_residuals"] += int(
        record["residual"] != list(v1.ZERO)
        and v1.F.norm(record["residual"]) == 0)


def emit_frames(spec, requests="all", chunk_size=24):
    """Yield frames incrementally; never accumulate the complete record set."""
    v2.validate_spec(spec)
    if type(chunk_size) is not int or not 1 <= chunk_size <= MAX_CHUNK_RECORDS:
        raise ValueError("invalid bounded records-per-chunk")
    edges = v1.checked_requests(N, requests)
    header = {
        "kind": "header", "version": VERSION, "spec": spec,
        "spec_sha256": v1.digest(spec), "requests": requests,
        "chunk_size": chunk_size, "expected_edges": len(edges),
    }
    yield _frame(header)
    previous = v1.digest(header)
    totals = _new_totals(spec, requests, len(edges))
    emitted = 0
    index = 0
    while emitted < len(edges):
        group = edges[emitted:emitted + chunk_size]
        records = [v1.compute_record(spec, edge) for edge in group]
        for record in records:
            _add_record(totals, record)
        body = {
            "kind": "chunk", "sequence": index,
            "previous_sha256": previous, "records": records,
        }
        yield _sealed(body)
        previous = v1.digest(body)
        emitted += len(records)
        index += 1
    seal = {
        "kind": "seal", "chunks": index, "records": emitted,
        "previous_sha256": previous, "summary": totals,
    }
    yield _sealed(seal)


def verify_frames(frames, expected_spec_sha256, requested_faces=(),
                  max_cells=None):
    """Check byte frames one-by-one; return results only on seal plus EOF.

    Memory holds at most a bounded records chunk, the 1800 canonical edge
    keys, and the set of admitted edges needed to verify requested P6 cells.
    It does not retain the whole submitted list of record dictionaries.
    """
    iterator = iter(frames)
    observed_bytes = 0
    observed_frames = 0

    def next_frame():
        nonlocal observed_bytes, observed_frames
        if observed_frames >= MAX_FRAMES:
            raise ValueError("frame count budget exceeded")
        try:
            raw = next(iterator)
        except StopIteration as exc:
            raise ValueError("stream truncated: missing chunk or final seal") from exc
        _check_size(raw)
        observed_bytes += len(raw)
        observed_frames += 1
        if observed_bytes > MAX_STREAM_BYTES:
            raise ValueError("total byte budget exceeded")
        return _parse(raw)

    header = next_frame()
    if set(header) != _HEADER_FIELDS or header["kind"] != "header" or (
            header["version"] != VERSION):
        raise ValueError("invalid stream header")
    spec = v2.validate_spec(header["spec"])
    if (type(expected_spec_sha256) is not str
            or expected_spec_sha256 != v1.digest(spec)
            or header["spec_sha256"] != expected_spec_sha256):
        raise ValueError("untrusted specification pin")
    size = header["chunk_size"]
    if type(size) is not int or not 1 <= size <= MAX_CHUNK_RECORDS:
        raise ValueError("invalid advertised chunk size")
    edges = v1.checked_requests(N, header["requests"])
    if (type(header["expected_edges"]) is not int
            or header["expected_edges"] != len(edges)):
        raise ValueError("untrusted claimed edge coverage")
    totals = _new_totals(spec, header["requests"], len(edges))
    previous = v1.digest(header)
    admitted_edges = set()
    checked = 0
    chunk_index = 0

    while checked < len(edges):
        chunk = next_frame()
        if set(chunk) != _CHUNK_FIELDS or chunk["kind"] != "chunk":
            raise ValueError("missing or malformed stream chunk")
        core = {key: val for key, val in chunk.items() if key != "sha256"}
        if (type(chunk["sequence"]) is not int
                or chunk["sequence"] != chunk_index
                or chunk["previous_sha256"] != previous
                or chunk["sha256"] != v1.digest(core)):
            raise ValueError("chunk sequence, hash chain, or digest mismatch")
        records = chunk["records"]
        count = min(size, len(edges) - checked)
        if type(records) is not list or len(records) != count:
            raise ValueError("chunk coverage is incomplete or overfull")
        for offset, received in enumerate(records):
            edge = edges[checked + offset]
            expected = v1.compute_record(spec, edge)
            if received != expected:
                raise ValueError("exact record replay mismatch")
            if expected["admitted"]:
                if v1.route(edge[0], spec) != v1.route(edge[1], spec):
                    raise ValueError("admitted effect changed full route")
                admitted_edges.add(edge)
            _add_record(totals, expected)
        checked += count
        chunk_index += 1
        previous = v1.digest(core)

    seal = next_frame()
    if set(seal) != _SEAL_FIELDS or seal["kind"] != "seal":
        raise ValueError("missing or invalid final seal")
    core = {key: val for key, val in seal.items() if key != "sha256"}
    if (type(seal["chunks"]) is not int or seal["chunks"] != chunk_index
            or type(seal["records"]) is not int or seal["records"] != checked
            or seal["previous_sha256"] != previous
            or seal["sha256"] != v1.digest(core)
            or seal["summary"] != totals):
        raise ValueError("invalid terminal seal or false audit summary")
    sentinel = object()
    if next(iterator, sentinel) is not sentinel:
        raise ValueError("extra data after terminal seal")

    result = dict(totals)
    result["stream_version"] = VERSION
    result["chunks"] = chunk_index
    result["end_of_stream_verified"] = True
    result["seal_sha256"] = seal["sha256"]
    if type(requested_faces) not in (tuple, list):
        raise ValueError("face requests must be a sequence")
    if requested_faces:
        cache = DemandP6()
        closure = cache.request(requested_faces, max_cells=max_cells)
        if cache.chain_defects():
            raise ValueError("nonzero cellular boundary composition")
        profile = cache.admitted_profile(admitted_edges)
        result["face_witness"] = {
            "materialized": closure["cells_by_dimension"],
            "admitted": profile["admitted_cells"],
            "requested_admitted": all(
                v2._face_admitted(face, cache, admitted_edges)
                for face in requested_faces),
            "top_admitted": (
                (LABELS,) in cache.boundaries
                and profile["admitted_cells"] == cache.counts()
                and totals["scope"] == "complete"),
        }
    return result


def experiment():
    """Reproduce a sealed complete stream and a requested-only square."""
    frozen = v2.sample_spec("translations", 1)
    coupled = v2.sample_spec("scalar_coupled", 1)
    full = verify_frames(emit_frames(frozen, chunk_size=24), v1.digest(frozen))
    negative = verify_frames(emit_frames(coupled, chunk_size=19), v1.digest(coupled))
    square = ((0, 1), (2, 3), (4,), (5,))
    local = DemandP6()
    local.request((square,))
    pairs = []
    for face in local.boundaries:
        if len(face) == N - 1:
            ends = sorted(tuple(block[0] for block in vertex)
                          for vertex in local.boundaries[face])
            pairs.append(tuple(ends))
    requests = [[list(a), list(b)] for a, b in sorted(pairs)]
    sparse = verify_frames(
        emit_frames(frozen, requests=requests, chunk_size=2),
        v1.digest(frozen), requested_faces=(square,), max_cells=9)
    if (full["admitted_swaps"] != 1800
            or negative["blocked_effects"] != 120
            or sparse["audited_swaps"] != 4
            or not sparse["face_witness"]["requested_admitted"]
            or sparse["face_witness"]["top_admitted"]):
        raise AssertionError("bounded incremental acceptance mismatch")
    return {
        "status": "bounded-experiment",
        "full": {key: full[key] for key in (
            "audited_swaps", "admitted_swaps", "chunks",
            "end_of_stream_verified", "scope")},
        "state_dependent": {key: negative[key] for key in (
            "audited_swaps", "admitted_swaps", "blocked_effects", "chunks")},
        "square": sparse["face_witness"],
        "security_note": "hash chain verifies integrity, not author identity",
    }


if __name__ == "__main__":
    print(json.dumps(experiment(), sort_keys=True))
