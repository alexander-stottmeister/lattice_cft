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

# Every distinct BLOB ever committed whose path matches the given extension, as "<sha> <path>".
# Not a shell glob and not the index: a glob does not descend, and the index is one branch at
# one moment, so a binary committed and then deleted, or committed on a side branch, was never
# opened at all. Deduplicated by sha, because the same bytes at several paths need reading once.
blobsof() {
  for c in $(git rev-list --all); do
    git ls-tree -r "$c" | sed -n 's/^[0-9]* blob \([0-9a-f]*\)	\(.*\)$/\1 \2/p'
  done | grep -iE "\\$1\"?$" | sort -u -k1,1
}

echo "Pre-flight audit of $SLUG"
echo "  clone: $CLONE"
git clone --no-local --quiet "$REPO" "$CLONE"
cd "$CLONE"

echo
echo "0. the committed auditor parses"
# The script that RUNS is the working copy; the script that ships is the one in the clone, and
# they are not the same file. An unterminated string was once committed and pushed while the
# working copy ran fine, so a green audit said nothing about what a reader would get. Parse the
# committed copy of every shell and python tool before trusting anything below.
BADSYN=""
for f in $(git ls-files -- 'tools/*.sh' 'tools/*.py' '*.sh'); do
  case "$f" in
    *.sh) sh -n "$f" 2>/dev/null || BADSYN="$BADSYN$f " ;;
    *.py) python3 -c "import ast,sys; ast.parse(open(sys.argv[1]).read())" "$f" 2>/dev/null || BADSYN="$BADSYN$f " ;;
  esac
done
if [ -z "$BADSYN" ]; then pass "every committed shell and python tool parses"
else fail "a committed tool does not parse: $BADSYN"; fi

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
# -i, for parity with step 4, which was given it for this reason: REFS/, Evidence/ and
# Dossier-2023.txt were all green while .gitignore's protection rests on core.ignorecase,
# which is a property of the filesystem and not of the repository.
BAD=$(objpaths | grep -iE "$PRIVPATS" || true)
if [ -z "$BAD" ]; then pass "no third-party or private path in any commit"
else fail "a private path is in the history"; printf '%s\n' "$BAD" | sed 's/^/         /'; fi

# A REF NAME is pushed with the ref and becomes public exactly as a path does, and nothing
# else here reads one: step 3's paths live inside trees, step 4 reads content, and the tag
# check reads a tag's message and tagger but not its name. A branch called PRIVATE-referee-
# dossier, or one named after an address, passed the whole audit. Match the SHORT name: every
# full refname begins with refs/, which the patterns above would match on every ref alike.
# A submodule's content is not in this repository, so nothing here can speak for it, and its
# declared URL names a repository that may be private. This project has none; if one ever
# appears the audit must say so rather than pass over it in silence.
SUB=$(objpaths | grep -E '(^|/)\.gitmodules$' || true)
if [ -z "$SUB" ]; then pass "no submodule has ever been declared"
else
  fail "a submodule is declared, and this audit cannot read what it points at"
  printf '%s\n' "$SUB" | sed 's/^/         /'
  for c in $(git rev-list --all); do
    git show "$c:.gitmodules" 2>/dev/null | grep -E '^\s*url' | sed 's/^/         /'
  done | sort -u
fi

REFHIT=$(git for-each-ref --format='%(refname:short)' | grep -iE "$PRIVPATS|$SECRETS" || true)
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
# A UTF-16 blob reads as ordinary text after checkout but carries its characters with an
# interleaved zero byte, so an ASCII pattern never matches it. Rather than guess at encodings,
# name any such blob so a person reads it: this repository has none.
U16=""
for c in $(git rev-list --all); do
  git ls-tree -r "$c" | sed -n 's/^[0-9]* blob \([0-9a-f]*\)	\(.*\)$/\1 \2/p'
done | sort -u -k1,1 | while read -r sha path; do
  [ -n "$sha" ] || continue
  B=$(git cat-file blob "$sha" 2>/dev/null | head -c 2 | od -An -tx1 | tr -d ' \n')
  [ "$B" = "fffe" ] || [ "$B" = "feff" ] && printf '%s\n' "$path"
done > "$TMP/u16" || true
if [ -s "$TMP/u16" ]; then
  fail "a UTF-16 blob is in the history; the search above cannot see inside it, so it"
  note "proves nothing about this file. Read it, re-encode it, or excuse it deliberately."
  sort -u "$TMP/u16" | sed 's/^/         /'
else pass "no UTF-16 blob, so the searches above could see every byte"
fi

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
PDFBLOBS=$(blobsof '.pdf')
NPDF=$(printf '%s' "$PDFBLOBS" | grep -c . || true)
MET=""; TXT=""
printf '%s\n' "$PDFBLOBS" | while read -r sha path; do
  [ -n "$sha" ] || continue
  git cat-file blob "$sha" > "$TMP/b.pdf" 2>/dev/null || continue
  command -v strings >/dev/null 2>&1 && strings "$TMP/b.pdf" | grep -iE "$P_HOME|$P_WS|$P_MAIL" | sed "s|^|$path: |"
  command -v pdftotext >/dev/null 2>&1 && pdftotext "$TMP/b.pdf" - 2>/dev/null | grep -iE "$P_HOME|$P_SESS" | sed "s|^|$path: |"
done > "$TMP/pdfhits" || true
# A missing tool must not leave a green line over files nobody read, so each guard reports
# separately and the pass line only claims what was actually done.
HAVE=""
command -v strings   >/dev/null 2>&1 && HAVE="metadata and object streams" || warn "strings not installed; no PDF's metadata or object streams were read"
command -v pdftotext >/dev/null 2>&1 && HAVE="${HAVE:+$HAVE and }rendered text" || warn "pdftotext not installed; no PDF's rendered text was read"
if [ -s "$TMP/pdfhits" ]; then
  fail "a PDF embeds a local path or address"; sed 's/^/         /' "$TMP/pdfhits" | sort -u
elif [ -z "$HAVE" ]; then
  warn "no PDF was read at all, so nothing here is evidence"
else
  pass "$NPDF distinct PDF blobs ever committed, read for $HAVE; clean"
fi
note "limit: strings cannot read a compressed object stream, so metadata inside one is not"
note "seen here. pdfTeX leaves the Info dict uncompressed, so it is visible today."
# The SVGs, over every ref rather than a worktree glob, and counted: the glob did not descend,
# matched nothing at all if the figures ever moved, and its error was swallowed into a pass.
SVGBLOBS=$(blobsof '.svg')
NSVG=$(printf '%s' "$SVGBLOBS" | grep -c . || true)
printf '%s\n' "$SVGBLOBS" | while read -r sha path; do
  [ -n "$sha" ] || continue
  git cat-file blob "$sha" 2>/dev/null | grep -lE "$P_HOME|<!--" >/dev/null 2>&1 && printf '%s\n' "$path"
done > "$TMP/svghits" || true
if [ -s "$TMP/svghits" ]; then
  fail "an SVG carries a comment or a path"; sort -u "$TMP/svghits" | sed 's/^/         /'
elif [ "$NSVG" -eq 0 ]; then
  warn "no SVG was found in any commit, which is not what this repository should look like"
else
  pass "$NSVG distinct SVG blobs ever committed; no comments or paths"
fi

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
# Two messages DESCRIBE the patterns they added and so carry the vocabulary without carrying a
# leak. That is the self-reference step 4 had to solve; the script solves it by assembling its
# patterns from fragments, and prose cannot do that and stay readable. A message cannot be
# reworded without rewriting history and re-creating the remote, which is the author's
# decision, not this script's. So each is named here, having been read, and printed on every
# run. Adding to this list is a deliberate act and it is the only way past this check.
MSG_VOCAB="4d7ca11414795072198fff46cd61bfa68d5346e1 6d0161ad22757f56b429f431ae4e1b5a29fd66d4"
S=0; C=0; MSGHIT=""; MSGSKIP=0
for c in $(git rev-list --all); do
  M=$(git log -1 --format=%B "$c")
  # -E, because P_SESS is an alternation: basic grep would read the | literally and the
  # check would silently never match. Every other use of these patterns already passes -E.
  printf '%s' "$M" | grep -qE "$P_SESS" && S=$((S+1))
  # The excusal covers THIS check only. A listed commit is still counted for its trailer and
  # still searched for a session URL, because excusing vocabulary is not excusing the commit.
  case " $MSG_VOCAB " in
    *" $c "*) MSGSKIP=$((MSGSKIP+1));;
    *) printf '%s' "$M" | grep -qiE "$SECRETS" && MSGHIT="$MSGHIT$(git log -1 --format=%h "$c") ";;
  esac
  printf '%s' "$M" | grep -q 'Co-Authored-By:' && C=$((C+1))
done
if [ -z "$MSGHIT" ]; then
  pass "no address or local path in any commit message body ($MSGSKIP read and excused below)"
  for c in $MSG_VOCAB; do git log -1 --format='         excused: %h %s' "$c" 2>/dev/null; done
  note "each was read: it quotes the patterns it added, which is vocabulary and not a leak."
  note "Rewording needs history rewritten and the remote re-created; that is a decision."
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
  # Everything above audits THIS clone. What becomes public is the remote, so a branch that
  # exists only there is outside the whole audit. Compare the two sets of names.
  RREFS=$(gh api "repos/$SLUG/branches" --jq '.[].name' 2>/dev/null | sort -u || true)
  LREFS=$(git for-each-ref --format='%(refname:short)' refs/heads refs/remotes 2>/dev/null \
          | sed 's|^origin/||' | sort -u)
  printf '%s\n' "$RREFS" | sed '/^$/d' > "$TMP/rrefs"
  printf '%s\n' "$LREFS" | sed '/^$/d' > "$TMP/lrefs"
  ONLY=$(comm -23 "$TMP/rrefs" "$TMP/lrefs")
  if [ -z "$RREFS" ]; then warn "could not list the remote's branches; only this clone was audited"
  elif [ -z "$ONLY" ]; then pass "the remote has no branch this clone lacks"
  else fail "the remote carries a branch this audit never saw"; printf '%s\n' "$ONLY" | sed 's/^/         /'; fi

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
