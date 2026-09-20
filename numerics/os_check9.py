"""
Part 9: structure of Lemma 3.16.  Claim: the renormalised symbols are CONVEX
combinations over aliasing classes,
    Shat^{(N)}_M(l) = sum_{k = l} w_M(k) S^{(N+M)}(k),   sum_{k = l} w_M(k) = 1,
with w_M(k) = |prod_{m=1..M} m0(eps_{N+m} k)|^2  and  w_inf(k) = |shat(eps_N k)|^2.
If so, no decay estimate on shat is needed anywhere -- the weights are probabilities.
"""
import numpy as np, sys
sys.path.insert(0, '.')
from os_check4 import daubechies, m0 as m0f

PI = np.pi
def shat(x, h):
    x = np.asarray(x, float)
    J = int(np.ceil(np.log2(max(np.max(np.abs(x)), 1.0)))) + 34
    o = np.ones(x.shape, complex)
    for j in range(1, J+1): o = o*m0f(x*2.0**(-j), h)
    return o

print("="*88)
print("[19] alias weights are probability weights (L = pi, so Gamma_N = Z_{2L_N}-classes)")
print("="*88)
for K in (1, 2, 4, 8):                      # K=1 is Haar: no regularity at all
    h = daubechies(K) if K > 1 else np.array([1/np.sqrt(2), 1/np.sqrt(2)])
    for N in (2, 4):
        epsN = 2.0**(-N)*PI
        # infinite-scale weights: class of l is  l + (2 pi / epsN) Z
        errs_inf, errs_fin = [], []
        for l in (np.arange(-2**N, 2**N) + 0.5):
            n = np.arange(-4000, 4001)
            w = np.abs(shat(epsN*l + 2*PI*n, h))**2
            errs_inf.append(abs(w.sum() - 1.0))
            for M in (1, 3, 6):
                kk = l + (2*PI/epsN)*np.arange(0, 2**M)     # 2^M aliases inside Gamma_{N+M}
                wf = np.ones_like(kk)
                for m in range(1, M+1):
                    wf = wf*np.abs(m0f(2.0**(-(N+m))*PI*kk, h))**2
                errs_fin.append(abs(wf.sum() - 1.0))
        print(f"  K={K} N={N}: max|sum_inf w - 1| = {max(errs_inf):.2e}   "
              f"max|sum_fin w - 1| = {max(errs_fin):.2e}")
