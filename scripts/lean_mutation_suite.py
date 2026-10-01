#!/usr/bin/env python3
"""Mutation suite for the Lean pentagon oracle: which self-checks kill each mutant of Oracle.lean.

Each mutant replaces one exact source fragment of NoveltyLab/Oracle.lean,
rebuilds with `lake build`, runs `lake exe oracle-selfcheck`, and records the
names of the checks reported FAIL. The original file is restored afterwards,
whatever happens. The baseline (no mutation) must pass every check.

Requires a Lean toolchain (lean-toolchain) on PATH; not part of the Python CI.
Usage: lean_mutation_suite.py        writes data/n2/oracle-mutants-v1.json
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORACLE = ROOT / "NoveltyLab" / "Oracle.lean"
OUT = ROOT / "data" / "n2" / "oracle-mutants-v1.json"

MUTANTS = (
    ("drop sign of [a,b,cd]", "    neg p (assoc p t a b (mul p t c d)),", "    assoc p t a b (mul p t c d),"),
    ("d[a,b,c] for [a,b,c]d", "#[mul p t (assoc p t a b c) d,", "#[mul p t d (assoc p t a b c),"),
    ("[bc,a,d] for [a,bc,d]", "    assoc p t a (mul p t b c) d,", "    assoc p t (mul p t b c) a d,"),
    ("negated associator", "  sub p (mul p t x (mul p t y z)) (mul p t (mul p t x y) z)",
     "  sub p (mul p t (mul p t x y) z) (mul p t x (mul p t y z))"),
    ("(ba) for (ab) in [ab,c,d]", "    neg p (assoc p t (mul p t a b) c d)]", "    neg p (assoc p t (mul p t b a) c d)]"),
    ("transposed tensor", "x[i]! * y[j]! * t[i]![j]![k]!", "x[i]! * y[j]! * t[j]![i]![k]!"),
)


def run_selfcheck() -> tuple[bool, list[str]]:
    build = subprocess.run(["lake", "build"], cwd=ROOT, capture_output=True, text=True)
    if build.returncode:
        return False, ["<build failed>"]
    out = subprocess.run(["lake", "exe", "oracle-selfcheck"], cwd=ROOT, capture_output=True, text=True)
    failed = [line[5:].strip() for line in out.stdout.splitlines() if line.startswith("FAIL")]
    return out.returncode == 0 and not failed, failed


def main() -> int:
    original = ORACLE.read_text(encoding="utf-8")
    passed, failed = run_selfcheck()
    if not passed:
        print(f"baseline does not pass: {failed}", file=sys.stderr)
        return 1
    rows = []
    try:
        for name, old, new in MUTANTS:
            if original.count(old) != 1:
                print(f"mutant {name!r}: fragment not found exactly once", file=sys.stderr)
                return 1
            ORACLE.write_text(original.replace(old, new), encoding="utf-8")
            survived, failed = run_selfcheck()
            rows.append({"mutant": name, "killed": not survived, "failing_checks": failed})
            print(f"{'SURVIVED' if survived else 'killed  '} {name} ({len(failed)} checks fail)")
    finally:
        ORACLE.write_text(original, encoding="utf-8")
        run_selfcheck()
    toolchain = (ROOT / "lean-toolchain").read_text(encoding="utf-8").strip()
    OUT.write_text(json.dumps({"schema": "novelty-lab/oracle-mutants/v1", "lean_toolchain": toolchain,
                               "oracle_sha256": hashlib.sha256(original.encode()).hexdigest(),
                               "mutants": rows}, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")
    return 0 if all(r["killed"] for r in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
