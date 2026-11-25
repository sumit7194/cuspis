"""h0(x) = P (G_inf(0) - G1_box(x,x)) at the strips' end positions, and the log-k coefficient this implies for Delta_bb against the exact bulk number. [model: Fable 5.2]"""
import numpy as np
GINF = 0.2527310098586630; y1 = 32 / (3 * np.pi ** 2)
def modes(L):
    j = np.arange(1, L + 1); return 2 - 2 * np.cos(np.pi * j / (L + 1)), np.sqrt(2 / (L + 1)) * np.sin(np.pi * np.outer(j, j) / (L + 1))
def h0_at(P, xs, ts):
    Lx, Lt, Ny = 3 * P, 2 * P, 4 * P; ex, Vx = modes(Lx); et, Vt = modes(Lt); m = 2 - 2 * np.cos(2 * np.pi * np.arange(Ny) / Ny); v = []
    for x in xs:
        for t in ts:
            w = np.outer(Vx[x] ** 2, Vt[t] ** 2); v.append(np.mean([(w / (ex[:, None] + et[None, :] + mm)).sum() for mm in m]))
    return P * (GINF - np.mean(v))
print("P : h0 centre | narrow-strip ends (x = 1.25P, 1.75P) | wide-strip ends (x = P, 2P)   [t = P-1, P]")
for P in (8, 16, 24, 40):
    ts = (P - 1, P); c = h0_at(P, (3 * P // 2 - 1, 3 * P // 2), ts)
    n = h0_at(P, (5 * P // 4 - 1, 5 * P // 4, 7 * P // 4 - 1, 7 * P // 4), ts); w = h0_at(P, (P - 1, P, 2 * P - 1, 2 * P), ts)
    print(f"  {P:3d}: {c:.5f} | {n:.5f} | {w:.5f}   (wide - narrow {w-n:+.5f})")
hn, hw = n, w; D1, Sbar, norm = 0.395, 3.6, 14.2
aL_raw = 2 * y1 * (0.5 * (hn + hw) * D1 + (hw - hn) * Sbar)
print(f"log coefficient of raw g_b against the exact bulk number: 2 y1 [hbar D1 + (h_w - h_n) |Sx|] = {aL_raw:.4f} per ln k  ->  {aL_raw*norm:.2f} in R units"
      f"   (uniform part {2*y1*0.5*(hn+hw)*D1*norm:.2f}, position part {2*y1*(hw-hn)*Sbar*norm:.2f})")
# what the stored k <= 2.5 numbers do when the bulk number is moved to c_inf = -0.1183 (arithmetic on brief numbers)
Yb = np.array([4.4737, 6.8406, 9.5555, 12.2847]); Gh = np.array([2.4920, 2.9765, 3.4507, 3.7567]); nm = np.array([14.1563, 13.7317, 14.0900, 14.3120]); k = np.array([1, 1.5, 2, 2.5])
for cinf in (-0.1175, -0.1183, -0.1190):
    G = Gh + Yb * (cinf / -0.11410550636913405 - 1); raw = G / nm; print(f"c_inf = {cinf}: G_b = {np.round(G, 3)}; raw {np.round(raw, 4)}; raw increments per ln k: {np.round(np.diff(raw)/np.diff(np.log(k)), 4)}")
