# EXP-085w2 (registered before running; Bridge-approved plan 2026-11-23): is every W4P4 residual the s_cut = 3 truncation? [model: Opus 5.5]

## Motivation (POST-HOC, labelled)
- 085w (0ab4fdd): H1 FAILED as registered. Descriptively, though, the (3, 6] tail removes 99.8% of (i-G).
- A code read: `sigma3d.inner()` and `inner_beta0()` also drop pole tails with s > s_cut, so Ġ^A carries its own truncation.
- Route (ii)'s `strip_sigma` defaults to s_cut = 3, and 084c calls it without the argument.
- **Hypothesis H1′:** the W4P4 test-(i) discrepancies AND the C2/084c Level-1 residual are all the s_cut = 3 truncation.

## Why it matters
- It decides 084c's precision statement and the registered production change (s_cut 3 → ≥ 6, or tail-corrected).
- W4P4 is already BOUNDED (≤ 6e-9, ≈ 2.5e-7 of |d|; Bridge). This run tries to EXPLAIN it.

## 2a: phase D at W4P4 with Strip3D s_cut = 6 (the one variable) — `exp085w2a.py`
- **Controls (can fail):**
  1. d^C is bitwise identical at s_cut 3 and 6: d^C does not use s_cut, so this fires if G() depends on it.
  2. d^B(6) − d^B(3) equals 085w's on-demand tail(3, 6] within s_dB. Two implementations: install residues against on-demand residues.
  3. Plant (c): 5e-9 at site 18 must FAIL (i-G).
- **Predictions:** (i-G) ≤ tolG and (i-B) ≤ tolB at s_cut 6. Tolerances use the same formulas as 085.
- **FAIL meaning:** a failing prediction means that residual is not (only) truncation, and (i-B) has another cause.

## 2b: route (ii), W4P4 (Wbox 4), n = 2, s_cut = SC in Gap AND every strip_sigma call — `exp085w2b.py`
- **KA first:** SC = 3 must reproduce the stored `exp084c/c84_W4P4_n2.json` qsad and dev_a BITWISE.
- **Test:** SC = 6.
  - Must-fire: probe σ(1 + 1e-6) > tol.
  - **PREDICTION 1:** dev ≤ 3.0756e-10 (084c's s_cut-3 tol).
  - **PREDICTION 2:** dev ≤ max(3·dev_a′, 1e-10), with dev_a′ recomputed at s_cut 6.
- **FAIL meaning:** the C2/Level-1 residual is not truncation. 084c's headline keeps "unexplained ~5e-10 at W4P4".

## Running
- Side jobs, one at a time, nice 12, no-kill. Each stops if the measured peak is ≥ 0.5 GB.
- Order: after 085w W2P4: 2a, then 2b (SC 3, then SC 6).
