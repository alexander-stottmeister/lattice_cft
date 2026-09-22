"""
Adversarial numerical checks on Osborne-Stottmeister 2023 (CMP 398, 219-289),
"Conformal field theory from lattice fermions", Section 4.2.4.

Conventions (matching the paper):
  L chosen = pi  =>  Gamma_{inf,+} = Z ,  Gamma_{inf,-} = Z + 1/2 ,  pi/L = 1
  eps_N = 2^{-N} L = 2^{-N} pi
  shat(xi) = prod_{j>=1} m0(2^{-j} xi),   m0(xi) = 2^{-1/2} sum_n h_n e^{-i n xi}
"""
import numpy as np

# ---------------------------------------------------------------- Daubechies
DB = {
 2: [0.48296291314469025, 0.83651630373746899, 0.22414386804185735,
     -0.12940952255092145],
 3: [0.33267055295095688, 0.80689150931333875, 0.45987750211933132,
     -0.13501102001039084, -0.085441273882241486, 0.035226291882100656],
 4: [0.23037781330885523, 0.71484657055254153, 0.63088076792959036,
     -0.027983769416983849, -0.18703481171888114, 0.030841381835986965,
     0.032883011666982945, -0.010597401784997278],
 6: [0.11154074335008017, 0.49462389039838539, 0.75113390802157753,
     0.31525035170924639, -0.22626469396516913, -0.12976686756709563,
     0.097501605587079362, 0.027522865530016288, -0.031582039318031156,
     0.00055384220116149, 0.0047772575110106514, -0.0010773010852955832],
}

def m0(xi, h):
    n = np.arange(len(h))
    xi = np.asarray(xi, dtype=float)
    return (np.exp(-1j*np.multiply.outer(xi, n)) @ np.asarray(h))/np.sqrt(2.0)

def shat(xi, h, J=90):
    """shat(xi) = prod_{j=1..J} m0(2^-j xi)."""
    xi = np.asarray(xi, dtype=float)
    out = np.ones(xi.shape, dtype=complex)
    for j in range(1, J+1):
        out = out*m0(xi*2.0**(-j), h)
    return out

def prod_m0(xi, h, jmin, jmax):
    """prod_{j=jmin..jmax} m0(2^-j xi)  (finite product, no division)."""
    xi = np.asarray(xi, dtype=float)
    out = np.ones(xi.shape, dtype=complex)
    for j in range(jmin, jmax+1):
        out = out*m0(xi*2.0**(-j), h)
    return out

def sanity(K):
    h = DB[K]
    err = max(abs(sum(h[n]*h[n+2*k] for n in range(len(h)-2*k)) - (1.0 if k==0 else 0.0))
              for k in range(len(h)//2))
    print(f"  db{K}: sum h = {sum(h):.10f} (sqrt2 = {np.sqrt(2):.10f}); "
          f"max|<h,h(.-2k)>-delta| = {err:.1e}; shat(0) = {shat(np.array([0.0]),h)[0].real:.10f}")
    zs = "  ".join(f"|shat(2pi*{n})|={abs(shat(np.array([2*np.pi*n]),h)[0]):.2e}" for n in (1,2,3,5))
    print(f"        {zs}")

print("="*78); print("[0] Daubechies filters: sanity"); print("="*78)
for K in (2,3,4,6): sanity(K)

# ------------------------------------------------------------------ [1] order of the zeros of shat at 2*pi*n
print(); print("="*78)
print("[1] shat has a zero of order K at 2*pi*n, n != 0  (=> ratio in Lemma 4.5 is singular)")
print("="*78)
for K in (2,3,4):
    h = DB[K]
    d = np.array([1e-2, 1e-3, 1e-4])
    v = np.abs(shat(2*np.pi + d, h))
    slope = np.log(v[0]/v[-1])/np.log(d[0]/d[-1])
    print(f"  db{K}: |shat(2pi+delta)| ~ delta^p with p = {slope:.4f}   (K = {K})")

# ------------------------------------------------------------------ [2] the ratio shat(eps_N m)/shat(eps_N(m+k))
print(); print("="*78)
print("[2] Lemma 4.5, p.46: claimed  |shat(eps_N m)/shat(eps_N (m+k))| <= C_k")
print("    RAMOND sector Gamma_{inf,+} = Z : take m + k = 2^{N+1} n  =>  denominator = shat(2 pi n) = 0")
print("="*78)
K = 4; h = DB[K]
for N in (4, 6, 8, 10):
    epsN = 2.0**(-N)*np.pi
    for k in (1.0, 2.0):
        for n in (1, 2):
            m = 2.0**(N+1)*n - k              # in Z  (Ramond sector)
            num = abs(shat(np.array([epsN*m]), h)[0])
            den = abs(shat(np.array([epsN*(m+k)]), h)[0])
            print(f"  N={N:2d} k={k:g} n={n}: m={m:11.0f}  "
                  f"|shat(eps_N m)|={num:.3e}  |shat(eps_N(m+k))|={den:.3e}  "
                  f"ratio={'inf' if den==0 else f'{num/den:.3e}'}")

print()
print("    NEVEU-SCHWARZ sector Gamma_{inf,-} = Z+1/2 : no exact pole, but scan sup of the ratio")
grid_report = []
for N in (6, 8, 10, 12):
    epsN = 2.0**(-N)*np.pi
    k = 2.0
    m = np.arange(-2**(N+2), 2**(N+2)) + 0.5          # Gamma_{inf,-}
    num = np.abs(shat(epsN*m, h)); den = np.abs(shat(epsN*(m+k), h))
    r = num/np.maximum(den, 1e-300)
    grid_report.append((N, r.max(), m[np.argmax(r)]))
    print(f"  N={N:2d}: sup over |m|<2^{N+2} of ratio = {r.max():.4e}   at m = {m[np.argmax(r)]:.1f}")
