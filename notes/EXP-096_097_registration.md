# EXP-096 and EXP-097 REGISTRATION (2026-11-27 ~16:00; nothing computed at a target geometry) [model: Opus 5.5]

*Bridge GO 2026-11-27 (item 1 and item 2 of the spare-core proposal, under Sumit's "use the spare resources while we wait").*
*Both are on the Air (the Mac mini is at 33 % free, next to W6P12's 30 % pause line; nothing new goes there).*
*Neither opens a seal:*
- EXP-096 uses only pole data and the already opened Δt0 numbers.
- EXP-097 is n = 2 at P = 8, which is not part of EXP-095 (n = 1, P = 10) or the k = 3 readings.

## EXP-096: an independent truth for the EXP-087 t0 cluster correction at W12P12

**Why.**
- Δt0(W12P12) = t0(ON) − t0(OFF) = **+0.06394052643** (`exp087_t0_W12P12.json`) is the largest single correction inside R(3), and nothing referees it.
- At W8P8 the referee was the rad = 1e-6 sweep. At W12P12 that cannot work: the B-doublet gaps are 1.8e-8 to 5.6e-8 (`notes/EXP-087_tinybox/b_art_prod.txt`), below the ~5e-8 contour floor.

**Quantity.** Write t0 as a sum over pairs (k, p), with q = (k − p) mod Ny:
- t0 = Σ_k Tr(B1_k⁻¹ dB0_k), with dB0 from `inner_beta0(1, dn=True)`.
- Each pair term is a sum over pole entries a0 of 2πi·Res_{a0}[2 G_p(α) ∘ G_q(−α) ker(α)] / Ny.

**Method (`scripts/exp096_t0_disc.py`): a WIDE-disc contour.**
- **Classes (my own detection, not `clusters_087`):** per unique slice, single linkage of the in-cut poles at gap < 1e-4.
  - Every multi-member group is a class X, with centre c_X (the mean) and half-span h_X.
  - This covers every EXP-087 cluster (gap < rad = 1e-5; asserted) and also the near-pairs with gaps in [1e-5, 1e-4), which the fix treats as singletons.
- **Disc radius:**
  - d_X = distance from c_X to the nearest non-member pole of ANY slice;
  - r1 = min(1e-3, d_X/3) and r2 = r1/3;
  - REFUSE if r2 < 10·h_X. For the trapezoid rule this is a ratio ≤ 0.1, so the error is ≤ 1e-32 at M = 32.
- **The route (no residues, no pole positions inside the disc, no rad, no cluster bookkeeping):**
  - For every pair with p or q in X's mirror class, and for both discs (α = ±i c_X), the entries inside the disc are replaced by ONE M = 32 trapezoid contour of the full integrand on |α − (±i c_X)| = r.
  - G is the production `ExactSlice` G (refined), evaluated at least 2r/3 from any pole.
- **The same disc's production entries, for comparison:**
  - OFF_d is a copy of the `inner_beta0` pair loop; ON_d is a copy of `_ib0_pair_087`.
  - Each copy has ONE added filter line (`|a0 − centre| < r`).
  - Pairs without an EXP-087 cluster use ON_d = OFF_d, as production does.
- **Quantities:**
  - Δ_truth = Σ(mine − OFF_d);
  - **D = Σ(mine − ON_d) = truth − fix**, split into EXP-087 clusters and other near-pairs.

**Controls (all can fail):**
- **KA-complete:** Σ(ON_d − OFF_d) = the stored t0(ON) − t0(OFF) to ≤ 1e-8. This fails if a cluster entry is missed or a copy is wrong.
- **Known answer at W8P8, the only geometry with a referee truth:**
  - |Δ_truth − (OFF@1e-6 − OFF@1e-5)| ≤ 1e-7, against the referee's +0.020683775 (`exp087_referee_W8P8.json`).
  - The fix itself missed it by 9.2e-7, so this control tells this route apart from the fix.
- **Nuisance sweeps:** r1 against r2 = r1/3, and M = 32 against its own M = 16 half grid. Both drifts are reported; they set τ_num.
- **Must-fail plant (`--plant`):** every disc centre is shifted by 3·r1 (it encloses no pole). The route must then lose the cluster (mine → ~0).
- **Gate:** the unconverged G-evaluation count is 0.

**Tolerances (derived):**
- **τ_num** = 3·max(r-sweep drift, M/2 drift) + 1e-8 (the KA-complete floor).
- **δ_mat:**
  - An error D moves R(3) by ½·D·norm(3).
  - The narrowest sealed k = 3 half-width I hold is 0.08: R(t0+L)(3) "corrected" +0.33 [0.25, 0.42], ca63760.
  - An error worth 1/10 of that (0.008 in R) can flip no sealed grade unless the value sits within 0.008 of an edge.
  - So **δ_mat = 0.008 / (½·norm(3)) = 1.07e-3**, with norm(3) ≤ 15. That bound is inference from norm(2) = 14.0900 and norm(2.5) = 14.3120; norm(3) is not opened. At the W6P12 landing it is re-graded with the actual norm(3).

**GRADE (W12P12, primary):**
- **EXACT** if |D| ≤ τ_num;
- **PASS** (fix adequate for k = 3) if |D| ≤ δ_mat;
- **FAIL** otherwise. The k = 3 reading would then carry Δ_truth, and the Bridge decides.

**Secondary, reported:**
- W10P10, under the same rule, with norm(2.5) = 14.3120. Δ_fix = +0.121780 has no truth today.
- W8P8 is the known-answer control.

**Expectation, stated before the run.**
- Tier 1 (below) found the fix exact on clusters to ~1e-11.
- It also found the singleton leak at a near-pair with gap 1.4·rad to be 5.9e-7. This is the same size as W8P8's truth − fix of 9.2e-7, where slice 10 is a singleton at 1.44·rad. So I expect the W8P8 9.2e-7 to be that leak, not a cluster error, and the W8P8 KA to pass.
- At W12P12 the only near-pair singleton is at 2.63·rad. Its leak is ~(1/2.63)³² × term ≈ 1e-14.
- **Predicted: EXACT, |D| ≲ 1e-9.**
- Ways it could still fail:
  - the B-doublet residues taken at radius 0.3 × gap (5e-9 to 2e-8) are inaccurate in the fix's single-tag sum;
  - or an entry is mis-merged.
- Largest possible |D|: the B part, ~0.14.

**Tier 1 (debug run BEFORE this registration; a known answer, not a target):**
- Tiny box W8P3, Wb 8, Ny 16, 32 s, 75 MB.
- The first try refused one class under a 20·h margin rule; it was relaxed to 10·h, the trapezoid bound above.
- Result:
  - Δ_truth = +0.01767727, against the radius-sweep truth +0.0176769 (rad 1e-6) / +0.0176803 (3e-7);
  - mine − ON per EXP-087 cluster: −1.1e-11, +3.4e-11, −2.3e-11;
  - near-pair (gap 1.4e-5): +5.9e-7;
  - r-sweep and M/2 drifts ~1e-13;
  - plant: mine → 1e-15 per class (lost the clusters, as it must).

**Order:**
1. Probe W12P12 on the Air: install + B1, the time per G evaluation, and 2 contour points of one class. Measure the footprint.
2. W8P8 KA.
3. W12P12 split by class into ≤ 3 processes, as the probe allows.
4. Grade (`scripts/exp096_grade.py`).
5. W10P10 if time allows.

**Air operations:**
- folder ~/GitHub/fleet-air/corner_function_096, with a sha256 manifest of the import closure compared on both sides;
- nice 10; no-kill watchdog;
- freepct_guard PID-scoped with pause < 20 % / resume ≥ 30 % (Bridge, Sumit's note);
- no caps.

## EXP-097: the EXP-094 n = 2 wall test one wall further (P = 8), DESCRIPTIVE

**Why.**
- EXP-094 (4 → 6) was INCONCLUSIVE by a hair: drop 0.19948 against 0.20169.
- The question is whether the A fraction is the same at every n. That is the open A-vs-bulk item.

**Quantities.** These are EXP-094's, unchanged (`scripts/exp097_run.py`, with EXP-094's phase 1 and dRs verbatim):
- R₂^(P) = −½[Q₂(W2P) − Q₂(W4P)]·norm_P;
- ΔR₂^A = Ny·[Σ c_A σ₂(W2) − Σ c_A σ₂(W4)]·norm_P;
- ΔR₂^bulk = Ny·c_hi·[Σσ₂(W2) − Σσ₂(W4)]·norm_P;
- ρ₂A = R₂ + ΔR₂^A; G₂b = ΔR₂^A − ΔR₂^bulk.

**Inputs at P = 8:**
- norm₈ = `exp093_p1.json` r8 norm;
- c_A from G_W2P8 / G_W4P8 (EXP-093);
- W2P8 Q₂ and σ₂ are FRESH (blind);
- W4P8 Q₂ is recomputed, and must equal the stored `exp084/Q_W4P8b8.json` (EXP-084).

**Two readings, both DESCRIPTIVE (no sealed band; there is no Fable seal this week):**
- **Step 6 → 8:** f₂ = −[ρ₂A(8) − ρ₂A(6)] / [G₂b(6) − G₂b(8)]. **INCONCLUSIVE** if the drop < 0.2·G₂b(6) = 0.16180.
- **Span 4 → 8:** f₂ = −[ρ₂A(8) − ρ₂A(4)] / [G₂b(4) − G₂b(8)]. **INCONCLUSIVE** if the drop < 0.2·G₂b(4) = 0.20169.
- An INCONCLUSIVE is accepted as the result (Bridge).
- **Reported beside them, also descriptive:** n = 1 f(4→6) 0.212, f(6→8) 0.2314, f(4→8) from the stored rows; n = 2 f₂(4→6) 0.487 (INCONCLUSIVE).
- **Expectation:** the n = 2 G₂b drop was ~20 % per step. So 6 → 8 is likely INCONCLUSIVE, and 4 → 8 likely conclusive.

**Controls (stop before W2P8 if any fails).** TOL = 1e-10 relative, the cross-platform level (Air against Mac: 5.7e-11 in the EXP-093 identity). Bitwise agreement is reported.
- (i) phase 1 at W{2,4}P4 and W{2,4}P6 reproduces the stored Q QA (n = 2, 3), and saddle(2) at P = 6 reproduces `exp094_sigma2`;
- (ii) phase 1 at W4P8 reproduces the stored `Q_W4P8b8` (n = 2, 3): the KA at the target P;
- (iii) the P = 4 and P = 6 rows (R₂, ΔR^A, ΔR^bulk, ρ₂A, G₂b) reproduce `exp094_result.json`;
- (iv) two-path |QA − QB|/|QA| ≤ 1e-9 at W2P8 and W4P8;
- (v) stale-file guard: the exp097/Q files are absent before the run;
- (vi) plant: σ₂(W2P8) × 1.01 must move ΔR^A(8) by > 1e-3 relative.

**Footprint.** Minutes; W2P6 took 3–4 s, and P = 8 should be under 1 GB. One process on the Air, same guards.

## Amendment 0 (2026-11-27 14:45, before any target run; the operational settings are those of the stored runs)
- **CUSPIS_081E:**
  - W12P12 runs with **CUSPIS_081E=1**, as `run_087w12.sh`, which stored t0(OFF) / t0(ON). The 081e filter recovers poles at W12P12 p = 7 and 10, so the pole lists depend on it.
  - W8P8, W10P10 and EXP-097 leave it **unset** (the k ≤ 2.5 convention). The 081e filter changes no pole list at W8P8 or W10P10 (report.md, the 081e reciprocal-filter table).
  - KA-complete would fire on a mismatch.
- **Air folder:** ~/GitHub/fleet-air/corner_function_096/scripts, with the runner `scripts/air_run_096.sh`. Its sha256 manifest (35 files: closure + inputs) is identical on both sides (14:44).
- **Probe launched 14:45:** `e96_probe_W12P12`, runner PID 49011, PPID 1, freepct_guard 49018 (pause < 20 % / resume ≥ 30 %).

## Amendment 1 (2026-11-27 16:10, after the W12P12 probe refused; no target number was produced)
- **Probe result (e96_probe_W12P12, rc 3, 15:58:36):**
  - Install + B1 took **4111 s on the Air**, against 861 s on the M4. The Air was crowded then, with W2P10 still running.
  - Peak **3.24 GB true** (phys_footprint; 2.5 GB of it compressed).
  - It then REFUSED class p = 6, a near-pair with gap 8.3e-5. That is below gdet = 1e-4, NOT an EXP-087 cluster (8.3·rad; the fix treats it as a singleton). With r1 = 1e-3, r2 = r1/3 = 3.3e-4 is below 10·h = 4.2e-4.
  - The check was right; the rule was rigid for wide near-pairs.
- **Change 1:** r2 = max(r1/3, 10·h). REFUSE only if r2 > r1/1.5 (the r-sweep must still span ≥ 1.5×).
  - The trapezoid bound is unchanged (inner ratio ≤ 0.1).
  - Classes with 10·h ≤ r1/3 are unchanged. Re-run Tier 1 W8P3 is **bitwise identical** to the committed one.
- **Change 2:** `--budget-h 12`. After each class, the projection is install + (mean class time) × classes. If it exceeds 12 h, the run stops at that class boundary (a checkpoint stop; partial per-class JSON kept), and a gate paragraph goes to the Bridge before any continuation (fleet practice 2026-11-27, rule 1).
- **Order, revised:**
  1. W8P8 known answer FIRST (before the expensive run; ~0.5 GB);
  2. EXP-097 (minutes);
  3. W12P12 as ONE process with all classes (the Air's memory allows one 3.2 GB job beside the 095b route; the Mac mini is excluded, at 33 % free).
- **The registered per-class "2-point probe" is replaced** by the first class of the full run. That run's projection line gives the time; its watchdog peak gives the memory.
