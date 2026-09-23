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
# Every search here runs in the C locale. git grep in a UTF-8 locale stops at the first
# invalid byte of a line, so an ordinary single-byte-encoded note -- no NUL, so not named by
# the binary rule -- hid an address and a home path from step 4 on this machine while the
# same clone and the same script found both under LC_ALL=C. It also makes sort and comm
# order bytes rather than collate, which is what the set comparisons in steps 1 and 7 assume.
export LC_ALL=C

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
# Every root whose tree has to be walked. `git rev-list --all` lists COMMITS, and a tag may
# point straight at a TREE, which publishes that tree and every blob under it while no loop
# here reaches them. Such a tag travels in a clone. The enumeration this script replaced did
# list those blobs, so the fix for the duplicate-blob defect is what opened the hole.
allroots() {
  git rev-list --all
  git for-each-ref --format='%(objectname)' 2>/dev/null | while read -r o; do
    [ -n "$o" ] || continue
    ty=$(git cat-file -t "$o" 2>/dev/null)
    if [ "$ty" = "tag" ]; then
      o=$(git rev-parse "$o^{}" 2>/dev/null) || continue
      ty=$(git cat-file -t "$o" 2>/dev/null)
    fi
    [ "$ty" = "tree" ] && printf '%s\n' "$o"
  done
}

objpaths() {
  for c in $(allroots); do git ls-tree -r --name-only "$c"; done \
    | sed 's/^"//; s/"$//' | sort -u
}

# Every distinct BLOB ever committed whose path matches the given extension, as "<sha> <path>".
# Not a shell glob and not the index: a glob does not descend, and the index is one branch at
# one moment, so a binary committed and then deleted, or committed on a side branch, was never
# opened at all. Deduplicated by sha, because the same bytes at several paths need reading once.
blobsof() {
  for c in $(allroots); do
    git ls-tree -r "$c" | sed -n 's/^[0-9]* blob \([0-9a-f]*\)	\(.*\)$/\1 \2/p'
  done | grep -iE "\\$1\"?$" | sort -u -k1,1
}

echo "Pre-flight audit of $SLUG"
echo "  clone: $CLONE"
git clone --no-local --quiet "$REPO" "$CLONE"
cd "$CLONE"

# Which .pdf-named blobs really are PDFs. The exclusion in step 4 is by extension while the
# readers in step 5 are not, so a gzip named .pdf was skipped by one and counted as read by
# the other. Decide once, by the magic bytes, and let both steps use the answer.
: > "$TMP/realpdf"; : > "$TMP/fakepdf"
blobsof '.pdf' | while read -r sha path; do
  [ -n "$sha" ] || continue
  # Within the first kilobyte, not at byte zero: a reader accepts a header that is preceded
  # by other bytes, so a five-byte test at offset zero decided a genuine document was not one
  # and no reader ever opened it.
  if git cat-file blob "$sha" 2>/dev/null | head -c 1024 | LC_ALL=C grep -q '%PDF-'; then
    printf '%s\n' "$sha" >> "$TMP/realpdf"
  else
    printf '%s %s\n' "$sha" "$path" >> "$TMP/fakepdf"
  fi
done || true

echo
echo "0. the committed auditor parses"
# The script that RUNS is the working copy; the script that ships is the one in the clone, and
# they are not the same file. An unterminated string was once committed and pushed while the
# working copy ran fine, so a green audit said nothing about what a reader would get. Parse the
# committed copy of every shell and python tool before trusting anything below.
# EVERY committed script, wherever it sits. A pathspec of tools/ plus the root once selected
# 8 of the 34, leaving the generator at the root, the numerics and the site's own JavaScript
# unparsed while the line claimed all of them.
# -c core.quotepath=false and a read loop, not `for f in $(...)`. Word splitting turned a
# valid "my tool.sh" into a failure on a path that does not exist, while never parsing the
# real file; and git quotes a non-ASCII path by default, so the anchored pattern skipped it
# and a BROKEN script at HEAD was reported as parsing. That is the defect this step exists to
# name, in this step.
python3 - "$TMP" <<'PYEND' > "$TMP/headsyn"
import ast, os, subprocess, sys
tmp = sys.argv[1]
names = subprocess.run(["git","ls-files","-z"], capture_output=True).stdout.split(b"\0")
bad, n, unparsed = [], 0, []
have_node = subprocess.run(["sh","-c","command -v node"], capture_output=True).returncode == 0
for raw in names:
    if not raw: continue
    low = raw.lower()
    # -z gives raw bytes, so no quoting to undo, and the extension is matched without regard
    # to case: the blocking half once selected case-sensitively while the warning half did not.
    if low.endswith(b".sh"):
        n += 1
        if subprocess.run(["sh","-n",raw], capture_output=True).returncode: bad.append(raw)
    elif low.endswith(b".py"):
        n += 1
        try: ast.parse(open(raw,"rb").read())
        except SyntaxError: bad.append(raw)
    elif low.endswith(b".js") or low.endswith(b".mjs"):
        if have_node:
            n += 1
            if subprocess.run(["node","--check",raw], capture_output=True).returncode: bad.append(raw)
        else: unparsed.append(raw)
print(n)
print(len(unparsed))
for b in bad: os.write(1, b"BAD " + b + b"\n")
PYEND
NSYN=$(sed -n 1p "$TMP/headsyn"); NJS=$(sed -n 2p "$TMP/headsyn")
BADSYN=$(sed -n '3,$p' "$TMP/headsyn" | sed 's/^BAD //')
if [ -n "$BADSYN" ]; then
  fail "a committed script does not parse"; printf '%s\n' "$BADSYN" | sed 's/^/         /'
else pass "$NSYN scripts parse at HEAD"; fi
# HEAD is what ships, but every script blob in the history is published too, and the index
# speaks for one branch at one moment -- the defect removed from step 5 and left here. Parse
# them all. A broken blob that is not at HEAD is a historical artefact rather than a defect in
# what ships, so it is named rather than blocking.
: > "$TMP/oldsyn"
for c in $(allroots); do
  git ls-tree -r "$c" | sed -n 's/^[0-9]* blob \([0-9a-f]*\)	\(.*\)$/\1 \2/p'
done | grep -iE '\.(sh|py|mjs|js)"?$' | sort -u -k1,1 | while read -r sha path; do
  [ -n "$sha" ] || continue
  git cat-file blob "$sha" > "$TMP/blob.src" 2>/dev/null || continue
  # Strip the quotes ls-tree adds to a path with an unusual character before deciding what
  # this is: the grep above allows the trailing quote and the case below forbade it, so such
  # a blob was read and then dropped, counted as parsed without ever being parsed. The same
  # gap swallowed every .js and .mjs, which is four of the files the published site serves.
  clean=$(printf '%s' "$path" | sed 's/^"//; s/"$//' | tr 'A-Z' 'a-z')
  case "$clean" in
    *.sh)  sh -n "$TMP/blob.src" 2>/dev/null || printf '%s %s\n' "$sha" "$path" >> "$TMP/oldsyn" ;;
    *.py)  python3 -c "import ast,sys; ast.parse(open(sys.argv[1]).read())" "$TMP/blob.src" 2>/dev/null || printf '%s %s\n' "$sha" "$path" >> "$TMP/oldsyn" ;;
    *.mjs|*.js)
      if command -v node >/dev/null 2>&1; then
        cp "$TMP/blob.src" "$TMP/blob.mjs"
        node --check "$TMP/blob.mjs" 2>/dev/null || printf '%s %s\n' "$sha" "$path" >> "$TMP/oldsyn"
      fi ;;
  esac
done || true
if [ -s "$TMP/oldsyn" ]; then
  warn "$(grep -c . < "$TMP/oldsyn" || true) script blob(s) in the history do not parse"
  while read -r sha path; do
    printf '         %s %s  (in %s)\n' "$(printf '%s' "$sha" | cut -c1-7)" "$path" \
      "$(git log --all --oneline --find-object="$sha" | tail -1 | cut -d' ' -f1)"
  done < "$TMP/oldsyn"
  note "a broken intermediate version is published with the history; it is not what ships."
else pass "every script blob in the history parses too"
fi
[ "${NJS:-0}" -gt 0 ] && warn "node not installed; $NJS JavaScript files went unparsed"
note "sh -n and node --check are parsers: they do not resolve a name, so a call to a function"
note "that no longer exists parses cleanly. Step 2 once shipped exactly that." 

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
# By extension AND by leading bytes: the project's own third-party PDF committed under another
# suffix drew a clean line here while step 4 blocked it on an unrelated ground, two checks
# disagreeing about one object.
UNEXPECTED=$(objpaths | grep -i '\.pdf$' | grep -v '^docs/pdf/' || true)
# Drop the allowed directory BEFORE deduplicating, not after. `sort -u -k1,1` keeps one line
# per blob, so a real document at a private path that is byte-identical to an allowed one
# survived only under the allowed path and the filter then removed it entirely: the same
# enumeration defect this script has now fixed twice, back inside the check written to close
# it. Quoting is off, so the filter sees the real path.
for c in $(allroots); do
  git -c core.quotepath=false ls-tree -r "$c" | sed -n 's/^[0-9]* blob \([0-9a-f]*\)	\(.*\)$/\1 \2/p'
done | awk '{ s=$1; i=index($0," "); pth=substr($0,i+1); if (index(pth,"docs/pdf/")!=1) print s" "pth }' \
  | sort -u > "$TMP/outside" || true
: > "$TMP/pdfbytes"
while read -r sha path; do
  [ -n "$sha" ] || continue
  git cat-file blob "$sha" 2>/dev/null | head -c 1024 | LC_ALL=C grep -q '%PDF-' && printf '%s\n' "$path" >> "$TMP/pdfbytes"
done < "$TMP/outside" || true
UNEXPECTED=$(printf '%s\n' "$UNEXPECTED"; cat "$TMP/pdfbytes")
UNEXPECTED=$(printf '%s\n' "$UNEXPECTED" | sed '/^$/d' | sort -u)
if [ -z "$UNEXPECTED" ]; then
  pass "only docs/pdf/ ever held a PDF; $(blobsof '.pdf' | grep -c . || true) distinct PDF blobs in all"
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
  for c in $(allroots); do
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
git grep -l -i -E "$SECRETS" $(allroots) -- . > "$TMP/hits4" 2> "$TMP/err4"
RC4=$?
set -e
HIT=$(sort -u "$TMP/hits4")
if [ "$RC4" -gt 1 ]; then
  fail "the content search itself failed, so step 4 proves nothing"
  head -3 "$TMP/err4" | sed 's/^/         /'
elif [ -z "$HIT" ]; then
  pass "clean across $(git ls-files | wc -l | tr -d ' ') tracked files and all $(git rev-list --all | wc -l | tr -d ' ') commits"
else fail "a file on some branch carries one of these"; echo "$HIT" | sed 's/^/         /'; fi
# The search above reads bytes as text, so it is blind to any blob holding a NUL. A byte-order
# mark was the first attempt at naming those and was the wrong predicate: UTF-16 without a BOM
# is invisible to it, UTF-32BE evades it even with one, and a gzip, a zip or a PNG text chunk
# were never in scope at all. Review planted all three carrying a real address and they passed.
# Use git's own rule, a NUL byte in the first 8000, and name every such blob except the PDFs,
# which step 5 opens with readers of their own.
for c in $(allroots); do
  git ls-tree -r "$c" | sed -n 's/^[0-9]* blob \([0-9a-f]*\)	\(.*\)$/\1 \2/p'
done | sort -u -k1,1 | while read -r sha path; do
  [ -n "$sha" ] || continue
  # Skip only a blob that really is a PDF and so is read by step 5's own readers. Skipping by
  # extension let a gzip named .pdf through both: past this test for its name, and counted by
  # step 5 as read when neither reader could decode it.
  grep -qx "$sha" "$TMP/realpdf" 2>/dev/null && continue
  # The WHOLE blob, not git's first-8000-bytes heuristic. That bound is right for deciding how
  # to diff a file and wrong for a claim about what the searches could read: nine thousand
  # bytes of ordinary prose followed by an address in a wide encoding, or a compressed member
  # in the same position, passed both this rule and the pattern search, and the line said
  # every blob was readable end to end. If the claim is end to end, the test has to be too.
  N=$(git cat-file blob "$sha" 2>/dev/null | wc -c | tr -d ' ')
  Z=$(git cat-file blob "$sha" 2>/dev/null | LC_ALL=C tr -d '\000' | wc -c | tr -d ' ')
  [ "$N" != "$Z" ] && printf '%s\n' "$path"
done > "$TMP/binblob" || true
if [ -s "$TMP/binblob" ]; then
  fail "a blob the content search cannot read is in the history, so step 4 says nothing of it"
  sort -u "$TMP/binblob" | sed 's/^/         /'
  note "read it, re-encode it as text, or excuse it deliberately."
else pass "apart from the PDFs, every blob is text the searches above could read end to end"
fi

# A SYMLINK's content is its target, and git grep over a revision skips mode 120000, so a
# link pointing at a private absolute path was read by nothing: only its own name reached
# step 3. Read every link target ever committed.
for c in $(allroots); do
  git ls-tree -r "$c" | sed -n 's/^120000 blob \([0-9a-f]*\)	\(.*\)$/\1 \2/p'
done | sort -u > "$TMP/links" || true   # by line, not by blob: two links sharing one target are two links
: > "$TMP/linkhits"
while read -r sha path; do
  [ -n "$sha" ] || continue
  TGT=$(git cat-file blob "$sha" 2>/dev/null)
  printf '%s' "$TGT" | grep -qiE "$SECRETS|$PRIVPATS" && printf '%s -> %s\n' "$path" "$TGT" >> "$TMP/linkhits"
done < "$TMP/links" || true
if [ -s "$TMP/linkhits" ]; then
  fail "a symlink points somewhere private"; sort -u "$TMP/linkhits" | sed 's/^/         /'
else pass "$(grep -c . < "$TMP/links" || true) symlinks ever committed, none pointing anywhere private"
fi

# An annotated tag is an object of its own: its tagger line and its message are pushed with
# the ref and become public, and no step above reads either, because rev-list enumerates
# commits and trees.
# cat-file -p on a tag prints the tag object; ^{} dereferences it to whatever it finally
# points at, which may be a BLOB, and a tag pointing straight at a blob publishes content that
# no tree contains and nothing else here reads.
TAGHIT=""
for tg in $(git for-each-ref --format='%(refname)' refs/tags 2>/dev/null); do
  git cat-file -p "$tg" 2>/dev/null | grep -qiE "$SECRETS" && TAGHIT="$TAGHIT$tg "
  if [ "$(git cat-file -t "${tg}^{}" 2>/dev/null)" = "blob" ]; then
    git cat-file blob "${tg}^{}" 2>/dev/null | grep -qiE "$SECRETS" && TAGHIT="$TAGHIT${tg}(blob) "
  fi
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
if [ -s "$TMP/fakepdf" ]; then
  fail "a file named .pdf is not a PDF, so neither reader below can decode it"
  sed 's/^/         /' "$TMP/fakepdf"
else pass "every .pdf blob really is a PDF, so the readers below can decode all of them"
fi
PDFBLOBS=$(blobsof '.pdf')
NPDF=$(printf '%s' "$PDFBLOBS" | grep -c . || true)
MET=""; TXT=""; : > "$TMP/unread"
printf '%s\n' "$PDFBLOBS" | while read -r sha path; do
  [ -n "$sha" ] || continue
  git cat-file blob "$sha" > "$TMP/b.pdf" 2>/dev/null || continue
  command -v strings >/dev/null 2>&1 && strings "$TMP/b.pdf" | grep -iE "$SECRETS" | awk -v p="$path" '{print p": "$0}'
  # Require the reader to have SUCCEEDED. Five magic bytes followed by anything, or a document
  # truncated past its trailer, were counted among the files "read" while neither reader could
  # decode a word of them. A file nobody could read is not a clean file.
  if command -v pdftotext >/dev/null 2>&1; then
    # Not just non-empty: pdftotext exits 0 and writes a single form feed for a page with no
    # extractable text, so an image-only page -- which is exactly the shape of a scanned page
    # image -- satisfied a size test while nothing had been read from it. Require a character
    # that is not whitespace.
    # PER PAGE. The defect this replaced is per-page -- a page carried as an image yields
    # nothing while the pages around it yield plenty -- and testing the whole document only
    # asks whether SOME page could be read. A scanned appendix inside a typeset document is
    # the commoner shape, and it passed under a line saying the document had been read.
    NP=$(pdfinfo "$TMP/b.pdf" 2>/dev/null | awk '/^Pages/{print $2}')
    case "$NP" in ''|*[!0-9]*) NP=0;; esac
    if [ "$NP" -lt 1 ]; then
      printf '%s\n' "UNREADABLE $path: no page count could be read" >> "$TMP/unread"
    else
      BADP=""; : > "$TMP/b.all"; PG=1
      while [ "$PG" -le "$NP" ]; do
        pdftotext -f "$PG" -l "$PG" "$TMP/b.pdf" "$TMP/b.txt" 2>/dev/null || true
        if [ -n "$(tr -d '[:space:]' < "$TMP/b.txt" 2>/dev/null | head -c 1)" ]; then
          cat "$TMP/b.txt" >> "$TMP/b.all"
        else
          BADP="$BADP$PG "
        fi
        PG=$((PG+1))
      done
      [ -n "$BADP" ] && printf '%s\n' "UNREADABLE $path: page(s) $BADP yielded no text at all" >> "$TMP/unread"
      grep -iE "$SECRETS" "$TMP/b.all" | awk -v p="$path" '{print p": "$0}'
    fi
  fi
done > "$TMP/pdfhits" || true
# A missing tool must not leave a green line over files nobody read, so each guard reports
# separately and the pass line only claims what was actually done.
HAVE=""
command -v strings   >/dev/null 2>&1 && HAVE="metadata and object streams" || warn "strings not installed; no PDF's metadata or object streams were read"
command -v pdftotext >/dev/null 2>&1 && HAVE="${HAVE:+$HAVE and }rendered text" || warn "pdftotext not installed; no PDF's rendered text was read"
if [ -s "$TMP/unread" ]; then
  fail "a PDF could not be read at all, so calling it clean would mean nothing"
  sort -u "$TMP/unread" | sed 's/^/         /'
fi
if [ -s "$TMP/pdfhits" ]; then
  fail "a PDF embeds a local path or address"; sed 's/^/         /' "$TMP/pdfhits" | sort -u
elif [ -s "$TMP/unread" ]; then
  : # already reported above; do not follow a failure with a line calling the same files clean
elif [ -z "$HAVE" ]; then
  warn "no PDF was read at all, so nothing here is evidence"
else
  pass "$NPDF distinct PDF blobs ever committed, read for $HAVE; clean"
fi
note "limit: strings cannot read a compressed object stream, so metadata inside one is not"
note "seen here. pdfTeX leaves the Info dict uncompressed, so it is visible today."
# The SVGs, over every ref rather than a worktree glob, and counted: the glob did not descend,
# matched nothing at all if the figures ever moved, and its error was swallowed into a pass.
# Both searches above now use the whole pattern set. They used two different subsets, with the
# institutional address in neither, so a page whose text carried one inside a compressed stream
# -- invisible to the byte search and to step 4 -- was reported clean.
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
# A commit object carries four identity fields and only the two addresses were ever read.
# An author NAME that is an address, and a committer NAME that is a home path, both travel in
# a clone and are printed beside every commit, and passed under a line about the noreply
# address. The tag check beside this one already reads a whole tag object, tagger included.
NAMEHIT=$(git log --all --format='%an%n%cn' | sort -u | grep -iE "$SECRETS" || true)
if [ -z "$NAMEHIT" ]; then pass "no author or committer NAME carries an address or a path"
else fail "an author or committer name carries one of these"; printf '%s\n' "$NAMEHIT" | sed 's/^/         /'; fi
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
  # A listed sha will not survive the history rewrite this node's trailer notice contemplates.
  # Without this guard git log exits 128 on a missing object and set -e kills the run inside
  # step 6, after a green line and before any verdict is printed.
  for c in $MSG_VOCAB; do
    if git cat-file -e "${c}^{commit}" 2>/dev/null; then
      git log -1 --format='         excused: %h %s' "$c"
    else
      warn "excused commit $c is not in this history; the list is stale after a rewrite"
    fi
  done
  note "both were read. 6d0161a quotes bare domains and a path fragment, with no local part"
  note "and no user name: vocabulary. 4d7ca11 names an EXAMPLE branch that is a syntactically"
  note "complete address; it is fabricated and is not the author's, so publishing it is a"
  note "knowing decision rather than a leak. Rewording either needs history rewritten and the"
  note "remote re-created."
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
      # Two situations give the same mismatch and they are not equally serious. The clone
      # already holds the remote's tip when this copy is merely ahead; it does not when the
      # remote carries commits nobody here has read.
      if git cat-file -e "$TIP" 2>/dev/null; then
        note "this copy is ahead of the remote. Push, then re-run before treating this as a"
        note "go-ahead: steps 7 and 9 describe the remote, every other step describes here."
      else
        fail "the remote carries commits this clone does not have, so they were never audited"
      fi
    fi
  else
    fail "positive control failed: the API did not serve its own tip, so step 7 is inconclusive"
    note "$(printf '%s' "$TIP" | tr '\n' ' ' | head -c 160)"
  fi
  # Everything above audits THIS clone. What becomes public is the remote, so a branch that
  # exists only there is outside the whole audit. Compare the two sets of names.
  # --paginate: without it the API returns one page, so only the first 30 branches were ever
  # compared and a 31st gave a clean line.
  RREFS=$(gh api --paginate "repos/$SLUG/branches" --jq '.[].name' 2>/dev/null | sort -u || true)
  LREFS=$(git for-each-ref --format='%(refname:short)' refs/heads refs/remotes 2>/dev/null \
          | sed 's|^origin/||' | sort -u)
  printf '%s\n' "$RREFS" | sed '/^$/d' > "$TMP/rrefs"
  printf '%s\n' "$LREFS" | sed '/^$/d' > "$TMP/lrefs"
  ONLY=$(comm -23 "$TMP/rrefs" "$TMP/lrefs")
  if [ -z "$RREFS" ]; then warn "could not list the remote's branches; only this clone was audited"
  elif [ -z "$ONLY" ]; then pass "the remote has no branch this clone lacks"
  else fail "the remote carries a branch this audit never saw"; printf '%s\n' "$ONLY" | sed 's/^/         /'; fi
  # Tags too: this script already treats a local annotated tag as a publication surface.
  # Fail closed, as the branch comparison beside it does. With only this call failing the step
  # printed a clean line over an answer it never received.
  # Capture the API's OWN status. Taken after a pipeline it was sort's status, which is
  # always zero, so the guard below could never fire and the step stayed fail-open.
  set +e; gh api --paginate "repos/$SLUG/tags" --jq '.[].name' > "$TMP/rtags.raw" 2>/dev/null; RCT=$?; set -e
  RTAGS=$(sort -u "$TMP/rtags.raw" 2>/dev/null)
  git for-each-ref --format='%(refname:short)' refs/tags | sort -u > "$TMP/ltags"
  printf '%s\n' "$RTAGS" | sed '/^$/d' > "$TMP/rtags"
  ONLYT=$(comm -23 "$TMP/rtags" "$TMP/ltags")
  if [ "$RCT" -ne 0 ]; then warn "could not list the remote's tags, so none were compared"
  elif [ -z "$ONLYT" ]; then pass "the remote has no tag this clone lacks"
  else fail "the remote carries a tag this audit never saw"; printf '%s\n' "$ONLYT" | sed 's/^/         /'; fi

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
  # TRAP: `git diff --quiet` cannot tell "regenerated identically" from "not regenerated at
  # all". A generator given an early exit wrote nothing and the step still passed. So overwrite
  # every generated file with a sentinel first: a generator that does not run leaves its
  # sentinel behind and the diff fails. Silence is no longer a pass.
  SENT=0
  for g in "$CLONE"/docs/figures/*.svg "$CLONE"/docs/data/*.json "$CLONE"/docs/reference/*.html \
           "$CLONE"/docs/reference/results.md "$CLONE"/docs/pdf/*.pdf "$CLONE"/mainrefs.tex; do
    [ -f "$g" ] || continue
    printf 'PREFLIGHT SENTINEL\n' > "$g"; SENT=$((SENT+1))
  done
  note "$SENT fully generated files overwritten with a sentinel before the rebuild"
  # Two files are SPLICED rather than written whole: the generator reads them, replaces the
  # text between two markers and writes them back. A sentinel would destroy the markers and
  # make the generator fail rather than prove it ran, so these are timestamped instead. Both
  # were outside the sentinel list entirely, so a sync_docs.py that stopped writing them was
  # not caught by the check written to catch exactly that.
  SPLICED="IMPROVEMENT-PLAN.md CHANGES-v4-to-v5.md"
  for s in $SPLICED; do [ -f "$CLONE/$s" ] && touch -t 200001010000 "$CLONE/$s"; done
  # tools/build_pdfs.sh is what produces the three PDFs under docs/pdf/, with the fixed epoch
  # that makes them reproducible. Step 8 used to compile into build/ and never run it, so the
  # three files a reader actually downloads were the ones its byte-identity claim did not
  # cover. The sentinel above is what exposed that.
  # Order matters and the sentinel is what proved it. The two notes \input mainrefs.tex, which
  # sync_docs.py generates from the paper's compiled aux, so the paper must be compiled first,
  # then sync_docs.py run, and only then the three documents built. Building them first left
  # the notes compiling against a sentinel and one PDF never written at all.
  # Chain with && rather than relying on errexit. The subshell is the condition of an `if`,
  # and a shell suppresses errexit for a condition -- including inside a subshell there -- so
  # `set -e` in it is ignored and only the LAST generator's status survived. A generator made
  # to write everything and then exit 1 left the step fully green. With &&, the chain stops at
  # the first failure and that failure is the subshell's status.
  # The two bare compiles are for the cross-reference data only and are allowed to fail: the
  # three published documents are built by tools/build_pdfs.sh, which runs under its own
  # errexit, and the reference generator says so when the comparison data is absent.
  if ( cd "$CLONE" && mkdir -p build \
       && { pdflatex -interaction=nonstopmode -output-directory=build free_fermion_cft_v5.tex >/dev/null 2>&1 || true; } \
       && { pdflatex -interaction=nonstopmode -output-directory=build free_fermion_cft_v5.tex >/dev/null 2>&1 || true; } \
       && python3 sync_docs.py \
       && sh tools/build_pdfs.sh \
       && { pdflatex -interaction=nonstopmode -output-directory=build free_fermion_cft_v4.tex >/dev/null 2>&1 || true; } \
       && { pdflatex -interaction=nonstopmode -output-directory=build free_fermion_cft_v4.tex >/dev/null 2>&1 || true; } \
       && python3 sync_docs.py \
       && python3 tools/make_data.py \
       && python3 tools/make_figures.py \
       && python3 tools/build_reference.py ) > "$TMP/buildlog" 2>&1; then :
  else fail "the rebuild itself failed"; tail -8 "$TMP/buildlog" | sed 's/^/         /'
  fi
  STALE=""
  for s in $SPLICED; do
    [ -f "$CLONE/$s" ] || continue
    [ -n "$(find "$CLONE/$s" -newermt '2001-01-01' 2>/dev/null)" ] || STALE="$STALE$s "
  done
  [ -z "$STALE" ] || { fail "a spliced file was never rewritten by the rebuild: $STALE"; }
  LEFT=$( { grep -rl '^PREFLIGHT SENTINEL$' "$CLONE"/docs 2>/dev/null; grep -l '^PREFLIGHT SENTINEL$' "$CLONE"/mainrefs.tex 2>/dev/null; } | wc -l | tr -d ' ')
  [ "$LEFT" = "0" ] || { fail "$LEFT generated file(s) were never rewritten by the rebuild"; { grep -rl '^PREFLIGHT SENTINEL$' "$CLONE"/docs; grep -l '^PREFLIGHT SENTINEL$' "$CLONE"/mainrefs.tex 2>/dev/null; } | sed "s|$CLONE/|         |"; }
  if git -C "$CLONE" diff --quiet; then pass "all $SENT generated and $(printf '%s' "$SPLICED" | wc -w | tr -d ' ') spliced files were rewritten and are byte-identical"
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
  # has_pages belongs here above all: enabling Pages IS the visibility change step 10 is
  # about, and the line that omitted it was the one a reader would check for exactly that.
  gh api "repos/$SLUG" --jq '"         private=\(.private) pages=\(.has_pages) wiki=\(.has_wiki) issues=\(.has_issues) branch=\(.default_branch) forks=\(.forks_count) description=\(.description // "none")"' \
    || warn "could not read the remote settings, so step 9 shows nothing rather than nothing to show"
  # The repository's own prose becomes public with it, and nothing here read any of it. A
  # description, a homepage, a topic, an issue or a release note is published exactly as a
  # file is, and none of them is in any tree, so no step above can reach them.
  set +e
  gh api "repos/$SLUG" --jq '"\(.description // "")\n\(.homepage // "")\n\(.topics|join(" "))"' > "$TMP/meta" 2>/dev/null
  RM1=$?
  gh api --paginate "repos/$SLUG/issues?state=all" --jq '.[] | "\(.title)\n\(.body // "")"' >> "$TMP/meta" 2>/dev/null
  RM2=$?
  gh api --paginate "repos/$SLUG/releases" --jq '.[] | "\(.name // "")\n\(.body // "")\n\((.assets // [])|map(.name)|join(" "))"' >> "$TMP/meta" 2>/dev/null
  RM3=$?
  # Each of these is a separate endpoint and each is published exactly as an issue body is.
  # An issue's own payload carries a comment COUNT, not the comment text, so the comments have
  # to be asked for by themselves.
  gh api --paginate "repos/$SLUG/issues/comments" --jq '.[].body // ""' >> "$TMP/meta" 2>/dev/null
  RM4=$?
  gh api --paginate "repos/$SLUG/pulls/comments" --jq '.[].body // ""' >> "$TMP/meta" 2>/dev/null
  RM5=$?
  gh api --paginate "repos/$SLUG/comments" --jq '.[].body // ""' >> "$TMP/meta" 2>/dev/null
  RM6=$?
  set -e
  if [ "$RM1" -ne 0 ] || [ "$RM2" -ne 0 ] || [ "$RM3" -ne 0 ] \
     || [ "$RM4" -ne 0 ] || [ "$RM5" -ne 0 ] || [ "$RM6" -ne 0 ]; then
    warn "could not read all of the remote's own prose, so some of it went unchecked"
  elif grep -qiE "$SECRETS" "$TMP/meta"; then
    fail "the remote's own prose carries one of these"
    grep -inE "$SECRETS" "$TMP/meta" | sed 's/^/         /'
  else
    pass "the remote's description, topics, issues, comments, releases and assets are clean"
  fi
  note "decide each of these deliberately; enabling Pages is itself the flip"
else
  warn "gh not installed; the remote's settings and its own prose went unchecked"
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
