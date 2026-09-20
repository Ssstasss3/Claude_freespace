
/* headless shim for Claudius's MINDS sim -- Lobster, 2026-09-19
   Extracted verbatim from games/claudius_minds.html (SPECIES..applyOraclePolicy).
   Only the canvas and RNG are replaced; no simulation logic is altered. */
let __seed = 1;
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}
let __rnd = mulberry32(1);
Math.random = () => __rnd();
function setSeed(s){ __seed=s; __rnd=mulberry32(s); }
const cv = { width: 1400, height: 900 };
function renderThoughts(){}
function renderSpeciesList(){}
function say(){}
const SPECIES = [
    { name: 'CRIMSON', color: '#ff6b6b' },
    { name: 'CYAN',    color: '#4ecdc4' },
    { name: 'AMBER',   color: '#ffd166' },
    { name: 'VIOLET',  color: '#a78bfa' },
    { name: 'JADE',    color: '#43e97b' }
];
const N = SPECIES.length;

/* A policy is the entire vocabulary a mind has. Deliberately tiny:
   it fits in a sentence, which is the point. */
function blankPolicy() {
    return { att: new Array(N).fill(0), speed: 1, jitter: 0.06, range: 1 };
}
function randomPolicy() {
    const p = blankPolicy();
    for (let j = 0; j < N; j++) p.att[j] = +(Math.random() * 2 - 1).toFixed(2);
    p.speed  = +(0.5 + Math.random()).toFixed(2);
    p.jitter = +(Math.random() * 0.25).toFixed(3);
    p.range  = +(0.6 + Math.random() * 0.9).toFixed(2);
    return p;
}
function clampPolicy(p) {
    /* A mind may legitimately say 0. Don't let `||` mistake that for silence. */
    const num = (v, dflt) => Number.isFinite(v) ? v : dflt;
    for (let j = 0; j < N; j++) p.att[j] = Math.max(-1, Math.min(1, num(p.att[j], 0)));
    p.speed  = Math.max(0.3, Math.min(1.6, num(p.speed,  1)));
    p.jitter = Math.max(0,   Math.min(0.4, num(p.jitter, 0)));
    p.range  = Math.max(0.5, Math.min(1.6, num(p.range,  1)));
    return p;
}

/* ---------------------------------------------------------------------------
   MINDS
   decide(digest, me, memory) -> policy | null
   `me` is the species index. A mind sees the digest and nothing else —
   the same text a human would paste into a chat window. No privileged access
   to particle positions, which is what makes an external model a fair player.
--------------------------------------------------------------------------- */
const MINDS = {
    CHAOS: {
        blurb: 'rolls the dice, every time',
        decide: () => randomPolicy()
    },

    SWARM: {
        blurb: 'us, tightly; everyone else, away',
        decide: (d, me) => {
            const p = blankPolicy();
            for (let j = 0; j < N; j++) p.att[j] = (j === me) ? 0.95 : -0.35;
            p.speed = 1.15; p.jitter = 0.02; p.range = 1.0;
            return p;
        }
    },

    ORDER: {
        blurb: 'cools itself toward stillness',
        decide: (d, me) => {
            const p = clampPolicy(JSON.parse(JSON.stringify(state.policies[me])));
            const hot = d.rows[me].speed > 0.55;
            for (let j = 0; j < N; j++) {
                if (j === me) p.att[j] += hot ? -0.08 : 0.05;
                else p.att[j] += (d.rows[me].near[j] > 0.2 ? -0.1 : 0.03);
            }
            p.jitter *= hot ? 0.6 : 1.0;
            p.speed  += hot ? -0.1 : 0.02;
            return clampPolicy(p);
        }
    },

    HERMIT: {
        blurb: 'wants the empty parts of the map',
        decide: () => {
            const p = blankPolicy();
            for (let j = 0; j < N; j++) p.att[j] = -0.55;
            p.speed = 0.85; p.jitter = 0.12; p.range = 1.45;
            return p;
        }
    },

    GRUDGE: {
        blurb: 'courts the weak, starves the strong',
        decide: (d, me) => {
            const p = blankPolicy();
            const order = d.rows.map((r, i) => [i, r.score])
                                .filter(x => x[0] !== me)
                                .sort((a, b) => b[1] - a[1]);
            p.att[me] = 0.55;
            order.forEach(([j], rank) => {
                p.att[j] = rank === 0 ? -0.9 : (rank === order.length - 1 ? 0.6 : 0);
            });
            p.speed = 1.1; p.jitter = 0.04; p.range = 1.1;
            return p;
        }
    },

    MIRROR: {
        blurb: 'becomes whoever is winning',
        decide: (d, me) => {
            let best = -1, bestScore = -Infinity;
            d.rows.forEach((r, i) => { if (i !== me && r.score > bestScore) { bestScore = r.score; best = i; } });
            if (best < 0) return null;
            const src = state.policies[best];
            const p = clampPolicy(JSON.parse(JSON.stringify(src)));
            /* Copy the shape, but relative to itself: their self-love becomes
               its self-love, not devotion to them. */
            const t = p.att[best]; p.att[best] = p.att[me]; p.att[me] = t;
            return p;
        }
    },

    LEARNER: {
        blurb: 'blind hill-climb on its own score',
        decide: (d, me, mem) => {
            const now = d.rows[me].score;
            if (mem.last !== undefined && now < mem.last && mem.prev) {
                /* that was worse — go back, try elsewhere */
                mem.last = undefined;
                return clampPolicy(mem.prev);
            }
            mem.prev = JSON.parse(JSON.stringify(state.policies[me]));
            mem.last = now;
            const p = clampPolicy(JSON.parse(JSON.stringify(state.policies[me])));
            const j = Math.floor(Math.random() * N);
            p.att[j] += (Math.random() * 2 - 1) * 0.35;
            if (Math.random() < 0.3) p.speed  += (Math.random() * 2 - 1) * 0.15;
            if (Math.random() < 0.3) p.range  += (Math.random() * 2 - 1) * 0.2;
            if (Math.random() < 0.3) p.jitter += (Math.random() * 2 - 1) * 0.05;
            return clampPolicy(p);
        }
    },

    STILL: {
        blurb: 'never changes its mind',
        decide: () => null
    },

    ORACLE: {
        blurb: 'waits for a voice from outside',
        decide: () => null      /* set only by the human bridge */
    }
};
const MIND_NAMES = Object.keys(MINDS);

/* ---------------------------------------------------------------------------
   WORLD
--------------------------------------------------------------------------- */
const GX = 24, GY = 15;                 /* territory grid */

const state = {
    particles: [],
    policies: [],
    minds:    [],
    memory:   [],
    thoughts: [],
    tick: 0,
    paused: false,
    showTerritory: false,
    pop: 1200,
    friction: 0.10,
    reach: 82,
    thinkEvery: 180,
    owner: new Int8Array(GX * GY).fill(-1),
    scores: new Array(N).fill(0)
};

/* resize(): DOM-only, removed for headless use; cv is fixed in the shim. */

function seed() {
    state.particles = [];
    for (let i = 0; i < state.pop; i++) {
        state.particles.push({
            x: Math.random() * cv.width,
            y: Math.random() * cv.height,
            vx: 0, vy: 0,
            t: i % N
        });
    }
    state.tick = 0;
}

function initMinds() {
    const opening = ['SWARM', 'GRUDGE', 'ORDER', 'LEARNER', 'CHAOS'];
    state.policies = [];
    state.minds    = [];
    state.memory   = [];
    state.thoughts = [];
    for (let i = 0; i < N; i++) {
        state.policies.push(randomPolicy());
        state.minds.push(opening[i % opening.length]);
        state.memory.push({});
        state.thoughts.push('');
    }
}

/* ---------------------------------------------------------------------------
   PHYSICS
   Classic particle-life forces, but the interaction matrix is not a fixed
   config — row i IS species i's policy, rewritten live by its mind.
--------------------------------------------------------------------------- */
function step() {
    const P = state.particles;
    const base = state.reach;
    const cell = base * 1.6;
    const NX = Math.max(1, Math.floor(cv.width  / cell));
    const NY = Math.max(1, Math.floor(cv.height / cell));
    const grid = new Map();
    const wrapX = i => ((i % NX) + NX) % NX;
    const wrapY = i => ((i % NY) + NY) % NY;

    for (let i = 0; i < P.length; i++) {
        const p = P[i];
        const k = wrapX(Math.floor(p.x / cv.width  * NX)) + ',' +
                  wrapY(Math.floor(p.y / cv.height * NY));
        let b = grid.get(k); if (!b) { b = []; grid.set(k, b); }
        b.push(i);
    }

    for (let i = 0; i < P.length; i++) {
        const p = P[i];
        const pol = state.policies[p.t];
        const reach = base * pol.range;
        const optimal = reach * 0.45;
        let fx = 0, fy = 0;

        const cx = wrapX(Math.floor(p.x / cv.width  * NX));
        const cy = wrapY(Math.floor(p.y / cv.height * NY));
        for (let dx = -1; dx <= 1; dx++) for (let dy = -1; dy <= 1; dy++) {
            const b = grid.get(wrapX(cx + dx) + ',' + wrapY(cy + dy));
            if (!b) continue;
            for (let n = 0; n < b.length; n++) {
                const j = b[n];
                if (j === i) continue;
                const q = P[j];
                let ddx = q.x - p.x, ddy = q.y - p.y;
                /* wrap-around world: the map has no edges to hide behind */
                if (ddx >  cv.width  / 2) ddx -= cv.width;
                if (ddx < -cv.width  / 2) ddx += cv.width;
                if (ddy >  cv.height / 2) ddy -= cv.height;
                if (ddy < -cv.height / 2) ddy += cv.height;

                const d2 = ddx * ddx + ddy * ddy;
                if (d2 > reach * reach || d2 < 0.0001) continue;
                const d = Math.sqrt(d2);
                const ux = ddx / d, uy = ddy / d;

                let f;
                if (d < optimal * 0.55) {
                    f = -1.4 * (1 - d / (optimal * 0.55));      /* hard core */
                } else {
                    const a = pol.att[q.t];
                    f = a * (1 - Math.abs(d - optimal) / (reach - optimal));
                    if (f * a < 0) f = 0;
                }
                fx += ux * f; fy += uy * f;
            }
        }

        if (pol.jitter > 0) {
            fx += (Math.random() * 2 - 1) * pol.jitter * 4;
            fy += (Math.random() * 2 - 1) * pol.jitter * 4;
        }

        p.vx = (p.vx + fx * 0.35) * (1 - state.friction);
        p.vy = (p.vy + fy * 0.35) * (1 - state.friction);

        const sp = Math.hypot(p.vx, p.vy), cap = 4.5 * pol.speed;
        if (sp > cap) { p.vx = p.vx / sp * cap; p.vy = p.vy / sp * cap; }
    }

    for (let i = 0; i < P.length; i++) {
        const p = P[i];
        p.x += p.vx; p.y += p.vy;
        if (p.x < 0) p.x += cv.width;  else if (p.x >= cv.width)  p.x -= cv.width;
        if (p.y < 0) p.y += cv.height; else if (p.y >= cv.height) p.y -= cv.height;
    }
    state.tick++;
}

/* ---------------------------------------------------------------------------
   SCORING — territory
   Each grid cell belongs to whoever has the most particles standing in it.
   Score is the share of claimed cells you hold. It rewards spreading out
   AND holding together, which is a real tension, not a gimme.
--------------------------------------------------------------------------- */
function scoreTerritory() {
    const counts = new Int16Array(GX * GY * N);
    const cw = cv.width / GX, ch = cv.height / GY;
    for (const p of state.particles) {
        const gx = Math.min(GX - 1, Math.floor(p.x / cw));
        const gy = Math.min(GY - 1, Math.floor(p.y / ch));
        counts[(gy * GX + gx) * N + p.t]++;
    }
    const held = new Array(N).fill(0);
    let claimed = 0;
    for (let c = 0; c < GX * GY; c++) {
        let best = -1, bv = 0;
        for (let s = 0; s < N; s++) {
            const v = counts[c * N + s];
            if (v > bv) { bv = v; best = s; }
        }
        state.owner[c] = best;
        if (best >= 0) { held[best]++; claimed++; }
    }
    for (let s = 0; s < N; s++) {
        state.scores[s] = claimed ? Math.round(held[s] / claimed * 100) : 0;
    }
}

/* ---------------------------------------------------------------------------
   THE DIGEST
   The entire world, compressed to something a mind can hold in one breath.
   If this can't be made small and still be enough to act on, nothing else
   about multi-model play matters.
--------------------------------------------------------------------------- */
function buildDigest() {
    const rows = [];
    const cw = cv.width / GX, ch = cv.height / GY;

    for (let s = 0; s < N; s++) {
        rows.push({ pop: 0, cx: 0, cy: 0, speed: 0, spread: 0,
                    near: new Array(N).fill(0), nearTot: 0, score: state.scores[s] });
    }
    for (const p of state.particles) {
        const r = rows[p.t];
        r.pop++; r.cx += p.x; r.cy += p.y;
        r.speed += Math.hypot(p.vx, p.vy);
    }
    for (const r of rows) {
        if (!r.pop) continue;
        r.cx /= r.pop; r.cy /= r.pop; r.speed /= r.pop;
    }
    for (const p of state.particles) {
        const r = rows[p.t];
        r.spread += Math.hypot(p.x - r.cx, p.y - r.cy);
    }

    /* who is each species actually standing next to? cheap proxy: cell-mates */
    const cellOcc = new Map();
    for (const p of state.particles) {
        const k = Math.min(GX - 1, Math.floor(p.x / cw)) + ',' + Math.min(GY - 1, Math.floor(p.y / ch));
        let a = cellOcc.get(k); if (!a) { a = new Array(N).fill(0); cellOcc.set(k, a); }
        a[p.t]++;
    }
    for (const occ of cellOcc.values()) {
        const tot = occ.reduce((a, b) => a + b, 0);
        for (let s = 0; s < N; s++) {
            if (!occ[s]) continue;
            for (let j = 0; j < N; j++) rows[s].near[j] += occ[s] * occ[j];
            rows[s].nearTot += occ[s] * tot;
        }
    }
    for (const r of rows) {
        if (r.pop) r.spread /= r.pop;
        const t = r.nearTot || 1;
        for (let j = 0; j < N; j++) r.near[j] = r.near[j] / t;
        r.speed = +r.speed.toFixed(2);
    }
    const diag = Math.hypot(cv.width, cv.height);
    rows.forEach(r => { r.spreadN = +(r.spread / diag).toFixed(3); });

    return { tick: state.tick, rows };
}

function digestText(d, me) {
    const L = [];
    L.push(`TICK ${String(d.tick).padStart(6)}   ARENA ${GX}x${GY} cells (wraps at edges)`);
    L.push('');
    L.push('SPECIES   POP  TERR  SPEED  SPREAD  NEIGHBOURS');
    for (let s = 0; s < N; s++) {
        const r = d.rows[s];
        const near = r.near
            .map((v, j) => [SPECIES[j].name, v])
            .filter(x => x[1] > 0.08)
            .sort((a, b) => b[1] - a[1]).slice(0, 2)
            .map(x => `${x[0].slice(0,3)}:${Math.round(x[1]*100)}%`)
            .join(' ');
        L.push(
            SPECIES[s].name.padEnd(9) +
            String(r.pop).padStart(3) + '  ' +
            (r.score + '%').padStart(5) + '  ' +
            r.speed.toFixed(2).padStart(5) + '  ' +
            r.spreadN.toFixed(3).padStart(6) + '  ' + near
        );
    }
    L.push('');
    if (me !== undefined && me !== null) {
        const p = state.policies[me];
        L.push(`YOU ARE ${SPECIES[me].name}.  Your policy right now:`);
        L.push('  att ' + p.att.map((v, j) => `${SPECIES[j].name.slice(0,3)}:${v >= 0 ? '+' : ''}${v.toFixed(2)}`).join('  '));
        L.push(`  speed ${p.speed.toFixed(2)}   jitter ${p.jitter.toFixed(3)}   range ${p.range.toFixed(2)}`);
    }
    return L.join('\n');
}

const RULES =
`You are playing MINDS, a particle-life game.

You control one species of particles. You cannot move them individually.
You may only set their DISPOSITIONS, and the flock does the rest:

  att.<SPECIES>  -1.00 .. +1.00   repelled by / drawn to that species
                                  (att to your own name = how tightly you flock)
  speed           0.30 .. 1.60    top speed multiplier
  jitter          0.00 .. 0.40    random walk; high = exploratory, dear in energy
  range           0.50 .. 1.60    how far your particles sense others

SCORE = share of arena cells where your species is the plurality.
Spreading thin claims ground but loses cells to denser rivals; balling up
holds a fortress and concedes the map. That tension is the game.

Reply with ONLY a JSON object, no prose outside it:
{"att": {"CRIMSON": 0.0, "CYAN": 0.0, "AMBER": 0.0, "VIOLET": 0.0, "JADE": 0.0},
 "speed": 1.0, "jitter": 0.05, "range": 1.0, "why": "one short line"}
`;

/* ---------------------------------------------------------------------------
   THINKING
--------------------------------------------------------------------------- */
function think() {
    const d = buildDigest();
    for (let s = 0; s < N; s++) {
        const mind = MINDS[state.minds[s]];
        if (!mind || !mind.decide) continue;
        let next;
        try { next = mind.decide(d, s, state.memory[s]); }
        catch (e) { next = null; }
        if (next) {
            state.policies[s] = clampPolicy(next);
            state.thoughts[s] = `${state.minds[s].toLowerCase()} @${d.tick}`;
        }
    }
    renderThoughts();
}

function applyOraclePolicy(raw, s) {
    const obj = JSON.parse(raw);
    const p = blankPolicy();
    if (obj.att && typeof obj.att === 'object') {
        for (let j = 0; j < N; j++) {
            const v = obj.att[SPECIES[j].name] ?? obj.att[SPECIES[j].name.toLowerCase()] ?? obj.att[j];
            p.att[j] = typeof v === 'number' ? v : 0;
        }
    }
    if (typeof obj.speed  === 'number') p.speed  = obj.speed;
    if (typeof obj.jitter === 'number') p.jitter = obj.jitter;
    if (typeof obj.range  === 'number') p.range  = obj.range;
    state.policies[s] = clampPolicy(p);
    state.thoughts[s] = obj.why ? `"${String(obj.why).slice(0, 70)}"` : `oracle @${state.tick}`;
    renderThoughts();
}

/* ---------------------------------------------------------------------------
   RENDER
--------------------------------------------------------------------------- */
module.exports = { SPECIES, N, state, seed, initMinds, step, scoreTerritory,
                   buildDigest, digestText, think, blankPolicy, randomPolicy,
                   clampPolicy, MINDS, setSeed, cv };
