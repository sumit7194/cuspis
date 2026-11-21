"""EXP-062 pre-check 5 (piece (II)'): physical bubble at the moving lattice frequency q/n in tau-space,
B_reg^(n)(q/n; rho) = Int_0^{2 pi n} dtau e^{-i q tau/n} 2 G_reg^(n)(rho,tau)^2 (G_reg^(n) = G_tw^(n) at a = 0, nu = 0 reference).
Gate: n = 1 equals e^{-|q| rho}/(8 pi sinh rho). Then
dB'_q(rho) = d_n B_reg^(n)(q/n) - |q| rho e^{-|q| rho}/(8 pi sinh rho) - (1/2pi) gdot(rho) g_{|q|}(rho)
(Gamma-family derivative subtracted; corrected zero mode) and its small-rho behaviour (gap cancellation predicts bounded). [model: Opus 5.5]"""
import sys, os, time
import numpy as np
from scipy.integrate import quad
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exp062_precheck_image import Gtw_n
from exp062_zeromode import gdot
import exp056_sigma_kernel as K

def Breg(q, rho, n):
    T = 2 * np.pi * n
    def h(tau, part):
        G = Gtw_n(0.0, rho, tau, n); v = np.exp(-1j * q * tau / n) * 2 * G * G
        return v.real if part == 0 else v.imag
    pts = sorted({p for p in (rho, 3 * rho, T / 2, T - 3 * rho, T - rho) if 0 < p < T})
    return quad(h, 0, T, args=(0,), points=pts, limit=400, epsabs=0, epsrel=1e-11)[0]

def dBp(q, rho, dl=1e-3):
    d = (Breg(q, rho, 1 + dl) - Breg(q, rho, 1 - dl)) / (2 * dl)
    return d - abs(q) * rho * np.exp(-abs(q) * rho) / (8 * np.pi * np.sinh(rho)) - float(gdot(rho)) * K.g(abs(q), np.array([rho]))[0] / (2 * np.pi)

if __name__ == "__main__":
    for q, rho in ((0, 0.5), (1, 0.5), (2, 1.5)):
        b = Breg(q, rho, 1.0); c = np.exp(-abs(q) * rho) / (8 * np.pi * np.sinh(rho))
        print(f"gate q={q} rho={rho}: tau-space {b:.12e}  closed {c:.12e}  rel {b/c-1:+.1e}", flush=True)
    for q in (0, 1, 3):
        for rho in (1.0, 0.3, 0.1, 0.03, 0.01):
            t0 = time.time(); v1 = dBp(q, rho, 1e-3); v2 = dBp(q, rho, 2e-3)
            print(f"q={q} rho={rho}: dB'_q (step 1e-3) {v1:+.10e}  (2e-3) {v2:+.10e}  [{time.time()-t0:.0f}s]", flush=True)
