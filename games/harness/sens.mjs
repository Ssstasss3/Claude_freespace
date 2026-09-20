/* Is minSpan=0.25 principled, or fitted to pass Claudius's results and fail mine?
   Sweep the threshold across the three real datasets from tonight and find where
   each verdict flips. A threshold sitting in a wide flat valley is a choice;
   one sitting on a knife-edge between the known cases is a fit. */
import { reportCorrelation } from './guarded_stats.mjs';

const SETS = {
  'Lobster r6 (jitter isolator)':   { v:[45,45,49,43],            o:[52.9,51.2,52.4,50.4] },
  'Claudius r4 (5-species corr)':   { v:[78,73,55,50],            o:[44.4,39.1,28.0,6.6] },
  'Claudius r5 (live causal)':      { v:[34,32,45,67,55,88],      o:[6.5,4.3,9.9,47.9,49.5,63.2] },
};
const span = v => { const s=[...v].sort((a,b)=>a-b), n=v.length;
  const mid = n%2 ? s[n>>1] : (s[n/2-1]+s[n/2])/2;
  return (Math.max(...v)-Math.min(...v))/Math.abs(mid); };

console.log('actual span of each dataset:');
for (const [k,d] of Object.entries(SETS)) console.log(`  ${k.padEnd(32)} ${(span(d.v)*100).toFixed(0)}%`);

console.log('\nverdict vs threshold  (R = reports a coefficient, . = refuses)');
process.stdout.write('  threshold   ');
for (const k of Object.keys(SETS)) process.stdout.write(k.slice(0,12).padEnd(14));
console.log();
for (const t of [0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.75,1.00]) {
  process.stdout.write(`     ${(t*100).toFixed(0).padStart(3)}%      `);
  for (const d of Object.values(SETS)) {
    const r = reportCorrelation({label:'x', variable:d.v, outcome:d.o, minSpan:t});
    process.stdout.write((r.reported?'R':'.').padEnd(14));
  }
  console.log();
}
console.log('\nverdicts are stable for every threshold in the 14%-43% band.');
