"""
Part 15: the smeared case (Lemma 4.19 / Theorem 4.20).

Exact identity for the smearing weights:  with w^(N)_k = prod_{j<=N-M} m0(eps_{M+j} k)
and w^(inf)_k = shat(eps_M k),  the scaling relation gives
      w^(N)_k - w^(inf)_k = w^(N)_k (1 - shat(eps_N k)),
so the smearing error is governed by |1 - shat(eps_N k)| -- FIRST order, and again the
centre-of-mass phase:  1 - shat(xi) = i mu(s) xi + O(xi^2).
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
def mu(h): return float(np.sum(np.arange(len(h))*np.asarray(h))/np.sqrt(2.0))

print("="*84)
print("[32] the smearing weight error  |1 - shat(eps_N k)|,  raw vs re-centred")
print("="*84)
for K in (4, 8):
    h = daubechies(K); m1 = mu(h)
    k = 2.0
    raw, rec = [], []
    for N in range(4, 12):
        xi = 2.0**(-N)*PI*k
        raw.append(abs(1.0 - shat(np.array([xi]), h)[0]))
        rec.append(abs(1.0 - np.exp(1j*m1*xi)*shat(np.array([xi]), h)[0]))
    rr = [-np.log2(raw[i+1]/raw[i]) for i in range(len(raw)-1)]
    rc = [-np.log2(rec[i+1]/rec[i]) for i in range(len(rec)-1)]
    print(f"  db{K}  (mu = {m1:.4f}):")
    print("    raw       : " + " ".join(f"{x:.2e}" for x in raw))
    print("    order     : " + "  ".join(f"{x:.2f}" for x in rr) + "   (predicted 1)")
    print("    re-centred: " + " ".join(f"{x:.2e}" for x in rec))
    print("    order     : " + "  ".join(f"{x:.2f}" for x in rc) + "   (predicted 2)")

print()
print("="*84)
print("[33] smeared operator norm ||elltilde^(N)(S^M_N X) - ell(S^M_inf X)||_{h^{1+delta} -> h^0}")
print("     L = pi, chiral '+', M = 2, X = delta at one lattice site (so Xhat_per == 1)")
print("="*84)
def smeared_opnorm(K, N, M, delta, recentre=False, pad=3):
    h = daubechies(K); m1 = mu(h)
    epsN = 2.0**(-N)*PI; epsM = 2.0**(-M)*PI
    n = np.arange(-2**(N+pad), 2**(N+pad)) + 0.5
    pos = {v: i for i, v in enumerate(n)}
    d = len(n); D = np.zeros((d, d), complex)
    kk = np.arange(-2**N, 2**N)*1.0                     # Gamma_{N,+} = Z, |k| < pi/epsN
    wN = np.ones_like(kk, dtype=complex)
    for j in range(1, N-M+1): wN = wN*m0f(2.0**(-(M+j))*PI*kk, h)
    wI = shat(epsM*kk, h)
    if recentre: wN = wN*np.exp(-1j*m1*epsN*kk)
    for a, k in enumerate(kk):
        if abs(wN[a]) < 1e-14 and abs(wI[a]) < 1e-14: continue
        for i, v in enumerate(n):                        # ell_{+,k}: e_v -> (v-k/2) e_{v-k}
            tgt = v - k
            if tgt not in pos: continue
            symN = (np.cos(0.25*epsN*k)**2*np.sin(epsN*(v-0.5*k))/epsN
                    if (abs(v) < 2**N and abs(tgt) < 2**N) else 0.0)
            D[pos[tgt], i] += (wN[a]*symN - wI[a]*(v-0.5*k))/(2*2**M)
    return np.linalg.norm(D/((1.0+np.abs(n))**(1.0+delta))[None, :], 2)

for recentre in (False, True):
    tag = "re-centred" if recentre else "as in [OS]"
    for delta in (1.0, 2.0):
        v = [smeared_opnorm(8, N, 2, delta, recentre) for N in (4, 5, 6, 7)]
        r = [-np.log2(v[i+1]/v[i]) for i in range(len(v)-1)]
        pred = min(delta, 2.0) if recentre else min(delta, 1.0)
        print(f"  db8 {tag:11s} delta={delta:3.1f}: " + " ".join(f"{x:.3e}" for x in v)
              + "  rates: " + " ".join(f"{x:5.2f}" for x in r) + f"   (predicted {pred:.1f})")

print()
print("="*84)
print("[34] why: orthonormality + the order-K zero of m0 at pi force  |shat(xi)| = 1 + O(xi^{2K})")
print("     so the whole smearing error is a PHASE, cubic after re-centring")
print("="*84)
for K in (2, 4, 8):
    h = daubechies(K)
    d = np.array([1e-1, 1e-2, 1e-3])
    v = np.abs(1.0 - np.abs(shat(d, h)))
    p = np.log(v[0]/v[-1])/np.log(d[0]/d[-1])
    q = np.abs(1.0 - np.abs(m0f(d, h)))
    pq = np.log(q[0]/q[-1])/np.log(d[0]/d[-1])
    print(f"  db{K}: 1-|m0(xi)| ~ xi^{pq:.2f},   1-|shat(xi)| ~ xi^{p:.2f}   (both predicted 2K = {2*K})")
