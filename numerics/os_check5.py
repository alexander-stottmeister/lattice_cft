"""
Part 5: normalisation of the one-particle Virasoro generators.

Two mutually inconsistent normalisations of ell_{pm,k} appear:
  (A) eq. (165)/(143):  symbol  ell_k(l) = -(l + k/2)          (chiral '-')
  (B) Def. 4.2 (181) + (199):  symbol  = +-(L/pi)(l -+ k/2)

Both are used with the SAME bridge formula  L_{pm,k} = (L/pi) dF_S(ell_{pm,k})  and the
same commutator (170):
   [L_k, L_k'] = (L/pi)(k-k') L_{k+k'} + (L/pi)^2 c_{P}(ell_k, ell_k')
                                       =  ... + delta (1/12) n (n^2 - 1),  n = (L/pi) k .
Check which normalisation reproduces c = 1.
"""
import numpy as np

def schwinger(L, n, norm):
    """Tr( (ell_k)_{-+} (ell_{-k})_{+-} )  for the '+' chiral component, Hardy S_- = 1_{l<0}.
       Gamma_{inf,-} = (pi/L)(Z + 1/2);  k = (pi/L) n."""
    s = np.pi/L
    k = s*n
    tot = 0.0
    lam = np.arange(-4*abs(n)-4, 4*abs(n)+4) + 0.5
    for l in s*lam:
        if not (l < 0 and l + k > 0):        # (ell_{+,-k})_{+-}: l<0 -> l+k>0
            continue
        a = (l + 0.5*k)                      # (ell_{+,-k}) symbol at l
        b = ((l + k) - 0.5*k)                # (ell_{+,k})   symbol at l+k
        if norm == 'B':
            a *= L/np.pi; b *= L/np.pi
        tot += a*b
    return tot

print("="*80)
print("[13] does (170) give c = 1 ?   target central term = (1/12) n (n^2-1)")
print("="*80)
print(f"  {'L':>8} {'n':>3} {'target':>12} {'(L/pi)^2 c_S  [norm A]':>24} {'(L/pi)^2 c_S  [norm B]':>24}")
for L in (np.pi, 2*np.pi, 5.0):
    for n in (2, 3, 5):
        target = (n**3 - n)/12.0
        cA = (L/np.pi)**2*schwinger(L, n, 'A')
        cB = (L/np.pi)**2*schwinger(L, n, 'B')
        print(f"  {L:8.4f} {n:3d} {target:12.6f} {cA:24.6f} {cB:24.6f}")
print()
print("  => (170) reproduces c = 1 only with the (165)-normalisation (A).")
print("     With Definition 4.2 / (181)/(199) the central term is too large by (L/pi)^2,")
print("     and the structure constant comes out as (L/pi)^2 (k-k') instead of (L/pi)(k-k').")
print("     Both agree iff L = pi.")
