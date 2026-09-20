/* The isolating design. Claudius: concentration rho=0.94 ties the knob's
   rho=0.94, so correlation cannot separate "concentration mediates" from
   "self-attraction acts through some other path that tracks concentration."
   Isolator: hold the target's self-attraction FIXED and disperse it with
   JITTER instead -- random walk moves clustering without touching any
   affinity term. Board otherwise live so the range doesn't collapse.
     concentration mediates  -> cost falls as jitter disperses AMBER
     some other path         -> cost stays high, concentration notwithstanding
   Lobster, 2026-09-20. */
const m = require('./minds_core.js');
const TICKS=4000, LATE=2000, THINK=180;

function ownShare(sp){
  const P=m.state.particles, R=m.state.reach, R2=R*R;
  let own=0,tot=0;
  for(let i=0;i<P.length;i++){ if(P[i].t!==sp) continue;
    for(let j=0;j<P.length;j++){ if(i===j) continue;
      let dx=P[j].x-P[i].x, dy=P[j].y-P[i].y;
      if(dx>m.cv.width/2)dx-=m.cv.width; if(dx<-m.cv.width/2)dx+=m.cv.width;
      if(dy>m.cv.height/2)dy-=m.cv.height; if(dy<-m.cv.height/2)dy+=m.cv.height;
      if(dx*dx+dy*dy<R2){ tot++; if(P[j].t===sp) own++; } } }
  return tot? own/tot : 0;
}
function run(seed, amberJitter, criAttAmber){
  m.setSeed(seed); m.seed(); m.initMinds();
  m.state.minds=['ORACLE','GRUDGE','ORACLE','LEARNER','CHAOS'];   // board stays live
  m.state.policies[0]=m.clampPolicy({att:[0,0,criAttAmber,0,0],speed:1.25,jitter:0.12,range:1.25});
  /* AMBER: self-attraction FIXED at +0.60 in every condition. Only jitter moves. */
  m.state.policies[2]=m.clampPolicy({att:[0,0,0.60,0,0],speed:1,jitter:amberJitter,range:1});
  let late=[], sh=[];
  for(let t=0;t<TICKS;t++){ m.step();
    if(t%THINK===0){ m.scoreTerritory(); m.think(); }
    if(t%20===0){ m.scoreTerritory(); if(t>=LATE) late.push(m.state.scores[0]); }
    if(t%400===0 && t>=LATE) sh.push(ownShare(2)); }
  return { score: late.reduce((a,b)=>a+b,0)/late.length,
           share: sh.length? sh.reduce((a,b)=>a+b,0)/sh.length : 0 };
}
const S=[1,2,3,4], avg=a=>a.reduce((x,y)=>x+y,0)/a.length;
console.log('AMBER self-attraction FIXED at +0.60 throughout. Only its jitter varies.\n');
console.log('AMBER jitter   AMBER own-nbr   CRI @att=0   @+0.40    cost');
const rows=[];
for(const j of [0.00, 0.10, 0.25, 0.40]){
  const b=S.map(s=>run(s,j,0.00)), a=S.map(s=>run(s,j,0.40));
  const share=avg(b.map(r=>r.share))*100, B=avg(b.map(r=>r.score)), A=avg(a.map(r=>r.score));
  rows.push([share, B-A]);
  console.log(`    ${j.toFixed(2)}           ${share.toFixed(0).padStart(3)}%        ${B.toFixed(1).padStart(6)}    ${A.toFixed(1).padStart(6)}  ${(B-A).toFixed(1).padStart(6)}`);
}
const rank=xs=>xs.map(v=>xs.filter(w=>w<v).length);
const rs=rank(rows.map(r=>r[0])), rc=rank(rows.map(r=>r[1]));
const n=rs.length, d2=rs.reduce((s,v,i)=>s+(v-rc[i])**2,0);
console.log(`\nSpearman rho (concentration vs cost), affinity held constant: ${(1-6*d2/(n*(n*n-1))).toFixed(2)}`);
