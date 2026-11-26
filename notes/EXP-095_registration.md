# EXP-095 REGISTRATION (2026-11-26 ~18:00; nothing computed): third wall step, strips (2, 4), walls P = 8 → 10, SEALED-READ design [model: Opus 5.5]
*Registered on the Bridge's rulings of 2026-11-26 (after draft 862d378, `notes/EXP-095_DRAFT.md`, whose quantities, inputs and footprint carry over unchanged unless restated here).*

## Quantities (fixed now)
- `row(10)` = exp089_wall.row VERBATIM, through a new grader `exp095_p1.py`, a copy of exp093_p1.py with P 8 → 10 and the reference row = exp093_p1.json's r8.
- Read at P = 10: R, Y_A, Y_bulk, **ρ_A(10) = R − Y_A**, **G_b(10) = Y_bulk − Y_A**, κ₁₀, norm₁₀.
- **f(8 → 10) = −[ρ_A(10) − ρ_A(8)] / [G_b(8) − G_b(10)]**, with ρ_A(8) = −0.046306…, G_b(8) = 1.021478… (exp093_p1.json, bitwise).
- **INCONCLUSIVE for f** if G_b(8) − G_b(10) < 0.2·G_b(8) = 0.204 (scaling rule as in EXP-089/093). ρ_A(10) and G_b(10) are read regardless.

## Inputs (all fresh; none exist today, checked 17:40)
- **W2P10 route:** `exp081d_route.py 2 10 10` on the MacBook Air (`~/GitHub/fleet-air/corner_function/scripts`). It uses the 3.14.10 environment that passed the EXP-093 identity, CUSPIS_081E/087 unset, nice 10, caffeinate -i, the no-kill watchdog, freepct_guard v3 (LOW 25 / HIGH 35, PID-scoped, pause-only), and a **3 GB pause-only peak hold** (tools/peak_hold.sh, SIGSTOP only, resume only on the Bridge's word).
- **W4P10 route:** `exp081d_route.py 4 10 10` on the Air, AFTER W2P10, under the same guards. That keeps the Cuspis Air budget of 1 process. Running it alongside W2P10, which the Bridge allows if the peak is ≤ 2.5 GB and free ≥ 40%, is NOT used unless the Bridge confirms that Sumit has raised the Air budget.
- **GEOM:** `exp085c_run.py GEOM 2 10` and `GEOM 4 10` on the Mac mini, nice 15, with the no-kill watchdog and pgate.
- **Pull-back:** tools/pull_air_093.sh with NAME = each checkpoint, every 30 min, validated by sha256 at both ends, JSON parse and node count non-decreasing. The Air is read-only.
- No new identity run (same code, environment and machine as EXP-093). The import closure's sha256 manifest is re-checked on both sides before launch.

## SEALED-READ protocol (the blindness of every reader, me included)
- **While computing and at landing, I may look at ONLY:** rc lines; gate verdict words (PASS / FAIL / STOP / NON-CONVERGED); unconverged counts; node counts; sha256; watchdog memory and time columns; and file existence.
  - Each look at a route or GEOM `.out` is a `grep -c` for those words, or a gate line on its own. No line carrying t0, tsad, T_sad, g, X_cA or Sigma3D values is printed.
- **At landing:** commit ONLY the sha256 of the four outputs (both checkpoints, both G files), written to `exp081d_results/exp095_sealed_sha256.txt`.
  - The outputs themselves stay uncommitted and unopened. They may be copied, but not parsed beyond node counts.
  - `exp095_p1.py` is written and committed, but **NOT run**.
- **Opening (next week):**
  - **Path S (seal):** a blind predictor, Fable on Sumit's personal account if Sumit OKs it then, seals ρ_A(10), G_b(10) and f(8 → 10), each with a ±1σ band. The seal is committed and its hash recorded.
    - Then the sha256 of the four outputs are re-verified against the sealed file. Any mismatch is a FAIL of the protocol, reported, and no grade.
    - Then `exp095_p1.py` runs. Controls run first with a hard stop: row(4), row(6) and row(8) bitwise against exp089_wall.json / exp093_p1.json; the route gates; the stale-file guard (must-fire tested); G files with empty `failed`.
    - PASS per item iff inside ±1σ; the ±2σ result is reported beside it, as in EXP-093.
  - **Path D (descriptive):** if Sumit declines Fable, the same opening and controls run, and the numbers are reported as a **measurement only, no PASS/FAIL**, stated as such.
    - Reported, not graded: whether f(8 → 10) lies within ±0.08 of the mean of f(4 → 6) and f(6 → 8), i.e. 0.2215. This band is mine and I am not blind, so it is descriptive.
- **Leak rule:** if any P = 10 value is seen by accident, it is declared at once to the Bridge and in report.md. Path S is then void for the items it touches, and those items go descriptive.

## Footprint (scaled, unverified; the measured peak is reported to the Bridge after the first hour)
- W2P10 on the Air: ~23 h, ~2–3 GB.
- W4P10 on the Air: ~30 h, so the routes finish in ~2–2.5 days serially.
- GEOM: minutes each, < 1 GB expected.
