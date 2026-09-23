import mpmath as mp
mp.mp.dps=40
def a_emi(th): return 1+(mp.pi-th)*mp.cot(th)
def a_min(th): return -mp.log(mp.sin(th/2))  # 8 sigma dropped
def F(u,a):
    th=4*mp.atan(mp.sqrt(u)); return mp.sqrt(u)*a(th)
for name,a in [('EMI',a_emi),('amin',a_min)]:
    print(name)
    bad=[]
    for k in range(1,400):
        u=mp.mpf(k)/100  # u in (0,4): theta up to ~4.43 rad
        th=4*mp.atan(mp.sqrt(u))
        if abs(th-mp.pi)<1e-6: continue
        d2=mp.diff(lambda x:F(x,a),u,2)
        if d2<0: bad.append((float(u),float(th),float(d2)))
    print(' n negative F\'\' :',len(bad), bad[:3], bad[-3:] if bad else '')
    for u in [0.01,0.1,0.5,1,2,4,10,50]:
        print('  u=%g th=%.4f F=%.6g F\'\'=%.6g'%(u,float(4*mp.atan(mp.sqrt(u))),float(F(mp.mpf(u),a)),float(mp.diff(lambda x:F(x,a),mp.mpf(u),2))))
