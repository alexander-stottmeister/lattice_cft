# Notation and conventions

Symbols first, then the three conventions that are easy to get wrong and that cost time when
they are got wrong.

## Symbols

| symbol | meaning |
|---|---|
| `L` | the circumference of the spatial circle. Throughout the numerics `L = π`, which makes `π/L = 1` |
| `ε_N` | the lattice spacing at scale `N`, equal to `2^{-N} L`. Larger `N` is a finer lattice |
| `Λ_N` | the lattice at scale `N`; `#Λ_{N+1}` is the qubit count in the simulation budget |
| `Γ_{N,±}` | the momentum lattice, `+` Ramond and `−` Neveu–Schwarz. With `L = π` these are `ℤ` and `ℤ + 1/2` |
| `K` | the Daubechies order. The filter has `2K` taps and the scaling function support `[0, 2K−1]` |
| `h_n` | the low-pass filter taps, normalised so that their sum is `√2` |
| `m₀(ξ)` | the low-pass symbol, `2^{-1/2} Σ_n h_n e^{-inξ}` |
| `ŝ(ξ)` | the transform of the scaling function, the infinite product `∏_{j≥1} m₀(2^{-j}ξ)` |
| `μ(s)` | the centre of mass `∫ x s(x) dx`, equal to `2^{-1/2} Σ_n n h_n` |
| `σ_K` | the Sobolev exponent of the scaling function |
| `ρ` | the pointwise decay exponent of `ŝ` |
| `R^N_∞`, `α^N_∞` | the renormalization maps on the one-particle space and on the algebra |
| `ℓ_{±,k}`, `L_{±,k}` | the one-particle and second-quantised Virasoro generators, `±` for the two chiralities |
| `δ` | the Sobolev index in which rates are stated; the advertised rate is at `δ = 2` |
| `m(S)` | the number of eigenvalues of a symbol lying strictly between 0 and 1 |

## Three conventions worth stating

**Which reflection of the filter.** The spectral factorisation used by `tools/dbfilters.py`
and by `numerics/os_check4.py` produces the *mirror image* of the filter table hard-coded in
`numerics/os_check.py`. Reversing a real filter replaces `m₀(ξ)` by `e^{-i(2K−1)ξ} conj(m₀(ξ))`,
so `|m₀|` and hence `|ŝ|` are untouched: the zeros, the Sobolev exponents and every aliasing
quantity are the same either way. What does change is the centre of mass, which becomes
`(2K−1) − μ(s)`, and the centre of mass is exactly what the re-centring results turn on. The
manuscript's convention is the constructed one: it gives `μ = 5.99` at `K = 4` and `16.87` at
`K = 10`, the values Remark 3.5 quotes. The self-test in `tools/dbfilters.py` pins this.

**Two regularity exponents, not one.** `σ_K` controls sums of `ŝ` against a Sobolev weight;
`ρ` controls a single value of `ŝ`. They are close, with `ρ` slightly the larger, and they are
not interchangeable: Lemma 4.28 needs both, entering through different factors. Every
"`ρ`-regular" hypothesis in the revision means `σ_K > ρ`, a strict inequality, which is why
`5/2`-regularity needs `K ≥ 7` and not the `K ≥ 6` printed in Theorem 4.25.

**Which version's numbering.** The revision, the audit and the two Markdown records do not
share a numbering. The audit uses the **published** numbers. The records use the revision's,
with a correspondence table in `CHANGES-v4-to-v5.md`. `results.md` in this folder is generated
from the compiled revision, so it is the one place where the numbers cannot drift.
