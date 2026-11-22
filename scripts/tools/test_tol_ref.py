"""Known-answer test of tools/tol_ref.py at W4P4 (the slip-15 geometry): alias=True must take the 'paths differ' branch (mirror
poles differ by ~8.6e-8); alias=False (production behaviour) must take 'paths agree' (poles identical). [model: Opus 5.5]"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sigma3d as S3, exp083_armb as AB
from exp083_honest import Geom
from tools.tol_ref import ref_tol
g = Geom(4, 4); Sp = S3.Strip3D(g.Lx, g.Lt, g.Ny, g.cutx, g.tcut, s_cut=3.0); ok = True
for alias, want in ((True, "paths differ: larger used"), (False, "paths agree")):
    tol, info = ref_tol(3, 1.04e-10, 1e-10, Sp, AB.strip_sigma(g, None, alias=alias), own_dev=lambda: 2.32e-10)
    good = info["branch"] == want; ok &= good
    print(f"alias={alias}: branch '{info['branch']}' (|ds| {info['ds']:.1e}, residue rel {info['dr']:.1e}), tol {tol:.2e} -> {'as expected' if good else 'UNEXPECTED'}")
print("ALL AS EXPECTED" if ok else "SOME UNEXPECTED"); sys.exit(0 if ok else 1)
