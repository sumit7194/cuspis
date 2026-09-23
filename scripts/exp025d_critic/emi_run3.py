from emi_general import *
import sys
which=sys.argv[1]
if which=="eye":
    for up in [1.5,3.0]:
        print(f"u'={up}: Fbar={Fbar(up):.9f} Fbar'={Fbarp(up):.9f}",flush=True)
        for u in [0.3,0.7,2.0,5.0]:
            r=R(u,eye_arc(up)); G=Fbar(u)-4*r; t=Fbar(up)+Fbarp(up)*(u-up)
            print(f"   u={u} R={r:.9f} G={G:.9f} tangent={t:.9f} diff={G-t:.2e}",flush=True)
else:
    A=float(which)
    us=[0.02,0.05,0.1,0.15,0.2]; Gs=[]
    for u in us:
        r=R(u,ellipse_arc(A)); G=Fbar(u)-4*r; Gs.append(G)
        print(f"ellipse A={A} u={u} R={r:.9f} Fbar={Fbar(u):.9f} G={G:.9f}",flush=True)
    us=np.array(us); Gs=np.array(Gs); c=np.polyfit(us,Gs,1)
    print("linear fit slope,intercept:",c," max residual:",np.max(abs(np.polyval(c,us)-Gs)))
    print("min over u of Fbar-G (should be >0, not touching):",min(Fbar(u)-g for u,g in zip(us,Gs)))
