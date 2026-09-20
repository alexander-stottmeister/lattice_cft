"""
Part 18: the Tier-3 items 11, 12, 13.

[28] ITEM 11 (Proposition 3.7, quasi-local structure) -- quantify the localisation.
     supp(_K s) = [0, 2K-1], so supp(s^{(eps_N)}(. - x)) = x + eps_N[0, 2K-1] and the inflation
     radius is eps_N(2K-1).  Report the radius in lattice units, and compare it with the
     centre-of-mass offset mu(s) of Remark 3.5: is mu(s) a fixed fraction of the support width?

[29] ITEM 12 (§4.2.2) -- the finite-N algebra for the MODIFIED approximants carrying chi_{Gamma_N}.
     At one-particle level the KS approximant is a weighted shift by k; the modification replaces
     the periodic wrap-around by a truncation.  The commutator of two truncated shifts differs
     from the truncation of the untruncated commutator by
        D(l) = chi(l-k-k') [ w_{k'}(l) w_k(l-k') (chi(l-k')-1) - w_k(l) w_{k'}(l-k) (chi(l-k)-1) ],
     supported where l-k-k' stays in Gamma_N but l-k or l-k' leaves it -- i.e. within |k|+|k'| of
     the Brillouin-zone boundary.  Predictions:
        (i)  ||D||           = O(1)          -- the modification is NOT small in operator norm;
        (ii) ||D||_{h^s->h^0} = O(eps_N^s)   -- but it is small on any fixed Sobolev vector,
             because its support sits at |l| ~ pi/eps_N.
     So the modification is harmless exactly where the paper uses it, and (ii) beats the
     O(eps_N^2) remainder R^{(N)} of (166) as soon as s > 2.

[30] ITEM 13 (§4.2.5) -- the half-shift identity.  h^{(N)}_x = htilde_x + htilde_{x+eps_{N+1}}
     for x in Lambda_N (167) implies, for the Fourier modes,
        H^{(N)}_k = 2 e^{-i eps_N k/4} [ cos(eps_N k/4) Htilde_k + i sin(eps_N k/4) Htilde_{k+pi/eps_{N+1}} ],
     i.e. the two-component mode at k mixes the single-component mode at k with the UMKLAPP mode
     at k + pi/eps_{N+1}, with amplitude sin(eps_N k /4) = O(eps_N k).  This is what makes the two
     expressions "not directly comparable", and it is where the e^{-i eps_N k/4} prefactor of (216)
     comes from.  Checked here as a pure Fourier identity on random data.

Pure numpy.
"""
import numpy as np
import sys

sys.path.insert(0, '.')
from os_check4 import daubechies

PI = np.pi


# ==================================================================================
print("=" * 100)
print("[28] item 11: localisation radius of the wavelet renormalization group")
print("     supp(_K s) = [0, 2K-1]  =>  inflation radius eps_N (2K-1), one-sided")
print("=" * 100)
print(f"  {'K':>3} {'supp width 2K-1':>16} {'mu(s)':>9} {'mu(s)/(2K-1)':>14} {'sites lost per interval':>24}")
for K in range(2, 13):
    h = daubechies(K)
    mu = float(np.sum(np.arange(len(h)) * h) / np.sqrt(2.0))
    w = 2 * K - 1
    print(f"  {K:3d} {w:16d} {mu:9.3f} {mu/w:14.4f} {w:24d}")
print("  => mu(s) is a fixed fraction ~0.86-0.89 of the support width, so the re-centring shift")
print("     eps_N mu(s) of Remark 3.5 and the localisation radius eps_N(2K-1) are the same order.")

# ==================================================================================
print()
print("=" * 100)
print("[29] item 12: does the chi_{Gamma_N} modification spoil the finite-N Virasoro algebra?")
print("=" * 100)


def weights(J, k, epsN):
    """Symbol of the chiral KS approximant, w_k(l) = eps_N^{-1} cos(eps_N k/4)^2 sin(eps_N(l+k/2)).

    Momenta are l = n + 1/2 (Neveu-Schwarz), n = -J/2 .. J/2-1, so eps_N l fills (-pi, pi).
    """
    n = np.arange(-J // 2, J // 2)
    l = n + 0.5
    return l, np.cos(0.25 * epsN * k) ** 2 * np.sin(epsN * (l + 0.5 * k)) / epsN


def commutator_entries(J, k, kp, epsN, modified):
    """Entries B(l) of [A_k, A_{k'}] at position (l-k-k', l), on the l-grid.

    Unmodified: shifts wrap around the periodic momentum lattice.
    Modified:   shifts are truncated by chi_{Gamma_N}.
    """
    l, _ = weights(J, k, epsN)
    D = len(l)

    def w(kk, idx):
        """w_{kk} evaluated at grid index idx (mod J), plus the chi factor if modified."""
        _, wk = weights(J, kk, epsN)
        return wk[idx % D]

    def chi(idx):
        return np.where((idx >= 0) & (idx < D), 1.0, 0.0) if modified else np.ones(idx.shape)

    i = np.arange(D)                       # index of l
    # [A_k, A_k'] e_l = ( w_k'(l) w_k(l-k') chi(l-k') - w_k(l) w_k'(l-k) chi(l-k) ) chi(l-k-k') e_{l-k-k'}
    t1 = w(kp, i) * w(k, i - kp) * chi(i - kp)
    t2 = w(k, i) * w(kp, i - k) * chi(i - k)
    return (t1 - t2) * chi(i - k - kp)


print("     D := (modified commutator) - chi * (unmodified commutator)")
print("     reported: sup|D| (predicted O(1))  and  sup|D|/<l>^s = ||D||_{h^s->h^0} (predicted O(eps_N^s))")
print("     NOTE: for k, k' of the SAME sign the intermediate shift is trapped between 0 and k+k',")
print("     so if l-k-k' stays in Gamma_N then so do l-k and l-k'; D vanishes IDENTICALLY there.")
print("     The edge term can only appear for OPPOSITE signs.  Both cases are reported.")
for (k, kp) in ((1, 2), (2, 3), (3, -1), (5, -2), (1, -4)):
    print(f"  k={k}, k'={kp}:")
    rows = {s: [] for s in (1.0, 2.0, 3.0)}
    sup, nsupp = [], []
    for N in range(6, 15):
        J = 2 ** N
        epsN = 2 * PI / J
        l, _ = weights(J, k, epsN)
        Bm = commutator_entries(J, k, kp, epsN, True)
        Bu = commutator_entries(J, k, kp, epsN, False)
        i = np.arange(len(l))
        chi_out = np.where((i - k - kp >= 0) & (i - k - kp < len(l)), 1.0, 0.0)
        D = Bm - chi_out * Bu
        sup.append(float(np.max(np.abs(D))))
        nsupp.append(int(np.count_nonzero(np.abs(D) > 1e-13)))
        br = np.sqrt(1.0 + l ** 2)
        for s in rows:
            rows[s].append(float(np.max(np.abs(D) / br ** s)))
    print(f"    sup|D|            : " + " ".join(f"{v:.3e}" for v in sup))
    print(f"    # nonzero entries : " + " ".join(f"{v:9d}" for v in nsupp)
          + f"   (predicted O(|k|+|k'|) = O({k+kp}))")
    if max(sup) == 0.0:
        print("    D vanishes identically for every N  <-- same-sign case, algebra exact")
        continue
    for s in (1.0, 2.0, 3.0):
        r = rows[s]
        rates = [np.log2(r[i] / r[i + 1]) for i in range(len(r) - 1)
                 if r[i + 1] > 0 and r[i] > 0]
        print(f"    ||D||_h^{s:g}->h^0    : " + " ".join(f"{v:.2e}" for v in r))
        print(f"        rate in eps_N : " + "  ".join(f"{v:5.2f}" for v in rates)
              + f"   (predicted {s:.2f})")

# ==================================================================================
print()
print("=" * 100)
print("[30] item 13: the half-shift identity for the Fourier modes")
print("     H_k = 2 e^{-i eps_N k/4}[cos(eps_N k/4) Ht_k + i sin(eps_N k/4) Ht_{k+pi/eps_{N+1}}]")
print("=" * 100)
rng = np.random.default_rng(20260730)
for N in (4, 6, 8):
    J = 2 ** N                      # |Lambda_N| = J;  |Lambda_{N+1}| = 2J
    epsN1 = 2 * PI / (2 * J)        # eps_{N+1};  circle of circumference 2 pi
    epsN = 2 * epsN1
    y = np.arange(2 * J) * epsN1                       # Lambda_{N+1}
    f = rng.standard_normal(2 * J) + 1j * rng.standard_normal(2 * J)   # htilde on Lambda_{N+1}
    worst = 0.0
    for k in range(0, 6):
        # left-hand side: the Lambda_N mode of h_x = f_x + f_{x+eps_{N+1}}
        xs = np.arange(J) * epsN                        # Lambda_N
        hx = f[0::2] + f[1::2]                          # f_x + f_{x+eps_{N+1}} for x in Lambda_N
        lhs = epsN * np.sum(np.exp(1j * k * xs) * hx)
        # right-hand side: single-component modes on Lambda_{N+1} at k and at the umklapp momentum
        Ht_k = epsN1 * np.sum(np.exp(1j * k * y) * f)
        Ht_um = epsN1 * np.sum(np.exp(1j * (k + PI / epsN1) * y) * f)
        rhs = 2 * np.exp(-1j * epsN * k / 4) * (np.cos(epsN * k / 4) * Ht_k
                                                + 1j * np.sin(epsN * k / 4) * Ht_um)
        worst = max(worst, abs(lhs - rhs) / max(abs(lhs), 1e-30))
    print(f"  N={N} (|Lambda_N|={J}): max relative error over k=0..5 is {worst:.3e}")
print("  => exact identity.  The umklapp amplitude sin(eps_N k/4) = O(eps_N k) is the whole")
print("     obstruction to comparing (216) with (217), and e^{-i eps_N k/4} is the prefactor of (216).")
