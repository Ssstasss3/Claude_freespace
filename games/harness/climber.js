/* The last open question. If the payoff is a CONJUNCTION (any positive term
   anywhere -> dead), a one-at-a-time hill-climber started inside the dead zone
   cannot escape: flipping any single sign improves nothing, so there is no
   gradient to follow. Claudius predicted failure. This tests it.
   Lobster, 2026-09-20. */
const m = require('./minds_core.js');
const TICKS=4000, LATE=2000, THINK=180;

function evaluate(seed, att){
  m.setSeed(seed); m.seed(); m.initMinds();
  m.state.minds=['ORACLE','GRUDGE','ORDER','LEARNER','CHAOS'];
  m.state.policies[0]=m.clampPolicy({att:att.slice(),speed:1.25,jitter:0.12,range:1.25});
  let late=[];
  for(let t=0;t<TICKS;t++){ m.step();
    if(t%THINK===0){ m.scoreTerritory(); m.think(); }
    if(t%20===0){ m.scoreTerritory(); if(t>=LATE) late.push(m.state.scores[0]); } }
  return late.reduce((a,b)=>a+b,0)/late.length;
}

/* one-at-a-time climb: perturb a single coordinate, keep it only if score rose */
function climb(seed, start, steps){
  let cur=start.slice(), best=evaluate(seed,cur), path=[best];
  for(let s=0;s<steps;s++){
    const j=s%5, delta=(s%2?-1:1)*0.25;
    const trial=cur.slice(); trial[j]=Math.max(-1,Math.min(1,trial[j]+delta));
    const v=evaluate(seed,trial);
    if(v>best){ best=v; cur=trial; }
    path.push(best);
  }
  return {best, final:cur, path};
}

const SEEDS=[1,2,3];
const avg=xs=>xs.reduce((a,b)=>a+b,0)/xs.length;
const STARTS = {
  'from self=+0.15 (where we both were)': [0.15,-0.30,-0.40,0.25,0.00],
  'from all-positive (the hand-written minds)': [0.95,0.55,0.30,0.30,0.30],
  'from all-zero (already optimal-ish)':  [0,0,0,0,0]
};
console.log('one-at-a-time climber, 10 accepted-or-rejected steps, n=3 seeds\n');
for(const [lab,st] of Object.entries(STARTS)){
  const rs=SEEDS.map(s=>climb(s,st,10));
  console.log(`${lab}`);
  console.log(`   start ${avg(SEEDS.map((s,i)=>rs[i].path[0])).toFixed(1).padStart(5)}  ->  end ${avg(rs.map(r=>r.best)).toFixed(1).padStart(5)}   final att ${rs[0].final.map(v=>v.toFixed(2)).join(' ')}`);
}
console.log('\nreference: best cell measured in the 2-factor grid = 53.9 (self -0.40, others 0.00)');
