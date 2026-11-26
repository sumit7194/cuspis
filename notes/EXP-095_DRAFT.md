# EXP-095 DRAFT (NOT registered; nothing computed): third wall step, strips (2, 4), walls P = 8 → 10 [model: Opus 5.5]
*Drafted 2026-11-26 ~17:45 for the Bridge, after EXP-093 passed. It becomes a registration only on the Bridge's go, with a sealed prediction attached.*

## Why
- f(4 → 6) = +0.212 (EXP-089) and f(6 → 8) = +0.231 (EXP-093) agree.
- A third step tests whether f is constant, i.e. "a property of the box". ρ_A changed sign between P = 6 and 8 (+0.047 → −0.046), so ρ_A(10) also shows whether it keeps falling.

## Quantities
- Exactly `exp089_wall.row(10)`, verbatim (as in exp093_p1.py). f(8 → 10) = −[ρ_A(10) − ρ_A(8)] / [G_b(8) − G_b(10)], with the P = 8 row taken from exp093_p1.json.

## Inputs (none exist today: checked, no W2/W4 P10 checkpoint or G file)
- **Route W2P10:** `exp081d_route.py 2 10 10`, run on the Air. It uses the same 3.14.10 environment that passed identity, CUSPIS_081E unset, nice 10, the no-kill watchdog and freepct_guard v3 (LOW 25 / HIGH 35, pause-only), and the same 30-min validated pull (pull_air_093.sh with NAME=…W2_P10…).
- **Route W4P10:** `exp081d_route.py 4 10 10`, run on the Mac mini after the W12 chain, or on the Air after W2P10.
- **GEOM:** `exp085c_run.py GEOM 2 10` and `GEOM 4 10`, on the Mac mini.

## Footprint (scaled from measured runs; unverified)
- **W2 route on the Air:** P = 6 took 1952 s and P = 8 took 16174 s (×8.3, effective exponent 7.35). Scaled, P = 10 takes ~84000 s ≈ **23 h**.
  - Peak: 0.89 GB at P = 8 (0.62 resident + 0.27 compressed). Scaled, P = 10 is ~2–3 GB, **at or above the ~2 GB Air line**, so it needs a peak hold at 3 GB (pause-only).
- **W4 route:** at P = 6 it took 1.3× the W2 time (Mac mini). Scaled, P = 10 is ~30 h on the Air, fewer on the Mac mini.
- **GEOM:** G_W4P8 took 6 min at 0.33 GB, so P = 10 should take minutes and well under 1 GB.

## Controls (same as EXP-093)
- row(4), row(6) and row(8) reproduce exp089_wall.json and exp093_p1.json bitwise.
- The route gates pass: B2b, t0 refined vs unrefined, residue, every unconverged count 0, and rc 0.
- Stale-file guard, must-fire tested.
- The G files have an empty `failed`.
- The Air gets no new identity run, since the code, environment and machine are unchanged. If the Bridge wants one, the stored W2P8 is the reference (5 h).

## Grading: needs a sealed prediction
- I am NOT blind: I know f at two steps and ρ_A at P = 4, 6, 8, so a band from me is not a test.
- **Proposal:** the Bridge asks Fable for a seal on ρ_A(10), G_b(10) and f(8 → 10), if Sumit allows Fable use for this. Otherwise it is registered as **descriptive only** (a measurement, no PASS/FAIL).
- **INCONCLUSIVE for f** if G_b(8) − G_b(10) < 0.2·G_b(8) = 0.204. This is the same scaling rule as EXP-089/093.
