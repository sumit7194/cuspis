# EXP-085c REGISTRATION (2026-11-23, after the Bridge's final look; nothing computed): the counterterm under ONE pre-chosen prescription [model: Opus 5.5]

*Draft 2026-11-23, revised per the Bridge's 4 points. Written after EXP-085 closed INCONCLUSIVE (3e8e610) and the T55 verification (9f5b121). Header status: 085w W4P4 gives H1 FAILS, and W4P4 is BOUNDED (≤ 6e-9 absolute, ≈ 2.5e-7 of |d|).
The (i-G) mismatch is 99.8% the s ∈ (3, 6] truncation tail of d^B; (i-B) shows a separate ≈ 2.4e-9 Ġ^A-route discrepancy (0ab4fdd). W2P4: family prediction PASS (no poles in (3, 6], tail = 0), plant fires, KA bitwise. 085w2 (s_cut 3 → 6) is running.*

## A. The PRIMARY prescription and why (argued; written before anything is computed)
- **What production does at N = ∞.** 1/g(x) = G₁^box(x, x) site by site (`exp083_honest.saddle`: target = the n = 1 coincident G per site). This makes σ₁ ≡ 0 exact on the box, and the same 1/g(x) is held fixed on the replicas.
- At N = ∞, σ₁ ≡ 0 does TWO jobs at once: (i) the σ expectation vanishes, and (ii) the theory is critical (the φ propagator is massless).
- **At O(1/N) the two jobs separate.** Criticality requires the renormalised mass to vanish, i.e. σ̄ = Σ(0), the mass counterterm cancelling the self-energy. It does NOT require σ̄ = 0. The object of study (δκ) belongs to the critical theory. So the consistent O(1/N) continuation of production's prescription keeps job (ii), criticality, site by site on the SAME box with the SAME propagators.
  - That is **prescription A** (Neon T55 1(b)): σ̄₁(x) = Σ₁^loc(x) and δ_A(1/g(z)) = −(4/N)Σ_{x,y}B₁⁻¹(x,y)G₁(x,y)G₁(z,x)[G₁(y,z) − G₁(x,z)], with n = 1 box propagators and no cut.
- **Supporting facts:**
  - (a) A's bulk limit IS the registered c. On a periodic lattice the two terms Fourier-transform exactly into ⟨B⁻¹(q)⟨G(k)²G(k+q)⟩⟩ − ⟨B⁻¹(q)G(q)⟩⟨G²⟩ = C_BZ, so N·δ_A → −4C_BZ = c (derived on paper; KA-torus below makes it checkable).
  - (b) A needs no BZ input and no n → ∞ extrapolation.
- **PRIMARY = A.** The other two are DESCRIPTIVE ("not a reading"). Nothing is promoted after the fact.
  - If a descriptive prescription flattens and A does not, the result reads "A FAILS; descriptive X flattens (post-hoc, needs its own registration)".

## B. The three prescriptions as formulas (R units, with the stored component split R = R_t0 + R_Tsad + R_C from `exp081d_results.json`)
- R-operator: R[X] := −(X(W₁) − X(W₂)) / (Ny·(1/W₁ − 1/W₂)·κ(k)), the 081d normalisation with stored κ.
- **A (PRIMARY):** ΔS_A = −(N/2)·Σ_3D δ_A(1/g)σ̇. By the algebraic identity (T55 verification) this equals −½T_sad − 2Σ_3D Λ·d, with Λ(x) := Σ_y B₁⁻¹(x, y)G₁(x, y) (3D sum).
  - In sectors: Λ(x) = Σ_x′ (1/Ny)Σ_k [B_k⁻¹ ∘ G_k](x, x′). Hence Σ_3D Λd = Ny·Σ_xt Λ(x)d(x).
  - **Route 1 (direct; the reading's route, Bridge):** R_corr^A = R − R[½Σ_3D c_A(x)σ̇(x)], with c_A(x) = N·δ_A(1/g(x)) built on the box. R has no k² content (g_raw is linear), so the 1/a² question is whether **R[½Σc_Aσ̇]** has k² content. It is read there, with no subtraction of large numbers.
  - **Route 2 (identity; the second implementation):** R_corr^A = R_t0 + R_C + R[−2·Ny·Σ_xt Λd].
  - **Two-route KA (can fail through code errors):** routes 1 and 2 agree to ≤ 1e-10 relative per geometry.
- **Bulk (descriptive):** R_corr^bulk = R + ½c·ΔSigma3D·norm. This is the 085 number, re-read with signed bands at both bracket ends.
- **Full box tadpole (descriptive):** δ(1/g(x)) = T₁^box(x)/N keeps σ̄₁ ≡ 0 at O(N⁰) and removes ALL of ½T_sad. **R_corr^full = R_t0 + R_C.**
  - **ALREADY KNOWN from stored components (NOT blind):** −36.64, −73.18, −122.99, −187.92 at k = 1…2.5, a k² blow-up.
  - Listed for completeness: it is refuted by stored data before registration, and that fact is not used to choose the primary (§A is the physics argument).

## C. 1/a² structure, predicted before computing
| prescription | predicted k² content of R_corr | basis |
|---|---|---|
| A | **none**: R_Λ cancels R_t0's k² piece (T55 (P2): the Σ^loc·d term cancels the UV/OPE piece of ½Q′_explicit) | argued (OPE, not exact) |
| bulk | none (registered §1.3: the −2B̃(0)I_UV piece stays and cancels (A)'s OPE term) | argued |
| full tadpole | **k² blow-up** (removes the OPE-cancelling piece) | known from stored data |
- **Row, A's 1/a² test (threshold tied to the reading, Bridge):** fit R[½Σc_Aσ̇](k) = c₂k² + c₁k + c₀ with the 084b-style 3-parameter fit (full covariance). On these 4 k the fit has **1 dof**.
  - A k² term induces a 2-dof linear-fit slope of 3.5·c₂ on k ∈ {1, 1.5, 2, 2.5}: Σ(k − k̄)(k² − ⟨k²⟩)/Σ(k − k̄)² = 4.375/1.25 (checked).
  - **"no 1/a² remainder"** iff |c₂^A| + 2σ(c₂) ≤ 0.057: the WHOLE interval satisfies 3.5·|c₂| ≤ 0.05·g_raw (whole-interval condition, Bridge).
  - If |c₂^A| > 0.057 with the whole ±2σ interval outside: **"A leaves a 1/a² remainder → (P2) fails"**, and no slope reading is made.
  - Otherwise (unresolved): **INCONCLUSIVE**.

## D. Reading (PRIMARY A only; SIGNED bands, Bridge rule)
- g_A = least-squares slope of R_corr^A over k ∈ {1, 1.5, 2, 2.5}, 2 dof, with σ_g as in 085 §6 (fit and propagation). ρ_s := g_A / g_raw (signed), with g_raw = 4.019821717340081 (stored).

| reading | the whole interval ρ_s ± 2σ lies in |
|---|---|
| **overshoot** (sign-reversed remainder) | ρ_s < −0.1 |
| **supported** (A flattens) | −0.1 ≤ ρ_s ≤ 0.1 |
| **partial** | 0.1 < ρ_s < 0.5 |
| **refuted as sole cause** | ρ_s ≥ 0.5 |
| INCONCLUSIVE | straddles an edge; or the 1/a² row fails; or a control fails |

- The descriptive prescriptions get the same table, labelled "not a reading".
- **Physical meaning of "supported" under A:** the 1/a growth of R is removed by the box-consistent O(N⁰) criticality counterterm. Graded **partially verified** (one mechanism, two implementations).
- **Descriptive decomposition (Bridge; not a reading), for interpretation:**
  - (i) R[½Σ(c_A − c)σ̇] per k: the box-minus-bulk part of the counterterm, at both 085 bracket ends;
  - (ii) the map c_A(x)/c in the interior (|x − x_mid| ≤ 1, t mid-box), at the walls (x = 0, t = 0), and next to the cut ends.
  - Neon's claim "c_A → c in the interior" is checked here, descriptively.

## E. Controls
| row | check | expected |
|---|---|---|
| **KA-torus** (can fail: independent code path) | c_A(z) from the position-space δ_A on a periodic n³ torus (zero mode of G excluded, dense B⁻¹) at n = 8, 12 | uniform in z, and equal to `exp085_a4.c_of_n(n)` to ≤ 1e-10 relative |
| **KA-sector** (can fail) | Λ(x) via sectors (1/Ny)Σ_k B_k⁻¹∘G_k against a dense 3D construction at W2P4 (N·Ny = 1536) | ≤ 1e-12 |
| identity KA + planted break | at W2P4: ½T_sad = ½Σc_Aσ̇ − 2Σ_3DΛd to 1e-12; planted σ̇ × (1 + 1e-6) at one site must FAIL | implementation only (algebraic; cannot test the physics) |
| zero | R_corr with the counterterm × 0 reproduces g_raw | bitwise |
| must-fail sign | −ΔS_A in place of +ΔS_A | must not land in the band A reads (pre-stated: it fires iff its band differs) |
| two-route KA | route 1 (direct c_A) against route 2 (identity) per geometry | ≤ 1e-10 relative |
| reproduction | stored R_t0, R_Tsad, R_C reproduce R_T0 per k | 1e-12 (already: sums match) |

## F. Cost (to be measured; nothing run)
- Per geometry: install + B₁ + d + Λ. Phase C's install times were 11–888 s per geometry; B–E peaked at 3.15 GB, at the big geometries.
- **k ≤ 2 (6 geometries) beside part 8 only if the measured peak is < 0.5 GB.** k = 2.5 (W5P10, W10P10) is likely above that, so it runs after part 8, alone.
- Tier 1: KA-torus and KA-sector first (seconds to minutes), then W2P4 alone with a measured peak, then the rest.

## G. The W4P4 bound in R units (stated BEFORE the reading)
- The 085w/085w2 discrepancies at W4P4 are ≤ 6e-9 absolute in d (Bridge's bound).
- Route 2 is linear in d: R[−2NyΣΛd] = −(X(W₁) − X(W₂))·norm with X = −2NyΣΛd. So |ΔR| ≤ 2·Ny·Σ_x|Λ(x)|·6e-9·norm(1).
- This bound is evaluated numerically at W4P4 by the 085c script BEFORE the reading line is printed, with Λ from the same run. Expected (argued): ~1e-6 or less, against the 0.05·g_raw ≈ 0.2 band resolution.
- **If the evaluated bound exceeds 0.01, the k = 1 point is reported with that caveat in the headline.**
