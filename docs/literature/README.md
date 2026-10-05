# Literature stop/go notes

A note here comes before any of the following:

- a new theorem-facing diagnostic;
- a test of a proposed universal invariant;
- the promotion of a lemma.

See `AGENTS.md` § *Literature stop/go gate*. The note keeps computation and
proof effort away from known constructions, known counterexamples, and routes
whose hypotheses do not match this repository's conventions. Those
conventions are the cayley-dickson/v1 model, the field and characteristic, and
the integrality and quotient conventions of `docs/calibration.md`.

A note is literature clearance, not a novelty finding.

## File name and format

`docs/literature/<topic>-<YYYY-MM-DD>.md`, with these sections in order:

1. **Proposed claim or experiment.** The exact statement, with its field,
   characteristic and conventions.
2. **Sources.** Three to six primary sources. Give each one's exact locator
   (theorem or section number, page) and the date it was read. Include:
   - the closest known construction;
   - the strongest relevant theorem;
   - the known hypothesis boundaries or counterexamples.
3. **Terminology.** What the field calls the objects, so later searches use
   its words.
4. **Hypotheses.** Those that transfer to this repository's setting, and those
   that do not, with the reason.
5. **Negative controls.** Known counterexamples or overstrong variants that the
   tests should calibrate against.
6. **Decision.** One of **stop**, **redirect**, or **proceed with a narrowed
   target**, with the narrowed statement.

Keep it proportional. A note is a page, not a survey.

## Notes owed by claims that predate this gate

These claims were stated before the gate existed. Each still needs a note
before its record can move past `pending` or `experimental`. The
citation-check checklist in `paper/associator-defects/README.md` covers the
same sources.

| Claim | What the note must settle |
|---|---|
| Conjecture 3.32 (`WordDefectG2Data`) | the exact form of the first fundamental theorem for G₂ (Schwarz 1988): generators B, φ, ψ, and in which characteristics |
| Corollary 3.24 (`DefectSOClassFinite`) | the exact statement in Wall (1963) of conjugacy for semisimple orthogonal elements over 𝔽_q |
| Proposition 3.26 (`WordDefectLengthThreeClassical`) | a reference for the Clifford trace facts on the spin module |
| H3 (`DefectStratifiedCollisions`) | prior work on factorization and recomposition in integral octonions (Conway–Smith), and on collision statistics in non-associative word problems |
