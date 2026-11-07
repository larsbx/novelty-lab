import NoveltyLab.N7

def main : IO Unit := do
  unless NoveltyLab.N7.lawChecks do
    throw (IO.userError "N7 bounded laws or negative controls failed")
  IO.println NoveltyLab.N7.fixtureJson.compress
