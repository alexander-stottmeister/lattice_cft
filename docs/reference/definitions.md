# Definitions

The objects the results are about, in words. Precise statements are in the revision at the
numbers given; [results.md](results.md) links each to its page.

## The chain of lattices

At scale `N` the circle carries `#Λ_N` sites at spacing `ε_N = 2^{-N} L`, and on each site a
fermionic degree of freedom. Finer lattices are larger `N`. The question is what happens as
`N → ∞`, and the answer has to say in what sense the algebras at different scales are
comparable at all.

## Two renormalization groups (Definitions 3.2 and 3.16)

A renormalization group here is a family of maps embedding the scale-`N` description into the
scale-`N+1` one, compatibly.

- The **wavelet** group is built from a compactly supported Daubechies scaling function of
  order `K`. Its virtue is locality: it maps one lattice site into an interval of width
  `ε_N(2K−1)` lying entirely to that site's right, a strict one-sided light cone with no tail
  (Remark 3.8). Its cost is that the scaling function enters every estimate, which is where the
  regularity hypotheses come from.
- The **momentum-cutoff** group simply restricts to the momenta the lattice can represent. It
  is not local in real space — its kernel decays only like the reciprocal of the distance — but
  no scaling function appears in its symbol, so it carries no regularity hypothesis and gives
  better rates.

The revision uses both, and part of its work is saying precisely what each is good for. With
re-centring the two are equivalent in rate, so the wavelet group's locality comes for free.

## Re-centring (Remark 3.5)

Daubechies scaling functions are markedly asymmetric: the centre of mass sits at 79 to 89 per
cent of the way along the support. Comparing a lattice site with the *centre of mass* of the
wavelet sitting on it, rather than with the site itself, removes a first-order error and gains
one order in every wavelet-route rate. It is deliberately **not** built into the definition,
for two reasons the remark gives: the re-centred maps are not compatible between scales, and
re-centring the scaling function instead would destroy the dyadic structure.

## The Koo–Saleur approximants (Definition 4.1)

The lattice candidates for the Virasoro generators: a specific quadratic expression in the
lattice fermions whose continuum limit ought to be the generator of a conformal transformation.
"Ought to" is what the theorems make precise. A modification by the indicator of the momentum
lattice is needed to make them behave at the zone boundary, and the consequences of that
modification are Remark 4.2.

## Quasi-free states and their symbols

A quasi-free state of a fermion system is determined by a single operator, its symbol, with
spectrum in the unit interval. The state is pure exactly when the symbol is a projection. The
renormalization group acts on symbols by compression along an isometry, and that one
observation drives the whole Zini–Wang note.

## GNS multiplicity (Zini–Wang note, Proposition 3.1)

For a quasi-free state on a finite lattice the Gelfand–Naimark–Segal representation has
multiplicity `2^{m}`, where `m` counts the eigenvalues of the symbol lying strictly between
0 and 1. Connecting unitaries between the representations at successive steps exist exactly
when `m` is *constant*, which is a weaker demand than the state being pure. This is the
criterion the article's introduction should have used, and the correction is the note's main
point.

## Regularity (Definition 3.12)

`s` is called `ρ`-regular when its Sobolev exponent exceeds `ρ`, strictly. This replaces the
published article's unquantified "sufficiently regular". Four thresholds occur, needing orders
3, 4, 7 and 9 respectively; see [notation.md](notation.md) for why there are two exponents in
play and which is which.
