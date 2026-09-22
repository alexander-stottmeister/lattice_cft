import { WIDGETS } from './widgets.js';
import { plot } from './plot.js';
import * as K from './kernels.js';

const $ = (s, r = document) => r.querySelector(s);
const el = (t, cls, html) => { const e = document.createElement(t); if (cls) e.className = cls; if (html !== undefined) e.innerHTML = html; return e; };

async function load(p) { const r = await fetch(p); if (!r.ok) throw new Error(`${p}: ${r.status}`); return r.json(); }

export function buildWidget(w, ctx) {
  const sec = el('section', 'widget'); sec.id = w.id;
  sec.appendChild(el('h2', null, w.title));
  sec.appendChild(el('p', 'result', w.result));
  sec.appendChild(el('p', 'blurb', w.blurb));
  const controls = el('div', 'controls'), state = {};
  for (const c of w.controls) {
    state[c.k] = c.value;
    const wrap = el('label', 'control');
    wrap.appendChild(el('span', 'clabel', c.label));
    let input;
    if (c.type === 'check') {
      input = el('input'); input.type = 'checkbox'; input.checked = !!c.value;
      input.addEventListener('input', () => { state[c.k] = input.checked ? 1 : 0; render(); });
    } else {
      input = el('input'); input.type = 'range';
      input.min = c.min; input.max = c.max; input.step = c.step; input.value = c.value;
      input.addEventListener('input', () => { state[c.k] = parseFloat(input.value); render(); });
    }
    wrap.appendChild(input);
    const out = el('span', 'cvalue', c.type === 'check' ? '' : String(c.value));
    if (c.type !== 'check') input.addEventListener('input', () => { out.textContent = input.value; });
    wrap.appendChild(out);
    controls.appendChild(wrap);
  }
  sec.appendChild(controls);
  const canvas = el('canvas', 'plot'); sec.appendChild(canvas);
  const readout = el('p', 'readout'); sec.appendChild(readout);
  function render() {
    try { readout.innerHTML = w.draw(canvas, state, ctx) ?? ''; }
    catch (e) { readout.innerHTML = `<span class="err">this widget failed: ${e.message}</span>`; }
  }
  sec._render = render;
  return sec;
}

/* The panel that makes "computed live" checkable rather than decorative. */
export function buildCheck(ctx) {
  const sec = el('section', 'widget'); sec.id = 'check';
  sec.appendChild(el('h2', null, 'Check the numbers yourself'));
  sec.appendChild(el('p', 'result', 'tools/check_js.mjs runs the same comparisons outside the browser'));
  sec.appendChild(el('p', 'blurb', `Every curve above is computed here, in your browser, from the
    filter taps in <code>data/filters.json</code>. These rows compare that computation against the
    values <code>tools/make_data.py</code> produced with numpy. If a row disagrees, the page is
    lying to you and the badge says so.`));
  const rows = [];
  const R = ctx.recorded, F = ctx.filters;
  let worst = 0;
  const add = (name, got, want, tol) => {
    const rel = want === 0 ? Math.abs(got) : Math.abs(got / want - 1);
    worst = Math.max(worst, rel);
    rows.push({ name, got, want, rel, ok: rel <= tol });
  };
  for (const k of ['2', '6', '12']) add(`centre of mass, K = ${k}`, K.centreOfMass(F.taps[k]), F.mu[k], 1e-12);
  for (const d of ['0.5', '2']) {
    const e = R.momentum_cutoff_opnorm.by_delta[d];
    add(`operator norm, δ = ${d}, N = 8`, K.opnorm(8, 2, parseFloat(d)), e.value[e.N.indexOf(8)], 1e-12);
  }
  const hs = R.momentum_cutoff_hs.by_k['4'];
  add('off-diagonal HS norm, k = 4, N = 6', K.hsnorm(6, 4), hs.value[hs.N.indexOf(6)], 1e-12);
  const V = R.vacuum_deviation;
  add('vacuum deviation, full', K.vacuumDeviation(V.N[3], V.k).full, V.full[3], 1e-9);
  add('vacuum deviation, chiral', K.vacuumDeviation(V.N[3], V.k).chiral, V.chiral[3], 1e-9);
  add('entropy density 2ln2 − 1', K.ENTROPY_DENSITY, R.multiplicity.entropy_density, 1e-12);
  const fit = K.fitRate([4, 5, 6, 7, 8], [4, 5, 6, 7, 8].map((N) => K.opnorm(N, 2, 2)));
  add('fitted rate at δ = 2 (predicted 2)', fit, 2, 3e-2);

  const allOk = rows.every((r) => r.ok);
  const badge = el('p', 'badge ' + (allOk ? 'ok' : 'bad'),
    allOk ? `all ${rows.length} checks agree, worst relative difference ${worst.toExponential(1)}`
          : `${rows.filter((r) => !r.ok).length} of ${rows.length} checks disagree`);
  sec.appendChild(badge);
  const tbl = el('table', 'check');
  tbl.innerHTML = '<thead><tr><th>quantity</th><th>in your browser</th><th>from numpy</th><th>relative</th></tr></thead>';
  const tb = el('tbody');
  for (const r of rows) {
    const tr = el('tr', r.ok ? '' : 'bad');
    tr.innerHTML = `<td>${r.name}</td><td>${r.got.toPrecision(10)}</td><td>${Number(r.want).toPrecision(10)}</td><td>${r.rel.toExponential(1)}</td>`;
    tb.appendChild(tr);
  }
  tbl.appendChild(tb); sec.appendChild(tbl);
  return sec;
}

export async function start() {
  const ctx = {
    filters: await load('data/filters.json'),
    recorded: await load('data/recorded.json'),
    results: await load('data/results.json').catch(() => null),
  };
  const host = $('#content'), nav = $('#nav-list');
  const sections = [];
  for (const w of WIDGETS) {
    const sec = buildWidget(w, ctx);
    host.appendChild(sec); sections.push(sec);
    const a = el('a', null, w.title); a.href = `#${w.id}`;
    nav.appendChild(el('li')).appendChild(a);
  }
  const chk = buildCheck(ctx); host.appendChild(chk);
  const a = el('a', null, 'Check the numbers yourself'); a.href = '#check';
  nav.appendChild(el('li')).appendChild(a);

  const renderAll = () => sections.forEach((s) => s._render());
  renderAll();
  let t; addEventListener('resize', () => { clearTimeout(t); t = setTimeout(renderAll, 150); });
  matchMedia('(prefers-color-scheme: dark)').addEventListener('change', renderAll);
  $('#status').textContent = `${WIDGETS.length} widgets, computed in your browser`;
}
