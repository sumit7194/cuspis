"""Post-seal arithmetic on stored numbers (nothing recomputed; no P = 10 saddle exists). [model: Fable 5.2]
(a) honest R_2 and the A counterterm in raw units (divide by norm): second differences; (b) Sum c_A sigdot (n -> 1) vs Sum c_A sigma_2 (n = 2)
per geometry: contact-like vs log-growing; (c) what different 3-point continuations of the counterterm give at l = 2.5 (shows the sensitivity)."""
import json, numpy as np
R = '/Users/sumit/Github/corner_function/scripts/exp081d_results/'; JD = json.load(open(R[:-1] + '.json'))
R2 = json.load(open(R + 'exp084/result.json'))['Rn']['2']; ends = json.load(open(R + 'exp085/E.json'))['ends']; chi = ends['hi c(384)']
ks = [1, 1.5, 2, 2.5]; norm = {k: 1 / (16 * k) / (1 / (2 * k) - 1 / (4 * k)) / JD[str(k)]['kappa'] for k in ks}
def geo(W, P):
    s = np.array(json.load(open(R + f'exp084c/c84_W{W}P{P}_n2.json'))['sigma']); g = json.load(open(R + f'exp085c/G_W{W}P{P}.json')); cA = np.array(g['cA'])
    return s.sum(), float(cA @ s), 2 * g['X_cA'] / g['Ny']
print("norm(k):", {k: round(v, 4) for k, v in norm.items()})
r2n = np.array([R2[str(k)] / norm[k] for k in ks]); print("(a) R_2/norm         :", np.round(r2n, 5), " incr", np.round(np.diff(r2n), 5), " 2nd diff", np.round(np.diff(r2n, 2), 5))
DA = []; D = []; rows = []
for k in ks[:3]:
    W1, W2, P = int(2 * k), int(4 * k), int(4 * k); a = geo(W1, P); b = geo(W2, P); DA.append(a[1] - b[1]); D.append(a[0] - b[0]); rows.append((k, W1, W2, P, a, b))
DA = np.array(DA); D = np.array(D); Ny = np.array([16, 24, 32.]); yan = -Ny * DA
print("    Y_A/norm = Ny|DA| :", np.round(yan, 5), " incr", np.round(np.diff(yan), 5), " 2nd diff", np.round(np.diff(yan, 2), 5))
print("    S/norm            :", np.round(r2n[:3] - yan, 5), " incr", np.round(np.diff(r2n[:3] - yan), 5))
print("    D = Sum s2(W1) - Sum s2(W2):", np.round(D, 5), "  DA:", np.round(DA, 6))
for t, c in ends.items():
    yb = Ny * c * D * np.array([norm[k] for k in ks[:3]]) * (-1) * (-1)     # dR2 bulk = Ny c D norm  (negative)
    inc = -np.diff(yb); r2inc = np.diff([R2[str(k)] for k in ks[:3]])
    print(f"    bulk [{t}]: dR2 {np.round(yb, 4)}; local overshoot ratio (1->1.5, 1.5->2): {np.round(inc / r2inc, 3)}; R2 + dR2 bulk {np.round(np.array([R2[str(k)] for k in ks[:3]]) + yb, 4)}")
print("(b) per geometry: Sum s2, Sum cA s2 (n = 2);  Sum cA sigdot (n -> 1);  each divided by c_hi*(1 - 2/P) to remove the interior c_A factor")
for k, W1, W2, P, a, b in rows:
    f = chi * (1 - 2 / P)
    print(f"    k={k}: W{W1}P{P}: s2 {a[0]:+.5f} cA.s2/f {a[1]/f:+.5f} cA.sigdot/f {a[2]/f:+.5f} | W{W2}P{P}: s2 {b[0]:+.5f} cA.s2/f {b[1]/f:+.5f} cA.sigdot/f {b[2]/f:+.5f}")
for W, P in ((5, 10), (10, 10)):
    g = json.load(open(R + f'exp085c/G_W{W}P{P}.json')); print(f"    k=2.5: W{W}P{P}: cA.sigdot/f {2*g['X_cA']/g['Ny']/(chi*(1-2/P)):+.5f}   (n -> 1 only; no sigma_2 here)")
print("(c) continuations to l = 2.5 (R_2(2.5) = %.4f, norm %.4f):" % (R2['2.5'], norm[2.5]))
def rep(lab, y): print(f"    {lab:58s} Y_A/norm {y:.5f} -> dR2A {-y*norm[2.5]:+.4f} -> S = {R2['2.5'] - y*norm[2.5]:+.4f}")
rep("Y_A/norm quadratic (constant 2nd difference)", yan[2] + (yan[2] - yan[1]) + (yan[2] - 2 * yan[1] + yan[0]))
sn = r2n[:3] - yan; rep("S/norm quadratic", r2n[3] - (sn[2] + (sn[2] - sn[1]) + (sn[2] - 2 * sn[1] + sn[0])))
rep("S/norm straight line from last two", r2n[3] - (2 * sn[2] - sn[1]))
rep("DA quadratic (no Ny), times Ny = 40", 40 * -(DA[2] + (DA[2] - DA[1]) + (DA[2] - 2 * DA[1] + DA[0])))
A = np.array([[1, -1, -1], [1, -1 / 1.5, -1 / 2.25], [1, -.5, -.25]]); co = np.linalg.solve(A, -DA); rep("|DA| = A - B/l - C/l^2 (saturating form), times 40", 40 * (co[0] - co[1] / 2.5 - co[2] / 6.25))
