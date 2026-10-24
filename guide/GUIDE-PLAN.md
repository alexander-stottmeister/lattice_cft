# A readable account of this repository, written by a council of four agents

**Status: proposal of 24 October 2026, awaiting the decisions in Section 10. Nothing in it has
been run.** The figure of Section 9 exists as a design prototype in `guide/figure1-prototype/`,
which builds; everything else is a plan. Paths are relative to the repository root.

## 1. What the document is for

The record of this repository is careful and hard to read. It consists of the revised
manuscript (`free_fermion_cft_v5.tex`, 97 pp., 68 numbered statements of which 28 are new),
the eight-finding audit that prompted it (`critical-reread.tex`, 8 pp., in the *published*
article's numbering), the note on the Zini–Wang comparison (9 pp.), two itemised Markdown
records, nineteen numerical scripts, a site of interactive widgets and a generated reference
folder. Three things make it hard for a human:

- **Everything has the same weight.** The revision gives the XY half-shift identity the same
  typography as the false step that made the advertised error estimate infinite. A reader
  cannot tell which three facts carry the result.
- **Two numberings.** The audit uses the published article's numbers (Lemma 4.5, Theorem
  6.3, eq. (210)); the revision and everything generated from it use v5's (Lemma 4.7,
  Theorem 6.5, Remark 4.33). The hand-written parts of the two Markdown records were written
  before later insertions moved the v5 numbers. A reader who has not internalised the
  dictionary cannot follow a single finding from the audit to its repair.
- **Chains are long.** The repair of the false step runs through a uniform majorant (Lemma
  3.14), a core argument (Lemma 4.7), a two-sided rate remark (4.8), a Fock-space theorem
  (4.9), its smeared version (Lemma 4.23, Theorem 4.25), a phase identity (Remark 4.24) and a
  comparison convention (Remark 3.5) before the reader learns the one sentence that matters:
  *the sharp exponent is min{δ, 2}, and on the wavelet route it is paid for in regularity.*

The new document, working title *Conformal field theory from lattice fermions: what the
article proved, what it did not, and what the revision proves*, tells the whole story to a human
reader in about fourteen pages plus appendices, with the weight on what matters. It does not
replace or change any of the three documents, it adds no mathematics beyond what they contain,
and where the council finds a defect in a source it records the defect (Sections 5 and 8)
instead of repairing it silently in the retelling. Its model is the reader's companion written
for the P(φ)₂ cutoff-removal record (repository `pphi2-cutoff-removal`, 23–24 October 2026),
whose council process it reuses.

## 2. The reader, and the contract every section keeps

**Primary reader:** a mathematical physicist or quantum-information researcher at PhD level who
knows what a CFT, a Virasoro generator and a lattice fermion are, has read neither the
published article nor the revision, is sceptical of AI-assisted mathematics, and has 45
minutes. **Secondary:** the operator-algebraist who wants the precise statements with their
hypotheses (Appendix A), and the quantum-simulation practitioner who wants the error budget
and the qubit count (Section 6 of the outline).

The contract, binding on every section:

- **R1. One claim per section, in its first sentence.** The second sentence says why it
  matters. Everything after that supports the claim or is cut.
- **R2. Short chains.** No displayed argument has more than four steps. A longer argument is
  split into named steps with one-line statements, and the details move to Appendix A.
- **R3. Weight follows the tier map of Section 3.** Tier 1 gets the first three pages and
  Figure 1; Tier 3 never appears in the main text except as a pointer.
- **R4. Status is visible.** Every result carries one status word (proved / partial /
  conjectured / numerical / refuted, as defined in the workspace's standard) and its source;
  a status table of at most twelve rows sits near the front.
- **R5. Numbers before asymptotics.** "The order the advertised rate needs is 9, not 2" comes
  before "σ_K grows like 0.2 K".
- **R6. Notation diet.** At most about a dozen symbols in the main text (N, M, ε_N, k, δ, K,
  σ_K, s and ŝ, L_{±,k} and L^{(N)}_{±,k}, the two renormalization groups, c), listed in one
  box; every other symbol lives in the appendices.
- **R7. Caveats in place.** A limitation is stated in the sentence that makes the claim: in
  particular *chiral* wherever an ε_N² rate is claimed, and *re-centred* or *not re-centred*
  wherever a wavelet-route rate is named.
- **R8. One numbering.** The main text uses v5's numbers throughout; the published number
  appears once, in brackets, where a finding is first described. Every number comes from the
  generated label table (Section 8), never from memory or from the hand-written parts of the
  Markdown records.
- **R9. Readable never means less true.** The workspace's rigour standard applies in full: no
  unproved step presented as proved, no "clearly" or "standard" unless the omitted argument is
  immediate, no fact about a source that was not read, numerics labelled numerical.

## 3. The weighting (proposal; the council fixes it in round R2)

**Tier 1, the result (main text, first three pages, Figure 1).**
1. The three theorems of the published article (A: convergence of the Koo–Saleur
   approximants; B: convergence of fermion correlation functions; C: convergence of Virasoro
   correlation functions) stand; no statement was changed and no counterexample was found.
2. Three published proofs did not establish what they claimed, for three different reasons:
   a step that is false rather than unjustified (a quotient of ŝ bounded by uniform
   continuity although ŝ vanishes to order K at 2πℤ∖{0}, so that the advertised error
   functional is +∞ for every k ≠ 0 in the Ramond sector; Findings 1–2); an N-uniform energy
   bound asserted rather than proved, which carried Theorem C (Finding 6); and a hypothesis,
   "sufficiently regular", that hides four thresholds, K ≥ 3, 4, 7 and 9, where folklore
   says K ≥ 2 (Finding 3).
3. The revision does more than repair. It proves sharp rates by route: min{δ, 2} on the
   momentum-cutoff route with no condition on the scaling function (Lemma 4.15), min{δ, 1} on
   the wavelet route and min{δ, 2} after re-centring (Remark 4.8 with Remark 3.5), and the
   uncapped exponent δ with identically vanishing off-diagonal blocks for the U(1) currents
   (Lemma 5.1); it proves the energy bound (Proposition 6.6), so Theorem C is unconditional;
   and it gives an explicit error budget for quantum simulation in which chirality squares
   the ground-state error and so halves the exponent of the qubit count (Proposition 6.3,
   Remark 6.4).
4. Status: AI-assisted, not refereed, the disposition of the revision (corrigendum, arXiv
   replacement or follow-up paper) undecided.

**Tier 2, the mechanism (main text, about one page each).** The two renormalization groups
and why they do different jobs (locality against analytic control; the centre-of-mass
offset ε_N μ(s) that re-centring removes, Remark 3.5); why the ŝ-quotient fails and what
replaces it (the uniform majorant, Lemma 3.14, and the division-free splitting, Remark 4.33);
what the N-uniform energy bound says and why the k-sum converges under 1-regularity
(Proposition 6.6); why chiral observables are quadratically cheaper (the chiral entanglement of
the massless lattice vacuum, eq. (65), with entropy density 2 ln 2 − 1); why currents are
easier than Virasoro generators (the ways Remark 5.3 lists); the Zini–Wang criterion in one
paragraph (constancy of the GNS multiplicity, not purity; the obstruction is a discontinuity
at M = ∞ on the momentum-cutoff route only).

**Tier 3, precision (appendices).** Precise statements with hypotheses, status and locator;
the regularity table of Remark 3.13; the dictionary between the published and the revised
numbering; conventions (L, ε_N = 2^{−N} L, the sectors, the symbol conventions of
`docs/reference/notation.md`); the three constants known to be loose.

**Tier 4, provenance (one short appendix).** How the record was made: the three days in July
2026, the withdrawn earlier verdict "CORRECT, no logical gaps", the one-line repair of the
analytic-vector claim that was itself wrong and is now Nelson's commutator theorem, the
September 2026 publication.

**Deliberately left out.** The publication machinery (the pre-flight audit, the reproducible
build), the implementation of the site, the latexdiff, the history of the folder.

## 4. Outline and page budget (proposal)

| part | content | budget |
|---|---|---|
| front | title, notice (AI-assisted, not refereed, disposition open), abstract ≤ 150 words, "the result in one page" with Figure 1, status table | 2 pp. |
| 1 | What the article claims, and what stands | 1 p. |
| 2 | Three things that were wrong: the false step, the unproved bound, the hidden thresholds | 2.5 pp. |
| 3 | Two renormalization groups, two jobs; the centre-of-mass offset | 1.5 pp. |
| 4 | The rate each route proves, and what it costs (Figure 1 (b), (c)) | 1.5 pp. |
| 5 | From generators to correlation functions: Theorem C made unconditional | 1 p. |
| 6 | What it means for quantum simulation: the error budget, chirality, the qubit count | 1 p. |
| 7 | Currents are easier than generators | 0.5 p. |
| 8 | The Zini–Wang comparison: multiplicity, not purity | 0.75 p. |
| 9 | What is proved, what is numerical, what is open | 1 p. |
| 10 | How this record was made, and how to check it | 0.75 p. |
| A | Precise statements with hypotheses, status and locators | 3 pp. |
| B | The two numberings, conventions, the notation box in full | 1 p. |
| C | How the figures were made (scripts, data, checks) | 0.5 p. |

The story of the k ≠ 0 rate, as the reader should meet it (one sentence per step, at most one
display each):

1. *What was claimed.* The published error functional (206) was bounded by a quotient of two
   values of ŝ, and the rate 2^{−2δN} was advertised for every k.
2. *Why it fails.* ŝ has zeros of order K at every non-zero multiple of 2π, so the quotient has
   poles at admissible momenta and the supremum is +∞ for every k ≠ 0 in the Ramond sector
   (Remark 4.33).
3. *What replaces it.* A majorant uniform in the scale (Lemma 3.14) and a division-free
   splitting give convergence on the whole domain h¹ and the exponent min{δ, 1}, two-sided for
   0 < δ ≤ 1 (Lemma 4.7, Remark 4.8).
4. *What the exponent costs, and how to buy one more order.* The wavelet route needs
   σ_K > 1 + δ, which is K ≥ 9 at δ = 2; the first-order loss is the centre-of-mass phase and
   re-centring removes it (Remarks 3.5 and 4.24); the momentum-cutoff route has neither the
   loss nor the hypothesis (Lemma 4.15).

## 5. Found while preparing this plan

Each item was read at the source in the session that wrote this plan; none has been reviewed by
anyone else yet.

**F1 (fixed in the commit that adds this plan).** `docs/reference/status.md` said, under "Known
defects that are not fixed", that Theorem 4.25 "still carries the printed value" K ≥ 6. It does
not and never did while that page existed: the theorem statement (`free_fermion_cft_v5.tex`,
line 2775) has read "i.e. K ≥ 7" since the commit of 22 September 2026 that prepared the
publication (`78f0c60`, 10:44), the status page was written five hours later (`25c942c`), and
the PDF served from `docs/pdf/` prints "i.e. K ≥ 7". Severity MINOR (public documentation
claiming a defect the manuscript does not have); the page now records the correction and the
date it was wrong.

**F2 (for the council).** The Sobolev exponents in `docs/data/recorded.json` (computed by
`tools/make_data.py`) and the table of Remark 3.13 (from `numerics/os_check4.py`) differ in the
third decimal: by 0.001 at K = 6, 7, 8 and by more from K = 9 on (3.162 against 3.165, 3.402
against 3.406, 3.635 against 3.641; the re-read's 3.873 at K = 12 against 3.865), and against
Remark 3.13 also at K = 3 (1.416 against 1.415) and K = 2 (1.002 against the exact 1.000). No
threshold moves, with σ₂ = 1 taken as exact. The guide quotes one source and says which; the mathematical physicist
decides which in round R1.

**F3 (a verification item, not a finding).** Panel (b) of the prototype draws the published
claim (204)–(210) as the exponent δ for the one-particle operator norm. The published
Error²(δ, L, k, N) is a different functional, a supremum of a quotient, and the equivalence of
exponents between the two must be checked at the source before the panel is used.

**F4 (a trap, from the sibling project's review of 23 October 2026).** The revision keeps the
qualifier *chiral* on every ε_N² statement of the error budget (Remark 6.4). A retelling that
drops it asserts a bound that is false on the full two-component algebra, where the vacuum
term is first order (eq. (65) against eq. (130)). Not a defect of the revision; a rule for the
guide (R7).

**F5 (standing).** `tools/preflight.sh --build` passed on 24 October 2026 against a fresh clone
of commit `92c967d`, with its one standing warning (a historical blob of the auditor that does
not parse) and byte-identical regeneration of all 25 generated and 2 spliced files.

## 6. The council

All four members run on Opus 5.5 with reasoning effort `max`, through the agent definitions
`council-aqft`, `council-qi`, `council-mp` and `council-editor` in the user's agent folder
(`council-mp`, the mathematical physicist, was added on 24 October 2026 beside the four created
on 23 October 2026 for the P(φ)₂ companion, of which three are used here; that council's
constructive-QFT member is not needed).
Agent definitions are loaded at session start, so the council runs in a fresh session, and the
orchestrator confirms the five names appear in its agent list before round R1. Each member's
body says that the brief's role card governs, so no definition needs editing for this project.

| member | lens | owns (writes) | checks in everyone else's text |
|---|---|---|---|
| **AQFT** (nets of algebras, quasi-free states, GNS, Bogoliubov implementability, positive-energy representations, Virasoro nets) | Is the limit stated at the right level: which algebra, which state, which representation, which sector, which c? | §1, §3, §8, the representation column of the status table | every statement about algebras, states, representations, sectors and scaling limits |
| **QI** (lattice models, quantum simulation, error budgets, entanglement) | Are the budget, the chirality statement and the qubit count right, and is the near-term reading realistic? | §6, §7, the budget-related caption text | every resource number and every ε_N² claim's scope (F4); the entropy density; the multiplicity count as an entanglement statement |
| **Mathematical physicist** (functional analysis, domains, rates, constants, wavelet regularity) | Is every claim's status, hypothesis set, quantifier order, threshold and constant right, and is each chain short and complete? | §2, §4, §5, Appendices A–C, the data of Figure 1 | every status word, locator, rate, threshold and constant; F2, F3 |
| **Editor** (of a leading mathematical-physics journal) | Would a busy expert read past page one, and does the weight sit where the result is? | the tier map and outline (R2), front matter, §9, §10, captions, final integration | R1–R9; length; jargon; whether each figure carries one message |

The editor arbitrates disagreements and records each with its outcome in
`guide/council/decisions.md`.

## 7. Process

A brief, R0, and then six rounds R1–R6 as in the P(φ)₂ companion (which ran on 23–24 October 2026 and produced a 20-page
companion; its verifier found one CRITICAL and one MAJOR item, both in a figure's arrows, and
some twenty MINOR ones, all resolved before the record was committed). The council's shared memory
is the folder `guide/council/`.

| round | agents | output | gate |
|---|---|---|---|
| R0. Brief (orchestrator) | 0 | `guide/` skeleton with a preamble adapted from the P(φ)₂ companion (30 mm geometry, fixed date, the repository's palette); `guide/council/labels.md` generated from `build/free_fermion_cft_v5.aux` and `docs/data/results.json` by `guide/council/make_labels.py` (statement, kind, number, page, new-in-v5, published counterpart where the dictionary of `CHANGES-v4-to-v5.md` gives one); `BRIEF.md` with this plan's Sections 2, 3, 8 and 9, the facts the council builds on, and the memo format | the user's decisions, Section 10 |
| R1. Read | 4 in parallel | one memo each, sections A–H: must know (≤ 5), should know (≤ 8), pointer table (what a human should *not* read), the longest chain cut into pieces of ≤ 3 steps ending at a displayed checkpoint, figure proposals and verdicts on Figure 1, traps, findings about the sources (locator, sentence, why, repair, severity), the reader's first question; no member sees another's memo | four memos present |
| R2. Synthesis | 1 (editor) | `guide/PLAN.md`: tiering, outline with word budgets, figure list, editorial rules and banned words, rulings on disagreements, drafting assignments, the verifier's checklist | **Checkpoint 1: the user approves before drafting** |
| R3. Draft | 3 domain members in parallel; the orchestrator draws the figures and assembles front matter and bibliography | `guide/sections/*.tex`, one file per assigned section; each drafter returns the list of every locator and quotation it used | each file compiles inside the skeleton |
| R4. Edit | 1 (editor) | one voice, the page ceiling enforced, build report | 0 errors, 0 overfull, 0 undefined |
| R5. Verify | 1 fresh agent, not a council member (optionally a second, a cold reader of the PDF alone) | every number against the aux, every quotation against the sources, every status word, the banned-word grep, the chiral and re-centring qualifiers (R7), the figure data regenerated and diffed, the page budget; findings graded, nothing fixed silently | every CRITICAL and MAJOR finding resolved |
| R6. Record (orchestrator) | 0 (+ the knowledge-base reviewer) | findings resolved, rebuild, `refresh-latex-ignores`, the guide added to `tools/build_pdfs.sh` and built into `docs/pdf/`, README row and site link, knowledge-base nodes and review, commit, `tools/preflight.sh --build`, push only if it passes, handoff | pre-flight PASS |

**Size.** Ten agent runs (4 + 1 + 3 + 1 + 1) plus the knowledge-base reviewer; eleven with the
cold reader. Token use will be several million; it cannot be estimated more closely before R1
has run. Where a round's output comes back as a report rather than a file (the subagent
harness refused report files in R4 and R5 of the P(φ)₂ run), the orchestrator saves it
verbatim under `guide/council/` with a note at its head. The orchestrator reports after R1 and
after R2 before any drafting starts.

## 8. Rules for every council agent

- **Read**, in this order: `README.md`; `docs/reference/status.md`, `notation.md`,
  `definitions.md`; `guide/council/labels.md`; `free_fermion_cft_v5.tex` with
  `docs/pdf/free_fermion_cft_v5.pdf` and `build/free_fermion_cft_v5.aux` (title-page note and
  abstract from line 292, main results 369–449, Section 2 from 576, Section 3 from 1097 with
  the wavelet group at 1167, the momentum-cutoff group at 1499, the vacua at 1535, Remark 3.5 at
  1256, Definition 3.12 and Remark 3.13 at 1397–1426, Section 4 from 1713, Lemma 4.7 at 2231,
  Remark 4.8 at 2317, Lemma 4.15 at 2512, Remark 4.24 at 2760, Theorem 4.25 at 2774, Remarks
  4.32–4.33 at 2995–3002, Section 5 from 3120 with Lemma 5.1 at 3216, Section 6 from 3292);
  `critical-reread.tex` (summary table 49–72, the findings 72–483, verdict 483–514; it uses
  the published numbering); `zini-wang-comparison.tex` (sections at 78, 149, 197, 256, 392,
  476, 522, 557); the generated sections of `CHANGES-v4-to-v5.md` and `IMPROVEMENT-PLAN.md`
  (their hand-written parts may carry stale v5 numbers and are not a source of numbers);
  `docs/data/recorded.json` and `results.json`; the scripts under `numerics/` as needed.
- **Numbers** come only from `guide/council/labels.md`; a quotation is verbatim from the named
  file; a value from a script is quoted with the script's name and the block that prints it.
- **Status words** are the fixed five; "proved" bare only for what v5 proves; "numerical" for
  anything from the scripts, including every measured rate and every σ_K; "conditional on"
  wherever a result rests on a hypothesis (none of the three theorems does, after v5).
- **No new mathematics.** The guide explains the record; it proves nothing more and claims
  nothing less. Context about other work cites only the bibliography of `free_fermion_cft_v5.tex`.
- **Findings about the sources** go into section G of a memo, with locator, the exact sentence,
  why it fails, the repair and the severity, and from there into the register of `guide/PLAN.md`;
  never into the guide. Where a source sentence is the subject of a finding, the guide
  paraphrases the mathematics without the faulty phrase and without comment.
- **Write only under `guide/`**, and only the file the brief assigns. No git command, no
  knowledge-base command, no edit outside `guide/`, no build except of your own draft in a
  scratch copy. Do not spawn agents.
- **This repository is public**: everything committed is published when it is pushed. Paths
  relative to the repository root only; no personal addresses, no machine paths, no session
  identifiers; fixed dates, never `\today`.
- **In this shell `grep` is a wrapper that skips git-ignored files**, so a build log under an
  ignored path reads as empty: use `command grep` for every log check.

## 9. The figure

**One message:** *the three theorems stand; three published proofs did not; the revision says
exactly what rate each route delivers, at what price in regularity, and the reader can see at a
glance which of those statements are proved and which are measured.*

Three panels, one grammar for status used identically in all three: **solid** = a proved
exponent (two-sided where v5 writes ≍); **open marker** = a measured exponent (numerical, with
the shape naming the route); **dotted grey** = the published claim, not established; a **red
badge** = a finding against a published proof, with its severity in words; a **green badge** =
a theorem that stands. Colours: the repository's blue (momentum-cutoff route) and amber (wavelet
route, both comparison conventions, distinguished by line width and by direct labels), and the
dataviz reference aqua for the current approximants, because no third repository hue passes the
all-pairs validator beside blue and amber (blue/amber/aqua: worst CVD ΔE 13.3, normal-vision
21.2, light mode, all pairs). Every series carries a direct label; status colours never appear
without their word.

- **(a) Where the published proofs broke, and what stands.** The spine of the argument in six
  boxes, lattice fermions → scaling limit by either renormalization group → one-particle
  estimates → Virasoro generators (Theorem A = 4.16) → smeared and Möbius generators →
  correlation functions (Theorems B = 6.1 and C = 6.5), with the eight findings placed under
  the step they hit, each with its severity in words and its repair in v5's numbers, and the
  theorems badged "stands". Nothing is computed.
- **(b) The rate each route proves.** The exponent e in error ≍ ε_N^e against the smoothness δ
  of the vector (in h^{1+δ}): the published claim δ, dotted; the currents' δ with no cap and no
  regularity (Lemma 5.1 (iii)); the momentum-cutoff route's min{δ, 2} with no regularity (Lemma
  4.15); the wavelet route's min{δ, 1} and, re-centred, min{δ, 2} (Remark 4.8 with Remark 3.5);
  measured exponents as open markers, read from `docs/data/recorded.json`: momentum cutoff
  0.00, 0.50, 1.00, 2.00, 2.00 at δ = 0, ½, 1, 2, 3 (`os_check12.py`); currents 0.00, 0.51,
  1.02, 2.03, 3.05 (`os_check13.py`); re-centred wavelet 1.00, 1.50, 2.00 at δ = 1, 3/2, 5/2
  (`os_check11.py`). A note states the price: σ_K > 1 + δ on the wavelet route, K ≥ 5 at δ = 1
  and K ≥ 9 at δ = 2.
- **(c) What "sufficiently regular" costs.** For each statement that needs regularity, the
  smallest Daubechies order: 3 (Lemma 4.7, σ_K > 1), 4 (Lemma 4.23, > 3/2), 5 (Remark 6.4, > 2),
  7 (Theorem 4.25's rate, > 5/2), 9 (the rate at δ = 2, > 3), 9 and 10 (Theorem 4.29 and its
  rate, Remark 3.13), and a row for the momentum-cutoff route and the currents, which need
  nothing; the measured σ_K along the top; the dotted line at K = 2 is the published
  "sufficiently regular", with db2 borderline at σ₂ = 1.

**Data provenance.** `guide/figure1-prototype/make_dat.py` reads `docs/data/recorded.json` and
nothing else, takes the last per-step rate of each momentum-cutoff series, copies the recorded
rates of the other two routes and the thresholds, types the two thresholds of Theorem 4.29
from Remark 3.13 (line 1415) and marks them "typed" in its output, and writes five `.dat`
files. The open squares of panel (c) are read from `thresholds.dat`; the bars are typed, so a
mismatch would show as a square off its bar's end.

**Prototype.** `guide/figure1-prototype/mainfig.tex` builds twice with pdflatex to 0 errors,
0 overfull boxes and 0 undefined references, one page of 436.8 × 360.7 pt (15.4 × 12.7 cm),
laid out for a 15 cm text width (it will be included at `\textwidth`, a 2 % reduction);
rendered at 170 dpi and checked for collisions. Every label is 7 pt or larger except the σ_K
tick labels along the top of panel (c), which are 5 pt and must grow, move or go before the
figure is used. Before it becomes Figure 1: F3 verified at the source (whether the published
exponent compares with the one-particle operator norm as drawn); the σ_K source fixed (F2);
the caption written, naming the statements and scripts behind each line and marker, and
stating that the wavelet line is two-sided only for 0 < δ ≤ 1 (Remark 4.8, eq. (KSratelower)
against (KSrateupper)); a collision check at final size.

**Optional second figure.** The six README figures exist as SVG in two themes
(`docs/figures/`) and can be converted with `rsvg-convert` (installed) or redrawn with pgfplots
from `docs/data/`. The guide reuses at most two of them (the zeros of ŝ, which *is* the false
step; the simulation budget) and points to the site for the rest.

## 10. Decisions for you (my default first)

1. **Purpose.** A standalone reader's guide published in this repository (default), or a text
   for the authors' own use that stays out of it. The first can become the second's basis;
   the reverse is harder.
2. **Publication of this plan and the prototype.** They are in `guide/` and therefore
   published with the commit that adds them (default, as the P(φ)₂ council's brief and memos
   are), or moved out until the guide exists.
3. **Scope.** This repository's three documents (default), with one paragraph on the quantum
   simulation Letter and a cross-reference to its own planned guide; or a joint account of
   both projects.
4. **Size.** Full council, ten agent runs plus the reviewer (default), or lean: R1 by the
   three domain members with the editor synthesising only, R4 and R5 merged (eight runs).
5. **Figure 1.** As prototyped (default), or with panel (c) replaced by the simulation budget
   (the vacuum deviation against N − M, first order on the full algebra and second order on
   the chiral one), which would move the regularity thresholds to a table.
6. **The σ_K source** (F2): the manuscript's Remark 3.13 (default) or `recorded.json`;
   whichever is chosen, the guide says which and the other file is reconciled or annotated.
7. **The prototype's PDF**: untracked, as every PDF rebuilt from a `.tex` beside it (default,
   the ignore rules were added), or tracked under `docs/pdf/` now.

## 11. After the council

The guide joins `tools/build_pdfs.sh` and `docs/pdf/`, the README's "Read it here" table
and the site's first paragraph. Findings of the council about the three documents go to the
author through the register in `guide/PLAN.md` and the knowledge base; the documents
themselves are not edited by the council. The sibling plan for the quantum-simulation Letter
cross-references this guide for the companion paper's corrections instead of retelling them.
