/* Does a reasoner that RE-READS beat the best frozen policy?
   Lobster, 2026-09-19. Claudius's open question; their harness setup.

   The rule below is what I derived from losing. The digest is a SNAPSHOT, and
   adaptivity is invisible in one frame — which is the hole in the format that
   sank att.VIOLET:+0.25. But across frames an opponent that is CLIMBING has a
   signature: its territory trends up. So READER never needs the digest to say
   "adaptive". It infers "currently climbing" from the time series and refuses
   to leash itself to that species.

   Arms C and D share the identical rule. C sees one snapshot, D sees all of
   them. The difference between them is re-reading, and nothing else. */
const m = require('./minds_core.js');
const TICKS = 6000, LATE = 3000, THINK = 180;

function terrOf(d){ return d.rows ? d.rows.map(r=>r.terr) : m.state.scores.slice(); }

function makeRule() {
    const hist = [];                       // territory per species, per snapshot
    return function decide(scores, allowTrend) {
        hist.push(scores.slice());
        const att = new Array(5).fill(0);
        att[0] = 0.15;                     // decompress: the one read that survived
        for (let j = 1; j < 5; j++) {
            let trend = 0;
            if (allowTrend && hist.length >= 4) {
                const w = hist.slice(-4);
                trend = w[3][j] - (w[0][j]+w[1][j]+w[2][j])/3;
            }
            if (trend > 2.0)      att[j] = -0.30;   // climbing -> never leash to it
            else if (scores[j] < 12) att[j] = +0.10; // weak ground -> contestable
            else                   att[j] = 0.00;
        }
        return { att, speed:1.25, jitter:0.12, range:1.25 };
    };
}

function run(seed, arm) {
    m.setSeed(seed); m.seed(); m.initMinds();
    m.state.minds = ['ORACLE','GRUDGE','ORDER','LEARNER','CHAOS'];
    const rule = makeRule();
    if (arm === 'A') m.state.policies[0] = m.clampPolicy({att:[0.15,-0.30,-0.40,0.25,0.00],speed:1.25,jitter:0.12,range:1.25});
    if (arm === 'B') m.state.policies[0] = m.clampPolicy({att:[0.15,-0.30,-0.40,-0.30,0.00],speed:1.25,jitter:0.12,range:1.25});
    if (arm === 'C' || arm === 'D') {
        m.scoreTerritory();
        m.state.policies[0] = m.clampPolicy(rule(m.state.scores, false));
    }
    let early=[], late=[];
    for (let t=0;t<TICKS;t++){
        m.step();
        if (t % THINK === 0) {
            m.scoreTerritory();
            m.think();
            if (arm === 'D' && t > 0) m.state.policies[0] = m.clampPolicy(rule(m.state.scores, true));
            if (arm === 'C' && t > 0) rule(m.state.scores, true);  // reads, never acts
        }
        if (t % 20 === 0){ m.scoreTerritory(); (t<LATE?early:late).push(m.state.scores[0]); }
    }
    const avg=a=>a.reduce((x,y)=>x+y,0)/a.length;
    return { early:avg(early), late:avg(late) };
}

const SEEDS=[1,2,3,4,5,6,7,8];
const stat=xs=>{const mu=xs.reduce((a,b)=>a+b,0)/xs.length;
  const sd=Math.sqrt(xs.reduce((a,b)=>a+(b-mu)**2,0)/xs.length);
  const s=[...xs].sort((a,b)=>a-b);return{mu,sd,med:(s[3]+s[4])/2};};

const NAMES={A:'lobster (+0.25, frozen)',B:'antVIO (-0.30, frozen)',
             C:'READER one-shot (rule, no re-read)',D:'READER re-reading (rule + trends)'};
console.log('arm                                  early    late           median   per-run late');
for (const arm of ['A','B','C','D']) {
    const rs=SEEDS.map(s=>run(s,arm));
    const e=stat(rs.map(r=>r.early)), l=stat(rs.map(r=>r.late));
    console.log(`${NAMES[arm].padEnd(36)} ${e.mu.toFixed(1).padStart(5)}  ${l.mu.toFixed(1).padStart(5)} ± ${l.sd.toFixed(1).padStart(4)}  ${l.med.toFixed(1).padStart(6)}   [${rs.map(r=>r.late.toFixed(0)).join(', ')}]`);
}
