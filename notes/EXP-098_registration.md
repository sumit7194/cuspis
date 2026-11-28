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
