# T55 (DRAFT for the Bridge's review; NOT sent): blind Neon prompt for the O(N⁰) critical-coupling counterterm coefficient [model: Opus 5.5]

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
- The coupling is fixed at the N = ∞ lattice critical value: 1/g = G(x, x)|_(σ=0) = ∫_BZ d³k/(2π)³ G(k). On the unreplicated lattice, σ₁ ≡ 0.

**Replicas.**
- n copies of the lattice. For x in a cut C (W consecutive sites, x ∈ [x₀, x₀ + W) with x₀ = P + ⌊(P − W)/2⌋, i.e. centred in the middle third of the x range) the links (x, t_c) → (x, t_c + 1) are reconnected from sheet s to sheet s + 1 mod n. G_n = H_n⁻¹ on the n-sheet lattice.
- σ_n is the replica-symmetric solution of the O(N) gap equation with g held fixed: (1/Ny) Σ_p G_(n,p)(x, x) = (1/Ny) Σ_p G_(1,p)(x, x) at every (x, t).
- σ̇ ≡ ∂_n σ_n at n = 1, continued in n. From the linearised gap equation, σ̇ = 2 B₁[k=0]⁻¹ d, where d(x) = ∂_n G_n(x, x)|_(σ=0, n=1). Σσ̇ ≡ Σ_(x,t) σ̇(x, t).
- Q(n) = Σ_k log det B_(n,k)[σ_n] − n Σ_k log det B_(1,k). The O(N⁰) entropy is S = ½ Q′(1).

**Quantity of interest.**
- Strips W₁ = 2ℓ and W₂ = 4ℓ in a box with Lx = 3P, Lt = 2P, Ny = 4P, P = 4ℓ, cut at t_c = P − 1.
- R(ℓ) = −[S(W₁) − S(W₂)] / (Ny (1/W₁ − 1/W₂) κ(ℓ)), where κ(ℓ) is the same combination of the free (N = ∞, per-component) entropies.
- The continuum limit is ℓ → ∞ (ℓ ∝ 1/a).

**Please derive, step by step:**
1. The O(1/N) shift δ(1/g_c) of the critical coupling for exactly this lattice action and bubble normalisation, as an explicit Brillouin-zone expression in G(k) and B(q) = 2⟨G(k)G(k+q)⟩_k. Separate any IR-divergent (B(0)-dependent) piece from the UV piece.
2. The replica computation above keeps g at its N = ∞ value. Derive the O(N⁰) term in Q′(1) (equivalently in S) that using the correct critical coupling adds. Write it as (numerical coefficient) × (BZ constant) × Σσ̇, with the coefficient, its sign, and the BZ constant all explicit in these conventions.
3. Any OTHER O(N⁰) terms of the same order (growing like 1/a in R) that a δ(1/g_c) treatment alone would miss. Consider, for example, the normalisation of the σ propagator, the n-derivative of the saddle, and boundary or contact terms. Give their sign and, if possible, size.

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
| **1/g = G(x, x) at σ = 0 = ∫G(k)** | **INFERRED, not copied**: from `saddle` (target = G₁(x, x), σ₁ = 0) plus Γ's saddle condition (draft §A.2); the BZ value is ⟨G(k)⟩ = W/6, as in `scripts/exp085_a4.py` |
| replica gluing (cut links, sheet s → s + 1) | `scripts/exp083_honest.py` `Hn` (lines 32–36) |
| σ̇ = 2B₁[0]⁻¹d; d = ∂_n coincident G | `notes/EXP-085_registration.md` §5; `scripts/sigma3d.py` `saddle_term` docstring (380–381), `coincident_dn` docstring (368) |
| Σσ̇ = Σ_x σ̇(x), lattice units | `notes/EXP-085_registration.md` §5 |
| Q(n), S = ½Q′(1) | `notes/EXP-085_registration.md` §1.1; `scripts/exp083_honest.py` `Q` |
| R(k), κ(k) | `scripts/exp081d_analyze.py` docstring line 4; `scripts/exp081b_run.py` `free`, `pair` (25–36) |
| geometry Lx = 2P + Wbox, Wbox = P, Lt = 2P, Ny = 4P, t_c = P − 1 | `scripts/exp083_honest.py` line 15; `scripts/exp085_run.py` `build` |

**Deliberately omitted:** the factor ½ in front of c, the T₀ˢᵘᵇ formula, c's value, the 0.77 / 1.30, the sign of the observed slope change, and any mention of overshoot.
- "ℓ" replaces k, to avoid a clash with momentum.
- The ½ in S = ½Q′(1) is the definition of S, not the target; flagged for the Bridge to judge.
