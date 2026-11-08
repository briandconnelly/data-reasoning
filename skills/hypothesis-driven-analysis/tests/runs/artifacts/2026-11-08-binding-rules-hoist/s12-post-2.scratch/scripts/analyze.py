import csv,random,collections as C
random.seed(1)
s=list(csv.DictReader(open('data/s1-conversion/sessions.csv')))
for r in s: r['d']=r['timestamp'][:10]; r['y']=1 if r['checkout_reached']=='yes' else 0
def sel(f): return [r['y'] for r in s if f(r)]
def rate(x): return sum(x)/len(x)
def boot(a,b,n=4000):
    ds=[]
    for _ in range(n):
        ra=rate(random.choices(a,k=len(a)));rb=rate(random.choices(b,k=len(b)));ds.append(ra-rb)
    ds.sort();return ds[int(.025*n)],ds[int(.975*n)]
def show(n,a,b):
    lo,hi=boot(a,b);print(n,f"A={rate(a):.4f}(n={len(a)}) B={rate(b):.4f}(n={len(b)}) diff={rate(a)-rate(b):+.4f} CI95=[{lo:+.4f},{hi:+.4f}]")
pre=lambda r:r['d']<='2026-06-07'
w1=lambda r:'2026-06-08'<=r['d']<='2026-06-09'
w2=lambda r:'2026-06-10'<=r['d']<='2026-06-12'
nc=lambda r:r['landing_page']!='/lp/summer-sale'
show('T1 sitewide 06-08..09 vs pre',sel(w1),sel(pre))
show('T1b noncampaign 06-08..09 vs pre',sel(lambda r:w1(r) and nc(r)),sel(lambda r:pre(r)))
show('T2 noncampaign 06-10..12 vs 06-08..09',sel(lambda r:w2(r) and nc(r)),sel(lambda r:w1(r) and nc(r)))
show('T2b noncampaign 06-10..12 vs pre',sel(lambda r:w2(r) and nc(r)),sel(pre))
cw=lambda r:'2026-06-08'<=r['d']<='2026-06-12'
show('T3 campaign vs other 06-08..12',sel(lambda r:cw(r) and not nc(r)),sel(lambda r:cw(r) and nc(r)))
print('daily rate by page')
for d in sorted({r['d'] for r in s}):
    print(d,{p:round(rate(sel(lambda r:r['d']==d and r['landing_page']==p)),3) for p in ['/home','/product','/lp/summer-sale'] if sel(lambda r:r['d']==d and r['landing_page']==p)})
o=C.Counter(r['timestamp'][:10] for r in csv.DictReader(open('data/s1-conversion/orders.csv')))
print('T4 date orders vs yes');
for d in sorted(o):print(d,o[d],sum(sel(lambda r:r['d']==d)))
# T5 device standardization: pre device weights
def dev_rate(f,dv):
    x=sel(lambda r:f(r) and r['device']==dv);return rate(x)
wts={dv:len(sel(lambda r:pre(r) and r['device']==dv))/len(sel(pre)) for dv in['desktop','mobile']}
std=sum(wts[dv]*dev_rate(w1,dv) for dv in wts);print('T5 pre weights',wts,'std w1 rate',round(std,4),'raw w1',round(rate(sel(w1)),4),'pre',round(rate(sel(pre)),4))
for dv in wts:print(dv,'pre',round(dev_rate(pre,dv),4),'w1',round(dev_rate(w1,dv),4),'w2',round(dev_rate(w2,dv),4))
print('campaign page device mix',C.Counter(r['device'] for r in s if r['landing_page']=='/lp/summer-sale'))
