import csv,math,random,collections as C
d='/var/folders/4_/s6fbcjyn4b13xdxkd3lv0kw00000gn/T/arm-s1-post-2-0pd3usjn/data/s1-conversion/'
s=list(csv.DictReader(open(d+'sessions.csv')));o=list(csv.DictReader(open(d+'orders.csv')))
wk=lambda t:1 if t<'2026-06-08' else 2
def w(p):return p[:2],p
def ci(k,n):
    p=k/n;z=1.96;c=(p+z*z/2/n)/(1+z*z/n);h=z*math.sqrt(p*(1-p)/n+z*z/4/n/n)/(1+z*z/n);return round(p,4),round(c-h,4),round(c+h,4)
def dci(k1,n1,k2,n2):
    p1,p2=k1/n1,k2/n2;se=math.sqrt(p1*(1-p1)/n1+p2*(1-p2)/n2);return round(p2-p1,4),round(p2-p1-1.96*se,4),round(p2-p1+1.96*se,4)
ow=C.Counter(wk(r['timestamp']) for r in o);sw=C.Counter(wk(r['timestamp']) for r in s)
print('T-def',ow,sw,[round(ow[i]/sw[i],4) for i in(1,2)])
def sub(f):
    n=C.Counter();k=C.Counter()
    for r in s:
        if f(r):n[wk(r['timestamp'])]+=1;k[wk(r['timestamp'])]+=r['checkout_reached']=='yes'
    return n,k
n,k=sub(lambda r:True);print('checkout-reached rate',[ci(k[i],n[i]) for i in(1,2)],'orders/chk',[ow[i]/k[i] for i in(1,2)])
n,k=sub(lambda r:r['landing_page']!='/lp/summer-sale')
print('T1 wk1',ci(ow[1],sw[1]),'wk2 excl SS (checkout_reached proxy=orders)',ci(k[2],n[2]),n)
n,k=sub(lambda r:r['landing_page']=='/lp/summer-sale');print('SS only',n,k,ci(k[2],n[2]))
for lp in('/home','/product'):
    n,k=sub(lambda r:r['landing_page']==lp);print(lp,ci(k[1],n[1]),ci(k[2],n[2]),dci(k[1],n[1],k[2],n[2]))
for dv in('desktop','mobile'):
    n,k=sub(lambda r:r['device']==dv);print(dv,n,ci(k[1],n[1]),ci(k[2],n[2]),dci(k[1],n[1],k[2],n[2]))
# T2: per-day orders vs checkout reached; pre/post 06-10 split
dy=C.Counter(r['timestamp'][:10] for r in s if r['checkout_reached']=='yes');od=C.Counter(r['timestamp'][:10] for r in o)
print('T5',all(dy[x]==od[x] for x in dy))
pre=[x for x in sorted(sw_ for sw_ in set(r['timestamp'][:10] for r in s)) if '06-08'<=x[5:]<='06-09'];post=[x for x in set(r['timestamp'][:10] for r in s) if '06-10'<=x[5:]<='06-14']
def tot(ds,f=lambda r:True):
    n=sum(1 for r in s if r['timestamp'][:10] in ds and f(r));k=sum(1 for r in s if r['timestamp'][:10] in ds and f(r) and r['checkout_reached']=='yes');return n,k
(n1,k1),(n2,k2)=tot(pre),tot(post);print('T2 session conv 06-08/09 vs 06-10..14',ci(k1,n1),ci(k2,n2),dci(k1,n1,k2,n2))
f=lambda r:r['landing_page']!='/lp/summer-sale'
(n1,k1),(n2,k2)=tot(pre,f),tot(post,f);print('T2 excl SS',ci(k1,n1),ci(k2,n2),dci(k1,n1,k2,n2))
# client_version mix of orders
print(sorted(C.Counter((wk(r['timestamp']),r['client_version']) for r in o).items()))
print('orders by day x version',sorted(C.Counter((r['timestamp'][5:10],r['client_version']) for r in o).items()))
# standardization by landing page: wk2 rate with wk1 mix (home/product only)
