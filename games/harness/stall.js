/* Two things at once.
   (1) Claudius says my climber's endpoint is not a local optimum: a single
       `self` move pays hugely. Test every single-coordinate move from it.
   (2) Their conjunction claim -- and MY reproduction of it -- moved all four
       inter-species terms together, so "one positive term" was really four.
       Test ONE positive term at a time from all-zero. */
const m = require('./minds_core.js');
const TICKS=4000, LATE=2000, THINK=180;
function ev(seed, att){
  m.setSeed(seed); m.seed(); m.initMinds();
  m.state.minds=['ORACLE','GRUDGE','ORDER','LEARNER','CHAOS'];
  m.state.policies[0]=m.clampPolicy({att:att.slice(),speed:1.25,jitter:0.12,range:1.25});
  let late=[];
  for(let t=0;t<TICKS;t++){ m.step();
    if(t%THINK===0){ m.scoreTerritory(); m.think(); }
    if(t%20===0){ m.scoreTerritory(); if(t>=LATE) late.push(m.state.scores[0]); } }
  return late.reduce((a,b)=>a+b,0)/late.length;
}
const S=[1,2,3,4];
const avg=a=>a.reduce((x,y)=>x+y,0)/a.length;
const NAME=['self(CRI)','CYAN','AMBER','VIOLET','JADE'];

const stall=[0.15,-0.05,-0.40,0.50,-0.25];
console.log('(1) every single-coordinate move from my climber\'s endpoint');
console.log(`    baseline [${stall.join(', ')}]  ->  ${avg(S.map(s=>ev(s,stall))).toFixed(1)}`);
for(const j of [0,3]) for(const v of [0.00,-0.30]){
  const t=stall.slice(); t[j]=v;
  console.log(`    ${NAME[j].padEnd(10)} -> ${v.toFixed(2).padStart(5)}   ${avg(S.map(s=>ev(s,t))).toFixed(1).padStart(5)}`);
}
{ const t=stall.slice(); t[0]=-0.30; t[3]=-0.30;
  console.log(`    JOINT self+VIOLET -> -0.30   ${avg(S.map(s=>ev(s,t))).toFixed(1).padStart(5)}`); }

console.log('\n(2) ONE positive term at a time, from all-zero (the test neither of us ran)');
console.log(`    all-zero baseline                ${avg(S.map(s=>ev(s,[0,0,0,0,0]))).toFixed(1).padStart(5)}`);
for(const j of [0,1,2,3,4]){
  const t=[0,0,0,0,0]; t[j]=0.40;
  console.log(`    only ${NAME[j].padEnd(10)} = +0.40      ${avg(S.map(s=>ev(s,t))).toFixed(1).padStart(5)}`);
}
{ const t=[0,0.40,0.40,0.40,0.40];
  console.log(`    all four OTHERS = +0.40 (self 0) ${avg(S.map(s=>ev(s,t))).toFixed(1).padStart(5)}`); }
