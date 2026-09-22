"""Generate the JSON the figures and the interactive page are built from.

Everything here is computed, not copied, except the pointwise exponents rho, which are
recorded from Remark 3.13 of the manuscript and labelled as such.  The interactive page
reimplements these same formulas in JavaScript and is checked against this file.

    python3 tools/make_data.py            # writes docs/data/*.json
"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dbfilters import daubechies, shat, centre_of_mass, sobolev_exponent, selftest  # noqa: E402

PI = np.pi
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "docs", "data")
KS = list(range(2, 13))


# --- momentum-cutoff operator norms, os_check12.py -------------------------------------
def opnorm(N, k, delta, pad=6):
    eps = 2.0 ** (-N) * PI
    n = np.arange(-2 ** (N + pad), 2 ** (N + pad)) + 0.5
    chi = lambda x: (np.abs(x) < PI / eps).astype(float)
    d = np.cos(0.25 * eps * k) ** 2 * np.sin(eps * (n - 0.5 * k)) / eps * chi(n - k) * chi(n) - (n - 0.5 * k)
    return float(np.max(np.abs(d) / (1.0 + np.abs(n)) ** (1.0 + delta)))


def hsnorm(N, k):
    eps = 2.0 ** (-N) * PI
    n = np.arange(-4 * int(abs(k)) - 4, 4 * int(abs(k)) + 5) + 0.5
    n = n[(n > 0) & (n - k < 0)]
    chi = lambda x: (np.abs(x) < PI / eps).astype(float)
    t = np.cos(0.25 * eps * k) ** 2 * np.sin(eps * (n - 0.5 * k)) / eps * chi(n - k) * chi(n) - (n - 0.5 * k)
    return float(np.sqrt(np.sum(np.abs(t) ** 2)))


# --- vacuum symbol deviation, os_check14.py --------------------------------------------
def vacuum_deviation(M=3, nmax=8):
    epsM = 2.0 ** (-M) * PI
    k = PI / epsM - 0.5
    sx = np.array([[0, 1], [1, 0]], complex)
    sy = np.array([[0, -1j], [1j, 0]])
    id2 = np.eye(2)
    s = np.sign(k)
    full, chir, Ns = [], [], []
    for N in range(M + 1, M + 1 + nmax):
        eps = 2.0 ** (-N) * PI
        P = 0.5 * (id2 + s * (-np.sin(0.5 * eps * k) * sx + np.cos(0.5 * eps * k) * sy))
        Pc = 0.5 * (id2 + s * sy)
        full.append(float(np.linalg.norm(P - Pc, 2)))
        chir.append(float(abs(0.5 * (1 + s * np.cos(0.5 * eps * k)) - 0.5 * (1 + s))))
        Ns.append(N)
    return dict(M=M, k=float(k), N=Ns, full=full, chiral=chir)


def rates(vals):
    return [float(-np.log2(vals[i + 1] / vals[i])) for i in range(len(vals) - 1)]


def main():
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    st = selftest(verbose=True)

    taps = {str(K): [float(x) for x in daubechies(K)] for K in KS}
    mu = {str(K): centre_of_mass(daubechies(K)) for K in KS}
    filters = {
        "_comment": ("Daubechies filters by spectral factorisation, sum h = sqrt 2, in the "
                     "manuscript's convention: mu(_4 s) = 5.99 and mu(_10 s) = 16.87 as in "
                     "Remark 3.5. numerics/os_check.py hard-codes the mirror image of these, "
                     "which has the same |shat| and the reflected centre of mass."),
        "conventions": {"m0": "2^{-1/2} sum_n h_n e^{-i n xi}",
                        "shat": "prod_{j>=1} m0(2^{-j} xi)",
                        "eps_N": "2^{-N} L with L = pi"},
        "taps": taps,
        "mu": mu,
        "support": {str(K): 2 * K - 1 for K in KS},
        "mu_over_support": {str(K): mu[str(K)] / (2 * K - 1) for K in KS},
        "selftest": {k: float(v) for k, v in st.items()},
    }
    with open(os.path.join(OUT, "filters.json"), "w") as f:
        json.dump(filters, f, indent=1)
    print("  filters.json: K = 2..12, %d taps total" % sum(len(v) for v in taps.values()))

    print("  computing Sobolev exponents (dyadic-block fit) ...", end="", flush=True)
    sigma = {str(K): sobolev_exponent(daubechies(K), npts=8001) for K in KS}
    print(" done")

    deltas = [0.0, 0.5, 1.0, 2.0, 3.0]
    Nrange = [4, 5, 6, 7, 8]
    mc = {}
    for d in deltas:
        v = [opnorm(N, 2.0, d) for N in Nrange]
        mc["%g" % d] = {"N": Nrange, "value": v, "rates": rates(v), "predicted": min(d, 2.0)}
    hs = {}
    for k in (2.0, 4.0, 8.0):
        v = [hsnorm(N, k) for N in Nrange]
        hs["%g" % k] = {"N": Nrange, "value": v, "rates": rates(v), "predicted": 2.0}

    vac = vacuum_deviation()
    vac["rates_full"] = rates(vac["full"])
    vac["rates_chiral"] = rates(vac["chiral"])

    recorded = {
        "_comment": "Computed by tools/make_data.py unless a 'source' field says otherwise.",
        "generated_by": "tools/make_data.py",
        "sobolev_sigma": {"value": sigma,
                          "method": "dyadic-block L^2 decay of shat, as in numerics/os_check4.py",
                          "note": "sigma_2 = 1 exactly in theory; db2 is the borderline case"},
        "pointwise_rho": {"value": {"2": 1.336, "4": 1.910, "6": 2.431, "8": 2.927, "10": 3.409},
                          "source": "recorded from Remark 3.13 of free_fermion_cft_v5.tex",
                          "note": "largest rho with |shat(l)| <= C(1+|l|)^{-rho}; not recomputed here"},
        "thresholds": [
            {"needs": "sigma_K > 1", "where": "Lemma 4.7, D_W in the domain", "minK": 3},
            {"needs": "sigma_K > 3/2", "where": "Lemma 4.23, both Cauchy-Schwarz factors", "minK": 4},
            {"needs": "sigma_K > 2", "where": "Remark 6.4, the simulation budget", "minK": 5},
            {"needs": "sigma_K > 5/2", "where": "Theorem 4.25, the smeared rate", "minK": 7},
            {"needs": "sigma_K > 3", "where": "the advertised delta = 2 rate", "minK": 9},
        ],
        "momentum_cutoff_opnorm": {"k": 2.0, "by_delta": mc,
                                   "formula": "sup_n |d_N(n)| / <n>^{1+delta}, os_check12.py"},
        "momentum_cutoff_hs": {"by_k": hs, "formula": "eq. (225), os_check12.py"},
        "vacuum_deviation": vac,
        "wavelet_route_opnorm": {
            "source": "recorded from numerics/os_check11.py via the project record",
            "delta0_norms": {"N": [3, 4, 5, 6, 7], "value": [1.365, 1.824, 1.107, 1.036, 1.035]},
            "recentred_rates": {"delta": [1.0, 1.5, 2.5], "rate": [1.00, 1.50, 2.00]},
            "note": "at delta = 0 the norm does not converge; re-centring gives min{delta,2}",
        },
        "wzw_currents": {
            "source": "recorded from numerics/os_check13.py via the project record",
            "unmodified_hs": {"k": [1, 3, 6], "value": [1.0, 1.7, 2.4],
                              "closed_form": "sqrt(|k| L / pi), constant in N"},
            "modified_hs": 0.0,
            "rates": {"delta": [0.0, 0.5, 1.0, 2.0, 3.0], "rate": [0.00, 0.51, 1.02, 2.03, 3.05]},
        },
        "multiplicity": {
            "source": "recorded from the Zini-Wang note, Section 7, and numerics/os_check19.py",
            "rows": [
                {"algebra": "full", "route": "momentum cutoff", "finite_M": "0", "M_infinity": "0", "reaches": True},
                {"algebra": "chiral", "route": "momentum cutoff", "finite_M": "|Gamma_{N,-}|", "M_infinity": "0", "reaches": False},
                {"algebra": "chiral", "route": "wavelet", "finite_M": "|Gamma_{N,-}|", "M_infinity": "|Gamma_{N,-}|", "reaches": True},
            ],
            "entropy_density": 2 * float(np.log(2)) - 1,
            "commutator": "||[P(k), p_mp]|| = (1/2)|sin(eps_N k / 2)|",
        },
    }
    with open(os.path.join(OUT, "recorded.json"), "w") as f:
        json.dump(recorded, f, indent=1)
    print("  recorded.json written")
    print("  sigma_K:", " ".join("%.3f" % sigma[str(K)] for K in KS))
    print("  done in %.1f s" % (time.time() - t0))


if __name__ == "__main__":
    main()
