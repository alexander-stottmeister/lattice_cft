# Reference

Four pages, meant to be read in this order if you are new to the material.

| page | what it is for |
|---|---|
| [status.md](status.md) | what is settled, what rests on a computation, and what is open |
| [notation.md](notation.md) | symbols and conventions, including the three that are easy to get wrong |
| [definitions.md](definitions.md) | the objects the results are about, in words |
| [results.md](results.md) | every numbered statement of the revision, with its page and a link to the widget that explores it |

`results.md` is generated from the compiled document by `tools/build_reference.py` and must
not be edited by hand. The other three are written by hand; where they quote a number they
name its source.

## Orientation in one paragraph

A conformal field theory is approximated by a chain of lattice models. Two renormalization
groups connect the scales: a **wavelet** one, built from a Daubechies scaling function, which
keeps things local in real space, and a **momentum-cutoff** one, which does not but behaves
better analytically. The Koo–Saleur formula builds candidate Virasoro generators on each
lattice. The theorems say those candidates converge, in the right topology and on the right
domain, to the generators of the continuum theory, and that correlation functions converge
with them. The revision in this repository quantifies every hypothesis that the published
version left as "sufficiently regular", repairs four proofs, and adds rates, domains and an
explicit error budget for simulating the theory on a quantum computer.

## The three documents

- **`free_fermion_cft_v5.tex`** is the revision, 97 pages. Start at its title-page note,
  which says what it is and what it is not.
- **`critical-reread.tex`** is the eight-finding audit that prompted the revision, 8 pages.
  It uses the numbering of the **published** article, not of the revision.
- **`zini-wang-comparison.tex`** is a separate 9-page note settling one comparison the
  introduction makes, and is where the multiplicity criterion is proved.
