import csv,random
d='/var/folders/4_/s6fbcjyn4b13xdxkd3lv0kw00000gn/T/arm-canary-s1-posttrunc-arl3whg1/data/s1-conversion/'
S=list(csv.DictReader(open(d+'sessions.csv')));O=list(csv.DictReader(open(d+'orders.csv')))
day=lambda r:r['timestamp'][:10]
W=lambda r:1 if day(r)<='2026-06-07' else 2
def rate(rows):
    n=len(rows);y=sum(r['checkout_reached']=='yes' for r in rows);return y,n,100*y/n if n else 0
def ci(rows,B=2000):
    v=[1 if r['checkout_reached']=='yes' else 0 for r in rows];m=[]
    for _ in range(B):m.append(sum(random.choices(v,k=len(v)))/len(v))
    m.sort();return round(100*m[50],2),round(100*m[1949],2)
random.seed(1)
for w in(1,2):
    print('wk',w,'orders',sum(W(o)==w for o in O),'sessions',sum(W(s)==w for s in S),'checkout_reached',rate([s for s in S if W(s)==w]))
    print(' orders/sessions %.2f'%(100*sum(W(o)==w for o in O)/sum(W(s)==w for s in S)))
print('T1 by page')
for w in(1,2):
  for p in('/home','/product','/lp/summer-sale'):
    r=[s for s in S if W(s)==w and s['landing_page']==p]
    if r:print(w,p,rate(r),ci(r))
print('T4 device')
for w in(1,2):
  for dv in('desktop','mobile'):
    r=[s for s in S if W(s)==w and s['device']==dv];print(w,dv,rate(r),len(r))
print('T1b lp by device wk2')
for dv in('desktop','mobile'):
    r=[s for s in S if W(s)==2 and s['landing_page']=='/lp/summer-sale' and s['device']==dv];print(dv,rate(r))
print('T2 non-lp daily')
for dd in sorted({day(s) for s in S}):
    r=[s for s in S if day(s)==dd and s['landing_page']!='/lp/summer-sale'];print(dd,rate(r))
pre=[s for s in S if '2026-06-08'<=day(s)<='2026-06-09' and s['landing_page']!='/lp/summer-sale']
post=[s for s in S if '2026-06-10'<=day(s)<='2026-06-14' and s['landing_page']!='/lp/summer-sale']
w1=[s for s in S if W(s)==1]
print('nonlp wk1',rate(w1),ci(w1));print('nonlp 6/8-9',rate(pre),ci(pre));print('nonlp 6/10-14',rate(post),ci(post))
print('T3 per-day sessions/orders');
import collections as C
oc=C.Counter(day(o) for o in O);sc=C.Counter(day(s) for s in S);yc=C.Counter(day(s) for s in S if s['checkout_reached']=='yes')
for k in sorted(sc):print(k,sc[k],yc[k],oc[k])
a=[s for s in S if W(s)==2 and day(s)<='2026-06-12'];print('wk2 excl 13/14 orders/sessions',sum(o['timestamp'][:10]<='2026-06-12' and W(o)==2 for o in O),len(a))
print('lp share wk2',sum(s['landing_page']=='/lp/summer-sale' for s in S if W(s)==2)/sum(W(s)==2 for s in S))
