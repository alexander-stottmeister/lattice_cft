"""
Part 7: what is the O(eps_N) obstruction at k != 0 ?

Conjecture: shat(eps_N m)/shat(eps_N(m+k)) = e^{+i m_1 eps_N k}(1 + O(eps_N^2)),
where m_1 = int x s(x) dx = (1/sqrt2) sum_n n h_n is the first moment (centre of mass)
of the scaling function.  I.e. the first-order error is a PURE PHASE = a translation by
the offset between the lattice origin and the centre of mass of s^{(eps_N)}.
If so, re-centring restores the O(eps_N^2) rate at k != 0.
"""
import numpy as np, sys
sys.path.insert(0, '.')
from os_check4 import daubechies, m0 as m0f

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

def first_moment(h):
    return float(np.sum(np.arange(len(h))*np.asarray(h))/np.sqrt(2.0))

def sigma(K, k, M, N, phase=False, pad=3):
    h = daubechies(K); shat, prod = make(h)
    m1 = first_moment(h)
    epsN, epsM = 2.0**(-N)*PI, 2.0**(-M)*PI
    m = np.arange(-2**(N+pad), 2**(N+pad)) + 0.5
    fN = shat(epsN*m)*np.cos(0.25*epsN*k)**2*np.sin(epsN*(m+0.5*k))/epsN*prod(epsM*(m+k), N-M)
    if phase:
        fN = fN*np.exp(-1j*m1*epsN*k)          # undo the centre-of-mass translation
    fL = shat(epsM*(m+k))*(m+0.5*k)
    return float(np.sum(np.abs(fN-fL)**2))

print("="*94)
print("[15] first moment m_1 = int x s(x) dx of the Daubechies scaling function")
print("="*94)
for K in (2, 4, 8, 10):
    h = daubechies(K)
    print(f"  db{K:2d}: supp = [0,{2*K-1}],  m_1 = {first_moment(h):.6f}")

print()
print("="*94)
print("[16] rate of Sigma_N at k != 0, with and without the phase e^{-i m_1 eps_N k}")
print("="*94)
for K in (8, 10):
    for k in (2.0, 4.0):
        for phase in (False, True):
            vals = [sigma(K, k, 2, N, phase=phase) for N in range(6, 13)]
            rates = [-np.log2(vals[i+1]/vals[i]) for i in range(len(vals)-1)]
            tag = "re-centred" if phase else "as in [OS]"
            print(f"  db{K:2d} k={k:g} {tag:11s}: Sigma_N = " + " ".join(f"{v:.2e}" for v in vals))
            print(f"  {'':22s}  rates   = " + "   ".join(f"{r:5.2f}" for r in rates))
        print()
