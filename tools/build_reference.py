"""Generate docs/reference/results.md and docs/data/results.json from the compiled aux.

Numbers and page references are read from build/free_fermion_cft_v5.aux; nothing here
hardcodes a statement number, which is the discipline sync_docs.py already applies to the
two Markdown records and the reason the hand-written parts of those drifted before.

The "new in v5" column is derived, not asserted: if build/free_fermion_cft_v4.aux is also
present it is the set difference of the labels.  Produce it with

    pdflatex -output-directory=build free_fermion_cft_v4.tex      (twice)

    python3 tools/build_reference.py
"""
import json
import os
import re
import sys
import datetime

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(HERE, "build")
REF = os.path.join(HERE, "docs", "reference")
DATA = os.path.join(HERE, "docs", "data")
PDF = "../pdf/free_fermion_cft_v5.pdf"

# label -> (one-line statement, status, widget anchor on the interactive page or "")
# status: proved | numerical | definition | convention
CURATED = {
 "def:convseq":        ("Convergent sequences of observables between scales", "definition", ""),
 "def:waveletrg":      ("The wavelet renormalization group, built from a Daubechies scaling function", "definition", "shat"),
 "prop:waveletrg":     ("It is an inductive system; item (4) is the asymptotic compatibility that re-centring would break", "proved", ""),
 "def:waveletrgcur":   ("The same maps for currents, quadratic in the fermions", "definition", ""),
 "rem:recentring":     ("Re-centring by the centre of mass, offered as a comparison convention and deliberately not built in", "convention", "support"),
 "def:antiloc":        ("Local one-particle spaces, discarding the last 2K-1 sites of an interval", "definition", ""),
 "prop:antilocal":     ("The wavelet group preserves localisation", "proved", ""),
 "rem:localisationradius": ("A strict one-sided light cone of width eps_N(2K-1), and the linear trade-off of locality against regularity", "proved", "support"),
 "lem:convergence":    ("Decay of the finite products of the low-pass symbol", "proved", ""),
 "cor:convergence":    ("What that decay gives inside the Brillouin zone, and only there", "proved", ""),
 "lem:decay":          ("Pointwise decay of the transform of the scaling function", "proved", "shat"),
 "def:regularity":     ("rho-regular means sigma_K > rho: the hypothesis the published version left as 'sufficiently regular'", "definition", "ladder"),
 "rem:regularityvalues": ("The table of sigma_K and rho, and the four thresholds that occur", "numerical", "ladder"),
 "lem:unifmaj":        ("The uniform majorant: the two decays interlock across the Brillouin zone", "proved", "majorant"),
 "cor:unifmaj":        ("The majorant in the form the dominated-convergence argument needs", "proved", "majorant"),
 "def:momrg":          ("The momentum-cutoff renormalization group", "definition", ""),
 "prop:momrg":         ("It is an inductive system, and the Hardy projections leave its core invariant", "proved", ""),
 "lem:stateconv":      ("The lattice vacua converge with no regularity hypothesis: the alias weights are probability weights", "proved", "alias"),
 "cor:stateconv":      ("The scaling limit of the lattice vacua, with the rate", "proved", "alias"),
 "rem:zeromode":       ("The massless Ramond zero mode, where the limit is convention-dependent", "proved", ""),
 "rem:stateconv":      ("One argument covers both renormalization groups", "proved", ""),
 "rem:staterate":      ("Where the rate comes from, and why a supremum over the aliasing class would not be small", "proved", "alias"),
 "def:KSapprox":       ("The Koo-Saleur approximants", "definition", ""),
 "rem:modalgebra":     ("The modified approximants' finite-scale algebra: the discrepancy vanishes for same-sign modes", "proved", "discrepancy"),
 "def:vir":            ("The one-particle Virasoro generators, renormalised: the published definition was off by L/pi", "definition", ""),
 "rem:normalisation":  ("The central charge is 1 (resp. 1/2) for every L under this normalisation", "proved", ""),
 "cor:viraesa":        ("Analytic vectors, with radius 1/|k| uniform in the mode", "proved", "radius"),
 "rem:impcond":        ("The Majorana implementability condition", "proved", ""),
 "lem:KSconv":         ("Wavelet route, one particle: convergence on the whole domain, not just a core", "proved", "rates"),
 "rem:KSconvrate":     ("The sharp rate in the Sobolev scale, with a matching lower bound at the Brillouin-zone edge", "proved", "rates"),
 "thm:KSconv":         ("Convergence of the approximants in the Fock representation (c = 0)", "proved", "rates"),
 "cor:KSconvbog":      ("The one-particle Bogoliubov transformations, made quantitative", "proved", "duhamel"),
 "rem:KSunitaryconv":  ("The estimate for multinomials in the creation and annihilation operators", "proved", ""),
 "lem:duhamel1p":      ("One-particle energy growth and Duhamel: linear in t at k = 0, exponential otherwise", "proved", "duhamel"),
 "rem:duhamel1psmeared": ("The same for smeared generators; the constant is sufficient but not sharp", "proved", "duhamel"),
 "cor:KSderivationconv": ("The derivations, with no t-dependence at all", "proved", "duhamel"),
 "lem:KSconvc":        ("Momentum-cutoff route, one particle: the sharp rate, with no regularity of the scaling function", "proved", "rates"),
 "thm:KSconvc":        ("Convergence in the positive-energy representations (c = 1/2, 1). Theorem A of the introduction", "proved", "rates"),
 "lem:energybound1k":  ("The energy bound at fixed mode, needing no regularity", "proved", ""),
 "cor:viraesac":       ("Essential self-adjointness on every core for the conformal Hamiltonian, by Nelson's commutator theorem", "proved", ""),
 "lem:duhamel":        ("Energy growth and Duhamel in Fock space", "proved", "duhamel"),
 "cor:KSunitariesc":   ("The unitary groups, with a rate", "proved", "duhamel"),
 "cor:KSconvbogc":     ("The Bogoliubov transformations on the momentum-cutoff route", "proved", "duhamel"),
 "rem:moeberror":      ("The Moebius generators in the Neveu-Schwarz sector", "proved", ""),
 "lem:KSconvsmeared":  ("The smeared approximants: uniform bound, domain and rate", "proved", "rates"),
 "rem:smearphase":     ("The smearing error is a pure phase, and re-centring makes it third order", "proved", "phase"),
 "thm:KSconvsmeared":  ("Convergence of the smeared approximants. Its rate needs K >= 7, not the K >= 6 printed", "proved", "phase"),
 "cor:KSconvsmeared":  ("The smeared corollary", "proved", ""),
 "rem:KSconvsmeared":  ("Lifting the restriction to basic sequences", "proved", "jackson"),
 "lem:loopjackson":    ("A Jackson estimate for the loop renormalization group, driven by the total aliasing mass", "proved", "jackson"),
 "thm:KSreconstruction": ("Reconstruction for every smooth loop, not only basic sequences; K >= 9, and K >= 10 for the rate", "proved", "jackson"),
 "rem:reconstructionrate": ("The two-scale rate", "proved", "jackson"),
 "cor:KSconvbogsmeared": ("The smeared Bogoliubov transformations", "proved", "duhamel"),
 "rem:errorrates":     ("The rate at nonzero mode is not an artefact of the estimate", "numerical", "rates"),
 "rem:noquotient":     ("Why the supremum must be taken with care: the step Finding 1 shows to be false", "proved", "shat"),
 "rem:stateapprox":    ("Simulating the theory: what the scale and the resolution mean in qubits", "proved", "budget"),
 "rem:timeerror":      ("The error of the time evolution, linear in t at zero mode", "proved", "duhamel"),
 "rem:conformalerror": ("The error for nonzero modes, on analytic vectors", "proved", "radius"),
 "lem:U1cur1pconv":    ("The modified current is exact on the bulk and its off-diagonal blocks vanish identically", "proved", "current"),
 "thm:U1cursmearedconv": ("Convergence of the Wess-Zumino-Witten currents, with no regularity for the qualitative statement", "proved", "current"),
 "rem:U1curvsvira":    ("Four ways the current is better behaved than the Virasoro generators", "proved", "current"),
 "thm:corapprox":      ("Convergence of the fermion correlation functions. Theorem B of the introduction", "proved", "budget"),
 "cor:corapprox":      ("The same for a wider class of observables", "proved", ""),
 "prop:corapproxrate": ("The explicit error bound for the chiral time evolution", "proved", "budget"),
 "rem:simulationbudget": ("The end-to-end qubit budget; locality costs a square root unless one re-centres", "proved", "budget"),
 "thm:corapproxvir":   ("Convergence of the Virasoro correlation functions. Theorem C, now unconditional", "proved", "budget"),
 "hyp:energybound":    ("The scale-uniform energy bound that makes Theorem C unconditional", "proved", ""),
 "rem:corapproxvir":   ("Mixed correlation functions", "proved", ""),
}

KIND = {"def": "Definition", "prop": "Proposition", "rem": "Remark", "lem": "Lemma",
        "cor": "Corollary", "thm": "Theorem", "hyp": "Proposition"}
SECTIONS = {3: "Scaling limits of lattice fermions", 4: "Approximation of conformal symmetries",
            5: "Approximation of Wess-Zumino-Witten currents", 6: "Approximation of correlation functions"}


def read_aux(path):
    out = {}
    if not os.path.exists(path):
        return out
    t = open(path, encoding="utf-8", errors="replace").read()
    for lab, num, page in re.findall(r"\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{([^}]*)\}", t):
        if lab.startswith(("eq:", "sec:", "fig:")):
            continue
        if re.match(r"^\d+\.\d+$", num):
            out[lab] = (num, page)
    return out


def main():
    v5 = read_aux(os.path.join(BUILD, "free_fermion_cft_v5.aux"))
    v4 = read_aux(os.path.join(BUILD, "free_fermion_cft_v4.aux"))
    if not v5:
        sys.exit("build/free_fermion_cft_v5.aux is missing; compile the revision first")
    missing = sorted(set(v5) - set(CURATED))
    extra = sorted(set(CURATED) - set(v5))
    if missing or extra:
        print("  WARNING: curated table out of step with the aux")
        for m in missing:
            print("    in the aux but not curated: %s (%s)" % (m, v5[m][0]))
        for e in extra:
            print("    curated but not in the aux: %s" % e)

    os.makedirs(REF, exist_ok=True)
    os.makedirs(DATA, exist_ok=True)
    rows = []
    for lab, (num, page) in sorted(v5.items(), key=lambda kv: [int(x) for x in kv[1][0].split(".")]):
        desc, status, widget = CURATED.get(lab, ("", "", ""))
        rows.append(dict(label=lab, number=num, page=int(page), section=int(num.split(".")[0]),
                         kind=KIND[lab.split(":")[0]], statement=desc, status=status,
                         widget=widget, new_in_v5=(bool(v4) and lab not in v4)))

    stamp = datetime.date.today().isoformat()
    L = ["# Results index", "",
         "One row per numbered statement of the revision. Generated by `tools/build_reference.py`",
         "from `build/free_fermion_cft_v5.aux` on %s; **do not edit by hand**, the numbers come" % stamp,
         "from the compiled document and change when it is recompiled.", ""]
    if v4:
        n_new = sum(1 for r in rows if r["new_in_v5"])
        L += ["The **new** column marks the %d statements that do not appear in `free_fermion_cft_v4.tex`," % n_new,
              "derived by comparing the two auxiliary files rather than asserted.", ""]
    else:
        L += ["> `build/free_fermion_cft_v4.aux` was not present, so the *new in v5* column is omitted.",
              "> Compile the draft with `pdflatex -output-directory=build free_fermion_cft_v4.tex` to get it.", ""]
    L += ["Statuses: **proved** in the revision, **numerical** where the evidence is a computation,",
          "**definition** and **convention** where nothing is claimed. The last column links to the",
          "widget on the interactive page that lets you vary the parameters.", ""]
    for sec in (3, 4, 5, 6):
        srows = [r for r in rows if r["section"] == sec]
        if not srows:
            continue
        L += ["## Section %d. %s" % (sec, SECTIONS[sec]), ""]
        head = "| statement | page | what it says | status |" + (" new |" if v4 else "") + " explore |"
        L += [head, "|---|---|---|---|" + ("---|" if v4 else "") + "---|"]
        for r in srows:
            link = "[p. %d](%s#page=%d)" % (r["page"], PDF, r["page"])
            w = "[%s](../index.html#%s)" % (r["widget"], r["widget"]) if r["widget"] else ""
            row = "| **%s %s** | %s | %s | %s |" % (r["kind"], r["number"], link, r["statement"], r["status"])
            if v4:
                row += " %s |" % ("yes" if r["new_in_v5"] else "")
            L += [row + " %s |" % w]
        L += [""]
    open(os.path.join(REF, "results.md"), "w").write("\n".join(L) + "\n")
    with open(os.path.join(DATA, "results.json"), "w") as f:
        json.dump({"generated": stamp, "rows": rows}, f, indent=1)
    print("  results.md: %d statements, %d sections, %d new in v5"
          % (len(rows), len({r["section"] for r in rows}), sum(1 for r in rows if r["new_in_v5"])))
    print("  results.json written")


if __name__ == "__main__":
    main()
