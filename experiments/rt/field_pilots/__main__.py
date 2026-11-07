"""Replay all independent bounded field pilots without promoting claim status."""
import json
from experiments.rt.field_pilots import (
    mathematics, rewriting, topology, systems, stochastic, machine_learning, bridges,
)

PILOTS = (
    mathematics.run, rewriting.run, topology.run, systems.run,
    stochastic.run, machine_learning.run, bridges.run,
)


def run():
    results = tuple(pilot() for pilot in PILOTS)
    labels = tuple(result["discipline"] for result in results)
    if len(labels) != len(set(labels)):
        raise AssertionError("duplicated discipline")
    return {"status": "bounded-experiment", "date": "2026-10-28",
            "pilot_count": len(results), "experiments": results,
            "scope": "seven independent toy/finite pilots; no cross-field proof transfer"}


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True, separators=(",", ":")))
