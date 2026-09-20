"""
Part 16: the one-particle energy-growth / Duhamel lemma (item 8).

Lemma 4.11 claims, for the one-particle Virasoro generators
    (ell_{pm,k})_{mn} propto delta_{m, n-k} * (n - k/2)          (a weighted shift by k)
    o = r_{pm,k} = (ell_{k} + ell_{-k})/2,   iota_{pm,k} = (ell_{k} - ell_{-k})/(2i)
the two statements

 (i)  || e^{i tau o} xi ||_{h^sigma}  <=  e^{c_{sigma,k} |tau|} || xi ||_{h^sigma},
      with c_{sigma,0} = 0  and  c_{sigma,k} <= C * sigma * |k| * <k>^{sigma+2},

 (ii) || (e^{it otilde} - e^{ito}) xi ||  <=  kappa * lambda_{sigma,k}(t) * || xi ||_{h^sigma},
      lambda_{sigma,k}(t) = (e^{c |t|} - 1)/c   ( = |t| for k = 0 ).

Checks performed here, on a truncated momentum lattice (l = n + 1/2, Neveu-Schwarz):
  [19] the commutator estimate  ||[W_rho, o] xi|| <= c ||W_rho xi||  that drives the Groenwall
       argument, and the *sharpened* exponent sigma+2 (v5 first had 2*sigma+2): report the
       measured operator norm of  W_rho^{-1}[W_rho, o]  against sigma|k|<k>^{sigma+2}, uniformly
       in the mollifier rho.
  [20] the growth itself: measured  sup_tau (1/tau) log( ||e^{i tau o} xi||_{h^sigma} / ||xi||_{h^sigma} )
       vs. the claimed c_{sigma,k}; and *exact conservation* at k = 0.
  [21] the Duhamel bound (ii) against the true difference of the two unitary groups.

Pure numpy.  Truncation: |n| <= NMAX, with the shift implemented so that mass leaving the
window is discarded -- this only *lowers* the measured norms, so we additionally report the
weight that the flow pushes to the boundary, to show the truncation is not what is being tested.
"""
import numpy as np

PI = np.pi


def lattice(NMAX):
    """Neveu-Schwarz momenta l = n + 1/2 (units L/pi = 1), |n| <= NMAX."""
    n = np.arange(-NMAX, NMAX + 1)
    return n + 0.5


def ell(l, k):
    """Weighted shift  (ell_k)_{mn} = delta_{m, n-k} (n - k/2)  on the truncated lattice.

    k must be an integer (so that l -> l - k stays on the l = n + 1/2 lattice).
    Returned as a dense matrix in the basis {e_l}.
    """
    D = len(l)
    A = np.zeros((D, D))
    for j in range(D):
        i = j - k                      # index of l_j - k
        if 0 <= i < D:
            A[i, j] = l[j] - 0.5 * k
    return A


def parts(l, k):
    """r = (ell_k + ell_{-k})/2 and iota = (ell_k - ell_{-k})/(2i), both hermitian."""
    Lk, Lmk = ell(l, k), ell(l, -k)
    r = 0.5 * (Lk + Lmk)
    io = (Lk - Lmk) / (2.0j)
    return r, io


def expm_herm(A, t):
    """exp(i t A) for hermitian A, via eigen-decomposition."""
    w, V = np.linalg.eigh(A)
    return (V * np.exp(1.0j * t * w)) @ V.conj().T


def wsob(l, sigma, rho=0.0):
    """Mollified Sobolev weight w_rho = <l>^sigma (1 + rho<l>)^{-sigma}."""
    br = np.sqrt(1.0 + l ** 2)
    return br ** sigma / (1.0 + rho * br) ** sigma


# ----------------------------------------------------------------------------------
print("=" * 96)
print("[19] commutator estimate  ||[W_rho,o]xi|| <= c ||W_rho xi||   (drives Groenwall)")
print("     reported: measured operator norm of W_rho^{-1}[W_rho,o]  /  (sigma|k|<k>^{sigma+2})")
print("     must stay BOUNDED (<= O(1)) and uniform in the mollifier rho")
print("=" * 96)
NMAX = 700
l = lattice(NMAX)
print(f"  lattice |n| <= {NMAX};  claimed exponent sigma+2  (v5 draft first had 2sigma+2)")
print(f"  {'sigma':>6} {'k':>4} | " + "  ".join(f"rho={r:g}".rjust(11) for r in (0.0, 1e-4, 1e-2, 1.0)))
for sigma in (1.0, 1.5, 2.0, 3.0):
    for k in (1, 2, 5):
        r_op, _ = parts(l, k)
        row = []
        for rho in (0.0, 1e-4, 1e-2, 1.0):
            w = wsob(l, sigma, rho)
            W = np.diag(w)
            C = W @ r_op - r_op @ W                    # [W_rho, o]
            # operator norm of W_rho^{-1} [W_rho, o]  (W_rho invertible, diagonal, positive)
            M = np.diag(1.0 / w) @ C
            nrm = np.linalg.norm(M, 2)
            pred = sigma * abs(k) * (1.0 + k ** 2) ** ((sigma + 2) / 2)
            row.append(nrm / pred)
        print(f"  {sigma:6.1f} {k:4d} | " + "  ".join(f"{v:11.4f}" for v in row))

# ----------------------------------------------------------------------------------
print()
print("=" * 96)
print("[20] Sobolev-norm growth along the flow:  ||e^{i tau o}xi||_{h^sigma} <= e^{c|tau|}||xi||_{h^sigma}")
print("     reported: measured growth exponent  max_tau log(ratio)/tau   vs. claimed c_{sigma,k}")
print("=" * 96)
NMAX = 400
l = lattice(NMAX)
rng = np.random.default_rng(20260730)
taus = np.array([0.05, 0.1, 0.2, 0.4])
for sigma in (1.0, 2.0):
    for k in (0, 1, 3):
        r_op, _ = parts(l, k)
        w = wsob(l, sigma)
        pred = sigma * abs(k) * (1.0 + k ** 2) ** ((sigma + 2) / 2)
        meas, bdry = -np.inf, 0.0
        for _ in range(6):
            # xi concentrated at moderate |n| so the truncation is not probed
            xi = rng.standard_normal(len(l)) * np.exp(-(l / 60.0) ** 2)
            xi = xi / np.linalg.norm(xi)
            n0 = np.linalg.norm(w * xi)
            for tau in taus:
                y = expm_herm(r_op, tau) @ xi
                meas = max(meas, np.log(np.linalg.norm(w * y) / n0) / tau)
                bdry = max(bdry, abs(y[:20]).max() + abs(y[-20:]).max())
        tag = "  <-- exact conservation expected" if k == 0 else ""
        print(f"  sigma={sigma:3.1f} k={k}: measured rate {meas:+.4e}   claimed c = {pred:8.3f}"
              f"   ok={meas <= pred + 1e-9}   (boundary weight {bdry:.1e}){tag}")

# ----------------------------------------------------------------------------------
print()
print("=" * 96)
print("[21] Duhamel bound (ii):  ||(e^{it otilde}-e^{ito})xi|| <= kappa lambda_{sigma,k}(t) ||xi||_{h^sigma}")
print("     otilde := o + eps*V  with V a bounded self-adjoint perturbation, kappa := ||otilde-o||_{h^sigma->h^0}")
print("=" * 96)
NMAX = 300
l = lattice(NMAX)
sigma = 1.5
w = wsob(l, sigma)
for k in (0, 2):
    r_op, _ = parts(l, k)
    pred_c = sigma * abs(k) * (1.0 + k ** 2) ** ((sigma + 2) / 2)
    # perturbation: a bounded weighted shift, so that ||V||_{h^sigma -> h^0} is finite and computable
    V = 0.5 * (ell(l, 1) + ell(l, -1)) / np.sqrt(1.0 + l ** 2).max()
    for eps in (1e-2, 1e-3):
        ot = r_op + eps * V
        # kappa = || (ot - o) ||_{h^sigma -> h^0}  =  || (eps V) W^{-1} ||_2
        kappa = np.linalg.norm((eps * V) @ np.diag(1.0 / w), 2)
        worst = 0.0
        for t in (0.1, 0.5, 1.0):
            lam = abs(t) if pred_c == 0 else (np.exp(pred_c * abs(t)) - 1.0) / pred_c
            U1, U0 = expm_herm(ot, t), expm_herm(r_op, t)
            for _ in range(4):
                xi = rng.standard_normal(len(l)) * np.exp(-(l / 40.0) ** 2)
                xi = xi / np.linalg.norm(w * xi)          # ||xi||_{h^sigma} = 1
                lhs = np.linalg.norm((U1 - U0) @ xi)
                worst = max(worst, lhs / (kappa * lam))
        print(f"  k={k} eps={eps:g}: kappa={kappa:.3e}  c={pred_c:7.3f}   "
              f"max over t,xi of LHS/(kappa*lambda) = {worst:.4f}   ok={worst <= 1.0}")
