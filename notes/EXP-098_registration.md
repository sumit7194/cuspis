# EXP-098 REGISTRATION: a third strip width (stage 0: k = 1 and k = 2) [model: Opus 5.5]

*2026-11-28. The Bridge approved this in stages: stage 0 GO; then a SEAL; then stage 1 (W9P12) with its own registration. It is registered BEFORE any stage-0 run. Nothing has been computed for the new widths.*

## 1. Why it matters
- Every R(k) is a two-width difference. The strip coefficient is δκ_lat = −[s(W₁) − s(W₂)] / (1/W₁ − 1/W₂), with W₁ = P/2 and W₂ = P (P = 4k), and κ_lat is built the same way on the free side.
- This assumes s(W) = s_∞ + δκ/W, with the 1/W² and box terms negligible (the premise stated in EXP-081b).
- That premise has never been tested on the σ side. The only measured scale is the free-side box systematic of about ±4% (081a/081b). At k = 3 no row tests width drift (the robustness row is about the t0 fix; correction of 2026-11-28).
- **How much it can move (from the stored k = 3 numbers):**
  - (R2) row 2 leaves "supported" if R(3) rises by ≥ +0.58 (4.9%) relative to the lower k.
  - (R4)(b) leaves "power-divergent" only if R(3) falls by ≥ 1.67 (14%). Its r is a ratio of increments, so a drift that is the same fraction at every k cancels.
  - So a drift on the free-side scale can change (R2).
- **Stage 0 measures the drift at k = 1 and k = 2 (cheap).** It is (i) the pilot for stage 1, with its timings used to re-estimate the cost, and (ii) the basis of the sealed k = 3 prediction.

## 2. Notation (every symbol used below)
- P = 4k; box Wb = P; Lx = 2P + Wb; Lt = 2P; Ny = 4P (c = 2); cut row P − 1; the strip occupies x0 … x0 + W − 1 with x0 = P + (Wb − W) // 2. This is the exp081d_route / exp087_t0 geometry, unchanged.
- **Widths:** W₁ = P/2, W₃ = 3P/4, W₂ = P. So k = 1 gives (2, 3, 4) at P = 4, and k = 2 gives (4, 6, 8) at P = 8.
  - **Premise kept and stated:** odd W₃ (k = 1: W = 3) sits ½ site off-centre in the box, since (Wb − W) // 2 rounds. k = 2 (W = 6) is centred. Any off-centre effect is included in D(1) and is not separated from width drift.
- **σ side:** for tail t ∈ {T0, T1}, S_t(W) comes from `exp081d_analyze.S_T(checkpoint, step0)`, verbatim. step0 files exist only at P ≥ 10, so at P = 4 and 8 step0 is None, as in the stored R(1) and R(2). cum(W) is S_T's cumulative error.
- **Corrected S:** S^c_t(W) = S_t(W) + ½·Δ(W), with Δ(W) = t0(ON) − t0(OFF) (EXP-087). This is the same as `corr()` in exp090_k3.py (it adds ½(Δ(W₂) − Δ(W₁))·norm).
  - Δ(W₂ = 8, P = 8) = d8 from exp087_referee_W8P8.json, as in exp090_k3.py, with s_Δ = s8. Δ(W₁) = 0 and Δ(W₂ = 4, P = 4) = 0, as stored (dW1 = 0, dW2(1) = 0).
  - **New:** Δ(W₃) comes from `exp087_t0.py W₃ P <route t0>`. Its uncertainty is s_Δ(W₃) = 3%·|Δ(W₃)| (the registered W8P8 model-gap fraction; EXP-090 robustness rule). If Δ(W₃) = 0 exactly, s_Δ = 0.
- **Free side:** F(W) = `exp081b_run.free(W, P, Wbox=P)` (cached in exp081b_results/), verbatim.
- **Pair quantities:** for widths a, b:
  - f_ab = 1 / Ny / (1/a − 1/b);
  - δ_t(a, b) = −(S^c_t(a) − S^c_t(b))·(1/Ny)/(1/a − 1/b);
  - κ(a, b) = `exp081b_run.pair` on F, i.e. −(F(a) − F(b)) / Ny / (1/a − 1/b);
  - R_t(a, b) = δ_t(a, b) / κ(a, b).
  - σ(a, b) = |R_T0 − R_T1| + |f_ab/κ(a, b)|·(cum(a) + cum(b) + ½s_Δ(a) + ½s_Δ(b)). This is Rk's σ convention, with the t0-fix uncertainty added linearly.
  - **R^c(k) := R_T0(W₁, W₂)**, the registered corrected series (KA below).
- **Drift:**
  - D_t(k) = R_t(W₁, W₃) − R_t(W₃, W₂); σ_D = σ(W₁, W₃) + σ(W₃, W₂) (linear sum, conservative).
  - d(k) = D_T0(k) / R^c(k) (relative).
  - "Drift seen at k" iff |D_T0(k)| > 2σ_D and D_T0, D_T1 have the same sign.
- **Three-width value:**
  - On each side, s(W) = s_∞ + A/W + B/W², solved exactly through the three widths (3×3 solve).
  - R_q,t(k) = A_σ,t / A_free (the sign convention cancels in the ratio). q(k) = (R_q,T0(k) − R^c(k)) / R^c(k).
  - σ_q = |R_q,T0 − R_q,T1| + Σ_W |∂R_q/∂S(W)|·(cum(W) + ½s_Δ(W)), with the derivatives by central finite difference, step 1e-6·max(|S|, 1).

## 3. Stage-0 readings (DESCRIPTIVE at k = 1, 2; they are the basis of the seal, not claims about k = 3)
- Per k: D_T0, D_T1, σ_D, d(k), "drift seen" (yes/no); R_q,T0, R_q,T1, σ_q, q(k); and the three pair values R(W₁, W₃), R(W₃, W₂), R(W₁, W₂).
- Also reported: Δ(W₃) at k = 1, 2; the wall time and peak of every run (the pilot for stage 1).

## 4. Controls (each can fail; run order as listed)
- **KA-0, the route known answer, run FIRST:** a fresh `exp081d_route.py 2 4 4 --tag-suffix _098ka` (flags as for the stored k ≤ 2.5 routes: CUSPIS_081E and CUSPIS_087 unset). It must reproduce the stored `exp081d_results/sigma_W2_P4_box4_c2_cp12_sc3.0_dd0_ckpt.json` **bitwise**: t0, tsad, all 48 g nodes, and the n1c arms.
  - If it is not bitwise: STOP, report, and find out WHY before anything else runs. A red light is a claim to investigate, not a finding.
- **KA-A, the analysis code path:** the exp098 code, given only (W₁, W₂), must reproduce `exp081d_results.json` R(1) and R(2) (R_T0, R_T1, sigma, kappa) **bitwise**, and R^c(1), R^c(2) against `exp090_k25.json` Rc **bitwise**.
- **KA-t0:** exp087_t0's OFF line at W3P4 and W6P8 must equal the new route's t0 (≤ 1e-10 rel; the script's own PASS line).
- **Route guards:** the route's own must-fire planted check and its other checks; stale-file guard (checkpoint mtime ≥ the runner start; t0, tsad, all 48 nodes, n1c, summary present).
- **Plant P1 (must fire / must hold):** add B·(1/W²) to S^c at all three widths of a planted copy. B is chosen so the predicted D_T0 shift is 10·max(σ_D, 1e-9·|R^c|). D_T0 must move by the predicted amount within 1% (FIRES), and R_q,T0 must not move by more than 1e-9 relative (HOLDS: an exact quadratic absorbs a pure 1/W² term).
- **Plant P2 (W₃ wiring):** add ε to S^c(W₃) only. D_T0 must move by the predicted −ε·(1/Ny)·[1/((1/W₁ − 1/W₃)κ₁₃) + 1/((1/W₃ − 1/W₂)κ₃₂)] within 1%.
- Each plant runs on planted copies only; the real values are not touched.

## 5. What D(1), D(2) are used for: the SEAL (method fixed HERE; numbers in a separate commit before W9P12)
- d_pred(3) = d(2) + (d(2) − d(1)) (linear in k).
  - σ_pred = hypot(|d(2) − d(1)|, σ_d(2) + σ_d(1)), with σ_d = σ_D/R^c. The first term is the model spread, linear against constant.
  - D_pred(3) = d_pred(3)·R^c(3), with R^c(3) = 11.7582 (EXP-090, d1c2da1).
- q_pred(3) = q(2) + (q(2) − q(1)); σ like σ_pred. Hence R_q,pred(3) = R^c(3)·(1 + q_pred(3)).
- **Also sealed:** the band of (W3) for stage 1: D(3) must lie within d_pred(3)·R^c(3) ± 2σ_pred·R^c(3).

## 6. Run plan (Mac mini; 1 BLAS thread; nice 10; ≥ 50% free gate + pgate; freepct_guard (pause-only); no-kill watchdog; no hard caps)
1. KA-0: W2P4 route, _098ka (minutes). If not bitwise: STOP.
2. Route W3P4 (_098) (minutes); `exp087_t0.py 3 4 <t0>` (seconds to minutes).
3. Route W6P8 (_098): estimated 3–6 core-h, < 2 GB (the k = 2 routes; the W2P8 route took 4.6 h on the Air). Then `exp087_t0.py 6 8 <t0>` (~0.5 h, < 1 GB; W8P8 took 20–24 min per flag).
4. The free sides, inside the analysis: free(3, 4, box 4), free(6, 8, box 8) (seconds).
5. `exp098_3w.py`: KA-A, plants P1 and P2, then the readings §3. Output `exp081d_results/exp098_stage0.json` and `.out`.
- New checkpoint names carry `_098` or `_098ka`, so no stored file can be overwritten. The runner STOPs if any target exists or a log tag is used.
- **Kill criteria (state + date):**
  - Good enough: exp098_stage0 printed rc 0 with KA-0, KA-A, KA-t0, P1, P2 all PASS.
  - Stop: not landed by **2026-11-30 12:00 IST**. Then report and ask the Bridge; nothing is killed.
  - The total is under 12 h, so no value gate or 25% check-in applies (those are for stage 1).

## 7. Exposure
- Known before this registration: all stored R(k) and R^c(k), k ≤ 3 (EXP-090 k = 3 accepted 2026-11-28). The seal is made knowing R^c(3); that is needed, since D_pred(3) = d_pred·R^c(3).
- No value at any of the new widths (W = 3, 6, 9) has been computed or seen.

## Amendment 1 (2026-11-28, before any stage-0 run; found while writing the code)
- **Sign typo in Plant P2 (§4).** Adding ε to S^c(W₃) changes R(W₁, W₃) by +ε·f₁₃ and R(W₃, W₂) by −ε·f₃₂, with f_ab = (1/Ny)/((1/a − 1/b)·κ(a, b)). So D moves by **+ε·(f₁₃ + f₃₂)**, not by "−ε·…" as written. The code uses the derived +ε(f₁₃ + f₃₂). The DRY on the stored k = 1, 2 values confirms it: P2 moves D by the predicted amount at both k. The tolerance is unchanged (1%).
- **Interpreters, stated:** the routes and exp087_t0 run on the project venv, as the stored routes did (Python 3.14, numpy 2.4.3). The analysis runs on the python3 that ran its DRY (3.15.2, numpy 2.5.4), where KA-A is bitwise.
- **DRY result (`exp098_3w.py DRY`, synthetic W₃ on an exact 1/W line, NOT a result):**
  - KA-A is bitwise at k = 1, 2: R_T0, R_T1, σ and κ against exp081d_results.json, and Rc against exp090_k25.json.
  - On the exact line: D = 0 to 7e-14 and R_q = R(W₁, W₂) to 9e-16.
  - P1 fires (D moves by the predicted 2.65e-8 at k = 1, 1.95e-4 at k = 2) and R_q holds (≤ 6e-14). P2 fires at the predicted size.

## Amendment 2 (2026-11-28; written 21:40 IST, Bridge GO 2026-11-28; after the stage-0 STOP, before any reading exists)
- **Grade: a post-failure plumbing amendment (a missing module).** No formula, metric, tolerance, or reading changes. Its support is KA-free, 4 of 4 bitwise on the venv (below). It is committed BEFORE the two free values are computed and before the analysis re-run.
- **What happened:** the analysis step (`exp098_3w.py S0`, on /opt/homebrew python3 3.15.2) crashed at k = 1 in `real()`, at `Rn.free(3, 4, Wbox=4)`. That interpreter has no scipy, and the free values at the new widths were not cached, so `free()` had to compute one. Exit code 1, so the runner stopped as designed. All controls that ran before the crash PASSED (KA-A at k = 1 and 2, bitwise; KA-t0 W3P4). No reading was computed or printed. No free-side cache file was written: the exception was raised before `open(f, "w")`.
- **Why the DRY missed it (my miss):** in the DRY, `synth()` replaced F(W₃) with a linear interpolation, so the `free()` compute path never ran on that interpreter. The DRY could not have caught it. The interpreter choice in amendment 1 was checked only on paths that read cached values.
- **Proposed fix (no change to any formula, metric, tolerance, or reading):**
  1. Compute the two free values free(3, 4, box 4) and free(6, 8, box 8) with `exp081b_run.free`, verbatim, on the project venv (3.14.5, numpy 2.4.3, scipy 1.17.1). That is the interpreter that made every stored free cache, and the only one with scipy.
  2. Re-run only `exp098_3w.py S0` on /opt/homebrew python3, unchanged. It now reads the cached free values, as it already does at W₁ and W₂.
- **Known-answer control for (1), already run:** `exp098_freeka.py` on the venv recomputes the four stored free values stage 0 uses (W2P4, W4P4, W4P8, W8P8) and matches all four **bitwise** (KA-free PASS, e98_freeka.out). It writes nothing into exp081b_results/.
- **Mechanism so this cannot recur (the Bridge's condition):** the re-run uses a NEW runner, `run_098s0b.sh`, a copy rather than an edit of run_098s0.sh. It runs an interpreter preflight before any stage, and STOPs if:
  - (a) PY is not the project venv or cannot import numpy and scipy;
  - (b) the analysis interpreter PYA has no scipy AND a free cache that the analysis needs (all six: k = 1 W2/W3/W4 at P = 4; k = 2 W4/W6/W8 at P = 8) is missing.
  - The preflight runs again right before the analysis stage.
  - It has a planted must-fire: PREFLIGHT_PLANT=1 adds a non-existent cache to the list, and the preflight must STOP.
- **DRY coverage is now an explicit checklist item.** The DRY's synth() path skipped free(), so the DRY did not exercise the compute path that crashed. From now on, every registration's DRY section lists each compute path the real run takes (every cache-miss branch included) and says whether the DRY runs it on the production interpreter. Any path the DRY does not run needs its own preflight or a known-answer test.
- **The Δ(W₃) = 0 question, settled from the code (the Bridge asked for this before the re-run):**
  - **Code facts. Verified by reading; line numbers are at f049c92.**
    - **The flag reaches every width.** `exp087_t0.py:10` sets the module global `S3.INNER_BETA0_087` before each `C.t0_term`. `exp081c_numerics.py:160-161` (`t0_term`) calls `S.inner_beta0(1.0, dn=True)`, which `install` does not replace: the only `inner_beta0` reference in exp081c_numerics.py is line 161. `sigma3d.py:275` reads the global at call time. Nothing in the path tests W, P, the box, or parity.
    - **The fix's only condition is in the data.** At `sigma3d.py:275`, `cl087` is built per slice by `clusters_087` (`sigma3d.py:19`): single-linkage clusters of the in-cut poles (s ≤ s_cut) with a gap < rad = 1e-5 (`sigma3d.py:261`), keeping only clusters with more than one member. The cluster branch at `sigma3d.py:279` is taken for a (p, q) pair only if slice p or slice q has such a cluster. Every other pair runs the identical OFF code.
    - **So ON == OFF bitwise exactly when no slice has an in-cut pole pair closer than 1e-5.** The stored ON and OFF are equal bitwise at both widths: −45.8640578760927 at W3P4 and −205.83158001212004 at W6P8. So the cluster branch was never taken there. A branch taken but equal to the last bit is not credible, since `_ib0_pair_087` is a different formula.
  - **Answer.** The fix is NOT inert by construction at odd or non-filling widths. It has no width condition and does reach them. It is inert there because their spectra (in the production pole lists) have no intra-slice in-cut pair with a gap below 1e-5.
    - That is correct as far as the fix goes. Isolated poles are handled by the OFF residue path, which is exact for a simple pole. EXP-087 changes only near-coincident pairs, whose separate residues are ill-conditioned.
    - Every stored nonzero Δ is at W = P = box (W8P8, W10P10, W12P12). Whether filling the box is what makes the near-doubles is **NOT settled by the code**. That is a spectral fact.
  - **What the code cannot settle, flagged BEFORE D(3) is read.** Two things decide whether Δ(W₃) = 0 is the whole story:
    - (i) near-pairs with gaps between 1e-5 and the s_KA scale, which are not EXP-087 clusters (as at W8P8 p = 8–10, line 12928 of report.md);
    - (ii) a pole that production misses (census failure mode (i), seen at W12P12).
    - Neither is tested at W3P4 or W6P8: no census exists at those geometries.
    - At W9P12 (stage 1) the census must be run, and its result stated, before D(3) is read. This goes into the stage-1 registration as a gate. For stage 0, D(1) and D(2) carry the label "Δ(W₃) = 0 from bitwise ON = OFF; no census at W₃".

## SEAL (2026-11-28, registered §5 method, verbatim; committed BEFORE free(9, 12) or any W9 value exists)
- Input: exp081d_results/exp098_stage0.json (sha256 0f8fbd478aa9c1a2…, commit f7175f2). Script: scripts/exp098_seal.py. Output: exp081d_results/exp098_SEAL.json.
- **d_pred(3) = −1.7573 ± 0.6153**, so **D_pred(3) = −20.66 ± 7.23** (R^c(3) = 11.7582).
- **The (W3) band for stage 1: D(3) ∈ [−35.13, −6.19]** (±2σ_pred).
- **q_pred(3) = −0.471 ± 1.015**, so **R_q,pred(3) = 6.22 ± 11.94.**
- **Premortem on the seal itself, stated now:**
  - The linear-in-k extrapolation is a two-point model.
  - The free side carries most of D (stage-0 decomposition), and free(9, 12) can be computed in seconds. So it is NOT computed until this seal is committed.
  - R_q is curvature-dominated at k = 1, 2 (negative), so its seal is wide and barely informative.
