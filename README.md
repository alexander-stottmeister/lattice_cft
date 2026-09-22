# Conformal field theory from lattice fermions — a critical re-reading and a revised manuscript

This repository holds an adversarial re-examination of the published article

> T. J. Osborne and A. Stottmeister, *Conformal Field Theory from Lattice Fermions*,
> Communications in Mathematical Physics **398** (2023) 219–289,
> [doi:10.1007/s00220-022-04521-8](https://doi.org/10.1007/s00220-022-04521-8),
> [arXiv:2107.13834](https://arxiv.org/abs/2107.13834), published open access under CC BY 4.0,

together with a revised version of that article in which every defect the re-examination found
is repaired, and a separate note settling one comparison the article makes in its introduction.

**The theorems of the published article stand.** No counterexample to any of them was found, and
no theorem statement has been changed. What the re-examination found is that several of the
published *proofs* do not establish what they claim, that the phrase "sufficiently regular" hides
three different and much larger thresholds than the folklore suggests, and that one normalisation,
read literally, would give the wrong central charge. All of this is repaired in the revision.

## What this is: an AI-assisted, experimental open-science project

This repository is an **experiment in open science, and the work in it is AI-assisted.** The
re-reading, the revision and the note were produced by the author working with Anthropic's Claude
as an interactive assistant, over three days in July 2026, and the working record — the list of
findings, the itemised changelog, the improvement plan and the numerical scripts behind every
number quoted — is published alongside the result rather than discarded.

**Human verification is ongoing.** Nothing in this repository has been refereed. Read every
statement here as a claim under active verification, not as a settled result, and check anything
you intend to rely on against the cited sources yourself. Direction, mathematical judgement and
final responsibility are the author's. T. J. Osborne, co-author of the published article, has
agreed to this material being made public.

## Relation to the published article — please read before citing

`free_fermion_cft_v5.tex` is **not the version of record** and must not be cited in its place.
The chain of versions is:

| version | what it is | public |
|---|---|---|
| arXiv v3, 24 Nov 2022 | last arXiv version, 71 pp | yes, CC BY 4.0 |
| CMP **398** (2023) 219–289 | version of record, 71 pp | yes, CC BY 4.0 |
| `free_fermion_cft_v4.tex` | the authors' own later draft, 72 pp as compiled here | **no** — first published in this repository |
| `free_fermion_cft_v5.tex` | the revision made here, 97 pp | this repository |

The middle step matters and is not documented anywhere else, so it is recorded here.
`free_fermion_cft_v4.tex` is a post-publication draft that was never released. It differs from
the arXiv v3 source in four places:

1. two typographical corrections in the second-quantisation formulas, `a†Aa → a†Ga` and
   `½Ψ*AΨ → ½Ψ*GΨ`;
2. the rescaled scaling function is **(anti)periodized**, `s^(ε_N) → s^(ε_N)_±` carrying a factor
   `(±1)^m`, with the scaling equation restated over all of `ℤ` and an added sentence explaining
   that in momentum space the (anti)periodization is the restriction of `ŝ` to `Γ_{N,±}`;
3. one rewritten sentence in the definition of the local one-particle spaces.

The version of record reads "2L-periodized" at point 2; the draft reads "2L-(anti)periodized".
The changelog `CHANGES-v4-to-v5.md` documents only the step from this draft to the revision, so
a reader comparing the revision against the published article will meet these four differences
in addition to everything the changelog lists. A `latexdiff` of the draft against the revision
does not show them either; the recipe for producing one is under **Building** below.

## Contents

| file | what it is |
|---|---|
| `critical-reread.tex` | 8 pp, 29 July 2026. The eight findings, with numerical evidence for each. Numbering is that of the published article. |
| `free_fermion_cft_v5.tex` | 97 pp. The revision. Carries a note on its title page saying what it is. |
| `free_fermion_cft_v4.tex` | the unreleased draft the revision starts from. |
| `CHANGES-v4-to-v5.md` | every change from the draft to the revision, itemised, with a v4↔v5 numbering table. |
| `IMPROVEMENT-PLAN.md` | the fourteen improvements made after the eight findings were repaired, in three tiers, all carried out. |
| `zini-wang-comparison.tex` | 9 pp, 31 July 2026. A note making §1.2's comparison with the low-energy scaling limit of Zini and Wang precise. |
| `numerics/` | nineteen `numpy` scripts. Every number quoted in the documents comes from one of them. |
| `sync_docs.py` | regenerates the parts of the two Markdown files, and `mainrefs.tex`, that carry statement numbers. |

### The eight findings

Numbers below are those of the **published** article.

| # | where | what | severity |
|---|---|---|---|
| 1 | Lemma 4.5 | the dominating function is obtained by bounding a quotient of `ŝ` by continuity; `ŝ` has zeros of order `K` at `2πℤ∖{0}`, so no such bound exists | gap, repairable |
| 2 | (204)–(210) | consequently `Error²(δ,L,k,N) = +∞` for every `k ≠ 0` in the Ramond sector, and the advertised rate is established only for `k = 0` | not established |
| 3 | "sufficiently regular" | three distinct thresholds, none stated: `σ_K > 1`, `σ_K > 3/2`, `σ_K > 1+δ`. The advertised `δ = 2` rate needs `K ≥ 9`, not `K ≥ 2` | hypothesis gap |
| 4 | Remark 4.14 | the Hardy projections do not preserve the wavelet core, so the claim does not follow from Lemma 4.5 | gap, repairable |
| 5 | Definition 4.2 | the one-particle generator is off by `L/π` against (165)/(167); read literally, (170) gives `c = (L/π)²` | normalisation |
| 6 | Theorem 6.3 | the two decisive ingredients are asserted, not proved; one is an `N`-uniform energy bound, a theorem in its own right | rigor debt |
| 7 | Theorem 4.16 | the preamble's locality claim is not established: that algebra is transported by the momentum-cutoff maps | overstatement |
| 8 | (25), Lemma 3.7, (204)/(205), (213) | typographical and constant errors | cosmetic |

All eight are repaired in the revision; §§1–7 of `CHANGES-v4-to-v5.md` say how. Finding 6 is
repaired by proving the energy bound, so Theorem 6.3 of the published article, Theorem 6.5 of the
revision, is now unconditional.

## Status and open points

- **The disposition of the revision is not settled.** Whether it becomes a corrigendum, an arXiv
  replacement or a separate follow-up paper has not been decided.
- **Nothing here has been refereed.**
- Three constants in the revision are known to be sufficient but not sharp: the growth constant of
  Remark 4.13, the aliasing exponent of Lemma 4.28, and the bound `σ_K ≥ K − 𝒦 − ½` of
  Definition 3.12. The revision says so at each place.
- The Zini–Wang note settles the comparison at fixed finite `N` for quasi-free states. Its §8
  lists four things it does not settle, among them the passage `N → ∞`, which needs quasi-equivalence
  rather than a multiplicity count.
- An earlier version of `critical-reread.tex` offered a one-line repair of the analytic-vector
  claim in Finding 6. That repair was itself wrong, for the reason now given in the text; the
  correct route is Nelson's commutator theorem, and it is what the revision uses.

## Building

No PDFs are tracked: they are rebuilt from the sources beside them. From the repository root,

```sh
mkdir -p build
pdflatex -output-directory=build free_fermion_cft_v5.tex   # twice, for cross-references
pdflatex -output-directory=build critical-reread.tex       # twice
pdflatex -output-directory=build zini-wang-comparison.tex  # twice
python3 sync_docs.py                                       # after any recompile of the revision
```

A marked-up comparison of the draft against the revision, deletions struck through and additions
underlined, is generated rather than tracked:

```sh
latexdiff free_fermion_cft_v4.tex free_fermion_cft_v5.tex > diff_v4_v5.tex
pdflatex -output-directory=build diff_v4_v5.tex            # twice; about 102 pp
```

It carries one unresolved cross-reference, to an equation label that the revision deletes. That is
an artifact of `latexdiff`, which strips labels out of deleted text while still typesetting the
text itself; both sources compile with no undefined references.

`sync_docs.py` reads `build/free_fermion_cft_v5.aux`, so the revision has to be compiled before it
runs; it regenerates `mainrefs.tex`, which `zini-wang-comparison.tex` inputs, and the parts of the
two Markdown files that quote statement numbers. Every source carries a fixed date rather than
`\today`, so builds are reproducible; setting `SOURCE_DATE_EPOCH` and `FORCE_SOURCE_DATE=1` makes
them byte-reproducible.

The numerical scripts need `numpy` and nothing else:

```sh
python3 numerics/os_check4.py    # Daubechies filters and Sobolev exponents, K = 2..12
```

They construct the Daubechies filters from scratch by spectral factorisation; orthonormality holds
to better than `6·10⁻¹⁵` and the measured Sobolev exponents reproduce the literature values to
three or four digits.

## Licence

- **Documents** (`*.tex`, `*.md`): [CC BY 4.0](LICENSE), the licence of the article they revise.
  The published article is © the authors, 2022, CC BY 4.0; this revision is a derivative work, and
  the modifications are indicated on the title page of the revision and itemised in
  `CHANGES-v4-to-v5.md`, as that licence requires.
- **Code** (`numerics/`, `sync_docs.py`): [MIT](LICENSE-CODE).

No third-party copyrighted material is contained in this repository or in its history.

## Citing

Cite the published article for the results it contains. If you refer to something that exists only
here — a finding, a rate, the energy bound, the multiplicity criterion — cite this repository by
URL and commit, and say that it has not been refereed. `CITATION.cff` carries the metadata.
