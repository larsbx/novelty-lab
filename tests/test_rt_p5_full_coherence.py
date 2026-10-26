"""Bounded exact P5 CW and F5 state-dependent admission regression suite."""
import unittest
from experiments.rt.event_stream_v1 import digest, make_envelope, sample_spec
from experiments.rt.p5_full_coherence import FullP5, audit_receipt, cube_fvector, homology_profile, run, signed_sum

GUARDS_CONTRACT = "P5 signed cell boundaries, exact F5 homology and effect-certified 4-cell"


class P5Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = FullP5()

    def test_fvector(self):
        self.assertEqual(self.p.face_fvector(), (120,240,150,30,1))
        self.assertEqual(self.p.face_types(), {"squares":90,"hexagons":60,"P4_facets":10,"hexagonal_prisms":20})
        self.assertEqual(self.p.differential_squared(), {})

    def test_orientation_mutant(self):
        top = self.p.cells[4][0]
        bad = dict(self.p.boundary[top])
        key = next(iter(bad))
        bad[key] *= -1
        self.assertTrue(signed_sum((c*d, sub) for face,c in bad.items()
                         for sub,d in self.p.boundary[face].items()))

    def test_homology(self):
        h=homology_profile(self.p)
        self.assertEqual(h["boundary_ranks_F5"], (119,121,29,1))
        self.assertEqual(h["filled_betti_F5"], (1,0,0,0,0))
        self.assertEqual(h["boundary_betti_F5"], (1,0,0,1))

    def test_sparse_closure(self):
        square=next(f for f in self.p.cells[2] if len(self.p.boundary[f])==4)
        facet=next(f for f in self.p.cells[3] if len(self.p.boundary[f])==14)
        self.assertEqual(self.p.requested_closure((square,)), (4,4,1,0,0))
        self.assertEqual(self.p.requested_closure((facet,)), (24,36,14,1,0))
        self.assertEqual(self.p.requested_closure(self.p.cells[4]), (120,240,150,30,1))
        with self.assertRaises(ValueError):
            self.p.requested_closure((((0,1,2,3,4),(0,)),))

    def test_hexagonal_prism_and_hexagon_closure(self):
        hexagon = next(f for f in self.p.cells[2] if len(self.p.boundary[f]) == 6)
        prism = next(f for f in self.p.cells[3] if len(self.p.boundary[f]) == 8)
        self.assertEqual(self.p.requested_closure((hexagon,)), (6,6,1,0,0))
        self.assertEqual(self.p.requested_closure((prism,)), (12,18,8,1,0))

    def test_cube_comparison(self):
        self.assertEqual(cube_fvector(5), (32,80,80,40,10,1))
        self.assertNotEqual(cube_fvector(5), self.p.face_fvector())

    def test_effect_promotion(self):
        for mode, expected in (("translations",(120,240,150,30,1)),
                               ("coupled",(120,216,114,16,0)),
                               ("null_defect",(120,216,114,16,0))):
            spec=sample_spec(5,mode)
            outcome=audit_receipt(self.p,make_envelope(spec),digest(spec))
            self.assertEqual(outcome["admitted_cell_counts"],expected)
            self.assertEqual(outcome["admitted_betti_F5"],
                             (1,0,0,0,0) if mode=="translations"
                             else (2,0,0,0,0))
            self.assertEqual(outcome["admitted_boundary_ranks_F5"],
                             (119,121,29,1) if mode=="translations"
                             else (118,98,16,0))
            self.assertEqual(outcome["top_admitted"],mode=="translations")
            self.assertEqual(outcome["geometric_passes"],240)

    def test_sparse_and_rank2(self):
        spec=sample_spec(5,"translations",2)
        self.assertTrue(audit_receipt(self.p,make_envelope(spec),digest(spec))["top_admitted"])
        sparse=sample_spec(5)
        edges=[[list(a),list(b)] for a,b in sorted(self.p.edge_of.values())[:2]]
        report=audit_receipt(self.p,make_envelope(sparse,edges),digest(sparse))
        self.assertEqual(report["admitted_cell_counts"],(120,2,0,0,0))
        self.assertEqual(report["scope"],"requested-only")

    def test_bounded_summary(self):
        report=run()
        self.assertEqual(report["P5_cells"],(120,240,150,30,1))


if __name__=="__main__":
    unittest.main()
