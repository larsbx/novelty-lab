"""Replay ordered vector counts, framed operations and plane incidence against exact references."""
import json
import unittest
from pathlib import Path

from experiments.n7 import build_fixture

GUARDS_CONTRACT = "N7 independent finite projective-arithmetic replay and semantic negative controls"


class ProjectiveArithmeticTest(unittest.TestCase):
    def test_exhaustive_fixture(self):
        """Recompute every finite table, including the counts for forbidden substitutions."""
        fixture = Path(__file__).with_name("fixtures") / "n7_projective_arithmetic_v1.json"
        self.assertEqual(build_fixture(), json.loads(fixture.read_text()))
