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
for f in free_fermion_cft_v5 critical-reread zini-wang-comparison; do
  pdflatex -interaction=nonstopmode -output-directory=build "$f.tex" >/dev/null
  pdflatex -interaction=nonstopmode -output-directory=build "$f.tex" >/dev/null
  cp "build/$f.pdf" "docs/pdf/$f.pdf"
  echo "  $f.pdf  $(pdfinfo "docs/pdf/$f.pdf" | awk '/^Pages/{print $2}') pages"
done
