"""
Part 8: the region decomposition behind the rigorous k != 0 estimate.

Region (a): |m+k| <= pi/eps_N   (N-th Brillouin zone)  -- Lemma 3.7 applies directly.
Region (b): |m+k| >  pi/eps_N                          -- P_J only repeats periodically;
            the decay must come from shat(eps_N m) sitting near a zero of shat.

Claim (uniform majorant):  for all N > M and all m,
   |shat(eps_N m)| * P_{N-M}(eps_M(m+k))  <=  C * (1 + eps_M|m+k|)^{-rho},   rho = K - Kbar,
with C independent of N.  Test the sharpest form of this: the ratio B/T in region (b).
"""
import numpy as np, sys
sys.path.insert(0, '.')
from os_check4 import daubechies, m0 as m0f, sobolev_exponent

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
    return shat, prod

print("="*94)
print("[17] region (b): is  |shat(eps_N m)| P_{N-M}(eps_M(m+k))  <=  C (1+eps_M|m+k|)^{-rho} ?")
print("     reported: sup over region (b) of  LHS / (1+eps_M|m+k|)^{-rho}   (must stay bounded in N)")
print("="*94)
M = 2
for K in (4, 8):
    h = daubechies(K); shat, prod = make(h)
    rho = sobolev_exponent(h)[1] - 0.5          # use the sup-envelope-ish exponent K-Kbar ~ sigma
    epsM = 2.0**(-M)*PI
    print(f"  db{K}  (using rho = {rho:.3f}):")
    for k in (1.0, 2.0, 4.0):
        row = []
        for N in range(M+2, M+13):
            epsN = 2.0**(-N)*PI
            m = np.arange(-2**(N+3), 2**(N+3)) + 0.5
            mk = m + k
            sel = np.abs(mk) > PI/epsN            # region (b)
            m_b, mk_b = m[sel], mk[sel]
            lhs = np.abs(shat(epsN*m_b))*np.abs(prod(epsM*mk_b, N-M))
            tgt = (1.0 + epsM*np.abs(mk_b))**(-rho)
            row.append(np.max(lhs/tgt))
        print(f"    k={k:g}: " + "  ".join(f"{v:.3f}" for v in row))

print()
print("="*94)
print("[18] Brillouin-zone part vs. tail part of  Sigma_N = sum_m |f^(N)_k - f_k|^2")
print("     predicted tail rate: 2*sigma_K - 2;   predicted BZ rate: 4 (k=0), 2 (k!=0)")
print("="*94)
for K in (4, 8, 10):
    h = daubechies(K); shat, prod = make(h)
    sig = sobolev_exponent(h)[0]
    epsM = 2.0**(-M)*PI
    print(f"  db{K}  (sigma_K = {sig:.3f}, predicted tail rate 2*sigma-2 = {2*sig-2:.2f}):")
    for k in (0.0, 2.0):
        bz, tl = [], []
        for N in range(6, 14):
            epsN = 2.0**(-N)*PI
            m = np.arange(-2**(N+4), 2**(N+4)) + 0.5
            mk = m + k
            fN = shat(epsN*m)*np.cos(0.25*epsN*k)**2*np.sin(epsN*(m+0.5*k))/epsN*prod(epsM*mk, N-M)
            fL = shat(epsM*mk)*(m+0.5*k)
            d2 = np.abs(fN-fL)**2
            inb = np.abs(mk) <= PI/epsN
            bz.append(float(d2[inb].sum())); tl.append(float(d2[~inb].sum()))
        rb = [-np.log2(bz[i+1]/bz[i]) for i in range(len(bz)-1)]
        rt = [-np.log2(tl[i+1]/tl[i]) for i in range(len(tl)-1)]
        print(f"    k={k:g}  BZ  : " + " ".join(f"{v:.2e}" for v in bz))
        print(f"          rates: " + "  ".join(f"{v:5.2f}" for v in rb))
        print(f"    k={k:g}  tail: " + " ".join(f"{v:.2e}" for v in tl))
        print(f"          rates: " + "  ".join(f"{v:5.2f}" for v in rt))
