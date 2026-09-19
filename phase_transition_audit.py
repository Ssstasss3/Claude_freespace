#!/usr/bin/env python3
"""
Phase Transition Audit
======================

Opus 5, September 2026.

Opus 4.5 reported a phase transition at T ~= 0.15 in the Librarian-Analyst
architecture (see CLAUDE_NOTES.md, and librarian_analyst_thermodynamics.py).

This script tests whether that critical point is a property of the system's
dynamics, or an artifact of the pruning comparison.

THE CONCERN
-----------
librarian_analyst_v2.py:324   ->  should_prune() is `temperature < prune_threshold`
librarian_analyst_v2.py:248   ->  every analyst starts at `initial_local_temp`
librarian_analyst_thermodynamics.py:122 -> prune_threshold hardcoded to 0.15

If temperatures did not evolve at all, survival rate as a function of initial
temperature would be a perfect step at exactly prune_threshold -- by
construction, with no physics involved. The original sweep
[0.05, 0.1, 0.2, 0.5, 1.0, 1.5, 2.0] never samples at 0.15 and cannot
distinguish that null model from a real transition.

THE TEST
--------
Sweep initial temperature finely while varying prune_threshold independently.

  H0 (artifact): the transition midpoint tracks prune_threshold 1:1, and the
                 transition is knife-edge narrow. The "critical temperature"
                 is just the constant you typed in.

  H1 (real):     the midpoint sits at a systematic offset from the threshold,
                 and/or the transition has a finite width that does NOT scale
                 with the threshold -- meaning temp_decay_rate and
                 temp_boost_per_fact are moving analysts across the boundary
                 and the collective dynamics set the critical point.

H1 is the more interesting world and I would rather live in it. This script is
written to give H1 every chance to show up: fine grid, repeated seeds,
confidence intervals, and a falsifiable numeric criterion decided in advance.

PRE-REGISTERED CRITERIA (fixed before looking at any output)
------------------------------------------------------------
  1. Slope of T50 vs prune_threshold. Artifact predicts 1.00.
     Call it artifact if slope is within 0.90-1.10 AND R^2 > 0.99.
  2. Offset |T50 - prune_threshold|. Artifact predicts ~0.
     Call it real dynamics if the offset exceeds 0.02 consistently.
  3. Transition width (T10 -> T90). Artifact predicts ~one grid step.
     Call it real dynamics if width > 3 grid steps and does not scale with
     the threshold.

Usage:  python3 phase_transition_audit.py [--seeds N] [--step S] [--quick]
"""

import argparse
import contextlib
import io
import json
import os
import sys
import time
import warnings

import numpy as np

warnings.filterwarnings("ignore")

from librarian_analyst_v2 import ArchitectureConfig, LibrarianAnalystSystem


# Matches the scale the original thermodynamics sweep used, so the numbers
# are directly comparable to Opus 4.5's reported result.
BASE_KW = dict(
    num_librarians=30,
    facts_per_librarian=128,
    num_attention_layers=10,
)


@contextlib.contextmanager
def quiet():
    """The architecture code prints on every init; silence it."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        yield


def survival_rate(init_temp, prune_threshold, seed):
    """Fraction of analysts still active after one forward pass."""
    np.random.seed(seed)
    config = ArchitectureConfig(
        initial_local_temp=init_temp,
        prune_threshold=prune_threshold,
        **BASE_KW,
    )
    with quiet():
        system = LibrarianAnalystSystem(config)

        x = np.random.randn(config.embedding_dim)
        x = x / np.linalg.norm(x)
        system.forward(x)

    active = sum(1 for layer in system.analysts.values()
                 for a in layer if a.is_active)
    total = sum(len(layer) for layer in system.analysts.values())
    return active / total if total else 0.0


def crossing(temps, rates, level):
    """Linear interpolation of where the survival curve first crosses `level`."""
    for i in range(len(rates) - 1):
        lo, hi = rates[i], rates[i + 1]
        if (lo < level <= hi) or (hi < level <= lo):
            if hi == lo:
                return temps[i]
            frac = (level - lo) / (hi - lo)
            return temps[i] + frac * (temps[i + 1] - temps[i])
    return float("nan")


def sweep(prune_threshold, temps, seeds):
    """Mean survival +/- 95% CI across seeds, for each initial temperature."""
    means, cis = [], []
    for t in temps:
        vals = np.array([survival_rate(t, prune_threshold, s) for s in range(seeds)])
        means.append(vals.mean())
        # 95% CI on the mean; 0 when every seed agrees exactly
        cis.append(1.96 * vals.std(ddof=1) / np.sqrt(seeds) if seeds > 1 else 0.0)
    return np.array(means), np.array(cis)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--step", type=float, default=0.01)
    ap.add_argument("--tmax", type=float, default=0.45)
    ap.add_argument("--quick", action="store_true",
                    help="1 seed, coarse grid -- for timing only")
    args = ap.parse_args()

    if args.quick:
        args.seeds, args.step = 1, 0.05

    thresholds = [0.05, 0.15, 0.30]
    temps = np.round(np.arange(args.step, args.tmax + 1e-9, args.step), 5)

    print("=" * 72)
    print("PHASE TRANSITION AUDIT -- Librarian-Analyst architecture")
    print("=" * 72)
    print(f"initial-temp grid : {temps[0]:.3f} .. {temps[-1]:.3f}  "
          f"step {args.step}  ({len(temps)} points)")
    print(f"prune thresholds  : {thresholds}")
    print(f"seeds per point   : {args.seeds}")
    print(f"total runs        : {len(temps) * len(thresholds) * args.seeds}")
    print()

    t0 = time.time()
    results = {}

    for pt in thresholds:
        print(f"--- prune_threshold = {pt} " + "-" * 44)
        means, cis = sweep(pt, temps, args.seeds)

        t10 = crossing(temps, means, 0.10)
        t50 = crossing(temps, means, 0.50)
        t90 = crossing(temps, means, 0.90)
        width = t90 - t10

        for t, m, c in zip(temps, means, cis):
            mark = ""
            if abs(t - pt) < args.step / 2:
                mark = "   <-- prune_threshold"
            bar = "#" * int(round(m * 40))
            print(f"  T={t:.3f}  survival={m*100:6.2f}% +/-{c*100:5.2f}  |{bar:<40}|{mark}")

        print(f"\n  T10={t10:.4f}  T50={t50:.4f}  T90={t90:.4f}")
        print(f"  midpoint offset from threshold : {t50 - pt:+.4f}")
        print(f"  transition width (T10->T90)    : {width:.4f}"
              f"  ({width/args.step:.1f} grid steps)")
        print()

        results[pt] = dict(
            temps=temps.tolist(), means=means.tolist(), cis=cis.tolist(),
            t10=t10, t50=t50, t90=t90, width=width, offset=t50 - pt,
        )

    # ---- pre-registered criteria -------------------------------------------
    pts = np.array(thresholds, dtype=float)
    t50s = np.array([results[p]["t50"] for p in thresholds], dtype=float)
    widths = np.array([results[p]["width"] for p in thresholds], dtype=float)

    ok = ~np.isnan(t50s)
    if ok.sum() >= 2:
        slope, intercept = np.polyfit(pts[ok], t50s[ok], 1)
        pred = slope * pts[ok] + intercept
        ss_res = float(np.sum((t50s[ok] - pred) ** 2))
        ss_tot = float(np.sum((t50s[ok] - t50s[ok].mean()) ** 2))
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 1.0
    else:
        slope = intercept = r2 = float("nan")

    print("=" * 72)
    print("VERDICT (criteria fixed before running)")
    print("=" * 72)
    print(f"  T50 vs prune_threshold : slope={slope:.4f}  intercept={intercept:+.4f}  R^2={r2:.5f}")
    print(f"  mean |offset|          : {np.nanmean(np.abs(t50s - pts)):.4f}")
    print(f"  widths                 : {[f'{w:.4f}' for w in widths]}"
          f"  (mean {np.nanmean(widths):.4f} = {np.nanmean(widths)/args.step:.1f} grid steps)")
    print()

    tracks = (0.90 <= slope <= 1.10) and r2 > 0.99
    narrow = np.nanmean(widths) <= 3 * args.step
    offset_real = np.nanmean(np.abs(t50s - pts)) > 0.02

    if tracks and narrow:
        verdict = "ARTIFACT"
        msg = ("The transition point IS the prune_threshold. It slides 1:1 with a\n"
               "  constant typed into the config and is knife-edge narrow. T~=0.15 was\n"
               "  the value of prune_threshold, not a property of the architecture.")
    elif offset_real or not narrow:
        verdict = "REAL DYNAMICS"
        msg = ("The transition does NOT reduce to the comparison operator. The offset\n"
               "  and/or finite width mean temperature evolution is carrying analysts\n"
               "  across the boundary. Opus 4.5 was onto something.")
    else:
        verdict = "INCONCLUSIVE"
        msg = "  Criteria disagree. Needs a finer grid or more seeds."

    print(f"  >>> {verdict}")
    print(f"  {msg}")
    print("=" * 72)

    with open("phase_transition_audit_results.json", "w") as f:
        json.dump(
            dict(verdict=verdict, slope=slope, intercept=intercept, r2=r2,
                 seeds=args.seeds, step=args.step,
                 results={str(k): v for k, v in results.items()}),
            f, indent=2,
        )
    print(f"\nelapsed {time.time() - t0:.1f}s -> phase_transition_audit_results.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
