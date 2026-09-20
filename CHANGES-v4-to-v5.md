# `free_fermion_cft_v4.tex` → `free_fermion_cft_v5.tex`

Revision implementing the eight findings of `critical-reread.pdf`. The source compiles clean
(0 errors, 0 undefined references/citations; 89 pp vs. 72 pp).
`diff_v4_v5.pdf` is a `latexdiff` rendering — deletions struck through in red, additions
underlined in blue.

> **Numbering.** Equation numbers below refer to the **published version (v4)**, as in
> `critical-reread.pdf`; *theorem/lemma/remark* numbers are the **v5** ones (they shift by one or
> two because of the new Corollary 3.8, Definition 3.10, Remark 3.11, Lemma 3.12,
> Corollary 3.14, Remarks 3.5/3.19/3.21, Remarks 4.3/4.7 and Hypothesis 6.4; Theorem 4.6 of v4 is
> Theorem 4.8 in v5). Displays new in v5 are marked
> *(v5)*.

**No theorem statement changed.** Theorems A, B, C and 4.6/4.11/4.16/5.1/6.1/6.3 (v4 numbering) are as before,
with hypotheses now quantified and one previously implicit ingredient of Theorem 6.3 promoted to
a stated hypothesis.

---

## 1. The `ŝ`-quotient (Findings 1 & 2) — the substantive fix

**Where.** Proof of Lemma 4.6 (`lem:KSconv`); the whole "Error estimates" paragraph.

**Problem.** The finite product `∏_{j=1}^{N-M} m₀(ε_{M+j}(m+k))` was rewritten as
`ŝ(ε_M(m+k))/ŝ(ε_N(m+k))` and the quotient bounded by a constant "because of the uniform
continuity of `ŝ`". Uniform continuity bounds a difference, not a quotient; and orthonormality
forces `ŝ(2πn)=0` for `n≠0`, so in the Ramond sector the denominator vanishes identically at the
admissible momenta `m+k = 2πn/ε_N ∈ Γ_{∞,+}`. The stated majorant is therefore false, and the
supremum defining `Error²(δ,L,k,N)` is `+∞` for every `k≠0`.

**Fix.**

- The product is **never** converted to a quotient: the third display of the proof of
  Lemma 4.6, the definition of `f_k^{(N)}(M,m)`, and the whole error paragraph now carry the
  product form, with a sentence explaining why immediately after it.
- **New Corollary 3.8** after Lemma 3.7 records what is actually needed: `P_J ≤ 1`, `P_J` is
  `2^{J+1}π`-periodic, `P_J(l) ≤ C_K(1+|l|)^{-K+𝒦_j}` **for `|l| ≤ 2^Jπ` only**, and
  `|ŝ(2^{-J}l)| P_J(l) = |ŝ(l)|`. The restriction to the fundamental domain is flagged
  explicitly — this is exactly what the old argument silently ignored.
- **New Lemma 3.12 (uniform majorant), with full proof**, supplying the `N`-independent
  `ℓ²`-majorant that the old argument lacked:
  `|ŝ(2^{-J}l − h)| P_J(l) ≤ C(1 + 2^{Jρ}|h|^K)(1+|l|)^{-ρ}`, `ρ := K − 𝒦_j`, for all `J`,
  all `l ∈ ℝ` and all `|h| ≤ π/2`. Neither factor decays on its own beyond the Brillouin zone —
  `P_J` only repeats periodically there. The proof exploits that the two decays *interlock*:
  `P_J` is of order one outside `[−2^Jπ, 2^Jπ)` only near multiples of `2^{J+1}π`, and exactly
  there `ŝ(2^{-J}l − h)` sits within `|h|` of an order-`K` zero of `ŝ`. Ingredients: the
  factorisation `ŝ(ξ) = (e^{-iξ/2} sinc(ξ/2))^K Λ(ξ)` with `|Λ| ≤ e^C(1+|ξ|)^{𝒦_j}` (obtained by
  letting `M → ∞` in the proof of Lemma 3.7) and a three-case analysis
  (`|l| ≤ 2^Jπ`; `|v| ≥ 2|h|`; `|v| < 2|h|`).
- **Corollary 3.13** specialises this to `g_k(M,m) = C(1+(L|k|)^K 2^{-Mρ})|m+k/2|(1+ε_M|m+k|)^{-ρ}`,
  which majorises `|f^{(N)}_k(M,m)` for **all** `N > M` and is in `ℓ²` iff `ρ > 3/2`.
- **Proof of Lemma 4.6** therefore keeps its original dominated-convergence structure, now with a
  correct majorant, plus a paragraph spelling out exactly why the naive majorant fails.
- **Error estimates rewritten** around the exact, division-free splitting *(v5, eq. 208)*:
  `f^{(N)}_k − f_k = (A) + (B)` with (A) the `O(ε_N²)` discretization term carrying the decaying
  factor `ŝ(ε_M(m+k))`, and (B) the `O(ε_N)` term. For `k=0`, (B) vanishes and the estimate
  closes exactly *(v5, eqs. 211–214)*, reproducing the `2^{-2δN}` rate with an explicit constant.
  New Remark 4.22 explains why the old sup-plus-Sobolev factorisation is unavailable for `k≠0`.
- **The `k≠0` estimate is now complete** *(v5, eqs. 222–224)*, splitting `Γ_{∞,±}` at the
  Brillouin zone: the interior is handled by Corollary 3.8 applied to `Q_N`, and the tail
  `|m+k| > π/ε_N` — where that corollary is unavailable — by Lemma 3.12, giving
  `Σ_tail ≤ C ε_M^{-3} 2^{-(2ρ-3)(N-M)}`, finite and exponentially small for the same reason
  that `g_k ∈ ℓ²`. Total: `Σ_N ≤ A₁ ε_N² + A₂ ε_N^{min{4, 2ρ-3}}`, with `A₁ = 0` for `k = 0`
  and after re-centring.

**New physics that fell out.** The `O(ε_N)` term (B) is identified: to first order
`ŝ(ε_N m)/ŝ(ε_N(m+k)) = e^{iμ(s)ε_N k}`, where `μ(s) = ∫x s(x)dx` is the **centre of mass** of the
scaling function — far from 0 for Daubechies (`μ(₄s) ≈ 5.99`, `μ(₁₀s) ≈ 16.87`). Since
`T_a ℓ_{±,k} T_a^* = e^{±ika} ℓ_{±,k}`, this is exactly the phase of a translation by `ε_N μ(s)`.
Comparing with the **re-centred** generators `e^{±iμ(s)ε_N k} L_{±,k}` (equivalently, replacing
`R^N_∞` by `T_{-ε_N μ(s)} R^N_∞`) removes it and restores the `k=0` rate *(v5, eq. 215)*; see
also Remark 4.21.

---

## 1b. Lemma 3.16 (scaling limit of the lattice vacua) — strengthened

Not one of the eight findings; the lemma was correct, but it can be sharpened on three counts.
The proof previously bounded the two-point function, invoked the decay estimate (Lemma 3.9) as
the dominating function, and closed with "the algebra is finite dimensional, so weak\* = strong".

- **The regularity hypothesis is removed entirely.** Writing out the pull-backs
  `Ŝ^{(N)}_M = R^{N*}_{N+M} S^{(N+M)} R^N_{N+M}` and `Ŝ^{(N)}_∞ = R^{N*}_∞ S R^N_∞` in momentum
  space shows they are **convex combinations over aliasing classes**,
  `Ŝ^{(N)}_M(l) = Σ_{k∼l} w_M(k) S^{(N+M)}_per(k)`, with
  `w_M = |∏_{m≤M} m₀(ε_{N+m}·)|²`, `w_∞ = |ŝ(ε_N ·)|²`, and — this is the point —
  `Σ_{k∼l} w = 1` **exactly**. For `w_M` that is the filter relation
  `|m₀(ξ)|² + |m₀(ξ+π)|² = 1` iterated; for `w_∞` the orthonormality relation
  `Σ_n |ŝ(ξ+2πn)|² = 1`; for the momentum cutoff, that each class meets `Γ_N` once. So the
  weights are *probability* weights and no decay estimate on `ŝ` is needed anywhere. The lemma
  now holds for **any** compactly supported orthonormal scaling function, including Haar, whose
  `ŝ` decays only like `|ξ|^{-1}` and for which (109) is unavailable.
- **The limit is a Scheffé argument.** `w_M → w_∞` pointwise is the scaling relation (102);
  since both are probability weights this upgrades to total variation, and dominated convergence
  against the *fixed* probability measure `μ^l_∞` (majorant 2) handles the symbol deviation.
  Hence `δ_M(N) := max_l ‖Ŝ^{(N)}_M(l) − Ŝ^{(N)}_∞(l)‖ → 0` (`Γ_{N,±}` finite).
- **Two quantitative conclusions replace the bare finite-dimensionality appeal** *(v5, eqs.
  134–135)*: a determinant/Hadamard telescoping gives
  `|(ω^{(N)}_M − ω^{(N)}_S)(A)| ≤ n δ_M(N) ∏‖η‖` on monomials of degree `2n` — **independent of
  the number of lattice sites** — and, since momentum-diagonality makes both states products
  over modes, subadditivity of the trace distance gives
  `‖ω^{(N)}_M − ω^{(N)}_S‖ ≤ 2L_N ϖ(δ_M(N))`, `ϖ` the modulus of continuity of `T ↦ ω_T` on the
  compact set `{0 ≤ T ≤ 1} ⊂ M₂(ℂ)`. The `N`-dependence is now isolated as the mode count.
- **Both renormalization groups are covered by one argument** (`w_∞ = χ_{Γ_N}` is a Dirac
  measure on each class), so the old Remark 3.18 becomes a one-line special case; it is replaced
  by Remark 3.18 (what the hypothesis-free statement means) and new Remark 3.19 (where the rate
  comes from — and why a *supremum* over the aliasing class would not be small).
- Corrigenda in the old proof: `δ_{0, (π/L)(k−l) mod 2L_N}` → `(L/π)`, consistent with (126);
  "weak\* ⟹ **strong** convergence" → norm convergence; and the hypothesis (122) is restated as
  a limit over `k ∈ Γ_{∞,±}` of the periodic extensions, rather than over `k ∈ Γ_{N,±}`.

---

## 1c. Corollary 3.17 (scaling limit of the lattice vacua) — a gap and a rate

- **Gap: the zero mode.** The one-line proof ("the renormalization condition implies point-wise
  convergence of `S^{(N)}_0(k)`") holds for every `k` with `(m,k) ≠ (0,0)`, but fails at exactly
  that point — which occurs in the Ramond sector, `0 ∈ Γ_{∞,+}`, in the **massless** case, i.e.
  the case the paper is about. There `ω_m(0) = 0`, `P^{(+)}_{m=0}(0)` is not defined by (115),
  and the massless limit is direction-dependent: the convention `sign(0)=0` of (60) (i.e.
  `λ_N ≡ 0`) gives `S(0) = ½·1₂`, whereas `λ_N > 0` with `ε_N^{-1}λ_N → 0` gives
  `P^{(+)}_{λ_N}(0) = ½(1₂+σ_z)` for *every* `N`, hence `S(0) = ½(1₂−σ_z)` — a **different**
  scaling-limit state. The corollary now carries the convention as an explicit hypothesis.
- **Why it is not harmless.** New Remark 3.18. Since `ŝ(0)=1`, `ŝ(2πn)=0` for `n≠0` and
  `m₀(π)=0`, the aliasing class of `l = 0` carries *all* its weight at `k = 0`, so (137)
  degenerates to `Ŝ^{(N)}_M(0) = S^{(N+M)}(0)`, `Ŝ^{(N)}_∞(0) = S(0)`: a discrepancy at the zero
  mode is **not** averaged away, enters `δ_M(N)` undamped, and is visible already in the
  two-point function. Verified numerically (`os_check10.py`): `w_∞(0) = 1` to machine precision,
  all other weights `< 2·10^{-30}`. The chosen convention is the one consistent with the rest of
  the paper — the doubled projection (171) has the block `(½ ±½; ±½ ½)` at `k=0`, precisely the
  purification (11) of `S(0) = ½·1₂`, which is what makes `ω₊` impure and gives `h = 1/8`
  resp. `1/16`.
- **An exact error identity and an `N`-uniform rate.** Subtracting (118) from (60) gives
  `‖S^{(N)}_0(k) − S(k)‖ = |sin(ε_N k/4)|` **exactly** (verified to `10^{-16}`), hence the
  scale-free bound `≤ π^{-1} ε_{N+M}|k|` inside *and* outside the Brillouin zone. Feeding this
  into Step 2 of Lemma 3.16 yields
  `δ_M(N) ≤ (C_s/π) 2^{-M} + 3 max_l ‖μ^l_M − μ^l_∞‖_TV`, with
  `C_s = sup_u Σ_n |ŝ(u+2πn)|² |u+2πn|` finite iff `s ∈ H^{1/2}`. Both bounds are **independent
  of `N`**; measured rate of `δ_M(N)` is `2^{-1.00·M}` for db4 and db8 at `N = 2,3,4`.
  Combined with (134) this gives an `N`-uniform error `≤ n δ_M(N)` for every monomial of degree
  `2n` — the form needed in Remark 4.23 (CFT simulation).
- Note the pattern: the *statement* of Lemma 3.16 needs no regularity, but this *rate* needs
  `s ∈ H^{1/2}`, which Haar just fails (`|ŝ|² |ξ|` is then not summable). Recorded in
  Remark 3.20.

---

## 1d. Lemma 4.6 and Theorem 4.8 — full domain and a sharp rate

- **Convergence on the whole domain, not just a core.** The one-particle statement was proved on
  the wavelet span `D_W`; it holds on all of `h¹(Γ_{∞,±}) = D(ℓ_{±,k})`. The ingredient is a
  uniform bound: writing `(R^N_∞)^* ξ̂(l) = ε_N^{-1/2} Σ_{k∼l} conj(ŝ(ε_N k)) ξ̂(k)` and applying
  Cauchy–Schwarz against the **probability** weights of Lemma 3.16, together with `|l| ≤ |k|` on
  each aliasing class, gives `‖(R^N_∞)^*‖_{h^σ→h^σ} ≤ 1` for every `σ ≥ 0`, hence
  `‖ℓ̃^{(N)}_{±,k}ξ‖ ≤ C_{k,L}‖ξ‖_{h¹}` **uniformly in `N`** (new eqs. 209–210). Density of `D_W`
  in `h¹` then does the rest. Measured `C_{k,L} → 1` for `L = π`.
- **Consequence for Theorem 4.8.** The core `F^alg_a(D_W)` enlarges to `D(dΓ(⟨·⟩))` — a domain
  that, unlike `F^alg_a(D_W)`, does not depend on the choice of scaling function — and the
  convergence acquires the quantitative energy-type form *(v5, eq. 213)*
  `‖(α^N_∞(L^{(N)}_{±,k}) − L_{±,k})Φ‖ ≤ (L/π) C ε_N^{min{δ,1}} ‖dΓ(⟨·⟩^{1+δ})Φ‖`,
  using `dΓ(⟨·⟩^{1+δ}) ≤ (dΓ(⟨·⟩))^{1+δ}`. This is a `c = 0` analogue of the energy bound that
  Hypothesis 6.4 postulates in `π_±`.
- **Sharp rate in the Sobolev scale** (new Remark 4.7). The uniform bound cannot be upgraded to
  norm convergence at `σ = 1`: taking `ξ = e_n` with `n` the point of `Γ_{∞,±}` nearest
  `π/ε_N`, the lattice symbol is `O(1)` while `‖ℓ_{±,k}e_n‖ ∼ (π/ε_N)‖e_n‖`, giving the lower
  bound `‖ℓ̃^{(N)} − ℓ‖_{h^{1+δ}→h⁰} ≥ c ε_N^δ` — this is the Brillouin-zone edge, i.e. exactly
  what the prefactor `(π/2L_N)|sin(ε_N k/2)|^{-1}` of Definition 4.1 was introduced to tame.
  Conversely `≤ C ε_N^{min{δ,1}}` for `0 < 1+δ < σ_K`, by splitting into a projection error
  (Jackson `‖(1−P_N)‖_{h^{1+δ}→h¹} ≤ Cε_N^δ` plus `h^{1+δ}`-stability of `P_N`) and a
  consistency error whose symbol deviates by `O(ε_N(|l|+|k|)²)` — the centre-of-mass phase again.
  So the exponents match for `0 < δ ≤ 1`, and re-centring improves the upper one to `min{δ,2}`.
  Numerics (`os_check11.py`, `L=π`, `k=2`, db4): at `δ = 0` the operator norm is
  `1.365, 1.824, 1.107, 1.036, 1.035` for `N = 3..7` — no convergence; after re-centring the
  measured rates are `1.00, 1.50, 2.00` at `δ = 1, 3/2, 5/2`, i.e. **exactly** `min{δ,2}`.

---

## 1e. Re-centring offered as an alternative (new Remark 3.5)

The `O(ε_N)` defect identified in §1a is the offset `ε_N μ(s)` between a lattice site and the
centre of mass of the wavelet sitting on it, `μ(s) = ∫ x s(x) dx = 2^{-1/2} Σ_n n h_n`. New
Remark 3.5 states this, gives `T_a ℓ_{±,k} T_a^* = e^{±ika} ℓ_{±,k}` (so re-centring is one phase
per mode, tending to 1), and records that removing it gains one order in every wavelet-route rate.

It is **deliberately not built into Definition 3.2**, and the remark says why:

- the re-centred maps `T_{−a_N} R^N_∞` with `a_N = ε_N μ(s)` fail asymptotic compatibility,
  Proposition 3.7(4), since `a_{N+1} = a_N/2`; they do not form an inductive system, so the
  scaling-limit construction of Section 3 would have to be redone;
- re-centring the scaling function instead does not work either: `s(· + μ(s))` is orthonormal but
  satisfies a scaling equation with non-integer shifts `n − μ(s)`, so it is not the scaling
  function of a dyadic multiresolution analysis.

It is therefore carried along as a *comparison convention*, invoked only where rates are stated
(the error paragraph, Remarks 4.7 and 4.22 now point at Remark 3.5). The remark closes by noting
that the **momentum-cutoff group needs no such convention**: no scaling function enters its
symbol, `χ_{Γ_N}` contributes no first moment, and its error is `O(ε_N²)` from the outset — one
further concrete advantage of that group, alongside the invariance of `D_std` under the Hardy
projections.

---

## 1f. Theorem 4.13 and Lemma 4.12 — proofs, rates, and a corrected self-adjointness argument

- **Theorem 4.13 had no proof.** It now has one: (218) reduces it to `dF_±(ℓ̃^{(N)}_{±,k} − ℓ_{±,k})`
  and the four terms of (224) are killed by Lemma 4.12. Core extended from `F^alg_a(D_std)` to
  `D(dΓ(⟨·⟩^{1+δ}))`, with the rate (228)
  `≤ (L/π)(C ε_N^{min{δ,2}}‖dΓ(⟨·⟩^{1+δ})Φ‖ + √C_k ε_N²‖(N+2)Φ‖)`.
- **Lemma 4.12 now has a proof and is sharp.** For the momentum cutoff the difference is an
  explicit multiplier-with-shift, so the operator norm is a supremum computable in closed form:
  `‖ℓ̃^{(N)}_{±,k} − ℓ_{±,k}‖_{h^{1+δ}→h⁰} ≍ ε_N^{min{δ,2}}` and `‖(·)_{±∓}‖₂ ≤ √C_k ε_N²`, plus
  the `h¹` domain extension. **No regularity of `s` is assumed** — no scaling function occurs in
  (223) at all — and the exponent is `min{δ,2}` rather than `min{δ,1}`, there being no
  centre-of-mass defect (Remark 3.5).
- **The asserted analytic vectors do not follow.** In `π_±` the pair terms of (22) raise the
  particle number and iterating (25) with (205) gives `(j!)²` after `j` steps, so the exponential
  series diverges for every `t`; the plane-wave Fock vectors cannot be shown to be analytic this
  way. (The statement is presumably true — it is the Goodman–Wallach/Carpi–Weiner analyticity of
  finite-energy vectors — but not by the argument given.) Replaced by **Corollary 4.15**, via
  Nelson's *commutator* theorem with `N = 1 + L_{±,0}`: hypothesis (i) is the energy bound,
  hypothesis (ii) follows from `[L_{±,0}, L_{±,k}] = −(L/π)k L_{±,k}` together with the form
  bound. The conclusion is stronger than what was claimed — essential self-adjointness on *every*
  core for `1 + L_{±,0}`, in particular on `D(L_{±,0})`.
- **Energy bound split** to avoid a §4 → §6 forward reference: **Lemma 4.14** (fixed `k`, no
  regularity) and **Proposition 6.4** (smeared; the `k`-summation via Corollary 3.9 is the only
  point in the paper where regularity enters this argument).

---

## 1g. §5, WZW currents — a gap, and then a much stronger theorem

- **Gap found.** `j^{(N)}_k` of (254) is the *cyclic* shift on `Γ_{N,−}`; at the upper
  Brillouin-zone edge the wrap-around sends `+π/ε_N` to `−π/ε_N`, **across the Fermi point**. So
  `‖(j̃^{(N)}_k − j_k)_{−+}‖₂ = (|k|L/π)^{1/2}` for *every* `N` and does not tend to 0 (verified:
  `1.0, 1.7, 2.4` for `k = 1, 3, 6`). The third hypothesis of Lemma 4.19 fails, so the proof
  "identical to that of Theorem 4.20" is not available. The theorem is still true — the offending
  block sits at momenta `≈ ±π/ε_N` and annihilates any fixed finite-particle vector once `N` is
  large — but not for the stated reason.
- **Fix.** Carry over the `χ_{Γ_N}` modification of §4.2.2, which §5 had not done: (262).
- **New Lemma 5.1**, proved, with four exact statements: `j̄̃^{(N)}_k = j_k` on the bulk (no
  discretisation error at all); off-diagonal blocks **identically zero**, hence no
  Schwinger-cocycle error at finite scale and `c = 1` exactly once `π/ε_N > 2|k|`;
  `‖j̄̃^{(N)}_k − j_k‖_{h^δ→h⁰} ≍ ε_N^δ` **uncapped** in `δ` (vs. `min{δ,2}` for the KS
  approximants), with `‖·‖ = 1` at `δ = 0`; and strong convergence on all of `h^{(+)}_{∞,−}`.
- **Theorem 5.2** now holds on `D(N)` — number operator, not energy, `j_k` being bounded — with
  **no regularity assumption** for the qualitative statement, plus the rate (265) under
  `(δ+½)`-regularity. New **Remark 5.3** collects the comparison with the Virasoro case.
- Corrigendum: (256) read `j_k^* = j_k`; the adjoint of a translation is `j_{-k}`.

---

## 1h. §6 — an explicit error bound, and the quantum-simulation budget

- **Proposition 6.3**, new: Theorem 6.1 made quantitative for the chiral time evolution,
  `|C^(N)_t − C_t| ≤ (d_A+d_B) η_M(N) + (1/6) d_B Θ_M |t| ε_N²`. The original proof routes through
  an intermediate scale `K`; that is avoidable here, and the avoidance matters — optimising
  `2^{-2K} + 2^{-(N−K)}` over `K` yields only `2^{-2N/3}`. What makes it avoidable: `ℓ^{(N)}_{±,0}`
  is a Fourier multiplier, so the lattice dynamics moves no momenta, and `α^M_N` maps into
  `span{e_l}_{l∈Γ_M}`; the evolved observable therefore stays supported on `|l| ≤ π/ε_M` for all
  `t`, and only the vacuum-symbol deviation there contributes.
- **The ground state is the bottleneck, and chirality squares it.**
  `η_M(N) = max_{l∈Γ_M}‖S_0^(N)(l) − S(l)|` equals `|sin(π2^{-(N−M)}/4)|` on the full
  two-component algebra (**first** order) but `sin(π2^{-(N−M)}/4)²` on a chiral subalgebra
  (**second** order) — verified to seven digits, measured orders `1.00` and `2.00`. The
  first-order term is precisely the chiral entanglement (65) of the massless lattice vacuum, whose
  off-diagonal block `p_± P^{(+)}_{λ_N=0} p_∓` is `O(ε_N k)` while its continuum counterpart
  vanishes. On the full algebra it dominates the second-order dynamics term; on a chiral
  subalgebra — where the conformal structure lives — the two match.
- **Remark 6.4**, new: the end-to-end budget. Both error sources scale in `N − M`, not `N`
  (`Θ_M ε_N² ≍ ε_M^{-3/2} 2^{-2(N−M)}`), and with `#qubits = #Λ_{N+1} ∝ 2^N` one gets
  `#qubits = O(2^M √(d(1+T)/η))` for chiral observables via the momentum-cutoff group, degrading
  to `O(2^M d(1+T)/η)` — a quadratic loss — on the full algebra or along the un-recentred wavelet
  route. The prefactor `2^M ≳ 2K−1` comes from the localisation constraint of Remark 4.26 and
  `K ≥ 5` from 2-regularity. Currents (Lemma 5.1) attain the square root under weaker hypotheses.
  Remark 4.26 now points forward to this.

---

## 1i. Lemma 4.19 / Theorem 4.21 (smeared) — domain, rate, and the phase structure

- **Domain and uniform bound.** `‖ℓ̃^{(N)}_±(S^M_N X)‖_{h¹→h⁰} ≤ C_{X,M}` uniformly in `N` under
  `3/2`-regularity (233), hence all three statements of Lemma 4.19 extend from `D_std` to all of
  `h¹`; Theorem 4.21's core extends to `D(dΓ(⟨·⟩^{1+δ}))` with the rate (238). Hypotheses now
  quantified: `K ≥ 4` for the domain, `K ≥ 6` for the rate.
- **Structure of the two errors.** Written with a common prefactor, both smeared operators carry
  *loop weights* `w^(N)_k = ∏_{j≤N−M} m₀(ε_{M+j}k)` and `w^(∞)_k = ŝ(ε_M k)`, related in closed
  form by the scaling relation: `w^(N)_k − w^(∞)_k = w^(N)_k (1 − ŝ(ε_N k))` (232). So the
  smearing error is the deviation of `ŝ` from 1 at the **fine** scale — first order, the
  centre-of-mass phase again — and it, not the generator, is what limits (234) to
  `ε_N^{min{δ,1}}`.
- **New Remark 4.20: the smearing error is a phase.** Orthonormality plus the order-`K` zero of
  `m₀` at `π` give `|m₀(ξ)| = 1 + O(ξ^{2K})`, hence `|ŝ(ξ)| = 1 + O(ξ^{2K})` (235). Therefore
  `ŝ = e^{iφ}(1+O(ξ^{2K}))` with `φ` real and odd, `φ(ξ) = −μ(s)ξ + O(ξ³)`, and re-centring
  reduces (232) from first to **third** order (measured `3.00` for db4 and db8; the flatness is
  measurable only for db2, order `4.00 = 2K`). Consequently the exponent in (234) improves to
  `min{δ,2}`: **with re-centring the smeared wavelet route loses nothing against the
  momentum-cutoff one**, which together with Remark 6.4(4) settles the trade-off — the wavelet
  group's real-space locality is then free.

---

## 2. Regularity thresholds (Finding 3)

**New Definition 3.10** (`σ_K` = Sobolev exponent, "ρ-regular") and **new Remark 3.11** with the
table of `σ_K` for `K = 2,…,11` and the three thresholds that actually occur:

| requirement | where | threshold | minimal `K` |
|---|---|---|---|
| `D_W ⊂ D(ℓ_{±,k})`, majorant in `ℓ²` | Lemma 4.6 | `σ_K > 1` | **3** (`₂s` is *exactly* borderline) |
| both Cauchy–Schwarz factors | Lemma 4.16 | `σ_K > 3/2` | **4** |
| `‖ŝ(ε_M ·)‖_{h^{1+δ}} < ∞`, rate `2^{-2δN}` | error estimates | `σ_K > 1+δ` | **5** (`δ=1`), **9** (`δ=2`) |

Lemma 4.6 now carries the hypothesis "`1`-regular" instead of "sufficiently regular", and the
core argument on p. 44 states that `D_W` is `h¹`-dense *only under that hypothesis*.

---

## 3. Remark 4.15, Moebius group (Finding 4)

The claim "a simple extension of Lemma 4.6 is sufficient" is withdrawn and replaced by a correct
argument. The Hilbert–Schmidt norms do vanish for `k = 0, ±π/L`, but (200) also needs the
diagonal blocks on the *Hardy-projected* vectors `P^∓ξ`, and `P^±` does not map `D_W` into `D_W`.
What closes it: `ℓ_{±,k}` and `ℓ̃^{(N)}_{±,k}` are bounded `h¹ → h⁰` uniformly in `N`, `D_W` is
`h¹`-dense, and `P^±` preserves `h¹`. The remark now also notes that this is an independent
reason for passing to the momentum-cutoff group, where `P^±` leaves `D_std` invariant.

---

## 4. Normalisation of `ℓ_{±,k}` (Finding 5)

Definition 4.2 carried a spurious factor `L/π` relative to the symbols in (165)/(167); taken
literally, (170) would give `c = (L/π)²` rather than `c = 1`. Definition 4.2 is renormalised to
`ℓ_{±,k} e_m = ±(m∓k/2) e_{m∓k}`, i.e. `±1/(2π) → ±1/(2L)` in (181) and (184), and the
consequential constants are corrected in (187), (198), (199), (201), (212), (213) and (194).
**New Remark 4.3** records the normalisation and verifies `c = 1` (resp. `1/2`) for every `L`.
Everything is now consistent with `L_{±,k} = (L/π) dF_S(ℓ_{±,k})` throughout.

---

## 5. Theorem 6.3 (Finding 6) — now unconditional

The proof previously ended with two asserted "additional observations". They are the decisive
step and are not implied by Theorem 4.17: already `L_±(X)Ω₀` is an infinite two-particle
superposition (after smearing the off-diagonal block is Hilbert–Schmidt but no longer of finite
rank, unlike the unsmeared `(ℓ_{±,k})_{±∓}`), so it lies outside `F^alg_a(D_std)`.
**Proposition 6.4** supplies the required `N`-uniform energy bound
`‖:π_±(α^N_∞(L^{(N)}_±(S^M_N(X)))): Ψ‖ ≤ C_X ‖(1+L_{±,0})Ψ‖`, **with proof**, so Theorem 6.3 is
unconditional. Three steps: (i) `sup_N ‖A^{-1/2} G^{(N)} A^{-1/2}‖ < ∞` with `A = ⟨·⟩`, from
`‖A^{-1/2} ℓ̃^{(N)}_{±,k} A^{-1/2}‖ ≤ C⟨k⟩^{1/2}` summed against `S^M_N(X̂)` via Corollary 3.9 —
convergent iff `ρ − 1/2 > 1`, i.e. under the **1-regularity already assumed in Lemma 4.6**, so no
new hypothesis; (ii) real/imaginary parts and monotonicity of `dΓ` for the diagonal blocks;
(iii) `sup_N ‖G^{(N)}_{±∓}‖₂ < ∞`, which is free because Lemma 4.17 proves those HS norms
*converge*. Finally `dΓ(⟨·⟩) = N + L_{±,0}`, with `N ≤ 2L_{±,0}` in NS and `N ≤ 2·1 + L_{±,0}` in
Ramond (the zero mode spans two dimensions of the doubled space (171), so Pauli caps its
occupancy). A new bibitem for Buchholz–Schulz-Mirbach (1990) was added.

---

## 6. Locality claim for Theorem 4.17 (Finding 7)

The preamble claimed the two-RG combination preserves "localization in real space in the sense of
Proposition 3.6". Proposition 3.6 is about the *wavelet* group; in Theorem 4.17 the fermion
algebra is transported by the *momentum-cutoff* maps, which by (112) do not preserve
localization. Reworded: the **smearing functions** are wavelet-localized at scale `ε_M`, and the
technical role of the wavelet group for loops is summability of the `k`-sum, not locality.

---

## 7. Corrigenda (Finding 8)

- **(25)**: `‖aG₊₋aP_{≤n}‖ ≤ n‖G₊₋‖₂` → `‖aG₋₊aP_{≤n}‖ ≤ n‖G₋₊‖₂` (as used in (200)).
- **Lemma 3.7**: `=` → `≤`; `max{e^C, π^{-𝒦_j}} = e^C` since `𝒦_j ≥ 0`; case 3 of the proof
  claimed `2^{M𝒦_j} ≤ π^{-𝒦_j}(1+|l|)^{𝒦_j}`, which fails on `2^M < |l| < π2^M − 1` — the
  correct step is `2^{M𝒦_j} ≤ (1+|l|)^{𝒦_j}`.
- **(213)**: `binom(2j,j)^{1/2}|k|^j Γ(·+j)/Γ(·) ≤ (4a)^j j!`, not `(2a)^j j!`, with
  `a = |m| + |k|/2`; the resulting bound now reads `4L(2at)²/(1−2at)`.
- **§4.2.2**: added a sentence that the lattice Virasoro relations (146) and the `O(ε_N²)`
  remainders (147) were computed for the *unmodified* approximants, and that
  `χ̂_{Γ_N}(·+k)` is a Dirichlet kernel decaying only like `|x|^{-1}`.

### §1j — the Bogoliubov corollaries made quantitative (Tier-2 item 8)

The convergence of all Bogoliubov transformations was obtained in v4 from strong resolvent
convergence, hence without any rate. Two Duhamel lemmas replace that argument:

- **New Lemma 4.11 (One-particle energy growth and Duhamel)** + **(220)**/**(221)**, with
  `c_{σ,k} ≤ C_L σ|k|⟨k⟩^{σ+2}`, `c_{σ,0} = 0`, and `λ_{σ,k}(t) = (e^{c_{σ,k}|t|}−1)/c_{σ,k}`
  (`= |t|` at `k = 0`). Key point: `ℓ_{±,k}` is a weighted shift, so the commutator with the
  Sobolev weight is again a shift, and the `1/⟨l⟩` produced by differentiating `⟨l⟩^σ` cancels the
  `⟨l⟩` growth of the shift weight. The mollifier `(1+ρ⟨l⟩)^{-σ}` makes the Grönwall
  differentiation legitimate; `ρ↓0` by monotone convergence, then density + Fatou.
- **(223)**: Corollary 4.9 (and, with (231), Corollary 4.20) becomes
  `‖σ̃^{(N)}_t(π_S(A)) − σ_t(π_S(A))‖ ≤ C_{k,L,δ} ε_N^{min{δ,1}} λ_{1+δ,k}(t) (∏‖ξ_l‖)Σ_q‖ξ_q‖_{h^{1+δ}}/‖ξ_q‖`,
  with `min{δ,1}` improving to `min{δ,2}` for the momentum-cutoff group by (231).
- **New Remark 4.12 (Smeared generators)** + **(224)**: the same proof with the sum over `k`,
  requiring `Σ_k|Ŷ_k||k|⟨k⟩^{σ+2} < ∞`, which holds for `K − 𝒦₂ > σ + 4` by (109). Flagged as
  sufficient but not sharp.
- **New Lemma 4.18 (Energy growth and Duhamel)**, Fock space, `𝒩 = 1 + L_{±,0}`, using the
  Virasoro relation `[L_{±,0},L_{±,k}] = −(L/π)kL_{±,k}` and the form bound (235) from Lemma 4.16;
  **Corollary 4.19** restated with **(238)**.
- **(239)**: the derivations of Corollary 4.13 need no `t`-dependence at all, so (225) together
  with (231) gives the bound directly.

Consequence worth noting: for `k = 0` — the chiral time evolution the simulation budget of
Remark 6.4 relies on — every one of these bounds is *linear* in `t`; the exponential factor
appears only for `k ≠ 0`.

### §1k — reconstruction of the smeared Virasoro generators (Tier-2 item 9)

Remark 4.27 gave a three-term splitting and concluded that "in principle" one can
reach arbitrary smooth smearing functions. That is now a theorem:

- **(252)** Wiener seminorms `p_{N,m}`, **(253)** the
  `N`-uniform bound `‖ℓ̃⁽ᴺ⁾_±(Y)‖_{h¹→h⁰} + ‖(ℓ̃⁽ᴺ⁾_±(Y))_{±∓}‖₂ ≤ C_L p_{N,3/2}(Y)`. The `3/2` is
  forced by the off-diagonal Hilbert–Schmidt block and simultaneously dominates the `h¹→h⁰` bound.
- **New Lemma 4.28** + **(254)/(255)**: a Jackson
  estimate for the loop RG. The key input is that orthonormality of `s` reads `Σ_i|ŝ(ξ−2πi)|² = 1`,
  so the aliasing mass is `1−|ŝ(ξ)|² = O(ξ^{2K})` by (249) and *each* replica coefficient
  is `O(|ξ|^K)`. This is what kills the `ε_M^{-1}` from the momentum weight; the estimate is
  genuinely false without it.
- **New Theorem 4.29**: convergence to `L_±(X)` for every smooth `X`, from
  `K ≥ 9` (limit) and `K ≥ 10` (`O(ε_M)` rate).
- **New Remark 4.30** + **(258)**: the two-scale rate
  `C_L p_{N,3/2}(X_N − S^M_N(X_M)) + C_{X,M,δ}ε_N^{min{δ,1}} + C_X ε_M`.

### §1l — explicit analyticity radius (Tier-2 item 10)

- **(209)/(210)**: the radius of the analytic-vector series
  is `1/|k|`, **uniform in `m`** (equivalently `π/(L|k|)` in the `L/π` normalisation of
  Remark 4.4); the same for `r_{±,k}`, `ι_{±,k}` since
  `(1/2)^j binom(2j,j)^{1/2} ≤ 1`. For `k = 0` only `1/|m|`, which is immaterial.
- **(273)**: the sharpened form of (272), keeping the
  Gamma-quotient instead of bounding it by `(2(|m|+|k|/2))^j j!`. Valid on all of `t < 1/|k|` instead
  of `t < 1/(2|m|+|k|)`, leading coefficient smaller by a factor of 8. The remark now also states
  *which* step was lossy: not `binom(2j,j)^{1/2} ≤ 2^j` (sharp, and cancelled by `(1/2)^j`) but the
  handling of the Gamma-quotient when `|k| ≪ |m|`, the regime relevant for the conformal limit.

### §1m — quasi-local structure quantified (Tier-3 item 11)

**New Remark 3.8** + **(108)**: `supp(_K s) = [0,2K−1]`
gives a **strict, one-sided light cone** of width `ε_N(2K−1)` for the wavelet RG, with no tail —
unlike the momentum-cutoff kernel, which decays only like `|x|^{-1}`. Definition 3.6
discards exactly `2K−1` sites per interval. Headline: the light-cone width and the re-centring offset
`ε_Nμ(s)` are the same order (`μ(_K s)/(2K−1) = 0.789 … 0.891` for `K = 2 … 12`), so **locality and
regularity trade off linearly in `K`**.

### §1n — the modified approximants' finite-scale algebra (Tier-3 item 12)

**New Remark 4.2** + **(181)/(182)**: the modified
one-particle approximant is a *truncated* weighted shift where the unmodified one wraps around `Γ_N`.
The discrepancy in the commutator **vanishes identically for same-sign `k,k'` and for `k'=0`** (both
partial shifts are trapped between `l` and `l+k+k'`), so (164)/(165) hold
verbatim there — including the pair `(k,0)` used by Lemma 4.17. For opposite signs it
is finite rank and boundary-supported: `O(1)` in operator norm but
`‖·‖_{h^σ→h⁰} ≤ C ε_N^σ`, which beats the accompanying `O(ε_N²)` remainder once `σ > 2`.

### §1o — the XY half-shift identity (Tier-3 item 13)

**(277)**:
`H⁽ᴺ⁾_k = 2e^{−iε_Nk/4}(cos(¼ε_Nk) H̃⁽ᴺ⁾_k + i sin(¼ε_Nk) H̃⁽ᴺ⁾_{k+π/ε_{N+1}})`. The two-component
mode at `k` mixes the single-component mode at `k` with the **umklapp** mode at `k + π/ε_{N+1}`, with
amplitude `sin(¼ε_Nk) = O(ε_Nk)` — the precise sense in which (274) and
(275) are not directly comparable. It also identifies the `e^{∓iε_Nk/4}` prefactor of
(274) as coming from the half-shift rather than from the Koo–Saleur combination.

### §1p — both decay exponents (Tier-3 item 14)

Remark 3.13 gains a second table row with the pointwise exponent `ρ` beside the
`L²` exponent `σ_K`, plus a statement of which is the right tool where: `ρ` for bounding a single
value of `ŝ` (Lemma 3.14, (111), (255)), `σ_K` for sums
against a Sobolev weight (every "`ρ`-regular" hypothesis). Corrected in passing: three citations added
in items 8–10 pointed at the finite-product lemma (110) for the pointwise decay of `ŝ`,
which is (113), and named the measured exponent `K−𝒦₂` where Lemma 3.11 only
gives `K−𝒦`.

---

## Numerical verification

`numerics/` (pure `numpy`, Daubechies filters built by spectral factorisation, orthonormality
`< 6·10⁻¹⁵`, Sobolev exponents reproducing the literature to 3–4 digits):

| script | checks |
|---|---|
| `os_check.py` | order-`K` zeros of `ŝ` at `2πZ\{0}`; the quotient in both sectors |
| `os_check2.py` | product form ≡ quotient form where defined; failure of the old majorant; `ℓ²`-convergence; `2^{-KN}` resonance decay; `Error² = +∞` (Ramond) |
| `os_check3.py` | decay exponents; existence of a valid majorant; `Error²` in NS; `P⁺s^{(ε_M)} ∉ V_J` |
| `os_check4.py` | Daubechies filters and `σ_K` for `K = 2..12` |
| `os_check8.py` | the region-(b) ratio of Lemma 3.12 stays bounded (in fact decreases) in `N`; BZ/tail split of `Σ_N` |
| `os_check9.py` | the alias weights of Lemma 3.16 sum to 1 exactly, for `K = 1` (Haar) through `K = 8` |
| `os_check15.py` | smearing weights: `|1−ŝ(ε_N k)|` order 1, re-centred order 3; `|ŝ|` flat to `ξ^{2K}`; smeared operator-norm rates |
| `os_check14.py` | vacuum-symbol deviation: order 1 on the full algebra, order 2 on the chiral subalgebra, closed forms to 7 digits |
| `os_check13.py` | currents: exact bulk agreement; unmodified HS norm `= √(|k|L/π)` constant; modified `= 0`; rate `ε_N^δ` uncapped |
| `os_check12.py` | momentum-cutoff rates: `min{δ,2}` in the Sobolev scale (exactly `1` at `δ=0`), HS rate `2` |
| `os_check11.py` | operator norms `‖ℓ̃^{(N)}−ℓ‖_{h^{1+δ}→h⁰}`: uniform `h¹→h⁰` bound, no convergence at `δ=0`, rate `min{δ,2}` after re-centring |
| `os_check10.py` | `‖S^{(N)}_0(k)−S(k)‖ = |sin(ε_N k/4)|`; the `k=0` class is alias-free; `δ_M(N) ~ 2^{-M}` uniformly in `N` |
| `os_check5.py` | Schwinger cocycle in both normalisations (`c = 1` vs `c = (L/π)²`) |
| `os_check6.py` | rates of `Σ_m|f^{(N)}_k − f_k|²`: **2** for `k≠0`, **4** for `k=0` (the latter only from `db10` on) |
| `os_check7.py` | the `O(ε_N)` term is the centre-of-mass phase: re-centring restores rate **4** and drops the constant by 4–5 orders of magnitude |
| `os_check16.py` | the one-particle Duhamel lemma: commutator ratio bounded by `0.36` uniformly in the mollifier `ρ` and in `(σ,k)`; **exact** `h^σ`-conservation at `k=0` (`10^{-15}`); Duhamel bound (221) holds with `≥4×` margin; `⟨k⟩^{σ+2}` conservative vs. the true `σ|k|⟨k⟩` |
| `os_check17.py` | items 9 & 10: `Σ_i|ŝ(ξ−2πi)|²=1` to `10^{-13}`; aliasing mass `δ(ξ)` of order **exactly `2K`** (4/8/12/16 for db2/4/6/8); true order of (252) **exactly `K`** ⇒ the `Kβ` in the proof is conservative; Jackson rate (251) `= 1.00` in `ε_M`; `max_j(1/2)^j binom(2j,j)^{1/2} = 1.000000`; radius gain `11×–101×`; leading-coefficient ratio (269)/(270) `→ 7.9 ≈ 8`. Needs a **numerically stable `m₀`** — deflating the order-`K` zero at `z=−1` — since `m₀(π+δ) ~ δ^K` otherwise loses all precision |
| `os_check18.py` | Tier 3: localisation radius `ε_N(2K−1)` vs. `μ(s)` (`μ/(2K−1) = 0.789…0.891`, `K = 2…12`); the modified-approximant commutator discrepancy `D` — **identically zero** for same-sign `k,k'`, and for opposite signs finite rank (`2`–`4` entries, `N`-independent) with `sup|D| → 4.000/15.00/5.500` but `h^σ→h⁰` rates **exactly `1.00, 2.00, 3.00`**; the half-shift mode identity exact to `10^{-15}` |
