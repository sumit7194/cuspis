"""Known-answer control on T46c's meshes: free z dS/dz -> -1/3 (strip, two edges) and -1/6 (single edge).
Uses T46c's own ConformalEllipticModel / SingleEdgeLogPolarModel and S_free_2d (production path)."""
import sys; sys.path.insert(0, sys.argv[1]); import numpy as np, brief_p2_t46c as T
h = 1e-3
def slope(op, k):  # dS/dln k at mass k
    return (op.S_free_2d(op.solve_q(k*np.exp(h))) - op.S_free_2d(op.solve_q(k*np.exp(-h))))/(2*h)
zs = [0.5, 1, 2, 3, 4, 5, 6, 8, 10]
print("strip (w=2, z=2k): z*dS/dz, target -1/3 = -0.3333 at large z (continuum)")
for Nth, mu in [(12, 4.0), (16, 4.0), (20, 4.0), (24, 4.0), (32, 4.0), (16, 6.5), (20, 6.5)]:
    op = T.ConformalEllipticModel(N_th=Nth, mu_max=mu)
    print(f"  N_th={Nth:2d} mu_max={mu} (h^2/2={0.5*(2*np.pi/Nth)**2:.3f}): " + " ".join(f"{z:g}:{slope(op, z/2):+.4f}" for z in zs), flush=True)
print("single edge (log-polar, Neumann hole): k*dS/dk, target -1/6 = -0.1667")
a_tip = 0.5*(2*np.pi/20)**2
for Nphi, umin in [(16, np.log(a_tip)), (24, np.log(a_tip)), (16, -5.0)]:
    se = T.SingleEdgeLogPolarModel(N_phi=Nphi, u_min=umin, u_max=3.2)
    print(f"  N_phi={Nphi} r_min={se.r_min:.4f}: " + " ".join(f"k={k:g}:{slope(se, k):+.4f}" for k in [0.25, 0.5, 1, 1.5, 2, 3]), flush=True)
