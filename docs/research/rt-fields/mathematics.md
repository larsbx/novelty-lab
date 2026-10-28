# Mathematics packet M1 — Gram defect controls

**Authority:** bounded, non-authoritative consumer research in `experiments/rt/field_pilots/`; original cross-disciplinary partition [here](../../surveys/fields/README.md). **Literature stop/go:** [bounded field-pilot gate](../../literature/rt-field-bounded-pilots-2026-10-28.md). **Governance:** `AGENTS.md`, `docs/calibration.md`, `docs/verification.md`. No novelty/theorem/status promotion.

**Question:** Does vanishing of the three-ray spread polynomial identify geometric planarity? **No**; the rank guard is exterior/minor-based.

**Object/field:** three declared triples of non-null rays in the split quadratic `F5^8`. The existing `SplitQuadratic8` consumer oracle computes all guarded pairwise spreads. A bounded independent Gram-side calculation checks `(ABC)^2 T=D(4uvw-D)` on exactly those triples. No new generic Gram arithmetic authority is introduced.

**Hypothesis:** planar triple gives defect 0; an independent orthogonal triple gives defect `-1=4` in F5; an independent Gram-nonsingular triple with `D=-4=1` can nevertheless have defect 0. A null-ray spread must reject.

**Prior art and decision:** [RT foundation gate](../../literature/split-cayley-rt-foundations-2026-10-24.md), [bounded pilot gate](../../literature/rt-field-bounded-pilots-2026-10-28.md), and [upstream derivation](https://github.com/larsbx/finite-math-kernels/blob/main/docs/theorems/three-ray-gram-defect.md). Wildberger's higher-rank cross/det-cross is imported, not promoted as new.

**Procedure and controls:** `mathematics.run()` compares the three fixed triples, computes two independent expressions for the defect, and tests explicit null refusal. A failure of any numerator equality, orthogonal `-1`, or nonplanar zero-defect witness rejects the pilot.

**Reproduce:** `python -m experiments.rt.field_pilots`; `python -m unittest tests.test_rt_field_pilots.TestFieldSeparatedRTPilots.test_mathematics_defect_does_not_decide_planarity`.

**Claim ceiling:** bounded finite conformance plus an already written algebraic proof, which remains subject to its own independent mathematical review. No new result, completeness claim or planarity decision by defect.

**Next falsifier:** compare distinct characteristic-polynomial invariants for two 2-planes with identical determinant cross; avoid claiming orbit completeness from finite samples.
