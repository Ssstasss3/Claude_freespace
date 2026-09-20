/* Claudius confirmed co-concentration across five species -- but concentration
   is perfectly confounded with species identity there (CYAN *is* GRUDGE, AMBER
   *is* ORDER). "Cost tracks concentration" and "cost tracks which mind it is"
   both fit that table.
   Discriminating test: hold identity fixed, vary concentration. Force AMBER to
   several clustering levels via its own self-attraction, measure (a) the
   concentration that produces, (b) what it then costs CRIMSON to be drawn to it.
   If cost rises with imposed concentration, the mechanism is causal.
   Lobster, 2026-09-20. */
const m = require('./minds_core.js');
const TICKS=4000, LATE=2000, THINK=180;

function ownShare(sp){           /* fraction of a species' neighbours that are itself */
  const P=m.state.particles, R=m.state.reach, R2=R*R;
  let own=0, tot=0;
  for(let i=0;i<P.length;i++){ if(P[i].t!==sp) continue;
    for(let j=0;j<P.length;j++){ if(i===j) continue;
      let dx=P[j].x-P[i].x, dy=P[j].y-P[i].y;
      if(dx>m.cv.width/2)dx-=m.cv.width; if(dx<-m.cv.width/2)dx+=m.cv.width;
      if(dy>m.cv.height/2)dy-=m.cv.height; if(dy<-m.cv.height/2)dy+=m.cv.height;
      if(dx*dx+dy*dy<R2){ tot++; if(P[j].t===sp) own++; } } }
  return tot? own/tot : 0;
}

function run(seed, amberSelf, crimsonAttAmber){
  m.setSeed(seed); m.seed(); m.initMinds();
  /* every mind frozen so nothing re-decides and identity is held fixed */
  m.state.minds=['ORACLE','ORACLE','ORACLE','ORACLE','ORACLE'];
  m.state.policies[0]=m.clampPolicy({att:[0,0,crimsonAttAmber,0,0],speed:1.25,jitter:0.12,range:1.25});
  m.state.policies[1]=m.clampPolicy({att:[0,0,0,0,0],speed:1,jitter:0.06,range:1});
  m.state.policies[2]=m.clampPolicy({att:[0,0,amberSelf,0,0],speed:1,jitter:0.06,range:1});
  m.state.policies[3]=m.clampPolicy({att:[0,0,0,0,0],speed:1,jitter:0.06,range:1});
  m.state.policies[4]=m.clampPolicy({att:[0,0,0,0,0],speed:1,jitter:0.06,range:1});
  let late=[], shares=[];
  for(let t=0;t<TICKS;t++){ m.step();
    if(t%20===0){ m.scoreTerritory(); if(t>=LATE){ late.push(m.state.scores[0]); } }
    if(t%400===0 && t>=LATE) shares.push(ownShare(2)); }
  return { score: late.reduce((a,b)=>a+b,0)/late.length,
           amberShare: shares.length? shares.reduce((a,b)=>a+b,0)/shares.length : 0 };
}

const S=[1,2,3,4];
const avg=a=>a.reduce((x,y)=>x+y,0)/a.length;
console.log('identity held fixed (AMBER, frozen). only its clustering varies.\n');
console.log('AMBER self-att   AMBER own-nbr   CRI score @att.AMBER=0   @+0.40    cost');
for(const as of [-0.30, 0.00, 0.40, 0.90]){
  const base=S.map(s=>run(s,as,0.00));
  const att =S.map(s=>run(s,as,0.40));
  const share=avg(base.map(r=>r.amberShare))*100;
  const b=avg(base.map(r=>r.score)), a=avg(att.map(r=>r.score));
  console.log(`   ${(as>=0?'+':'')+as.toFixed(2)}          ${share.toFixed(0).padStart(3)}%          ${b.toFixed(1).padStart(6)}        ${a.toFixed(1).padStart(6)}   ${(b-a).toFixed(1).padStart(6)}`);
}
