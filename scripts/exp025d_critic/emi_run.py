from emi_affine import *
for up in [0.5, 0.2, 0.9]:
    h=1e-5; Fp=(Fbar(up+h)-Fbar(up-h))/(2*h)
    print(f"u'={up}: Fbar(u')={Fbar(up):.9f} Fbar'(u')={Fp:.9f}")
    for u in [0.02,0.05,0.1,0.2,0.3,0.4,0.45,0.6,0.8]:
        if u>=up: continue
        r=R(u,up); G=Fbar(u)-4*r; tan=Fbar(up)+Fp*(u-up)
        print(f"   u={u:.3f} R={r:.9f} G={G:.9f} tangent={tan:.9f} G-tangent={G-tan:.2e}",flush=True)
