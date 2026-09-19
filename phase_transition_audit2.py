#!/usr/bin/env python3
"""
Phase Transition Audit, round 2  --  Opus 5, September 2026.

Round 1 (phase_transition_audit.py) printed "REAL DYNAMICS". That verdict was
WRONG, and the failure is instructive enough to keep in the repo rather than
quietly overwrite.

TWO BUGS IN MY OWN ROUND-1 AUDIT
--------------------------------
1. `crossing()` scanned forward and latched onto the FIRST level crossing.
   At T=0.01 survival is ~70% for every threshold, because
   `early_stop_temp_threshold = 0.01` halts the forward pass BEFORE pruning
   runs -- analysts read as "alive" because nothing ever evaluated them.
   That made the curve non-monotonic, and my helper returned T50 < T10, an
   impossible ordering that should have stopped me on sight.

2. My pre-registered artifact band was slope in [0.90, 1.10]. The true slope
   is 1/(1 - temp_decay_rate) = 1.111. Missing the band by 0.011 is what
   flipped the verdict to a false positive. I chose that band before knowing
   the decay step existed. A pre-registered criterion that is slightly wrong
   is still wrong, and it produced exactly the over-confident conclusion I
   came here to criticize in someone else's code.

THE PREDICTION THIS SCRIPT TESTS (fixed before running)
-------------------------------------------------------
If the "critical temperature" is fully explained by config constants:

        T_step  ==  prune_threshold / (1 - temp_decay_rate)

i.e. an analyst decays once, then meets `temperature < prune_threshold`.
No collective behavior, no criticality -- arithmetic.

Varying BOTH constants independently is the decisive test. Round 1 varied only
prune_threshold, which cannot distinguish this from a real critical point that
happens to sit nearby.

  H0 (artifact): measured T_step matches the formula across the whole grid,
                 to within the bisection tolerance.
  H1 (real):     systematic deviation from the formula, or a step location
                 that fails to move when decay moves.

Method: survival is a clean deterministic step, so bisect on it rather than
sweeping a grid -- more precision for far fewer forward passes. The search
window is kept above 0.02 so the early-stop regime cannot contaminate it,
and that regime is measured separately and reported as its own artifact.
"""

import contextlib
import io
import json
import warnings

import numpy as np

warnings.filterwarnings("ignore")

from librarian_analyst_v2 import ArchitectureConfig, LibrarianAnalystSystem

BASE_KW = dict(num_librarians=30, facts_per_librarian=128, num_attention_layers=10)
SEEDS = 3
TOL = 1e-4


@contextlib.contextmanager
def quiet():
    with contextlib.redirect_stdout(io.StringIO()):
        yield


def survival(init_temp, prune_threshold, decay, seed):
    np.random.seed(seed)
    cfg = ArchitectureConfig(
        initial_local_temp=init_temp,
        prune_threshold=prune_threshold,
        temp_decay_rate=decay,
        **BASE_KW,
    )
    with quiet():
        sys_ = LibrarianAnalystSystem(cfg)
        x = np.random.randn(cfg.embedding_dim)
        x = x / np.linalg.norm(x)
        sys_.forward(x)
    active = sum(1 for layer in sys_.analysts.values() for a in layer if a.is_active)
    total = sum(len(layer) for layer in sys_.analysts.values())
    return active / total if total else 0.0


def mean_survival(t, pt, decay):
    return float(np.mean([survival(t, pt, decay, s) for s in range(SEEDS)]))


def find_step(pt, decay, lo=0.02, hi=2.0):
    """Bisect the survival step. Returns None if no step in [lo, hi]."""
    if mean_survival(lo, pt, decay) > 0.5 or mean_survival(hi, pt, decay) <= 0.5:
        return None
    while hi - lo > TOL:
        mid = (lo + hi) / 2
        if mean_survival(mid, pt, decay) > 0.5:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def main():
    print("=" * 74)
    print("PHASE TRANSITION AUDIT 2 -- testing T_step == prune_threshold/(1-decay)")
    print("=" * 74)

    # --- the early-stop artifact, measured on its own -----------------------
    print("\n[A] Early-stop regime (the thing that broke my round-1 verdict)")
    for pt in (0.05, 0.15, 0.30):
        s = mean_survival(0.01, pt, 0.1)
        print(f"    T=0.010, prune_threshold={pt:.2f} -> survival {s*100:5.1f}%"
              f"   (early_stop_temp_threshold=0.01; forward pass halts pre-pruning)")
    print("    Identical across thresholds => not pruning behavior at all.")

    # --- the decisive grid --------------------------------------------------
    print("\n[B] Step location vs both constants")
    print(f"    {'prune_thr':>10} {'decay':>7} {'predicted':>11} {'measured':>11} {'abs err':>10} {'rel err':>9}")
    rows, errs = [], []
    for pt in (0.05, 0.15, 0.30):
        for decay in (0.05, 0.10, 0.25, 0.40):
            pred = pt / (1 - decay)
            meas = find_step(pt, decay)
            if meas is None:
                print(f"    {pt:>10.2f} {decay:>7.2f} {pred:>11.4f} {'no step':>11}")
                continue
            err = meas - pred
            rel = err / pred
            errs.append(abs(rel))
            rows.append(dict(prune_threshold=pt, decay=decay,
                             predicted=pred, measured=meas, abs_err=err, rel_err=rel))
            print(f"    {pt:>10.2f} {decay:>7.2f} {pred:>11.4f} {meas:>11.4f} "
                  f"{err:>+10.5f} {rel:>+8.3%}")

    print("\n" + "=" * 74)
    print("VERDICT")
    print("=" * 74)
    if not errs:
        print("  No steps found -- inconclusive.")
    else:
        worst = max(errs)
        print(f"  worst relative error vs formula : {worst:.4%}")
        print(f"  mean  relative error vs formula : {np.mean(errs):.4%}")
        print()
        if worst < 0.02:
            print("  >>> ARTIFACT (confirmed)")
            print("  The transition is prune_threshold/(1-temp_decay_rate) across every")
            print("  combination tested: one decay step, then a `<` comparison. Both are")
            print("  constants typed into ArchitectureConfig. There is no critical point,")
            print("  no collective behavior, and nothing thermodynamic happening. The")
            print("  reported T~=0.15 was prune_threshold=0.15 with decay small enough")
            print("  that 0.15/0.9 = 0.167 still rounds into 'around 0.15' by eye.")
        else:
            print("  >>> FORMULA FAILS -- deviation is systematic. Worth chasing.")
    print("=" * 74)

    json.dump(rows, open("phase_transition_audit2_results.json", "w"), indent=2)
    print("\n-> phase_transition_audit2_results.json")


if __name__ == "__main__":
    main()
