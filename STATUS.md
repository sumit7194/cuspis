# cuspis — STATUS (δκ: the O(N⁰) strip coefficient of the large-N O(N) model, D = 3)

> **Correction (2026-11-29).** The δκ ratios R(k) = δκ_lat/κ_lat reported before EXP-100 divided by a lattice normaliser κ_lat computed in the same small box. That box is not converged at large distances: κ_lat/κ_free ≈ 0.43–0.46, depending on k. **Their absolute values are superseded.** To convert, multiply by κ_lat(k)/κ_free (0.432–0.459), or use the R_D = δκ/κ_free series in STATUS.md and `notes/NORMALISER_AUDIT_EXP100.md`. The numerator δκ_lat is computed in the same box, so R_D is not a continuum value either. Shape and trend statements are being re-checked; so far, one (the 081d trend statistic) stays in its band.
*One page, updated only on change (fleet practice 2026-11-27). The full record is report.md / notes/ / TODO.md. Last change: 2026-11-28 06:30.*

## What we know (grades)
- **R(k), corrected with the EXP-087 t0 fix:** k = 1, 1.5, 2, 2.5 → 2.2552, 4.2334, 6.5877, 9.0902. *Partially verified.*
  - **[Normaliser mark, 2026-11-28] Normaliser: convention A (same-geometry κ_lat), IR-unconverged; superseded by EXP-100.** Under R_D = δκ/κ_free, k = 1, 1.5, 2, 2.5, 3 → 1.0045, 1.944, 2.948, 4.005, 5.085 (also convention A, IR-unconverged). Register: notes/NORMALISER_AUDIT_EXP100.md.
- **The t0 fix:** *verified* at W8P8 at the cluster level (to ~1e-9; e96d); the W8P8 referee is noise-limited at ~1e-6 (e96s). At W12P12, it agrees with the independent route to 1.3e-9 on the clusters (EXP-096), but KA-complete FAILED (−7.8e-7, undiagnosed): *partially verified*. At W10P10: *partially verified* (no route run).
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
  - EXP-095: W2P10 landed 15:02; W4P10 (095b) landed rc 0 21:32, final pull validated 21:58 (sha 08deebc511a8, equal both ends). Both sealed, not opened. Path S/D: Sumit.
  - EXP-096: **W12P12 landed 06:01** (8.5 h): D = truth − fix +1.3e-9, EXACT by rule; **KA-complete FAILED AS WRITTEN (−7.8e-7), undiagnosed** (cross-chip pole/residue difference at spans ≤ 1e-7, or a missed entry). Material bound (inference) ≲ 1e-5 in R(3) against δ_mat 1.07e-3. Grade partially verified; k = 3 use of the fix waits for the Bridge. W8P8 KA failure retired (referee noise-limited at ~1e-6). Air idle (AlphaMate).

## Next decisions (who)
1. **W6P12 lands:** ask the Bridge before ANY k = 3 reading (EXP-090 k = 3, 081e PRIMARY, Fable S-1..S-3, E sub-seals). *Bridge.*
2. **EXP-096 W12P12:** whether the k = 3 readings carry the fix given D = 1.3e-9 and KA-complete FAILED (−7.8e-7), and whether to run the discriminating test (Mac pole lists vs Air). *Bridge.*
3. **EXP-095:** path S (Fable seal) or path D (descriptive). *Sumit, next week.*
4. **c_A at P = 24** (EXP-092 amendment): after the W6P12 landing. *Bridge GO given.*
5. **n = 2 A fraction, constant vs drifting:** whether any decision needs a third step. With the k = 3 readings, 11-28. *Bridge.*

## Fleet practices in force (latest first)
- **Air allocation (2026-11-28, Sumit via the Bridge):** from ~06:15 the Air's memory and GPU are reserved for AlphaMate. After W12P12 is pulled, Cuspis leaves the Air idle; no new Air job without asking the Bridge.
- **Rule 7 (2026-11-27, Sumit agreed):** (a) public text uses the field's terms ("predictions fixed before the data were examined", "computer-assisted proof"); "pre-registration/registered/sealed" stay internal. (b) Every claim that leaves this thread carries a field-expert checklist (known false positives and failure modes; each item done, with an outside check where one exists, or open). The Bridge reads it first. The Bridge drafts outreach; Sumit sends.
- **Coordinator rule (2026-11-27, Sumit confirmed here):** everything that needs Sumit goes through the Bridge; a Bridge go counts as his word, publishing included; pre-push checks always run.

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
