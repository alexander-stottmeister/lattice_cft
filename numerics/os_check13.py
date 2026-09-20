"""
Part 13: WZW currents (Theorem 5.1).  j_k is the unitary momentum translation, so
jtilde^(N)_k = R^N_inf j^(N)_k (R^N_inf)^*  is: restrict to Gamma_N, shift by k CYCLICALLY,
embed.  Claims:
 (a) jtilde^(N)_k and j_k agree EXACTLY on {n : n, n+k both in Gamma_N} -- no bulk error at all;
 (b) ||jtilde^(N)_k - j_k||_{h^delta -> h^0}  =  Theta(eps_N^delta), UNCAPPED in delta;
 (c) the off-diagonal (Hilbert-Schmidt) blocks of the difference VANISH identically for large N.
L = pi, chiral '+', Gamma_{inf,-} = Z + 1/2, Hardy S_- = 1_{n<0}.
"""
import numpy as np
PI = np.pi

def build(N, k, pad=4):
    LN = 2**N                                   # |Gamma_N| = 2 L_N = 2^{N+1}
    n = np.arange(-2**(N+pad), 2**(N+pad)) + 0.5
    pos = {v: i for i, v in enumerate(n)}
    d = len(n); nl = 2*LN
    A = np.zeros((d, d)); B = np.zeros((d, d))
    inG = np.abs(n) < LN                        # Gamma_N  (|n| < pi/eps_N = 2^N)
    for i, v in enumerate(n):
        if v + k in pos: B[pos[v+k], i] = 1.0                     # j_k
        if inG[i]:
            w = v + k
            while w >= LN:  w -= nl                                # cyclic shift in Gamma_N
            while w < -LN:  w += nl
            A[pos[w], i] = 1.0                                     # jtilde^(N)_k
    return n, A, B, inG

print("="*86)
print("[27] (a) bulk agreement: entries where n and n+k are both inside Gamma_N")
print("="*86)
for N in (4, 6):
    for k in (1.0, 3.0):
        n, A, B, inG = build(N, k)
        both = inG & np.array([(v+k in {x for x in n}) and abs(v+k) < 2**N for v in n])
        print(f"  N={N} k={k:g}: max|A-B| on bulk columns = {np.max(np.abs((A-B)[:, both])):.1e}"
              f"   (#bulk = {both.sum()}, #wrap = {(inG & ~both).sum()})")

print()
print("="*86)
print("[28] (b) ||jtilde^(N)_k - j_k||_{h^delta -> h^0}   (k=3)")
print("="*86)
for delta in (0.0, 0.5, 1.0, 2.0, 3.0):
    v = []
    for N in (4, 5, 6, 7):
        n, A, B, _ = build(N, 3.0)
        v.append(np.linalg.norm((A-B)/((1.0+np.abs(n))**delta)[None, :], 2))
    r = [-np.log2(v[i+1]/v[i]) for i in range(len(v)-1)]
    print(f"  delta={delta:3.1f}: " + " ".join(f"{x:.4e}" for x in v)
          + "  rates: " + " ".join(f"{x:5.2f}" for x in r) + f"   (predicted {delta:.1f})")

print()
print("="*86)
print("[29] (c) off-diagonal blocks of the difference (Hardy S_- = 1_{n<0})")
print("="*86)
for k in (1.0, 3.0, 6.0):
    row = []
    for N in (4, 5, 6, 7):
        n, A, B, _ = build(N, k)
        P = (n > 0).astype(float); Q = 1.0 - P
        D = A - B
        od = np.linalg.norm(np.diag(P) @ D @ np.diag(Q), 'fro') + np.linalg.norm(np.diag(Q) @ D @ np.diag(P), 'fro')
        row.append(od)
    print(f"  k={k:g}: " + "  ".join(f"{x:.1e}" for x in row))

# ---------------------------------------------------------------- modified current
def build_mod(N, k, pad=4):
    """as build(), but with the chi_{Gamma_N}(n+k) modification of Section 4.2.2:
       the wrap-around entries are DELETED instead of folded back."""
    LN = 2**N
    n = np.arange(-2**(N+pad), 2**(N+pad)) + 0.5
    pos = {v: i for i, v in enumerate(n)}
    d = len(n)
    A = np.zeros((d, d)); B = np.zeros((d, d))
    inG = np.abs(n) < LN
    for i, v in enumerate(n):
        if v + k in pos: B[pos[v+k], i] = 1.0
        if inG[i] and abs(v+k) < LN and (v+k in pos):
            A[pos[v+k], i] = 1.0
    return n, A, B, inG

print()
print("="*86)
print("[30] the SAME quantities for the modified current  jbar^(N)_k  (chi_{Gamma_N} inserted)")
print("="*86)
print("  off-diagonal Hilbert-Schmidt norms of the difference:")
for k in (1.0, 3.0, 6.0):
    row = []
    for N in (4, 5, 6, 7):
        n, A, B, _ = build_mod(N, k)
        P = (n > 0).astype(float); Q = 1.0 - P
        D = A - B
        row.append(np.linalg.norm(np.diag(P) @ D @ np.diag(Q), 'fro')
                   + np.linalg.norm(np.diag(Q) @ D @ np.diag(P), 'fro'))
    print(f"    k={k:g}: " + "  ".join(f"{x:.1e}" for x in row))
print("  operator norms  ||jbar-tilde^(N)_k - j_k||_{h^delta -> h^0}  (k=3):")
for delta in (0.0, 0.5, 1.0, 2.0, 3.0):
    v = []
    for N in (4, 5, 6, 7):
        n, A, B, _ = build_mod(N, 3.0)
        v.append(np.linalg.norm((A-B)/((1.0+np.abs(n))**delta)[None, :], 2))
    r = [-np.log2(v[i+1]/v[i]) for i in range(len(v)-1)]
    print(f"    delta={delta:3.1f}: " + " ".join(f"{x:.4e}" for x in v)
          + "  rates: " + " ".join(f"{x:5.2f}" for x in r) + f"   (predicted {delta:.1f})")
