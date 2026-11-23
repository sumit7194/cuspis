# T55 (REVISED after the Bridge's review: FIX 1–4 applied; for sending by the Bridge): blind Neon prompt for the O(N⁰) critical-coupling counterterm coefficient [model: Opus 5.5]

*Blind: it states no target value, no factor, and no observed outcome. Sumit sends it from his Chrome after the Bridge's review.*

---

**Prompt (text to send):**

Large-N O(N) vector model on a 3D cubic lattice (spacing a = 1), Hubbard–Stratonovich field σ. Please derive the following from the conventions below, exactly as stated.

**Lattice and propagator.**
- Sites: (x, t) ∈ {0..Lx−1} × {0..Lt−1}, open (Dirichlet) in x and t; y is periodic with Ny sites, handled as Fourier sectors p with m_p² = 2 − 2cos(2πp/Ny).
- Per sector: H_p = diag(4 + m_p²) − A + diag σ, where A is the nearest-neighbour adjacency in (x, t). So the 3D stencil has diagonal 6 and hopping −1.
- σ(x, t) is y-independent and enters as **+diag σ**. G = H⁻¹, so **δG = −G δσ G**.
- Bulk lattice propagator: G(k) = 1/Σᵢ(2 − 2cos kᵢ).

**Effective action and coupling.**
- Γ[σ] = N[½ Tr log(H₀ + σ) − Σ_x σ(x)/(2g)] + ½ Tr log B[σ] + …
- B[σ](x, y) = 2 G(x, y)² is the σ kernel. In y-sectors: B_k = (2/Ny) Σ_p G_p ∘ G_(k−p), with ∘ the elementwise product.
- The coupling is SITE-DEPENDENT: 1/g(x) ≡ G₁^box(x, x)|_(σ=0), the coincident propagator of the unreplicated finite box. This makes σ₁ ≡ 0 an exact solution on the box, and away from the walls 1/g(x) → ∫_BZ d³k/(2π)³ G(k), the N = ∞ bulk critical value.

**Replicas.**
- n copies of the lattice. For x in a cut C (W consecutive sites, x ∈ [x₀, x₀ + W) with x₀ = P + ⌊(P − W)/2⌋, i.e. centred in the middle third of the x range) the links (x, t_c) → (x, t_c + 1) are reconnected from sheet s to sheet s + 1 mod n. G_n = H_n⁻¹ on the n-sheet lattice.
- σ_n is the replica-symmetric solution of the O(N) gap equation with this 1/g(x) held fixed SITE BY SITE: (1/Ny) Σ_p G_(n,p)(x, x)[σ_n] = (1/Ny) Σ_p G_(1,p)(x, x)[0] at every (x, t), on any one sheet.
- σ̇ ≡ ∂_n σ_n at n = 1, continued in n. From the linearised gap equation, σ̇ = 2 B₁[k=0]⁻¹ d, with d(x) = ∂_n [(1/Ny) Σ_p G_(n,p)(x, x) on any one sheet] at σ = 0, n = 1. The continuation in n is analytic: single-factor Poisson continuation of the pole terms of the sector propagators.
- Σσ̇ ≡ Σ_(x,t) σ̇(x, t): the sum over ONE sheet's (x, t) sites, with no y-sum and no Ny factor (σ is y-independent).
- Q(n) = Σ_k log det B_(n,k)[σ_n] − n Σ_k log det B_(1,k). The O(N⁰) entropy is S = ½ Q′(1).

**Quantity of interest.**
- Strips W₁ = 2ℓ and W₂ = 4ℓ in a box with Lx = 3P, Lt = 2P, Ny = 4P, P = 4ℓ, cut at t_c = P − 1.
- R(ℓ) = −[S(W₁) − S(W₂)] / (Ny (1/W₁ − 1/W₂) κ(ℓ)), where κ(ℓ) is the same combination of the free (N = ∞, per-component) entropies.
- The continuum limit is ℓ → ∞ (ℓ ∝ 1/a).

**Please derive, step by step:**
1. The O(1/N) shift δ(1/g_c) of the critical coupling for exactly this lattice action and bubble normalisation.
   - (a) In the bulk: as an explicit Brillouin-zone expression in G(k) and B(q) = 2⟨G(k)G(k+q)⟩_k, with any IR-divergent (B(0)-dependent) piece separated from the UV piece.
   - (b) For the site-dependent prescription 1/g(x) = G₁^box(x, x) above: the O(1/N) correction δ(1/g(x)) it requires, including near the walls.
2. The replica computation above keeps 1/g(x) at its N = ∞ (site-dependent) value. Derive the O(N⁰) term in Q′(1) (equivalently in S) that using the correct critical coupling adds. Write it as (numerical coefficient) × (BZ constant) × Σσ̇, with the coefficient, its sign, and the BZ constant all explicit in these conventions.
3. Any OTHER O(N⁰) terms of the same order (growing like 1/a in R) that a bulk δ(1/g_c) treatment alone would miss. Consider explicitly the wall/boundary terms arising from the site-dependent coupling prescription; also the normalisation of the σ propagator, the n-derivative of the saddle, and contact terms. Give their sign and, if possible, size.

State which steps are standard results (with references) and which are your own derivation.

---

## Source of each definition (for the Bridge's check)
| definition | copied from |
|---|---|
| lattice; open x, t; periodic y as sectors; m_p²; H_p = diag(4 + m_p²) − A + diag σ | `scripts/exp083_honest.py` `Geom.__init__`, `m2`, `Hn` (lines 13–37); `notes/EXP-085_registration.md` §3 |
| σ as +diag σ; δG = −GσG | `notes/EXP-085_registration.md` §1.2 |
| G(k) = 1/Σᵢ(2 − 2cos kᵢ); B(q) = 2⟨G(k)G(k+q)⟩ | `notes/EXP-085_registration.md` §3 |
| Γ[σ], including −Σσ/(2g) and ½ Tr log B | `notes/EXP-085_registration_draft.md` §A.2 (**graded "argued" there**) |
| B_k = (2/Ny) Σ_p G_p ∘ G_(k−p) | `scripts/exp083_honest.py` `logdetB` (lines 42–48); `notes/EXP-085_registration.md` §3 |
| gap equation for σ_n, g held fixed, replica-symmetric σ | `scripts/exp083_honest.py` `saddle` (lines 49–58: target = n = 1 coincident G; one σ applied to all sheets via `Hn`) |
| site-dependent 1/g(x) = G₁^box(x, x) (Bridge FIX 1) | `scripts/exp083_honest.py` `saddle` (line 50: target = Σ_p diag G₁ / Ny, held per site). The bulk limit ∫G(k) = W/6 is as in `scripts/exp085_a4.py`. The earlier draft's single bulk 1/g with σ₁ ≡ 0 was self-contradictory on a Dirichlet box |
| replica gluing (cut links, sheet s → s + 1) | `scripts/exp083_honest.py` `Hn` (lines 32–36) |
| σ̇ = 2B₁[0]⁻¹d; d = ∂_n of the sheet coincident G, Poisson continuation (FIX 2); Σσ̇ over one sheet, no y-sum (FIX 3) | `notes/EXP-085_registration.md` §5; `scripts/sigma3d.py` `saddle_term` docstring (380–381), `coincident_dn` docstring (368) |
| Σσ̇ = Σ_x σ̇(x), lattice units | `notes/EXP-085_registration.md` §5 |
| Q(n), S = ½Q′(1) | `notes/EXP-085_registration.md` §1.1; `scripts/exp083_honest.py` `Q` |
| R(k), κ(k) | `scripts/exp081d_analyze.py` docstring line 4; `scripts/exp081b_run.py` `free`, `pair` (25–36) |
| geometry Lx = 2P + Wbox, Wbox = P, Lt = 2P, Ny = 4P, t_c = P − 1 | `scripts/exp083_honest.py` line 15; `scripts/exp085_run.py` `build` |

**Deliberately omitted:** the factor ½ in front of c, the T₀ˢᵘᵇ formula, c's value, the 0.77 / 1.30, the sign of the observed slope change, and any mention of overshoot.
- "ℓ" replaces k, to avoid a clash with momentum.
- The ½ in S = ½Q′(1) is kept: it is a definition that follows from Γ, not the target (Bridge FIX 4).
