import csv,random,collections as C
random.seed(1)
s=list(csv.DictReader(open('data/s1-conversion/sessions.csv')))
for r in s: r['d']=r['timestamp'][:10]; r['y']=r['checkout_reached']=='yes'; r['lp']=r['landing_page']=='/lp/summer-sale'
def sel(f): return [r for r in s if f(r)]
def rate(x): return sum(r['y'] for r in x)/len(x) if x else float('nan')
def boot(a,b,n=2000):
    ds=[]
    for _ in range(n):
        ra=[random.choice(a)['y'] for _ in a];rb=[random.choice(b)['y'] for _ in b]
        ds.append(sum(rb)/len(rb)-sum(ra)/len(ra))
    ds.sort();return ds[int(.025*n)],ds[int(.975*n)]
def cmp(name,a,b):
    lo,hi=boot(a,b);print(f"{name}: A={rate(a):.4f} (n={len(a)}) B={rate(b):.4f} (n={len(b)}) diff={rate(b)-rate(a):+.4f} 95%CI [{lo:+.4f},{hi:+.4f}]")
print('daily');
for d in sorted({r['d'] for r in s}):
    x=sel(lambda r:r['d']==d);print(d,f"all={rate(x):.3f} nonlp={rate([r for r in x if not r['lp']]):.3f} lp={rate([r for r in x if r['lp']]):.3f} home={rate([r for r in x if r['landing_page']=='/home']):.3f} prod={rate([r for r in x if r['landing_page']=='/product']):.3f}")
pre=lambda r:r['d']<='2026-06-07'; p1=lambda r:'2026-06-08'<=r['d']<='2026-06-09'; p2=lambda r:'2026-06-10'<=r['d']<='2026-06-12'; p3=lambda r:r['d']>='2026-06-13'
cmp('T1 all pre vs 06-08..09',sel(pre),sel(p1))
cmp('T1b nonlp pre vs nonlp 06-08..09',sel(lambda r:pre(r) and not r['lp']),sel(lambda r:p1(r) and not r['lp']))
cmp('T1c all pre vs 06-08..12',sel(pre),sel(lambda r:p1(r) or p2(r)))
cmp('T2 nonlp 06-08..09 vs 06-10..12',sel(lambda r:p1(r) and not r['lp']),sel(lambda r:p2(r) and not r['lp']))
cmp('T2b nonlp pre vs 06-10..12',sel(lambda r:pre(r) and not r['lp']),sel(lambda r:p2(r) and not r['lp']))
cmp('T2c lp 06-08..09 vs lp 06-10..12',sel(lambda r:p1(r) and r['lp']),sel(lambda r:p2(r) and r['lp']))
w=lambda r:'2026-06-08'<=r['d']<='2026-06-12'
for dev in ['desktop','mobile']:
    cmp(f'T3 {dev}: nonlp vs lp (06-08..12)',sel(lambda r:w(r) and not r['lp'] and r['device']==dev),sel(lambda r:w(r) and r['lp'] and r['device']==dev))
    cmp(f'  {dev}: pre all vs 06-08..12 nonlp',sel(lambda r:pre(r) and r['device']==dev),sel(lambda r:w(r) and not r['lp'] and r['device']==dev))
cmp('T3 lp vs nonlp pooled (06-08..12)',sel(lambda r:w(r) and not r['lp']),sel(lambda r:w(r) and r['lp']))
cmp('lp 06-08..12 vs pre /home+/product',sel(lambda r:pre(r)),sel(lambda r:w(r) and r['lp']))
for dev in ['desktop','mobile']:
    cmp(f'T4 {dev}: 06-08..12 vs 06-13/14',sel(lambda r:w(r) and r['device']==dev),sel(lambda r:p3(r) and r['device']==dev))
print('pre device rate',{v:round(rate(sel(lambda r:pre(r) and r['device']==v)),4) for v in ['desktop','mobile']})
