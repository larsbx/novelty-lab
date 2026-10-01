#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).parents[1]
def load(name): return json.loads((ROOT/"research"/name).read_text(encoding="utf-8"))
def unique(rows,key,label):
    vals=[r[key] for r in rows]
    assert len(vals)==len(set(vals)), f"duplicate {label}"

candidates=load("candidates.json")["candidates"]
hypotheses=load("hypotheses.json")["hypotheses"]
obligations=load("obligations.json")["obligations"]
theorems=load("theorems.json")["theorems"]
candidate_ids={x["id"] for x in candidates}
unique(candidates,"id","candidate id"); unique(hypotheses,"id","hypothesis id")
unique(obligations,"id","obligation id"); unique(theorems,"id","theorem id")
hyp={x["id"]:x for x in hypotheses}; obl={x["id"]:x for x in obligations}
allowed_claims={"candidate","literature-cleared candidate","experimental result","proved result","artifact contribution","novel result"}
for x in candidates:
    assert x["status"] in allowed_claims and x["status"]!="novel result"
    assert x["gates"] and x["claims"]
    assert all(d in candidate_ids for d in x["dependencies"])
for h in hypotheses:
    assert h["candidate"] in candidate_ids
    assert h["id"].startswith(h["candidate"]+"-H")
    assert h["status"] in {"proposed","pinned","verified","refuted"}
    assert h["statement"].strip() and h["scope"].strip()
    if h["status"]=="verified": assert h["verified_by"], f"{h['id']}: verified without evidence"
    if h["status"]!="verified": assert not h["verified_by"], f"{h['id']}: evidence requires verified status"
for v in obligations:
    assert v["candidate"] in candidate_ids
    assert v["id"].startswith(v["candidate"]+"-V")
    assert v["class"] in {"structural","computational","certificate","formal","literature"}
    assert v["status"] in {"open","verified","failed"}
    assert v["description"].strip()
    assert all(d in hyp for d in v["depends_on"])
    assert all(hyp[d]["candidate"]==v["candidate"] for d in v["depends_on"])
    if v["status"]=="verified": assert v["evidence"], f"{v['id']}: verified without evidence"
    if v["status"]!="verified": assert not v["evidence"], f"{v['id']}: evidence requires verified status"
for t in theorems:
    cid=t["candidate"]; assert cid in candidate_ids and t["id"].startswith(cid+"-T")
    assert t["statement"].strip() and t["proof_artifact"].strip()
    assert t["claim_class"] in {"proved result","artifact contribution"}
    assert t["hypotheses"] and t["obligations"]
    assert all(h in hyp and hyp[h]["status"]=="verified" for h in t["hypotheses"])
    assert all(v in obl and obl[v]["status"]=="verified" for v in t["obligations"])
    assert all(hyp[h]["candidate"]==cid for h in t["hypotheses"])
    assert all(obl[v]["candidate"]==cid for v in t["obligations"])
print(f"validated {len(candidate_ids)} candidates, {len(hyp)} hypotheses, {len(obl)} obligations, {len(theorems)} theorems")
