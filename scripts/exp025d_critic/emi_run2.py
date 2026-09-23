from emi_affine import *
def Fb(u):
    return Fbar(u)
for up in [0.5, 1.5, 3.0]:
    h=1e-5; Fp=(Fb(up+h)-Fb(up-h))/(2*h)
    print(f"u'={up}: Fbar(u')={Fb(up):.9f} Fbar'(u')={Fp:.9f}")
    for u in [0.1,0.3,0.7,1.2,2.0,4.0,8.0]:
        if abs(u-up)<1e-9 or abs(u-1)<1e-9: continue
        r=R(u,up); G=Fb(u)-4*r; tan=Fb(up)+Fp*(u-up)
        print(f"   u={u:.3f} R={r:.9f} G={G:.9f} tangent={tan:.9f} G-tangent={G-tan:.2e}",flush=True)
# control: a deliberately wrong trial region (half-ellipse instead of u'-eye) should NOT give a line touching F
