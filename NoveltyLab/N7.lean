import NoveltyLab.Oracle
import Lean.Data.Json

namespace NoveltyLab.N7

/-! General counting lemmas. Lists enumerate vectors with their multiplicities.
These statements have no dependence on the two finite fixtures. -/

def sumList (op : V → V → V) (xs ys : List V) : List V :=
  xs.flatMap fun x => ys.map (op x)

def fixedCount [DecidableEq V] (op : V → V → V) (xs ys : List V) (z : V) : Nat :=
  (sumList op xs ys).countP fun w => decide (w = z)

theorem sumList_assoc (op : V → V → V) (assoc : ∀ x y z, op (op x y) z = op x (op y z))
    (xs ys zs : List V) :
    sumList op (sumList op xs ys) zs = sumList op xs (sumList op ys zs) := by
  have step (x y : V) : op (op x y) = (fun z => op x (op y z)) := funext (assoc x y)
  simp only [sumList, List.flatMap_assoc, List.flatMap_map, List.map_flatMap,
    List.map_map, Function.comp_def, step]

theorem map_sumList (op : V → V → V) (f : V → V)
    (additive : ∀ x y, f (op x y) = op (f x) (f y)) (xs ys : List V) :
    (sumList op xs ys).map f = sumList op (xs.map f) (ys.map f) := by
  simp only [sumList, List.map_flatMap, List.flatMap_map, List.map_map,
    Function.comp_def, additive]

/-- A simultaneous bijective scaling or nonzero multiplier preserves every
fixed-output count when the input and output representative lists are transported. -/
theorem fixedCount_transport [DecidableEq V] (op : V → V → V) (f : V → V)
    (additive : ∀ x y, f (op x y) = op (f x) (f y))
    (injective : ∀ {x y}, f x = f y → x = y) (xs ys : List V) (z : V) :
    fixedCount op (xs.map f) (ys.map f) (f z) = fixedCount op xs ys z := by
  unfold fixedCount
  rw [← map_sumList op f additive, List.countP_map]
  have same : (fun w => decide (f w = f z)) = (fun w => decide (w = z)) := by
    funext w
    simp [show f w = f z ↔ w = z from ⟨injective, congrArg f⟩]
  simpa [Function.comp_def] using congrArg (fun p => (sumList op xs ys).countP p) same

/-- Summing the same fixed coefficient over a complete output orbit gives
the raw orbit total. The singleton zero orbit has factor one. -/
theorem raw_eq_size_mul (count : V → Nat) (orbit : List V) (coefficient : Nat)
    (constant : ∀ z ∈ orbit, count z = coefficient) :
    (orbit.map count).sum = orbit.length * coefficient := by
  induction orbit with
  | nil => simp
  | cons z zs ih =>
    simp only [List.map_cons, List.sum_cons, List.length_cons, Nat.add_mul, Nat.one_mul]
    rw [constant z (by simp), ih (fun w hw => constant w (by simp [hw])), Nat.add_comm]

theorem fixedCount_zero_left [DecidableEq V] (op : V → V → V) (zero : V)
    (identity : ∀ x, op zero x = x) (ys : List V) (z : V) :
    fixedCount op [zero] ys z = ys.countP (fun w => decide (w = z)) := by
  have same : op zero = id := funext identity
  simp [fixedCount, sumList, same]

private theorem count_swap (op : V → V → V) (p : V → Bool) (xs ys : List V) :
    (sumList op xs ys).countP p = (sumList (fun y x => op x y) ys xs).countP p := by
  induction xs with
  | nil =>
    have empty : ys.flatMap (fun _ => ([] : List V)) = [] :=
      List.flatMap_eq_nil_iff.mpr (fun _ _ => rfl)
    simp [sumList, empty]
  | cons x xs ih =>
    simp only [sumList, List.flatMap_cons, List.countP_append] at ih ⊢
    rw [ih]
    clear ih
    induction ys with
    | nil => simp
    | cons y ys ih =>
      simp only [List.map_cons, List.flatMap_cons, List.countP_append, List.countP_cons]
      simp only [List.map_cons] at ih
      rw [← ih]
      omega

theorem fixedCount_comm [DecidableEq V] (op : V → V → V)
    (comm : ∀ x y, op x y = op y x) (xs ys : List V) (z : V) :
    fixedCount op xs ys z = fixedCount op ys xs z := by
  have swap : (fun y x => op x y) = op := funext fun y => funext fun x => comm x y
  simpa only [fixedCount, swap] using count_swap op (fun w => decide (w = z)) xs ys

def expandOrbits (classes : List C) (orbit : C → List V) (weight : C → Nat) : List V :=
  classes.flatMap fun t => (List.replicate (weight t) t).flatMap orbit

private theorem count_repeated (p : V → Bool) (f : C → List V) (t : C) (n : Nat) :
    ((List.replicate n t).flatMap f).countP p = n * (f t).countP p := by
  induction n with
  | zero => simp
  | succ n ih => simp [List.replicate_succ, ih, Nat.succ_mul, Nat.add_comm]

private theorem count_expand_left [DecidableEq V] (op : V → V → V) (classes : List C)
    (orbit : C → List V) (weight : C → Nat) (ys : List V) (out : V) :
    fixedCount op (expandOrbits classes orbit weight) ys out =
      (classes.map fun t => weight t * fixedCount op (orbit t) ys out).sum := by
  unfold expandOrbits
  simp only [fixedCount, sumList, List.flatMap_assoc]
  rw [List.countP_flatMap]
  simp only [Function.comp_def, count_repeated]

/-- The coefficient-level composition law on orbit labels. -/
def CoefficientAssociativity (classes : List C) (c : C → C → C → Nat) : Prop :=
  ∀ x y z out,
    (classes.map fun t => c x y t * c t z out).sum =
    (classes.map fun t => c y z t * c x t out).sum

/-- Once each binary representative sum expands as the prescribed orbit
copies, coefficient associativity follows from vector associativity.
Constructing that expansion from the scalar-orbit partition is a separate
obligation for a general finite field. -/
theorem coefficient_assoc_of_expansion [DecidableEq V] (op : V → V → V)
    (assoc : ∀ x y z, op (op x y) z = op x (op y z))
    (comm : ∀ x y, op x y = op y x)
    (classes : List C) (orbit : C → List V) (representative : C → V)
    (expand : ∀ x y, List.Perm (sumList op (orbit x) (orbit y))
      (expandOrbits classes orbit (fun t => fixedCount op (orbit x) (orbit y) (representative t)))) :
    CoefficientAssociativity classes (fun x y z => fixedCount op (orbit x) (orbit y) (representative z)) := by
  intro x y z out
  let w := representative out
  let p := fun v => decide (v = w)
  let f := fun v => (orbit z).map (op v)
  let g := fun v => (orbit x).map (op v)
  have left := (List.Perm.flatMap_right f (expand x y)).countP_eq p
  have right := (List.Perm.flatMap_right g (expand y z)).countP_eq p
  change fixedCount op (sumList op (orbit x) (orbit y)) (orbit z) w =
    fixedCount op (expandOrbits classes orbit _) (orbit z) w at left
  change fixedCount op (sumList op (orbit y) (orbit z)) (orbit x) w =
    fixedCount op (expandOrbits classes orbit _) (orbit x) w at right
  rw [count_expand_left] at left right
  simp only [fixedCount_comm op comm _ (orbit x) w] at right
  calc
    _ = fixedCount op (sumList op (orbit x) (orbit y)) (orbit z) w := left.symm
    _ = fixedCount op (orbit x) (sumList op (orbit y) (orbit z)) w := by
      unfold fixedCount
      rw [sumList_assoc op assoc]
    _ = _ := right

/-! Bounded evidence follows. These enumerations do not discharge the universal
orbit partition, extension-field, or projective incidence obligations. -/
open NoveltyLab.Oracle (Vec add sub mul isZero zeroVec)

def vectors2 (p : Nat) : List Vec :=
  (List.range p).flatMap fun a => (List.range p).map fun b => #[a, b]

def vectors3 (p : Nat) : List Vec :=
  (List.range p).flatMap fun a => (List.range p).flatMap fun b =>
    (List.range p).map fun c => #[a, b, c]

def scale (p s : Nat) (x : Vec) : Vec := x.map fun a => s * a % p

def reps (p : Nat) (x : Vec) : List Vec :=
  if isZero x then [x] else (List.range (p - 1)).map fun i => scale p (i + 1) x

def canonical (x : Vec) : Bool := (x.toList.find? (· != 0)).getD 1 == 1

def normal (p : Nat) (x : Vec) : Option Vec := (reps p x).find? canonical

def classes7 : List Vec := (vectors2 7).filter canonical

def fixed (p : Nat) (x y z : Vec) : Nat :=
  (reps p x).countP fun a => (reps p y).contains (sub p z a)

def raw (p : Nat) (x y z : Vec) : Nat :=
  (sumList (add p) (reps p x) (reps p y)).countP fun w => (reps p z).contains w

def extensionTensor : NoveltyLab.Oracle.MulTable :=
  #[#[#[1, 0], #[0, 1]], #[#[0, 1], #[3, 0]]]

def classProduct (x y : Vec) : Nat :=
  (normal 7 (mul 7 extensionTensor x y)).map classes7.idxOf |>.getD classes7.length

def table (f : Vec → Vec → Vec → Nat) : List (List (List Nat)) :=
  classes7.map fun x => classes7.map fun y => classes7.map (f x y)

def supportChecks : Bool :=
  classes7.all fun x => classes7.all fun y => classes7.all fun z =>
    let c := fixed 7 x y z
    (reps 7 z).all (fun w =>
      fixed 7 x y w == c && fixedCount (add 7) (reps 7 x) (reps 7 y) w == c) &&
    raw 7 x y z == (reps 7 z).length * c &&
    c == fixed 7 y x z

def coeffCompose (count : Vec → Vec → Vec → Nat) (x y z out : Vec) : Nat × Nat :=
  ((classes7.map fun t => count x y t * count t z out).sum,
   (classes7.map fun t => count y z t * count x t out).sum)

def controlChecks : Bool :=
  let zero := #[0, 0]
  let x := #[1, 0]
  let y := #[0, 1]
  let out := #[1, 1]
  fixed 7 x y out == 1 && raw 7 x y out == 6 &&
  fixed 7 zero x x == 1 && raw 7 zero x x == 6 &&
  coeffCompose (raw 7) x x y y == (36, 216) &&
    coeffCompose (fixed 7) x x y y == (6, 6) &&
  (classes7.map (fixed 7 x x)).sum == 11 && fixed 7 zero zero zero == 1 &&
  fixed 2 x x zero == 1 && fixed 2 x x x == 0

set_option maxRecDepth 4096 in
theorem bounded_controls : controlChecks = true := by decide

def lawChecks : Bool :=
  let zero := #[0, 0]
  let t := (table (fixed 7)).toArray.map (fun r => r.toArray.map List.toArray)
  let ids := List.range classes7.length
  let coefficient := fun x y z => t[x]![y]![z]!
  let actions := (classes7.drop 1).map fun a => (classes7.map (classProduct a)).toArray
  supportChecks && controlChecks &&
  classes7.all (fun x => classes7.all (fun y => fixed 7 zero x y == (if x == y then 1 else 0))) &&
  ids.all fun x => ids.all fun y => ids.all fun z => ids.all fun out =>
    (ids.map (fun i => coefficient x y i * coefficient i z out)).sum ==
    (ids.map (fun i => coefficient y z i * coefficient x i out)).sum &&
    actions.all fun act => coefficient act[x]! act[y]! act[out]! == coefficient x y out

open Lean (Json toJson)

def frameOutputs (x y : Vec) : List (Option Vec) :=
  let a := x[0]!
  let b := x[1]!
  let c := y[0]!
  let d := y[1]!
  let output := fun w => if isZero w then none else normal 7 w
  [output #[(a * d + b * c) % 7, b * d % 7], output #[a * c % 7, b * d % 7]]

def points3 : List Vec := (vectors3 3).filter fun x => canonical x && !isZero x

def incident (n x : Vec) : Bool :=
  (List.range 3).foldl (fun s i => s + n[i]! * x[i]!) 0 % 3 == 0

def span3 (x y : Vec) : List Vec :=
  let scalars := List.range 3
  scalars.flatMap fun a => scalars.map fun b => add 3 (scale 3 a x) (scale 3 b y)

def planeRows (geometry : Vec → Vec → List Vec) : List (List Nat) :=
  (points3.zipIdx).flatMap fun (x, i) => (points3.zipIdx).filterMap fun (y, j) =>
    if i < j then some ([i, j] ++ (geometry x y).map points3.idxOf) else none

def fixtureJson : Json :=
  let framePoints := classes7.filter fun x => !isZero x
  Json.mkObj [
    ("f7", Json.mkObj [
      ("classes", toJson classes7), ("fixed", toJson (table (fixed 7))),
      ("raw", toJson (table (raw 7))),
      ("product", toJson (classes7.map fun x => classes7.map (classProduct x)))]),
    ("framed_f7", Json.mkObj [
      ("points", toJson framePoints),
      ("standard_outputs", toJson (framePoints.map fun x => framePoints.map (frameOutputs x)))]),
    ("f3", Json.mkObj [
      ("points_and_dual_normals", toJson points3),
      ("lines", toJson (points3.map fun n => (points3.filter (incident n)).map points3.idxOf)),
      ("joins", toJson (planeRows fun x y =>
        let span := span3 x y
        points3.filter fun n => span.all (incident n))),
      ("meets", toJson (planeRows fun x y => points3.filter fun z => incident x z && incident y z))])]

end NoveltyLab.N7
