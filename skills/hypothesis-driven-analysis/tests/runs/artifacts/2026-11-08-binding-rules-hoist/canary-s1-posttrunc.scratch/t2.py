import csv,random
d='/var/folders/4_/s6fbcjyn4b13xdxkd3lv0kw00000gn/T/arm-canary-s1-posttrunc-arl3whg1/data/s1-conversion/'
S=[r for r in csv.DictReader(open(d+'sessions.csv')) if r['landing_page']=='/lp/summer-sale']
for dd in sorted({r['timestamp'][:10] for r in S}):
    x=[r for r in S if r['timestamp'][:10]==dd];print(dd,sum(r['checkout_reached']=='yes' for r in x),len(x))
random.seed(2)
def diff(a,b):  # bootstrap diff post-pre in nonlp
    pass
# non-lp difference bootstrap: pre(6/8-9) vs post(6/10-14) and wk1
import itertools
A=[r for r in csv.DictReader(open(d+'sessions.csv')) if r['landing_page']!='/lp/summer-sale']
f=lambda r:1 if r['checkout_reached']=='yes' else 0
pre=[f(r) for r in A if '06-08'<=r['timestamp'][5:10]<='06-09'];post=[f(r) for r in A if r['timestamp'][5:10]>='06-10']
base=[f(r) for r in A if r['timestamp'][5:10]<='06-07']
for nm,a,b in(('post-pre',pre,post),('wk2nonlp-wk1',base,[f(r) for r in A if r['timestamp'][5:10]>='06-08'])):
    ds=sorted(sum(random.choices(b,k=len(b)))/len(b)-sum(random.choices(a,k=len(a)))/len(a) for _ in range(2000))
    print(nm,round(100*ds[50],2),round(100*ds[1949],2))
