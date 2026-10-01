#!/usr/bin/env python3
import json
from pathlib import Path
ALLOWED={"candidate","literature-cleared candidate","experimental result","proved result","artifact contribution","novel result"}
data=json.loads(Path("research/candidates.json").read_text())
ids=[x["id"] for x in data["candidates"]]
assert len(ids)==len(set(ids)), "duplicate candidate id"
for item in data["candidates"]:
    assert item["status"] in ALLOWED
    assert item["gates"], f"{item['id']}: missing gates"
    assert item["claims"], f"{item['id']}: missing claim boundary"
    assert item["status"]!="novel result", f"{item['id']}: novelty requires human review"
    for dep in item["dependencies"]: assert dep in ids, f"{item['id']}: unknown dependency {dep}"
print(f"validated {len(ids)} calibrated candidates")
