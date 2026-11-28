# EXP-100 REGISTRATION: converge the box first; check the σ side for an Lt bias; continuum normaliser [model: Opus 5.5]

*2026-11-28. This is the Bridge's value-gate ruling on EXP-098 stage 1, made after the Neon outside view. Stage 1 (W9P12 under convention A) is NOT run. Registered BEFORE any EXP-100 value is computed. Known before this text: all EXP-098 and EXP-099 numbers.*

## 0. What changes, stated explicitly
- **The registered estimator changes (part D).**
  - Until now: R(k) = δκ_lat/κ_lat, both from the same convention-A geometry.
  - From EXP-100 on: **R_D(k) = δκ_lat(G)/κ_free**, with κ_free = 0.0396481, the continuum free value per real scalar.
    - Source of that value: this project, three routes (report.md, the EXP-079/080 calibration, "κ_free = 0.0396481 per real scalar"). It is in mild tension with the third printed figure of CHL09 (report.md, same entry). Graded there as partially verified.
  - The large-box κ_lat(W) at G is reported beside it as the UV bracket.
- **Why:** EXP-099 showed that the free side's finite-size artefact does not cancel in the ratio. The σ slope drifted 9–11% where the free slope drifted 50–83%.
- **Seal fb6060f is SUPERSEDED BEFORE TEST (part E).** Convention A's D(3) will not be measured. The seal stays committed and unopened as a test. It is not failed and not passed.
- **The Neon citations, checked at source (abstracts only, 2026-11-28, via a fetch agent; full papers not read):**
  - All six abstracts are SILENT on the specific claims attributed to them:
    - Casini & Huerta hep-th/0606256 (corners, not strips);
    - Casini & Huerta 0905.2562 (a review; no strip coefficient in the abstract);
    - Diehl & Rutkevich 1512.05892 (an O(n) n → ∞ strip with free surfaces, Casimir forces; no exp(−2mz) statement);
    - Whitsitt, Witczak-Krempa & Sachdev 1610.06568 (large-N Wilson-Fisher EE; no strip);
    - Metlitski, Fuertes & Sachdev 0904.4477 (O(N) EE, cylinder);
    - Chojnacki et al. 1607.05311 (two-cylinder Rényi on a lattice; no IR-convergence procedure stated).
  - **So no step of EXP-100 relies on any of them.** The design rests on this project's own measurements: EXP-080's box table, EXP-099, and the EXP-099 slab rate.

## 1. Notation
- **Free geometry G = (W, g, hT, Ny):** equalised x-gaps gL = gR = g, Lx = W + 2g, Lt = 2hT, tcut = hT − 1, y periodic with Ny sites. S_free(G) is exp099_free.S, verbatim.
- **σ geometry:** the same G, through `exp100_route.py`. That is a COPY of exp081d_route.py with the geometry as arguments (--gL --gR --hT --Ny). At the convention-A arguments it is the same code path.
- **Pair slope:** κ(a, b; G) = −(S(a) − S(b))/Ny/(1/a − 1/b). The same formula gives δκ(a, b; G) on σ's S_T0 (with the t0 fix as registered: Δ = 0 where ON = OFF).
- **Width pair:** (W₁, W₂) = (P/2, P), P = 4k.
- **Box chain T(m):** hT = m·P, g = Lt = 2hT, Ny = 2Lt = 4hT, for m = 1, 2, 4, 8, 16. Each step doubles every IR length at fixed ratios g/Lt = 1 and Ny/Lt = 2.

## 2. Part A: free side (seconds per point)
- **Points:**
  - Chain T(m) at k = 1, 2 for m ≤ 16, and at k = 3 for m ≤ 8. A point is scheduled only if the measured time of its chain predecessor, times 8, is under 15 min. Unscheduled points are listed, not killed.
  - At every scheduled m, two one-variable arms: g ∈ {Lt/2, 2Lt} and Ny ∈ {4Lt}. Ny ≥ 2Lt throughout.
  - Widths P/2, 3P/4, P at every point (3P/4 for later use).
  - The antiperiodic-in-t arm is NOT done. The current operator has open t-ends only, and adding a boundary type is a code change I am not making in this step. Stated.
- **Criterion (fixed now; the Bridge's 1%):** G* = T(m*) is IR-converged for k if m* is the smallest scheduled m such that ALL of the following move κ(W₁, W₂) by < 1%:
  - (i) T(m*) → T(2m*);
  - (ii) g: Lt → 2Lt at m*;
  - (iii) Ny: 2Lt → 4Lt at m*.
  - If no scheduled m qualifies, the reading is "NOT CONVERGED within the affordable chain". The sequence is reported, and any extrapolation is labelled inference.
- **Reported:**
  - the chain κ(W₁, W₂; T(m)), κ/κ_free, and the arm deltas;
  - the slope drift df(m) from EXP-099 at each m;
  - **the UV bracket:** κ_lat(W₁, W₂; G*)/κ_free.
  - A check that can fail: if that ratio lies outside [0.85, 1.05], a normalisation mismatch between our κ_lat and κ_free is FLAGGED. Its stated basis is EXP-099 (e), 0.90–0.94, and EXP-080, 0.92 at r = 32.
- **Prediction (from EXP-080's deficit of about 1/r and EXP-099's (e)):** convergence in m is SLOW, about 1/m, so the 1% criterion is reached late or not at all at k = 2, 3. (ii) and (iii) are small (< 1%) at every m ≥ 2. The latter follows from the slab rate: at g = Lt, the edge term is about e^(−2π) ≈ 2e-3.

## 3. Part B: interacting Lt-doubling check (route-hours)
- **Geometry, fixed now:**
  - B0 = T(1) (hT = P, g = 2P, Ny = 4P);
  - B1 = T(2) (hT = 2P, g = 4P, Ny = 8P);
  - both at k = 1, widths (2, 4).
  - So Lt doubles with equalised gaps and Ny = 2Lt.
- **Why k = 1:** it is the ONLY pair whose B1 fits the machine. At k = 1, B1 has N = Lx·Lt = 20 × 16 = 320 and Ny = 32, comparable to the W6P8 route (N = 384, Ny = 32), which took 3.18 h. At k = 2, B1 has N = 40 × 32 = 1280 and Ny = 64, so the (Ny, N, N) complex arrays alone are about 1.7 GB each, with several held at once. Over the envelope.
  - **Stated plainly:** k = 1 (W = 2, 4) is NOT shown to be in the scaling regime. R(k) is still growing with k (EXP-090), and W = 2 is lattice-scale. A null at k = 1 does not transfer to larger W without an argument. A non-null is evidence that the σ side carries an Lt bias somewhere.
- **Controls, run FIRST:**
  - KA-route: `exp100_route.py 2 4 4` with explicit convention-A geometry arguments (gL = 5, gR = 5, hT = 4, Ny = 16) reproduces the stored W2P4 checkpoint bitwise (t0, tsad, 48 nodes, n1c arms), as in EXP-098 KA-0.
  - The route's own guards: planted must-fire, B2b, N1'''c, t0 refined, stale-file guard.
  - The interpreter preflight (the amendment-2 mechanism).
  - exp087_t0 OFF = route t0 at each new geometry.
- **Cost, from a MEASURED timing probe:** `exp100_route.py --probe` at B0 and B1 for W = 4 runs install, B1 and one g node, prints only wall times, and writes and prints no value. The projection is install + t0 + tsad + 48 × (node time) + checks, scaled from the measured node.
  - **If the projected B total exceeds 12 h, B goes back to the value gate before running** (the Bridge's rule). Otherwise B runs with the standard guards, 1 thread, nice 10, pause-only, and with a 25% check-in if it runs over 6 h.
- **Reading:** Δ_B = [δκ(2, 4; B1) − δκ(2, 4; B0)] / δκ(2, 4; B1).

## 4. Part C: branch rule (fixed now)
- **Error budget for δκ(2, 4) at k = 1, stored:**
  - numerical σ, relative to R, is 2.6e-10;
  - Δ_t0 = 0 at W ≤ 4 (no t0-fix term);
  - s_KA does not apply at k = 1.
  - So the numerical budget is about 1e-9 relative. The relevant floor is instead the normaliser's own IR criterion of 1% (part A). An Lt bias below it cannot change R_D beyond the normaliser's convergence.
- **Threshold:** τ = max(5 × 1e-9, 0.01) = **0.01**.
- **Branches:**
  - If |Δ_B| > τ: the σ side has an IR (Lt) bias at the stage-0 geometry. The stage-1 budget is REALLOCATED to width pairs at the converged geometry G* (σ at G*, at the largest affordable k), with its own registration.
  - If |Δ_B| ≤ τ: a third width at the converged geometry G*, with its own registration.
  - Either branch goes to the Bridge before any route-hours are spent on it.

## 5. Part D: normaliser
- For every k with a σ value at geometry G: R_D(k; G) = δκ(W₁, W₂; G)/κ_free.
- The bracket R(k; G) = δκ/κ_lat(W₁, W₂; G) is reported beside it.
- For the stored convention-A values (k ≤ 3) both are reported, labelled "convention A, IR-unconverged".

## 6. Kill criteria and exposure
- **Part A:** good enough = rc 0 with all controls PASS. Stop = not landed by 2026-11-29 12:00 IST.
- **Part B:** good enough = both B geometries complete with all controls PASS. Stop = not landed by 2026-11-30 12:00 IST, or a projection over 12 h (then gate). Nothing is killed.
- **Exposure:** no EXP-100 value has been computed. EXP-099's (e) and amendment values at hT ≤ 4P, Ny ≤ 16P are known; chain T(m) points with m ≤ 2 overlap some of them (k = 1, 2, 3 at hT ≤ 4P).

## 7. Controls for part A (each can fail)
- **KA-sweep subset:** the part-A code reproduces the stored EXP-099 value B(W = P, g = P, hT = P, Ny = 4P) bitwise at each k.
- **Arm wiring negative:** each arm variable changes S by > 1e-12 rel.
- **Plant:** a 1% scale on Ny inside the slope formula only (the wrong normalisation) must move κ by 1% ± 1e-9. This catches an Ny mis-wiring in the slope.
- **Normalisation-mismatch flag** (§2): it can fire.

## Amendment 1 (2026-11-28 22:03 IST; before any EXP-100 value; the registered §3/§7 text above had arithmetic slips)
- **§3, "Why k = 1": the corrected sizes (g = Lt, so Lx = W + 2Lt):**
  - k = 1: B0 has N = Lx·Lt = 20 × 8 = 160, Ny = 16. **B1 has N = 36 × 16 = 576, Ny = 32** (not "20 × 16 = 320"). That is LARGER than the W6P8 route (N = 384, Ny = 32, 3.18 h), so B1 may exceed 12 h, and the timing probe decides.
  - k = 2: B1 has N = 72 × 32 = 2304, Ny = 64. **A single (Ny, N, N) complex array is about 5.4 GB** (not "about 1.7 GB"). The conclusion, out of the envelope, is unchanged.
- **§7 plant: corrected wording.** Using 1.01·Ny in the slope formula only must give exactly κ/1.01, to 1e-12 relative (κ ∝ 1/Ny). The old "by 1% ± 1e-9" was imprecise.
- Nothing else changes.

## Amendment 2 (2026-11-28 23:51 IST, committed b8906f1; the first draft of this heading said "2026-11-29 ~00:30", wrong; Bridge ruling (a) on part B; before any part-B value)
- **Ruling.** The Bridge chose (a): split the production nodes across 4 single-thread processes. A split-vs-whole BITWISE known answer at W2P4 runs first. If it is not bitwise, stop and report.
- **How the split runs.**
  - Each part gets its own checkpoint, through `--tag-suffix`. The parts cover nodes 0:6 | 6:20 | 20:34 | 34:48, and part 0 also computes t0 and tsad.
  - Why separate files: `exp100_route.put()` rewrites the whole in-memory dict on each write. Several processes on one file would silently drop each other's nodes.
  - `exp100_merge.py` merges the parts. It copies values and never recomputes them. It refuses: an overlapping node; a union that is not the 48 C-nodes; t0 or tsad outside part 0; install ranks that differ; check-stage keys inside a part; an existing output. Its self-test plants each of these defects, and each one must be refused.
  - The unsplit route then runs the check stage (planted, B2b, N1'''c, Woodbury, summary) on the merged file.
- **KA (phase 1).**
  - The split run is at W2P4 with the convention-A geometry passed explicitly (gL = gR = 5, hT = 4, Ny = 16), then merged and checked. It is compared with the stored whole checkpoint `sigma_W2_P4_box4_c2_cp12_sc3.0_dd0_ckpt.json`: t0, tsad, the 48 g nodes and the n1c arms, all bitwise.
  - A comparator plant runs first: one node moved by one ulp must be reported.
  - This also satisfies §3's KA-route.
- **t0 fix at the new geometries.** `exp087_t0.py` is convention-A only. `exp100_t0.py` is an exact-text copy with the geometry as arguments; the differences are shown by `diff`.
  - KA-t0: the OFF value must equal the route t0 to 1e-10 relative.
  - Δ = t0_on − t0_off enters as in `exp098_3w.pairR`: δκ = −[(S_T0(a) + Δ_a/2) − (S_T0(b) + Δ_b/2)]/Ny/(1/a − 1/b).
  - This t0 work was NOT in the 13.9 h projection. It runs alongside the split parts.
- **Analysis `exp100_B.py`.**
  - KAN: the δκ code applied to the stored convention-A k = 1 checkpoints, divided by κ_A(1), must reproduce the stored R^c_T0(1) = 2.2552242844155943 to 1e-12. The DRY passes at +0.0e+00.
  - The route guards are re-checked from each checkpoint. Each guard has a planted negative in the DRY, and all of them fire.
  - Plant: δκ(B1) × 1.02 must move Δ_B to its prediction.
  - The free κ_lat(2, 4; B0 / B1) must equal part A's chain T(1) / T(2) κ12, bitwise.
  - Readings are printed only if every control PASSES.
- **Phases and memory (peak per process from the probe).**
  - 1: KA, small.
  - 2: B0 W4 ∥ W2 (whole routes), then their t0 fixes.
  - 3: B1 W4 × 4 parts, about 6.0 GB.
  - 4: B1 W2 × 4 parts ∥ t0 fix at B1 W4, about 6.3 GB.
  - 5: merges; B1 W4 checks ∥ B1 W2 checks ∥ t0 fix at B1 W2, about 3.9 GB.
  - 6: reading.
  - Each phase passes the free ≥ 50% gate and the pgate. The freepct_guard is pause-only; nothing is killed.
- **Time, state plus date (from the probe):**
  - Expected wall about 5 h: phase 3 about 7,000 s, phase 4 about 6,300 s, phase 5 about 4,000 s, phases 1–2 about 0.4 h.
  - Check-in at about 25%: when B1 W4's parts have logged their first nodes, with the per-node rate against the probe's 490 s.
  - If it has not landed by 1.5 × the estimate (about 7.5 h after launch), report the state.
  - No automatic stop. The registered part-B stop date (2026-11-30 12:00 IST) stands.
- **What B can and cannot settle (stated before any value).**
  - **Can:** whether δκ(2, 4) at k = 1 moves by more than τ = 1% when every IR length doubles, T(1) → T(2). On the same step the free κ moves 38%.
  - **Cannot:**
    - (i) that δκ is IR-converged at T(2). A small |Δ_B| is consistent with convergence but does not show it. The free side's later steps are 13%, 4.4% and 1.5%, and a single σ step gives no tail.
    - (ii) anything about the scaling regime (k = 1, W = 2, 4).
    - (iii) R_D at k ≥ 2.
    - (iv) If |Δ_B| > τ, the size of the σ bias at T(2) is itself IR-unconverged, so δκ(B1) is not a converged value either.
