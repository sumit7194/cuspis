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
