"""n -> 1, stored office numbers only, k <= 2.5 (NO k = 3 file is opened). [model: Fable 5.2]
Per geometry: Sx = Sum_x sigdot = Sigma3D/Ny;  SA = Sum_x c_A sigdot = 2 X_cA/Ny;  w = SA/(c Sx) (sigdot-weighted c_A/c, c = hi end).
Per k: D1 = Sx(W1) - Sx(W2);  DA1 = SA(W1) - SA(W2);  raw counterterms y_A = -(1/2) Ny DA1, y_bulk = -(1/2) Ny c D1;  g_b = y_bulk - y_A."""
import json, numpy as np
R = '/Users/sumit/Github/corner_function/scripts/exp081d_results/'; JD = json.load(open(R[:-1] + '.json'))
c = json.load(open(R + 'exp085/E.json'))['ends']['hi c(384)']; ks = [1, 1.5, 2, 2.5]
def geo(W, P):
    g = json.load(open(R + f'exp085c/G_W{W}P{P}.json')); Ny = g['Ny']; return g['Sigma3D'] / Ny, 2 * g['X_cA'] / Ny, Ny
rows = []
for k in ks:
    W1, W2, P = int(2 * k), int(4 * k), int(4 * k); a = geo(W1, P); b = geo(W2, P); Ny = a[2]
    norm = 1 / (4 * P) / (1 / W1 - 1 / W2) / JD[str(k)]['kappa']
    w1, w2 = a[1] / (c * a[0]), b[1] / (c * b[0]); D1 = a[0] - b[0]; DA1 = a[1] - b[1]; yA = -0.5 * Ny * DA1; yb = -0.5 * Ny * c * D1
    rows.append((k, P, a[0], b[0], w1, w2, D1, DA1, yA, yb, norm))
    print(f"k={k}: Sx W1 {a[0]:+.5f} W2 {b[0]:+.5f} | w1 {w1:.4f} w2 {w2:.4f} (1-w)P: {(1-w1)*P:.3f} {(1-w2)*P:.3f} | D1 {D1:+.5f} DA1 {DA1:+.6f} | y_A {yA:+.5f} y_bulk {yb:+.5f} g_b {yb-yA:+.5f} | Y_A {yA*norm:+.4f} Y_bulk {yb*norm:+.4f} G_b {(yb-yA)*norm:+.4f}")
r = np.array(rows); gb = r[:, 9] - r[:, 8]
print("g_b:", np.round(gb, 5), " incr", np.round(np.diff(gb), 5)); print("y_A incr", np.round(np.diff(r[:, 8]), 5), " y_bulk incr", np.round(np.diff(r[:, 9]), 5), " ratio", np.round(np.diff(r[:, 9]) / np.diff(r[:, 8]), 4))
print("D1:", np.round(r[:, 6], 5), " incr", np.round(np.diff(r[:, 6]), 5))
print("same-W pairs in stored k <= 2.5 data: W4: P4 w2(k=1) %.4f vs P8 w1(k=2) %.4f ; (1-w)P %.3f vs %.3f" % (r[0, 5], r[2, 4], (1 - r[0, 5]) * 4, (1 - r[2, 4]) * 8))
print("             Sx at W=4: P4 %+.5f  P8 %+.5f" % (r[0, 3], r[2, 2]))
