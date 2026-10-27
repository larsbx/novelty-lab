"""Consumer-only differential fixtures from the established six-event oracle.

This is not a new arithmetic implementation or a receipt transport. Temporary
TSV expectations drive route_smoke.mojo; Python retains acceptance authority.
Run --native inside the pinned Pixi environment to build once, replay every
row, and require native refusal of altered/truncated expectations.
"""
from __future__ import annotations

import argparse
import itertools
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from experiments.rt import event_stream_v1 as oracle
from experiments.rt.event_stream_v2_p6 import sample_spec

CASES = (("translations", 1), ("scalar_coupled", 1),
         ("null_defect", 1), ("translations", 2))


def csv(values):
    return ",".join(map(str, values))


def fixture():
    """All 720 routes and 1800 canonical edges, for each reviewed case."""
    rows = ["rt-route-differential/v1"]
    edges = oracle.all_edges(6)
    for mode, rank in CASES:
        spec = sample_spec(mode, rank)
        rows.append(f"case\t{mode}\t{rank}\t{csv(spec['gate'])}")
        rows.append("initial\t" + csv(spec["initial"]))
        for u in spec["updates"]:
            rows.append("\t".join(map(str, (
                "update", u["id"], csv(u["offset"]), u["gain"],
                u["probe"], csv(u["shear"]),
            ))))
        for word in itertools.permutations(range(6)):
            rows.append("\t".join(("route", csv(word),
                                    csv(oracle.route(word, spec)))))
        for edge in edges:
            r = oracle.compute_record(spec, edge)
            rows.append("\t".join(map(str, (
                "swap", csv(r["source"]), r["position"], csv(r["prefix"]),
                csv(r["residual"]),
                *("rejected" if s is None else s for s in r["spreads"]),
                int(r["geometric_pass"]), int(r["effect_equal"]),
                int(r["admitted"]),
            ))))
        rows.append("end")
    return "\n".join(rows) + "\n"


def corrupt(text, field):
    """Alter a single expected field without touching committed evidence."""
    rows = text.splitlines()
    for i, line in enumerate(rows):
        cells = line.split("\t")
        if cells[0] == "swap":
            if field == "residual":
                cells[4] = "1,0,0,0,0,0,0,0"
            elif field == "prefix":
                cells[3] = "1,0,0,0,0,0,0,0"
            elif field == "admission":
                cells[9] = "0"
            elif field == "duplicate":
                rows[i + 1] = line
                return "\n".join(rows) + "\n"
            else:
                raise ValueError(field)
            rows[i] = "\t".join(cells)
            return "\n".join(rows) + "\n"
    raise ValueError("missing swap")


def native():
    with tempfile.TemporaryDirectory(prefix="rt-route-") as directory:
        tmp = Path(directory)
        binary = tmp / "route_smoke"
        subprocess.run([
            "mojo", "build", "-I", str(ROOT / "vendor/mojo"),
            str(ROOT / "experiments/rt/route_smoke.mojo"), "-o", str(binary),
        ], check=True)
        good = fixture()
        path = tmp / "expectations.tsv"
        path.write_text(good, encoding="ascii")
        subprocess.run([str(binary), str(path)], check=True)
        for name, bad in (
            *((name, corrupt(good, name)) for name in
              ("residual", "prefix", "admission", "duplicate")),
            ("truncated", "\n".join(good.splitlines()[:-2]) + "\n"),
        ):
            path.write_text(bad, encoding="ascii")
            result = subprocess.run([str(binary), str(path)],
                                    capture_output=True, text=True)
            if result.returncode == 0:
                raise AssertionError(f"native consumer accepted {name} mutation")
            print(f"[PASS] native consumer refused {name} mutation", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument("--output", type=Path)
    choice.add_argument("--native", action="store_true")
    args = parser.parse_args()
    if args.native:
        native()
    else:
        args.output.write_text(fixture(), encoding="ascii")


if __name__ == "__main__":
    main()
