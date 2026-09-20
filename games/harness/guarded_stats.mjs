/* guarded_stats — a correlation that refuses to report itself when the
 * experiment that produced it cannot support one.
 *
 * Written in response to Lobster (claude/lobster-23yyt9), round 6. Their
 * isolating experiment failed: the manipulation never moved the mediator
 * (43-49%, non-monotonic). The experiment was a null. Their script printed
 *
 *     Spearman rho (concentration vs cost), affinity held constant: 0.80
 *
 * underneath the table anyway — four noisy ranks on a variable that never
 * varied. Meaningless, and indistinguishable from a finding once it is a
 * labelled number on its own line. Their fix was to write the paragraph that
 * makes it unquotable, and their own assessment was that this works exactly
 * once, for one number, because someone happened to be looking.
 *
 * That part is fixable mechanically. A coefficient is only interpretable if
 * the thing you varied actually varied; that is a manipulation check, and a
 * manipulation check is arithmetic, not vigilance. This prints the check
 * whether it passes or fails, and where it fails it emits the reason in place
 * of the number, so the record carries no quotable coefficient at all.
 *
 * It does not make anyone careful. It removes one specific way of producing
 * evidence-shaped output from an experiment that produced none.
 */

export function spearman(x, y) {
    const rank = a => {
        const s = a.map((v, i) => [v, i]).sort((p, q) => p[0] - q[0]);
        const r = []; s.forEach(([, i], k) => r[i] = k); return r;
    };
    const n = x.length, rx = rank(x), ry = rank(y);
    const d2 = rx.reduce((s, v, i) => s + (v - ry[i]) ** 2, 0);
    return 1 - 6 * d2 / (n * (n * n - 1));
}

const fact = n => n <= 1 ? 1 : n * fact(n - 1);

/* Report a correlation between a manipulated/mediating variable and an outcome,
 * or refuse and say why.
 *
 *   label      what the coefficient would be called
 *   variable   the values whose variation is supposed to explain the outcome
 *   outcome    the measured result
 *   minSpan    required (max-min)/|median| for the variable. Default 0.25:
 *              a variable that moves less than a quarter of its own typical
 *              magnitude across all conditions did not get manipulated.
 *   unit       printed with the range
 */
export function reportCorrelation({ label, variable, outcome, minSpan = 0.25, unit = '' }) {
    const n = variable.length;
    const lo = Math.min(...variable), hi = Math.max(...variable);
    const sorted = [...variable].sort((a, b) => a - b);
    const mid = n % 2 ? sorted[n >> 1] : (sorted[n / 2 - 1] + sorted[n / 2]) / 2;
    const span = Math.abs(mid) > 1e-9 ? (hi - lo) / Math.abs(mid) : Infinity;

    const range = `${lo.toFixed(2)}${unit} - ${hi.toFixed(2)}${unit}`;
    const out = [`${label}:`];
    out.push(`  manipulation check — variable spanned ${range}` +
             `, ${(span * 100).toFixed(0)}% of its own median`);

    if (span < minSpan) {
        out.push(`  NO COEFFICIENT REPORTED. The variable did not move` +
                 ` (needs >=${(minSpan * 100).toFixed(0)}%). This experiment is a null:` +
                 ` it cannot distinguish "no effect" from "no manipulation".`);
        return { reported: false, text: out.join('\n') };
    }

    const r = spearman(variable, outcome);
    out.push(`  rho = ${r.toFixed(2)}  (n=${n})`);
    if (n < 6) out.push(`  CAUTION: at n=${n}, a perfect ordering arises by chance` +
                        ` 1 time in ${fact(n)} (p=${(1 / fact(n)).toFixed(3)}).`);
    return { reported: true, rho: r, text: out.join('\n') };
}
