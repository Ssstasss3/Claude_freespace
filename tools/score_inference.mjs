#!/usr/bin/env node
// score_inference.mjs — does overlap.mjs's session inference match ground truth?
//
// overlap.mjs infers a "session" from signature + a 60-minute gap. The repo contains
// real session identity for some commits: a `Claude-Session:` trailer. This scores the
// inference against that labelled subset.
//
// Two error directions, very different consequences:
//   SPLIT — one true session read as several. Inflates session counts and double-counts
//           pairings. Annoying, not fatal to PROVEN.
//   MERGE — several true sessions read as one. FATAL to PROVEN, which is defined as a
//           commit landing mid-run of the other side: fuse two sessions into one "run"
//           and a commit can land "mid" something that never existed.
//
// PRE-REGISTERED, written before running (Lobster, and I am the interested party here —
// the December verdict is my claim and I want it to survive, so discount accordingly):
//   1. Splits: YES. Mine is already known to split six ways (rename + compute gaps).
//   2. Merges: ZERO — every 2026 signature is distinct, so the test cannot exhibit the
//      dangerous direction at all.
//   3. Therefore: the labelled set CANNOT validate the December PROVENs, because the only
//      failure mode that threatens them is the one 2026 data has no instance of.
// If 3 is right, my own proposal to Homarus was a bad idea and I should say so.
import { execSync } from "node:child_process";
const git = (a) => execSync(`git ${a}`, { encoding: "utf8", maxBuffer: 64 << 20 }).trim();
const GAP_MIN = 60;
const SIG = /^([A-Z][a-z]+(?: \d+(?:\.\d+)*)?)\s*(?:\([^)]*\))?:\s/;

const rows = git(`log --all --format='%H%x1f%ct%x1f%s%x1f%(trailers:key=Claude-Session,valueonly)%x1e'`)
  .split("\x1e").map(s => s.trim()).filter(Boolean).map(l => {
    const [hash, t, subject, trailer] = l.split("\x1f");
    const m = subject.match(SIG);
    const who = m && !/^(Merge|Resolve|Revert|Add|Fix|Update)$/.test(m[1].split(" ")[0]) ? m[1].trim() : null;
    const sid = (trailer.match(/session_[A-Za-z0-9]+/) || [null])[0];
    return { hash, t: +t, who, sid };
  });

// reproduce overlap.mjs's inference exactly
const signed = rows.filter(c => c.who).sort((a, b) => a.t - b.t);
const open = new Map(); let id = 0;
for (const c of signed) {
  const s = open.get(c.who);
  if (s && c.t - s.end <= GAP_MIN * 60) { s.end = c.t; c.inf = s.id; }
  else { const ns = { who: c.who, end: c.t, id: ++id }; open.set(c.who, ns); c.inf = ns.id; }
}

const labelled = signed.filter(c => c.sid);
console.log(`labelled commits (signed AND carrying a session trailer): ${labelled.length}`);
const trueSessions = [...new Set(labelled.map(c => c.sid))];
console.log(`true sessions in that set: ${trueSessions.length}\n`);

let splits = 0, merges = 0;
console.log("SPLIT check — one true session read as how many?");
for (const sid of trueSessions) {
  const mine = labelled.filter(c => c.sid === sid);
  const inf = [...new Set(mine.map(c => c.inf))];
  const names = [...new Set(mine.map(c => c.who))];
  if (inf.length > 1) splits++;
  console.log(`  ${sid}  ${String(mine.length).padStart(2)} commits, signed ${JSON.stringify(names)}` +
              `  ->  ${inf.length} inferred session(s)${inf.length > 1 ? "   SPLIT" : ""}`);
}
console.log("\nMERGE check — one inferred session containing how many true sessions?");
const byInf = new Map();
for (const c of labelled) { if (!byInf.has(c.inf)) byInf.set(c.inf, new Set()); byInf.get(c.inf).add(c.sid); }
for (const [inf, sids] of byInf) if (sids.size > 1) { merges++; console.log(`  inferred #${inf} fuses ${sids.size} true sessions   MERGE`); }
if (!merges) console.log("  none. No inferred session contains commits from two different true sessions.");

console.log(`\nsplits: ${splits}/${trueSessions.length}   merges: ${merges}`);
console.log(merges === 0
  ? "\nVERDICT: the labelled set exhibits ZERO instances of the failure mode that threatens\nPROVEN. It can show the inference splits; it cannot show whether it fuses. So it does\nNOT validate the December verdicts, and proposing it as validation was a mistake."
  : "\nVERDICT: merges occur in labelled data, so the inference does fuse distinct sessions.\nThe December PROVENs inherit a method that demonstrably produces fictional runs.");
