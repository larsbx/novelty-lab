import Std

/-!
Supporting finite-order proofs for the 2026-10-31 independent audit.
Natural endpoints represent ranks in any finite linear order. No claim of a
formal proof of the entire multipartite forbidden-clique induction is made.
-/
namespace NoveltyLab.IntervalBound

structure Interval where
  lo : Nat
  hi : Nat
  valid : lo ≤ hi

/-- The explicit finite order {0,...,orderSize-1}. -/
structure FiniteInterval (orderSize : Nat) where
  lo : Fin orderSize
  hi : Fin orderSize
  valid : lo.val ≤ hi.val

def FiniteInterval.toInterval {N : Nat} (a : FiniteInterval N) : Interval :=
  ⟨a.lo.val, a.hi.val, a.valid⟩

def Contains (a : Interval) (x : Nat) : Prop := a.lo ≤ x ∧ x ≤ a.hi

def Meets (a b : Interval) : Prop := ∃ x, Contains a x ∧ Contains b x

theorem meets_iff (a b : Interval) :
    Meets a b ↔ a.lo ≤ b.hi ∧ b.lo ≤ a.hi := by
  constructor
  · rintro ⟨x, ⟨ha, ha'⟩, ⟨hb, hb'⟩⟩
    constructor <;> omega
  · rintro ⟨h, h'⟩
    refine ⟨max a.lo b.lo, ?_, ?_⟩ <;>
      simp only [Contains, Nat.le_max_left, Nat.le_max_right, true_and,
        Nat.max_le] <;> constructor <;> first | assumption | exact a.valid | exact b.valid

/-- For a pair, a max-left and a min-right occurrence are both contained.
The left/right tags stay different even when their coordinates coincide. -/
theorem endpoint_witnesses (a b : Interval) (h : Meets a b) :
    (Contains b a.lo ∨ Contains a b.lo) ∧
    (Contains b a.hi ∨ Contains a b.hi) := by
  have hab := (meets_iff a b).mp h
  constructor
  · by_cases hle : a.lo ≤ b.lo
    · exact Or.inr ⟨hle, hab.2⟩
    · exact Or.inl ⟨by omega, hab.1⟩
  · by_cases hle : a.hi ≤ b.hi
    · exact Or.inl ⟨hab.2, hle⟩
    · exact Or.inr ⟨hab.1, by omega⟩

/-- A left occurrence is tagged 0 and a right occurrence 1; the two
witnesses are unequal independently of their parent labels/coordinates. -/
theorem endpoint_tags_distinct (i j : Nat) : (i, false) ≠ (j, true) := by
  intro h
  have := congrArg Prod.snd h
  simp at this

def maxLo : List Interval → Nat
  | [] => 0
  | a :: rest => max a.lo (maxLo rest)

theorem lo_le_maxLo (xs : List Interval) (a : Interval) (h : a ∈ xs) :
    a.lo ≤ maxLo xs := by
  induction xs with
  | nil => simp at h
  | cons b xs ih =>
    simp only [List.mem_cons] at h
    rcases h with rfl | h
    · exact Nat.le_max_left _ _
    · exact Nat.le_trans (ih h) (Nat.le_max_right _ _)

theorem maxLo_le (xs : List Interval) (u : Nat)
    (h : ∀ a ∈ xs, a.lo ≤ u) : maxLo xs ≤ u := by
  induction xs with
  | nil => exact Nat.zero_le _
  | cons a xs ih =>
    apply Nat.max_le.mpr
    exact ⟨h a (by simp), ih (fun b hb => h b (by simp [hb]))⟩

/-- Finite Helly-2, including the empty family (witness 0). The explicit
cross-endpoint hypothesis follows from pairwise Meets by meets_iff. -/
theorem helly (xs : List Interval)
    (h : ∀ a ∈ xs, ∀ b ∈ xs, Meets a b) :
    ∃ x, ∀ a ∈ xs, Contains a x := by
  refine ⟨maxLo xs, fun a ha => ⟨lo_le_maxLo xs a ha, ?_⟩⟩
  apply maxLo_le
  intro b hb
  exact ((meets_iff b a).mp (h b hb a ha)).1

/-- Helly-2 directly over an explicit finite order; a nonempty order also
supplies a witness for an empty interval family. Equal entries remain labels. -/
theorem finite_helly {N : Nat} (hN : 0 < N) (xs : List (FiniteInterval N))
    (h : ∀ a ∈ xs, ∀ b ∈ xs, Meets a.toInterval b.toInterval) :
    ∃ x : Fin N, ∀ a ∈ xs, Contains a.toInterval x.val := by
  have hmap : ∀ a ∈ xs.map FiniteInterval.toInterval,
      ∀ b ∈ xs.map FiniteInterval.toInterval, Meets a b := by
    intro a ha b hb
    obtain ⟨a', ha', rfl⟩ := List.mem_map.mp ha
    obtain ⟨b', hb', rfl⟩ := List.mem_map.mp hb
    exact h a' ha' b' hb'
  obtain ⟨x, hx⟩ := helly (xs.map FiniteInterval.toInterval) hmap
  cases xs with
  | nil => exact ⟨⟨0, hN⟩, by simp⟩
  | cons a rest =>
    have hxa := hx a.toInterval (by simp)
    have hxN : x < N := Nat.lt_of_le_of_lt hxa.2 a.hi.isLt
    refine ⟨⟨x, hxN⟩, ?_⟩
    intro b hb
    exact hx b.toInterval (List.mem_map.mpr ⟨b, hb, rfl⟩)

/-- The geometric clique-lifting step needs only cross-part intersections;
there is no assertion that intervals within one part intersect. -/
theorem helly_extend (xs : List Interval) (d : Interval)
    (h : ∀ a ∈ xs, ∀ b ∈ xs, Meets a b)
    (hd : ∀ a ∈ xs, Meets a d) :
    ∃ x, Contains d x ∧ ∀ a ∈ xs, Contains a x := by
  have symm : ∀ a b : Interval, Meets a b → Meets b a := by
    intro a b hab
    obtain ⟨x, ha, hb⟩ := hab
    exact ⟨x, hb, ha⟩
  have hh : ∀ a ∈ d :: xs, ∀ b ∈ d :: xs, Meets a b := by
    intro a ha b hb
    simp only [List.mem_cons] at ha hb
    rcases ha with had | ha <;> rcases hb with hbd | hb
    · subst a; subst b
      exact ⟨d.lo, ⟨Nat.le_refl _, d.valid⟩, ⟨Nat.le_refl _, d.valid⟩⟩
    · subst a
      exact symm b d (hd b hb)
    · subst b
      exact hd a ha
    · exact h a ha b hb
  obtain ⟨x, hx⟩ := helly (d :: xs) hh
  exact ⟨x, hx d (by simp), fun a ha => hx a (by simp [ha])⟩

/-- Clipping retains the exact edge predicate. Tags are parameters, not
geometric equality classes, so distinct tags may give equal clips. -/
def clip (a b : Interval) (h : Meets a b) : Interval :=
  ⟨max a.lo b.lo, min a.hi b.hi, by
    have hab := (meets_iff a b).mp h
    have ha := a.valid
    have hb := b.valid
    omega⟩

theorem contains_clip (a b : Interval) (h : Meets a b) (x : Nat) :
    Contains (clip a b h) x ↔ Contains a x ∧ Contains b x := by
  simp only [Contains, clip]
  omega

theorem tagged_edge_iff (a b c : Interval) (h : Meets a b) :
    Meets (clip a b h) c ↔ ∃ x, Contains a x ∧ Contains b x ∧ Contains c x := by
  constructor
  · rintro ⟨x, hx, hc⟩
    exact ⟨x, ((contains_clip a b h x).mp hx).1,
      ((contains_clip a b h x).mp hx).2, hc⟩
  · rintro ⟨x, ha, hb, hc⟩
    exact ⟨x, (contains_clip a b h x).mpr ⟨ha, hb⟩, hc⟩

/-- Finite sums over labelled indices, retaining repeated entries. -/
def sumN : Nat → (Nat → Nat) → Nat
  | 0, _ => 0
  | n+1, f => sumN n f + f n

theorem sumN_add (n : Nat) (f g : Nat → Nat) :
    sumN n (fun i => f i + g i) = sumN n f + sumN n g := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [sumN, ih]; omega

theorem sumN_mono (n : Nat) (f g : Nat → Nat)
    (h : ∀ i, i < n → f i ≤ g i) : sumN n f ≤ sumN n g := by
  induction n with
  | zero => exact Nat.le_refl _
  | succ n ih =>
    simp only [sumN]
    exact Nat.add_le_add (ih (fun i hi => h i (by omega))) (h n (by omega))

theorem sumN_const (n c : Nat) : sumN n (fun _ => c) = n*c := by
  induction n with
  | zero => simp [sumN]
  | succ n ih => simp only [sumN, ih, Nat.succ_mul]

theorem sumN_swap (m n : Nat) (f : Nat → Nat → Nat) :
    sumN m (fun i => sumN n (f i)) = sumN n (fun j => sumN m (fun i => f i j)) := by
  induction m with
  | zero => simp only [sumN]; exact (sumN_const n 0).symm.trans (by simp)
  | succ m ih => simp only [sumN, ih, sumN_add]

/-- Number of integer indices in the half-open run [a,b) within [0,m). -/
theorem count_run (m a b : Nat) :
    sumN m (fun i => if a ≤ i ∧ i < b then 1 else 0) = min m b - min m a := by
  induction m with
  | zero => simp [sumN]
  | succ m ih =>
    simp only [sumN, ih]
    split <;> omega

/-- Core sliding-window incidence estimate. Each row is a consecutive run
[a_j,b_j), 0<=a_j<=b_j<=m. A late incidence at index i certifies the full
s-point window ending at i; K(s,t)-freeness gives the explicit capacity
hypothesis below. There is no assumption about distinct run geometries. -/
theorem point_run_bound (m n s t : Nat) (hs : 1 ≤ s)
    (a b : Nat → Nat)
    (hrow : ∀ j, j < n → a j ≤ b j ∧ b j ≤ m)
    (capacity : ∀ i, i < m →
      sumN n (fun j => if a j + (s-1) ≤ i ∧ i < b j then 1 else 0) ≤ t-1) :
    sumN n (fun j => b j - a j) ≤ m*(t-1) + n*(s-1) := by
  have row_bound : ∀ j, j < n → b j - a j ≤
      sumN m (fun i => if a j + (s-1) ≤ i ∧ i < b j then 1 else 0) + (s-1) := by
    intro j hj
    rw [count_run]
    have := hrow j hj
    omega
  have h₁ := sumN_mono n _ _ row_bound
  rw [sumN_add, sumN_const, sumN_swap] at h₁
  have h₂ := sumN_mono m _ (fun _ => t-1) capacity
  rw [sumN_const] at h₂
  omega

/-- The charged late incidence includes all s consecutive point labels. -/
theorem window_contained (a b i s : Nat) (hs : 1 ≤ s)
    (late : a + (s-1) ≤ i ∧ i < b) :
    ∀ k, i+1-s ≤ k → k ≤ i → a ≤ k ∧ k < b := by
  omega

/-- Endpoint pigeonhole arithmetic: fewer than s labels, each with at most
2 occurrences, cannot supply 2s-1 distinct occurrences. -/
theorem endpoint_pigeonhole (s labels occurrences : Nat) (hs : 1 ≤ s)
    (hcap : occurrences ≤ 2*labels) (hcount : 2*s-1 ≤ occurrences) :
    s ≤ labels := by omega

/-- This is why a non-strict induction hypothesis requires B+1. -/
theorem strict_threshold (B restricted e : Nat) (hm : restricted ≤ B)
    (he : B+1 ≤ e) : restricted < e := by omega

/-- Final coefficient comparison, abstracting C=4^(r-2) (or 2^(r-2)).
The hypothesis C>=1 holds in every induction step. -/
theorem coefficient_step (c C a p z S : Nat) (hC : 1 ≤ C) :
    c*(p*a + z*(C*a*S)) ≤ (c*C)*a*(p+z*S) := by
  have hp : p ≤ C*p := by
    simpa using Nat.mul_le_mul_right p hC
  have hpa := Nat.mul_le_mul_left (c*a) hp
  calc
    c*(p*a + z*(C*a*S)) = (c*a)*p + (c*C)*a*(z*S) := by
      simp [Nat.mul_add, Nat.mul_comm, Nat.mul_left_comm]
    _ ≤ (c*a)*(C*p) + (c*C)*a*(z*S) := Nat.add_le_add_right hpa _
    _ = (c*C)*a*(p+z*S) := by
      simp [Nat.mul_add, Nat.mul_comm, Nat.mul_left_comm]

end NoveltyLab.IntervalBound
