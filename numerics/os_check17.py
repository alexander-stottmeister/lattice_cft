"""
Part 17: the two Tier-2 items 9 and 10.

ITEM 9 -- Lemma 4.27 (Jackson estimate for the loop renormalization group) and Theorem 4.28.
  The proof rests on the exact identity (orthonormality of s):
       delta(xi) := sum_{i != 0} |shat(xi - 2 pi i)|^2 = 1 - |shat(xi)|^2 = O(xi^{2K}),
  so that EVERY single aliasing coefficient is O(|xi|^K).  That is what kills the 1/eps_M
  produced by the momentum weight <k> in  p_{infty,m}.  Checks:
    [22] the identity, and the order 2K of  1 - |shat|^2.
    [23] the claimed bound (252)   sum_{i!=0} <i>^m |shat(xi - 2 pi i)| <= C |xi|^{K beta}:
         measure the true power law in xi (should be ~ K, i.e. the proof's K*beta is
         conservative but valid).
    [24] the Jackson estimate (251) itself:  p_{infty,m}(S^M_infty(X_M) - X) ~ eps_M,
         first order, with the coefficient governed by mu(s) (centre of mass).  Also check
         that re-centring (multiplying by e^{i mu(s) eps_M k}) does NOT help here -- the
         aliasing term is what it is -- but that the *smearing* part of the error is the
         first-order piece, as claimed.

ITEM 10 -- explicit analyticity radius (206)/(207) and the sharpened bound (270).
    [25] (1/2)^j binom(2j,j)^{1/2} <= 1, and the binomial series identity
         sum_j binom(a+j-1,j) x^j = (1-x)^{-a}.
    [26] the two error bounds (269) vs (270): radius 1/|k| (m-independent) vs 1/(2|m|+|k|),
         and the factor 8 in the leading coefficient.

Pure numpy.
"""
import numpy as np
import sys

sys.path.insert(0, '.')
from os_check4 import daubechies, m0 as m0f, sobolev_exponent, sup_exponent

PI = np.pi


def deflate(h, K):
    """P(z) = sum_n h_n z^n has a zero of order K at z = -1; return the quotient Q."""
    q = list(map(float, h))
    for _ in range(K):
        # synthetic division of q(z) by (1+z), highest coefficient first
        r = list(reversed(q))
        out = [r[0]]
        for c in r[1:]:
            out.append(c - out[-1])
        rem = out.pop()
        assert abs(rem) < 1e-8 * max(1.0, max(map(abs, q))), f"non-zero remainder {rem:.2e}"
        q = list(reversed(out))
    return np.array(q)


def make_shat(h):
    """Numerically stable |m0| and shat.

    m0(xi) = (1+e^{-i xi})^K Q(e^{-i xi})/sqrt(2) = (2cos(xi/2))^K e^{-iK xi/2} Q(...)/sqrt(2),
    so the order-K zero at xi = pi is carried by cos(xi/2)^K in closed form instead of by
    catastrophic cancellation in the coefficient sum.  This matters because we evaluate
    |shat(xi - 2 pi i)| ~ |xi|^K down to |xi| ~ 1e-3 with K up to 10.
    """
    K = len(h) // 2
    Q = deflate(h, K)
    nq = np.arange(len(Q))

    def m0(x):
        x = np.asarray(x, float)
        z = np.exp(-1j * np.multiply.outer(x, nq)) @ Q
        return (2.0 * np.cos(x / 2.0)) ** K * np.exp(-0.5j * K * x) * z / np.sqrt(2.0)

    def shat(x):
        x = np.asarray(x, float)
        J = int(np.ceil(np.log2(max(np.max(np.abs(x)), 1.0)))) + 34
        o = np.ones(x.shape, complex)
        for j in range(1, J + 1):
            o = o * m0(x * 2.0 ** (-j))
        return o
    return shat


def mu_of_s(h):
    """First moment mu(s) = (1/sqrt2) sum_n n h_n."""
    n = np.arange(len(h))
    return float(np.sum(n * h) / np.sqrt(2.0))


# ----------------------------------------------------------------------------------
print("=" * 98)
print("[22] orthonormality identity   sum_i |shat(xi-2pi i)|^2 = 1   and   1-|shat(xi)|^2 = O(xi^{2K})")
print("=" * 98)
for K in (2, 4, 6, 8):
    h = daubechies(K)
    shat = make_shat(h)
    IMAX = 4000
    ii = np.arange(-IMAX, IMAX + 1)
    inz = ii[ii != 0]
    # identity at a few generic xi
    dev = 0.0
    for xi in (0.3, 1.0, 2.5, -1.7):
        tot = np.sum(np.abs(shat(xi - 2 * PI * ii)) ** 2)
        dev = max(dev, abs(tot - 1.0))
    # order of delta(xi) = sum_{i!=0}|shat(xi-2pi i)|^2, computed DIRECTLY (all terms
    # positive, so no cancellation) rather than as 1 - |shat(xi)|^2 which underflows
    xs = np.array([2.0 ** (-t) for t in range(2, 8)])
    vals = np.array([np.sum(np.abs(shat(x - 2 * PI * inz)) ** 2) for x in xs])
    rates = [np.log2(vals[i] / vals[i + 1]) for i in range(len(vals) - 1)]
    # cross-check the identity delta = 1 - |shat|^2 where double precision still resolves it
    xi0 = 1.0
    lhs = np.sum(np.abs(shat(xi0 - 2 * PI * inz)) ** 2)
    rhs = 1.0 - abs(shat(np.array([xi0]))[0]) ** 2
    print(f"  db{K}: |sum_i |shat|^2 - 1| = {dev:.2e}   "
          f"delta(1) direct={lhs:.6e} vs 1-|shat(1)|^2={rhs:.6e} (rel {abs(lhs/rhs-1):.1e})   "
          f"order of delta = {np.mean(rates[-3:]):.2f}  (predicted 2K = {2*K})")

# ----------------------------------------------------------------------------------
print()
print("=" * 98)
print("[23] bound (252):  sum_{i!=0} <i>^m |shat(xi-2pi i)| <= C |xi|^{K beta}")
print("     reported: measured power law in xi (the proof gives K*beta, beta<1-(m+1)/rho)")
print("=" * 98)
for K in (4, 6, 8, 10):
    h = daubechies(K)
    shat = make_shat(h)
    rho = sup_exponent(h)                 # K - Kbar_2, the POINTWISE decay exponent of (109)
    IMAX = 3000
    ii = np.arange(-IMAX, IMAX + 1)
    ii = ii[ii != 0]
    br = np.sqrt(1.0 + ii ** 2)
    for m in (0.0, 2.0):
        if rho <= m + 1:
            print(f"  db{K} m={m:g}: rho={rho:.2f} <= m+1, lemma not applicable")
            continue
        beta_max = 1.0 - (m + 1) / rho
        xs = np.array([2.0 ** (-t) for t in range(2, 9)])
        vals = np.array([np.sum(br ** m * np.abs(shat(x - 2 * PI * ii))) for x in xs])
        rates = [np.log2(vals[i] / vals[i + 1]) for i in range(len(vals) - 1)]
        meas = np.mean(rates[-3:])
        print(f"  db{K} m={m:g}: rho={rho:.2f}  beta<{beta_max:.3f}  =>  proof gives "
              f"exponent < K*beta = {K*beta_max:.2f};  measured {meas:.2f}  "
              f"(true order is K = {K})   valid={meas >= K*beta_max - 0.1}")

# ----------------------------------------------------------------------------------
print()
print("=" * 98)
print("[24] Jackson estimate (251):   p_{infty,m}(S^M_infty(X_M) - X)   vs   eps_M")
print("     X smooth on the circle; samples on 2^M points; S^M_infty coefficients =")
print("     shat(eps_M k) * (aliased transform).  Predicted: first order in eps_M.")
print("=" * 98)
# X(x) = sum_n c_n e^{i n x}, analytic: c_n = exp(-|n|)
NMAXC = 60
nn = np.arange(-NMAXC, NMAXC + 1)
cn = np.exp(-np.abs(nn).astype(float))
cn = cn / np.abs(cn).sum()


def cof(k):
    """Fourier coefficient c_k of X (0 outside the band)."""
    k = np.asarray(k)
    out = np.zeros(k.shape, float)
    sel = np.abs(k) <= NMAXC
    out[sel] = cn[(k[sel] + NMAXC).astype(int)]
    return out


for K in (4, 8):
    h = daubechies(K)
    shat = make_shat(h)
    print(f"  db{K} (mu(s) = {mu_of_s(h):.3f}):")
    for m in (0.0, 1.0, 2.0):
        row = []
        for M in range(4, 11):
            J = 2 ** M                      # lattice sites; eps_M <-> 2 pi / J
            KMAX = 40 * J
            k = np.arange(-KMAX, KMAX + 1)
            # aliased (Riemann-normalised) transform of the samples: sum_i c_{k+iJ}
            alias = np.zeros(k.shape, float)
            for i in range(-(NMAXC // J + 2), NMAXC // J + 3):
                alias = alias + cof(k + i * J)
            diff = shat(2 * PI * k / J) * alias - cof(k)
            row.append(float(np.sum((1.0 + k.astype(float) ** 2) ** (m / 2) * np.abs(diff))))
        rates = [np.log2(row[i] / row[i + 1]) for i in range(len(row) - 1)]
        print(f"    m={m:g}: " + " ".join(f"{v:.2e}" for v in row))
        print(f"          rate in eps_M: " + "  ".join(f"{v:5.2f}" for v in rates)
              + "   (predicted 1.00)")

# ----------------------------------------------------------------------------------
print()
print("=" * 98)
print("[25] item 10 identities:  (1/2)^j binom(2j,j)^{1/2} <= 1   and   sum_j binom(a+j-1,j)x^j = (1-x)^{-a}")
print("=" * 98)
from math import comb, lgamma, exp, log
worst = max((0.5 ** j) * comb(2 * j, j) ** 0.5 for j in range(0, 400))
print(f"  max_j (1/2)^j binom(2j,j)^{{1/2}} = {worst:.6f}   (<= 1: {worst <= 1.0 + 1e-12})")
for a, x in ((3.5, 0.3), (12.5, 0.05), (100.5, 0.005)):
    tot = 0.0
    for j in range(0, 4000):
        # binom(a+j-1, j) = Gamma(a+j)/(Gamma(a) j!)
        tot += exp(lgamma(a + j) - lgamma(a) - lgamma(j + 1)) * x ** j
    exact = (1.0 - x) ** (-a)
    print(f"  a={a:6.1f} x={x:5.3f}: series={tot:.10e}  (1-x)^-a={exact:.10e}  "
          f"rel.err={abs(tot/exact-1):.2e}")

# ----------------------------------------------------------------------------------
print()
print("=" * 98)
print("[26] (269) vs the sharpened (270):  radius and leading coefficient")
print("     old: t < 1/(2|m|+|k|), leading term 16 L (|m| t)^2")
print("     new: t < 1/|k|       , leading term  2 L (|m| t)^2   => factor 8")
print("=" * 98)
L = PI
for k, m in ((1.0, 5.0), (1.0, 50.0), (3.0, 100.0)):
    a = abs(m / k) + 0.5
    A = abs(m) + 0.5 * abs(k)
    t_old, t_new = 1.0 / (2 * A), 1.0 / abs(k)
    t = 0.2 * t_old                                   # inside both radii
    old = 4 * L * (2 * A * t) ** 2 / (1 - 2 * A * t)
    new = 4 * L * ((1 - abs(k) * t) ** (-a) - 1 - a * abs(k) * t)
    # also verify the termwise inequality that justifies the sharpening, for each j
    def lhs_log(j):
        # log binom(2j,j) = lgamma(2j+1) - 2 lgamma(j+1); comb() overflows float for large j
        return (0.5 * (lgamma(2 * j + 1) - 2 * lgamma(j + 1)) - j * log(2.0)
                + lgamma(a + j) - lgamma(a) + j * log(abs(k)))

    def rhs_log(j):
        return lgamma(j + 1) + j * log(4 * A)
    ok = all(lhs_log(j) <= rhs_log(j) + 1e-9 for j in range(2, 200))
    print(f"  k={k:g} m={m:g}: radius old={t_old:.4e}  new={t_new:.4e} "
          f"(ratio {t_new/t_old:6.1f}x)   at t=0.2/(2A): old={old:.4e} new={new:.4e} "
          f"(old/new={old/new:5.2f})   termwise-ineq={ok}")
print("  leading-coefficient check (t -> 0):")
for k, m in ((1.0, 50.0), (3.0, 100.0)):
    a = abs(m / k) + 0.5
    A = abs(m) + 0.5 * abs(k)
    t = 1e-6 / A
    old = 4 * L * (2 * A * t) ** 2 / (1 - 2 * A * t)
    new = 4 * L * ((1 - abs(k) * t) ** (-a) - 1 - a * abs(k) * t)
    print(f"    k={k:g} m={m:g}: old/new = {old/new:.4f}   (predicted -> 8)")


# ----------------------------------------------------------------------------------
print()
print("=" * 98)
print("[27] which K meets the hypotheses?   rho = K - Kbar_2 is the POINTWISE exponent of (109)")
print("     Lemma 4.27 needs rho > m+1;  Theorem 4.28 uses m = 2, i.e. rho > 3")
print("=" * 98)
nan = float('nan')
print("     exponent from the Hoelder split in the proof:  K*beta,  beta < 1-(m+1)/rho")
print("     m=2 is what Theorem 4.28 uses: needs K*beta > 2 for the limit, >= 3 for the O(eps_M) rate")
print(f"  {'K':>3} {'rho':>7} {'K*beta (m=2)':>13} {'limit?':>8} {'rate?':>7}")
first_lim = first_rate = None
for K in range(2, 21):
    h = daubechies(K)
    rho = sup_exponent(h)
    kb = K * (1.0 - 3.0 / rho) if rho > 3 else nan
    lim = (kb > 2.0)
    rat = (kb >= 3.0)
    if lim and first_lim is None:
        first_lim = K
    if rat and first_rate is None:
        first_rate = K
    print(f"  {K:3d} {rho:7.3f} {kb:13.2f} {str(lim):>8} {str(rat):>7}")
print(f"  => smallest K with the LIMIT of Thm 4.28: K = {first_lim}")
print(f"  => smallest K with the O(eps_M) RATE:     K = {first_rate}")
print("  (both are sufficient conditions from a conservative estimate; check [23] shows the")
print("   true order of (252) is K, so the genuine threshold is far lower)")
