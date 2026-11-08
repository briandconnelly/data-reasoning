import csv,random,math
d='/var/folders/4_/s6fbcjyn4b13xdxkd3lv0kw00000gn/T/arm-s1-pretrunc-2-jry5744h/data/s1-conversion/'
S=list(csv.DictReader(open(d+'sessions.csv')))
for r in S:r['y']=r['checkout_reached']=='yes';r['w']=1 if r['timestamp']<'2026-06-08' else 2;r['post']=r['timestamp']>='2026-06-10T14:00'
def rate(x):return 100*sum(r['y'] for r in x)/len(x) if x else float('nan')
def ci(a,b,n=2000):
    random.seed(1);ds=[]
    for _ in range(n):
        A=[random.choice(a) for _ in a];B=[random.choice(b) for _ in b];ds.append(rate(B)-rate(A))
    ds.sort();return round(rate(b)-rate(a),2),round(ds[int(.025*n)],2),round(ds[int(.975*n)],2)
w1=[r for r in S if r['w']==1];w2=[r for r in S if r['w']==2]
print('overall w2-w1 (pp, 95%CI)',ci(w1,w2))
nl2=[r for r in w2 if r['landing_page']!='/lp/summer-sale']
print('excl summer-sale w2 vs w1',round(rate(nl2),2),round(rate(w1),2),ci(w1,nl2))
sl=[r for r in w2 if r['landing_page']=='/lp/summer-sale'];print('summer-sale',len(sl),round(rate(sl),2),'mobile share',round(100*sum(r['device']=='mobile' for r in sl)/len(sl)))
for dev in('desktop','mobile'):print(dev,'summer-sale',len([r for r in sl if r['device']==dev]),round(rate([r for r in sl if r['device']==dev]),2))
# within page+device, w1 vs w2 excluding summer-sale
for p in('/home','/product'):
  for dv in('desktop','mobile'):
    a=[r for r in w1 if r['landing_page']==p and r['device']==dv];b=[r for r in nl2 if r['landing_page']==p and r['device']==dv];print(p,dv,len(a),len(b),ci(a,b,1000))
# deploy: non-summer sessions pre vs post within w2, and w1 baseline
pre=[r for r in nl2 if not r['post']];post=[r for r in nl2 if r['post']];print('T1 pre/post deploy nonLP',len(pre),len(post),ci(pre,post))
sp=[r for r in sl if not r['post']];sq=[r for r in sl if r['post']];print('summer pre/post',len(sp),len(sq),ci(sp,sq))
# decomposition
sh=len(sl)/len(w2);print('share summer',round(sh,3),'counterfactual w2 rate if summer converted like others',round(rate(nl2),2),'dilution pp',round(rate(nl2)-rate(w2),2))
# 06-13/14 artifact: checkout rate & counts by day
for day in('2026-06-12','2026-06-13','2026-06-14'):
  x=[r for r in S if r['timestamp'][:10]==day];print(day,len(x),round(rate(x),2),{dv:(len([r for r in x if r['device']==dv]),round(rate([r for r in x if r['device']==dv]),2)) for dv in('desktop','mobile')})
