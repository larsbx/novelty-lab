# novelty-lab

A calibration-first laboratory for turning mathematically plausible ideas into
auditable research claims.

Nothing in this repository is called novel merely because it follows from a
classical theorem. Every project begins as a **candidate** and advances only
after a literature record, an exact statement, and reproducible evidence exist.

## Active candidates

| ID | Program | Current label | First gate |
|---|---|---|---|
| N1 | Certified Cayley–Dickson division/splitting decisions | candidate — artifact novelty | audit Lean/mathlib coverage and state hypotheses |
| N3 | Shell collision multiplicities modulo ℓ | candidate — experimental | unit-orbit-aware Poisson baseline |
| N2 | Octonionic navigation and finite quotients | candidate — research-grade | literature clearance and well-defined generator model |
| N4 | Explicit certified shell/golden-gate discrepancy | candidate — dependent | pin an explicit theorem with constants |

The execution order is N1 → N3 → N2 → N4. See
[the calibration policy](docs/calibration.md) and the per-candidate dossiers in
[docs/candidates](docs/candidates).

## Reproducible checks

```sh
python scripts/check_registry.py
python -m unittest discover -s tests -v
```

The N3 analyzer consumes a JSON object whose `multiplicities` field is the
list of fiber occupancies, including zeros when the complete finite target is
known:

```sh
python experiments/n3/analyze_collisions.py data.json
```

## Claim boundary

Repository artifacts may establish implementation correctness, certificate
checking, and finite experimental facts. They do not establish mathematical
novelty. Novelty requires a dated, query-recorded literature audit and a
comparison against the nearest prior art.
