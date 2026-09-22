"""A very small SVG plotter: standard library only, no matplotlib.

Written for this repository because the figures it needs are simple (line, log-log,
scatter, bar, a little annotation) and because a reader should be able to regenerate
every figure with nothing installed but Python and numpy.

Every colour is a literal value.  CSS custom properties are deliberately avoided: the
renderer GitHub uses for SVG in Markdown (librsvg) does not resolve them and paints the
result as a black rectangle.  Light and dark variants are separate files, selected in the
README by a <picture> element on prefers-color-scheme, each with an explicit background.
"""
import math

THEMES = {
    "light": dict(bg="#ffffff", ink="#1f2328", mute="#57606a", grid="#d8dee4", axis="#8c959f",
                  series=["#0969da", "#cf222e", "#1a7f37", "#9a6700", "#8250df", "#57606a"]),
    "dark":  dict(bg="#0d1117", ink="#e6edf3", mute="#9198a1", grid="#30363d", axis="#6e7681",
                  series=["#4493f8", "#ff7b72", "#3fb950", "#d29922", "#ab7df8", "#8b949e"]),
}


def _esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _nice_ticks(lo, hi, want=6):
    if hi <= lo:
        return [lo]
    raw = (hi - lo) / max(want, 2)
    mag = 10.0 ** math.floor(math.log10(raw))
    for m in (1, 2, 2.5, 5, 10):
        if raw <= m * mag:
            step = m * mag
            break
    else:
        step = 10 * mag
    first = math.ceil(lo / step) * step
    out, v = [], first
    while v <= hi + 1e-9 * step:
        out.append(round(v, 12))
        v += step
    return out


def _fmt(v):
    if v == 0:
        return "0"
    a = abs(v)
    if a >= 1e4 or a < 1e-3:
        e = int(math.floor(math.log10(a)))
        m = v / 10.0 ** e
        return ("%g·10^%d" % (round(m, 2), e)) if abs(m - round(m)) > 1e-9 else ("10^%d" % e)
    s = ("%.6f" % v).rstrip("0").rstrip(".")
    return s if s not in ("-0", "") else "0"


class Fig:
    def __init__(self, width=820, height=460, theme="light", title=None,
                 xlabel=None, ylabel=None, margin=None):
        self.w, self.h, self.t = width, height, THEMES[theme]
        self.theme_name = theme
        self.title, self.xlabel, self.ylabel = title, xlabel, ylabel
        ml, mr, mt, mb = margin or (74, 22, 40 if title else 18, 56)
        self.ml, self.mr, self.mt, self.mb = ml, mr, mt, mb
        self._x = self._y = None
        self._xlog = self._ylog = None
        self._items, self._legend = [], []
        self._xticks = self._yticks = None
        self._xticklabels = None
        self._legend_loc = "tl"

    # ---- scales -------------------------------------------------------------
    def xlim(self, a, b): self._x = (float(a), float(b)); return self
    def ylim(self, a, b): self._y = (float(a), float(b)); return self
    def xlog(self, base=10): self._xlog = base; return self
    def ylog(self, base=10): self._ylog = base; return self
    def xticks(self, vals, labels=None): self._xticks = list(vals); self._xticklabels = labels; return self
    def yticks(self, vals): self._yticks = list(vals); return self
    def legend_at(self, loc): self._legend_loc = loc; return self  # tl, tr, bl, br

    def _autolim(self):
        xs, ys = [], []
        for kind, data in self._items:
            if kind in ("line", "points"):
                xs += list(data["x"]); ys += list(data["y"])
            elif kind == "bars":
                xs += list(data["x"]); ys += list(data["y"]) + [0.0]
        xs = [v for v in xs if v == v and abs(v) != float("inf")]
        ys = [v for v in ys if v == v and abs(v) != float("inf")]
        if self._xlog: xs = [v for v in xs if v > 0]
        if self._ylog: ys = [v for v in ys if v > 0]
        if self._x is None and xs:
            a, b = min(xs), max(xs)
            if self._xlog:
                self._x = (a / 1.25, b * 1.25)
            else:
                p = 0.04 * (b - a or abs(a) or 1.0); self._x = (a - p, b + p)
        if self._y is None and ys:
            a, b = min(ys), max(ys)
            if self._ylog:
                self._y = (a / 1.6, b * 1.6)
            else:
                p = 0.08 * (b - a or abs(a) or 1.0); self._y = (a - p, b + p)
        if self._x is None: self._x = (0.0, 1.0)
        if self._y is None: self._y = (0.0, 1.0)

    def _px(self, v):
        a, b = self._x
        if self._xlog:
            if v <= 0: return None
            f = (math.log(v) - math.log(a)) / (math.log(b) - math.log(a))
        else:
            f = (v - a) / (b - a)
        return self.ml + f * (self.w - self.ml - self.mr)

    def _py(self, v):
        a, b = self._y
        if self._ylog:
            if v <= 0: return None
            f = (math.log(v) - math.log(a)) / (math.log(b) - math.log(a))
        else:
            f = (v - a) / (b - a)
        return self.h - self.mb - f * (self.h - self.mt - self.mb)

    def _col(self, c):
        return c if isinstance(c, str) else self.t["series"][c % len(self.t["series"])]

    # ---- content ------------------------------------------------------------
    def line(self, x, y, color=0, width=2.0, dash=None, label=None, opacity=1.0):
        self._items.append(("line", dict(x=list(x), y=list(y), c=color, w=width,
                                         d=dash, label=label, o=opacity)))
        if label: self._legend.append((label, self._col(color), "line", dash))
        return self

    def points(self, x, y, color=0, size=3.6, label=None, marker="o"):
        self._items.append(("points", dict(x=list(x), y=list(y), c=color, s=size,
                                           label=label, m=marker)))
        if label: self._legend.append((label, self._col(color), "point", None))
        return self

    def bars(self, x, y, color=0, width=0.6, label=None, opacity=0.85):
        self._items.append(("bars", dict(x=list(x), y=list(y), c=color, bw=width,
                                         label=label, o=opacity)))
        if label: self._legend.append((label, self._col(color), "bar", None))
        return self

    def hline(self, y, color="mute", dash="4 3", label=None, width=1.2):
        self._items.append(("hline", dict(y=y, c=color, d=dash, label=label, w=width)))
        if label: self._legend.append((label, self._col(color) if color != "mute" else self.t["mute"], "line", dash))
        return self

    def vline(self, x, color="mute", dash="4 3", label=None, width=1.2):
        self._items.append(("vline", dict(x=x, c=color, d=dash, label=label, w=width)))
        return self

    def band(self, x0, x1, color=0, opacity=0.10):
        self._items.append(("band", dict(x0=x0, x1=x1, c=color, o=opacity)))
        return self

    def annotate(self, x, y, text, dx=0, dy=-8, color=None, anchor="middle", size=12.5, italic=False):
        self._items.append(("text", dict(x=x, y=y, s=text, dx=dx, dy=dy, c=color,
                                         a=anchor, fs=size, it=italic)))
        return self

    # ---- output -------------------------------------------------------------
    def svg(self):
        self._autolim()
        T, o = self.t, []
        o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
                 'viewBox="0 0 %d %d" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif">'
                 % (self.w, self.h, self.w, self.h))
        o.append('<rect width="%d" height="%d" fill="%s"/>' % (self.w, self.h, T["bg"]))
        L, R = self.ml, self.w - self.mr
        Tp, B = self.mt, self.h - self.mb
        cid = "plot-clip"
        o.append('<defs><clipPath id="%s"><rect x="%.2f" y="%.2f" width="%.2f" height="%.2f"/>'
                 '</clipPath></defs>' % (cid, L, Tp, R - L, B - Tp))
        # bands first
        for kind, d in self._items:
            if kind == "band":
                x0, x1 = self._px(d["x0"]), self._px(d["x1"])
                if x0 is not None and x1 is not None:
                    o.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s" opacity="%.3f"/>'
                             % (min(x0, x1), Tp, abs(x1 - x0), B - Tp, self._col(d["c"]), d["o"]))
        # grid + ticks
        xt = self._xticks if self._xticks is not None else self._auto_ticks("x")
        yt = self._yticks if self._yticks is not None else self._auto_ticks("y")
        for i, v in enumerate(xt):
            px = self._px(v)
            if px is None or px < L - .5 or px > R + .5: continue
            o.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="1"/>'
                     % (px, Tp, px, B, T["grid"]))
            lab = self._xticklabels[i] if self._xticklabels else self._ticklabel(v, "x")
            o.append('<text x="%.2f" y="%.2f" fill="%s" font-size="12.5" text-anchor="middle">%s</text>'
                     % (px, B + 19, T["mute"], _esc(lab)))
        for v in yt:
            py = self._py(v)
            if py is None or py < Tp - .5 or py > B + .5: continue
            o.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="1"/>'
                     % (L, py, R, py, T["grid"]))
            o.append('<text x="%.2f" y="%.2f" fill="%s" font-size="12.5" text-anchor="end">%s</text>'
                     % (L - 9, py + 4.4, T["mute"], _esc(self._ticklabel(v, "y"))))
        o.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="none" stroke="%s" stroke-width="1.2"/>'
                 % (L, Tp, R - L, B - Tp, T["axis"]))
        # content, clipped to the axes box so nothing spills into the margins
        o.append('<g clip-path="url(#%s)">' % cid)
        for kind, d in self._items:
            if kind == "line":
                pts, run = [], []
                for X, Y in zip(d["x"], d["y"]):
                    px, py = self._px(X), self._py(Y)
                    if px is None or py is None or py != py:
                        if len(run) > 1: pts.append(run)
                        run = []
                    else:
                        run.append("%.1f,%.1f" % (px, py))
                if len(run) > 1: pts.append(run)
                for seg in pts:
                    o.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%.2f"%s%s '
                             'stroke-linejoin="round" stroke-linecap="round"/>'
                             % (" ".join(seg), self._col(d["c"]), d["w"],
                                ' stroke-dasharray="%s"' % d["d"] if d["d"] else "",
                                ' opacity="%.3f"' % d["o"] if d["o"] < 1 else ""))
            elif kind == "points":
                for X, Y in zip(d["x"], d["y"]):
                    px, py = self._px(X), self._py(Y)
                    if px is None or py is None: continue
                    if d["m"] == "s":
                        o.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s"/>'
                                 % (px - d["s"], py - d["s"], 2 * d["s"], 2 * d["s"], self._col(d["c"])))
                    else:
                        o.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s"/>'
                                 % (px, py, d["s"], self._col(d["c"])))
            elif kind == "bars":
                n = len(d["x"])
                if n > 1:
                    step = abs(self._px(d["x"][1]) - self._px(d["x"][0]))
                else:
                    step = (R - L) / 8.0
                bw = max(2.0, step * d["bw"])
                zero = self._py(max(self._y[0], 0.0)) if self._y[0] <= 0 <= self._y[1] else self._py(self._y[0])
                for X, Y in zip(d["x"], d["y"]):
                    px, py = self._px(X), self._py(Y)
                    if px is None or py is None: continue
                    o.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s" opacity="%.3f"/>'
                             % (px - bw / 2, min(py, zero), bw, abs(zero - py), self._col(d["c"]), d["o"]))
            elif kind == "hline":
                py = self._py(d["y"])
                if py is not None:
                    c = T["mute"] if d["c"] == "mute" else self._col(d["c"])
                    o.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="%.2f"%s/>'
                             % (L, py, R, py, c, d["w"], ' stroke-dasharray="%s"' % d["d"] if d["d"] else ""))
            elif kind == "vline":
                px = self._px(d["x"])
                if px is not None:
                    c = T["mute"] if d["c"] == "mute" else self._col(d["c"])
                    o.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="%.2f"%s/>'
                             % (px, Tp, px, B, c, d["w"], ' stroke-dasharray="%s"' % d["d"] if d["d"] else ""))
            elif kind == "text":
                px, py = self._px(d["x"]), self._py(d["y"])
                if px is None or py is None: continue
                c = self._col(d["c"]) if d["c"] is not None else T["ink"]
                o.append('<text x="%.2f" y="%.2f" fill="%s" font-size="%.1f" text-anchor="%s"%s>%s</text>'
                         % (px + d["dx"], py + d["dy"], c, d["fs"], d["a"],
                            ' font-style="italic"' if d["it"] else "", _esc(d["s"])))
        o.append('</g>')
        # labels
        if self.title:
            o.append('<text x="%.2f" y="%.2f" fill="%s" font-size="15" font-weight="600" text-anchor="middle">%s</text>'
                     % ((L + R) / 2, Tp - 14, T["ink"], _esc(self.title)))
        if self.xlabel:
            o.append('<text x="%.2f" y="%.2f" fill="%s" font-size="13.5" text-anchor="middle">%s</text>'
                     % ((L + R) / 2, self.h - 12, T["ink"], _esc(self.xlabel)))
        if self.ylabel:
            o.append('<text transform="translate(%.2f,%.2f) rotate(-90)" fill="%s" font-size="13.5" '
                     'text-anchor="middle">%s</text>' % (16, (Tp + B) / 2, T["ink"], _esc(self.ylabel)))
        # legend
        if self._legend:
            wpx = max(len(t) for t, _, _, _ in self._legend) * 7.1 + 34
            hpx = 19 * len(self._legend) + 10
            loc = self._legend_loc
            bx = L + 12 if loc in ("tl", "bl") else R - 12 - wpx
            by = Tp + 12 if loc in ("tl", "tr") else B - 12 - hpx
            o.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s" opacity="0.88" '
                     'stroke="%s" stroke-width="1" rx="4"/>'
                     % (bx, by, wpx, hpx, T["bg"], T["grid"]))
            for i, (lab, col, kind, dash) in enumerate(self._legend):
                yy = by + 17 + 19 * i
                if kind == "point":
                    o.append('<circle cx="%.2f" cy="%.2f" r="3.6" fill="%s"/>' % (bx + 14, yy - 4, col))
                else:
                    o.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="2.4"%s/>'
                             % (bx + 7, yy - 4, bx + 24, yy - 4, col,
                                ' stroke-dasharray="%s"' % dash if dash else ""))
                o.append('<text x="%.2f" y="%.2f" fill="%s" font-size="12.5">%s</text>'
                         % (bx + 30, yy, T["ink"], _esc(lab)))
        o.append("</svg>")
        return "\n".join(o)

    def _auto_ticks(self, ax):
        lo, hi = self._x if ax == "x" else self._y
        log = self._xlog if ax == "x" else self._ylog
        if not log:
            return _nice_ticks(lo, hi)
        b = log
        out, e = [], math.floor(math.log(lo, b))
        while b ** e <= hi * 1.0000001:
            if b ** e >= lo * 0.9999999:
                out.append(b ** e)
            e += 1
        return out or [lo, hi]

    def _ticklabel(self, v, ax):
        log = self._xlog if ax == "x" else self._ylog
        if log == 2:
            e = round(math.log(v, 2))
            return "2^%d" % e if abs(2 ** e - v) < 1e-9 * max(1, abs(v)) else _fmt(v)
        if log == 10:
            e = round(math.log10(v))
            return "10^%d" % e if abs(10 ** e - v) < 1e-9 * max(1, abs(v)) else _fmt(v)
        return _fmt(v)

    def save(self, path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.svg() + "\n")
        return path


def figure_pair(build, stem, outdir):
    """Render the same figure in both themes: <stem>.light.svg and <stem>.dark.svg."""
    paths = []
    for theme in ("light", "dark"):
        fig = build(theme)
        paths.append(fig.save("%s/%s.%s.svg" % (outdir, stem, theme)))
    return paths
