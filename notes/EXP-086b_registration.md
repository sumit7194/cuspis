# EXP-086b (registered 2026-11-25 ~19:50; DESCRIPTIVE reading, not a test; zero compute): EXP-086 with the box c_A(x) in place of bulk c [model: Opus 5.5]

*Bridge GO before the Fable call. Stored inputs only:
- σ₂(x) from `exp084c/c84_W*P*_n2.json`;
- c_A(x) per site from `exp085c/G_W*P*.json` (c_A does not use inner_beta0, so it is unaffected by EXP-087);
- honest R₂ from 084 (exact n; immune);
- bulk c at both bracket ends.*

## Quantity
- Under prescription A at integer n: ΔF_n − nΔF₁ = −(N/2)·n·Ny·Σ_x δ_A(x)σ_n(x). So **ΔR_n^A = (n/(2(n − 1)))·Ny·[Σc_Aσ_n(W₁) − Σc_Aσ_n(W₂)]·norm(k)**; at n = 2 the prefactor is 1. Bulk: the same with c_A ≡ c (EXP-086).
- Reported per geometry W: the σ₂-weighted effective ratio Σc_Aσ₂ / (c·Σσ₂).
- Reported per k ∈ {1, 1.5, 2}: ΔR₂ (bulk and A), and on the parity-matched k = 1 → 2 pair the ratio r = −Δ_k(ΔR₂)/Δ_k(R₂), for both prescriptions.

## Expectation (stated before computing)
- 085c found c_A/c ≈ 0.57–0.80 in the interior (≈ 1 − 2/P). **If that carries over to n = 2**, the n = 2 ratio falls from EXP-086's ~1.37–1.50 (bulk) toward ~1.
- Rough expected value: r_A ≈ 1.4 × 0.7 ≈ 1.0 (argued; the effective weighting depends on where σ₂ lives, near the cut ends or in the interior).

## Caveat (stated before computing)
- c_A was derived for n → 1 (box prescription A). **Using it at n = 2 is itself the assumption that the Fable question (2) asks about.** So this result can SHARPEN that question but cannot SETTLE it.
- Descriptive only: no band, no verdict. EXP-086's registered reading ("overshoot at n = 2") stands as recorded.
