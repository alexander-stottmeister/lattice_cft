"""
Part 14: order of the vacuum error, full vs chiral algebra.
Full 2-component symbol deviation (Cor 3.18):  ||S_0^(N)(k) - S(k)|| = |sin(eps_N k/4)|  -> FIRST order.
Chiral restriction (eq. 67 vs 119):  |1/2(1 +- sgn(k) cos(eps_N k/2)) - 1/2(1 +- sgn(k))|
                                    = sin^2(eps_N k /4)                     -> SECOND order.
"""
import numpy as np
PI = np.pi
sx = np.array([[0,1],[1,0]], complex); sy = np.array([[0,-1j],[1j,0]]); id2 = np.eye(2)

def Pp_lat(k, eps): 
    s = np.sign(k)
    return 0.5*(id2 + s*(-np.sin(0.5*eps*k)*sx + np.cos(0.5*eps*k)*sy))
def Pp_cont(k): return 0.5*(id2 + np.sign(k)*sy)

print("="*80)
print("[31] full 2-component vs chiral vacuum-symbol deviation at the largest relevant momentum")
print("     k = pi/eps_M  with M = 3;  reported: deviation and measured order in (N-M)")
print("="*80)
M = 3; epsM = 2.0**(-M)*PI
k = PI/epsM - 0.5          # largest momentum in Gamma_{M,-}
full, chir = [], []
for N in range(M+1, M+9):
    eps = 2.0**(-N)*PI
    full.append(np.linalg.norm(Pp_lat(k, eps) - Pp_cont(k), 2))
    # chiral: p_+ P p_+ entries, eq (65)/(67):  1/2 (1 + sgn(k) cos(eps k/2))  vs  1/2(1+sgn(k))
    chir.append(abs(0.5*(1 + np.sign(k)*np.cos(0.5*eps*k)) - 0.5*(1 + np.sign(k))))
rf = [-np.log2(full[i+1]/full[i]) for i in range(len(full)-1)]
rc = [-np.log2(chir[i+1]/chir[i]) for i in range(len(chir)-1)]
print("  full  : " + " ".join(f"{x:.3e}" for x in full))
print("  order : " + "  ".join(f"{x:.2f}" for x in rf) + "   (predicted 1)")
print("  chiral: " + " ".join(f"{x:.3e}" for x in chir))
print("  order : " + "  ".join(f"{x:.2f}" for x in rc) + "   (predicted 2)")
print()
print("  closed forms:  full = |sin(eps_N k/4)|,  chiral = sin^2(eps_N k/4)")
eps = 2.0**(-(M+5))*PI
print(f"  check at N=M+5:  full {full[4]:.6e} vs {abs(np.sin(0.25*eps*k)):.6e};"
      f"  chiral {chir[4]:.6e} vs {np.sin(0.25*eps*k)**2:.6e}")
