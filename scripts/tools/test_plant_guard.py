"""Known-answer tests for tools/plant_guard.py on the real EXP-083 geometries. The guard must FIRE on the case that slipped
(W2P4, s_cut 1.5) and pass where the plants did fire. [model: Opus 5.5]"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sigma3d as S3
from exp083_honest import Geom
from tools.plant_guard import check_plant, derive_scut_plant, PlantInert
ok = True
def S_(W, P): g = Geom(W, P); return S3.Strip3D(g.Lx, g.Lt, g.Ny, g.cutx, g.tcut, s_cut=3.0)
cases = [((2, 4), "scut_low", 1.5, True), ((4, 4), "scut_low", 1.5, False), ((2, 4), "scut_low", 1.3, False),
         ((2, 2), "scut_low", 1.2, False), ((4, 2), "scut_low", 1.2, False)]
for (W, P), var, val, must_fire in cases:
    S = S_(W, P)
    try: r = check_plant(S, var, val); fired = False
    except PlantInert as e: r = str(e); fired = True
    good = fired == must_fire; ok &= good
    print(f"W{W}P{P} {var} {val}: {'INERT (guard fires)' if fired else 'changes input'} -> {'as expected' if good else 'UNEXPECTED'}  {r}")
for W, P in ((2, 2), (4, 2), (2, 4), (4, 4)):
    S = S_(W, P); d = derive_scut_plant(S); r = check_plant(S, "scut_low", d)
    for v in ("merge_tiny", "dd1", "drop_pole", "res_scale"):
        try: rv = check_plant(S, v); print(f"W{W}P{P} {v}: {rv}")
        except PlantInert as e: print(f"W{W}P{P} {v}: INERT {e}"); ok = False   # these all fired in the chain, so the guard must pass
    print(f"W{W}P{P} derived s_cut plant {d:.4f}: {r}")
print("ALL AS EXPECTED" if ok else "SOME UNEXPECTED"); sys.exit(0 if ok else 1)
