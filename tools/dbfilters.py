"""Daubechies filters and the scaling-function transform, in the paper's conventions.

The construction is the one used by `numerics/os_check4.py` (spectral factorisation of
the Daubechies polynomial); it is repeated here rather than imported because the check
scripts print at import time.  `selftest()` verifies the filters against the published
tables hard-coded in `numerics/os_check.py`, so the agreement is checked, not assumed.

Conventions, matching the manuscript and every check script:

    m0(xi)    = 2^{-1/2} sum_n h_n e^{-i n xi}
    shat(xi)  = prod_{j>=1} m0(2^{-j} xi)          (truncated adaptively)
    eps_N     = 2^{-N} L,  L = pi  =>  Gamma_{inf,+} = Z,  Gamma_{inf,-} = Z + 1/2

Stdlib + numpy only.
"""
import math
import numpy as np
from numpy.polynomial import polynomial as P

__all__ = ["daubechies", "m0", "shat", "prod_m0", "orthonormality_error",
           "centre_of_mass", "sobolev_exponent", "selftest"]


def daubechies(K):
    """Orthonormal Daubechies filter with K vanishing moments (2K taps), sum h = sqrt 2."""
    coef = np.array([float(math.comb(K - 1 + n, n)) for n in range(K)])
    ys = np.roots(coef[::-1]) if K > 1 else np.array([])
    zs = []
    for y in ys:
        b = 2 - 4 * y
        disc = np.sqrt(b * b - 4 + 0j)
        for z in ((b + disc) / 2, (b - disc) / 2):
            if abs(z) < 1.0 - 1e-12:
                zs.append(z)
                break
    poly = np.array([1.0 + 0j])
    for _ in range(K):
        poly = P.polymul(poly, [1.0, 1.0])
    for z in zs:
        poly = P.polymul(poly, [-z, 1.0])
    h = np.real_if_close(poly, tol=1e6).real
    return h / np.sum(h) * np.sqrt(2.0)


def m0(xi, h):
    n = np.arange(len(h))
    xi = np.asarray(xi, dtype=float)
    return (np.exp(-1j * np.multiply.outer(xi, n)) @ np.asarray(h)) / np.sqrt(2.0)


def shat(xi, h, J=None):
    """shat(xi) = prod_{j=1..J} m0(2^{-j} xi); J adaptive, as in the check scripts."""
    xi = np.asarray(xi, dtype=float)
    if J is None:
        J = int(np.ceil(np.log2(max(float(np.max(np.abs(xi))), 1.0)))) + 32
    out = np.ones(xi.shape, dtype=complex)
    for j in range(1, J + 1):
        out = out * m0(xi * 2.0 ** (-j), h)
    return out


def prod_m0(xi, h, jmin, jmax):
    """The finite product prod_{j=jmin..jmax} m0(2^{-j} xi), never formed as a quotient."""
    xi = np.asarray(xi, dtype=float)
    out = np.ones(xi.shape, dtype=complex)
    for j in range(jmin, jmax + 1):
        out = out * m0(xi * 2.0 ** (-j), h)
    return out


def orthonormality_error(h):
    n = len(h)
    return max(abs(sum(h[i] * h[i + 2 * k] for i in range(n - 2 * k)) - (1.0 if k == 0 else 0.0))
               for k in range(n // 2))


def centre_of_mass(h):
    """mu(s) = int x s(x) dx = 2^{-1/2} sum_n n h_n."""
    return float(sum(n * h[n] for n in range(len(h))) / math.sqrt(2.0))


def sobolev_exponent(h, jmin=6, jmax=14, npts=20001):
    """sigma_K from the dyadic-block L^2 decay of shat, as in os_check4.py."""
    a, e = [], []
    for j in range(jmin, jmax):
        lo, hi = 2.0 ** j, 2.0 ** (j + 1)
        xi = np.linspace(lo, hi, npts)
        a.append(2.0 ** j)
        e.append(np.trapezoid(np.abs(shat(xi, h)) ** 2, xi))
    a, e = np.array(a), np.array(e)
    # the dyadic block integral behaves as e ~ a^{1-2p} with p the L^2 decay exponent,
    # and sigma = p - 1/2, so sigma = -slope/2.  (Getting this offset wrong shifts every
    # value by exactly 1/2, which is why selftest() pins it against the published table.)
    slope = np.polyfit(np.log(a), np.log(e), 1)[0]
    return float(-slope / 2.0)


# The tables hard-coded in numerics/os_check.py.  They are the MIRROR IMAGE of what
# daubechies() builds: reversing a real filter replaces m0(xi) by e^{-i(2K-1)xi} conj(m0(xi)),
# so |m0| and hence |shat| are unchanged, while the scaling function is reflected about the
# midpoint of its support and the centre of mass mu(s) becomes (2K-1) - mu(s).
#
# Which convention is the manuscript's?  The built one: it gives mu(_4 s) = 5.9946 and
# mu(_10 s) = 16.8690, the values Remark 3.5 quotes as 5.99 and 16.87, and the ratios
# mu/(2K-1) = 0.7887 .. 0.8912 that Remark 3.8 quotes as 0.789 .. 0.891.  The reflected
# table gives 1.0054 and 2.1310 instead.  os_check.py uses the reflected table but computes
# only magnitudes, so nothing there is affected; os_check4.py and os_check18.py, which
# compute mu and the re-centring, build the filter and are in the manuscript's convention.
_MIRRORED = {
    2: [0.48296291314469025, 0.83651630373746899, 0.22414386804185735, -0.12940952255092145],
    3: [0.33267055295095688, 0.80689150931333875, 0.45987750211933132, -0.13501102001039084,
        -0.085441273882241486, 0.035226291882100656],
    4: [0.23037781330885523, 0.71484657055254153, 0.63088076792959036, -0.027983769416983849,
        -0.18703481171888114, 0.030841381835986965, 0.032883011666982945, -0.010597401784997278],
}

# mu(s) as Remark 3.5 quotes it, and mu/(2K-1) as Remark 3.8 tabulates it
_MU_REFERENCE = {4: 5.99, 10: 16.87}
_MU_RATIO_REFERENCE = {2: 0.789, 12: 0.891}

# the Villemoes/Daubechies values quoted in numerics/os_check4.py and in Remark 3.13
_SIGMA_REFERENCE = {2: 1.000, 3: 1.415, 4: 1.776, 6: 2.386, 8: 2.917}


def selftest(verbose=True):
    """Filters match the published tables up to reflection, are orthonormal, and are in the
    manuscript's convention for the centre of mass."""
    worst_tab = worst_orth = worst_mag = 0.0
    for K, ref in _MIRRORED.items():
        h = daubechies(K)
        worst_tab = max(worst_tab, float(np.max(np.abs(h[::-1] - np.array(ref)))))
    for K in range(2, 13):
        h = daubechies(K)
        worst_orth = max(worst_orth, orthonormality_error(h))
    xi = np.linspace(0.3, 40.0, 97)
    h4 = daubechies(4)
    worst_mag = float(np.max(np.abs(np.abs(shat(xi, h4)) - np.abs(shat(xi, h4[::-1])))))
    worst_sigma = max(abs(sobolev_exponent(daubechies(K), npts=8001) - v)
                      for K, v in _SIGMA_REFERENCE.items())
    worst_mu = max(abs(centre_of_mass(daubechies(K)) - v) for K, v in _MU_REFERENCE.items())
    worst_ratio = max(abs(centre_of_mass(daubechies(K)) / (2 * K - 1) - v)
                      for K, v in _MU_RATIO_REFERENCE.items())
    s0 = abs(shat(np.array([0.0]), h4)[0] - 1.0)
    ok = (worst_tab < 1e-11 and worst_orth < 6e-15 and worst_mag < 1e-14
          and worst_sigma < 6e-3 and worst_mu < 5e-3 and worst_ratio < 5e-4 and s0 < 1e-12)
    if verbose:
        print("dbfilters selftest")
        print("  vs published tables, up to reflection : %.1e" % worst_tab)
        print("  orthonormality, K = 2..12             : %.1e" % worst_orth)
        print("  |shat| invariant under reflection     : %.1e" % worst_mag)
        print("  sigma_K vs Villemoes/Daubechies       : %.1e" % worst_sigma)
        print("  mu(s) vs Remark 3.5 (5.99, 16.87)     : %.1e" % worst_mu)
        print("  mu/(2K-1) vs Remark 3.8 (0.789,0.891) : %.1e" % worst_ratio)
        print("  shat(0) - 1                           : %.1e" % s0)
        print("  -> %s" % ("OK" if ok else "FAIL"))
    if not ok:
        raise SystemExit("dbfilters selftest failed")
    return {"table": worst_tab, "orthonormality": worst_orth, "magnitude": worst_mag,
            "sigma": worst_sigma, "mu": worst_mu, "mu_ratio": worst_ratio, "shat0": s0}


if __name__ == "__main__":
    selftest()
