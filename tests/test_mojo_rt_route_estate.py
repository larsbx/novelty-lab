"""Compare consumer fixtures to the established exact P6 oracle, never floats.

The native lane separately replays every expected row through pinned Mojo.
This Python gate checks exhaustive context coverage and the known geometric
false positives, rather than treating a norm-zero residual as equal effect.
"""
import collections
import pathlib
import subprocess
import sys
import tempfile
import tomllib
import unittest

from experiments.rt import route_vectors as vectors
from experiments.rt.p6_lift_pilot import audit_updates

GUARDS_CONTRACT = "Pinned Mojo RT route consumer and exhaustive six-influence differential expectations"

ROOT = pathlib.Path(__file__).parents[1]


class TestMojoRTRouteEstate(unittest.TestCase):
    def test_source_and_native_lane_are_pinned(self):
        packages = tomllib.loads((ROOT / "vendored.toml").read_text())["package"]
        package = next(p for p in packages if p["name"] == "projective_limits")
        self.assertEqual(package["commit"], "3bb94d317b8f0712591b33f9657cf3a0e54207cd")
        self.assertIn("projective_limits/rt_route.mojo", package["files"])
        self.assertFalse((ROOT / "vendor/mojo/finite_graph").exists())
        tasks = tomllib.loads((ROOT / "experiments/rt/pixi.toml").read_text())["tasks"]
        self.assertIn("routes", tasks["conformance"]["depends-on"])
        self.assertEqual(tasks["routes"], "python route_vectors.py --native")

    def test_all_rows_and_negative_controls_match_existing_census(self):
        text = vectors.fixture()
        self.assertEqual(text, vectors.fixture())
        cases = {}
        current = None
        for line in text.splitlines()[1:]:
            c = line.split("\t")
            if c[0] == "case":
                current = (c[1], int(c[2]))
                cases[current] = {"routes": set(), "edges": set(),
                                  "geometry": 0, "effect": 0, "admitted": 0,
                                  "null_nonzero": 0, "positions": collections.Counter()}
            elif c[0] == "route":
                cases[current]["routes"].add(c[1])
            elif c[0] == "swap":
                report = cases[current]
                key = (c[1], int(c[2]))
                self.assertNotIn(key, report["edges"])
                report["edges"].add(key)
                report["positions"][key[1]] += 1
                report["geometry"] += int(c[7])
                report["effect"] += int(c[8])
                report["admitted"] += int(c[9])
                residual = tuple(map(int, c[4].split(",")))
                report["null_nonzero"] += residual != (0,) * 8 and vectors.oracle.F.norm(residual) == 0
        self.assertEqual(tuple(cases), vectors.CASES)
        for (mode, rank), report in cases.items():
            self.assertEqual(len(report["routes"]), 720)
            self.assertEqual(len(report["edges"]), 1800)
            self.assertEqual(report["positions"], dict.fromkeys(range(5), 360))
            # Independently implemented pilot update program vs receipt oracle.
            old, _ = audit_updates(mode, rank)
            self.assertEqual(report["geometry"], old["geometric_passes"])
            self.assertEqual(report["effect"], old["effect_equal"])
            self.assertEqual(report["admitted"], old["certified_swaps"])
            self.assertEqual(report["null_nonzero"], old["nonzero_null_residuals"])
            self.assertEqual(report["geometry"], 1800)
            self.assertEqual(report["admitted"], 1800 if mode == "translations" else 1680)
            self.assertEqual(report["null_nonzero"], 120 if mode == "null_defect" else 0)

    def test_mutations_change_only_temporary_expectations(self):
        good = vectors.fixture()
        for field in ("prefix", "residual", "admission", "duplicate"):
            with self.subTest(field=field):
                self.assertNotEqual(vectors.corrupt(good, field), good)

    def test_fixture_cli_from_pixi_working_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            output = pathlib.Path(directory) / "fixture.tsv"
            subprocess.run([sys.executable, "route_vectors.py", "--output", str(output)],
                           cwd=ROOT / "experiments/rt", check=True)
            self.assertEqual(output.read_text(), vectors.fixture())


if __name__ == "__main__":
    unittest.main()
