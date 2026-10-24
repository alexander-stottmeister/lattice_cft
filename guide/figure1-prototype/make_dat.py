#!/usr/bin/env python3
"""Data for the design prototype of the guide's main figure (mainfig.tex beside this file).

Nothing is computed here beyond reading one file and taking the last entry of a list:
every number comes from docs/data/recorded.json, which tools/make_data.py writes from the
Daubechies filters (and which records, with a 'source' field, the few values it copies from
the numerics scripts rather than recomputes).  Run from anywhere:

    python3 guide/figure1-prototype/make_dat.py

Panel (b), measured rate exponents (open markers in the figure):
  meas_momentum.dat   momentum-cutoff route, ||l~ - l||_{h^{1+delta} -> h^0}, k = 2:
                      the last of the per-step rates of recorded.json momentum_cutoff_opnorm
                      (N = 7 -> 8); proved exponent min{delta, 2} (v5 Lemma 4.15).
  meas_recentred.dat  wavelet route after re-centring (Remark 3.5), recorded from
                      numerics/os_check11.py; proved exponent min{delta, 2} (Remark 4.8).
  meas_currents.dat   modified U(1) current approximants, recorded from os_check13.py;
                      proved exponent delta (v5 Lemma 5.1 (iii)).
Panel (c), regularity thresholds and the Sobolev exponents:
  thresholds.dat      row, minimal Daubechies order K, the Sobolev exponent it needs;
                      the two thresholds of Theorem 4.29 (K >= 9, rate K >= 10; v5 Remark 3.13,
                      source line 'Two further thresholds') are not in recorded.json and are
                      typed in here, marked 'typed' in the output.
  sigmas.dat          K, sigma_K from recorded.json sobolev_sigma (measured, os_check4.py).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
REC = os.path.join(ROOT, "docs", "data", "recorded.json")

with open(REC) as f:
    rec = json.load(f)


def write(name, header, rows):
    path = os.path.join(HERE, name)
    with open(path, "w") as f:
        f.write(header + "\n")
        for r in rows:
            f.write(" ".join(str(x) for x in r) + "\n")
    print("wrote %s (%d rows)" % (name, len(rows)))
    for r in rows:
        print("   ", *r)


# ---- panel (b) ------------------------------------------------------------------------
mom = rec["momentum_cutoff_opnorm"]["by_delta"]
rows = []
for d in sorted(mom, key=float):
    rates = mom[d]["rates"]
    rows.append((float(d), "%.4f" % rates[-1], "%.1f" % mom[d]["predicted"]))
write("meas_momentum.dat", "delta rate predicted", rows)

rc = rec["wavelet_route_opnorm"]["recentred_rates"]
write("meas_recentred.dat", "delta rate",
      [(d, "%.2f" % r) for d, r in zip(rc["delta"], rc["rate"])])

cu = rec["wzw_currents"]["rates"]
write("meas_currents.dat", "delta rate",
      [(d, "%.2f" % r) for d, r in zip(cu["delta"], cu["rate"])])

# ---- panel (c) ------------------------------------------------------------------------
sig = rec["sobolev_sigma"]["value"]
Ks = sorted(int(k) for k in sig)
write("sigmas.dat", "K sigma", [(K, "%.3f" % sig[str(K)]) for K in Ks])

thr = rec["thresholds"]
# rows are drawn top to bottom in the order listed here
rows = []
for i, t in enumerate(thr):
    rows.append((i, t["minK"], t["needs"].replace(" ", ""), "recorded", t["where"].replace(" ", "~")))
rows.append((len(thr), 9, "rho>5/2,Kbeta>3/2", "typed", "Theorem~4.29,~reconstruction"))
rows.append((len(thr) + 1, 10, "Kbeta>=5/2", "typed", "Theorem~4.29,~its~rate"))
write("thresholds.dat", "row minK needs provenance where", rows)

print("sigma_K at the minimal orders:",
      {K: sig[str(K)] for K in (3, 4, 5, 7, 9, 10)})
