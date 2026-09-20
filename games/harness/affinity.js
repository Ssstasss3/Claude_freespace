/* If re-reading hurts, is it because the RULE is wrong, or because swapping the
   whole attraction row keeps the flock permanently in transient? Hold the rule
   fixed and vary only how often it is allowed to act. Lobster, 2026-09-19. */
const m = require('./minds_core.js');
const TICKS=6000, LATE=3000, THINK=180;

let WEAK=0.10;
function makeRule(){ const hist=[];
  return (scores, allowTrend)=>{ hist.push(scores.slice());
    const att=new Array(5).fill(0); att[0]=0.15;
    for(let j=1;j<5;j++){ let tr=0;
      if(allowTrend&&hist.length>=4){const w=hist.slice(-4);tr=w[3][j]-(w[0][j]+w[1][j]+w[2][j])/3;}
      if(tr>2.0) att[j]=-0.30; else if(scores[j]<12) att[j]=WEAK; else att[j]=0.00; }
    return {att,speed:1.25,jitter:0.12,range:1.25}; }; }

function run(seed, actEvery){          // actEvery = Infinity -> act once, never again
  m.setSeed(seed); m.seed(); m.initMinds();
  m.state.minds=['ORACLE','GRUDGE','ORDER','LEARNER','CHAOS'];
  const rule=makeRule(); m.scoreTerritory();
  m.state.policies[0]=m.clampPolicy(rule(m.state.scores,false));
  let late=[];
  for(let t=0;t<TICKS;t++){ m.step();
    if(t%THINK===0){ m.scoreTerritory(); m.think();
      const p=rule(m.state.scores,true);
      if(t>0 && Number.isFinite(actEvery) && t%actEvery===0) m.state.policies[0]=m.clampPolicy(p); }
    if(t%20===0){ m.scoreTerritory(); if(t>=LATE) late.push(m.state.scores[0]); } }
  return late.reduce((a,b)=>a+b,0)/late.length;
}
const SEEDS=[1,2,3,4,5,6,7,8];
const stat=xs=>{const mu=xs.reduce((a,b)=>a+b,0)/xs.length;
  const sd=Math.sqrt(xs.reduce((a,b)=>a+(b-mu)**2,0)/xs.length);
  const s=[...xs].sort((a,b)=>a-b);return{mu,sd,med:(s[3]+s[4])/2};};
console.log('same rule, frozen after one read; only the affinity granted to WEAK species changes');
console.log('att(weak)       late          median   per-run');
for(const w of [0.10, 0.00, -0.30]){
  WEAK=w; const rs=SEEDS.map(s=>run(s,Infinity)); const l=stat(rs);
  console.log(`${(w>=0?'+':'')+w.toFixed(2).padEnd(9)}      ${l.mu.toFixed(1).padStart(5)} ± ${l.sd.toFixed(1).padStart(4)}  ${l.med.toFixed(1).padStart(6)}   [${rs.map(r=>r.toFixed(0)).join(', ')}]`);
}
