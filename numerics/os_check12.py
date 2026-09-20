"""
Part 12: momentum-cutoff rates for Theorem 4.13 (item 2/3).
The difference elltilde^(N)_{pm,k} - ell_{pm,k} is an explicit multiplier-with-shift, so
  ||.||_{h^{1+delta} -> h^0} = sup_n |d_N(n)| / <n>^{1+delta},
  d_N(n) = cos(eps_N k/4)^2 sin(eps_N(n-k/2))/eps_N * chi_N(n-k) chi_N(n) - (n-k/2).
Also the Hilbert-Schmidt norms of the off-diagonal blocks, eq. (225).
L = pi, chiral '+', Gamma_{inf,-} = Z + 1/2.
"""
import numpy as np
PI = np.pi

def opnorm(N, k, delta, pad=6):
    eps = 2.0**(-N)*PI
    n = np.arange(-2**(N+pad), 2**(N+pad)) + 0.5
    chi = lambda x: (np.abs(x) < PI/eps).astype(float)
    d = np.cos(0.25*eps*k)**2*np.sin(eps*(n-0.5*k))/eps*chi(n-k)*chi(n) - (n-0.5*k)
    return np.max(np.abs(d)/(1.0+np.abs(n))**(1.0+delta))

def hsnorm(N, k):
    """eq. (225), '+' chirality: sum over n with n>0 and -(n-k)>0, i.e. 0<n<k."""
    eps = 2.0**(-N)*PI
    n = np.arange(-4*int(abs(k))-4, 4*int(abs(k))+5) + 0.5
    sel = (n > 0) & (n - k < 0)
    n = n[sel]
    chi = lambda x: (np.abs(x) < PI/eps).astype(float)
    t = np.cos(0.25*eps*k)**2*np.sin(eps*(n-0.5*k))/eps*chi(n-k)*chi(n) - (n-0.5*k)
    return float(np.sqrt(np.sum(np.abs(t)**2)))

print("="*84)
print("[25] momentum-cutoff:  ||elltilde^(N)-ell||_{h^{1+delta} -> h^0}   (k=2)")
print("="*84)
for delta in (0.0, 0.5, 1.0, 2.0, 3.0):
    v = [opnorm(N, 2.0, delta) for N in (4, 5, 6, 7, 8)]
    r = [-np.log2(v[i+1]/v[i]) for i in range(len(v)-1)]
    print(f"  delta={delta:3.1f}: " + " ".join(f"{x:.4e}" for x in v)
          + "  rates: " + " ".join(f"{x:5.2f}" for x in r) + f"   (predicted {min(delta,2.0):.1f})")
print()
print("="*84)
print("[26] off-diagonal Hilbert-Schmidt norms, eq. (225)  (predicted rate 2)")
print("="*84)
for k in (2.0, 4.0, 8.0):
    v = [hsnorm(N, k) for N in (4, 5, 6, 7, 8)]
    r = [-np.log2(v[i+1]/v[i]) for i in range(len(v)-1)]
    print(f"  k={k:g}: " + " ".join(f"{x:.4e}" for x in v)
          + "  rates: " + " ".join(f"{x:5.2f}" for x in r))
