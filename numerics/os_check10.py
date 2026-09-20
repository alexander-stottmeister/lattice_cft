"""
Part 10: Corollary 3.17 (scaling limit of the lattice vacua).

(a) massless symbol deviation is EXACTLY |sin(eps_N k / 4)|
(b) the zero mode in the Ramond sector is alias-free: w_inf(0)=1, w_inf(other aliases)=0,
    so a discrepancy at k=0 is NOT averaged away
(c) resulting rate for delta_M(N): O(2^-M), uniform in N
"""
import numpy as np, sys
sys.path.insert(0, '.')
from os_check4 import daubechies, m0 as m0f
PI = np.pi
sx = np.array([[0,1],[1,0]], complex); sy = np.array([[0,-1j],[1j,0]]); sz = np.diag([1,-1]).astype(complex)

def shat(x, h):
    x = np.asarray(x, float)
    J = int(np.ceil(np.log2(max(np.max(np.abs(x)), 1.0)))) + 34
    o = np.ones(x.shape, complex)
    for j in range(1, J+1): o = o*m0f(x*2.0**(-j), h)
    return o

def Pplus_massless(k, eps):                       # eq. (60), sign(0)=0
    s = np.sign(k)
    return 0.5*(np.eye(2) + s*(-np.sin(0.5*eps*k)*sx + np.cos(0.5*eps*k)*sy))
def Pplus_cont(k):                                # eq. (118)
    return 0.5*(np.eye(2) + np.sign(k)*sy)

print("="*86); print("[20] (a) massless symbol deviation"); print("="*86)
err = 0.0
for N in (3, 6, 9):
    eps = 2.0**(-N)*PI
    for k in (0.5, 1.5, 7.5, 100.5, -3.5):
        D = (np.eye(2)-Pplus_massless(k, eps)) - (np.eye(2)-Pplus_cont(k))
        err = max(err, abs(np.linalg.norm(D, 2) - abs(np.sin(0.25*eps*k))))
print(f"  max | ||S^(N)(k)-S(k)||  -  |sin(eps_N k/4)| |  = {err:.2e}   (claim: exact)")

print(); print("="*86); print("[21] (b) the k=0 aliasing class carries all its weight at k=0"); print("="*86)
for K in (2, 4, 8):
    h = daubechies(K)
    for N in (3, 5):
        eps = 2.0**(-N)*PI
        n = np.arange(-2000, 2001)
        w = np.abs(shat(eps*0.0 + 2*PI*n, h))**2      # aliases of l=0
        print(f"  db{K} N={N}: w(0) = {w[len(n)//2]:.12f},  max_{{n!=0}} w = "
              f"{max(w[:len(n)//2].max(), w[len(n)//2+1:].max()):.2e},  sum = {w.sum():.12f}")

print(); print("="*86); print("[22] (c) rate of delta_M(N) for the massless lattice vacua"); print("="*86)
def delta(K, N, M, nmax=3000):
    h = daubechies(K); epsN = 2.0**(-N)*PI; epsNM = 2.0**(-(N+M))*PI
    out = 0.0
    for l in (np.arange(-2**N, 2**N) + 0.5):          # Neveu-Schwarz
        n = np.arange(-nmax, nmax+1)
        k = l + (2*PI/epsN)*n
        w_inf = np.abs(shat(epsN*k, h))**2
        kf = l + (2*PI/epsN)*np.arange(0, 2**M)       # aliases inside Gamma_{N+M}
        w_M = np.ones_like(kf)
        for m in range(1, M+1): w_M = w_M*np.abs(m0f(2.0**(-(N+m))*PI*kf, h))**2
        A = sum(w_M[i]*(np.eye(2)-Pplus_massless(kf[i], epsNM)) for i in range(len(kf)))
        B = sum(w_inf[i]*(np.eye(2)-Pplus_cont(k[i])) for i in range(len(k)))
        out = max(out, np.linalg.norm(A-B, 2))
    return out
for K in (4, 8):
    for N in (2, 3, 4):
        d = [delta(K, N, M) for M in (2, 3, 4, 5, 6)]
        r = [-np.log2(d[i+1]/d[i]) for i in range(len(d)-1)]
        print(f"  db{K} N={N}: delta_M = " + " ".join(f"{v:.3e}" for v in d)
              + "   rates: " + "  ".join(f"{v:.2f}" for v in r))
