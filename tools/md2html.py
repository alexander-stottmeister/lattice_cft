"""A small Markdown-to-HTML converter, for the reference pages only.

The site sets .nojekyll, so GitHub Pages serves files verbatim and does not render Markdown.
Without this the reference folder is a repository-view artifact: `docs/reference/` would 404
under Pages and `results.md` would be served as plain text. The pages are therefore written
once as Markdown, which GitHub renders when browsing the repository, and rendered to HTML
here for the site.

Supports exactly what those pages use: ATX headings, paragraphs, pipe tables, unordered and
ordered lists, blockquotes, fenced code, horizontal rules, and inline code, emphasis, strong
and links. Nothing else; it is not a general Markdown implementation and does not try to be.
Links ending in .md are rewritten to .html so the rendered pages link to each other.
"""
import html
import re

__all__ = ["md_to_html", "page"]

_INLINE_CODE = re.compile(r"`([^`]+)`")
_STRONG = re.compile(r"\*\*([^*]+)\*\*")
_EM = re.compile(r"(?<![*\w])\*([^*\n]+)\*(?!\*)")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def _inline(s):
    out, last = [], 0
    for m in _INLINE_CODE.finditer(s):          # code spans first: nothing inside them is markup
        out.append(_markup(html.escape(s[last:m.start()], quote=False)))
        out.append("<code>%s</code>" % html.escape(m.group(1), quote=False))
        last = m.end()
    out.append(_markup(html.escape(s[last:], quote=False)))
    return "".join(out)


def _href(u):
    return re.sub(r"\.md(?=$|#)", ".html", u)


def _markup(s):
    s = _LINK.sub(lambda m: '<a href="%s">%s</a>' % (html.escape(_href(m.group(2)), quote=True), m.group(1)), s)
    s = _STRONG.sub(r"<strong>\1</strong>", s)
    s = _EM.sub(r"<em>\1</em>", s)
    return s


def _table(rows):
    head, body = rows[0], rows[2:]
    cells = lambda r: [c.strip() for c in r.strip().strip("|").split("|")]
    out = ["<table>", "<thead><tr>"]
    out += ["<th>%s</th>" % _inline(c) for c in cells(head)]
    out += ["</tr></thead>", "<tbody>"]
    for r in body:
        out.append("<tr>" + "".join("<td>%s</td>" % _inline(c) for c in cells(r)) + "</tr>")
    out += ["</tbody>", "</table>"]
    return "\n".join(out)


def md_to_html(md):
    lines = md.split("\n")
    out, i = [], 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
            continue
        if ln.startswith("```"):                                     # fenced code
            j = i + 1
            buf = []
            while j < len(lines) and not lines[j].startswith("```"):
                buf.append(lines[j]); j += 1
            out.append("<pre><code>%s</code></pre>" % html.escape("\n".join(buf), quote=False))
            i = j + 1
            continue
        if re.match(r"^#{1,6} ", ln):                                # heading
            n = len(ln) - len(ln.lstrip("#"))
            out.append("<h%d>%s</h%d>" % (n, _inline(ln[n:].strip()), n))
            i += 1
            continue
        if re.match(r"^\s*[-*]{3,}\s*$", ln):
            out.append("<hr>"); i += 1; continue
        if ln.lstrip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            j = i
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                j += 1
            out.append(_table(lines[i:j])); i = j; continue
        if re.match(r"^\s*[-*] ", ln) or re.match(r"^\s*\d+\. ", ln):  # list
            ordered = bool(re.match(r"^\s*\d+\. ", ln))
            tag = "ol" if ordered else "ul"
            items, j = [], i
            while j < len(lines) and (re.match(r"^\s*[-*] ", lines[j]) or re.match(r"^\s*\d+\. ", lines[j])
                                      or (lines[j].startswith("  ") and lines[j].strip() and items)):
                if re.match(r"^\s*[-*] ", lines[j]) or re.match(r"^\s*\d+\. ", lines[j]):
                    items.append(re.sub(r"^\s*(?:[-*]|\d+\.) ", "", lines[j]))
                else:
                    items[-1] += " " + lines[j].strip()
                j += 1
            out.append("<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % _inline(x) for x in items), tag))
            i = j
            continue
        if ln.lstrip().startswith(">"):                              # blockquote
            buf, j = [], i
            while j < len(lines) and lines[j].lstrip().startswith(">"):
                buf.append(re.sub(r"^\s*>\s?", "", lines[j])); j += 1
            out.append("<blockquote>%s</blockquote>" % _inline(" ".join(buf))); i = j; continue
        buf, j = [], i                                               # paragraph
        while j < len(lines) and lines[j].strip() and not re.match(r"^(#{1,6} |```|\s*[-*] |\s*\d+\. |\s*>)", lines[j]) \
                and not lines[j].lstrip().startswith("|"):
            buf.append(lines[j]); j += 1
        out.append("<p>%s</p>" % _inline(" ".join(buf))); i = j
    return "\n".join(out)


def page(title, body, up="..", css="../assets/site.css"):
    return ("""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<link rel="stylesheet" href="%s">
<style>
  main.doc { max-width: 90ch; margin: 0 auto; padding: 26px 22px 60px; }
  main.doc table { border-collapse: collapse; margin: 14px 0; font-size: .92rem; }
  main.doc th, main.doc td { text-align: left; padding: 5px 11px; border-bottom: 1px solid var(--line); vertical-align: top; }
  main.doc h1 { font-size: 1.5rem; } main.doc h2 { font-size: 1.18rem; margin-top: 1.7em; }
  main.doc pre { background: var(--soft); padding: 11px 13px; border-radius: 6px; overflow-x: auto; }
  main.doc blockquote { border-left: 3px solid var(--line); margin: 12px 0; padding: 2px 14px; color: var(--mute); }
  main.doc .crumb { font-size: .88rem; color: var(--mute); margin-bottom: 18px; }
</style>
</head>
<body>
<main class="doc">
<p class="crumb"><a href="%s/index.html">&larr; interactive companion</a> &middot;
   <a href="index.html">reference index</a></p>
%s
</main>
</body>
</html>
""" % (html.escape(title), css, up, body))
