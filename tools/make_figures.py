"""Generate the README figures, two themes each, into docs/figures/.

    python3 tools/make_figures.py

Everything is computed here from the filters; docs/data/recorded.json supplies only the
few quantities that are recorded rather than recomputed, and those are labelled in the
captions.  Output is deterministic: the same inputs give byte-identical SVG.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dbfilters import daubechies, shat, centre_of_mass  # noqa: E402
from svgplot import Fig, figure_pair  # noqa: E402

PI = np.pi
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGDIR = os.path.join(HERE, "docs", "figures")
DATA = os.path.join(HERE, "docs", "data")


def load(name):
    with open(os.path.join(DATA, name)) as f:
        return json.load(f)


def thin(x, y, target=1300):
    """Min-max decimation: keep the extremes of each bucket, so spikes and the deep zeros
    of |shat| survive.  Plain subsampling would skip straight over them."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    n = len(x)
    if n <= target:
        return x, y
    buckets = max(1, target // 2)
    idx = set([0, n - 1])
    edges = np.linspace(0, n, buckets + 1).astype(int)
    for a, b in zip(edges[:-1], edges[1:]):
        if b <= a:
            continue
        seg = y[a:b]
        idx.add(a + int(np.argmin(seg)))
        idx.add(a + int(np.argmax(seg)))
    keep = np.array(sorted(idx))
    return x[keep], y[keep]


def scaling_function(K, J=10, iters=60):
    """_K s on the dyadic grid of spacing 2^-J, by iterating the refinement equation
    s(x) = sqrt2 sum_n h_n s(2x - n) from the box function.

    Note the shift: a tap h_n displaces the argument of s(2x - .) by n, which on a grid of
    spacing 2^-J is n*2^J samples, not n.  Upsampling and convolving with h at unit shift,
    the obvious-looking cascade, is a different recursion; it stretches the support by one
    unit and puts the centre of mass out by mu*2^-J.  selfcheck() pins both.
    """
    h = daubechies(K)
    x = np.arange(0, (2 * K - 1) * 2 ** J + 1) / 2.0 ** J
    s = np.where((x >= 0) & (x < 1), 1.0, 0.0)
    for _ in range(iters):
        acc = np.zeros_like(s)
        for n, hn in enumerate(h):
            acc += hn * np.interp(2 * x - n, x, s, left=0.0, right=0.0)
        s = np.sqrt(2.0) * acc
    return x, s


# ------------------------------------------------------------------ figure 1
def fig_shat_zeros(theme):
    f = Fig(940, 470, theme, title="The transform of the scaling function vanishes to order K at every 2πn",
            xlabel="ξ", ylabel="|ŝ(ξ)|")
    xi = np.linspace(1e-3, 8 * PI, 9000)
    for i, K in enumerate((2, 4, 8)):
        h = daubechies(K)
        tx, ty = thin(xi, np.abs(shat(xi, h)))
        f.line(tx, ty, i, width=1.9, label="db%d  (K = %d)" % (K, K))
    for n in range(1, 5):
        f.vline(2 * PI * n, color="mute", dash="3 4", width=1.0)
    f.xlog(10) if False else None
    f.ylog(10)
    f.ylim(1e-13, 3.0)
    f.xlim(0, 8 * PI)
    f.xticks([0, 2 * PI, 4 * PI, 6 * PI, 8 * PI], ["0", "2π", "4π", "6π", "8π"])
    f.annotate(2 * PI, 2e-12, "zeros of order K", dx=6, dy=0, anchor="start", size=12.5)
    f.annotate(5.2 * PI, 0.9, "a quotient ŝ(εm)/ŝ(ε(m+k)) has no finite bound", dy=0,
               anchor="middle", size=12.5, italic=True)
    return f


# ------------------------------------------------------------------ figure 2
def fig_regularity(theme):
    rec = load("recorded.json")
    sig = rec["sobolev_sigma"]["value"]
    rho = rec["pointwise_rho"]["value"]
    Ks = sorted(int(k) for k in sig)
    f = Fig(940, 470, theme, title="Regularity of the Daubechies scaling function, and the thresholds that use it",
            xlabel="Daubechies order K", ylabel="exponent")
    f.line(Ks, [sig[str(K)] for K in Ks], 0, width=2.2, label="σ_K  (Sobolev, for ℓ² sums)")
    f.points(Ks, [sig[str(K)] for K in Ks], 0, size=3.8)
    rk = sorted(int(k) for k in rho)
    f.line(rk, [rho[str(K)] for K in rk], 1, width=1.8, dash="5 3",
           label="ρ  (pointwise, recorded)")
    f.points(rk, [rho[str(K)] for K in rk], 1, size=3.4)
    for thr, minK, lab in ((1.0, 3, "σ > 1  →  K ≥ 3"),
                           (1.5, 4, "σ > 3/2  →  K ≥ 4"),
                           (2.5, 7, "σ > 5/2  →  K ≥ 7"),
                           (3.0, 9, "σ > 3  →  K ≥ 9")):
        f.hline(thr, color="mute", dash="2 4", width=1.0)
        f.annotate(12.0, thr, lab, dx=-4, dy=-6, anchor="end", size=12, color=2)
        f.points([minK], [thr], 2, size=4.6, marker="s")
    f.xlim(1.6, 12.6)
    f.ylim(0.6, 4.1)
    f.xticks(Ks)
    return f


# ------------------------------------------------------------------ figure 3
def fig_rates(theme):
    rec = load("recorded.json")["momentum_cutoff_opnorm"]
    f = Fig(940, 470, theme, title="Momentum-cutoff route: the sharp rate ε_N^min{δ,2}",
            xlabel="scale N", ylabel="‖ℓ~(N) − ℓ‖ on h^{1+δ} → h^0")
    for i, d in enumerate(("0", "0.5", "1", "2", "3")):
        e = rec["by_delta"][d]
        f.line(e["N"], e["value"], i, width=2.0,
               label="δ = %s   rate %.2f  (predicted %.1f)"
                     % (d, np.mean(e["rates"][-2:]), e["predicted"]))
        f.points(e["N"], e["value"], i, size=3.4)
    f.ylog(2)
    f.xticks([4, 5, 6, 7, 8])
    f.legend_at("bl")
    return f


# ------------------------------------------------------------------ figure 4
def fig_support(theme):
    f = Fig(940, 470, theme, title="Asymmetry of the scaling function: support [0, 2K−1] and centre of mass μ(s)",
            xlabel="x", ylabel="s(x) for order K  (offset per order)")
    offs = {2: 0.0, 4: -1.6, 10: -3.2}
    for i, K in enumerate((2, 4, 10)):
        x, s = scaling_function(K, J=9)
        mu = centre_of_mass(daubechies(K))
        tx, ty = thin(x, s + offs[K])
        f.line(tx, ty, i, width=1.8, label="db%d,  μ = %.2f of %d" % (K, mu, 2 * K - 1))
        f.hline(offs[K], color="mute", dash="1 5", width=0.8)
        f.points([mu], [offs[K]], i, size=5.2, marker="s")
        f.annotate(mu, offs[K], "μ", dx=0, dy=16, color=i, size=13)
    f.xlim(-0.6, 19.6)
    f.ylim(-3.95, 1.55)
    f.yticks([])
    f.legend_at("tr")
    f.annotate(11.6, 0.18, "the centre of mass sits at 79% of the support at K = 2,",
               dy=0, anchor="middle", size=12.5, italic=True)
    f.annotate(11.6, 0.18, "rising to 89% at K = 12, so re-centring by ε_N μ(s) shifts by",
               dy=17, anchor="middle", size=12.5, italic=True)
    f.annotate(11.6, 0.18, "the same order as the light cone ε_N(2K−1)",
               dy=34, anchor="middle", size=12.5, italic=True)
    return f


# ------------------------------------------------------------------ figure 5
def fig_budget(theme):
    v = load("recorded.json")["vacuum_deviation"]
    nm = [n - v["M"] for n in v["N"]]
    f = Fig(940, 470, theme, title="The ground state is the bottleneck, and chirality squares it",
            xlabel="N − M", ylabel="η_M(N),  vacuum-symbol deviation")
    f.line(nm, v["full"], 1, width=2.2, label="full two-component algebra   order %.2f" % np.mean(v["rates_full"][-3:]))
    f.points(nm, v["full"], 1, size=3.6)
    f.line(nm, v["chiral"], 2, width=2.2, label="chiral subalgebra   order %.2f" % np.mean(v["rates_chiral"][-3:]))
    f.points(nm, v["chiral"], 2, size=3.6)
    f.ylog(2)
    f.xticks(nm)
    f.legend_at("tr")
    f.annotate(nm[len(nm) // 2], v["full"][len(nm) // 2], "|sin(π 2^-(N-M)/4)|",
               dx=8, dy=-10, anchor="start", color=1, size=12.5)
    f.annotate(nm[len(nm) // 2], v["chiral"][len(nm) // 2], "its square",
               dx=8, dy=14, anchor="start", color=2, size=12.5)
    return f


# ------------------------------------------------------------------ figure 6
def fig_multiplicity(theme):
    N = 3
    m = 2 ** (N + 1)
    Ms = list(range(1, 8))
    f = Fig(940, 470, theme, title="GNS multiplicity: constant at every finite scale, collapsing only in the limit",
            xlabel="renormalization step M", ylabel="m(S),  eigenvalues strictly between 0 and 1")
    # chiral, wavelet: constant all the way into the limit
    f.line(Ms + [8], [m] * 8, 2, width=3.4)
    f.points([8], [m], 2, size=5.4)
    # chiral, momentum cutoff: the same until the limit, then it collapses
    f.line(Ms, [m] * 7, 1, width=2.0, dash="7 4")
    f.line([7, 8], [m, 0], 1, width=2.0, dash="7 4")
    f.points([8], [0], 1, size=5.4)
    # full algebra: pure throughout, either route
    f.line(Ms + [8], [0] * 8, 0, width=2.4)
    f.points([8], [0], 0, size=3.4)
    f.vline(7.5, color="mute", dash="3 4", width=1.1)
    f.xlim(0.4, 8.9)
    f.ylim(-2.2, m * 1.30)
    f.xticks(Ms + [8], [str(x) for x in Ms] + ["\u221e"])
    f.annotate(4.4, m + 0.9, "chiral, wavelet route  —  reaches the limit",
               dy=0, anchor="middle", color=2, size=13)
    f.annotate(5.45, m * 0.62, "chiral, momentum cutoff:", dy=0, anchor="end", color=1, size=13)
    f.annotate(5.45, m * 0.62, "collapses by a factor 2^|Γ|, and only here",
               dy=17, anchor="end", color=1, size=13)
    f.annotate(4.4, 1.05, "full algebra, either route  —  pure throughout",
               dy=0, anchor="middle", color=0, size=13)
    f.annotate(3.2, m * 1.19, "N = 3, so |Γ_{N,-}| = %d;  the connecting unitaries exist at every finite M" % m,
               dy=0, anchor="middle", size=12.5, italic=True)
    return f


FIGURES = [
    ("shat-zeros", fig_shat_zeros),
    ("regularity-ladder", fig_regularity),
    ("momentum-cutoff-rates", fig_rates),
    ("scaling-function-support", fig_support),
    ("simulation-budget", fig_budget),
    ("multiplicity", fig_multiplicity),
]


def selfcheck():
    """The refinement iteration must give unit mass, the right support, and the centre of
    mass that the filter predicts."""
    worst_mass = worst_mu = 0.0
    for K in (2, 4, 10):
        x, s = scaling_function(K, J=9)
        step = x[1] - x[0]
        worst_mass = max(worst_mass, abs(np.sum(s) * step - 1.0))
        worst_mu = max(worst_mu, abs(np.sum(x * s) * step - centre_of_mass(daubechies(K))))
        assert abs(x[-1] - (2 * K - 1)) < 1e-12, "support is not [0, 2K-1]"
    print("  scaling function: |mass - 1| %.1e, |mu - centre_of_mass| %.1e" % (worst_mass, worst_mu))
    if worst_mass > 1e-9 or worst_mu > 1e-9:
        raise SystemExit("scaling-function selfcheck failed")


def main():
    os.makedirs(FIGDIR, exist_ok=True)
    selfcheck()
    for stem, build in FIGURES:
        paths = figure_pair(build, stem, FIGDIR)
        print("  %-26s %s" % (stem, " ".join(os.path.basename(p) for p in paths)))
    print("  %d figures, %d files" % (len(FIGURES), 2 * len(FIGURES)))


if __name__ == "__main__":
    main()
