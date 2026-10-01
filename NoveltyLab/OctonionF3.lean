import NoveltyLab.Oracle

namespace NoveltyLab.OctonionF3

open NoveltyLab.Oracle

def productIndex : Array (Array Nat) := #[
  #[0,1,2,3,4,5,6,7],
  #[1,0,3,2,5,4,7,6],
  #[2,3,0,1,6,7,4,5],
  #[3,2,1,0,7,6,5,4],
  #[4,5,6,7,0,1,2,3],
  #[5,4,7,6,1,0,3,2],
  #[6,7,4,5,2,3,0,1],
  #[7,6,5,4,3,2,1,0]
]

def productCoeff : Array (Array Nat) := #[
  #[1,1,1,1,1,1,1,1],
  #[1,2,1,2,1,2,2,1],
  #[1,2,2,1,1,1,2,2],
  #[1,1,2,2,1,2,1,2],
  #[1,2,2,2,2,1,1,1],
  #[1,1,2,1,2,2,2,1],
  #[1,1,1,2,2,1,2,2],
  #[1,2,1,1,2,2,1,2]
]

def table : MulTable :=
  (Array.range 8).map fun i =>
    (Array.range 8).map fun j =>
      (Array.range 8).map fun k =>
        if k == productIndex[i]![j]! then productCoeff[i]![j]! else 0

def basis (i : Nat) : Vec :=
  (Array.range 8).map fun j => if i == j then 1 else 0

def witnessEdges : Array Vec :=
  pentagonEdges 3 table (basis 0) (basis 1) (basis 2) (basis 4)

def tableChecks : Bool :=
  wellSized 8 table &&
  (Array.range 8).all (fun i =>
    mul 3 table (basis 0) (basis i) == basis i &&
    mul 3 table (basis i) (basis 0) == basis i)

def witnessCheck : Bool :=
  checkPentagon 3 table (basis 0) (basis 1) (basis 2) (basis 4) &&
  witnessEdges.any (fun edge => !(isZero edge)) &&
  witnessEdges[2]! == basis 7 &&
  witnessEdges[4]! == neg 3 (basis 7)

def selfCheck : Bool := tableChecks && witnessCheck

end NoveltyLab.OctonionF3
