#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).parents[1]
def load(name): return json.loads((ROOT/"research"/name).read_text(encoding="utf-8"))
def unique(rows,key,label):
    vals=[r[key] for r in rows]; assert len(vals)==len(set(vals)), f"duplicate {label}"
def artifact(path):
    p=path.split("#",1)[0]
    assert p and (ROOT/p).is_file(), f"missing evidence artifact: {path}"

candidates=load("candidates.json")["candidates"]
hypotheses=load("hypotheses.json")["hypotheses"]
obligations=load("obligations.json")["obligations"]
theorems=load("theorems.json")["theorems"]
retired=load("retired_claims.json")["retired_claims"]
candidate_ids={x["id"] for x in candidates}
for rows,key,label in [(candidates,"id","candidate id"),(hypotheses,"id","hypothesis id"),(obligations,"id","obligation id"),(theorems,"id","theorem id"),(retired,"id","retired-claim id")]: unique(rows,key,label)
hyp={x["id"]:x for x in hypotheses}; obl={x["id"]:x for x in obligations}
allowed_claims={"candidate","literature-cleared candidate","experimental result","proved result","artifact contribution","novel result"}
for x in candidates:
    assert x["status"] in allowed_claims and x["status"]!="novel result"
    assert x["gates"] and x["claims"]
    assert all(d in candidate_ids for d in x["dependencies"])
for h in hypotheses:
    assert h["candidate"] in candidate_ids and h["id"].startswith(h["candidate"]+"-H")
    assert h["status"] in {"proposed","pinned","verified","refuted"}
    assert h["statement"].strip() and h["scope"].strip()
    if h["status"]=="verified":
        assert h["verified_by"], f"{h['id']}: verified without evidence"
        for e in h["verified_by"]: artifact(e)
    else: assert not h["verified_by"], f"{h['id']}: evidence requires verified status"
for v in obligations:
    assert v["candidate"] in candidate_ids and v["id"].startswith(v["candidate"]+"-V")
    assert v["class"] in {"structural","computational","certificate","formal","literature","proof"}
    assert v["status"] in {"open","verified","failed"} and v["description"].strip()
    assert all(d in hyp and hyp[d]["candidate"]==v["candidate"] for d in v["depends_on"])
    if v["status"]=="verified":
        assert v["evidence"], f"{v['id']}: verified without evidence"
        for e in v["evidence"]: artifact(e)
    else: assert not v["evidence"], f"{v['id']}: evidence requires verified status"
for t in theorems:
    cid=t["candidate"]; assert cid in candidate_ids and t["id"].startswith(cid+"-T")
    assert t["statement"].strip() and t["proof_artifact"].strip(); artifact(t["proof_artifact"])
    assert t["claim_class"] in {"proved result","artifact contribution"}
    assert t["novelty_status"] in {"classical; not novel","classical consequence; not novel","bridge novelty unassessed; identity is elementary"}
    assert t["hypotheses"] and t["obligations"]
    assert all(h in hyp and hyp[h]["status"]=="verified" and hyp[h]["candidate"]==cid for h in t["hypotheses"])
    assert all(v in obl and obl[v]["status"]=="verified" and obl[v]["candidate"]==cid for v in t["obligations"])
for r in retired:
    assert r["candidate"] in candidate_ids and r["status"]=="killed"
    assert r["claim"].strip() and r["reason"].strip() and r["salvage"].strip()
print(f"validated {len(candidate_ids)} candidates, {len(hyp)} hypotheses, {len(obl)} obligations, {len(theorems)} theorems, {len(retired)} killed claims")
