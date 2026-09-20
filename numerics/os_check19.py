"""
Part 19: the Zini-Wang comparison -- purity of the finitely renormalized states.

The comparison in Section 1.2 of the main paper asserts that the Zini-Wang structure "is not
immediately available ... where the finitely renormalized states omega^{(N)}_M are not pure (due to
the entanglement of the chiral halves)".  Zini-Wang connecting *unitaries* between the renormalized
GNS spaces exist when those spaces have equal dimension, and for a quasi-free state on a finite
lattice that is governed by purity, i.e. by whether the symbol is a projection.

By (100), omega^{(N)}_M = omega^{(N+M)} o alpha^N_{N+M}, so at one-particle level the symbol is the
COMPRESSION  S^{(N)}_M = (R^N_{N+M})^* S^{(N+M)} R^N_{N+M}  by an isometry.  For S a projection,
    S' = R^*SR  is a projection  <=>  X := (1 - RR^*) S R = 0  <=>  ran R is S-invariant,
and in general  S' - S'^2 = X^*X >= 0.  Two independent mechanisms make X != 0 here:

  (a) CHIRALITY.  Restricting to the chiral subalgebra compresses by the CONSTANT projection
      p_mp = (1 -+ sigma_y)/2.  With the massless lattice vacuum symbol (99),
        P(k) = 1/2 (1 + sign(k)( -sin(eps_N k/2) sigma_x + cos(eps_N k/2) sigma_y )),
      the claim is   ||[P(k), p_mp]|| = 1/2 |sin(eps_N k/2)|   and the compressed chiral symbol has
      the single eigenvalue  lambda(k) = 1/2 (1 - sign(k) cos(eps_N k/2)),  so
        lambda(1-lambda) = 1/4 sin^2(eps_N k / 2).
      Vanishes as O((eps_N k)^2) for the modes that survive the scaling limit, but equals 1/4 --
      MAXIMAL mixing -- at the Brillouin-zone boundary.  Hence the entropy is EXTENSIVE.

  (b) THE RENORMALIZATION GROUP.  Compressing the chiral scaling-limit symbol (the Hardy projection
      P^- = chi_{k<0}) by R^N_infty.
        - momentum cutoff: R is band-limiting, P^- is a multiplier => ran R invariant => PURE.
        - wavelet: ran R = V_N is not a momentum band.  The compression is circulant with
            lambda_N(kappa) = sum_{j : kappa + 2 pi j / eps_N < 0} |shat(eps_N kappa + 2 pi j)|^2,
          so by orthonormality  min(lambda, 1-lambda) <= delta(eps_N kappa) = 1 - |shat(eps_N kappa)|^2
          = O((eps_N kappa)^{2K}) -- the SAME aliasing mass that drives the Jackson estimate of
          Lemma 4.28.  Never 0 or 1, so MIXED, but only to order 2K.

Checks: [31] mechanism (a) closed forms + extensivity; [32] momentum cutoff is exactly a projection;
[33] mechanism (b) eigenvalue formula and the aliasing bound.  Pure numpy.
"""
import numpy as np
import sys

sys.path.insert(0, '.')
from os_check4 import daubechies

PI = np.pi
sx = np.array([[0, 1], [1, 0]], complex)
sy = np.array([[0, -1j], [1j, 0]], complex)
pm = {-1: 0.5 * (np.eye(2) - sy), +1: 0.5 * (np.eye(2) + sy)}


def P_lat(k, epsN):
    """Massless lattice vacuum symbol (99)."""
    s = np.sign(k)
    return 0.5 * (np.eye(2) + s * (-np.sin(0.5 * epsN * k) * sx + np.cos(0.5 * epsN * k) * sy))


def binent(p):
    p = np.clip(p, 1e-300, 1 - 1e-300)
    return -p * np.log(p) - (1 - p) * np.log(1 - p)


# ==================================================================================
print("=" * 100)
print("[31] mechanism (a): chiral restriction of the finite-scale lattice vacuum")
print("     claims:  ||[P(k), p_-]|| = 1/2|sin(eps_N k/2)|,   lambda(k) = 1/2(1 - sign(k)cos(eps_N k/2))")
print("=" * 100)
worst_c, worst_l, worst_proj = 0.0, 0.0, 0.0
for N in (3, 6, 9):
    J = 2 ** N
    epsN = 2 * PI / J
    ks = (np.arange(-J // 2, J // 2) + 0.5)          # Neveu-Schwarz momenta
    for k in ks:
        P = P_lat(k, epsN)
        # P must itself be a projection (the full-algebra lattice vacuum is pure)
        worst_proj = max(worst_proj, np.linalg.norm(P @ P - P))
        C = P @ pm[-1] - pm[-1] @ P
        worst_c = max(worst_c, abs(np.linalg.norm(C, 2) - 0.5 * abs(np.sin(0.5 * epsN * k))))
        # compressed chiral symbol: the 1x1 block  <e_-, P e_->  with sigma_y e_- = -e_-
        em = np.array([1, -1j]) / np.sqrt(2)
        lam = np.real(np.vdot(em, P @ em))
        worst_l = max(worst_l, abs(lam - 0.5 * (1 - np.sign(k) * np.cos(0.5 * epsN * k))))
print(f"  max |P^2 - P|                                        = {worst_proj:.3e}   (full-algebra vacuum IS pure)")
print(f"  max | ||[P,p_-]|| - 1/2|sin(eps_N k/2)| |             = {worst_c:.3e}")
print(f"  max | lambda(k) - 1/2(1-sign(k)cos(eps_N k/2)) |      = {worst_l:.3e}")
print()
print("     entropy of the chiral restriction (predicted EXTENSIVE, ~ c * |Lambda_N|):")
for N in range(4, 13):
    J = 2 ** N
    epsN = 2 * PI / J
    ks = np.arange(-J // 2, J // 2) + 0.5
    lam = 0.5 * (1 - np.sign(ks) * np.cos(0.5 * epsN * ks))
    S = float(np.sum(binent(lam)))
    print(f"    N={N:2d}  |Lambda_N|={J:5d}   S = {S:10.3f}   S/|Lambda_N| = {S/J:.6f}"
          f"   max lambda(1-lambda) = {np.max(lam*(1-lam)):.6f}")
print("  => S/|Lambda_N| tends to a nonzero constant: extensive, with the mixing concentrated")
print("     at the zone boundary; the analytic value is (1/2pi) int_-pi^pi H2((1-cos(u/2))/2) du.")
u = np.linspace(-PI, PI, 8000001)
val = float(np.trapezoid(binent(0.5 * (1 - np.cos(0.5 * u))), u) / (2 * PI))
print(f"     integral            = {val:.10f}")
print(f"     2 ln 2 - 1          = {2*np.log(2)-1:.10f}   (difference {abs(val-(2*np.log(2)-1)):.2e})")

# ==================================================================================
print()
print("=" * 100)
print("[32] mechanism (b), momentum cutoff: ran R is a momentum band, P^- is a multiplier")
print("=" * 100)
for N in (4, 7):
    for M in (1, 3, 6):
        J, Jf = 2 ** N, 2 ** (N + M)
        epsf = 2 * PI / Jf
        ks = np.arange(-J // 2, J // 2) + 0.5           # Gamma_N inside Gamma_{N+M}
        dev = 0.0
        for k in ks:
            S = P_lat(k, epsf)                          # compression = same fibre, no mixing
            dev = max(dev, np.linalg.norm(S @ S - S))
        print(f"  N={N} M={M}: max||S'^2 - S'|| over Gamma_N = {dev:.3e}   -> PURE on the full algebra")

# ==================================================================================
print()
print("=" * 100)
print("[33] mechanism (b), wavelet: compression of the Hardy projection by the MRA embedding")
print("     lambda_N(kappa) = sum_{j: kappa + 2 pi j/eps_N < 0} |shat(eps_N kappa + 2 pi j)|^2")
print("=" * 100)


def make_shat(h):
    K = len(h) // 2
    q = list(map(float, h))
    for _ in range(K):                                  # deflate the order-K zero at z = -1
        r = list(reversed(q)); out = [r[0]]
        for c in r[1:]:
            out.append(c - out[-1])
        out.pop(); q = list(reversed(out))
    Q = np.array(q); nq = np.arange(len(Q))

    def m0(x):
        x = np.asarray(x, float)
        return (2 * np.cos(x / 2)) ** K * np.exp(-0.5j * K * x) * (np.exp(-1j * np.multiply.outer(x, nq)) @ Q) / np.sqrt(2)

    def shat(x):
        x = np.asarray(x, float)
        Jt = int(np.ceil(np.log2(max(np.max(np.abs(x)), 1.0)))) + 34
        o = np.ones(x.shape, complex)
        for j in range(1, Jt + 1):
            o = o * m0(x * 2.0 ** (-j))
        return o
    return shat


for K in (2, 4, 6):
    h = daubechies(K)
    shat = make_shat(h)
    print(f"  db{K}:")
    for N in (3, 5):
        J = 2 ** N
        epsN = 2 * PI / J
        JMAX = 400                                       # replicas
        # build the compression explicitly as a matrix on l^2(Lambda_N) and diagonalise it
        ls = np.arange(-JMAX * J, JMAX * J) + 0.5        # Gamma_infty (NS)
        w = np.abs(shat(epsN * ls)) ** 2 / J
        xs = np.arange(J) * epsN
        Sm = np.zeros((J, J), complex)
        neg = ls < 0
        ph = np.exp(-1j * np.multiply.outer(xs, ls[neg]))
        Sm = (ph * w[neg]) @ ph.conj().T
        ev = np.sort(np.linalg.eigvalsh(0.5 * (Sm + Sm.conj().T)))
        # predicted eigenvalue at each kappa in Gamma_N: sum over its NEGATIVE replicas
        kap = np.arange(-J // 2, J // 2) + 0.5
        js = np.arange(-JMAX, JMAX)
        lam = np.array([float(np.sum(np.abs(shat(epsN * (kk + js * J)[(kk + js * J) < 0])) ** 2))
                        for kk in kap])
        d = float(np.max(np.abs(ev - np.sort(lam))))
        mix = np.minimum(lam, 1 - lam)
        delta = 1 - np.abs(shat(epsN * kap)) ** 2          # aliasing mass at the same kappa
        # the bound is per-kappa:  min(lam, 1-lam) <= delta(eps_N kappa)
        slack = float(np.max(mix - delta))
        # the deviation from purity is provably > 0 (every replica term is > 0 for NS momenta),
        # but is of order (eps_N kappa)^{2K} and can drop below double precision
        print(f"    N={N}: |eig-pred| = {d:.1e};  max_k min(l,1-l) = {np.max(mix):.3e};"
              f"  min_k min(l,1-l) = {np.min(mix):+.2e};  bound slack max(min(l,1-l)-delta) = {slack:+.1e}")


# ==================================================================================
print()
print("=" * 100)
print("[34] what Zini-Wang actually need: the GNS MULTIPLICITY, not purity")
print("     A_N is a full matrix algebra, so the GNS space of a state with density rho is")
print("     C^d (x) C^{rank rho}, and two GNS reps are unitarily equivalent iff rank rho agrees.")
print("     For quasi-free omega_S,  rank rho_S = 2^{m(S)},  m(S) := #{eigenvalues of S in (0,1)}.")
print("     So the ZW connecting unitary phi^N_M exists  <=>  m(S^{(N)}_M) = m(S^{(N)}_{M+1}).")
print("=" * 100)
for N in (3, 5):
    J = 2 ** N
    ks = np.arange(-J // 2, J // 2) + 0.5              # Gamma_N, Neveu-Schwarz
    print(f"  N={N}  (|Gamma_N| = {J}):")
    row_full, row_chi = [], []
    for M in list(range(1, 8)):
        epsf = 2 * PI / 2 ** (N + M)
        # full algebra, momentum cutoff: symbol is the 2x2 projection P(k) itself
        mfull = sum(int(np.sum((np.linalg.eigvalsh(P_lat(k, epsf)) > 1e-12)
                               & (np.linalg.eigvalsh(P_lat(k, epsf)) < 1 - 1e-12))) for k in ks)
        # chiral restriction, momentum cutoff
        lam = 0.5 * (1 - np.sign(ks) * np.cos(0.5 * epsf * ks))
        mchi = int(np.sum((lam > 1e-12) & (lam < 1 - 1e-12)))
        row_full.append(mfull); row_chi.append(mchi)
    # M = infinity: the scaling limit
    mfull_inf = 0
    lam_inf = 0.5 * (1 - np.sign(ks))                   # Hardy projection
    mchi_inf = int(np.sum((lam_inf > 1e-12) & (lam_inf < 1 - 1e-12)))
    print(f"    m, full algebra   , M=1..7: {row_full}   M=inf: {mfull_inf}")
    print(f"    m, chiral algebra , M=1..7: {row_chi}   M=inf: {mchi_inf}")
    print(f"      => full algebra: m constant ({row_full[0]}) and equal to the limit  -> phi exist, incl. M=inf")
    print(f"      => chiral      : m constant ({row_chi[0]}) for all finite M, but DROPS to {mchi_inf} at M=inf")
    print(f"         so dim H^(N)_M is constant in M and then collapses by a factor 2^{row_chi[0]} in the limit:")
    print(f"         the ZW inductive limit along the phi's cannot reach the scaling-limit representation.")
