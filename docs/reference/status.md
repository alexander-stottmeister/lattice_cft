# Status

What is settled, what rests on a computation, and what is open. Nothing here has been
refereed; read it as a claim under verification. The audit that prompted the revision was
adversarial by design, and it was itself audited: several of its own repairs turned out to be
wrong and were corrected, which is recorded below rather than quietly dropped.

## Settled in the revision

The three theorems of the published article stand, with no statement changed. No
counterexample to any of them was found.

- **Theorem A**, convergence of the Koo–Saleur approximants to the Virasoro generators in the
  positive-energy representations, is Theorem 4.16 of the revision. The published version
  stated it with no proof; there is one now.
- **Theorem B**, convergence of the fermion correlation functions, is Theorem 6.1.
- **Theorem C**, convergence of the Virasoro correlation functions, is Theorem 6.5, and it is
  now **unconditional**. The published proof rested on two asserted ingredients, one of them a
  scale-uniform energy bound that is a theorem in its own right; that bound is Proposition 6.6
  and it needs no hypothesis beyond the one already in force.

All eight findings of the audit are repaired. The two substantive ones were a domination step
that is false rather than merely unjustified, and a normalisation that, read literally, would
have given central charge `(L/π)²` instead of 1.

Beyond repair, the revision adds sharp rates in the Sobolev scale, Duhamel estimates that
replace "converges uniformly on compact intervals" with an explicit bound, a reconstruction
theorem for arbitrary smooth loops, exact approximants for the currents, and an end-to-end
error budget for quantum simulation.

## Resting on a computation

These are supported by the scripts in `numerics/`, not by a proof, and are labelled
**numerical** in [results.md](results.md).

- The **regularity table**: the Sobolev exponents `σ_K` and the pointwise exponents `ρ`. The
  exponents are measured from the dyadic-block decay of `ŝ`, reproducing the standard values to
  three or four digits. Every threshold in the revision is read off this table, including the
  `K ≥ 9` that the advertised rate needs.
- The **measured rates** quoted beside each theoretical rate. Where the two disagree the
  revision says so: the growth constant of Remark 4.13 and the aliasing exponent of Lemma 4.28
  are both sufficient rather than sharp, and the revision states that at each place.

The interactive page recomputes much of this in the browser from the same filters, so the
agreement can be checked rather than taken on trust.

## Open

- **The disposition of the revision is not decided.** Whether it becomes a corrigendum, an
  arXiv replacement or a separate follow-up paper is an open question, and it governs what may
  be cited and how.
- **Three constants are known to be loose**: the growth constant of Remark 4.13, the aliasing
  exponent of Lemma 4.28, and the bound `σ_K ≥ K − 𝒦 − ½` of Definition 3.12, which gives away
  half a derivative that is not actually lost.
- **Four things the Zini–Wang note does not settle**, listed in its own Section 8: the converse
  direction, states that are not quasi-free, the passage to infinitely many scales, which needs
  quasi-equivalence rather than a multiplicity count, and the strong scaling limit in the mixed
  case.
- **Future work named in the article** and untouched here: central charge below 1 through the
  coset construction, arbitrary rational theories through anyonic chains, symplectic fermions,
  and odd observables in the Ising case.

## Known defects that are not fixed

- An **earlier version of the audit** offered a one-line repair of the analytic-vector claim.
  That repair is wrong: the pair terms raise the particle number, so iterating produces a
  factorial squared and the series diverges for every time. The text now says so, and the
  actual repair is Nelson's commutator theorem. This is recorded rather than removed because
  the mistake is instructive.
- **Theorem 4.25 prints `K ≥ 6`** where the strict inequality of Definition 3.12 and the table
  of Remark 3.13 give `K ≥ 7`. Corrected in the two Markdown records; the theorem statement
  itself still carries the printed value at the time of writing.
- A **sibling folder** in the author's workspace, not part of this repository, still cites the
  published article with the wrong volume and year.
