import copy, importlib.util, json, pathlib, subprocess, sys, tempfile, unittest
ROOT=pathlib.Path(__file__).parents[1]
class TestClaimGate(unittest.TestCase):
    def test_repository_ledgers_validate(self):
        p=subprocess.run([sys.executable,str(ROOT/"scripts/check_registry.py")],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
        self.assertIn("0 theorems",p.stdout)
    def test_every_candidate_has_hypotheses_and_obligations(self):
        cs={x["id"] for x in json.loads((ROOT/"research/candidates.json").read_text())["candidates"]}
        hs={x["candidate"] for x in json.loads((ROOT/"research/hypotheses.json").read_text())["hypotheses"]}
        vs={x["candidate"] for x in json.loads((ROOT/"research/obligations.json").read_text())["obligations"]}
        self.assertEqual(cs,hs); self.assertEqual(cs,vs)
    def test_no_hypothesis_is_prematurely_verified(self):
        hs=json.loads((ROOT/"research/hypotheses.json").read_text())["hypotheses"]
        self.assertFalse([h for h in hs if h["status"]=="verified"])
if __name__=="__main__": unittest.main()
