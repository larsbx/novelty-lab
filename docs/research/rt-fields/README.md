# Independent field research tracks — first empirical packets (2026-10-28)

**Authority:** bounded, non-authoritative consumer research in `experiments/rt/field_pilots/`; original cross-disciplinary partition [here](../../surveys/fields/README.md). **Literature stop/go:** [bounded field-pilot gate](../../literature/rt-field-bounded-pilots-2026-10-28.md). **Governance:** `AGENTS.md`, `docs/calibration.md`, `docs/verification.md`. No novelty/theorem/status promotion.

## SOP packet anatomy

Each packet declares a field-specific **question**, **object and exact scope**, **hypothesis**, **primary literature and local gate**, **procedure**, **positive and negative controls**, **reproduction command**, **claim ceiling**, and a **next falsifiable packet**. These are **not** a sequence in which mathematics must await ML or software tests before it can become proved. The only coupling is through a separately declared [bridge](bridges.md).

| Discipline | Packet | Executable |
| --- | --- | --- |
| Mathematics / finite quadratic geometry | [Gram and RT](mathematics.md) | `experiments/rt/field_pilots/mathematics.py` |
| Theoretical CS / rewriting | [P4 operational swaps](rewriting.md) | `experiments/rt/field_pilots/rewriting.py` |
| Algebraic topology | [Cylinder witness classes](topology.md) | `experiments/rt/field_pilots/topology.py` |
| Systems verification / security | [Receipt tamper control](systems.md) | `experiments/rt/field_pilots/systems.py` |
| Stochastic processes / control | [Two-step rational scheduler](stochastic.md) | `experiments/rt/field_pilots/stochastic.py` |
| Empirical optimization / ML | [Toy SGD and momentum orders](machine-learning.md) | `experiments/rt/field_pilots/machine_learning.py` |
| Interdisciplinary formal interface | [F5 reduction falsifier](bridges.md) | `experiments/rt/field_pilots/bridges.py` |

**Reproduction:** from repository root, `python -m experiments.rt.field_pilots` prints deterministic JSON; `python -m unittest discover -s tests -p test_rt_field_pilots.py -v` checks each independently. No stochastic sample, random seed, experimental population, generated `data/` or external service is involved. Reports are **read-only stdout**, not accepted proof records. This pilot runner belongs to the experimental plane. Upstream reusable math remains in `finite-math-kernels`.

**Acceptance:** all declared negative controls must pass; an incomplete/failed run is a failure, not supporting evidence. Hosted CI results must be observed and documented, not presumed. A success establishes precisely the bounded observable named in each packet; do not infer significance, broad confluence, accuracy, security or sound training.

**Cross-track evaluation:** [full evidence boundary](../../surveys/fields/bridges.md); failure of a representation transfer retracts only the transfer claim, not source mathematics.

## Next iteration

The next mathematics packet can target general `k` characteristic-polynomial coefficients upstream. Theoretical CS can classify prefix-stable commutations beyond P4. Topology can implement exact inclusion-map witnesses in a small changing complex. Systems can verify externally supplied canonical receipt records with independent trust pins. Probability can test a complete finite transition kernel (all row sums, conditional paths). ML can run a named real optimizer on a synthetic dataset with recorded configuration and performance; until that exists this is only a toy. Bridges can define a faithful fixed-point abstraction with a provable bound—or retain a falsification report.
