/* Check that the browser kernels reproduce the Python numbers.
 *
 *     node tools/check_js.mjs
 *
 * The page recomputes the paper's quantities live; this is what makes that honest rather
 * than decorative. Exits non-zero on disagreement, so it belongs in the pre-flight audit.
 */
import { readFileSync } from 'fs';
import * as K from '../docs/assets/kernels.js';
const F = JSON.parse(readFileSync(new URL('../docs/data/filters.json', import.meta.url)));
const R = JSON.parse(readFileSync(new URL('../docs/data/recorded.json', import.meta.url)));
let worst = 0, lines = [];
// centre of mass against Python
for (const k of Object.keys(F.taps)) {
  const d = Math.abs(K.centreOfMass(F.taps[k]) - F.mu[k]); worst = Math.max(worst, d);
}
lines.push(['centre of mass, K=2..12', worst]);
// shat(0) = 1 and the zeros at 2 pi n
const h4 = F.taps['4'];
lines.push(['shat(0) - 1', Math.abs(K.shatAbs(0, h4) - 1)]);
lines.push(['|shat(2 pi)| (a zero)', K.shatAbs(2 * Math.PI, h4)]);
// operator norms against the Python table
let wo = 0;
for (const d of Object.keys(R.momentum_cutoff_opnorm.by_delta)) {
  const e = R.momentum_cutoff_opnorm.by_delta[d];
  e.N.forEach((N, i) => { wo = Math.max(wo, Math.abs(K.opnorm(N, 2, parseFloat(d)) / e.value[i] - 1)); });
}
lines.push(['momentum-cutoff opnorm, rel. err', wo]);
let wh = 0;
for (const k of Object.keys(R.momentum_cutoff_hs.by_k)) {
  const e = R.momentum_cutoff_hs.by_k[k];
  e.N.forEach((N, i) => { wh = Math.max(wh, Math.abs(K.hsnorm(N, parseFloat(k)) / e.value[i] - 1)); });
}
lines.push(['off-diagonal HS norm, rel. err', wh]);
// vacuum deviation
const V = R.vacuum_deviation; let wv = 0;
V.N.forEach((N, i) => {
  const d = K.vacuumDeviation(N, V.k);
  wv = Math.max(wv, Math.abs(d.full / V.full[i] - 1), Math.abs(d.chiral / V.chiral[i] - 1));
});
lines.push(['vacuum deviation, rel. err', wv]);
// fitted rate reproduces min(delta,2)
const rr = ['0','0.5','1','2','3'].map(d => {
  const Ns=[4,5,6,7,8], v=Ns.map(N=>K.opnorm(N,2,parseFloat(d)));
  return [d, K.fitRate(Ns,v), Math.min(parseFloat(d),2)];
});
console.log('  check                                 value');
for (const [n, v] of lines) console.log('  %s %s', n.padEnd(36), v.toExponential(2));
console.log('\n  fitted rate vs predicted:');
for (const [d, f, p] of rr) console.log('    delta = %s   fitted %s   predicted %s', d.padEnd(4), f.toFixed(3), p.toFixed(1));
const ok = lines.every(([, v]) => v < 1e-6) && rr.every(([, f, p]) => Math.abs(f - p) < 0.06);
console.log('\n  -> %s', ok ? 'JS agrees with the Python' : 'MISMATCH');
process.exit(ok ? 0 : 1);
