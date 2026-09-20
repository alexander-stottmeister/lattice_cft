"""
Part 2: does the *conclusion* of Lemma 4.5 survive the broken domination step,
and what happens to the error estimates (204)-(210)?
"""
import numpy as np
from os_check import DB, m0, shat, prod_m0

PI = np.pi

def f_N(m, k, M, N, h):
    """f_k^{(N)}(M,m) written WITHOUT the singular ratio:
         shat(eps_N m) cos(eps_N k/4)^2 sin(eps_N(m+k/2))/eps_N * prod_{j=1}^{N-M} m0(eps_{M+j}(m+k))
       (identical to the paper's expression wherever shat(eps_N(m+k)) != 0)."""
    epsN = 2.0**(-N)*PI; epsM = 2.0**(-M)*PI
    m = np.asarray(m, dtype=float)
    pref = shat(epsN*m, h) * np.cos(0.25*epsN*k)**2 * np.sin(epsN*(m+0.5*k))/epsN
    # prod_{j=1..N-M} m0(eps_{M+j}(m+k)) = prod_{j} m0(2^{-j} * eps_M (m+k))
    return pref * prod_m0(epsM*(m+k), h, 1, N-M)

def f_lim(m, k, M, h):
    epsM = 2.0**(-M)*PI
    m = np.asarray(m, dtype=float)
    return shat(epsM*(m+k), h)*(m+0.5*k)

def f_N_paper(m, k, M, N, h):
    """the paper's own expression, with the ratio, for cross-checking."""
    epsN = 2.0**(-N)*PI; epsM = 2.0**(-M)*PI
    m = np.asarray(m, dtype=float)
    return (shat(epsM*(m+k), h)*np.cos(0.25*epsN*k)**2
            * np.sin(epsN*(m+0.5*k))/epsN
            * shat(epsN*m, h)/shat(epsN*(m+k), h))

K = 4; h = DB[K]; M = 2

print("="*78)
print("[3] the two expressions for f^{(N)} agree away from the zeros (cross-check)")
print("="*78)
mm = np.arange(-40, 41) + 0.5
a = f_N(mm, 2.0, M, 8, h); b = f_N_paper(mm, 2.0, M, 8, h)
print(f"  db4, M=2, N=8, k=2, m in Gamma_-, |m|<40:  max|f_prod - f_ratio| = {np.max(np.abs(a-b)):.2e}"
      f"   (scale max|f| = {np.max(np.abs(a)):.2e})")

print(); print("="*78)
print("[4] the claimed dominating function g_k(M,m) = C_k |(m+k/2) shat(eps_M(m+k))|")
print("    FAILS: at m+k = 2^{N+1} n (Ramond) the bound is 0 but |f^{(N)}| > 0")
print("="*78)
for N in (6, 8, 10, 12):
    for n in (1, 2):
        for k in (1.0, 2.0):
            m = np.array([2.0**(N+1)*n - k])
            fn  = abs(f_N(m, k, M, N, h)[0])
            fl  = abs(f_lim(m, k, M, h)[0])
            rr = "INF" if fl < 1e-25 else f"{fn/fl:.0e}"
            print(f"  N={N:2d} n={n} k={k:g}: m={m[0]:9.0f}   |f^(N)| = {fn:.6e}   "
                  f"g_k/C_k = |f_k| = {fl:.2e}   |f^(N)|/|f_k| = {rr}")

print(); print("="*78)
print("[5] ... but the CONCLUSION of Lemma 4.5 still holds: sum_m |f^{(N)}-f_k|^2 -> 0")
print("="*78)
for k in (1.0, 2.0, 4.0):
    print(f"  k = {k:g}:")
    prev = None
    for N in range(4, 15):
        m = np.arange(-2**(N+3), 2**(N+3)) + 0.5      # Neveu-Schwarz
        d = f_N(m, k, M, N, h) - f_lim(m, k, M, h)
        s = float(np.sum(np.abs(d)**2))
        rate = "" if prev is None else f"  (x {s/prev:.3f})"
        print(f"    N={N:2d}: sum_m |f^(N)-f_k|^2 = {s:.6e}{rate}")
        prev = s

print(); print("="*78)
print("[6] resonance spikes: |f^{(N)}| at m+k = 2^{N+1} n decays like eps_N^{K-1}")
print("    (this is *why* Lemma 4.5 survives -- and it needs K >= 2, not just 'sufficiently regular')")
print("="*78)
for Kd in (2, 3, 4):
    hh = DB[Kd]; vals = []
    for N in range(6, 14):
        m = np.array([2.0**(N+1)*1 - 2.0])
        vals.append(abs(f_N(m, 2.0, M, N, hh)[0]))
    sl = np.polyfit(np.arange(6,14)*np.log(2.0), np.log(np.array(vals)), 1)[0]
    print(f"  db{Kd}: |f^(N)|(resonance) ~ 2^(-p N) with p = {-sl:.3f}   (K-1 = {Kd-1})")

print(); print("="*78)
print("[7] Error^2(delta,L,k,N) as DEFINED in (206) -- sup over m in Gamma_inf of a ratio")
print("="*78)
delta = 2.0; L = PI
for N in (6, 8, 10):
    for k in (0.0, 1.0, 2.0):
        # Ramond sector: m in Z
        m = np.arange(-2**(N+2), 2**(N+2)+1).astype(float)
        epsN = 2.0**(-N)*PI; LN = L/epsN
        num = shat(epsN*m, h); den = shat(epsN*(m+k), h)
        with np.errstate(divide='ignore', invalid='ignore'):
            ratio = np.abs(num)/np.abs(den)
        inner = np.cos(0.25*epsN*k)**2*np.sinc((epsN*(m+0.5*k))/PI)*ratio - 1.0
        err2 = (1.0+abs(m+0.5*k))**(-2*delta)*np.abs(inner)**2
        bad = np.sum(~np.isfinite(err2)) + np.sum(err2 > 1e20)
        top = np.nanmax(err2[np.isfinite(err2)]) if np.any(np.isfinite(err2)) else np.inf
        print(f"  N={N:2d} k={k:g} (Ramond): #divergent m = {bad:3d};  "
              f"sup over finite m = {top:.3e}   ->  Error^2 = "
              f"{'+INF' if bad>0 else f'{2*PI/L*top:.3e}'}")
