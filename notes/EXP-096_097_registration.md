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

## Amendment 2 (2026-11-27 17:25; registered 5d203db before the run): two controls fired. Both diagnosed BEFORE any rerun; no tolerance changed
**A. EXP-096 W8P8 known answer FAILED (rc 0, 17:16; `exp096/W8P8Wb8Ny32.json`, sha 4bc71372…).**
- Route: Δ_truth = +0.0206829953. Referee (OFF@1e-6 − OFF@1e-5) = +0.0206837753. Gap **G = −7.80e-7** (route − referee); tolerance 1e-7.
- Everything else passed:
  - unconverged 0;
  - KA-complete diff −1.1e-14;
  - r-sweep 3.2e-13; M/2 ≤ 3.8e-12;
  - on the six EXP-087 clusters, mine − ON per class ≤ 2.8e-11. Two independent methods agree there.
- The route finds truth − fix = +1.395e-7, all in near-pair class p = 10 (span 1.4e-5 = 1.44·rad; the predicted singleton leak, ~1e-7 in the EXP-087 check (b)).
- **My registration's expectation** (that the referee's 9.2e-7 is the p = 10 leak) **was wrong by a factor of ~6.6.**
- **Premise I had not checked:** the referee is ONE rad point, and its own precision at W8P8 was never measured. On the W8P3 box, 1e-6 against 3e-7 agreed only to 3.4e-6 (EXP-087 registration, line 37).
- **Readings, and what tells them apart.** Define g(rad) = Σ over the 9 classes of [OFF entries in the r1 disc at rad − mine], so that g(1e-6) + rest = −G = +7.80e-7, where rest = the non-class part of the referee.
  - **H1 (referee floor at the class entries):** |g(1e-6) − 7.8e-7| ≤ 2e-7, AND g moves with rad: |g(3e-7) − g(1e-6)| ≥ 2e-7.
  - **H2 (the referee's 7.8e-7 lies outside the classes):** |g(1e-6)| ≤ 1e-7. Then rest ≈ 7.8e-7. Off-class OFF entries have no physical rad dependence: single-tag entries use stored exact residues, and there are no neighbours within 3·rad. So rest is the small-contour floor (or a cross-slice merge at 1e-2·rad), not truth.
  - **H3 (the route is wrong at the classes):** |g(1e-6) − 7.8e-7| ≤ 2e-7, AND g is stable: |g(5e-7) − g(1e-6)| ≤ 2e-8 and |g(3e-7) − g(1e-6)| ≤ 2e-8.
  - Anything else: UNCLASSIFIED, reported as such.
- **Diagnostic `scripts/exp096_diag_rad.py`:**
  - Lines from "import os" to the end of off_disc are a verbatim copy of exp096_t0_disc.py, with 3 marked edits (--rads, the output name, rad = RADX[0]), plus a verbatim pairs_of.
  - Own KA: per class, off(1e-5) must equal the stored off_r1 to ≤ 1e-12 (same platform).
  - Tier 1, W8P3 on the Air against the Air-run route (`_tier1air`): KA **PASS, max 0.0e+00**.
  - Against the Mac-stored `_tier1` it FAILS at 4.6e-10 (cross-platform, as expected). So the KA can fail.
  - The tiny-box reading (debug only): per class, OFF@1e-6 − mine ≤ 1.1e-8, and it grows to ~1.3e-7 at 3e-7.
- **The decision this feeds (the Bridge's):**
  - H1 or H2: the 1e-7 KA was set against a referee that is not good to 1e-7. Propose replacing it with the referee's measured spread.
  - H3: the route fails, and W12P12 does not run.
  - **W12P12 does not launch until the Bridge rules.**
- Run: `e96d_W8P8` on the Air (flag unset, same guards). ~1.2 h. Under 12 h, so no gate paragraph.

**B. EXP-097 control (iii) P = 6 ρ₂A FAILED (rel 5.4e-10 > TOL 1e-10, rc 1 at 16:07; STOP, W2P8 not computed).**
- ρ₂A = R₂ + ΔR^A = 1.35581 − 1.33477 = 0.02103. This cancellation amplifies relative error by (|R₂| + |ΔR^A|)/|ρ₂A| = 127.9.
- R₂ itself passed at 8.3e-12 relative, which is 1.125e-11 absolute. Propagated: 1.125e-11 / 0.02103 = **5.38e-10, the observed value**.
- To pass, R₂ would have had to agree to 1.55e-12, tighter than the cross-platform 5.7e-11 the TOL was set from. The check could not pass across platforms for a cancelled quantity. It fired on the tolerance's design, not on the computation.
- Every input control passed: R₂ 8.3e-12, ΔR^A 5.2e-14, ΔR^bulk 5.8e-14, G₂b 6.6e-14, and all QA ≤ 1.8e-12.
- Effect on the target: f₂ uses ρ₂A differences over a G₂b drop ~0.16. An absolute 1e-11 is 1e-10 of f₂. Nil.
- **Proposed (needs the Bridge's GO; NOT applied):** for the derived rows (ρ₂A, G₂b), use the propagated tolerance TOL·(|x| + |y|)/|x + y| from their two inputs; keep 1e-10 on every input row. Then rerun EXP-097 unchanged otherwise (minutes).
- I do not rerun before the GO. The failed run is kept (`air_pull_096/e97_P8.out`, sha 70712b52…).

## Amendment 3 (2026-11-27 ~17:50; Bridge ruling on amendment 2; before the diagnostic lands and before any W2P8 value)
**Honest misses (recorded):**
- **EXP-096:** I expected the referee's 9.2e-7 (truth − fix at W8P8) to be the p = 10 singleton leak. The route measures that leak at 1.395e-7. **Out by ~6.6×.**
- **EXP-097, my message to the Bridge:** I wrote "8.3e-12 × 128 = 5.38e-10". **Wrong arithmetic** (that product is 1.06e-9).
  - The observed value is R₂'s input error alone, propagated with the factor |R₂|/|ρ₂A| = 64.46: 8.3e-12 × 64.46 = 5.35e-10 (printed as 5.4e-10).
  - The worst-case first-order bound factor is (|R₂| + |ΔR^A|)/|ρ₂A| = **127.92**, from the stored inputs. The Bridge quoted 128.1.
  - Amendment 2's own route (1.125e-11 absolute / 0.02103) was right. Its "127.9" is the bound, not the observed factor.
- **Amendment 2's header time:** first written as 17:45; corrected to 17:25 (the Air clock showed the diagnostic launched at 17:27).

**EXP-096 e96d: what each reading decides** (the Bridge rules when it lands):
- **H1 (referee floor at the clusters):** the 1e-7 W8P8 known answer could never have passed with a single-rad referee. It is replaced by a referee whose precision is MEASURED (a rad sweep with a stated spread), not waived.
- **H2 (referee error outside the clusters):** the same. The region is named as "OFF entries outside the 9 class discs".
  - This diagnostic cannot localise it further.
  - A per-slice whole-sum rad sweep would be a follow-up, registered separately if wanted.
- **H3 (route wrong at the clusters):** W12P12 stays held, and any EXP-095 / EXP-097 input that uses the route is re-read. (Today none does: EXP-097 uses no t0, and EXP-095 is sealed and uses the stored fix.)

**EXP-097 control (iii) (Bridge GO, with conditions):**
- **(a) As written, control (iii) FAILED on the first run:**
  - verbatim line: `(iii) P=6 rho2A vs exp094_result.json   FAIL  rel 5.4e-10` (e97_P8, rc 1, 16:07:44; kept in `air_pull_096/e97_P8.out`, sha 70712b52…);
  - the new rule below is a **correction of the control's design**, derived from first-order error propagation. It is method-derived, not tuned;
  - the as-written verdict is still printed, as an INFO line, on every run.
- **(b) Input rows** R₂, ΔR^A, ΔR^bulk stay at TOL = 1e-10 and remain the controlling check.
  - R₂ = −½(Q₂ − Q₄)·norm is itself a difference of two QA values, but it stays an input row at 1e-10.
  - The derived-row check catches errors in the COMBINATION step (sign, a missing or extra term, the pairing). Those are O(1).
  - **Plant (vii):** in a copy of each P = 4 / 6 row, flip the sign of ΔR^A. Each derived row must then FAIL its tolerance. Predicted from the stored values:
    - ρ₂A: rel 9.55 at P = 4, 127 at P = 6;
    - G₂b: rel 1.12 at P = 4, 3.30 at P = 6;
    - against tolerances ≤ 1.3e-8.
- **(c) The derived rows, all of them:** ρ₂A = R₂ + ΔR^A and G₂b = ΔR^A − ΔR^bulk, at P = 4 and P = 6. No other row is controlled as derived. Tolerance = TOL × (|x| + |y|)/|x ± y| from the stored exp094 inputs:
  - P = 4: ρ₂A 1.055e-9 (amp 10.55); G₂b 2.12e-10 (amp 2.12).
  - P = 6: ρ₂A 1.279e-8 (amp 127.92); G₂b 4.30e-10 (amp 4.30).
- **(d) At P = 8, report the amplification factor of every combination:**
  - R₂ (from the two QA values), ρ₂A, G₂b;
  - both G₂b drops (6→8, 4→8), and both ρ₂A numerators.
  - FLAG any factor above 1e4 to the Bridge (inform, not a stop).
- **Then rerun EXP-097 unchanged otherwise:**
  - the stale guard holds (the Air's exp097/ is empty; the first run wrote nothing);
  - code: `scripts/exp097_run.py`, with the (iii) block, (vii) and (d) marked "amendment 3".

## Amendment 4 (2026-11-27 18:30, registered 1ca4cb9 before the production scan; Bridge ruling on e96d: scan, then W12P12 with a gate paragraph, and a whole-sum referee sweep)
**Order and memory:**
- The Air has **8 GB**. The worst-case sum of pilot peaks is W12P12 3.24 + sweep ~1.05 (the Mac referee figure) + the 095b route up to its 3.06 hold = 7.35 GB. That is over the 6.4 GB the < 20 % pause allows, so the sweep does NOT run alongside W12P12.
- Order (the Bridge's fallback): (1) the scan; (2) the sweep; (3) W12P12 after the sweep lands. If the scan FIRES, report to the Bridge before (3).

**Step 1: pole-list scan, `scripts/exp096_scan.py W P`.**
- Pole lists only, no install: `Slice.poles()` fixes them at construction, reading CUSPIS_081E at import; the install only iterates over them.
- Run at W8P8 (flag unset) and W12P12 (CUSPIS_081E=1), as the stored runs.
- **FIRE, then report before W12P12:**
  - S1: any pole s ≤ 1e-5 (the 1e-5 contour around ±i s would enclose the kernel's pole at α = 0);
  - S2: any cross-slice pole gap < 1e-6 (the 1e-2·rad merge threshold is 1e-7 at 1e-5 and 1e-8 at 1e-6).
- Reported, no fire:
  - S3: the same-slice classes at gap < 1e-4. **KA:** they must reproduce the route's class lists (9 at W8P8; 11 at W12P12, p = 6–16).
  - S4: the count of two-tag entries outside vs inside the classes.
- **Plant (must fire):** add s = 5e-6 to one list and a cross copy at +5e-8 to another; both S1 and S2 must fire. Tier 1 (W4P4, Air): CLEAR, plant PASS, 0.6 s.

**Step 2: whole-sum referee sweep at W8P8, `scripts/exp096_refsweep.py 8 8`.**
- Code: the diag code verbatim except the output name.
- Computed:
  - whole OFF t0 at rad 1e-6, 2e-6, 5e-7;
  - class OFF_d at 1e-6 and 2e-6 (5e-7 from the diagrad JSON);
  - out(rad) = whole − Σ class OFF_d (the part outside the 9 discs).
- **KAs:**
  - KA-1: class OFF_d(1e-6) bitwise against the diagrad JSON;
  - KA-2: whole OFF(1e-6) equals the Mac referee −209.27942615304573 to ≤ 2.1e-8 (1e-10 × 209.3, the cross-platform TOL).
  - Tier 1 (W8P3, Air, 266 s): KA-1 PASS bitwise, and KA-2 FAILS (wrong geometry, by design), so both can fail.
- **Readings** (d1 = out(2e-6) − out(1e-6), d2 = out(5e-7) − out(1e-6)):
  - **R-real:** |d2| ≤ 1e-7. The outside part is stable below 1e-6, so the 7.8e-7 is a real rad dependence of production t0 outside the clusters. d1 locates the step above or below 2e-6.
  - **R-noise:** |d2| ≥ 3e-7. The whole-sum referee is noise-limited at that level, and the 7.8e-7 is not a measured truth.
  - Otherwise: **UNCLASSIFIED.**
- ~2 h on the Air (3 whole t0 at ~30 min + 2 class passes at ~12 min). Under 12 h, so no gate paragraph.
- **Correction to my e96d message (an honest miss):** I wrote that the per-class floor "would need hundreds of times more entries" to reach 7.8e-7, so noise was "not the obvious answer". The Tier-1 sweep (W8P3; debug, not a target) shows the outside part moving **−8.9e-7 between 1e-6 and 5e-7**, while each class moves ~1e-8. Outside entries can carry a far larger floor than the clusters. That inference was wrong at W8P3; W8P8 is decided by the sweep.
- Until the sweep lands, **W12P12's R(2) carries an unquantified outside-entry term** (STATUS.md). Its reading is folded into W12P12's 25 % check-in.

**Step 3: W12P12. Gate paragraph (the run is over 12 h):**
- **What it decides:** whether the EXP-087 fix's Δt0(W12P12) = +0.06394052643 is right at the cluster level (EXACT / PASS / FAIL against τ_num and δ_mat). That sets whether every k = 3 reading carries the fix or Δt0(truth).
- **Pilot cost, and the projection:**
  - W8P8 on the Air: 430 s per class, 0.56 GB.
  - W12P12 probe: install 4111 s (Air crowded), 3.24 GB true peak.
  - Scaled per class: × 1.5 (Ny 48/32) × 11.4 (N 864/384, cubed for G) ≈ 2.0 h. With 11 classes (p = 6–16) plus install ≈ **23.5 h**.
  - Outside-view overrun from our own record: × 2 (the W12P12 install took 4.8× the M4; memory came out 1.9× my estimate). That gives **47 h ≈ 2.0 days of one core**, under the 3-day line, so no referral to Sumit.
  - Memory: 3.24 GB true (install), plus ~0.15 GB G cache.
- **Premortem:**
  - (i) a real outside-entry rad dependence at W12P12, which the cluster route cannot see (steps 1–2 test this first);
  - (ii) pauses from 095b memory on the 8 GB Air (pause-only: a delay, not a loss; per-class JSON checkpoints).
- **Dependencies:** the scan CLEAR; the sweep landed; the 095b route shares the Air.
- **Stop rule:**
  - `--budget-h 47` (2× the estimate): a checkpoint stop at a class boundary, then re-gate with the Bridge;
  - the 25 % check-in at ~12 h, with the sweep reading folded in;
  - **kill date: not graded by 2026-11-30 12:00**: report what exists and stop.
- Launch: `air_run_096.sh e96_W12P12 1 exp096_t0_disc.py 12 12 --budget-h 47`, one process. The launch note confirms the first-class projection.

## Amendment 5 (2026-11-27 ~18:55; the Bridge's no-hard-caps check, before the W12P12 launch)
- **Found:** the amendment-1 budget gate ended the run (`sys.exit(4)`), and the code had no resume path. A restart would redo the install (~1 h at W12P12) and every class. That is a job-ending cap, against the no-hard-caps rule.
- **Changed to pause + alert:**
  - At a class boundary where the projection exceeds the budget, the run writes its partial per-class JSON, logs `GATE PAUSE …`, and waits, alive, with its install held, for `exp081d_results/exp096/{name}.resume`. A "still waiting (N h)" line is logged each hour.
  - The file's content is the new budget in hours; an empty file means no further gate.
  - Then `GATE RESUME`, and the run continues from the next class.
  - Paused seconds are kept out of later projections.
- No computation changed. These are the only edits to `scripts/exp096_t0_disc.py`.
- **Tier 1 (W8P3 on the Air, `--budget-h 1e-6`, tag `_tier1pz`):**
  - it paused after class 1, alive at +70 s;
  - an empty resume file gave RESUME after 120 s, budget inf;
  - rc 0, and all 5 classes are **bitwise equal** to the unpaused `_tier1air`;
  - the post-resume projections show 17–19 s per class (the pause is excluded).
- **The alert path for W12P12:** my watcher greps `GATE PAUSE` in e96_W12P12.out and reports to the Bridge. The Bridge (or Sumit) gives the new budget, and I write it into the resume file.

## Amendment 6 (2026-11-28 ~07:00, Bridge ruling on the W12P12 KA-complete failure; registered BEFORE any run; nothing computed yet)
**Context.** W12P12 (304ecd9): D = +1.28e-9, EXACT by rule; KA-complete FAILED AS WRITTEN: Σ_classes(ON_d − OFF_d) (Air, M1) − stored t0(ON) − t0(OFF) (Mac mini, M4) = −7.84e-7. Candidates: (a) cross-chip; (b) a missed entry or copy defect. Bridge rulings: run the discriminating test on the Mac after W6P12 lands; add a must-fail; localise the residual per class; state a falsifiable check for the 7.84e-7 (W12P12) vs 7.80e-7 (W8P8) match. The k = 3 readings carry the fix, partially verified, with |7.8e-7| in t0 as an explicit systematic, dropped only if this amendment resolves it.

**Code:** `scripts/exp096_onoff.py` — a VERBATIM copy of exp096_t0_disc.py lines 1–162 (args, install, class detection, off_disc, on_disc, pairs_of), plus edits marked "# A6": (1) the name tag `_onoff`; (2) the Strip3D build is split from the install so step A is written before the install; (3) a tail that runs the od/on block of run_class verbatim for every class (no "mine"), with per-pair recording for the plant. Runner `scripts/run_096a6.sh` (Mac mini).

**Step A (pole lists, no install).** Class members built on the Mac versus the Air's (`exp096/W12P12Wb12Ny48.json`). Report max |member diff| and span differences per class. "Same" if the class lists match and max |diff| ≤ 1e-12; otherwise "DIFFER".
- **Change from the ruling's conditional (stated, with the reason):** step B runs whether or not step A differs. (1) The per-class localisation you asked for needs one-chip class values, because the stored totals have no per-class breakdown. (2) Identical pole lists would not exclude a cross-chip difference in the install (residues Rfull, G, B1). Say if you want B conditional instead; the runner starts only after W6P12 lands.

**Step B (one install on the Mac).** Per class, ON_d and OFF_d at r1 (the same disc and entries as the route).
- **KA-complete-1chip** = Σ_Mac(ON_d − OFF_d) − stored t0(ON) − t0(OFF).
- **Localisation:** per class, (ON_d − OFF_d)_Mac − (ON_d − OFF_d)_Air, plus ON_d and OFF_d separately (Mac − Air); their sum is reported against −7.84e-7.

**Readings (falsifiable; decided by these lines only):**
- **R-a (cross-chip):** |KA-complete-1chip| ≤ 1e-8. Candidate (a) holds; the systematic term is dropped from the k = 3 budget, and the reason stated.
- **R-b (chip-independent):** |KA-complete-1chip − (−7.84e-7)| ≤ 1e-8, i.e. the Mac reproduces the Air residual. Candidate (b), or a fixed term in the ON/OFF bookkeeping; the systematic stays; next step to the Bridge.
- Otherwise **UNCLASSIFIED**: the systematic stays, and the localisation table goes to the Bridge.

**The 7.84e-7 / 7.80e-7 match: falsifiable check.**
- **H-fixed** (one chip-independent term common to both geometries) predicts R-b at W12P12: the Mac residual is −7.8e-7 to ≤ 1e-8.
  - It is already strained at W8P8. There the same comparison on one chip (the Air's own whole OFF at 1e-6 minus 1e-5, e96s) gives −2.7e-7, not +7.8e-7; the W8P8 gap moved by 1.05e-6 with the chip.
  - So **R-a at W12P12 falsifies H-fixed outright**: neither number would then be chip-invariant.
- **H-common-cross-chip** (both are the same cross-chip component) predicts R-a, plus a W12P12 Mac − Air difference concentrated where W8P8's lived. W8P8's lived OUTSIDE the class discs (e96d: on the clusters the referee matched to ~1e-9). So if the W12P12 Mac − Air difference sits INSIDE the classes (the localisation table sums to −7.8e-7 over the 11 classes), the two are different components, and the size match is a coincidence. That is decided by the table, not by me.

**Controls (each can fail):**
- **Known-answer control first (Mac, W8P8, flag unset; ~1 GB, minutes):** the same script must give KA-complete-1chip ≤ 1e-8 there, where the cross-chip KA-complete already closed to 1.1e-14. If it fails, STOP and tell the Bridge; W12P12 does not start.
- **Must-fail plant (at both geometries):** in class p = 16, disc +i c, the FIRST pair in pairs_of order has its ON entry replaced by its OFF entry. The planted sum must move KA-complete-1chip by > 1e-8. The pair is fixed here, before any run, not picked. If its own |ON − OFF| ≤ 1e-8, the plant cannot fire; it is then reported as FAILED, and no other pair is substituted.
- Gate: unconverged 0; step A's class list must be 11 classes (p = 6–16) at W12P12 and 9 (p = 8–16) at W8P8.

**Run plan (Mac mini, after `run_w6p12.done`; one core, replacing W6P12's one for one):**
- `run_096a6.sh`: wait for run_w6p12.done; if W6P12 STOPs, do not start.
- Gate free ≥ 50% plus pgate; freepct_guard (pause-only); no-kill watchdog.
- e96a6_W8P8 (control) first, then e96a6_W12P12 with CUSPIS_081E=1.
- **Cost estimate:** W12P12 install ~15 min on the M4 (the e87 install took 861 s), plus 11 classes of OFF/ON only (~2–3% of the route's G evaluations) ≈ 30–60 min; peak ~3.8 GB. Beside DeepStrain (2–5 GB) on 16 GB: worst case ~9 GB, under the 50% gate.
- **Kill criteria:**
  - Good enough: the W12P12 READING line is printed rc 0 with both controls PASS.
  - Stop: not landed by 2026-11-28 18:00. Then report and ask the Bridge; nothing is killed: the guard pauses only, and the run is left paused or running for the Bridge to decide.
- **No k = 3 reading starts before this lands, unless the Bridge says so**; if it is delayed, the readings carry the systematic term (Bridge ruling).
