"""
Part 4: how regular must the Daubechies scaling function actually be?

Two distinct thresholds appear in Section 4.2.4:
  (i)  D_W subset D(ell_{pm,k})   <=>  s in H^1        <=>  sigma_K > 1
  (ii) ||shat(eps_M(.+k/2))||_{h^{1+delta}} < infty in (207)  <=>  sigma_K > 1 + delta
       (delta = 2 is the value used for the advertised 2^{-2N} rate)
sigma_K = Sobolev exponent of the Daubechies-K scaling function.
"""
import numpy as np
from numpy.polynomial import polynomial as P

def daubechies(K):
    """orthonormal Daubechies filter with K vanishing moments (2K taps), sum h = sqrt2."""
    # P(y) = sum_{n<K} binom(K-1+n,n) y^n
    coef = np.array([float(np.math.comb(K-1+n, n)) for n in range(K)]) if hasattr(np, 'math') \
           else np.array([float(__import__('math').comb(K-1+n, n)) for n in range(K)])
    ys = np.roots(coef[::-1]) if K > 1 else np.array([])
    zs = []
    for y in ys:
        b = 2 - 4*y
        disc = np.sqrt(b*b - 4 + 0j)
        for z in ((b+disc)/2, (b-disc)/2):
            if abs(z) < 1.0 - 1e-12:
                zs.append(z); break
    poly = np.array([1.0+0j])
    for _ in range(K):                       # K factors (1 + z)
        poly = P.polymul(poly, [1.0, 1.0])
    for z in zs:                             # (1 - z/z_j) type factors -> use (z_j - z)
        poly = P.polymul(poly, [-z, 1.0])
    h = np.real_if_close(poly, tol=1e6).real
    h = h/np.sum(h)*np.sqrt(2.0)
    return h

def check_orth(h):
    n = len(h)
    return max(abs(sum(h[i]*h[i+2*k] for i in range(n-2*k)) - (1.0 if k == 0 else 0.0))
               for k in range(n//2))

def m0(xi, h):
    n = np.arange(len(h)); xi = np.asarray(xi, float)
    return (np.exp(-1j*np.multiply.outer(xi, n)) @ h)/np.sqrt(2.0)

def shat(xi, h, J=None):
    xi = np.asarray(xi, float)
    if J is None:   # |m0(x)-1| = O(x): iterate until 2^-J max|xi| << 1, then 30 more
        J = int(np.ceil(np.log2(max(np.max(np.abs(xi)), 1.0)))) + 32
    out = np.ones(xi.shape, complex)
    for j in range(1, J+1): out = out*m0(xi*2.0**(-j), h)
    return out

def sobolev_exponent(h, jmin=6, jmax=14, npts=20001):
    """sigma = q where (int_{a<|xi|<2a} |shat|^2)^{1/2} ~ a^{-q-1/2+1/2}; fit log-log."""
    a, e = [], []
    for j in range(jmin, jmax):
        lo, hi = 2.0**j, 2.0**(j+1)
        xi = np.linspace(lo, hi, npts)
        blk = np.trapezoid(np.abs(shat(xi, h))**2, xi)
        a.append(2.0**j); e.append(blk)
    a = np.array(a); e = np.array(e)
    slope = np.polyfit(np.log(a), np.log(e), 1)[0]   # e ~ a^{1-2p}
    p = (1.0 - slope)/2.0
    return p - 0.5, p                                # (Sobolev sigma, L^2 decay exponent p)

def sup_exponent(h, jmin=5, jmax=13, npts=8001):
    a, e = [], []
    for j in range(jmin, jmax):
        xi = np.linspace(2.0**j, 2.0**(j+1), npts)
        a.append(2.0**j); e.append(np.max(np.abs(shat(xi, h))))
    return -np.polyfit(np.log(np.array(a)), np.log(np.array(e)), 1)[0]

print("="*86)
print("[12] Daubechies regularity vs. the two thresholds in Section 4.2.4")
print("     known sigma_K (Villemoes/Daubechies): db2 1.000, db3 1.415, db4 1.776, db6 2.386, db8 2.917")
print("="*86)
print(f"  {'K':>3} {'orth.err':>10} {'sigma_K (meas)':>15} {'p_L2':>8} {'K-Kbar (sup)':>13}"
      f"   {'s in H^1 ? (Lem 4.5 core)':>26}   {'delta=2 in (207)?':>18}")
for K in range(2, 13):
    h = daubechies(K)
    oe = check_orth(h)
    sig, p2 = sobolev_exponent(h)
    ps = sup_exponent(h)
    print(f"  {K:3d} {oe:10.1e} {sig:15.4f} {p2:8.3f} {ps:13.3f}"
          f"   {'YES' if sig > 1 else 'NO':>26}   {'YES' if sig > 3 else 'NO':>18}")
