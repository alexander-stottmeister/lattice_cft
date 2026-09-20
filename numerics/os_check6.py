"""
Part 6: rates for the division-free error estimate, to make sure the revised
Section 4.2.4 states the truth.

  Sigma_N := sum_m |f^{(N)}_k(M,m) - f_k(M,m)|^2
  predicted:  k=0  ->  O(eps_N^4)  (Taylor)      provided K - Kbar > 2 + delta
              k!=0 ->  O(eps_N^2)  (shat-shift)  provided K - Kbar > 2 + delta
  otherwise the tail |m| ~ 1/eps_N dominates and the rate is regularity-limited.
"""
import numpy as np, sys
sys.path.insert(0, '.')
from os_check4 import daubechies, m0 as m0f, shat as shatf

PI = np.pi

def make(h):
    def m0(x): return m0f(np.asarray(x, float), h)
    def shat(x):
        x = np.asarray(x, float)
        J = int(np.ceil(np.log2(max(np.max(np.abs(x)), 1.0)))) + 32
        o = np.ones(x.shape, complex)
        for j in range(1, J+1): o = o*m0(x*2.0**(-j))
        return o
    def prod(x, J):
        x = np.asarray(x, float); o = np.ones(x.shape, complex)
        for j in range(1, J+1): o = o*m0(x*2.0**(-j))
        return o
    return m0, shat, prod

def sigma(K, k, M, N, halfint=True, pad=3):
    h = daubechies(K); _, shat, prod = make(h)
    epsN, epsM = 2.0**(-N)*PI, 2.0**(-M)*PI
    m = np.arange(-2**(N+pad), 2**(N+pad)) + (0.5 if halfint else 0.0)
    fN = shat(epsN*m)*np.cos(0.25*epsN*k)**2*np.sin(epsN*(m+0.5*k))/epsN*prod(epsM*(m+k), N-M)
    fL = shat(epsM*(m+k))*(m+0.5*k)
    return float(np.sum(np.abs(fN-fL)**2))

print("="*92)
print("[14] rate of  Sigma_N = sum_m |f^(N)_k - f_k|^2   (division-free form), M=2")
print("     'rate' = -log2(Sigma_{N+1}/Sigma_N);  Taylor prediction: 4 for k=0, 2 for k!=0")
print("="*92)
for K in (4, 8, 10):
    for k in (0.0, 2.0):
        vals = []
        for N in range(6, 13):
            vals.append(sigma(K, k, 2, N))
        rates = [-np.log2(vals[i+1]/vals[i]) for i in range(len(vals)-1)]
        print(f"  db{K:2d}  k={k:g}:  Sigma_N = " + " ".join(f"{v:.2e}" for v in vals))
        print(f"            rates   = " + "   ".join(f"{r:5.2f}" for r in rates)
              + f"      (K-Kbar needed > 2+delta; predicted {4.0 if k==0 else 2.0:.0f})")
