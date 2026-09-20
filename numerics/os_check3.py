"""
Part 3:  (a) measured decay exponent of shat  -> admissible delta in (207)/(210)
         (b) does a valid N-uniform dominating function exist (the repair)?
         (c) Error^2 in the Neveu-Schwarz sector
         (d) Remark 4.14: does the Hardy projection preserve the wavelet core D_W?
"""
import numpy as np
from os_check import DB, m0, shat, prod_m0
from os_check2 import f_N, f_lim

PI = np.pi

print("="*78)
print("[8] measured decay |shat(l)| ~ (1+|l|)^{-p}  =>  p = K - Kbar  (Lemma 3.8)")
print("    admissibility of (207): ||shat(eps_M(.+k/2))||_{h^{1+delta}} < inf  needs  p > delta + 3/2")
print("="*78)
for Kd in (2, 3, 4, 6):
    hh = DB[Kd]
    # envelope of |shat| on dyadic windows (shat oscillates & vanishes at 2 pi Z)
    ps = []
    for a in (2.0**np.arange(4, 12)):
        l = np.linspace(a, 2*a, 4001)
        ps.append((a, np.max(np.abs(shat(l, hh)))))
    ps = np.array(ps)
    p = -np.polyfit(np.log(ps[:,0]), np.log(ps[:,1]), 1)[0]
    dmax = p - 1.5
    print(f"  db{Kd}: p = K - Kbar = {p:.3f}   -> max admissible delta in (207)/(210) = {dmax:.3f}"
          f"   {'(delta=2 OK)' if dmax > 2 else '(delta=2 NOT admissible)'}")

print(); print("="*78)
print("[9] the repair: G(m) := sup_{N>M} |f_k^{(N)}(M,m)| -- is it in l^2 ?")
print("    (bounded by |m+k/2| |shat(eps_N m)| prod_{j=1..N-M}|m0(eps_{M+j}(m+k))|, Lemma 3.7)")
print("="*78)
K = 4; h = DB[K]; M = 2; k = 2.0
mm = np.arange(1, 2**13) + 0.5
G = np.zeros_like(mm)
for N in range(M+1, 20):
    G = np.maximum(G, np.abs(f_N(mm, k, M, N, h)))
FL = np.abs(f_lim(mm, k, M, h))
for lo, hi in [(1,10),(10,100),(100,1000),(1000,8000)]:
    sel = (mm > lo) & (mm <= hi)
    pG = -np.polyfit(np.log(mm[sel]), np.log(np.maximum(G[sel],1e-300)), 1)[0]
    pF = -np.polyfit(np.log(mm[sel]), np.log(np.maximum(FL[sel],1e-300)), 1)[0]
    print(f"  m in ({lo},{hi}]:  G(m) ~ m^-{pG:.2f}   |f_k(M,m)| ~ m^-{pF:.2f}   "
          f"sum G^2 over window = {np.sum(G[sel]**2):.3e}")
print(f"  total sum_m G(m)^2 over 0<m<2^13 = {np.sum(G**2):.6e}   "
      f"(sum |f_k|^2 = {np.sum(FL**2):.6e})   -> ratio {np.sum(G**2)/np.sum(FL**2):.3f}")
print("  => G and f_k have the SAME decay; a valid dominating function exists, just not the stated one.")

print(); print("="*78)
print("[10] Error^2(delta,L,k,N) of (206) in the NEVEU-SCHWARZ sector (no exact pole)")
print("="*78)
delta = 2.0
for k in (0.0, 1.0, 2.0):
    row = []
    for N in (6, 8, 10, 12):
        epsN = 2.0**(-N)*PI
        m = np.arange(-2**(N+2), 2**(N+2)) + 0.5
        r = np.abs(shat(epsN*m, h))/np.maximum(np.abs(shat(epsN*(m+k), h)), 1e-300)
        inner = np.cos(0.25*epsN*k)**2*np.sinc(epsN*(m+0.5*k)/PI)*r - 1.0
        e2 = np.max((1.0+np.abs(m+0.5*k))**(-2*delta)*np.abs(inner)**2)
        row.append(e2)
    rates = "  ".join(f"{row[i]/row[i+1]:.1f}x" for i in range(len(row)-1))
    print(f"  k={k:g}: Error^2 (N=6,8,10,12) = " + "  ".join(f"{v:.2e}" for v in row))
    print(f"        successive ratios (expect 2^{{2*delta*2}} = {2**(2*delta*2):.0f} for the claimed rate): {rates}")

print(); print("="*78)
print("[11] Remark 4.14: does the Hardy projection P^+ preserve the wavelet core D_W?")
print("     D_W = union_N R^N_inf(h_N) = union_N V_N (multiresolution spaces).")
print("     test: is P^+ s^{(eps_M)}(. - x) in V_J for some J >= M ?  measure ||(1-Q_J) P^+ v|| / ||P^+ v||")
print("="*78)
# Fourier picture on S^1_L with L = pi:  Gamma_{inf,-} = Z + 1/2 ; V_J has  xi_hat(mm) = eps_J^{1/2} shat(eps_J mm) eta_per(mm)
Mv = 3
mm = np.arange(-2**14, 2**14) + 0.5
epsM = 2.0**(-Mv)*PI
v = epsM**0.5*shat(epsM*mm, h)                       # a single scaling function at scale M (eta = delta_0)
print(f"  ||v||^2 = {np.sum(np.abs(v)**2):.6f}  (should be ~1 up to truncation)")
Pv = np.where(mm > 0, v, 0.0)                        # Hardy projection = positive frequencies
for J in (3, 4, 6, 8, 10):
    epsJ = 2.0**(-J)*PI; LJ = PI/epsJ                # V_J: eta_per has period 2 L_J in the index
    sJ = shat(epsJ*mm, h)
    # orthogonal projection onto V_J in Fourier: for each residue class r mod 2L_J,
    #   (Q_J w)^(m) = sJ(m) * [ sum_{m' == m} conj(sJ(m')) w(m') ] / sum_{m'==m} |sJ(m')|^2
    per = int(round(2*LJ))
    idx = np.mod(np.round(mm - 0.5).astype(int), per)
    num = np.zeros(per, dtype=complex); den = np.zeros(per)
    np.add.at(num, idx, np.conj(sJ)*Pv); np.add.at(den, idx, np.abs(sJ)**2)
    QPv = sJ*(num[idx]/np.maximum(den[idx], 1e-300))
    resid = np.sqrt(np.sum(np.abs(Pv-QPv)**2)/np.sum(np.abs(Pv)**2))
    print(f"  J={J:2d}: relative distance of P^+ v from V_J  = {resid:.6f}")
