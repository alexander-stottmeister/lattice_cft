#!/bin/sh
# Build the three reader-facing PDFs into docs/pdf/, reproducibly.
#
# The committed PDFs are byte-identical to what this produces, so a reader can check them.
# SOURCE_DATE_EPOCH fixes the timestamps pdfTeX would otherwise embed; the sources already
# carry fixed dates rather than \today, which is the other half of reproducibility.
set -eu
cd "$(dirname "$0")/.."
export SOURCE_DATE_EPOCH=1790035200 FORCE_SOURCE_DATE=1
mkdir -p build docs/pdf
# Run until the output stops changing, not a fixed number of times. Two passes settle the two
# notes but not the paper, whose cross-references need a third: the committed PDF was built
# with enough passes and a two-pass rebuild came out ten bytes short, so the claim above was
# false for the one file most likely to be checked. Five is a cap, not a target.
for f in free_fermion_cft_v5 critical-reread zini-wang-comparison; do
  PREV=""
  N=0
  while [ "$N" -lt 5 ]; do
    pdflatex -interaction=nonstopmode -output-directory=build "$f.tex" >/dev/null
    N=$((N+1))
    NOW=$(cksum < "build/$f.pdf")
    [ "$NOW" = "$PREV" ] && break
    PREV=$NOW
  done
  cp "build/$f.pdf" "docs/pdf/$f.pdf"
  echo "  $f.pdf  $(pdfinfo "docs/pdf/$f.pdf" | awk '/^Pages/{print $2}') pages, settled after $N passes"
done
