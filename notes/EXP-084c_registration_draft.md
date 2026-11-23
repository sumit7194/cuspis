# EXP-084c (DRAFT for the Bridge; not registered): does the production continuation equal the honest family at integer n, at the 084 geometries?

*Draft 2026-11-23, after 084b ("c(1) non-zero"; meaning unestablished) and the Bridge's C2 conflict note. Before n = 5. Alone, no-kill;
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
