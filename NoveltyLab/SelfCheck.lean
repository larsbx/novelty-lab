import NoveltyLab.Oracle
import NoveltyLab.Fixture

namespace NoveltyLab.SelfCheck

open NoveltyLab.Oracle NoveltyLab.Fixture

/-- The checks one fixture case must pass. Every product is recomputed from the tensor;
`edges` are only compared against, never used. -/
def caseChecks (c : Case) : List (String × Bool) :=
  let p := prime
  let t := cayleyDickson8
  let e := boundaryTerms p t c.a c.b c.c c.d
  [("pentagon boundary closes", checkPentagon p t c.a c.b c.c c.d),
   ("edges replay the Python experiment", e == c.edges),
   ("each edge is its vertex difference", edgesMatchVertices p t c.a c.b c.c c.d),
   ("some edge is nonzero", e.any (fun v => !isZero v)),
   ("sign-flip mutants are killed", killsSignFlips p t c.a c.b c.c c.d),
   ("discriminating case: all edges nonzero and order mutants killed",
     !c.discriminating || (e.all (fun v => !isZero v) && killsOrderSwaps p t c.a c.b c.c c.d))]

/-- Every named check of the oracle self-test. -/
def checks : List (String × Bool) :=
  [("scalar table (associative sanity case)", checkPentagon 5 scalarTable #[2] #[3] #[4] #[1]),
   ("octonion tensor is 8x8x8", wellSized 8 cayleyDickson8),
   ("some case is discriminating", cases.any (·.discriminating))] ++
  (cases.toList.zipIdx.flatMap fun (c, i) =>
    (caseChecks c).map fun (name, ok) => (s!"case {i}: {name}", ok))

def selfCheck : Bool := checks.all (·.2)

end NoveltyLab.SelfCheck
