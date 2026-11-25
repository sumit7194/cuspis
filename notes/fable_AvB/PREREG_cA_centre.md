# Pre-registration: centre c_A beyond P = 10, second implementation (2026-11-26 ~03:50) [model: Fable 5.2]
The brief allows a minutes-scale c_A check on boxes beyond P = 10. Written before `ca_centre.py` is run at any P. UNVERIFIED.
- **What:** c_A at the 4 centre sites of the n = 1 box (Lx = 3P, Lt = 2P, Ny = 4P, no cut), my own numpy implementation of the 085c sector formula (sine-mode propagators,
  no Strip3D, no office code). u = 1 - c_A/c_hi.
- **Known-answer control FIRST (can fail):** all sites at P = 4 and P = 6, and the centre at P = 8, 10, must equal the stored office c_A to 1e-8 relative.
  Negative control: with the factor 2 of the B_0 Lambda term set to 1 the P = 4 comparison must FAIL. If the KA fails there is no conclusion.
- **Then P = 12 and P = 14.** P = 12 is my own sealed S-c quantity (c615773); running it un-blinds me, which is allowed after the seal, and gives the office a second implementation.
- **Predictions (centre u*P):** saturating form 2.30 - 2.64/P: 2.078 at P = 12, 2.111 at P = 14. Log form (2.034 + 0.296 ln(P/10)): 2.088, 2.134.
- **Reading, fixed now:** P = 14 centre u*P <= 2.117 supports saturation (Delta_bb interior -> const, c_Ainf on the hi end). >= 2.128 contradicts it (a log is alive).
  Between: undecided. P = 12 alone cannot separate them (0.010 apart).
- **Cost stated before running:** P = 14 has 1176 sites, 29 distinct sectors: about 0.7 GB, 1 core, a few minutes. If memory passes 1 GB I stop it myself.

## Outcome of the above, and a second pre-registration (written 2026-11-26 after the P <= 14 run, BEFORE h0 is computed)
- KA: PASS at 1e-14 (P = 4, 6 all sites; P = 8, 10 centre); negative control FAILS as required. Centre u*P = 1.6656, 1.8578, 1.9681, 2.0338, 2.0716, 2.0905 (P = 4..14).
- By the reading fixed above, P = 14 (2.0905 <= 2.117) "supports saturation". **I do not accept my own reading.** It assumed c_inf = c_hi. Fits of c_A itself (`ca_centre_fits.txt`)
  put c_Ainf beyond the hi end (-0.1157 to -0.1190), and a (ln P)/P form fits 5 points 10x better than powers (rms 9e-8 vs 1e-6). The check named the failure mode and could not detect it.
- **New hypothesis H-log (argued):** the massless-box tuning is a coupling of dimension y = 3 - Delta_sigma = 1 + y1/N, y1 = 32/(3 pi^2) = 1.0808 (standard large-N value, from memory,
  not checked at source). Scale covariance then gives c_A - c_inf = (g1 + gL ln P)/P at the centre with **gL = y1 * h0, h0 = lim P (G_inf(0) - G1_box(centre, centre))**.
- **Test, thresholds fixed now:** free fits gave gL = 0.074-0.077. H-log is supported if y1*h0 is in [0.06, 0.09]; contradicted if outside [0.04, 0.12]. h0 is a leading-order
  lattice sum (seconds). If supported, refit c_A with gL FIXED to y1*h0 and report c_Ainf and the rms.
