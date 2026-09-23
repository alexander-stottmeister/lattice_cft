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
# repository; the traps recorded in steps 5, 7 and 10 are ones that caught somebody out there.
set -eu

REPO=$(cd "$(dirname "$0")/.." && pwd)
SLUG=alexander-stottmeister/lattice_cft
TMP=$(mktemp -d)
CLONE=$TMP/clone
FAIL=0
WARN=0
pass() { printf '  [ ok ] %s\n' "$1"; }
fail() { printf '  [FAIL] %s\n' "$1"; FAIL=$((FAIL+1)); }
# A warning does not block, but it must reach the closing verdict rather than scroll past:
# it means the audit is sound and yet does not describe what would actually become public.
warn() { printf '  [warn] %s\n' "$1"; WARN=$((WARN+1)); }
note() { printf '         %s\n' "$1"; }
trap 'rm -rf "$TMP"' EXIT

# The strings step 4 and step 5 look for are assembled from fragments, so that this script
# does not contain them literally and therefore does not match itself. Written out, step 4
# fails on the auditor: it passed while the script was still untracked, because a clone
# cannot see an untracked file, and failed the moment the script was committed.
# Each pattern describes an ACTUAL leak, not the vocabulary of one. The looser forms fired on
# any text that merely discussed them -- including this script's own history, where the version
# committed in c5636a7 carries the pattern list inline and nothing else. A check that fails on
# a list of patterns trains its reader to ignore it, and the list is not private: the fragments
# below sit in the published file, where anyone can reassemble them. So a bare '/Users/' is not
# a finding; '/Users/' followed by a name is. The fragments are kept as well, so that this file
# still does not contain the strings it searches for.
P_SESS='Claude-Sess''ion:|claude''\.ai/code/session'
P_MAIL='[A-Za-z0-9._%+-]+@gm''ail|@gm''ail\.com'
P_INST='[A-Za-z0-9._%+-]+@itp''\.uni-hannover|@itp''\.uni-hannover\.de'
P_HOME='/Us''ers/[A-Za-z0-9._-]+'
P_WS='/Doc''uments/Uni|Doc''uments/Uni/'
SECRETS="$P_SESS|$P_MAIL|$P_INST|$P_HOME|$P_WS"

# Every path that has ever existed in any tree, one per line.
#
# TRAP, and it has bitten twice. `git rev-list --objects` looks like the right tool and is not.
#   It names each unique BLOB once, under the first path it reaches, so a private path whose
#   content is byte-identical to content at an allowed path is never printed at all: a copy of
#   this project's third-party PDF at refs/ stayed invisible while the same bytes sat under
#   docs/pdf/, and steps 2 and 3 both passed. The defect is the enumeration, not the parsing.
#   It also prints the path unquoted after the sha, so a path containing a space was truncated
#   by `awk '{print $2}'` and a path containing a newline split the record.
# ls-tree per commit lists every path in every tree, and quotes a path with a newline rather
# than splitting it, so both shapes survive as one line.
# ls-tree quotes a path containing a newline -- "docs/notes\nOsborne-scan.pdf" -- which is
# what keeps it on one line, but the surrounding quotes then defeat an anchored match: a
# pattern ending in \.pdf$ does not fire, because the line ends in a quote. Strip them.
objpaths() {
  for c in $(git rev-list --all); do git ls-tree -r --name-only "$c"; done \
    | sed 's/^"//; s/"$//' | sort -u
}

# The PDFs this repository publishes, from the index rather than a shell glob. A glob does not
# descend, while step 2 accepts anything under the docs/pdf/ prefix, so a PDF one directory
# deeper was counted by step 2 and never opened by step 5.
pubpdfs() { git ls-files -- docs/pdf | grep -i '\.pdf$' || true; }

echo "Pre-flight audit of $SLUG"
echo "  clone: $CLONE"
git clone --no-local --quiet "$REPO" "$CLONE"
cd "$CLONE"

echo
echo "1. paths that were committed and later removed"
# These stay in the history and stay readable after a flip. That is not automatically wrong:
# what matters is whether their CONTENT may be published. This repository deliberately
# untracked some build output, so this step only lists them: it has no failing branch at
# all. A removed path whose NAME is on step 3's private list is caught there, over every
# object in the history. Step 3 reads names and not content, and step 4 greps only the
# tracked tree, so a deleted file with an innocuous name and private content is caught by
# nobody: the list this step prints is for a human to read.
# -m diffs merge commits against each parent. Without it a path introduced by a merge and
# later deleted appears nowhere in this list, which is the human backstop the steps below
# lean on.
git log --all -m --diff-filter=A --name-only --format= | sed '/^$/d' | sort -u > "$TMP/added"
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
UNEXPECTED=$(objpaths | grep -i '\.pdf$' | grep -v '^docs/pdf/' || true)
if [ -z "$UNEXPECTED" ]; then
  pass "only docs/pdf/ ($(pubpdfs | wc -l | tr -d ' ') files) has ever held a PDF"
else
  fail "a PDF outside docs/pdf/ is in the history"; echo "$UNEXPECTED" | sed 's/^/         /'
fi

echo
echo "3. nothing private ever entered the history"
# Only genuinely private material belongs here: third-party copyrighted PDFs, reference
# corpora, page images, correspondence. Superseded build output is not private, it is stale,
# and step 1 reports it instead.
#
# TRAP: these match the PATH NAME and never the content, so the private material has to be
# recognisable from its name. Anchor every directory and prefix pattern with (^|/) rather
# than ^ or a bare slash: '^refs/' misses sub/refs/x, '/evidence/' misses a top-level
# evidence/x because there is no parent to supply the slash, and '^PRIVATE' misses
# sub/PRIVATE-x. Review planted exactly those and step 3 passed.
# Keep this list in step with the private directories .gitignore declares: an ignore rule
# states the intent, and this step is what proves the intent held. Review found six of the ten
# unrepresented here.
PRIVPATS='Osborne und Stottmeister|(^|/)refs[^/]*/|(^|/)(additional_)?references[^/]*/'
PRIVPATS="$PRIVPATS|(^|/)papers/|(^|/)citation_screenshots?/|(^|/)citation_shots/|(^|/)shots/"
PRIVPATS="$PRIVPATS|(^|/)cited/pdfs/|(^|/)evidence/|dossier|(^|/)PRIVATE"
BAD=$(objpaths | grep -E "$PRIVPATS" || true)
if [ -z "$BAD" ]; then pass "no third-party or private path in any commit"
else fail "a private path is in the history"; printf '%s\n' "$BAD" | sed 's/^/         /'; fi

# A REF NAME is pushed with the ref and becomes public exactly as a path does, and nothing
# else here reads one: step 3's paths live inside trees, step 4 reads content, and the tag
# check reads a tag's message and tagger but not its name. A branch called PRIVATE-referee-
# dossier, or one named after an address, passed the whole audit. Match the SHORT name: every
# full refname begins with refs/, which the patterns above would match on every ref alike.
REFHIT=$(git for-each-ref --format='%(refname:short)' | grep -E "$PRIVPATS|$SECRETS" || true)
if [ -z "$REFHIT" ]; then
  pass "$(git for-each-ref | wc -l | tr -d ' ') refs, none carrying a private name"
else fail "a branch or tag NAME carries one of these"; printf '%s\n' "$REFHIT" | sed 's/^/         /'; fi

echo "4. no session URL, address or local path, on any branch"
# Three traps, all three of which review demonstrated live.
#   -I skips anything git calls binary, and one NUL byte is enough to earn that label, so a
#   plain text file with a stray NUL hid an address from this grep. Search binaries too.
#   Without -i, a path or address that differs only in case walks through, and step 5's
#   equivalent search has always been case-insensitive, so the pair disagreed.
#   Grepping the worktree reads ONE branch. Steps 2 and 3 read every ref, so a side branch
#   could carry in content what those two would have caught in a name.
# Do not swallow the error. `2>/dev/null ... || true` turns a search that FAILED into an
# empty result, and an empty result reads as a green line: the same fail-open shape as a
# missing tool. git grep exits 0 when it matches, 1 when it does not, and above 1 on error.
set +e
git grep -l -i -E "$SECRETS" $(git rev-list --all) -- . > "$TMP/hits4" 2> "$TMP/err4"
RC4=$?
set -e
HIT=$(sort -u "$TMP/hits4")
if [ "$RC4" -gt 1 ]; then
  fail "the content search itself failed, so step 4 proves nothing"
  head -3 "$TMP/err4" | sed 's/^/         /'
elif [ -z "$HIT" ]; then
  pass "clean across $(git ls-files | wc -l | tr -d ' ') tracked files and all $(git rev-list --all | wc -l | tr -d ' ') commits"
else fail "a file on some branch carries one of these"; echo "$HIT" | sed 's/^/         /'; fi
# An annotated tag is an object of its own: its tagger line and its message are pushed with
# the ref and become public, and no step above reads either, because rev-list enumerates
# commits and trees.
TAGHIT=""
for tg in $(git for-each-ref --format='%(refname)' refs/tags 2>/dev/null); do
  git cat-file -p "$tg" 2>/dev/null | grep -qiE "$SECRETS" && TAGHIT="$TAGHIT$tg "
done
if [ -z "$TAGHIT" ]; then
  pass "$(git for-each-ref refs/tags | wc -l | tr -d ' ') tags, none carrying one in its message or tagger"
else fail "a tag carries one of these: $TAGHIT"; fi

echo
echo "5. binaries: metadata as well as page content"
# TRAP: a PDF can be clean on every rendered page and still carry a local path, an author
# or a producer string in its metadata and its object streams, so a binary has to be read as
# a binary and not through pdftotext alone. Both are checked below, and the SVGs separately:
# a plotting library writes its own name, and sometimes a source path, into a comment.
if ! command -v strings >/dev/null 2>&1; then
  warn "strings not installed; no PDF's metadata or object streams were read at all"
  MET=""
else
  MET=$(pubpdfs | while IFS= read -r f; do strings "$f" | grep -iE "$P_HOME|$P_WS|$P_MAIL" || true; done)
fi
if [ -z "$MET" ]; then pass "$(pubpdfs | wc -l | tr -d ' ') PDFs read; no local path or address in their readable metadata or streams"
else fail "a PDF embeds a local path or address"; echo "$MET" | sed 's/^/         /'; fi
if command -v pdftotext >/dev/null 2>&1; then
  TXT=$(pubpdfs | while IFS= read -r f; do pdftotext "$f" - 2>/dev/null | grep -iE "$P_HOME|$P_SESS" || true; done)
  [ -z "$TXT" ] && pass "no such string in the rendered text either" || { fail "rendered PDF text carries one"; echo "$TXT" | sed 's/^/         /'; }
else warn "pdftotext not installed; the rendered text of every PDF went unchecked"
fi
note "limit: strings cannot read a compressed object stream, so metadata inside one is not"
note "seen here. pdfTeX leaves the Info dict uncompressed, so it is visible today."
SVG=$(grep -l -E "$P_HOME|<!--" docs/figures/*.svg 2>/dev/null || true)
[ -z "$SVG" ] && pass "no comments or paths in the committed SVGs" || { fail "an SVG carries a comment or a path"; echo "$SVG" | sed 's/^/         /'; }

echo
echo "6. authorship"
# --all, not the checked-out branch: steps 2 and 3 read every ref, and an address that
# reaches the remote on a side branch is just as public.
IDS=$(git log --all --format='%ae %ce' | tr ' ' '\n' | sort -u)
if [ "$(echo "$IDS" | grep -cv 'users\.noreply\.github\.com')" -eq 0 ]; then
  pass "every author and committer is the GitHub noreply address"
else fail "a commit carries a real address"; echo "$IDS" | sed 's/^/         /'; fi
N=$(git rev-list --count --all)
# count COMMITS, not lines: a commit message that discusses the trailer as well as carrying
# one would be counted twice by `git log --format=%B | grep -c`.
# A commit MESSAGE is published with the commit. Until now only the session pattern was
# looked for in one, and only the author and committer FIELDS were checked for an address,
# so a message body carrying a local path or an address passed the whole audit.
S=0; C=0; MSGHIT=""
for c in $(git rev-list --all); do
  M=$(git log -1 --format=%B "$c")
  # -E, because P_SESS is an alternation: basic grep would read the | literally and the
  # check would silently never match. Every other use of these patterns already passes -E.
  printf '%s' "$M" | grep -qE "$P_SESS" && S=$((S+1))
  printf '%s' "$M" | grep -qiE "$SECRETS" && MSGHIT="$MSGHIT$(git log -1 --format=%h "$c") "
  printf '%s' "$M" | grep -q 'Co-Authored-By:' && C=$((C+1))
done
if [ -z "$MSGHIT" ]; then pass "no address or local path in any commit message body"
else
  fail "a commit message carries one of these"
  for c in $MSGHIT; do
    git log -1 --format='         %h %s' "$c"
    git log -1 --format=%B "$c" | grep -inE "$SECRETS" | sed 's/^/           line /'
  done
  note "a message cannot be edited without rewriting history, so judge each: text that"
  note "DISCUSSES these patterns is vocabulary, an actual address or path is a leak."
fi
[ "$S" -eq 0 ] && pass "no session URL in any of $N commit messages" || fail "$S commit message(s) carry a session URL"
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
  # Positive control first. Without it, an unauthenticated gh or a network failure answers
  # nothing and every line below reads as "not served".
  # Ask the API for its OWN tip, by the ref name HEAD, which GitHub resolves to the default
  # branch. Two traps this avoids. Asking for the local HEAD's sha cannot tell an unreachable
  # API from a commit that has simply not been pushed yet, and running the audit before
  # pushing is a plausible moment. And git ls-remote is no help here: this script runs inside
  # a clone of the working copy, so its origin is a local path, not GitHub.
  TIP=$(gh api "repos/$SLUG/commits/HEAD" --jq '.sha' 2>&1 || true)
  if printf '%s' "$TIP" | grep -qE '^[0-9a-f]{40}$'; then
    pass "positive control: the API serves its own tip, so a negative answer below means something"
    if [ "$TIP" != "$(git rev-parse HEAD)" ]; then
      warn "the remote tip is $(printf '%s' "$TIP" | cut -c1-7), not this clone's HEAD"
      note "steps 7 and 9 describe the remote; every other step describes this unpushed"
      note "working copy. Push, then re-run, before treating this as a go-ahead."
    fi
  else
    fail "positive control failed: the API did not serve its own tip, so step 7 is inconclusive"
    note "$(printf '%s' "$TIP" | tr '\n' ' ' | head -c 160)"
  fi
  for sha in 69c2afa a66065d 8b4a370; do
    OUT=$(gh api "repos/$SLUG/commits/$sha" --jq '.sha' 2>&1 || true)
    if printf '%s' "$OUT" | grep -qE '^[0-9a-f]{40}$'; then fail "$sha is still served by the remote"
    else pass "$sha is not served"; fi
  done
else warn "gh not installed, so the whole of step 7 went unrun, positive control included"
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
  if command -v node >/dev/null 2>&1; then
    node "$CLONE/tools/check_js.mjs" >/dev/null 2>&1 && pass "browser kernels agree with the Python" || fail "browser kernels disagree with the Python"
    node "$CLONE/tools/check_widgets.mjs" >/dev/null 2>&1 && pass "every widget renders across its control range" || fail "a widget fails to render"
  else warn "node not installed; the browser kernels and every widget went unchecked"
  fi
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
if [ "$FAIL" -ne 0 ]; then
  echo "FAIL: $FAIL blocking finding(s)."
elif [ "$WARN" -ne 0 ]; then
  echo "PASS with $WARN warning(s): no blocking finding, but read them before flipping."
else
  echo "PASS: no blocking finding."
fi
exit "$FAIL"
