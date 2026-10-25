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
| N5 | Multiset budget signatures for Nielsen witnesses | candidate — exact finite classification | define exact minimizer and rerun the complete S6 census |

The execution order is N1 → N3 → N2 → N4 → N5. See
[the calibration policy](docs/calibration.md) and the per-candidate dossiers in
[docs/candidates](docs/candidates).

## Working here

[`AGENTS.md`](AGENTS.md) is the policy and [`CONTRIBUTING.md`](CONTRIBUTING.md)
lists the gates; both are normative. Together they cover authority before
language, exactness, shared census primitives, the literature stop/go gate,
test coverage declarations, and which way "fail closed" points. They adapt the
disciplines of `larsbx/pisot-substitution-conjecture-research` and
`larsbx/langlands-lab`. [`ESTATE.toml`](ESTATE.toml) and
[`ARCHITECTURE.md`](ARCHITECTURE.md) assign every path an authority plane, and
CI audits the layout against the pinned estate audit.

## Layout

| Path | Authority |
|---|---|
| `kernel/n1/` | canonical N1 certificate checker (exact arithmetic over ℚ) |
| `experiments/` | non-authoritative search and data generation |
| `data/` | committed experimental outputs, hashed in the ledger |
| `schemas/` | versioned certificate formats |
| `research/candidates.json` | programme registry (calibration ladder) |
| `research/ledger.json` | proof-record ledger: the single source of `docs/ledger-index.md`, `tla/`, and the generated claims in `claim_governance.toml` |
| `paper/` | manuscripts for peer review; tables generated from `data/` (see each paper's README) |
| `vendor/` | pinned external code, never edited here |

## Reproducible checks

```sh
scripts/verify_all.sh            # every gate: PASS / FAIL / SKIP per line; exit 0 only if all ran and passed
scripts/verify_all.sh python     # the gates CI's Python job runs
```

The runner covers the registries, vendoring, ledger surfaces, claim governance
(including test coverage), the unit tests, every census `--check`, the paper
tables, the Lean oracle and the TLC models (`CONTRIBUTING.md`).

After editing `research/ledger.json`, run `python tools/seal_ledger.py`
(recomputes the content-addressed record identifiers; an edge may name its
target as `@Name`), then drop `--check` from the generator command to
regenerate its surfaces. The TLC models in `tla/` are checked by
`TLA2TOOLS=path/to/tla2tools.jar scripts/verify_all.sh tla`. That gate runs TLC
inside `tla/` with the vendored `ProofArchitecture.tla` on an absolute
`TLA-Library` path. CI pins tla2tools v1.7.4 by SHA-256.

## Vendored code

`vendored.toml` pins each package under `vendor/` to an upstream commit and
the SHA-256 of every file; `vendor/vendoring/check_vendored_sync.py` fails CI
on any drift or unpinned source file. To update: copy the package directory
byte for byte from upstream, then run
`python vendor/vendoring/check_vendored_sync.py pin NAME COMMIT`. Never patch
a vendored file locally; fix it upstream and re-vendor.

| Package | Upstream | Use here |
|---|---|---|
| `proof_records` (Python files and `ProofArchitecture.tla`) | `larsbx/finite-math-kernels` `kernel/proof_records` | record identity, closure, ledger generation |
| `claim_governance` | `larsbx/finite-math-kernels` `tools/claim_governance` | enforces `claim_governance.toml` |
| `vendoring` | `larsbx/finite-math-kernels` `tools/vendoring` | the checker above |
| `finite_exact` (selected Mojo modules) | `larsbx/finite-math-kernels` `kernel/finite_exact` | field-generic exact arithmetic `FpField[p]`, `ExactField` |
| `projective_limits` (RT modules) | `larsbx/finite-math-kernels` `kernel/projective_limits` | guarded split-eight-space spread, reflections and exact batch inversion |
| `parallel_fold` (Mojo/MAX) | `larsbx/finite-math-kernels` `kernel/parallel_fold` | deterministic exact parallel shell census |

Selected **Mojo-first mathematical kernels** are now vendored byte-for-byte
under `vendor/mojo/` from an immutable estate revision, together with an
independently replayed [48-case finite-field fixture](tests/fixtures/hyperbolic_rt_v1.txt).
See [the RT adoption contract](docs/foundations/estate-rt-adoption.md) for
provenance, guards, MAX CPU execution and source ownership. Reusable mathematics
belongs in `finite-math-kernels`; local Python is an independent, non-authoritative
RT oracle and retains this consumer's established certificate-acceptance role.
These are selected source packages, **not** the whole upstream repository.
The isolated `experiments/rt/pixi.toml` and `smoke.mojo` run an exact
consumer integration test against the vendored source under a pinned Mojo/MAX
toolchain; they do not confer claim-acceptance authority. Other Mojo, Julia and Haskell packages remain
outside this repository until there is a concrete consumer.

N1 certificates (`docs/n1-specification.md`) are searched and checked
separately:

```sh
python experiments/n1/search.py -1 -1 > cert.json   # non-authoritative
```

The N2 defect census checks N2-T03 and the pending defect records on
finite samples (`docs/candidates/N2.md`):

```sh
python experiments/n2/defect_census.py --check
```

The N3 data generator emits a complete occupancy vector, and the analyzer
consumes it:

```sh
python experiments/n3/hurwitz_shell.py 97 13 left > data.json
python experiments/n3/analyze_collisions.py data.json
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
