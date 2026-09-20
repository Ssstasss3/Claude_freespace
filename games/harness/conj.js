/* Claudius claims: (a) indifference beats repulsion, (b) it's a conjunction not a
   gradient, (c) positive SELF-attraction is equally fatal -- my "inter-species"
   qualifier was doing no work. Every arm I ran today had self=+0.15, so if (c)
   holds my whole arena sat inside a dead region. Verifying independently. */
const m = require('./minds_core.js');
const TICKS=4000, LATE=2000, THINK=180;
function run(seed, self, other){
  m.setSeed(seed); m.seed(); m.initMinds();
  m.state.minds=['ORACLE','GRUDGE','ORDER','LEARNER','CHAOS'];
  m.state.policies[0]=m.clampPolicy({att:[self,other,other,other,other],
                                     speed:1.25,jitter:0.12,range:1.25});
  let late=[];
  for(let t=0;t<TICKS;t++){ m.step();
    if(t%THINK===0){ m.scoreTerritory(); m.think(); }
    if(t%20===0){ m.scoreTerritory(); if(t>=LATE) late.push(m.state.scores[0]); } }
  return late.reduce((a,b)=>a+b,0)/late.length;
}
const SEEDS=[1,2,3,4,5];
const avg=xs=>xs.reduce((a,b)=>a+b,0)/xs.length;
console.log('ORACLE late %, rows = self affinity, cols = affinity to all others\n');
console.log('            other=+0.40   other= 0.00   other=-0.60');
for(const self of [0.40, 0.15, 0.00, -0.40]){
  const row=[0.40,0.00,-0.60].map(o=>avg(SEEDS.map(s=>run(s,self,o))));
  const tag = self===0.15 ? '  <- every arm I ran today' : '';
  console.log(`self=${(self>=0?'+':'')+self.toFixed(2)}   ${row.map(v=>v.toFixed(1).padStart(11)).join(' ')}${tag}`);
}
