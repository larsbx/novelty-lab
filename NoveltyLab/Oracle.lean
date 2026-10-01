import Std

namespace NoveltyLab.Oracle

abbrev Vec := Array Nat
abbrev MulTable := Array (Array (Array Nat))

def wellSized (n : Nat) (t : MulTable) : Bool :=
  t.size == n &&
  t.all (fun row => row.size == n && row.all (fun cell => cell.size == n))

def vecSized (n : Nat) (x : Vec) : Bool := x.size == n

def add (p : Nat) (x y : Vec) : Vec :=
  (Array.range x.size).map (fun i => (x[i]! + y[i]!) % p)

def neg (p : Nat) (x : Vec) : Vec :=
  x.map (fun a => (p - (a % p)) % p)

def sub (p : Nat) (x y : Vec) : Vec := add p x (neg p y)

def mul (p : Nat) (t : MulTable) (x y : Vec) : Vec :=
  let n := x.size
  (Array.range n).map fun k =>
    (List.range n).foldl (fun acc i =>
      (List.range n).foldl (fun acc' j =>
        (acc' + x[i]! * y[j]! * t[i]![j]![k]!) % p) acc) 0

def assoc (p : Nat) (t : MulTable) (x y z : Vec) : Vec :=
  sub p (mul p t x (mul p t y z)) (mul p t (mul p t x y) z)

def pentagonBoundary (p : Nat) (t : MulTable) (a b c d : Vec) : Vec :=
  let e₀ := mul p t (assoc p t a b c) d
  let e₁ := assoc p t a (mul p t b c) d
  let e₂ := mul p t a (assoc p t b c d)
  let e₃ := neg p (assoc p t a b (mul p t c d))
  let e₄ := neg p (assoc p t (mul p t a b) c d)
  add p (add p (add p e₀ e₁) (add p e₂ e₃)) e₄

def isZero (x : Vec) : Bool := x.all (fun a => a == 0)

def checkPentagon (p : Nat) (t : MulTable) (a b c d : Vec) : Bool :=
  let n := t.size
  p > 1 && wellSized n t &&
  vecSized n a && vecSized n b && vecSized n c && vecSized n d &&
  isZero (pentagonBoundary p t a b c d)

def scalarTable : MulTable := #[#[#[1]]]

def selfCheck : Bool :=
  checkPentagon 5 scalarTable #[2] #[3] #[4] #[1]

end NoveltyLab.Oracle
