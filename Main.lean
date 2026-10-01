import NoveltyLab.Oracle

def main : IO Unit :=
  if NoveltyLab.Oracle.selfCheck then
    IO.println "Lean oracle self-check passed"
  else
    throw (IO.userError "Lean oracle self-check failed")
