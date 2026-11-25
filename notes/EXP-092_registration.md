# EXP-092 REGISTRATION (2026-11-26 ~05:00; nothing computed at P = 16, 20): centre c_A at P = 16, 20 (third implementation) and the log-in-c_A fit test [model: Opus 5.5]

*Bridge items (b) and (e), from Fable's revision d79a113 (branch fable/2026-11-26-A-vs-bulk). Fable's values are UNVERIFIED predictions.*

## 1. Quantity
- **Centre c_A(P):** the mean of c_A over the 4 centre sites (x ∈ {Lx//2 − 1, Lx//2}, t ∈ {Lt//2 − 1, Lt//2}; site index x·Lt + t). This is Fable's definition (ca_centre.py).
  - It is computed on the n = 1 box: Lx = 3P, Lt = 2P, Ny = 4P, Dirichlet in (x, t), y periodic as Fourier sectors, no cut.
  - The formula is the 085c sector formula: c_A(z) = −4·term1(z) + 2·(B₀Λ)(z), with term1 = (1/Ny)Σ_k diag(G_k M_k G_k), M_k = (1/Ny)Σ_q A_q∘G_{k−q}, A_q = B_q⁻¹, B_q = (2/Ny)Σ_p G_p∘G_{q−p}, and Λ = rowsum((1/Ny)Σ_k A_k∘G_k).
- **My implementation (`scripts/exp092_cA_centre.py`, new):**
  - G_p by dense inverse of H_p = diag(4 + m_p²) − A_2D (no sine modes, no Strip3D, no 085c code).
  - It streams over the distinct |q| (multiplicity 2 except q = 0 and Ny/2) and keeps only the G_p in memory.
  - One core.

## 2. Predictions, computed BEFORE any P = 16/20 run, from Fable's P = 8–14 centre values (`notes/fable_AvB/cA_centre_P*.json`; P = 8, 10, 12 equal the office's to 1e-14)
| P | H-log (fixed gL = 0.0611: c∞ + (g1 + gL ln P)/P + g2/P²; fit rms 6.5e-7) | no-log (c∞ + g1/P + g2/P²; rms 4.3e-6) | gap |
|---|---|---|---|
| 16 | **−0.0991561** (Fable quotes −0.09915) | −0.0991277 | 2.83e-5 |
| 20 | **−0.1022378** (Fable quotes −0.10224) | −0.1021242 | 1.14e-4 |

## 3. Reading (fixed now)
- d_L = |meas − H-log|, d_N = |meas − no-log| (full-precision predictions above).
- **H-log supported:** d_L < d_N at BOTH P, AND d_L(20) ≤ ½·gap(20) = 5.7e-5.
- **H-log contradicted:** d_N < d_L at P = 20.
- **Neither form:** d_L(20) and d_N(20) both > gap(20). Neither 3-parameter form extrapolates, whatever the ordering.
- Otherwise: **undecided**.
- Fable's quoted 5-digit values are reported beside the reading, not graded separately.

## 4. Controls (before P = 16/20; exit 1 = no measurement)
- **KA-all:** all sites at P = 4 and P = 6 against the stored office c_A (`exp085c/G_W4P4.json`, `G_W6P6.json`, key `cA`), to 1e-10 relative.
- **KA-centre:** the centre at P = 8, 10, 12 against the G files (G_W8P8, G_W10P10, G_W12P12), to 1e-10 relative.
- **Must-fail plant:** with the factor 2 of the B₀Λ term set to 1, KA-all at P = 4 must FAIL.
- **Symmetry:** the 4 centre sites agree to 1e-12 relative at P = 16 and 20 (box symmetry). If not, the value is not read.

## 5. Fit test (item (e); descriptive with stated criteria; uses P = 6 … 20 once measured)
- **Fits on centre c_A:**
  - (i) no-log, c∞ + g1/P + g2/P² + g3/P³ (4 parameters);
  - (ii) free log, c∞ + (g1 + gL ln P)/P + g2/P² (4 parameters);
  - (iii) fixed gL = 0.0611 with g2 (3 parameters).
- **Point sets:** P = 8–14 (4 points: 0 dof for (i) and (ii), so NOT a test; stated, not used); P = 6–14 (1 dof); P = 8–20 (2 dof for (i)/(ii), 3 for (iii)); P = 6–20.
- **Criterion "the log preference survives":** on P = 8–20, rms(ii) ≤ ⅓·rms(i), AND the free gL of (ii) lies in Fable's pre-stated "not contradicted" window [0.04, 0.12]. Otherwise "does not survive". c∞ from every fit is reported, as the drift across forms and sets (the nuisance sweep).
- Even if it survives, this does not establish the log: it is a model comparison with few dof. The derivation read (item (e), first part) is separate.

## 6. Cost and footprint (declared)
- Estimates: P = 16, N = 1536 sites, 33 distinct sectors, ~0.9 GB, a few minutes. P = 20, N = 2400, 41 sectors, ~2.3 GB, ~10–20 min.
- Measured peak and wall time are reported (no-kill watchdog). nice 12, one core: this replaces run_089's finished core one for one. Gate: free ≥ 50% and pgate before each P.
