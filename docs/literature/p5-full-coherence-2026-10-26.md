# Full P5 permutohedral route complex — bounded literature gate (2026-10-26)

**Decision: proceed with a narrowed finite experiment.** Construct the complete four-dimensional permutohedron P5 over its ordered-partition face poset, with signed integer CW boundaries; verify d²=0, exact F5 homology, and compare cell-admission consequences of existing state-dependent route receipts. No theorem or novelty promotion.

## 1. Mathematical target
P5 has dimension 4, not 5; expected cell vector (120,240,150,30,1). Two-faces: 90 squares and 60 hexagons. Three-faces: 10 P4 truncated-octahedral facets and 20 hexagonal prisms (P3 times segment); 30 surround the top 4-cell. Verify exact integer boundary cancellation and ranks over F5: (119,121,29,1), full Betti vector (1,0,0,0,0), boundary H3 rank one. Compare to P3 (6,6,1), P4 (24,36,14,1), and the additive five-cube (32,80,80,40,10,1), which has dimension **5** and encodes frozen subset updates, not permutational coherence.

Reuse externally replayed version-one RT route receipts and their independently trusted specification pin. Admit each higher face only when all its facets have been admitted; geometric spread alone does not prove exact update commutation.

## 2. Primary sources (revisited October 26, 2026)

| Work | Locator and reading depth | Boundary |
| --- | --- | --- |
| A. Postnikov, *Permutohedra, Associahedra, and Beyond* (IMRN 2009) | Introduction, ordered-partition face organization and §§1–2, Propositions 2.5–2.6, https://sites.math.washington.edu/~billey/classes/Hopf.algebra/bulletins/postnikov.2009.pdf ; primary PDF inspected | Classical face construction; no mathematical novelty. |
| A. Postnikov, V. Reiner, L. Williams, *Faces of Generalized Permutohedra* (2008) | Introduction and face-number results, https://math.mit.edu/~apost/papers/genpermfaces.pdf ; primary PDF/abstract inspected | Face-count identities are classical. |
| A. Hatcher, *Algebraic Topology* (2002) | §2.2 Cellular Homology, https://pi.math.cornell.edu/~hatcher/AT/AT-doublepage.pdf ; earlier read, not full proof independently reviewed this turn | Cellular chain condition is standard. |
| A. Mazurkiewicz, *Concurrent Program Schemes and their Interpretations* (1977) | Publication abstract, https://doi.org/10.7146/dpb.v6i78.7691 | Classical trace equivalence requires independently verified event independence. |

Earlier relevant literature gates: p4-permutohedral-coherence-2026-10-26.md and rt-route-stream-replay-2026-10-26.md.

## 3. Hypotheses, conventions and negative controls
- Face = ordered partition of {0,1,2,3,4}, dimension = 5 minus number of blocks; a facet refines one block into two ordered nonempty subblocks. Orientation uses blockwise coordinate-difference bases and **outward-first** doubled-barycenter difference, taking exact integer determinant sign. No numerical analysis or field ordering is used.
- The reference constructs all cells, and selectively exposes requested boundary closures. Do not claim a lazy implementation or asymptotic speedup.
- Flip one top-facet incidence sign to violate d3 d4=0. An omitted required lower face must prevent higher-cell admission.
- In the prior exact field model, all 240 frozen-translation swaps admit; the 24 semantically failing swaps in state-dependent and null-defect modes must block the higher P5 filling, although all 240 geometric gates pass.
- SHA-256 record checks are not signatures. F5 results make no claims about floating-point optimizers or actual LLM training.

## 4. Decision
**Proceed with a narrowed experiment** in experiments/rt/, tests/, docs/. Leave upstream/vendored mathematical kernels, generated ledgers, canonical kernel authority and theorem status unchanged. Findings are exact bounded conformance only.
