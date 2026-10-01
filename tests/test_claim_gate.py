import json, pathlib, subprocess, sys, unittest
ROOT=pathlib.Path(__file__).parents[1]
class TestClaimGate(unittest.TestCase):
    def test_repository_ledgers_validate(self):
        p=subprocess.run([sys.executable,str(ROOT/"scripts/check_registry.py")],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
        self.assertIn("3 theorems",p.stdout)
        self.assertIn("7 killed claims",p.stdout)
    def test_every_candidate_has_hypotheses_and_obligations(self):
        cs={x["id"] for x in json.loads((ROOT/"research/candidates.json").read_text())["candidates"]}
        hs={x["candidate"] for x in json.loads((ROOT/"research/hypotheses.json").read_text())["hypotheses"]}
        vs={x["candidate"] for x in json.loads((ROOT/"research/obligations.json").read_text())["obligations"]}
        self.assertEqual(cs,hs); self.assertEqual(cs,vs)
    def test_only_promoted_hypotheses_are_verified(self):
        hs=json.loads((ROOT/"research/hypotheses.json").read_text())["hypotheses"]
        verified={h["id"] for h in hs if h["status"]=="verified"}
        self.assertEqual(verified,{"N1-H09","N2-H06","N3-H06"})
        for h in hs:
            if h["id"] in verified: self.assertTrue(h["verified_by"])
            else: self.assertNotEqual(h["status"],"verified")
    def test_promoted_theorems_are_not_novelty_claims(self):
        ts=json.loads((ROOT/"research/theorems.json").read_text())["theorems"]
        self.assertEqual({t["id"] for t in ts},{"N1-T01","N2-T01","N3-T01"})
        self.assertTrue(all("novel" in t["novelty_status"] or "unassessed" in t["novelty_status"] for t in ts))
        self.assertTrue(all(not t["novelty_status"].startswith("novel result") for t in ts))
if __name__=="__main__": unittest.main()
