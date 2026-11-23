# T55 (Neon) answer: Cuspis verification against the files (2026-11-23) [model: Opus 5.5]

*Input: the Bridge's condensation `~/Github/neon_work/cuspis/T55_answer.md` (Neon output, UNVERIFIED data). I did not read the full Gemini text; the condensation is what was checked.*

## Item 1: coefficient and sign. **Consistent with the registration (partially verified: two independent derivations agree on paper; no numerical test of the coefficient itself)**
- **D_σ.** The second-order expansion of N[½Tr log(H₀ + σ) − Σσ/(2g)] gives −(N/4)ΣG²δσδσ = −(N/8)δσᵀBδσ, with B = 2G∘G. Rotating gives ⟨δσδσ⟩ = −(4/N)B⁻¹. I re-derived this; it agrees.
- **1-loop gap equation.** ∂Γ/∂σ(z) = N[½G(z,z) − 1/(2g)] + ½T(z) with T(z) = Tr B⁻¹∂B/∂σ(z) = −4Σ_{x,y}B⁻¹(x,y)G(x,y)G(x,z)G(z,y). Hence 1/g = G(z,z) + T(z)/N. This is Neon's equation, and my draft §A.2.
- **Bulk.** Neon's δ(1/g_c) = −(4/N)C_BZ, C_BZ = ⟨B⁻¹(q)⟨G²[G(k+q) − G(q)]⟩_k⟩_q.
  - My registration §4 and `exp085_a4.py: c_of_n` have c = −4·mean((1/B)(⟨G²G⟩ − G·⟨G²⟩)) = −4C_BZ. So **N·δ(1/g_c) = c**, and the IR split matches §A.3.
- **ΔS.** ΔF_n = −(N/2)·n·Ny·Σ_xt δ(1/g)σ_n. With S = ∂_n(F_n − nF₁) and σ₁ = 0, this gives ΔS = −(N/2)Ny Σ_xt δ(1/g)σ̇.
  - In the bulk: ΔS = −½c·Ny·Σ_xt σ̇.
  - The code: `exp085_run.py` line 114 has `Sigma3D = Ny·Σ_xt σ̇`, and `corr = ½c·ΔSigma3D·norm`. So the registered S_corr = S − ½c·Sigma3D is **identical**, including the factor Ny.
- **Consequence:** branch 1 (a coefficient or sign error in the bulk counterterm) is disfavoured. It is NOT excluded: what remains open is the PRESCRIPTION (bulk c, box c_A, or the full box tadpole), not the coefficient.
- **References** "Ma 1973" (η) and "MFS 2009" (saddle sign): NOT checked by me (Rule III). They are not used for anything.

## Item 2: the "exact site-by-site identity". **Verified on paper as an algebraic identity, so it carries no evidence for Neon's physics**
- Write Λ(x) := Σ_y B₁⁻¹(x,y)G₁(x,y), so (N/2)Σ₁^loc(x) = −2Λ(x).
- From Neon's δ_A: (N/2)δ_A(1/g(z)) = −2Σ_{x,y}B⁻¹GG(z,x)G(y,z) + 2Σ_x Λ(x)G(z,x)² = ½T(z) + 2Σ_x Λ(x)G(x,z)².
- Multiply by σ̇(z) and sum over z. The linearised gap equation (test (i)'s content) is Σ_z G(x,z)²σ̇(z) = d(x). This gives
  **½Σ_z T(z)σ̇(z) = (N/2)Σ_z δ_A(z)σ̇(z) + (N/2)Σ_x Σ₁^loc(x)d(x)**: Neon's identity, exactly.
- **So the identity holds wherever σ̇ solves the linearised gap equation.** It is exact up to test (i)'s residual.
  - At W2P4, where (i) passes at 1.5e-13, a numerical check of it **cannot fail**. At W4P4 it would fail by the known (i) mismatch, ≈5e-9.
- **Proposed 3(a) is therefore an implementation check of the c_A code, not a test of Neon's derivation** ("a check that cannot fail is not a check").
- **The real content of Neon's item 2 lies elsewhere:**
  - (P1) the physics claim that prescription A (σ̄₁ = Σ₁^loc site by site) is the right O(N⁰) criticality condition;
  - (P2) the claim that the leftover (N/2)Ny ΣΣ₁^loc·d term cancels the UV piece of ½Q′_explicit. That is an OPE-type statement, NOT exact: ∂_nB_n is not exactly local in d.
  - A third prescription shows what is at stake. Keeping σ̄₁ ≡ 0 exactly at O(N⁰) needs δ(1/g(x)) = T₁^box(x)/N (the full box tadpole). That counterterm removes the ENTIRE saddle term ½T_sad. Prescriptions A and "full tadpole" differ by exactly the Σ^loc·d term.
- **Cheap consequence:** under prescription A, ½Σ_z c_A(z)σ̇(z) = ½T_sad + 2Ny Σ_x Λ(x)d(x).
  - So the c_A-corrected R needs only the stored T_sad plus Λ (the diagonal of B₁⁻¹∘G₁, computed with production's sector convolution) and d. No σ̇ solve and no FFT extrapolation are needed.

## Neon's checkable side claims, against stored data (`exp081d_results/exp085/C_*.json`; descriptive, read after the 085 reading closed)
| k | Σ_xt σ̇(W₁) | Σ_xt σ̇(W₂) | difference |
|---|---|---|---|
| 1 | −2.1321 | −2.4783 | +0.3462 |
| 1.5 | −2.4912 | −2.8550 | +0.3638 |
| 2 | −2.6971 | −3.0685 | +0.3715 |
| 2.5 | −2.8295 | −3.2056 | +0.3761 |
- σ̇ < 0 (Neon's sign): **consistent**.
- Σσ̇(W₁) − Σσ̇(W₂) = O(1) and > 0: **consistent**. It is nearly k-independent: +8.6% from k = 1 to 2.5, with shrinking increments.
- Hence ΔR_bulk = ½c·Ny·ΔΣ·norm ∝ −ℓ, since c < 0 and norm ≈ 1/(4κ): **consistent** with "ΔR_bulk ∝ −ℓ". This is the mechanism by which the counterterm acts on the slope.
- The coefficient "−4πc ln W": NOT checked. The condensation doesn't define this c, and W and P change together along the series.
- "No other 1/a term (σ the only relevant singlet)": an RG argument, **argued**. The lattice cut endpoints and the corners at the cut are not obviously covered.
- The "wrong D_σ prefactor leaves ½ or ¾" remark: not used (it does not match 0.77).
