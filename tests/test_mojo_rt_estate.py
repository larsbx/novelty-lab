"""Replay upstream finite-math-kernels RT vectors against the independent Python oracle.

This is consumer differential conformance, not a second authoritative kernel.
The fixture is byte-identical to upstream conformance/hyperbolic_rt_v1.txt at
the immutable finite-math-kernels commit recorded in vendored.toml.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import tomllib
import unittest

from experiments.rt.independent_reference import SplitQuadratic8, triple_spread_defect

GUARDS_CONTRACT = "Mojo RT estate source pin and independent 48-vector exact conformance"

ROOT = pathlib.Path(__file__).parents[1]
FIXTURE = ROOT / "tests/fixtures/hyperbolic_rt_v1.txt"
UPSTREAM_FIXTURE_SHA1 = "9dc55c38af391e71deb2f2b2f0c898e7084c8cad"
UPSTREAM_COMMIT = "194780a6d314c972c7d066d3da2cae8e21231cba"


class TestMojoEstateRT(unittest.TestCase):
    def test_pinned_mojo_modules(self):
        packages = tomllib.loads((ROOT / "vendored.toml").read_text())["package"]
        by_name = {p["name"]: p for p in packages}
        self.assertTrue({"finite_exact", "projective_limits", "parallel_fold"} <= by_name.keys())
        for name in ("finite_exact", "projective_limits", "parallel_fold"):
            package = by_name[name]
            self.assertEqual(package["repository"], "larsbx/finite-math-kernels")
            self.assertEqual(package["commit"], UPSTREAM_COMMIT)
            self.assertEqual(package["root"], "vendor/mojo")
            for rel, digest in package["files"].items():
                self.assertEqual(hashlib.sha256((ROOT / package["root"] / rel).read_bytes()).hexdigest(), digest)
        manifest = tomllib.loads((ROOT / "ESTATE.toml").read_text())
        deps = {p["id"]: p for p in manifest["dep"]}
        self.assertEqual(deps["finite-math-kernels"]["rev"], UPSTREAM_COMMIT)

    def test_upstream_vectors_against_independent_python_reference(self):
        data = FIXTURE.read_bytes()
        self.assertEqual(
            hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest(),
            UPSTREAM_FIXTURE_SHA1,
        )
        checked = 0
        for raw in data.decode("utf-8").splitlines():
            if not raw or raw.startswith("#"):
                continue
            cells = raw.split("\t")
            kind, p = cells[0], int(cells[1])
            f = SplitQuadratic8(p)
            if kind == "triple":
                _, _, label, a, b, c, expected = cells
                actual = triple_spread_defect(int(a), int(b), int(c), p)
                self.assertEqual(actual, int(expected))
                self.assertEqual(actual == 0, label == "planar")
            else:
                def parse(value):
                    return tuple(int(v) for v in value.split(","))
                if kind == "norm":
                    self.assertEqual(f.norm(parse(cells[2])), int(cells[3]))
                elif kind == "polar":
                    self.assertEqual(f.polar(parse(cells[2]), parse(cells[3])), int(cells[4]))
                elif kind == "spread":
                    value = f.spread(parse(cells[2]), parse(cells[3]))
                    self.assertEqual(value, None if cells[4] == "rejected" else int(cells[4]))
                else:
                    self.fail("unexpected RT vector kind: " + kind)
            checked += 1
        self.assertEqual(checked, 48)


if __name__ == "__main__":
    unittest.main()
