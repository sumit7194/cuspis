# EXP-084 (DRAFT for the Bridge; not registered): where does R's 1/a growth live? The exact integer-n width pair

*Draft 2026-11-23. Context: report entries faaf72f (component scaling), afdbade (081e outcomes pre-stated), a54d999 (two withdrawn designs).
Runs beside the 081e W6/W12 routes only at measured peaks that keep pressure green. [model: Opus 5.5]*

## A. Question
- Stage-1 R(k) grows linearly in k: R ≈ 4.02k − 1.75 (descriptive).
- The growth is the 1/a remainder of near-cancelled k² parts of t0 and T_sad (descriptive). Argued: it is not physics (locality of UV divergences).
- **Where does the defect live?**
  - in the n → 1 continuation (how t0 and T_sad are built from residues and σ̇), or
  - upstream, in the lattice σ-sector Π = 2G∘G on the replica lattice?

## B. Premises kept, stated
1. **The estimator is not the suspect.** The free κ(k) through the same width pair is k-stable (0.01766, 0.01821, 0.01774, 0.01747), so the pair formula and geometry are exonerated on the free side. Branch (ii) therefore narrows to the σ-sector (Bridge, point 2).
2. **The exact-n width-pair coefficient is UV-finite in the continuum** (argued; premises):
   - (a) conical-singularity counterterms (MFS 0904.4477) and the σₙ − σ₁ ∝ c(n)/r edge profile are local on each edge, and the two widths share the same local edge environment, so they cancel in the pair;
   - (b) the cross-term between the two edges' σₙ tails, ∫ d²r 1/(r₁r₂) over the transverse plane, has only integrable 1/r singularities, so it is UV-finite (IR set by the box) and W-dependent only through W/L_box.
   - Hence a ∝ k (∝ 1/a) growth of the exact-n pair is not continuum physics at n = 2, 3.
   - **Caveat (registered, Bridge point 1):** at n ≠ 1 the saddle σₙ is not the n = 1 one, and MFS report unusual O(N) Rényi behaviour near d = 3 (a correlation-length correction scaling as N², a transition in n). So an n-dependent growth could be genuine conical physics outside (a)/(b). See the n-dependence test in C.
3. The exact machinery is `exp083_honest.Geom.Q(n, saddle=True)`: the n-sheet manifold, B_n = (2/Ny)Σ G∘G, and the honest replica saddle σₙ (Newton). No continuation in n, no residues, no QEP.

## C. Measurement (one variable relative to the 081d estimator: exact Q(n) in place of the continued Q′(1))
- Geometries exactly as Stage 1: width pair (W₁, W₂) = (2k, 4k), P = box = 4k, c = 2, for k ∈ {1, 1.5, 2, 2.5}. k = 3 only if its measured peak permits.
- **R_n(k) = −[Q_n(W₁) − Q_n(W₂)] / Ny / (1/W₁ − 1/W₂) / κ(k)**, the 081d normalisation with κ(k) from the free pair.
- n = 2 and n = 3, arm b (honest saddle). Arm a (σ = 0) is a second column, reported only.

## D. Reading (pre-stated; ratio r_n = [R_n(2.5) − R_n(1.5)] / [R_n(2) − R_n(1)], the 081d ratio shifted to the available k)
- Bands as in 081d `decide_r`, applied per n, with ±2σ from float64 precision (measured below). Same tail rule: not applicable (no s-quadrature).

| outcome | pre-stated meaning |
|---|---|
| (i) both n k-stable or converging (r_n ≤ 1.15), while Q′(1) grows | the defect is in the n → 1 continuation (t0/T_sad construction). Next: dissect the continuation. |
| (ii-a) both n power-divergent with r₂ ≈ r₃ (\|r₂ − r₃\| < 0.15) | an n-independent growth: a σ-sector lattice defect upstream of the continuation (Π = 2G∘G on the replica lattice); the continuation is exonerated |
| (ii-b) power-divergent with r₂, r₃ clearly different | n-dependent growth: genuine conical O(N⁰) physics (caveat B.2) cannot be excluded; no defect localised |
| anything else (gap, non-monotone, mixed) | INCONCLUSIVE between (i) and (ii) |

- No physics reading of δκ under any outcome.
- **Known before reading:** nothing about R_n. The dry run formed no width pair.

## E. Controls and checks
| row | check | must-fire / known answer |
|---|---|---|
| KA | float64 Q(2), Q(3) at W2P2 (Wbox 4) against the stored 400-digit Arb values (exp083_r2/W2P2b.json) | **dry run: \|Δ\| = 4.0e-13 and 3.7e-13. PASS** |
| SAD | saddle Newton converges (\|F\| < 1e-13) at every geometry and n | it raises otherwise |
| PREC | float64 precision of R_n: recompute one geometry with Ny-ordering reversed / an alternative logdet path; spread → σ | spread reported |
| PLANT | a planted linear-in-k term c·k added to Q_n(W₁) must turn a k-stable series power-divergent in `decide_r` | must FIRE |
| MEM | per-geometry peak measured progressively (k = 1 → 2.5); a job runs beside a route only if the measured peak keeps pressure green | queue otherwise |

## F. Cost (measured, dry run 2026-11-23, beside the 7 GB W6 route, pressure green at 73% free)
- W3P6b6 (W₁ at k = 1.5), arm b: n = 2 in 0.8 s, n = 3 in 2.2 s. Peak 0.062 GB (whole dry run).
- Larger k are not measured. The scaling estimate (argued) is ~1 GB at k = 2.5, n = 3. Each is measured before running beside a route; k = 3 queues after 081e unless measured small.

## G. Open for the Bridge
- The reading ratio uses k ∈ {1, 1.5, 2, 2.5} (k = 3 is likely queued). Accept the shifted ratio, or wait for k = 3?
- The |r₂ − r₃| < 0.15 threshold for "n-independent": I'd base it on σ_r once PREC is measured. Fix the number now, or after the PREC row?
