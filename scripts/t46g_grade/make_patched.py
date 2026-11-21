"""T46g grade: build the two instrumented scratch copies of Neon's T46g (brief_p2_t46g.py, sha256 426e751b...) into ./code/.
Neon's code is NOT committed here; pass its path. Patches (diagnostic only, no change at defaults):
 t46g_ntf.py: noise_tol multiplied by env NTF (default 1); raw delta spectrum recorded in DREC.
 t46g_mp.py : + when sigma is None and MPSPEC is set, (M_-^{1/2}, M_-^{-1/2}, delta, Y) are replaced by a supplied
              high-precision spectrum and modes are kept iff delta > MPFLOOR.   Usage: python -I make_patched.py <T46g.py>
[model: Opus 5.5]"""
import sys, os, hashlib
src = open(sys.argv[1]).read(); print("sha256", hashlib.sha256(src.encode()).hexdigest())
os.makedirs("code", exist_ok=True); open("code/brief_p2_t46g.py", "w").write(src)
def rep(s, a, b):
    assert a in s, a; return s.replace(a, b, 1)
s = rep(src, "import numpy as np\n", 'import numpy as np, os\nNTF = float(os.environ.get("NTF", "1"))\nDREC = []\n')
s = rep(s, "    deltas_raw, Y = sym_eig_complex(S_shift)\n", "    deltas_raw, Y = sym_eig_complex(S_shift); DREC.append(np.array(deltas_raw))\n")
s = rep(s, "noise_tol = max(16.0 * neg_noise, 32.0 * np.finfo", "noise_tol = NTF * max(16.0 * neg_noise, 32.0 * np.finfo")
s = rep(s, "noise_tol = 64.0 * np.finfo", "noise_tol = NTF * 64.0 * np.finfo")
open("code/t46g_ntf.py", "w").write(s)
s = rep(s, "DREC = []\n", "DREC = []\nMPSPEC = None\nMPFLOOR = 1e-14\n")
a = "    deltas_raw, Y = sym_eig_complex(S_shift); DREC.append(np.array(deltas_raw))\n"
s = rep(s, a, a + "    if sigma_vec is None and MPSPEC is not None:\n        Mm_h, Mm_ih, deltas_raw, Y = MPSPEC(op, q)\n")
a = "        deltas = np.where(deltas_raw.real > noise_tol, deltas_raw, 0.0 + 0.0j)\n"
s = rep(s, a, a + "        if sigma_vec is None and MPSPEC is not None: deltas = np.where(deltas_raw.real > MPFLOOR, deltas_raw, 0.0 + 0.0j)\n")
open("code/t46g_mp.py", "w").write(s)
