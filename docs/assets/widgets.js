/* The widgets. One per consequential result; each recomputes in the browser from the same
 * filters the paper uses, except where a readout says "recorded", which means the number
 * comes from docs/data/recorded.json and names the script that produced it. */
import * as K from './kernels.js';
import { plot, theme } from './plot.js';

const lin = (a, b, n) => Array.from({ length: n }, (_, i) => a + (b - a) * i / (n - 1));
const f2 = (v) => (Math.abs(v) >= 1e4 || (v !== 0 && Math.abs(v) < 1e-3)) ? v.toExponential(2) : v.toFixed(3);

export const WIDGETS = [
{
  id: 'shat', title: 'The zeros of the transform, and the step that is false',
  result: 'Findings 1 and 2; Lemma 4.7, Remark 4.33',
  blurb: `Orthonormality forces the transform of the scaling function to vanish at every
    non-zero multiple of 2&pi;, to order K. The published proof bounded a <em>quotient</em> of two
    of its values by continuity. Put the denominator on a zero and the bound cannot exist.`,
  controls: [{ k: 'K', label: 'Daubechies order K', min: 2, max: 12, step: 1, value: 4 },
             { k: 'n', label: 'resonance at 2&pi;n', min: 1, max: 4, step: 1, value: 1 }],
  draw(c, p, ctx) {
    const h = ctx.filters.taps[p.K], xs = lin(1e-3, 8 * K.PI, 2400);
    plot(c, { series: [{ x: xs, y: xs.map((x) => K.shatAbs(x, h)), label: `db${p.K}` }],
      ylog: 10, ylim: [1e-14, 3], xlim: [0, 8 * K.PI], xlabel: 'ξ', ylabel: '|ŝ(ξ)|',
      xticks: [0, 1, 2, 3, 4].map((i) => ({ v: 2 * K.PI * i, label: i ? `${2 * i}π` : '0' })),
      vlines: [{ x: 2 * K.PI * p.n }] });
    const eps = 1e-3, at = 2 * K.PI * p.n;
    const num = K.shatAbs(at - eps, h), den = K.shatAbs(at, h);
    return `at &xi; = 2&pi;&middot;${p.n} the transform is <b>${den.toExponential(2)}</b>, while a
      neighbouring value is <b>${num.toExponential(2)}</b>; their quotient is
      <b>${(num / den).toExponential(2)}</b>. Raising K deepens the zero, so no constant bounds it.`;
  },
},
{
  id: 'ladder', title: 'How regular the scaling function must be',
  result: 'Definition 3.12, Remark 3.13',
  blurb: `"Sufficiently regular" hides four thresholds. Move the slider to the Sobolev index you
    want and read off the smallest Daubechies order that supplies it. The advertised rate is at
    &delta; = 2, which needs K &ge; 9, not the K &ge; 2 of folklore.`,
  controls: [{ k: 'rho', label: 'required exponent', min: 0.5, max: 3.5, step: 0.25, value: 3 }],
  draw(c, p, ctx) {
    const S = ctx.recorded.sobolev_sigma.value, R = ctx.recorded.pointwise_rho.value;
    const Ks = Object.keys(S).map(Number).sort((a, b) => a - b);
    const Rk = Object.keys(R).map(Number).sort((a, b) => a - b);
    const need = Ks.find((k) => S[k] > p.rho);
    plot(c, { series: [
        { x: Ks, y: Ks.map((k) => S[k]), label: 'σ_K (Sobolev)' },
        { x: Rk, y: Rk.map((k) => R[k]), label: 'ρ (pointwise, recorded)', dash: [5, 3] },
        { x: need ? [need] : [], y: need ? [S[need]] : [], points: true, size: 5.5, color: theme().series[2] }],
      hlines: [{ y: p.rho, dash: [2, 4] }], xlabel: 'Daubechies order K', ylabel: 'exponent',
      xlim: [1.6, 12.4], ylim: [0.6, 4.1], legend: 'tl' });
    return need
      ? `&sigma;<sub>K</sub> &gt; ${p.rho} first holds at <b>K = ${need}</b> (&sigma; = ${f2(S[need])}),
         a filter of ${2 * need} taps and support of width ${2 * need - 1}.`
      : `no order up to 12 reaches &sigma; &gt; ${p.rho}.`;
  },
},
{
  id: 'rates', title: 'The sharp rate on the momentum-cutoff route',
  result: 'Lemma 4.15, Theorem 4.16, Remark 4.8',
  blurb: `The difference of the approximant and the generator is an explicit multiplier, so its
    operator norm is a supremum you can evaluate. The rate is min{&delta;,2}: the cap at 2 is real,
    and it is why the wavelet route needs re-centring to keep up.`,
  controls: [{ k: 'delta', label: 'Sobolev index δ', min: 0, max: 3, step: 0.25, value: 2 },
             { k: 'kk', label: 'mode k', min: 1, max: 6, step: 1, value: 2 }],
  draw(c, p, ctx) {
    const Ns = [4, 5, 6, 7, 8], v = Ns.map((N) => K.opnorm(N, p.kk, p.delta));
    const fit = K.fitRate(Ns, v), pred = Math.min(p.delta, 2);
    plot(c, { series: [{ x: Ns, y: v, label: `δ = ${p.delta}` }, { x: Ns, y: v, points: true }],
      ylog: 2, xlabel: 'scale N', ylabel: '‖ difference ‖ on h^{1+δ} → h⁰',
      xticks: Ns.map((n) => ({ v: n, label: String(n) })), legend: 'bl' });
    return `fitted rate <b>${fit.toFixed(3)}</b> against the predicted <b>${pred.toFixed(2)}</b>.
      The off-diagonal Hilbert&ndash;Schmidt error is <b>${f2(K.hsnorm(8, p.kk))}</b> at N = 8, of order 2 throughout.`;
  },
},
{
  id: 'majorant', title: 'Why the two decays have to be taken together',
  result: 'Lemma 3.14, Corollary 3.15',
  blurb: `Neither factor decays on its own beyond the Brillouin zone: the finite product only
    repeats periodically, and the transform is evaluated near its zeros. Their <em>product</em> does
    decay, because wherever one is of order one the other sits near a zero of order K.`,
  controls: [{ k: 'K', label: 'Daubechies order K', min: 2, max: 10, step: 1, value: 4 },
             { k: 'J', label: 'scale J', min: 2, max: 6, step: 1, value: 4 },
             { k: 'hh', label: 'offset h (×π/2)', min: 0, max: 1, step: 0.1, value: 0.3 }],
  draw(c, p, ctx) {
    const h = ctx.filters.taps[p.K], off = p.hh * K.PI / 2;
    const ls = lin(0.01, Math.pow(2, p.J) * 4 * K.PI, 1800);
    const A = ls.map((l) => K.shatAbs(l * Math.pow(2, -p.J) - off, h));
    const P = ls.map((l) => Math.hypot(...K.prodM0(l, h, 1, p.J)));
    plot(c, { series: [
        { x: ls, y: A, label: '|ŝ(2^-J l − h)|' },
        { x: ls, y: P, label: 'P_J(l), the finite product' },
        { x: ls, y: A.map((a, i) => a * P[i]), label: 'their product', width: 2.6 }],
      ylog: 10, ylim: [1e-10, 3], xlabel: 'l', ylabel: 'magnitude', legend: 'bl' });
    const prod = A.map((a, i) => a * P[i]);
    return `the largest value of the product beyond the zone is
      <b>${Math.max(...prod.slice(Math.floor(prod.length / 4))).toExponential(2)}</b>, while the first
      factor alone reaches <b>${Math.max(...A.slice(Math.floor(A.length / 4))).toExponential(2)}</b>.`;
  },
},
{
  id: 'alias', title: 'The alias weights are probability weights',
  result: 'Lemma 3.18, Remark 3.22',
  blurb: `The renormalised symbol is an average of the continuum symbol over an aliasing class,
    and the weights sum to one <em>exactly</em>, by orthonormality. That is why the lattice vacua
    converge with no regularity hypothesis at all, Haar included.`,
  controls: [{ k: 'K', label: 'Daubechies order K', min: 2, max: 10, step: 1, value: 4 },
             { k: 'M', label: 'steps M', min: 1, max: 8, step: 1, value: 3 },
             { k: 'N', label: 'scale N', min: 1, max: 4, step: 1, value: 2 }],
  draw(c, p, ctx) {
    const h = ctx.filters.taps[p.K];
    const W = K.aliasWeights(0.5, p.N, p.M, h, 5), Winf = K.aliasWeights(0.5, p.N, Infinity, h, 5);
    const sum = W.reduce((s, w) => s + w.w, 0), sumInf = Winf.reduce((s, w) => s + w.w, 0);
    plot(c, { series: [
        { x: W.map((w) => w.i), y: W.map((w) => w.w), label: `finite M = ${p.M}`, points: true, size: 6 },
        { x: Winf.map((w) => w.i), y: Winf.map((w) => w.w), label: 'the limit', points: true, size: 4 }],
      xlabel: 'member of the aliasing class', ylabel: 'weight', ylim: [-0.05, 1.08], legend: 'tr' });
    return `the finite weights sum to <b>${sum.toFixed(10)}</b> and the limiting weights to
      <b>${sumInf.toFixed(10)}</b>. Both are 1 to machine precision, which is the whole of the argument.`;
  },
},
{
  id: 'current', title: 'The current, and the wrap-around that broke the published proof',
  result: 'Lemma 5.1, Theorem 5.2',
  blurb: `The lattice current is a cyclic shift on the momentum lattice. At the zone boundary the
    wrap-around carries a momentum across the Fermi point, so an off-diagonal block of modulus one
    survives at every scale. Truncating instead of wrapping removes it exactly.`,
  controls: [{ k: 'N', label: 'scale N', min: 2, max: 7, step: 1, value: 4 },
             { k: 'kk', label: 'mode k', min: 1, max: 6, step: 1, value: 3 },
             { k: 'mod', label: 'truncated (modified)', type: 'check', value: 1 }],
  draw(c, p, ctx) {
    const lim = Math.pow(2, p.N), ns = [];
    for (let i = -lim; i < lim; i++) ns.push(i + 0.5);
    const img = ns.map((n) => { const m = n + p.kk; return p.mod ? (Math.abs(m) < lim ? m : NaN) : ((m + lim) % (2 * lim)) - lim; });
    /* the defect is the WRAP, not an ordinary sign change: a shift by k moves |k| momenta
       across zero in either case. What only the cyclic shift does is carry momenta from one
       edge of the zone to the other, and those are the ones that cross the Fermi point the
       wrong way and leave an off-diagonal block of modulus one. */
    const wrapped = ns.filter((n) => Math.abs(n + p.kk) >= lim);
    plot(c, { series: [
        { x: ns, y: img, label: p.mod ? 'truncated shift' : 'cyclic shift', points: true, size: 2.2 },
        { x: ns, y: ns, label: 'identity', dash: [4, 4], width: 1.2 }],
      xlabel: 'momentum n', ylabel: 'image of n', hlines: [{ y: 0 }], vlines: [{ x: 0 }], legend: 'tl' });
    return p.mod
      ? `the ${wrapped.length} momenta at the top of the zone are <b>dropped</b> rather than wrapped,
         so nothing is carried across the Fermi point and the off-diagonal Hilbert&ndash;Schmidt norm
         is <b>exactly 0</b> &mdash; at every scale, and for every mode.`
      : `${wrapped.length} momenta <b>wrap</b> from one edge of the zone to the other, crossing the
         Fermi point. They leave an off-diagonal block of modulus one, so the Hilbert&ndash;Schmidt
         norm is <b>${Math.sqrt(p.kk).toFixed(3)}</b> = &radic;(|k|L/&pi;), the same at every scale:
         it does not tend to zero, which is why the published proof pattern is unavailable.`;
  },
},
{
  id: 'budget', title: 'The simulation budget, and why chirality halves the cost',
  result: 'Proposition 6.3, Remark 6.4',
  blurb: `The bottleneck is not the dynamics but the ground state. Its error is first order on the
    full two-component algebra and <em>second</em> order on a chiral subalgebra, which is where the
    conformal structure lives; that squaring is a square root in the qubit count.`,
  controls: [{ k: 'M', label: 'observation scale M', min: 2, max: 8, step: 1, value: 4 },
             { k: 'logeta', label: 'target accuracy 10^', min: -8, max: -1, step: 1, value: -4 },
             { k: 'd', label: 'degree d', min: 1, max: 8, step: 1, value: 2 },
             { k: 'T', label: 'time T', min: 0, max: 10, step: 1, value: 1 }],
  draw(c, p, ctx) {
    const kk = K.PI / (Math.pow(2, -p.M) * K.PI) - 0.5, ds = [];
    for (let i = 1; i <= 9; i++) ds.push(i);
    const full = ds.map((i) => K.vacuumDeviation(p.M + i, kk).full);
    const chir = ds.map((i) => K.vacuumDeviation(p.M + i, kk).chiral);
    plot(c, { series: [{ x: ds, y: full, label: 'full algebra (order 1)' },
                       { x: ds, y: chir, label: 'chiral subalgebra (order 2)' }],
      ylog: 2, xlabel: 'N − M', ylabel: 'η_M(N)', xticks: ds.map((i) => ({ v: i, label: String(i) })), legend: 'bl' });
    const eta = Math.pow(10, p.logeta), base = Math.pow(2, p.M), fac = p.d * (1 + p.T) / eta;
    return `at accuracy 10<sup>${p.logeta}</sup> the chiral route needs about
      <b>${(base * Math.sqrt(fac)).toExponential(2)}</b> qubits and the full algebra about
      <b>${(base * fac).toExponential(2)}</b>: order 2^M&radic;(d(1+T)/&eta;) against 2^M d(1+T)/&eta;.`;
  },
},
{
  id: 'multiplicity', title: 'What the connecting unitaries really require',
  result: 'Zini–Wang note, Corollary 3.2 and Theorem 4.1',
  blurb: `The introduction gave the obstruction as the states failing to be pure. The criterion is
    the <em>constancy</em> of the multiplicity, not its vanishing. It is constant at every finite
    scale, and collapses only in the limit, and only on one of the two routes.`,
  controls: [{ k: 'N', label: 'scale N', min: 2, max: 6, step: 1, value: 3 },
             { k: 'kk', label: 'momentum k', min: 1, max: 30, step: 1, value: 8 }],
  draw(c, p, ctx) {
    const m = Math.pow(2, p.N + 1), Ms = [1, 2, 3, 4, 5, 6, 7];
    plot(c, { series: [
        { x: Ms.concat([8]), y: Ms.map(() => m).concat([m]), label: 'chiral, wavelet', width: 3.2 },
        { x: Ms.concat([8]), y: Ms.map(() => m).concat([0]), label: 'chiral, momentum cutoff', dash: [7, 4] },
        { x: Ms.concat([8]), y: Ms.map(() => 0).concat([0]), label: 'full algebra' }],
      xlabel: 'renormalization step M', ylabel: 'm(S)', ylim: [-2, m * 1.25],
      xticks: Ms.map((x) => ({ v: x, label: String(x) })).concat([{ v: 8, label: '∞' }]),
      vlines: [{ x: 7.5 }], legend: 'tl' });
    return `|&Gamma;| = ${m}, so the collapse is by a factor 2<sup>${m}</sup>. The chiral halves are
      entangled with &Vert;[P(k), p]&Vert; = <b>${f2(K.commutatorNorm(p.N, p.kk))}</b>, and the entropy
      density is exactly 2ln2 &minus; 1 = <b>${K.ENTROPY_DENSITY.toFixed(6)}</b>.`;
  },
},
{
  id: 'duhamel', title: 'Growth in time: exponential, except where it matters',
  result: 'Lemma 4.12, Remark 4.13, Lemma 4.19',
  blurb: `Turning convergence of generators into convergence of the groups they generate costs a
    Gr&ouml;nwall factor. For a non-zero mode it grows exponentially in time; for the zero mode the
    constant vanishes and the factor is exactly linear. The simulation uses the zero mode.`,
  controls: [{ k: 'sigma', label: 'Sobolev index \u03c3', min: 1, max: 3, step: 0.5, value: 2 },
             { k: 'kk', label: 'mode k', min: 0, max: 4, step: 1, value: 2 }],
  draw(c, p, ctx) {
    /* the constant is sigma|k|<k>^{sigma+2}, which for a few units of k is already in the
       thousands, so a fixed time axis would show a vertical line or overflow to infinity.
       The window is chosen from the constant itself and the readout says what it is. */
    const cc = p.kk === 0 ? 0 : p.sigma * Math.abs(p.kk) * Math.pow(Math.hypot(1, p.kk), p.sigma + 2);
    const tmax = p.kk === 0 ? 4 : Math.min(4, 8 / cc);
    const ts = lin(0, tmax, 300);
    plot(c, { series: [
        { x: ts, y: ts.map((t) => K.lambdaDuhamel(p.sigma, p.kk, t)), label: `k = ${p.kk}` },
        { x: ts, y: ts.map((t) => K.lambdaDuhamel(p.sigma, 0, t)), label: 'k = 0 (linear)', dash: [5, 3] }],
      xlabel: 'time t', ylabel: '\u03bb(t)', legend: 'tl' });
    if (p.kk === 0) {
      return `at the zero mode the growth constant vanishes, so &lambda;(t) = |t| exactly:
        <b>${f2(K.lambdaDuhamel(p.sigma, 0, tmax))}</b> at t = ${tmax}. This is the case the
        simulation budget uses, which is why that budget carries no exponential factor.`;
    }
    const at = K.lambdaDuhamel(p.sigma, p.kk, tmax);
    const blow = Math.log(1e308) / cc;
    return `the constant is <b>${f2(cc)}</b>, so the window shown is only t &le; ${tmax.toExponential(2)}:
      &lambda; reaches <b>${f2(at)}</b> there against <b>${f2(tmax)}</b> at the zero mode, and it passes
      the largest representable number at t &asymp; <b>${blow.toExponential(2)}</b>. The bound is
      conservative &mdash; the measured constant behaves like &sigma;|k|&langle;k&rangle; &mdash; but the
      contrast with the zero mode is the point.`;
  },
},
{
  id: 'radius', title: 'The analyticity radius, uniform in the mode',
  result: 'Corollary 4.5, Remark 4.36',
  blurb: `Summing the binomial series instead of bounding it crudely gives a radius of 1/|k|,
    independent of which basis vector you start from. The published estimate gave a radius that
    shrank as the momentum grew.`,
  controls: [{ k: 'kk', label: 'mode k', min: 1, max: 8, step: 1, value: 2 }],
  draw(c, p, ctx) {
    const ms = lin(1, 60, 120);
    plot(c, { series: [
        { x: ms, y: ms.map(() => K.radiusNew(p.kk)), label: 'uniform: 1/|k|' },
        { x: ms, y: ms.map((m) => K.radiusOld(p.kk, m)), label: 'published: 1/(2|m|+|k|)' }],
      ylog: 10, xlabel: 'basis vector m', ylabel: 'radius of convergence', legend: 'tr' });
    const g = K.radiusNew(p.kk) / K.radiusOld(p.kk, 30);
    return `at m = 30 the radius is larger by a factor <b>${g.toFixed(1)}</b>, and the gap grows
      linearly in m. The recorded gains on the tested pairs run from 11 to 101.`;
  },
},
{
  id: 'phase', title: 'The smearing error is a phase',
  result: 'Remark 4.24, Theorem 4.25',
  blurb: `Orthonormality plus the zero of the symbol force the transform to have modulus one to
    order 2K. So the whole smearing error is a phase, whose leading term is the centre of mass;
    removing it turns a first-order error into a third-order one.`,
  controls: [{ k: 'K', label: 'Daubechies order K', min: 2, max: 8, step: 1, value: 4 }],
  draw(c, p, ctx) {
    const h = ctx.filters.taps[p.K], mu = K.centreOfMass(h);
    /* log spacing: the order has to be read near the origin, and linear spacing puts almost
       every sample in the region where the higher-order terms already dominate. */
    const xs = lin(Math.log(1e-4), Math.log(1.2), 400).map(Math.exp);
    /* |1 - shat|, the MODULUS: comparing real parts instead measures |1 - Re shat| ~ mu^2 xi^2/2
       and reports order 2 where the answer is 1. */
    const raw = xs.map((x) => { const s = K.shat(x, h); return Math.hypot(1 - s[0], -s[1]); });
    const rec = xs.map((x) => {
      const s = K.shat(x, h), c = Math.cos(mu * x), si = Math.sin(mu * x);
      return Math.hypot(1 - (c * s[0] - si * s[1]), -(si * s[0] + c * s[1]));
    });
    const flat = xs.map((x) => Math.abs(1 - K.shatAbs(x, h)));
    plot(c, { series: [{ x: xs, y: raw, label: '|1 − ŝ(ξ)|, first order' },
                       { x: xs, y: rec, label: 're-centred, third order' },
                       { x: xs, y: flat, label: '|1 − |ŝ||, order 2K', dash: [4, 3] }],
      xlog: 10, ylog: 10, xlabel: 'ξ', ylabel: 'deviation', legend: 'tl' });
    /* fit each order only where the curve is above the noise floor of the computation and
       below the range where higher-order terms take over; a fixed index window would measure
       the third-order curve in the region where it is 1e-12 and the fit is noise. */
    const ord = (a, lo, hi) => {
      const idx = a.map((v, i) => [v, i]).filter(([v]) => v >= lo && v <= hi).map(([, i]) => i);
      if (idx.length < 8) return NaN;
      const i = idx[0], j = idx[idx.length - 1];
      return Math.log(a[j] / a[i]) / Math.log(xs[j] / xs[i]);
    };
    const oRaw = ord(raw, 1e-9, 1e-2), oRec = ord(rec, 1e-9, 1e-3), oFlat = ord(flat, 1e-13, 1e-3);
    const say = (v) => (Number.isFinite(v) ? v.toFixed(2) : 'not measurable here');
    return `measured orders, each fitted where the curve is above the noise floor: raw
      <b>${say(oRaw)}</b> (predicted 1), re-centred <b>${say(oRec)}</b> (predicted 3), modulus
      <b>${say(oFlat)}</b> against 2K = ${2 * p.K}. The modulus deviation reaches double
      precision quickly, so that last fit uses a narrow window and degrades as K grows; the
      manuscript reports it as measurable only at K = 2 for that reason.`;
  },
},
{
  id: 'jackson', title: 'The aliasing mass, and the estimate that needs it',
  result: 'Lemma 4.28, Theorem 4.29',
  blurb: `The total mass that aliasing moves is one minus the squared modulus of the transform, and
    orthonormality makes it vanish to order 2K. That is what defeats the negative power the momentum
    weight produces; without it the reconstruction estimate is false.`,
  controls: [{ k: 'K', label: 'Daubechies order K', min: 2, max: 8, step: 1, value: 4 }],
  draw(c, p, ctx) {
    const h = ctx.filters.taps[p.K], xs = lin(1e-2, 1.0, 300);
    const d = xs.map((x) => Math.max(1 - Math.pow(K.shatAbs(x, h), 2), 1e-18));
    plot(c, { series: [{ x: xs, y: d, label: 'δ(ξ) = 1 − |ŝ(ξ)|²' }],
      xlog: 10, ylog: 10, xlabel: 'ξ', ylabel: 'aliasing mass', legend: 'tl' });
    const i = 20, j = 150, ord = Math.log(d[j] / d[i]) / Math.log(xs[j] / xs[i]);
    return `measured order <b>${ord.toFixed(2)}</b> against the predicted 2K = <b>${2 * p.K}</b>.
      Every individual aliasing coefficient is therefore of order K, which is what the proof uses.`;
  },
},
{
  id: 'umklapp', title: 'Why the two lattice forms are not directly comparable',
  result: 'Section 4.2.5, equation (277)',
  blurb: `Splitting the two-component lattice over its two sublattices shows that the mode at k
    mixes the single-component mode at k with the <em>umklapp</em> mode at the zone boundary, with
    an amplitude of first order. That is the precise sense of "not directly comparable".`,
  controls: [{ k: 'N', label: 'scale N', min: 2, max: 8, step: 1, value: 4 }],
  draw(c, p, ctx) {
    const eps = Math.pow(2, -p.N) * K.PI, ks = lin(0, K.PI / eps, 300);
    plot(c, { series: [
        { x: ks, y: ks.map((k) => Math.cos(0.25 * eps * k)), label: 'weight of the mode at k' },
        { x: ks, y: ks.map((k) => Math.sin(0.25 * eps * k)), label: 'weight of the umklapp mode' }],
      xlabel: 'mode k', ylabel: 'amplitude', ylim: [-0.05, 1.05], legend: 'tl' });
    const kmax = K.PI / eps;
    return `at the zone boundary the umklapp weight reaches
      <b>${Math.sin(0.25 * eps * kmax).toFixed(4)}</b>. For a fixed mode it is of order &epsilon;<sub>N</sub>k,
      so the two forms agree to leading order and differ at first order.`;
  },
},
{
  id: 'discrepancy', title: 'The modified approximants still satisfy the algebra',
  result: 'Remark 4.2',
  blurb: `Truncating rather than wrapping changes the commutator only for modes of opposite sign,
    and then only within a few steps of the zone boundary. For same-sign modes, and for the pair the
    energy bound uses, the discrepancy vanishes identically.`,
  controls: [{ k: 'sigma', label: 'Sobolev index σ', min: 1, max: 3, step: 1, value: 2 }],
  draw(c, p, ctx) {
    const Ns = [3, 4, 5, 6, 7, 8];
    const C = { 1: 4.0, 2: 15.0, 3: 5.5 }[p.sigma];
    const v = Ns.map((N) => C * Math.pow(Math.pow(2, -N) * K.PI, p.sigma));
    const rem = Ns.map((N) => Math.pow(Math.pow(2, -N) * K.PI, 2));
    plot(c, { series: [
        { x: Ns, y: v, label: `‖D‖ on h^σ → h⁰, σ = ${p.sigma}` },
        { x: Ns, y: rem, label: 'the O(ε²) remainder it accompanies', dash: [5, 3] }],
      ylog: 2, xlabel: 'scale N', ylabel: 'norm', xticks: Ns.map((n) => ({ v: n, label: String(n) })), legend: 'bl' });
    return `for same-sign modes the discrepancy is <b>identically zero</b>. For opposite signs it is
      finite rank and of order &epsilon;<sup>&sigma;</sup>, so it beats the accompanying remainder once
      &sigma; &gt; 2. Constants recorded from <code>numerics/os_check18.py</code>.`;
  },
},
];
