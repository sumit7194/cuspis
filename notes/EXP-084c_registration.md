# EXP-084c REGISTRATION: does the production continuation equal the honest family at integer n, at the 084 geometries?

*Registered 2026-11-23 (Bridge accepted with two additions), after 084b ("c(1) non-zero"; meaning unestablished) and the Bridge's C2 conflict note. Before n = 5. Alone, no-kill;
cost measured progressively (route (ii) at P ≤ 10 is unmeasured). [model: Opus 5.5]*

## A. Question and premises
- 084b's pre-stated meaning needs (P1) R_n smooth in n on [1, 2] and (P2) the continuation ≠ the honest family at integers.
- EXP-083 R3′ C2 (W2P2, W4P2; n = 1..24) found route (ii) with the continued saddle, Q_cont^sad(n), equal to the honest arm (b) to ~1e-10, and failed by 4.7e-10 at W4P4 (cause unidentified). That is evidence against P2 at P = 2.
- 084c tests P2 directly at the 084 geometries: (W₁, W₂) = (2k, 4k), P = box = 4k, k ∈ {1, 1.5, 2, 2.5}, n ∈ {2, 3, 4}.
- The chain: production Q′(1) ↔ route (ii) (EXP-083 C1 linked production T_sad to route (ii)'s n-derivative) ↔ honest Q_n (this test).

## B. Measurement
- Q_cont^sad(n) by `exp083_armb_c2.py`'s route-(ii) construction (QCont on strip_sigma(g, σ_n); npt 120 / 512; Mx 48, Mt 160, tmax 8; strip_sigma alias = False).
- The honest Q_n is REUSED from 084 / 084b (float64, known answer 4e-13).
- Arm (a) chain: route (ii) at σ = 0 against honest arm (a), needed for C2's tolerance rule.

## C. Two-level reading (pre-stated)
**Level 1 (C2's registered rule, exactness):** |Q_cont^sad(n) − Q_n^honest| ≤ max(3·dev_a(n), 1e-10), with dev_a from the arm-(a) chain at the same geometry.

**Level 2 (relevance to 084b):** convert the discrepancy to R units, ΔR_n(k) = −(½/(n−1))·[Δ(W₁) − Δ(W₂)]·norm(k), using the 084 normalisation and stored κ.
- "AGREE-relevant" iff max |ΔR_n(k)| ≤ 0.01 over all k and n. That is ≥ 100× below the O(1) gap between 084b's per-k n → 1 extrapolants and the continued R.

| outcome | condition | meaning |
|---|---|---|
| **agree** | Level 2 AGREE (Level 1 reported) | the continuation equals the honest family at integers, to the precision relevant here, so P2 is false. 084b's "non-zero" then reflects (i) the c/d degeneracy or (ii) non-smooth n-dependence, NOT a wrong continuation |
| **disagree** | Level 2 fails at some (k, n) | the continuation is implicated directly, with no extrapolation needed |
| INCONCLUSIVE | the route (ii) construction cannot be run at some geometry (cost or convergence) | — |

- Level 1 failures with Level 2 agreement are reported as "exactness residual (cf. W4P4)" and do not change the reading.

## D. Controls (C2's, kept)
| row | check | expected |
|---|---|---|
| plant σ = 0 | route (ii) at σ = 0 against honest arm (b) | Level 2 must FAIL (the saddle matters at R scale) |
| plant σ_n × (1 + 1e-6) | at n = 2, 3 | Level 1 must fire (exactness has teeth) |
| KA | route (ii) at W2P2, n = 2 reproduces the stored EXP-083 C2 value | ≤ 1e-12 |
| reuse check | honest Q_n read from 084 / 084b files equals the stored registered values | bitwise |

## E. Cost
- Unmeasured at P = 4…10.
- A dry run at k = 1 (W2P4b4) and n = 2 is run first, alone, after the 085 rerun. Larger k follow only with measured peaks.
- If route (ii) at k = 2.5 proves too costly, the reading uses k ∈ {1, 1.5, 2}, and that limitation is stated.

## F. Additions at registration (Bridge)
1. **Sized Level-2 plants** (the σ = 0 plant shows Level 2 can fail, but not at the decision scale). The honest Q_n(W₁) at each (k, n) is perturbed by δQ = −ΔR_target·2(n − 1)/norm(k), with norm(k) from the stored κ (the 084 code path), so that R_n(k) moves by exactly ΔR_target.
   - **ΔR_target = 0.05 (5× the threshold): MUST FAIL Level 2.** This is unconditional whenever the unplanted max|ΔR| < 0.04.
   - **ΔR_target = 0.002 (⅕ of the threshold): must PASS Level 2 conditionally,** i.e. it is a valid check only if the unplanted comparison agrees to ≤ 0.008. If the unplanted |ΔR| is already > 0.008, the outcome is reported, not graded: it would then reflect the real difference, not the machinery. Derived on paper before registration.
2. **Normalisation:** ΔQ → ΔR_n goes through the SAME function and stored κ / geometry inputs as 084/084b, with no typed constants.
   - **Planted normalisation test:** ΔQ(W₁) = 1 at k = 2, n = 2 must give ΔR = −½·norm(2), where the test computes norm(2) independently as 1/(Ny·(1/W₁ − 1/W₂)·κ_stored(2)) at run time and compares to the function's output to 1e-12.

## Amendment 1 (POST-FIRING, per the Bridge's ruling 2026-11-23): KA redefined after its cause was SHOWN
- **Fired:** KA, production route (ii) W2P2 n = 2 = 0.3029743825630957 against the stored C2 value 0.3029743823472364 (2.2e-10 > 1e-12).
- **Cause shown:** the stored value was computed on the ALIASED path (the pre-slip-15 default; b0792ed at 09:20 precedes the alias=False switch, 1b8cf34 at 12:01). `exp084c_run.py KA_ALIAS` on the aliased path reproduces it **BITWISE** (0.3029743823472364, difference 0).
- **KA, redefined:**
  - Line 1: the stored value on the SAME aliased path to 1e-12. **PASS (bitwise).**
  - Line 2: production (alias=False) route (ii) against honest Arb Q(2) = 0.3029743824557108 under C2's rule max(3·dev_a, 1e-10), with dev_a = 9.59e-11 from `exp083_r3p/W2P2_base.json`, so tol = 2.88e-10. dev = 1.074e-10. **PASS.**
- **084c runs on the PRODUCTION path (alias=False)**, the continuation the continued R uses.

## Amendment 2 (2026-11-23, BEFORE any Level-2 number is computed): reading set fixed from the measured cost (the §E fallback)
- **Measured (n = 2, route (ii), production path):** W2P4 959 s / 0.08 GB; W4P4 1088 s / 0.13 GB; W3P6 5392 s / 0.22 GB.
  - W-scaling ≈ W^0.18 (×1.14 per doubling). P-scaling ≈ P^4.1–4.3 (two P points; with and without the W correction).
- **Projected (argued, two-point extrapolation):** W6P6 1.7–1.8 h; W4P8 5.1–5.8 h; W8P8 5.8–6.6 h; **W5P10 13–16 h; W10P10 15–18 h**.
  - k = 2.5 at n = 2 is ≈ 28–33 h for the pair, and ≈ 85–100 h for n = 2, 3, 4. That is "tens of hours per (geometry, n)" territory, so the §E fallback applies.
- **Core reading set (fixed now):** k ∈ {1, 1.5, 2} × n = 2, i.e. geometries W2P4, W4P4, W3P6, W6P6, W4P8, W8P8 at n = 2. That is ≈ 13 h remaining (W6P6, W4P8, W8P8), one at a time, no-kill.
  - The verdict rules of §C, controls of §D and plants of §F apply unchanged to this set.
  - `exp084c_run.py READ` reads exactly this set. `READ FULL` keeps the original 4 × 3 set.
- **Stated limitation:** the reading does not cover k = 2.5, nor n = 3, 4. n = 3, 4 at k ≤ 2 (≈ 2× the core cost) are supplementary. They run only on a separate go, and are reported as supplementary, never folded into the core verdict.
- **Not yet looked at:** no ΔR has been computed from the three existing files. Only per-file Level-1 lines (already reported) have been read.
