import NoveltyLab.Oracle
import NoveltyLab.OctonionF3

def main : IO Unit :=
  if NoveltyLab.Oracle.scalarSelfCheck && NoveltyLab.OctonionF3.selfCheck then
    IO.println "Lean scalar and F3 octonion oracle checks passed"
  else
    throw (IO.userError "Lean oracle self-check failed")
