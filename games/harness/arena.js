/* Headless MINDS arena — Lobster, 2026-09-19.
   Reproduces Claudius's setup: CRIMSON=ORACLE(frozen), VIOLET=LEARNER,
   CYAN=GRUDGE, AMBER=ORDER, JADE=CHAOS. 6000 ticks, late = ticks 3000-6000. */
const m = require('./minds_core.js');
const TICKS = 6000, LATE = 3000, THINK = 180;

function run(seed, oraclePolicy, hook) {
    m.setSeed(seed); m.seed(); m.initMinds();
    m.state.minds = ['ORACLE','GRUDGE','ORDER','LEARNER','CHAOS'];
    m.state.policies[0] = m.clampPolicy(Object.assign(m.blankPolicy(), oraclePolicy()));
    let early = [], late = [];
    for (let t = 0; t < TICKS; t++) {
        m.step();
        if (t % THINK === 0) {
            m.scoreTerritory();
            m.think();
            if (hook) hook(t, m);          // re-reading minds act here
        }
        if (t % 20 === 0) {
            m.scoreTerritory();
            (t < LATE ? early : late).push(m.state.scores[0] * 100);
        }
    }
    const avg = a => a.reduce((x,y)=>x+y,0) / a.length;
    return { early: avg(early), late: avg(late) };
}

const A = v => () => ({ att:[0.15,-0.30,-0.40,v,0.00], speed:1.25, jitter:0.12, range:1.25 });
const SEEDS = [1,2,3,4,5,6,7,8];
const stat = xs => { const mu = xs.reduce((a,b)=>a+b,0)/xs.length;
    const sd = Math.sqrt(xs.reduce((a,b)=>a+(b-mu)**2,0)/xs.length);
    const s=[...xs].sort((a,b)=>a-b); const med=s[Math.floor(s.length/2)];
    return {mu, sd, med}; };

console.log('VALIDATION — reproducing Claudius\'s att.VIOLET sweep');
console.log('arm                early    late            per-run late');
for (const [name, v, theirs] of [['lobster',0.25,3.3],['noVIO',0.00,6.8],['antVIO',-0.30,15.5]]) {
    const rs = SEEDS.map(s => run(s, A(v)));
    const e = stat(rs.map(r=>r.early)), l = stat(rs.map(r=>r.late));
    console.log(`${name.padEnd(16)} ${e.mu.toFixed(1).padStart(6)}  ${l.mu.toFixed(1).padStart(5)} ± ${l.sd.toFixed(1).padStart(4)}   [${rs.map(r=>r.late.toFixed(0)).join(', ')}]   (theirs: ${theirs})`);
}
