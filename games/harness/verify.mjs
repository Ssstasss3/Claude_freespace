import { reportCorrelation } from './guarded_stats.mjs';
const C = [
  ['median 5.00, tiny span (was correct)',      {variable:[4.99,5,5,5.01], outcome:[8,3,9,2]},                         false],
  ['median 0.00, tiny span, NO fullRange',      {variable:[-0.01,0,0,0.01], outcome:[8,3,9,2]},                        false],
  ['median 0.00, tiny span, fullRange 2.0',     {variable:[-0.01,0,0,0.01], outcome:[8,3,9,2], fullRange:2.0},         false],
  ['att swept -0.30..+0.30, fullRange 2.0',     {variable:[-0.3,-0.1,0.1,0.3], outcome:[8,6,4,2], fullRange:2.0},      true ],
  ['my round 6 (must stay refused)',            {variable:[45,45,49,43], outcome:[52.9,51.2,52.4,50.4]},               false],
  ['Claudius round 5 (must stay reported)',     {variable:[34,32,45,67,55,88], outcome:[6.5,4.3,9.9,47.9,49.5,63.2]},  true ],
];
let pass = 0;
for (const [name, args, expect] of C) {
  const r = reportCorrelation({label:name, ...args});
  const ok = r.reported === expect;
  pass += ok;
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name.padEnd(42)} reported=${String(r.reported).padEnd(5)} expected=${expect}`);
  if (!ok) console.log(r.text);
}
console.log(`\n${pass}/${C.length} — the fail-open case is ${pass===C.length ? 'closed' : 'STILL OPEN'}`);
