# EXP-099 REGISTRATION: where the free-side width curvature comes from (free side only) [model: Opus 5.5]

*2026-11-28. Ordered by the Bridge after the EXP-098 stage-0 result (f7175f2) and the seal (fb6060f). Registered BEFORE any new free value is computed. The only free values computed before this text are the stored ones, recomputed for the timing probe (e99_probe.out, all bitwise).*

## 1. The question
- EXP-098 stage 0 found a width drift d = −53% (k = 1) and −114% (k = 2). Most of it is on the free side: the per-1/W slope of the free S drifts by +49.7% and +79.2% between the pairs (W₁, W₃) and (W₃, W₂), against +8.7% and +11.0% on the σ side.
- **Question:** is the free-side curvature a finite-size effect of the geometry convention, or is it intrinsic to s(W) at these widths?
  - The convention ties Lx = 2P + Wb to the box, not to W. It also ties Lt = 2P and Ny = 4P to P.
- **Prior art, in this project (M1; found now, and it should have been read before EXP-098 was designed):**
  - EXP-080's free-side calibration (report.md, the "Free-side calibration" table under EXP-080, around line 8808) measured κ_lat/κ_free = 0.32, 0.55, 0.73, 0.85, 0.92 at box ratio r = pad/W = 2, 4, 8, 16, 32 (L = ∞, W = 4).
  - The deficit falls roughly like 1/r. That entry says the box is "the dominant systematic", and that finite periodic L = N_y overshoots when the box exceeds L.
  - In the EXP-098 convention, the x-pad over W is 2.5, 1.5, 1.0 for W₁, W₃, W₂, and the t-pad over W is 2, 1.33, 1. So each width sits at a different r, in the range where that table changes fastest. That makes a finite-size origin likely before any run, and it is the expectation stated in §4.
  - Outside this project I have done no literature search for this step: it is a lattice-convention test on our own code. Stated, not claimed.

## 2. Notation
- **The free geometry (as in `sigma3d.FreeStrip`):**
  - A 2D slice (x, t) of Lx × Lt sites with Dirichlet boundaries, and y periodic with Ny sites.
  - The cut is the t-links (x, tcut) → (x, tcut + 1) for the W strip columns x = gL … gL + W − 1.
  - A geometry is G = (W, gL, gR, hT, Ny), with Lx = gL + W + gR, Lt = 2hT and tcut = hT − 1.
  - S(G) = `FreeStrip(Lx, Lt, Ny, cols, tcut).S(cpts=12).real`, the same call as `exp081b_run.free`.
- **Convention A (stored; EXP-081b/098):** Wb = P, Lx = 3P, gL = P + (P − W)//2, gR = Lx − gL − W, hT = P, Ny = 4P.
- **Per-1/W slope for widths a, b at one geometry family:** κ(a, b) = −(S(a) − S(b)) / Ny / (1/a − 1/b), which is `exp081b_run.pair`.
- **Width triple at k:** P = 4k, (W₁, W₃, W₂) = (P/2, 3P/4, P), for k = 1, 2, 3 (P = 4, 8, 12).
- **The free drift:** df = (κ(W₁, W₃) − κ(W₃, W₂)) / κ(W₁, W₂), at each k and each geometry family. Stored, convention A: df = +0.4970 (k = 1), +0.7920 (k = 2).

## 3. Design (each arm changes ONE variable from convention A, or from its own base)
- **(a)+(b) x-gap arm, B(g):** symmetric x-gaps gL = gR = g at every width, so the strip-to-x-edge distance is held fixed as W varies. hT = P and Ny = 4P.
  - g ∈ {P, 2P, 4P, 8P}.
  - (a) is S(W, g) against g at each fixed W: the box sweep.
  - (b) is df_B(g) from the triple at the same g: the alternative convention.
  - Base check: B(P) at W = P is convention A exactly.
- **(c) t-extent arm, C(h):** convention A in x and Ny; hT ∈ {P, 2P, 4P}. C(P) = A.
- **(d) y-length arm, Dy(n):** convention A in x and t; Ny ∈ {4P, 8P, 16P}. Dy(4P) = A.
- **(e) all large (DESCRIPTIVE only; more than one variable changed):** g = 8P, hT = 4P, Ny = 16P.
- **Total:** 3 k × 3 widths × (4 + 2 + 2 + 1) geometries = 81 points, minus the duplicates that equal A.

## 4. Readings and pre-stated predictions
- **Per arm, k and swept value:** S at each width, κ(W₁, W₃), κ(W₃, W₂), κ(W₁, W₂), and df.
- **Criteria. "Largest" means the largest swept value of that arm; df_A is the convention-A value at the same k (k = 3 under A is computed here too):**
  - **REMOVED by variable X:** |df_X(largest)| ≤ 0.10 at every k.
  - **NOT REMOVED by X:** |df_X(largest)| ≥ 0.5·|df_A| at every k.
  - **PARTIAL:** anything else, reported with the numbers.
  - **INTRINSIC (no finite-size variable explains it):** NOT REMOVED in (b), (c) and (d), AND |df_E| ≥ 0.5·|df_A| at every k.
- **What each hypothesis predicts:**
  - Finite-Lx, the Bridge's hypothesis: S(W, g) depends on g in (a), and the drift shrinks under (b) as g grows (REMOVED or PARTIAL).
  - Intrinsic: the drift survives (b), (c), (d) and (e).
  - Finite-Lt and finite-Ny are the same hypothesis for the other two lengths, in (c) and (d).
- **My expectation, stated before any run (from the EXP-080 table):** both the x-pad and the t-pad matter.
  - Neither (b) nor (c) alone reaches ≤ 0.10: PARTIAL in each.
  - (e) shrinks the drift more than any single arm.
  - (d) changes it little at these Ny/W ≥ 4. Weakly held: the EXP-080 overshoot is a warning.
- **The edge-effect functional form, a GUESS:**
  - A power law in the distance, not exponential: the p = 0 slice is massless.
  - The leading term is about 1/ℓ in the per-1/W slope, by analogy with EXP-080's "deficit ≈ 1/r".
  - It is checked descriptively in (a) by the local exponent a(g) = log[ΔS(g→2g) / ΔS(2g→4g)] / log 2 at each fixed W, reported with its drift between the two g-windows.
  - **Extracting an exponent from points is inference, not verification.** It is labelled descriptive, and a drift between windows larger than 0.3 means "no stable exponent".

## 5. Controls (each can fail; run FIRST, readings only after all PASS)
- **Preflight:** the venv with numpy and scipy (the amendment-2 mechanism).
- **KA-sweep:** the sweep's geometry function, called at each stored geometry, reproduces every stored free cache in exp081b_results/ **bitwise**. That is all 23 files, in both box conventions (Wb = P and Wb = 4): Lx = 2P + Wb, gL = P + (Wb − W)//2, hT = P, Ny = 4P.
  - It includes the stage-0 values free(3, 4, b4) and free(6, 8, b8), as the Bridge required.
- **KA-base (arm wiring, positive):** at each arm's base value the arm's code reproduces convention A bitwise: B(P) at W = P, C(P) and Dy(4P), at every width where they coincide.
- **Arm wiring, negative (must change):** at the next swept value, S must differ from the base by > 1e-12·|S|. This catches a variable that is silently ignored.
- **Plant 1 (a wrong convention must change the value):** shift the strip by one column (gL + 1, gR − 1) at W2P4 with g = P. S must change by > 1e-9·|S| (FIRES).
- **Plant 2 (a wrong cut row):** tcut = hT − 2 at W2P4 (A). S must change by > 1e-9·|S| (FIRES).
- **If any control fails:** STOP and report; no reading is printed.

## 6. The W9P12 free values and the seal
- Free values at W = 9, P = 12 (all arms, convention A included) are computed in this sweep. The seal fb6060f is already committed and stays the falsifier, **unchanged**.
  - **Seeing free(9, 12) does NOT amend the seal.** No re-seal follows from it.
  - The D(3) census gate (amendment 2 of EXP-098) stands.

## 7. Cost, run plan, kill criteria
- **Timing probe (MEASURED, e99_probe.out, stored geometries only, 1 thread on the venv):**
  - W4P4b4: 0.25 s (includes warm-up);
  - W8P8b8: 0.03 s;
  - W12P12b12: 0.11 s (N = 864, Ny = 48);
  - W4P12b4: 0.06 s.
  - **The largest geometry is an ESTIMATE, not measured:** (e) at k = 3 has N = Lx·Lt = 204 × 96 = 19584 and Ny = 192. Scaling the sparse LU as about N^1.5 per slice from the W12P12 timing gives roughly 0.11 s × (19584/864)^1.5 × (192/48) ≈ 50 s for that point.
  - The total for 81 points is estimated at under 10 min. The run logs each point's measured time.
- **Run:** `exp099_free.py` on the venv, 1 BLAS thread, nice 10, under the no-kill watchdog with the ≥ 50% free gate. No hard caps.
- **Kill criteria:**
  - Good enough: rc 0 with all controls PASS.
  - Stop: not landed by **2026-11-29 12:00 IST**. Then report and ask the Bridge; nothing is killed.
- **After the sweep:** stage 1 of EXP-098 goes back to the value gate, with a Neon outside view on the two field questions (the Bridge's plan).

## 8. Exposure
- Known before this text: every stored free value (23 caches) and every EXP-098 stage-0 number.
- No free value at any non-stored geometry has been computed or seen.

## Amendment 1 (2026-11-28 21:50 IST; after the registered readings, BEFORE these two points are computed)
- **Why:** the registered verdicts are (b) PARTIAL (|df| 0.21, 0.30, 0.32, saturated at g ≥ 2P), (c) and (d) NOT REMOVED, and (e) all-large |df| 0.014, 0.035, 0.038. Going from B_g8P to E changes TWO variables (hT and Ny), so the step that removes the rest is not isolated.
- **Added points (one variable from B_g8P):** B(g = 8P, hT ∈ {2P, 4P}, Ny = 4P) at k = 1, 2, 3. Same code (`exp099_free.S`), same df.
- **Prediction, stated now:** Ny was inert in (d) under convention A, to ≤ 4e-4 in df. So |df| at B(8P, hT = 4P, Ny = 4P) equals |df_E| within 0.01 at every k, and hT = 2P lies between B_g8P and that value.
  - If it does not, then Ny matters under symmetric gaps, and the "t-extent removes the rest" reading is wrong.
- **Control:** B(8P, hT = P, Ny = 4P) is recomputed by the amendment script and must equal the stored B_g8P κ values bitwise.
- **Label:** a post-registration amendment, descriptive. It does not change the registered verdicts.
