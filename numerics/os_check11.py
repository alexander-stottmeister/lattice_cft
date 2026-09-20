"""
Part 11: Lemma 4.6 / Theorem 4.7 -- operator norms in the Sobolev scale.
L = pi, chiral '+', Gamma_{inf,-} = Z+1/2.  Normalised Fourier coordinates, so that
R_{m,l} = shat(eps_N m) [m ~ l]  is an isometry  h_N -> h_inf.
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

def build(K, N, k, pad=3, recentre=False):
    h = daubechies(K); eps = 2.0**(-N)*PI; LN = 2**N          # |Gamma_N| = 2 L_N = 2^{N+1}
    m = np.arange(-2**(N+pad), 2**(N+pad)) + 0.5              # Gamma_inf (truncated)
    l = np.arange(-LN, LN) + 0.5                              # Gamma_N
    nl = len(l); per = 2*PI/eps                               # = 2 L_N  (since L = pi)
    # alias map: index of l-class of each m
    cls = np.rint((m - l[0])/1.0).astype(int) % nl
    R = np.zeros((len(m), nl), complex)
    R[np.arange(len(m)), cls] = shat(eps*m, h)
    # ell^{(N)} on Gamma_N (periodic wrap), symbol sigma(l) = cos(eps k/4)^2 sin(eps(l-k/2))/eps
    sig = np.cos(0.25*eps*k)**2*np.sin(eps*(l - 0.5*k))/eps
    sh = int(round(k))                                        # e_l -> e_{l-k}
    lN = np.zeros((nl, nl), complex)
    for i in range(nl):
        lN[(i - sh) % nl, i] = sig[i]
    A = R @ lN @ R.conj().T
    if recentre:
        mu = float(np.sum(np.arange(len(h))*np.asarray(h))/np.sqrt(2.0))
        A = A*np.exp(-1j*mu*eps*k)
    B = np.zeros((len(m), len(m)), complex)                   # ell:  (ell u)(m) = (m+k/2) u(m+k)
    pos = {v: i for i, v in enumerate(m)}
    for i, mm in enumerate(m):
        if mm + k in pos: B[i, pos[mm + k]] = mm + 0.5*k
    return m, A - B

def opnorm(K, N, k, delta, pad=3, recentre=False):
    m, D = build(K, N, k, pad, recentre)
    return np.linalg.norm(D/((1.0 + np.abs(m))**(1.0+delta))[None, :], 2)

print("="*92)
print("[23] ||elltilde^(N)_{+,k} - ell_{+,k}||_{h^{1+delta} -> h^0}   (db4, k=2, L=pi)")
print("="*92)
for delta in (0.0, 0.5, 1.0, 1.5):
    v = [opnorm(4, N, 2.0, delta) for N in (3, 4, 5, 6, 7)]
    r = [-np.log2(v[i+1]/v[i]) for i in range(len(v)-1)]
    print(f"  delta={delta:3.1f}: " + " ".join(f"{x:.4e}" for x in v)
          + "  rates: " + " ".join(f"{x:5.2f}" for x in r) + f"   (predicted {min(delta,1.0):.1f})")
print("\n  with the centre-of-mass phase removed (predicted min(delta,2)):")
for delta in (1.0, 1.5, 2.5):
    v = [opnorm(4, N, 2.0, delta, recentre=True) for N in (3, 4, 5, 6, 7)]
    r = [-np.log2(v[i+1]/v[i]) for i in range(len(v)-1)]
    print(f"  delta={delta:3.1f}: " + " ".join(f"{x:.4e}" for x in v)
          + "  rates: " + " ".join(f"{x:5.2f}" for x in r) + f"   (predicted {min(delta,2.0):.1f})")
print("\n[24] uniform h^1 -> h^0 bound  sup_N ||elltilde^(N)||  (must stay bounded)")
for K in (4, 8):
    row = []
    for N in (3, 4, 5, 6, 7):
        m, _ = build(K, N, 2.0)
        h = daubechies(K); eps = 2.0**(-N)*PI; LN = 2**N
        l = np.arange(-LN, LN) + 0.5; nl = len(l)
        cls = np.rint((m - l[0])).astype(int) % nl
        R = np.zeros((len(m), nl), complex); R[np.arange(len(m)), cls] = shat(eps*m, h)
        sig = np.cos(0.25*eps*2.0)**2*np.sin(eps*(l - 1.0))/eps
        lN = np.zeros((nl, nl), complex)
        for i in range(nl): lN[(i-2) % nl, i] = sig[i]
        A = R @ lN @ R.conj().T
        row.append(np.linalg.norm(A/((1.0+np.abs(m)))[None, :], 2))
    print(f"  db{K}: " + " ".join(f"{x:.4f}" for x in row))
