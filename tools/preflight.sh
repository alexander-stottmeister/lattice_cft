#!/bin/sh
# Pre-flight audit, to be run before making this repository public.
#
#     sh tools/preflight.sh            # audit only
#     sh tools/preflight.sh --build    # also rebuild everything from the clone and diff it
#
# It clones the repository afresh with --no-local and audits the clone, never the working
# tree: a local-path clone hardlinks the pack and can carry objects a real fetch would not.
# Exits non-zero if any check fails. Nothing here modifies the repository or the remote.
#
# The checklist is due to the glimm_jaffe session, which ran the same exercise on a sibling
# repository; the traps in steps 2, 5 and 7 are ones that caught somebody out there.
set -eu

REPO=$(cd "$(dirname "$0")/.." && pwd)
SLUG=alexander-stottmeister/lattice_cft
TMP=$(mktemp -d)
CLONE=$TMP/clone
FAIL=0
pass() { printf '  [ ok ] %s\n' "$1"; }
fail() { printf '  [FAIL] %s\n' "$1"; FAIL=$((FAIL+1)); }
note() { printf '         %s\n' "$1"; }
trap 'rm -rf "$TMP"' EXIT

echo "Pre-flight audit of $SLUG"
echo "  clone: $CLONE"
git clone --no-local --quiet "$REPO" "$CLONE"
cd "$CLONE"

echo
echo "1. paths that were committed and later removed"
# These stay in the history and stay readable after a flip. That is not automatically wrong:
# what matters is whether their CONTENT may be published. This repository deliberately
# untracked some build output, so the check lists them and fails only if one is on the
# private list of step 3.
git log --all --diff-filter=A --name-only --format= | sed '/^$/d' | sort -u > "$TMP/added"
git ls-files | sort -u > "$TMP/tracked"
comm -23 "$TMP/added" "$TMP/tracked" > "$TMP/gone"
if [ ! -s "$TMP/gone" ]; then
  pass "$(wc -l < "$TMP/tracked" | tr -d ' ') paths, none ever deleted"
else
  pass "$(wc -l < "$TMP/tracked" | tr -d ' ') tracked; $(wc -l < "$TMP/gone" | tr -d ' ') removed and still in the history"
  sed 's/^/         still readable: /' "$TMP/gone"
  note "check each is publishable; they are text extracts and generated output here"
fi

echo "2. only the intended PDFs, in the history as well as the tree"
# NOTE: this repository deliberately publishes three PDFs. The check is that there are no
# OTHERS, and the stronger form looks at every blob ever written, not just what is tracked.
UNEXPECTED=$(git rev-list --objects --all | awk '{print $2}' | grep -i '\.pdf$' | sort -u | grep -v '^docs/pdf/' || true)
if [ -z "$UNEXPECTED" ]; then
  pass "only docs/pdf/ ($(git ls-files 'docs/pdf/*.pdf' | wc -l | tr -d ' ') files) has ever held a PDF"
else
  fail "a PDF outside docs/pdf/ is in the history"; echo "$UNEXPECTED" | sed 's/^/         /'
fi

echo
echo "3. nothing private ever entered the history"
# Only genuinely private material belongs here: third-party copyrighted PDFs, reference
# corpora, page images, correspondence. Superseded build output is not private, it is stale,
# and step 1 reports it instead.
BAD=""
for p in 'Osborne und Stottmeister' '^refs/' '/evidence/' 'citation_screenshot' 'dossier' '^PRIVATE'; do
  HIT=$(git rev-list --objects --all | awk '{print $2}' | grep -E "$p" | sort -u || true)
  [ -n "$HIT" ] && BAD="$BAD$HIT\n"
done
if [ -z "$BAD" ]; then pass "no third-party or private path in any commit"
else fail "a private path is in the history"; printf "%b" "$BAD" | sed 's/^/         /'; fi

echo "4. no session URL, address or local path in tracked content"
HIT=$(git grep -l -I -E 'Claude-Session|@gmail|@itp\.uni-hannover|/Users/|Documents/Uni' -- . || true)
if [ -z "$HIT" ]; then pass "clean across $(git ls-files | wc -l | tr -d ' ') tracked files"
else fail "a tracked file carries one of these"; echo "$HIT" | sed 's/^/         /'; fi

echo
echo "5. binaries: metadata as well as page content"
MET=$(for f in docs/pdf/*.pdf; do strings "$f" | grep -iE '/Users/|Documents/Uni|@gmail' || true; done)
if [ -z "$MET" ]; then pass "no local path or address in any PDF's metadata or streams"
else fail "a PDF embeds a local path or address"; echo "$MET" | sed 's/^/         /'; fi
if command -v pdftotext >/dev/null 2>&1; then
  TXT=$(for f in docs/pdf/*.pdf; do pdftotext "$f" - 2>/dev/null | grep -iE '/Users/|Claude-Session' || true; done)
  [ -z "$TXT" ] && pass "no such string in the rendered text either" || { fail "rendered PDF text carries one"; echo "$TXT" | sed 's/^/         /'; }
else note "pdftotext not installed; rendered text not checked"
fi
SVG=$(grep -l -E '/Users/|<!--' docs/figures/*.svg 2>/dev/null || true)
[ -z "$SVG" ] && pass "no comments or paths in the committed SVGs" || { fail "an SVG carries a comment or a path"; echo "$SVG" | sed 's/^/         /'; }

echo
echo "6. authorship"
IDS=$(git log --format='%ae %ce' | tr ' ' '\n' | sort -u)
if [ "$(echo "$IDS" | grep -cv 'users\.noreply\.github\.com')" -eq 0 ]; then
  pass "every author and committer is the GitHub noreply address"
else fail "a commit carries a real address"; echo "$IDS" | sed 's/^/         /'; fi
N=$(git rev-list --count HEAD)
S=$(git log --format=%B | grep -c 'Claude-Session' || true)
C=$(git log --format=%B | grep -c 'Co-Authored-By' || true)
[ "$S" -eq 0 ] && pass "no Claude-Session line in $N commits" || fail "$S commit message(s) carry a session URL"
if [ "$C" -eq "$N" ]; then pass "$C Co-Authored-By trailers for $N commits"; else
  note "$C Co-Authored-By trailers for $N commits; these lack one:"
  for c in $(git rev-list HEAD); do
    git log -1 --format=%B "$c" | grep -q 'Co-Authored-By' || git log -1 --format='         %h %s' "$c"
  done
  note "a decision, not a defect: making them uniform means another rewrite, and the clean"
  note "way to do that is delete-and-recreate rather than a force-push."
fi

echo
echo "7. the pruned commits are still gone from the remote"
# TRAP: a re-created repository answers 422 "No commit found", not a repository-level 404,
# and gh --jq prints that error JSON to stdout. Testing for "Not Found", or for empty
# output, reports the opposite of the truth. Test for a 40-hex sha.
if command -v gh >/dev/null 2>&1; then
  for sha in 69c2afa a66065d 8b4a370; do
    OUT=$(gh api "repos/$SLUG/commits/$sha" --jq '.sha' 2>&1 || true)
    if printf '%s' "$OUT" | grep -qE '^[0-9a-f]{40}$'; then fail "$sha is still served by the remote"
    else pass "$sha is not served"; fi
  done
else note "gh not installed; remote not checked"
fi

echo
echo "8. the committed output regenerates from this clone"
if [ "${1:-}" = "--build" ]; then
  ( cd "$CLONE" && mkdir -p build
    for f in free_fermion_cft_v5 free_fermion_cft_v4 critical-reread zini-wang-comparison; do
      pdflatex -interaction=nonstopmode -output-directory=build "$f.tex" >/dev/null 2>&1
      pdflatex -interaction=nonstopmode -output-directory=build "$f.tex" >/dev/null 2>&1
    done
    python3 sync_docs.py >/dev/null
    python3 tools/make_data.py >/dev/null
    python3 tools/make_figures.py >/dev/null
    python3 tools/build_reference.py >/dev/null ) || { fail "the rebuild itself failed"; }
  if git -C "$CLONE" diff --quiet; then pass "every generated file is byte-identical after a rebuild"
  else fail "a committed file does not regenerate"; git -C "$CLONE" diff --stat | sed 's/^/         /'; fi
  command -v node >/dev/null 2>&1 && { node "$CLONE/tools/check_js.mjs" >/dev/null 2>&1 && pass "browser kernels agree with the Python" || fail "browser kernels disagree with the Python"; }
  command -v node >/dev/null 2>&1 && { node "$CLONE/tools/check_widgets.mjs" >/dev/null 2>&1 && pass "every widget renders across its control range" || fail "a widget fails to render"; }
else
  note "skipped; pass --build to compile and diff (needs pdflatex, numpy and node)"
fi

echo
echo "9. remote settings"
if command -v gh >/dev/null 2>&1; then
  gh api "repos/$SLUG" --jq '"         private=\(.private) wiki=\(.has_wiki) issues=\(.has_issues) branch=\(.default_branch) forks=\(.forks_count) description=\(.description // "none")"' || true
  note "decide each of these deliberately; enabling Pages is itself the flip"
fi

echo
echo "10. order of operations"
note "audit, then flip, then enable Pages. Never prune before a push: a fetch or push"
note "rewrites the remote-tracking reflog and re-anchors unreachable objects."

echo
if [ "$FAIL" -eq 0 ]; then echo "PASS: no blocking finding."; else echo "FAIL: $FAIL blocking finding(s)."; fi
exit "$FAIL"
