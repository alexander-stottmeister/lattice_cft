/* Kernels of the lattice-CFT page: the same formulas the numerics use, in the browser.
 *
 * Conventions match the manuscript and numerics/: L = pi, eps_N = 2^-N pi,
 *   m0(xi)   = 2^-1/2 sum_n h_n e^{-i n xi}
 *   shat(xi) = prod_{j>=1} m0(2^-j xi), truncated adaptively
 * The filter taps come from data/filters.json, produced by tools/make_data.py, so the page
 * and the Python agree by construction rather than by transcription.
 */
export const PI = Math.PI;

/* --- complex helpers, kept minimal ------------------------------------------------- */
const cmul = (a, b) => [a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]];
const cabs = (a) => Math.hypot(a[0], a[1]);

export function m0(xi, h) {
  let re = 0, im = 0;
  for (let n = 0; n < h.length; n++) { const p = -n * xi; re += h[n] * Math.cos(p); im += h[n] * Math.sin(p); }
  const s = 1 / Math.SQRT2;
  return [re * s, im * s];
}

export function shat(xi, h, J) {
  if (J === undefined) J = Math.ceil(Math.log2(Math.max(Math.abs(xi), 1))) + 32;
  let acc = [1, 0];
  for (let j = 1; j <= J; j++) acc = cmul(acc, m0(xi * Math.pow(2, -j), h));
  return acc;
}
export const shatAbs = (xi, h, J) => cabs(shat(xi, h, J));

/* finite product, never formed as a quotient: this is the repair of Finding 1 */
export function prodM0(xi, h, jmin, jmax) {
  let acc = [1, 0];
  for (let j = jmin; j <= jmax; j++) acc = cmul(acc, m0(xi * Math.pow(2, -j), h));
  return acc;
}

export const centreOfMass = (h) => h.reduce((s, hn, n) => s + n * hn, 0) / Math.SQRT2;

/* --- momentum-cutoff operator norms, numerics/os_check12.py ------------------------ */
export function opnorm(N, k, delta, pad = 5) {
  const eps = Math.pow(2, -N) * PI, lim = PI / eps, c = Math.pow(Math.cos(0.25 * eps * k), 2);
  const M = Math.pow(2, N + pad);
  let best = 0;
  for (let i = -M; i < M; i++) {
    const n = i + 0.5;
    const chi = (Math.abs(n - k) < lim ? 1 : 0) * (Math.abs(n) < lim ? 1 : 0);
    const d = c * Math.sin(eps * (n - 0.5 * k)) / eps * chi - (n - 0.5 * k);
    const v = Math.abs(d) / Math.pow(1 + Math.abs(n), 1 + delta);
    if (v > best) best = v;
  }
  return best;
}

export function hsnorm(N, k) {
  const eps = Math.pow(2, -N) * PI, lim = PI / eps, c = Math.pow(Math.cos(0.25 * eps * k), 2);
  let s = 0;
  for (let i = -4 * Math.abs(k) - 4; i <= 4 * Math.abs(k) + 4; i++) {
    const n = i + 0.5;
    if (!(n > 0 && n - k < 0)) continue;
    const chi = (Math.abs(n - k) < lim ? 1 : 0) * (Math.abs(n) < lim ? 1 : 0);
    const d = c * Math.sin(eps * (n - 0.5 * k)) / eps * chi - (n - 0.5 * k);
    s += d * d;
  }
  return Math.sqrt(s);
}

/* --- vacuum symbol deviation, numerics/os_check14.py ------------------------------- */
export function vacuumDeviation(N, k) {
  const eps = Math.pow(2, -N) * PI;
  return { full: Math.abs(Math.sin(0.25 * eps * k)), chiral: Math.pow(Math.sin(0.25 * eps * k), 2) };
}

/* --- Duhamel growth factor, v5 Lemma 4.12 ------------------------------------------ */
export function lambdaDuhamel(sigma, k, t, CL = 1) {
  if (k === 0) return Math.abs(t);
  const c = CL * sigma * Math.abs(k) * Math.pow(Math.hypot(1, k), sigma + 2);
  return (Math.exp(c * Math.abs(t)) - 1) / c;
}

/* --- analyticity radius, v5 Corollary 4.5 ------------------------------------------ */
export const radiusNew = (k) => 1 / Math.abs(k);
export const radiusOld = (k, m) => 1 / (2 * Math.abs(m) + Math.abs(k));

/* --- alias weights, v5 Lemma 3.18 -------------------------------------------------- */
export function aliasWeights(l, N, M, h, reach = 6) {
  /* w_M(k) over the aliasing class of l: |prod_{j=1..M} m0(eps_{N+j} k)|^2, which sums to 1 */
  const eps = Math.pow(2, -N) * PI, out = [];
  for (let i = -reach; i <= reach; i++) {
    const k = l + (2 * PI / eps) * i;
    let w;
    if (M === Infinity) w = Math.pow(shatAbs(eps * k, h), 2);
    else w = Math.pow(cabs(prodM0(eps * k, h, 1, M)), 2);
    out.push({ i, k, w });
  }
  return out;
}

/* --- rate fitting ------------------------------------------------------------------- */
export function fitRate(Ns, vals) {
  const n = Ns.length;
  const xs = Ns, ys = vals.map((v) => Math.log2(v));
  const mx = xs.reduce((a, b) => a + b, 0) / n, my = ys.reduce((a, b) => a + b, 0) / n;
  let num = 0, den = 0;
  for (let i = 0; i < n; i++) { num += (xs[i] - mx) * (ys[i] - my); den += (xs[i] - mx) ** 2; }
  return -num / den;
}

export const ENTROPY_DENSITY = 2 * Math.log(2) - 1;
export const commutatorNorm = (N, k) => 0.5 * Math.abs(Math.sin(0.5 * Math.pow(2, -N) * PI * k));
