# cuspis — STATUS (δκ: the O(N⁰) strip coefficient of the large-N O(N) model, D = 3)
*One page, updated only on change (fleet practice 2026-11-27). The full record is report.md / notes/ / TODO.md. Last change: 2026-11-27 21:35.*

## What we know (grades)
- **R(k), corrected with the EXP-087 t0 fix:** k = 1, 1.5, 2, 2.5 → 2.2552, 4.2334, 6.5877, 9.0902. *Partially verified.*
- **The t0 fix:** *verified* at W8P8 at the cluster level (to ~1e-9 against OFF@1e-6; EXP-096 e96d). The referee's non-cluster 7.8e-7 is unexplained. *Partially verified* at W10P10 and W12P12, where none exists yet. EXP-096 is building one now.
- **Counterterm (box c_A vs bulk c):**
  - EXP-090 at k ≤ 2.5: A *supported*; bulk overshoots. *Partially verified*: argued, not derived.
  - Wall test at n = 1: f(4→6) = 0.212 and f(6→8) = 0.2314 ("A not wrong"). *Partially verified.*
  - Wall test at n = 2: EXP-094 4→6 INCONCLUSIVE (f₂ 0.487); EXP-097 6→8 INCONCLUSIVE (f₂ 0.305); span 4→8 conclusive, **f₂ = 0.414** (descriptive; about 2× n = 1's 0.22). *Partially verified.*
    - **Open descriptive lean:** the A fraction may not be the same at every n (n = 2 ≈ 0.41 against n = 1 ≈ 0.22). *Unresolved* because there is one W2/W4 pair, no σ on f₂, and the steps fall 0.49 → 0.30, so f₂ may still drift with P. The span is the weighted mean of the steps, not a third number.
    - A third conclusive step runs only if a decision depends on constant vs drifting. The Bridge looks at this with the k = 3 readings after the W6P12 landing (11-28).
- **EXP-092:** the H-log form is supported. y₁ = 32/(3π²) is *verified* at source. c∞ lies in −0.1166 … −0.1188.

## What is running
- **Mac mini:**
  - W6P12 route (the k = 3 input): 19/48 nodes at 15.4 h, ~2.2 ks per node.
  - **ETA 28 Nov ~11:30** (range 10:30–15:30), on estimate (1.0×).
  - Guards: hold at 6.9 GB true; pause below 30 % free.
- **Air:**
  - EXP-095 routes W2P10 and W4P10 (sealed-read; sha-seal at landing).
  - EXP-095: W2P10 landed 15:02 (sealed, not opened); W4P10 (095b) running.
  - EXP-096: W8P8 known answer FAILED against the single-rad referee. Diagnostic (ea201a0) reads **H2**: the route matches OFF@1e-6 on the clusters to ~1e-9 (route verified at the cluster level); the referee's extra 7.8e-7 lies outside the clusters (unexplained; ≤ 5.5e-6 in R(2) if real). Bridge ruling (amendment 4, 1ca4cb9): pole scan W8P8 + W12P12 **CLEAR** (18:35); whole-sum referee sweep e96s_W8P8 landed 21:25: **R-noise** (d2 −2.6e-6; KA-2 FAILED, Air M1 vs Mac M4 same code 1.05e-6): the referee is noise-limited at ~1e-6, so its 7.8e-7 is not a measured truth. **W12P12 running since 21:28** (PID 22185; ~23.5 h, ×2 → 47 h; budget-h 47 pauses, never exits). **W12P12's R(2) carries an outside-entry term not resolvable below ~1e-6 in t0 (~7e-6 in R(2)).**

## Next decisions (who)
1. **W6P12 lands:** ask the Bridge before ANY k = 3 reading (EXP-090 k = 3, 081e PRIMARY, Fable S-1..S-3, E sub-seals). *Bridge.*
2. **EXP-096:** after the diagnostic, the W8P8 KA reading (H1/H2/H3) and whether W12P12 runs. Then, if the grade is FAIL, the k = 3 reading carries Δt0(truth) instead of the fix. *Bridge.*
3. **EXP-095:** path S (Fable seal) or path D (descriptive). *Sumit, next week.*
4. **c_A at P = 24** (EXP-092 amendment): after the W6P12 landing. *Bridge GO given.*
5. **n = 2 A fraction, constant vs drifting:** whether any decision needs a third step. With the k = 3 readings, 11-28. *Bridge.*

## Kill criteria (state + date, set in advance)
- **k = 3 stage** (W6P12 route → k = 3 readings):
  - *Good enough:*
    - the route lands rc 0, every route gate PASS, the stale-file guard PASS;
    - then the registered k = 3 readings are graded against their sealed bands, and the 081e PRIMARY verdict is written.
    - Then write it up. No k = 3.5.
  - *Stop:*
    - not landed rc 0 by **2026-11-29 23:30** (2 × the 36 h estimate): stop, and bring a short plan to Sumit;
    - a route gate FAILs: diagnose; no rerun without the Bridge. A VOID k = 3 is reported as VOID.
  - *25 % check-in:* done at 15.4 h. Projection 1.0× → no re-gate.
- **EXP-095** (n = 1 wall step 8 → 10):
  - *Good enough:* f(8→10) read with all controls PASS, or INCONCLUSIVE accepted.
  - *Stop:* both routes not landed by **2026-11-29 12:00**: report and ask.
- **EXP-096** (Δt0 truth at W12P12):
  - *Good enough:* W12P12 graded (EXACT / PASS / FAIL) and the W8P8 known answer PASS.
  - *Stop:* gate paragraph in amendment 4 (47 h, under 3 days). A checkpoint stop if the projection passes 47 h, then re-gate. 25 % check-in at ~12 h (sweep reading folded in). Not graded by **2026-11-30 12:00**: report what exists and stop.
- **EXP-097:** done (84b2c5c): good enough reached.
