/* A small canvas plotter for the widgets: linear or log axes, lines, points, rules, notes.
 * Deliberately tiny and dependency-free; the page loads no third-party script at all. */

const THEMES = {
  light: { ink: '#1f2328', mute: '#57606a', grid: '#d8dee4', axis: '#8c959f', bg: '#ffffff',
           series: ['#0969da', '#cf222e', '#1a7f37', '#9a6700', '#8250df', '#57606a'] },
  dark:  { ink: '#e6edf3', mute: '#9198a1', grid: '#30363d', axis: '#6e7681', bg: '#0d1117',
           series: ['#4493f8', '#ff7b72', '#3fb950', '#d29922', '#ab7df8', '#8b949e'] },
};
export const theme = () =>
  THEMES[matchMedia && matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'];

const niceTicks = (lo, hi, want = 6) => {
  if (!(hi > lo)) return [lo];
  const raw = (hi - lo) / want, mag = Math.pow(10, Math.floor(Math.log10(raw)));
  let step = 10 * mag;
  for (const m of [1, 2, 2.5, 5, 10]) if (raw <= m * mag) { step = m * mag; break; }
  const out = []; let v = Math.ceil(lo / step) * step;
  while (v <= hi + 1e-9 * step) { out.push(Math.round(v * 1e12) / 1e12); v += step; }
  return out;
};
const fmt = (v) => {
  if (v === 0) return '0';
  const a = Math.abs(v);
  if (a >= 1e4 || a < 1e-3) {
    const e = Math.floor(Math.log10(a)), m = v / Math.pow(10, e);
    return Math.abs(m - Math.round(m)) < 1e-9 ? `10^${e}` : `${(Math.round(m * 100) / 100)}e${e}`;
  }
  return String(Math.round(v * 1e6) / 1e6);
};

export function plot(canvas, spec) {
  const T = theme(), dpr = window.devicePixelRatio || 1;
  const W = canvas.clientWidth, H = canvas.clientHeight;
  canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
  const g = canvas.getContext('2d');
  g.setTransform(dpr, 0, 0, dpr, 0, 0);
  g.clearRect(0, 0, W, H);
  g.font = '12px -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif';

  const ml = spec.ml ?? 62, mr = 14, mt = 12, mb = spec.xlabel ? 44 : 28;
  const L = ml, R = W - mr, Tp = mt, B = H - mb;
  const S = spec.series.filter((s) => s.x.length);
  const finite = (v) => Number.isFinite(v);
  let xs = [], ys = [];
  for (const s of S) { xs = xs.concat(s.x); ys = ys.concat(s.y); }
  xs = xs.filter(finite); ys = ys.filter(finite);
  if (spec.ylog) ys = ys.filter((v) => v > 0);
  if (spec.xlog) xs = xs.filter((v) => v > 0);
  let [x0, x1] = spec.xlim ?? [Math.min(...xs), Math.max(...xs)];
  let [y0, y1] = spec.ylim ?? [Math.min(...ys), Math.max(...ys)];
  if (!spec.xlim) { const p = spec.xlog ? 0 : 0.03 * (x1 - x0 || 1); x0 -= p; x1 += p; }
  if (!spec.ylim) {
    if (spec.ylog) { y0 /= 2; y1 *= 2; } else { const p = 0.08 * (y1 - y0 || Math.abs(y0) || 1); y0 -= p; y1 += p; }
  }
  const px = (v) => spec.xlog
    ? L + (Math.log(v) - Math.log(x0)) / (Math.log(x1) - Math.log(x0)) * (R - L)
    : L + (v - x0) / (x1 - x0) * (R - L);
  const py = (v) => spec.ylog
    ? B - (Math.log(v) - Math.log(y0)) / (Math.log(y1) - Math.log(y0)) * (B - Tp)
    : B - (v - y0) / (y1 - y0) * (B - Tp);

  const logTicks = (lo, hi, base) => {
    const out = []; let e = Math.floor(Math.log(lo) / Math.log(base));
    while (Math.pow(base, e) <= hi * 1.0000001) { if (Math.pow(base, e) >= lo * 0.9999999) out.push(Math.pow(base, e)); e++; }
    return out.length ? out : [lo, hi];
  };
  const xt = spec.xticks ?? (spec.xlog ? logTicks(x0, x1, spec.xlog).map((v) => ({ v, label: `${spec.xlog}^${Math.round(Math.log(v) / Math.log(spec.xlog))}` }))
                                       : niceTicks(x0, x1).map((v) => ({ v, label: fmt(v) })));
  const yt = spec.ylog ? logTicks(y0, y1, spec.ylog).map((v) => ({ v, label: `${spec.ylog}^${Math.round(Math.log(v) / Math.log(spec.ylog))}` }))
                       : niceTicks(y0, y1).map((v) => ({ v, label: fmt(v) }));

  g.strokeStyle = T.grid; g.lineWidth = 1; g.fillStyle = T.mute; g.textBaseline = 'middle';
  for (const t of xt) { const X = px(t.v); if (X < L - 1 || X > R + 1) continue;
    g.beginPath(); g.moveTo(X, Tp); g.lineTo(X, B); g.stroke();
    g.textAlign = 'center'; g.fillText(t.label, X, B + 14); }
  for (const t of yt) { const Y = py(t.v); if (Y < Tp - 1 || Y > B + 1) continue;
    g.beginPath(); g.moveTo(L, Y); g.lineTo(R, Y); g.stroke();
    g.textAlign = 'right'; g.fillText(t.label, L - 7, Y); }
  g.strokeStyle = T.axis; g.lineWidth = 1.2; g.strokeRect(L, Tp, R - L, B - Tp);

  g.save(); g.beginPath(); g.rect(L, Tp, R - L, B - Tp); g.clip();
  for (const r of spec.hlines ?? []) {
    g.strokeStyle = r.color ?? T.mute; g.lineWidth = r.width ?? 1.2;
    g.setLineDash(r.dash ?? [4, 3]); const Y = py(r.y);
    g.beginPath(); g.moveTo(L, Y); g.lineTo(R, Y); g.stroke(); g.setLineDash([]);
  }
  for (const r of spec.vlines ?? []) {
    g.strokeStyle = r.color ?? T.mute; g.lineWidth = r.width ?? 1.2;
    g.setLineDash(r.dash ?? [4, 3]); const X = px(r.x);
    g.beginPath(); g.moveTo(X, Tp); g.lineTo(X, B); g.stroke(); g.setLineDash([]);
  }
  S.forEach((s, i) => {
    const col = s.color ?? T.series[i % T.series.length];
    if (s.points) {
      g.fillStyle = col;
      for (let j = 0; j < s.x.length; j++) {
        const X = px(s.x[j]), Y = py(s.y[j]);
        if (!finite(X) || !finite(Y)) continue;
        g.beginPath(); g.arc(X, Y, s.size ?? 3.4, 0, 2 * Math.PI); g.fill();
      }
    } else {
      g.strokeStyle = col; g.lineWidth = s.width ?? 2; g.setLineDash(s.dash ?? []);
      g.beginPath(); let pen = false;
      for (let j = 0; j < s.x.length; j++) {
        const X = px(s.x[j]), Y = py(s.y[j]);
        if (!finite(X) || !finite(Y)) { pen = false; continue; }
        if (!pen) { g.moveTo(X, Y); pen = true; } else g.lineTo(X, Y);
      }
      g.stroke(); g.setLineDash([]);
    }
  });
  for (const n of spec.notes ?? []) {
    g.fillStyle = n.color ?? T.ink; g.textAlign = n.anchor ?? 'center';
    g.font = `${n.italic ? 'italic ' : ''}12px -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif`;
    g.fillText(n.text, px(n.x) + (n.dx ?? 0), py(n.y) + (n.dy ?? 0));
  }
  g.restore();
  g.font = '12px -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif';
  g.fillStyle = T.ink; g.textAlign = 'center';
  if (spec.xlabel) g.fillText(spec.xlabel, (L + R) / 2, H - 10);
  if (spec.ylabel) { g.save(); g.translate(13, (Tp + B) / 2); g.rotate(-Math.PI / 2); g.fillText(spec.ylabel, 0, 0); g.restore(); }

  const leg = S.filter((s) => s.label);
  if (leg.length) {
    const wpx = Math.max(...leg.map((s) => s.label.length)) * 6.4 + 30, hpx = 17 * leg.length + 8;
    const bx = spec.legend === 'br' || spec.legend === 'tr' ? R - 10 - wpx : L + 10;
    const by = spec.legend === 'bl' || spec.legend === 'br' ? B - 10 - hpx : Tp + 10;
    g.fillStyle = T.bg; g.globalAlpha = 0.86; g.fillRect(bx, by, wpx, hpx); g.globalAlpha = 1;
    g.strokeStyle = T.grid; g.lineWidth = 1; g.strokeRect(bx, by, wpx, hpx);
    leg.forEach((s, i) => {
      const Y = by + 13 + 17 * i, col = s.color ?? T.series[S.indexOf(s) % T.series.length];
      g.strokeStyle = col; g.lineWidth = 2.4; g.setLineDash(s.dash ?? []);
      g.beginPath(); g.moveTo(bx + 6, Y - 4); g.lineTo(bx + 22, Y - 4); g.stroke(); g.setLineDash([]);
      g.fillStyle = T.ink; g.textAlign = 'left'; g.fillText(s.label, bx + 27, Y - 4);
    });
  }
}
