# Osborne–Stottmeister — what else can be improved right now

Numbering is **v5**, as compiled in `build/free_fermion_cft_v5.aux`; the v4-to-v5 correspondence
is tabulated in the "Numbering" note of `CHANGES-v4-to-v5.md`, to which "already done" refers.

## Tools now available

The v5 work produced six reusable techniques. Everything below is an application of one or
more of them, which is why these items are *immediate* rather than research problems.

| | technique | source |
|---|---|---|
| **T1** | alias weights are **probability** weights; convergence via Scheffé + dominated convergence against a fixed probability measure | Lemma 3.18, eq. (139) |
| **T2** | **uniform majorant** for `ŝ(2^{-J}l−h) P_J(l)`; the two decays interlock across the Brillouin zone | Lemma 3.14 |
| **T3** | `‖(R^N_∞)^*‖_{h^σ→h^σ} ≤ 1` for all `σ ≥ 0` ⟹ uniform-in-`N` bounds, hence **extension from cores to full Sobolev domains** | eqs. (209)–(210) |
| **T4** | **Jackson + Bernstein** for the MRA projection `P_N` ⟹ rates in the Sobolev scale; Brillouin-zone edge gives the matching lower bound | Remark 4.8 |
| **T5** | the `O(ε_N)` defect is the **centre-of-mass phase** `e^{iμ(s)ε_N k}`; re-centring buys one order | eq. (233), Remark 4.32 |
| **T6** | determinant/Hadamard telescoping ⟹ **`N`-uniform** monomial bounds for quasi-free states | eq. (134) |

---

## Tier 1 — ~~high value, provable with what is in hand~~ **ALL DONE (items 1–5)**

### 1. ~~The smeared energy bound, carried as a hypothesis → **Theorem**~~ — **DONE** (now Proposition 6.6, with proof)

Theorem 6.5 is unconditional. The proof went as sketched, with one improvement over the estimate
made here: the relative bound needs only `⟨k⟩^{1/2}`, not `⟨k⟩`, because

```
sup_n |n ∓ k/2| / (⟨n∓k⟩^{1/2} ⟨n⟩^{1/2})  ≤  C ⟨k⟩^{1/2}
```

(the quotient → 1 as |n| → ∞ and peaks at order |k|^{1/2} near n = 0). Summing against
`S^M_N(X̂)` with Corollary 3.10 — whose Brillouin-zone hypothesis holds precisely because `k`
ranges over `Γ_{N,+}` — then converges iff `ρ − 1/2 > 1`, i.e. under **1-regularity**, the
hypothesis already standing in Lemma 4.7. So no new regularity assumption was needed.

Ingredients, all now in the paper: `‖A^{-1/2}G^{(N)}A^{-1/2}‖ ≤ c_X` uniformly (267); real/imaginary
parts plus monotonicity of `dΓ` for the diagonal blocks (268); Lemma 4.23's *convergence* of the
HS norms giving `sup_N ‖G^{(N)}_{±∓}‖₂ < ∞` for the off-diagonal blocks (269); and
`dΓ(A) = N + L_{±,0}` with `N ≤ 2L_{±,0}` in NS, `N ≤ 2·1 + L_{±,0}` in Ramond (the zero mode
spans two dimensions of the doubled space, so Pauli caps its occupancy).

### 2. ~~Theorem 4.16's missing proof~~ — **DONE**, and item 3 came with it

The proof is three lines: (218) turns the statement into `dF_±(ℓ̃^{(N)}_{±,k} − ℓ_{±,k})`, and the
four terms of (224) are killed by the second and third assertions of Lemma 4.15. Also done:
the core extension to `D(dΓ(⟨·⟩^{1+δ}))` and the rate (228), and — since the domain extension
needs its uniform bound — **item 3** as well: Lemma 4.15 now carries a proof, the sharp rate
`‖ℓ̃^{(N)}_{±,k} − ℓ_{±,k}‖_{h^{1+δ}→h⁰} ≍ ε_N^{min{δ,2}}`, `‖(·)_{±∓}‖₂ ≤ √C_k ε_N²`, the
`h¹` domain extension, and the observation that no regularity is assumed anywhere. Measured
rates `0.00, 0.50, 1.00, 2.00, 2.00` at `δ = 0, ½, 1, 2, 3` (exactly `min{δ,2}`, with the value
at `δ = 0` exactly `1`), HS rate `2.00` for `k = 2,4,8` (`os_check12.py`).

**The analytic-vector claim turned out to be unprovable as asserted.** In `π_±` the pair terms
`a†G_{+−}a†`, `aG_{−+}a` raise the particle number, and iterating (25) with (205) produces a
factor `(j!)²` after `j` steps — the exponential series then diverges for every `t > 0`. (The
statement itself is presumably true, being the Goodman–Wallach/Carpi–Weiner analyticity of
finite-energy vectors, but it does not follow from Corollary 4.5 and (224) as claimed.) Replaced
by **Corollary 4.18**: Nelson's *commutator* theorem [Reed–Simon X.37] applied with
`N = 1 + L_{±,0}`, whose hypothesis (i) is the energy bound and whose hypothesis (ii) follows from
the Virasoro relation `[L_{±,0}, L_{±,k}] = −(L/π)k L_{±,k}` plus the *form* bound. This is
stronger than what was claimed: essential self-adjointness on **every** core for `1 + L_{±,0}`.

**Structural side-effect.** To avoid a §4 → §6 forward reference, the energy bound was split:
**Lemma 4.17** (fixed `k`, no regularity at all, proved where it is used) and **Proposition 6.6**
(smeared, the summation over `k` via Corollary 3.10, the single place where regularity enters).
Item 1 is thereby also tidier.

### 3. ~~Lemma 4.15 (momentum-cutoff)~~ — **DONE** as part of item 2 (see above).

<details><summary>original entry</summary>

#### Lemma 4.15 — the easy twin of Lemma 4.7, and **strictly better**.

Here `R^N_∞` is a sharp cutoff, so `ℓ̃^{(N)}_{±,k}` is an explicit Fourier multiplier (199) and the
sums in (201) are finite. Consequences, all one-liners:

- **no regularity hypothesis whatsoever** (no `ŝ` appears);
- an **exact** error formula, hence the sharp rate
  `‖ℓ̃^{(N)}_{±,k} − ℓ_{±,k}‖_{h^{1+δ}→h⁰} ≍ ε_N^{min{δ,2}}`;
- note the **exponent 2, not 1**: the sharp cutoff is symmetric, so there is no centre-of-mass
  defect (**T5**). This is precisely why (212) was already clean, and it is worth saying —
  it is an argument for the momentum-cutoff group that the paper does not currently make;
- domain extension `D_std → h¹` (**T3**).

*Effort ≈ ½ page. Confidence: high.*

</details>

### 4. ~~Theorem 5.2 (WZW currents)~~ — **DONE**, and it uncovered a gap

The upgrade landed, but not quite as forecast: `j^{(N)}_k` as defined in (254) is the **cyclic**
shift on `Γ_{N,−}`, and for the `|k|L/π` momenta at the upper Brillouin-zone edge the wrap-around
sends `+π/ε_N` to `−π/ε_N`, i.e. **across the Fermi point**. So `j̃^{(N)}_k` acquires off-diagonal
matrix elements of modulus one relative to the Hardy decomposition, and

```
‖(j̃^{(N)}_k − j_k)_{−+}‖₂ = (|k| L/π)^{1/2}   for all N,
```

which does **not** tend to 0. The third hypothesis of Lemma 4.23 therefore fails and the proof
pattern of Theorem 4.25 — which the paper invoked verbatim — is unavailable. Verified numerically:
constant `1.0, 1.7, 2.4` for `k = 1, 3, 6`, i.e. exactly `√(|k|L/π)`.

Fixed by carrying over the `χ_{Γ_N}` modification of §4.2.2, which §5 had not done. With it
(**Lemma 5.1**, new, proved):

- `j̄̃^{(N)}_k` and `j_k` agree **exactly** on `{n : n, n+k ∈ Γ_{N,−}}` — no bulk error at all;
- the off-diagonal blocks vanish **identically**, so there is no Schwinger-cocycle error at any
  finite scale: `c = 1` is reproduced exactly once `π/ε_N > 2|k|`, not merely in the limit
  (measured: exactly `0.0` for all `N`, `k`);
- `‖j̄̃^{(N)}_k − j_k‖_{h^δ→h⁰} ≍ ε_N^δ`, **uncapped** in `δ` (measured `0.00, 0.51, 1.02, 2.03,
  3.05` at `δ = 0, ½, 1, 2, 3`; exactly `1` at `δ = 0`), against `min{δ,2}` for the KS
  approximants — the only error being Brillouin-zone truncation;
- strong convergence on **all** of `h^{(+)}_{∞,−}`.

**Theorem 5.2** accordingly holds on `D(N)` with the number operator in place of the energy, needs
**no regularity of `s`** at all for the qualitative statement, and carries the rate (265). New
**Remark 5.3** collects the four ways the current is better behaved than the Virasoro generators.
Also fixed: (256) stated `j_k^* = j_k`; the correct adjoint is `j_{-k}`.

### 5. ~~Remark 4.34 (CFT simulation)~~ and ### 6. ~~Theorems 6.1/6.2~~ — **BOTH DONE**

Done together, since the budget is assembled from the explicit bound.

**Proposition 6.3** (item 6) makes Theorem 6.1 quantitative for the chiral time evolution:

```
|C^(N)_t − C_t|  ≤  (d_A+d_B) η_M(N)          [ground state]
                  + (1/6) d_B Θ_M |t| ε_N²    [dynamics]
```

Two features of the momentum-cutoff group make this work **without the intermediate scale `K`**
of the original proof (which would have cost a factor: optimising `2^{-2K} + 2^{-(N−K)}` gives
only `2^{-2N/3}`): the one-particle generator `ℓ^{(N)}_{±,0}` is a Fourier multiplier, so the
lattice dynamics moves no momenta at all, and `α^M_N` maps into `span{e_l}_{l∈Γ_M}`. The evolved
observable therefore stays supported on `|l| ≤ π/ε_M` for all times, and only the vacuum-symbol
deviation *there* enters.

**The key finding: the bottleneck is the ground state, and chirality squares it.**

```
η_M(N) = max_{l∈Γ_M} ‖S_0^(N)(l) − S(l)‖ = | sin(π 2^{-(N−M)}/4) |    on  A_{M,±}     — FIRST order
                                         = sin(π 2^{-(N−M)}/4)²      on  A^(±)_{M,±}  — SECOND order
```

verified to 7 digits (`os_check14.py`; measured orders `1.00` and `2.00`). The first-order term is
exactly the **chiral entanglement** (65) of the massless lattice vacuum — the off-diagonal block
`p_± P^{(+)}_{λ_N=0} p_∓` is `O(ε_N k)` while its continuum counterpart vanishes. On the full
two-component algebra it dominates the second-order dynamics term; restricted to a chiral
subalgebra — which is where the conformal structure lives — it is second order and matches.

**Remark 6.4** (item 5) is the budget. Both terms scale in `N − M`, not `N`
(`Θ_M ε_N² ≍ ε_M^{-3/2} 2^{-2(N−M)}`), and with `#qubits = #Λ_{N+1} ∝ 2^N`:

```
#qubits = O( 2^M √(d(1+T)/η) )          chiral observables, momentum-cutoff group
        = O( 2^M  d(1+T)/η  )          full 2-component algebra, or wavelet route un-recentred
```

with `2^M ≳ 2K−1` from the localisation constraint of Remark 4.34 and `K ≥ 5` from 2-regularity.
So **locality (the wavelet group) is paid for in qubits unless one re-centres** — the square root
is lost, a quadratic cost — which retrospectively justifies keeping re-centring available
(Remark 3.5). And by item 4, currents attain the square root under weaker hypotheses still.

## Tier 2 — worthwhile, moderate effort  **ALL DONE (items 6–10)**

### 6. Theorems 6.1 / 6.2 — explicit error bounds for dynamical correlation functions.

The proofs are complete but qualitative. Combining **T6** (the `N`-uniform monomial bound (134)),
Corollary 3.19's rate and the unitary bounds (211)/(213) gives a fully explicit bound, uniform on
compact time intervals. *Effort ≈ 1 page.*

### 7. ~~Lemma 4.23 / Theorem 4.25 (smeared)~~ — **DONE**

Done as planned (domain `D_std → h¹`, rate, explicit thresholds `σ_K > 3/2` and `> 5/2`,
i.e. `K ≥ 4` and `K ≥ 7`), plus one thing that was not planned.

Writing the two smeared operators with a common prefactor exhibits the **loop weights**
`w^(N)_k = ∏_{j≤N−M} m₀(ε_{M+j}k)` and `w^(∞)_k = ŝ(ε_M k)`, and the scaling relation gives them in
closed form relative to one another:

```
w^(N)_k − w^(∞)_k = w^(N)_k (1 − ŝ(ε_N k)),
```

so the smearing error is governed by the deviation of `ŝ` from 1 at the **fine** scale — and is
therefore first order, the centre-of-mass phase yet again. It is what limits (234) to
`ε_N^{min{δ,1}}`; the generator error is already `ε_N^{min{δ,2}}` since the fermions use the
momentum cutoff.

**Unplanned: the smearing error is a pure phase, and re-centring makes it cubic.** Orthonormality
gives `|m₀(ξ)|² + |m₀(ξ+π)|² = 1`, and `m₀` has an order-`K` zero at `π`, so
`|m₀(ξ)| = 1 + O(ξ^{2K})` and hence

```
|ŝ(ξ)| = ∏_{j≥1} |m₀(2^{-j}ξ)| = 1 + O(ξ^{2K}).
```

So `ŝ(ξ) = e^{iφ(ξ)}(1 + O(ξ^{2K}))` with `φ` real and **odd**, `φ(ξ) = −μ(s)ξ + O(ξ³)`. The whole
smearing error is a phase, and after re-centring it is **third** order, not merely second:
`1 − e^{iμ(s)ε_N k} ŝ(ε_N k) = O((ε_N k)³)` (measured rate `3.00` for db4 and db8 alike; the
flatness itself is measurable only for db2, where the order is `4.00 = 2K`, being below machine
precision for `K ≥ 4`).

**Consequence:** under re-centring the exponent in (234) improves to `min{δ,2}`, so the smeared
**wavelet route loses nothing against the momentum-cutoff one** — measured `0.95` at `δ=1` and
`1.86` at `δ=2`. Together with Remark 6.4(4) this closes the wavelet-vs-cutoff question: with
re-centring the two routes are equivalent in rate, and the wavelet group's real-space locality
comes for free. Recorded as **Remark 4.24**; Theorem 4.25 gains the core extension and (238).

### 8. Corollaries 4.10 / 4.14 / 4.20 / 4.21 / 4.31 — make the Bogoliubov statements quantitative. **DONE**

All were "→ 0 uniformly on compact intervals", obtained from strong resolvent convergence, which
carries no rate. Replaced by **Duhamel + Grönwall** at two levels, since the corollaries split into
two genuinely different kinds:

- **One-particle** (Cor. 4.10 wavelet, 4.21 momentum-cutoff,
  4.31 smeared, and the derivations 4.14): the estimate
  (224) that carries these bounds `‖(e^{itõ⁽ᴺ⁾}−e^{ito})ξ‖` in the *one-particle*
  space, so no Fock-space input is needed. New **Lemma 4.12 (One-particle energy growth
  and Duhamel)**: (i) `‖e^{iτo}ξ‖_{h^σ} ≤ e^{c_{σ,k}|τ|}‖ξ‖_{h^σ}` with `c_{σ,k} ≤ C_L σ|k|⟨k⟩^{σ+2}`
  and **`c_{σ,0} = 0`**; (ii) `‖õ⁽ᴺ⁾−o‖_{h^σ→h⁰} ≤ ϰ_N` implies
  `‖(e^{itõ⁽ᴺ⁾}−e^{ito})ξ‖ ≤ ϰ_N λ_{σ,k}(t)‖ξ‖_{h^σ}`, `λ_{σ,k}(t) = (e^{c_{σ,k}|t|}−1)/c_{σ,k}`
  (`= |t|` for `k = 0`). Proof: `ℓ_{±,k}` is a *weighted shift* on the momentum lattice, so
  `[⟨·⟩^σ, o]` is again a shift, and the `1/⟨l⟩` from differentiating the weight is exactly what
  cancels the `⟨l⟩` growth of the shift weight. Grönwall with the mollified weight
  `⟨l⟩^σ(1+ρ⟨l⟩)^{-σ}`, then `ρ↓0` by monotone convergence. Inserted into (224)
  this gives the explicit **(228)**. **Remark 4.13** extends it
  to smeared generators, `c_{σ,Y} ≤ C_L σ Σ_k|Ŷ_k||k|⟨k⟩^{σ+2}` (229) —
  a condition on the *constant* only, not on the rate, and flagged as not sharp.
- **Fock space** (Cor. 4.20, the unitaries `e^{itdF_±(o)}`): here the energy bound of
  Lemma 4.17 (item 1) is genuinely needed. New **Lemma 4.19 (Energy growth
  and Duhamel)** with `𝒩 = 1 + L_{±,0}`: `‖𝒩^p e^{iτT}Φ‖ ≤ e^{pc_k|τ|}‖𝒩^pΦ‖` from
  `[L_{±,0},L_{±,k}] = −(L/π)kL_{±,k}` plus the form bound (240), giving
  **(243)**. The derivations need no `t`-dependence at all:
  **(244)**.

The `t`-dependence is `λ ~ e^{c_k|t|}` for `k ≠ 0` and **exactly linear in `t` for `k = 0`** — so the
chiral time evolution, which is what the simulation budget uses, has no exponential factor at all.

*Verified numerically* (`numerics/os_check16.py`): the commutator ratio driving Grönwall is bounded by
`0.36` uniformly in the mollifier and in `(σ,k)`; the `k=0` Sobolev norm is conserved to `10^{-15}`;
the Duhamel bound (ii) holds with `≥ 4×` margin. The numerics also show `⟨k⟩^{σ+2}` is conservative
(the true constant behaves like `σ|k|⟨k⟩`), which is recorded in Remark 4.13.

### 9. Remark 4.27 (basic sequences) — upgrade "in principle" to a theorem. **DONE**

The three-term splitting in the remark needs two things the remark did not supply: an `N`-uniform
bound on `ℓ̃⁽ᴺ⁾_±(Y)` in terms of a seminorm of `Y`, and a genuine approximation statement for
`S^M_∞(X_M) → X`. Both are now there:

- **Wiener seminorms (252)** `p_{N,m}(Y) = (1/2L_N)Σ_k⟨k⟩^m|Ŷ_k|` and
  **(253)** `‖ℓ̃⁽ᴺ⁾_±(Y)‖_{h¹→h⁰} + ‖(ℓ̃⁽ᴺ⁾_±(Y))_{±∓}‖₂ ≤ C_L p_{N,3/2}(Y)`,
  uniformly in `N`. The exponent `3/2` is exactly what the off-diagonal Hilbert–Schmidt block needs
  (supported on the `O(|k|)` momenta between `0` and `±k`, each weighted by `≤|k|/2`), and it already
  dominates the `⟨k⟩` of the `h¹→h⁰` bound — so one seminorm serves all three statements of
  Lemma 4.23.
- **New Lemma 4.28 (Jackson estimate for the loop renormalization group)** +
  **(254)**. **The mechanism is one exact identity**: orthonormality of `s` is
  `Σ_i|ŝ(ξ−2πi)|² = 1`, so the total aliasing mass is `δ(ξ) = 1 − |ŝ(ξ)|² = O(ξ^{2K})` by
  (249) — hence *every individual* aliasing coefficient is `≤ δ(ξ)^{1/2} = O(|ξ|^K)`.
  That is what defeats the `ε_M^{-1}` which the momentum weight `⟨k⟩` produces on the replicas;
  without it the estimate is **false** (the periodization `X̂_per` does not decay, so a sampling-type
  quasi-interpolant is *not* close to `X` in any norm with a derivative). A Hölder split against the
  pointwise decay `⟨i⟩^{-ρ}` then gives (255)
  `Σ_{i≠0}⟨i⟩^m|ŝ(ξ−2πi)| ≤ C|ξ|^{Kβ}`, `β < 1−(m+1)/ρ`.
- **New Theorem 4.29 (Reconstruction of the smeared Virasoro generators)**: under
  `lim_M limsup_N p_{N,3/2}(X_N − S^M_N(X_M)) = 0` the smeared KS approximants converge to `ℓ_±(X)` /
  `L_±(X)` for **every smooth `X`**, not only for `X` of the form `S^M_∞(X)`. **Threshold: `K ≥ 9`**
  for the limit, **`K ≥ 10`** for the `O(ε_M)` rate. *(`m = 2` would have forced `K ≥ 12`/`13`;
  `m = 3/2` is what makes the threshold coincide with the `K ≥ 9` the paper already needs for
  `δ = 2`.)*
- **New Remark 4.30 (Two-scale rate)** + **(258)**: the
  error splits into the price of the sequence, the generator error `ε_N^{min{δ,1}}` at the fine scale,
  and the smearing `ε_M` at the coarse scale; only the middle term improves under re-centring. Basic
  sequences are the case where the first term vanishes identically.

*Verified numerically* (`numerics/os_check17.py`): the identity `Σ_i|ŝ(ξ−2πi)|²=1` to `10^{-13}`;
`δ(ξ)` of order **exactly `2K`** (4.00, 8.00, 12.00, 16.00 for db2/4/6/8 — needs a numerically stable
`m₀`, see the changelog); the true order of (255) is **exactly `K`** (4, 6, 8, 10), so
the `Kβ` in the proof is conservative and the `K` thresholds are sufficient, not necessary; and the
Jackson rate (254) is **1.00** in `ε_M` for `m = 0, 1, 2` and both db4 and db8.

### 10. Corollary 4.5 / (208) — explicit analyticity radius. **DONE**

- **(209)/(210)**: summing the binomial series,
  `Γ(a+j)/(Γ(a)j!) = binom(a+j−1,j)` with `a = |m/k|+1/2`, gives
  `Σ_j (t^j/j!)‖ℓ^j_{±,k}e_m‖ ≤ √(2L)(1−|k|t)^{-a}`, so the radius is **`1/|k|` — uniform in `m`**
  (equivalently `π/(L|k|)` for the `L/π`-scaled generators that enter the second-quantized Virasoro
  generators). The same radius holds for `r_{±,k}`, `ι_{±,k}` because `(1/2)^j binom(2j,j)^{1/2} ≤ 1`.
  For `k = 0` the radius is only `1/|m|`, immaterial since `ℓ_{±,0}` is diagonal hence already
  self-adjoint.
- **(273)**: the `binom(2j,j)^{1/2} ≤ 2^j` step is *not* the lossy one — it is
  sharp up to `(πj)^{-1/4}` and is exactly cancelled by the `(1/2)^j`. What is lossy is replacing
  `∏_{i<j}(|m|+|k|/2+i|k|)` by `(2(|m|+|k|/2))^j j!`, crude precisely when `|k| ≪ |m|`. Keeping the
  Gamma-quotient gives `‖(e^{itr̃}−e^{itr})e_m‖ ≤ t‖(r̃−r)e_m‖ + 4L[(1−|k|t)^{-a}−1−a|k|t]`, valid on
  the **whole** interval `t < 1/|k|` whereas (272) is confined to `t < 1/(2|m|+|k|)`.

*Verified numerically* (`os_check17.py`): `max_j (1/2)^j binom(2j,j)^{1/2} = 1.000000`; the binomial
series identity to `10^{-15}`; the radius gain is `11×`–`101×` on the tested `(k,m)`; and the leading
coefficient ratio (272)/(273) `→ 7.87, 7.77`, i.e. the
predicted factor **8**.

## Tier 3 — cheap, cosmetic, or bookkeeping  **ALL DONE (items 11–14)**

### 11. Proposition 3.7 — quantify the localisation. **DONE**

**New Remark 3.8 (Localisation radius, and the trade-off against regularity)**
+ **(108)**. Since `supp(_K s) = [0,2K−1]`:
(i) `R^N_∞` maps one lattice site into an interval of length `ε_N(2K−1)` lying entirely to its
**right**; (ii) hence `α^N_∞(A_{N,±}(J)) ⊂ A_{∞,±}(J⁺)` with `J⁺` the right-fattening by
`ε_N(2K−1)` — a **strict, one-sided light cone with no tail at all**, in contrast to the
momentum-cutoff group whose kernel is a Dirichlet kernel decaying only like `|x|^{-1}`;
(iii) Definition 3.6 discards exactly the last `2K−1` sites of `I`, so
`ε_N#(Λ_N ∩ I) ≥ |I| − ε_N(2K−1)` and the construction becomes vacuous only below
`N ≈ log₂((2K−1)/|I|)`.

The observation worth having: the light-cone width `ε_N(2K−1)` and the re-centring offset `ε_Nμ(s)`
of Remark 3.5 are the **same order** — numerically `μ(_K s)/(2K−1)` rises from `0.789`
at `K=2` to `0.891` at `K=12`, so the scaling function's mass sits in the right-hand tenth of its
support. Buying regularity by raising `K` widens the light cone *and* the re-centring shift
proportionally: **locality and regularity trade off linearly in `K`**, so the thresholds of
Remark 3.13 are simultaneously statements about how non-local the renormalization
group is allowed to be. (`numerics/os_check18.py`, check [28].)

### 12. §4.2.2 — the finite-`N` algebra for the **modified** approximants. **DONE**

v5 flagged that (164)/(165) were computed for the *unmodified*
approximants and left the modified case open. **New Remark 4.2** settles it. At
one-particle level (178) the modified approximant is a **truncated** weighted shift where
the unmodified one wraps around `Γ_N`; composing two gives (181), and the
discrepancy `D⁽ᴺ⁾_{k,k'}` is obtained by replacing the two inner multipliers by `χ_{Γ_N}(·)−1`.

- **Same-sign `k,k'` (and `k'=0`): `D⁽ᴺ⁾_{k,k'} = 0` identically** — both partial shifts lie between
  `l` and `l+k+k'`, so if the total shift stays in `Γ_N` so does each partial one. In particular the
  pair `(k,0)` governing the energy bound of Lemma 4.17 is untouched, and
  (164)/(165) hold **verbatim**.
- **Opposite signs**: `D⁽ᴺ⁾_{k,k'}` is supported on at most `|k|+|k'|` momenta within `|k|+|k'|` of
  the zone boundary — finite rank uniformly in `N`, but **not** small in operator norm
  (`‖D⁽ᴺ⁾‖ = O(1)`, since the symbol `ε_N^{-1}sin(ε_N(l+k/2))` is of order `|k|` at the boundary).
  What is small is (182) `‖D⁽ᴺ⁾_{k,k'}‖_{h^σ→h⁰} ≤ C_{k,k'} ε_N^σ`, which for
  `σ > 2` is **smaller than the `O(ε_N²)` remainder it accompanies**.

So the modification is harmless on the domains where the convergence statements live, and
(182) is the quantitative form of "affects only momenta of order `π/ε_N`".
*Verified numerically* (`os_check18.py`, check [29]): `D ≡ 0` to machine zero for same-sign pairs;
for `(3,−1)`, `(5,−2)`, `(1,−4)` the support has `2`–`4` entries independent of `N`, `sup|D|` tends to
a nonzero constant (`4.000`, `15.00`, `5.500`), and the `h^σ→h⁰` rates are **exactly `1.00, 2.00,
3.00`** for `σ = 1, 2, 3`.

### 13. §4.2.5 (XY model) — the explicit half-shift identity. **DONE**

"Not directly comparable" is now **(277)**:
`H⁽ᴺ⁾_k = 2e^{−iε_Nk/4}(cos(¼ε_Nk) H̃⁽ᴺ⁾_k + i sin(¼ε_Nk) H̃⁽ᴺ⁾_{k+π/ε_{N+1}})`, derived from
(276) by splitting (150) over `Λ_N ∪̇ (Λ_N+ε_{N+1}) = Λ_{N+1}` and writing the
two-valued weight as a phase times `cos + i sin ×` the staggering sign. So the two-component mode at
`k` mixes the single-component mode at `k` with the **umklapp** mode at the zone-boundary momentum
`k + π/ε_{N+1}`, with amplitude `sin(¼ε_Nk) = O(ε_Nk)`: (274) and
(275) agree to leading order and differ at **first** order by an umklapp
contribution. It also explains the `e^{∓iε_Nk/4}` prefactor of (274) — it comes from
the half-shift, not from the Koo–Saleur combination, which contributes no further phase since
`H̃⁽ᴺ⁾_0` enters with `cos 0 = 1`. *(I first also claimed the identity explains the
`cos(¼ε_Nk)²` of the chiral symbols; it does not — it supplies only one such factor, so that claim
was dropped.)* Verified as an exact Fourier identity to `10^{-15}` (`os_check18.py`, check [30]).

### 14. Lemma 3.11 / Remark 3.13 — state both decay exponents. **DONE**

Remark 3.13 now carries a second table row with the **pointwise** exponent `ρ`
alongside the **`L²`** exponent `σ_K`, and says which is the right tool where:

| | 2 | 4 | 6 | 8 | 10 |
|---|---|---|---|---|---|
| `σ_K` | 1.000 | 1.776 | 2.390 | 2.917 | 3.406 |
| `ρ` | 1.336 | 1.910 | 2.431 | 2.927 | 3.409 |

- `ρ` (largest exponent with `|ŝ(l)| ≤ C(1+|l|)^{-ρ}`, bounded below by `K−𝒦` via (113))
  is for bounding **a single value** of `ŝ`: the uniform majorant Lemma 3.14, the
  Brillouin-zone/tail split (111), the aliasing estimate (255).
- `σ_K` (114) is for **sums against a Sobolev weight**: every "`s` is `ρ`-regular"
  hypothesis.
- They are numerically close with `ρ` slightly larger, so the implication `σ_K ≥ ρ − ½` of
  Definition 3.12 gives away half a derivative that is not actually lost — a
  discrepancy that matters only at small `K`. Where a result needs both
  (Lemma 4.28 is the clearest case) they enter through different factors and cannot be
  traded for one another.

Also fixed while doing this: three places added in items 8–10 cited the finite-product lemma
(110) for the **pointwise** decay of `ŝ`, which is (113) instead, and
called the measured exponent `K−𝒦₂` when Lemma 3.11 only guarantees `K−𝒦` with
`𝒦 = inf_j 𝒦_j`. All now reference `ρ` as defined in Remark 3.13.

---

## Not immediate (recorded so the list is honest)

- `c < 1` minimal models via the coset construction; anyonic chains and Jones–Wenzl refining maps;
  symplectic fermions at `c = −2`. All flagged as future work by the authors, correctly.
- Odd observables and conformal covariance in the Ising case — deferred to a separate paper.
- ~~Turning the Zini–Wang comparison (§1.2) into a theorem.~~ **DONE**, in the separate note
  `zini-wang-comparison.{tex,pdf}` (9 pp), which cites the manuscript through the auto-generated
  `mainrefs.tex`. Headline: the criterion for the Zini–Wang connecting unitaries is constancy of the
  **GNS multiplicity** `m(S) = #{eigenvalues of the symbol in (0,1)}`, not purity — so the
  manuscript's inference from "not pure" to "structure unavailable" does not go through. What is
  true is sharper: on the chiral algebra `m` is constant at every finite `M` and **collapses only at
  `M = ∞`**, and only for the momentum-cutoff route; the wavelet route keeps `m = |Γ_{N,−}|` all the
  way to the limit. The mechanism the manuscript names is vindicated and quantified,
  `‖[P(k),p_∓]‖ = ½|sin(½ε_N k)|`, and the resulting mixing is **extensive with entropy density
  exactly `2 ln 2 − 1`**. Numerics in `numerics/os_check19.py`; open points listed in §8 of the note.
- ~~One design question: should the centre-of-mass shift be built into Definition 3.2?~~
  **Decided (and implemented): no.** It is carried along as an alternative *comparison
  convention* in the new **Remark 3.5**, invoked only where rates are stated. Two reasons, both
  now recorded in the paper: (i) the re-centred maps `T_{−a_N}R^N_∞`, `a_N = ε_N μ(s)`, violate
  asymptotic compatibility (Proposition 3.3(4)) because `a_{N+1} = a_N/2`, so they do not define
  an inductive system and the whole construction of Section 3 would have to be redone;
  (ii) one cannot re-centre the scaling function instead — `s(·+μ(s))` is orthonormal but obeys a
  scaling equation with non-integer shifts `n − μ(s)`, hence is not the scaling function of a
  dyadic MRA. Remark 3.5 also records that the momentum-cutoff group needs no such convention at
  all, since no scaling function enters its symbol — reinforcing Tier-1 item 3.

---

## Status

**All 14 items are done** (Tier 1: 1–5; Tier 2: 6–10; Tier 3: 11–14). What remains is the
"Not immediate" list above, which is genuinely future work rather than proof debt.

`free_fermion_cft_v5.tex` compiles clean (0 errors, 0 undefined references or citations, no
multiply-defined labels); `diff_v4_v5.pdf` is the latexdiff against the untouched author source.
Numerical support is `numerics/os_check.py … os_check19.py`, pure numpy.

Run `python3 sync_docs.py` after any recompile: the item 8–14 sections of this file and of
`CHANGES-v4-to-v5.md` are generated from `{{label}}` placeholders substituted out of
`build/free_fermion_cft_v5.aux`, so the theorem and equation numbers stay correct when new
material shifts them.
