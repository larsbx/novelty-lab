import NoveltyLab.IntrinsicSelection

namespace NoveltyLab.IntrinsicSelectionF7

abbrev Matrix := List (List Nat)

def entry (a : Matrix) (i j : Nat) : Nat := (a[i]?.getD [])[j]?.getD 0

def matrix (f : Nat → Nat → Nat) : Matrix :=
  (List.range 8).map fun i => (List.range 8).map (f i)

def identity : Matrix := matrix fun i j => if i == j then 1 else 0
def gram : Matrix := matrix fun i j => if i == j then 2 else 1
def phi : Matrix := gram
def phiInv : Matrix := matrix fun i j => if i == j then 4 else 3

def mul (a b : Matrix) : Matrix := matrix fun i j =>
  ((List.range 8).foldl (fun s k => s + entry a i k * entry b k j) 0) % 7

def transpose (a : Matrix) : Matrix := matrix fun i j => entry a j i

/-- The eight explicit basis-defect diagonal patterns in octonion coordinates.
The Python regression binds these declared patterns to its independently
computed Cayley-Dickson defects; no abstract octonion identity is assumed.
-/
def patterns : List (List Nat) :=
  [[1,1,1,1,1,1,1,1], [1,1,1,1,6,6,6,6],
   [1,1,6,6,1,1,6,6], [1,1,6,6,6,6,1,1],
   [1,6,1,6,1,6,1,6], [1,6,1,6,6,1,6,1],
   [1,6,6,1,1,6,6,1], [1,6,6,1,6,1,1,6]]

def diagonal (row : List Nat) : Matrix := matrix fun i j =>
  if i == j then row[i]?.getD 0 else 0

def defects : List Matrix := patterns.map fun row => mul phi (mul (diagonal row) phiInv)

def swap (k : Nat) : Matrix := matrix fun i j =>
  let image := if i == k then k+1 else if i == k+1 then k else i
  if image == j then 1 else 0

def orthogonal (a : Matrix) : Bool := mul (transpose a) (mul gram a) == gram

def rejectionChecks : Bool :=
  let witnesses := [(1,3,0,0), (2,1,0,0), (3,1,0,0),
                    (4,0,0,2), (5,0,0,2), (6,0,0,2), (7,0,0,2)]
  witnesses.all fun (index, k, i, j) =>
    let d := defects[index]?.getD []
    -- Each defect is an involution, so its inverse is itself.
    mul d d == identity &&
    entry (mul d (mul (swap k) d)) i j == 3

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
/-- Kernel-checked finite bridge, Gram, involution, and seven rejection identities.
`decide` is used, not `native_decide`, and no new axioms are introduced.
-/
theorem finite_certificates :
    (mul phi phiInv == identity &&
     mul (transpose phi) (mul gram phi) == identity &&
     defects.all orthogonal && rejectionChecks) = true := by
  decide

end NoveltyLab.IntrinsicSelectionF7
