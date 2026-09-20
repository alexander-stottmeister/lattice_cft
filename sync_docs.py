#!/usr/bin/env python3
"""Regenerate the item 8-14 sections of IMPROVEMENT-PLAN.md and CHANGES-v4-to-v5.md.

The prose is written with {{label}} placeholders which are substituted from
build/free_fermion_cft_v5.aux, so the numbering is correct by construction and stays
correct when new material shifts it.  Re-run after any compile:  python3 sync_docs.py
"""
import re
import sys
import pathlib

BASE = pathlib.Path(__file__).resolve().parent
AUX = BASE / 'build' / 'free_fermion_cft_v5.aux'

if not AUX.exists():
    sys.exit(f'missing {AUX}; compile the paper first')
NUM = dict(re.findall(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}', AUX.read_text(errors='replace')))


def sub(text):
    def one(m):
        lab = m.group(1)
        if lab not in NUM:
            sys.exit(f'unknown label {lab!r}')
        return NUM[lab]
    return re.sub(r'\{\{([^}]+)\}\}', one, text)


PLAN_8_10 = r"""### 8. Corollaries {{cor:KSconvbog}} / {{cor:KSderivationconv}} / {{cor:KSunitariesc}} / {{cor:KSconvbogc}} / {{cor:KSconvbogsmeared}} — make the Bogoliubov statements quantitative. **DONE**

All were "→ 0 uniformly on compact intervals", obtained from strong resolvent convergence, which
carries no rate. Replaced by **Duhamel + Grönwall** at two levels, since the corollaries split into
two genuinely different kinds:

- **One-particle** (Cor. {{cor:KSconvbog}} wavelet, {{cor:KSconvbogc}} momentum-cutoff,
  {{cor:KSconvbogsmeared}} smeared, and the derivations {{cor:KSderivationconv}}): the estimate
  ({{eq:KSmultiestimate}}) that carries these bounds `‖(e^{itõ⁽ᴺ⁾}−e^{ito})ξ‖` in the *one-particle*
  space, so no Fock-space input is needed. New **Lemma {{lem:duhamel1p}} (One-particle energy growth
  and Duhamel)**: (i) `‖e^{iτo}ξ‖_{h^σ} ≤ e^{c_{σ,k}|τ|}‖ξ‖_{h^σ}` with `c_{σ,k} ≤ C_L σ|k|⟨k⟩^{σ+2}`
  and **`c_{σ,0} = 0`**; (ii) `‖õ⁽ᴺ⁾−o‖_{h^σ→h⁰} ≤ ϰ_N` implies
  `‖(e^{itõ⁽ᴺ⁾}−e^{ito})ξ‖ ≤ ϰ_N λ_{σ,k}(t)‖ξ‖_{h^σ}`, `λ_{σ,k}(t) = (e^{c_{σ,k}|t|}−1)/c_{σ,k}`
  (`= |t|` for `k = 0`). Proof: `ℓ_{±,k}` is a *weighted shift* on the momentum lattice, so
  `[⟨·⟩^σ, o]` is again a shift, and the `1/⟨l⟩` from differentiating the weight is exactly what
  cancels the `⟨l⟩` growth of the shift weight. Grönwall with the mollified weight
  `⟨l⟩^σ(1+ρ⟨l⟩)^{-σ}`, then `ρ↓0` by monotone convergence. Inserted into ({{eq:KSmultiestimate}})
  this gives the explicit **({{eq:KSconvbograte}})**. **Remark {{rem:duhamel1psmeared}}** extends it
  to smeared generators, `c_{σ,Y} ≤ C_L σ Σ_k|Ŷ_k||k|⟨k⟩^{σ+2}` ({{eq:sobolevgrowthsmeared}}) —
  a condition on the *constant* only, not on the rate, and flagged as not sharp.
- **Fock space** (Cor. {{cor:KSunitariesc}}, the unitaries `e^{itdF_±(o)}`): here the energy bound of
  Lemma {{lem:energybound1k}} (item 1) is genuinely needed. New **Lemma {{lem:duhamel}} (Energy growth
  and Duhamel)** with `𝒩 = 1 + L_{±,0}`: `‖𝒩^p e^{iτT}Φ‖ ≤ e^{pc_k|τ|}‖𝒩^pΦ‖` from
  `[L_{±,0},L_{±,k}] = −(L/π)kL_{±,k}` plus the form bound ({{eq:energybound1k}}), giving
  **({{eq:KSunitariescrate}})**. The derivations need no `t`-dependence at all:
  **({{eq:KSconvbogderrate}})**.

The `t`-dependence is `λ ~ e^{c_k|t|}` for `k ≠ 0` and **exactly linear in `t` for `k = 0`** — so the
chiral time evolution, which is what the simulation budget uses, has no exponential factor at all.

*Verified numerically* (`numerics/os_check16.py`): the commutator ratio driving Grönwall is bounded by
`0.36` uniformly in the mollifier and in `(σ,k)`; the `k=0` Sobolev norm is conserved to `10^{-15}`;
the Duhamel bound (ii) holds with `≥ 4×` margin. The numerics also show `⟨k⟩^{σ+2}` is conservative
(the true constant behaves like `σ|k|⟨k⟩`), which is recorded in Remark {{rem:duhamel1psmeared}}.

### 9. Remark {{rem:KSconvsmeared}} (basic sequences) — upgrade "in principle" to a theorem. **DONE**

The three-term splitting in the remark needs two things the remark did not supply: an `N`-uniform
bound on `ℓ̃⁽ᴺ⁾_±(Y)` in terms of a seminorm of `Y`, and a genuine approximation statement for
`S^M_∞(X_M) → X`. Both are now there:

- **Wiener seminorms ({{eq:loopseminorms}})** `p_{N,m}(Y) = (1/2L_N)Σ_k⟨k⟩^m|Ŷ_k|` and
  **({{eq:loopseminormbound}})** `‖ℓ̃⁽ᴺ⁾_±(Y)‖_{h¹→h⁰} + ‖(ℓ̃⁽ᴺ⁾_±(Y))_{±∓}‖₂ ≤ C_L p_{N,3/2}(Y)`,
  uniformly in `N`. The exponent `3/2` is exactly what the off-diagonal Hilbert–Schmidt block needs
  (supported on the `O(|k|)` momenta between `0` and `±k`, each weighted by `≤|k|/2`), and it already
  dominates the `⟨k⟩` of the `h¹→h⁰` bound — so one seminorm serves all three statements of
  Lemma {{lem:KSconvsmeared}}.
- **New Lemma {{lem:loopjackson}} (Jackson estimate for the loop renormalization group)** +
  **({{eq:loopjackson}})**. **The mechanism is one exact identity**: orthonormality of `s` is
  `Σ_i|ŝ(ξ−2πi)|² = 1`, so the total aliasing mass is `δ(ξ) = 1 − |ŝ(ξ)|² = O(ξ^{2K})` by
  ({{eq:shatflat}}) — hence *every individual* aliasing coefficient is `≤ δ(ξ)^{1/2} = O(|ξ|^K)`.
  That is what defeats the `ε_M^{-1}` which the momentum weight `⟨k⟩` produces on the replicas;
  without it the estimate is **false** (the periodization `X̂_per` does not decay, so a sampling-type
  quasi-interpolant is *not* close to `X` in any norm with a derivative). A Hölder split against the
  pointwise decay `⟨i⟩^{-ρ}` then gives ({{eq:aliasingmass}})
  `Σ_{i≠0}⟨i⟩^m|ŝ(ξ−2πi)| ≤ C|ξ|^{Kβ}`, `β < 1−(m+1)/ρ`.
- **New Theorem {{thm:KSreconstruction}} (Reconstruction of the smeared Virasoro generators)**: under
  `lim_M limsup_N p_{N,3/2}(X_N − S^M_N(X_M)) = 0` the smeared KS approximants converge to `ℓ_±(X)` /
  `L_±(X)` for **every smooth `X`**, not only for `X` of the form `S^M_∞(X)`. **Threshold: `K ≥ 9`**
  for the limit, **`K ≥ 10`** for the `O(ε_M)` rate. *(`m = 2` would have forced `K ≥ 12`/`13`;
  `m = 3/2` is what makes the threshold coincide with the `K ≥ 9` the paper already needs for
  `δ = 2`.)*
- **New Remark {{rem:reconstructionrate}} (Two-scale rate)** + **({{eq:reconstructionrate}})**: the
  error splits into the price of the sequence, the generator error `ε_N^{min{δ,1}}` at the fine scale,
  and the smearing `ε_M` at the coarse scale; only the middle term improves under re-centring. Basic
  sequences are the case where the first term vanishes identically.

*Verified numerically* (`numerics/os_check17.py`): the identity `Σ_i|ŝ(ξ−2πi)|²=1` to `10^{-13}`;
`δ(ξ)` of order **exactly `2K`** (4.00, 8.00, 12.00, 16.00 for db2/4/6/8 — needs a numerically stable
`m₀`, see the changelog); the true order of ({{eq:aliasingmass}}) is **exactly `K`** (4, 6, 8, 10), so
the `Kβ` in the proof is conservative and the `K` thresholds are sufficient, not necessary; and the
Jackson rate ({{eq:loopjackson}}) is **1.00** in `ε_M` for `m = 0, 1, 2` and both db4 and db8.

### 10. Corollary {{cor:viraesa}} / ({{eq:analyticvector}}) — explicit analyticity radius. **DONE**

- **({{eq:analyticradius}})/({{eq:analyticradiusvalue}})**: summing the binomial series,
  `Γ(a+j)/(Γ(a)j!) = binom(a+j−1,j)` with `a = |m/k|+1/2`, gives
  `Σ_j (t^j/j!)‖ℓ^j_{±,k}e_m‖ ≤ √(2L)(1−|k|t)^{-a}`, so the radius is **`1/|k|` — uniform in `m`**
  (equivalently `π/(L|k|)` for the `L/π`-scaled generators that enter the second-quantized Virasoro
  generators). The same radius holds for `r_{±,k}`, `ι_{±,k}` because `(1/2)^j binom(2j,j)^{1/2} ≤ 1`.
  For `k = 0` the radius is only `1/|m|`, immaterial since `ℓ_{±,0}` is diagonal hence already
  self-adjoint.
- **({{eq:conformalerrorsharp}})**: the `binom(2j,j)^{1/2} ≤ 2^j` step is *not* the lossy one — it is
  sharp up to `(πj)^{-1/4}` and is exactly cancelled by the `(1/2)^j`. What is lossy is replacing
  `∏_{i<j}(|m|+|k|/2+i|k|)` by `(2(|m|+|k|/2))^j j!`, crude precisely when `|k| ≪ |m|`. Keeping the
  Gamma-quotient gives `‖(e^{itr̃}−e^{itr})e_m‖ ≤ t‖(r̃−r)e_m‖ + 4L[(1−|k|t)^{-a}−1−a|k|t]`, valid on
  the **whole** interval `t < 1/|k|` whereas ({{eq:conformalerror}}) is confined to `t < 1/(2|m|+|k|)`.

*Verified numerically* (`os_check17.py`): `max_j (1/2)^j binom(2j,j)^{1/2} = 1.000000`; the binomial
series identity to `10^{-15}`; the radius gain is `11×`–`101×` on the tested `(k,m)`; and the leading
coefficient ratio ({{eq:conformalerror}})/({{eq:conformalerrorsharp}}) `→ 7.87, 7.77`, i.e. the
predicted factor **8**.
"""

PLAN_TIER3 = r"""## Tier 3 — cheap, cosmetic, or bookkeeping  **ALL DONE (items 11–14)**

### 11. Proposition {{prop:antilocal}} — quantify the localisation. **DONE**

**New Remark {{rem:localisationradius}} (Localisation radius, and the trade-off against regularity)**
+ **({{eq:localisationradius}})**. Since `supp(_K s) = [0,2K−1]`:
(i) `R^N_∞` maps one lattice site into an interval of length `ε_N(2K−1)` lying entirely to its
**right**; (ii) hence `α^N_∞(A_{N,±}(J)) ⊂ A_{∞,±}(J⁺)` with `J⁺` the right-fattening by
`ε_N(2K−1)` — a **strict, one-sided light cone with no tail at all**, in contrast to the
momentum-cutoff group whose kernel is a Dirichlet kernel decaying only like `|x|^{-1}`;
(iii) Definition {{def:antiloc}} discards exactly the last `2K−1` sites of `I`, so
`ε_N#(Λ_N ∩ I) ≥ |I| − ε_N(2K−1)` and the construction becomes vacuous only below
`N ≈ log₂((2K−1)/|I|)`.

The observation worth having: the light-cone width `ε_N(2K−1)` and the re-centring offset `ε_Nμ(s)`
of Remark {{rem:recentring}} are the **same order** — numerically `μ(_K s)/(2K−1)` rises from `0.789`
at `K=2` to `0.891` at `K=12`, so the scaling function's mass sits in the right-hand tenth of its
support. Buying regularity by raising `K` widens the light cone *and* the re-centring shift
proportionally: **locality and regularity trade off linearly in `K`**, so the thresholds of
Remark {{rem:regularityvalues}} are simultaneously statements about how non-local the renormalization
group is allowed to be. (`numerics/os_check18.py`, check [28].)

### 12. §4.2.2 — the finite-`N` algebra for the **modified** approximants. **DONE**

v5 flagged that ({{eq:latviraCRchi}})/({{eq:latviraR}}) were computed for the *unmodified*
approximants and left the modified case open. **New Remark {{rem:modalgebra}}** settles it. At
one-particle level ({{eq:KSmod1p}}) the modified approximant is a **truncated** weighted shift where
the unmodified one wraps around `Γ_N`; composing two gives ({{eq:modcommutator}}), and the
discrepancy `D⁽ᴺ⁾_{k,k'}` is obtained by replacing the two inner multipliers by `χ_{Γ_N}(·)−1`.

- **Same-sign `k,k'` (and `k'=0`): `D⁽ᴺ⁾_{k,k'} = 0` identically** — both partial shifts lie between
  `l` and `l+k+k'`, so if the total shift stays in `Γ_N` so does each partial one. In particular the
  pair `(k,0)` governing the energy bound of Lemma {{lem:energybound1k}} is untouched, and
  ({{eq:latviraCRchi}})/({{eq:latviraR}}) hold **verbatim**.
- **Opposite signs**: `D⁽ᴺ⁾_{k,k'}` is supported on at most `|k|+|k'|` momenta within `|k|+|k'|` of
  the zone boundary — finite rank uniformly in `N`, but **not** small in operator norm
  (`‖D⁽ᴺ⁾‖ = O(1)`, since the symbol `ε_N^{-1}sin(ε_N(l+k/2))` is of order `|k|` at the boundary).
  What is small is ({{eq:modalgebrarate}}) `‖D⁽ᴺ⁾_{k,k'}‖_{h^σ→h⁰} ≤ C_{k,k'} ε_N^σ`, which for
  `σ > 2` is **smaller than the `O(ε_N²)` remainder it accompanies**.

So the modification is harmless on the domains where the convergence statements live, and
({{eq:modalgebrarate}}) is the quantitative form of "affects only momenta of order `π/ε_N`".
*Verified numerically* (`os_check18.py`, check [29]): `D ≡ 0` to machine zero for same-sign pairs;
for `(3,−1)`, `(5,−2)`, `(1,−4)` the support has `2`–`4` entries independent of `N`, `sup|D|` tends to
a nonzero constant (`4.000`, `15.00`, `5.500`), and the `h^σ→h⁰` rates are **exactly `1.00, 2.00,
3.00`** for `σ = 1, 2, 3`.

### 13. §4.2.5 (XY model) — the explicit half-shift identity. **DONE**

"Not directly comparable" is now **({{eq:halfshiftmodes}})**:
`H⁽ᴺ⁾_k = 2e^{−iε_Nk/4}(cos(¼ε_Nk) H̃⁽ᴺ⁾_k + i sin(¼ε_Nk) H̃⁽ᴺ⁾_{k+π/ε_{N+1}})`, derived from
({{eq:hdstag1c}}) by splitting ({{eq:hdfourier}}) over `Λ_N ∪̇ (Λ_N+ε_{N+1}) = Λ_{N+1}` and writing the
two-valued weight as a phase times `cos + i sin ×` the staggering sign. So the two-component mode at
`k` mixes the single-component mode at `k` with the **umklapp** mode at the zone-boundary momentum
`k + π/ε_{N+1}`, with amplitude `sin(¼ε_Nk) = O(ε_Nk)`: ({{eq:latvirastag}}) and
({{eq:latvirastag1c}}) agree to leading order and differ at **first** order by an umklapp
contribution. It also explains the `e^{∓iε_Nk/4}` prefactor of ({{eq:latvirastag}}) — it comes from
the half-shift, not from the Koo–Saleur combination, which contributes no further phase since
`H̃⁽ᴺ⁾_0` enters with `cos 0 = 1`. *(I first also claimed the identity explains the
`cos(¼ε_Nk)²` of the chiral symbols; it does not — it supplies only one such factor, so that claim
was dropped.)* Verified as an exact Fourier identity to `10^{-15}` (`os_check18.py`, check [30]).

### 14. Lemma {{lem:decay}} / Remark {{rem:regularityvalues}} — state both decay exponents. **DONE**

Remark {{rem:regularityvalues}} now carries a second table row with the **pointwise** exponent `ρ`
alongside the **`L²`** exponent `σ_K`, and says which is the right tool where:

| | 2 | 4 | 6 | 8 | 10 |
|---|---|---|---|---|---|
| `σ_K` | 1.000 | 1.776 | 2.390 | 2.917 | 3.406 |
| `ρ` | 1.336 | 1.910 | 2.431 | 2.927 | 3.409 |

- `ρ` (largest exponent with `|ŝ(l)| ≤ C(1+|l|)^{-ρ}`, bounded below by `K−𝒦` via ({{eq:decaysf}}))
  is for bounding **a single value** of `ŝ`: the uniform majorant Lemma {{lem:unifmaj}}, the
  Brillouin-zone/tail split ({{eq:convergencecor}}), the aliasing estimate ({{eq:aliasingmass}}).
- `σ_K` ({{eq:sobolevindex}}) is for **sums against a Sobolev weight**: every "`s` is `ρ`-regular"
  hypothesis.
- They are numerically close with `ρ` slightly larger, so the implication `σ_K ≥ ρ − ½` of
  Definition {{def:regularity}} gives away half a derivative that is not actually lost — a
  discrepancy that matters only at small `K`. Where a result needs both
  (Lemma {{lem:loopjackson}} is the clearest case) they enter through different factors and cannot be
  traded for one another.

Also fixed while doing this: three places added in items 8–10 cited the finite-product lemma
({{eq:convergence}}) for the **pointwise** decay of `ŝ`, which is ({{eq:decaysf}}) instead, and
called the measured exponent `K−𝒦₂` when Lemma {{lem:decay}} only guarantees `K−𝒦` with
`𝒦 = inf_j 𝒦_j`. All now reference `ρ` as defined in Remark {{rem:regularityvalues}}.
"""

CHANGES = r"""### §1k — reconstruction of the smeared Virasoro generators (Tier-2 item 9)

Remark {{rem:KSconvsmeared}} gave a three-term splitting and concluded that "in principle" one can
reach arbitrary smooth smearing functions. That is now a theorem:

- **({{eq:loopseminorms}})** Wiener seminorms `p_{N,m}`, **({{eq:loopseminormbound}})** the
  `N`-uniform bound `‖ℓ̃⁽ᴺ⁾_±(Y)‖_{h¹→h⁰} + ‖(ℓ̃⁽ᴺ⁾_±(Y))_{±∓}‖₂ ≤ C_L p_{N,3/2}(Y)`. The `3/2` is
  forced by the off-diagonal Hilbert–Schmidt block and simultaneously dominates the `h¹→h⁰` bound.
- **New Lemma {{lem:loopjackson}}** + **({{eq:loopjackson}})/({{eq:aliasingmass}})**: a Jackson
  estimate for the loop RG. The key input is that orthonormality of `s` reads `Σ_i|ŝ(ξ−2πi)|² = 1`,
  so the aliasing mass is `1−|ŝ(ξ)|² = O(ξ^{2K})` by ({{eq:shatflat}}) and *each* replica coefficient
  is `O(|ξ|^K)`. This is what kills the `ε_M^{-1}` from the momentum weight; the estimate is
  genuinely false without it.
- **New Theorem {{thm:KSreconstruction}}**: convergence to `L_±(X)` for every smooth `X`, from
  `K ≥ 9` (limit) and `K ≥ 10` (`O(ε_M)` rate).
- **New Remark {{rem:reconstructionrate}}** + **({{eq:reconstructionrate}})**: the two-scale rate
  `C_L p_{N,3/2}(X_N − S^M_N(X_M)) + C_{X,M,δ}ε_N^{min{δ,1}} + C_X ε_M`.

### §1l — explicit analyticity radius (Tier-2 item 10)

- **({{eq:analyticradius}})/({{eq:analyticradiusvalue}})**: the radius of the analytic-vector series
  is `1/|k|`, **uniform in `m`** (equivalently `π/(L|k|)` in the `L/π` normalisation of
  Remark {{rem:normalisation}}); the same for `r_{±,k}`, `ι_{±,k}` since
  `(1/2)^j binom(2j,j)^{1/2} ≤ 1`. For `k = 0` only `1/|m|`, which is immaterial.
- **({{eq:conformalerrorsharp}})**: the sharpened form of ({{eq:conformalerror}}), keeping the
  Gamma-quotient instead of bounding it by `(2(|m|+|k|/2))^j j!`. Valid on all of `t < 1/|k|` instead
  of `t < 1/(2|m|+|k|)`, leading coefficient smaller by a factor of 8. The remark now also states
  *which* step was lossy: not `binom(2j,j)^{1/2} ≤ 2^j` (sharp, and cancelled by `(1/2)^j`) but the
  handling of the Gamma-quotient when `|k| ≪ |m|`, the regime relevant for the conformal limit.

### §1m — quasi-local structure quantified (Tier-3 item 11)

**New Remark {{rem:localisationradius}}** + **({{eq:localisationradius}})**: `supp(_K s) = [0,2K−1]`
gives a **strict, one-sided light cone** of width `ε_N(2K−1)` for the wavelet RG, with no tail —
unlike the momentum-cutoff kernel, which decays only like `|x|^{-1}`. Definition {{def:antiloc}}
discards exactly `2K−1` sites per interval. Headline: the light-cone width and the re-centring offset
`ε_Nμ(s)` are the same order (`μ(_K s)/(2K−1) = 0.789 … 0.891` for `K = 2 … 12`), so **locality and
regularity trade off linearly in `K`**.

### §1n — the modified approximants' finite-scale algebra (Tier-3 item 12)

**New Remark {{rem:modalgebra}}** + **({{eq:modcommutator}})/({{eq:modalgebrarate}})**: the modified
one-particle approximant is a *truncated* weighted shift where the unmodified one wraps around `Γ_N`.
The discrepancy in the commutator **vanishes identically for same-sign `k,k'` and for `k'=0`** (both
partial shifts are trapped between `l` and `l+k+k'`), so ({{eq:latviraCRchi}})/({{eq:latviraR}}) hold
verbatim there — including the pair `(k,0)` used by Lemma {{lem:energybound1k}}. For opposite signs it
is finite rank and boundary-supported: `O(1)` in operator norm but
`‖·‖_{h^σ→h⁰} ≤ C ε_N^σ`, which beats the accompanying `O(ε_N²)` remainder once `σ > 2`.

### §1o — the XY half-shift identity (Tier-3 item 13)

**({{eq:halfshiftmodes}})**:
`H⁽ᴺ⁾_k = 2e^{−iε_Nk/4}(cos(¼ε_Nk) H̃⁽ᴺ⁾_k + i sin(¼ε_Nk) H̃⁽ᴺ⁾_{k+π/ε_{N+1}})`. The two-component
mode at `k` mixes the single-component mode at `k` with the **umklapp** mode at `k + π/ε_{N+1}`, with
amplitude `sin(¼ε_Nk) = O(ε_Nk)` — the precise sense in which ({{eq:latvirastag}}) and
({{eq:latvirastag1c}}) are not directly comparable. It also identifies the `e^{∓iε_Nk/4}` prefactor of
({{eq:latvirastag}}) as coming from the half-shift rather than from the Koo–Saleur combination.

### §1p — both decay exponents (Tier-3 item 14)

Remark {{rem:regularityvalues}} gains a second table row with the pointwise exponent `ρ` beside the
`L²` exponent `σ_K`, plus a statement of which is the right tool where: `ρ` for bounding a single
value of `ŝ` (Lemma {{lem:unifmaj}}, ({{eq:convergencecor}}), ({{eq:aliasingmass}})), `σ_K` for sums
against a Sobolev weight (every "`ρ`-regular" hypothesis). Corrected in passing: three citations added
in items 8–10 pointed at the finite-product lemma ({{eq:convergence}}) for the pointwise decay of `ŝ`,
which is ({{eq:decaysf}}), and named the measured exponent `K−𝒦₂` where Lemma {{lem:decay}} only
gives `K−𝒦`.
"""


def splice(path, start_marker, end_marker, body):
    f = BASE / path
    t = f.read_text()
    i, j = t.index(start_marker), t.index(end_marker)
    f.write_text(t[:i] + body.rstrip() + '\n\n' + t[j:])
    print(f'  {path}: spliced {len(body)} chars')


# --- macros for the standalone note, so its citations into the main file stay correct ---
MAINREFS = {
    'mrRGiso': 'eq:rgH', 'mrRGflow': 'eq:rgflow', 'mrSL': 'eq:sl',
    'mrChiral': 'eq:chiral1p', 'mrLatVac': 'eq:Fmassless', 'mrHardy': 'eq:masslesslimproj',
    'mrMomRG': 'eq:momrg1p', 'mrAlias': 'eq:shatflat', 'mrHS': 'eq:hilbertschmidt',
    'mrDefMomRG': 'def:momrg', 'mrDefWavRG': 'def:waveletrg', 'mrJackson': 'lem:loopjackson',
    'mrMoeb': 'rem:moeberror', 'mrThmC': 'thm:KSconvc', 'mrThmSm': 'thm:KSconvsmeared',
}
mr = BASE / 'mainrefs.tex'
lines = ['% AUTO-GENERATED by sync_docs.py from build/free_fermion_cft_v5.aux -- do not edit.',
         '% Numbers of the companion manuscript free_fermion_cft_v5.tex.']
for macro, lab in MAINREFS.items():
    if lab not in NUM:
        sys.exit(f'unknown label {lab!r}')
    lines.append(f'\\newcommand{{\\{macro}}}{{{NUM[lab]}}}')
mr.write_text('\n'.join(lines) + '\n')
print(f'  mainrefs.tex: {len(MAINREFS)} macros')

splice('IMPROVEMENT-PLAN.md', '### 8. Corollaries', '## Tier 3', sub(PLAN_8_10))
splice('IMPROVEMENT-PLAN.md', '## Tier 3', '---\n\n## Not immediate', sub(PLAN_TIER3))
splice('CHANGES-v4-to-v5.md', '### §1k', '---\n\n## Numerical verification', sub(CHANGES))
print('docs synced against build/free_fermion_cft_v5.aux')
