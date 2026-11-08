import csv,collections as C,random
S=list(csv.DictReader(open('data/s1-conversion/sessions.csv')))
O=list(csv.DictReader(open('data/s1-conversion/orders.csv')))
ds=C.Counter(s['timestamp'][:10] for s in S); do=C.Counter(o['timestamp'][:10] for o in O)
dc=C.Counter(s['timestamp'][:10] for s in S if s['checkout_reached']=='yes')
days=sorted(ds)
print('day sess orders conv% chk%')
for d in days: print(d,ds[d],do[d],round(100*do[d]/ds[d],2),round(100*dc[d]/ds[d],2))
def rate(ds_):
    return sum(do[d] for d in ds_)/sum(ds[d] for d in ds_)
w1=days[:7];w2=days[7:]
print('wk1',rate(w1),'wk2',rate(w2))
print('pre-deploy 06-08..09',rate(days[7:9]),'06-10..12',rate(days[9:12]),'06-13..14',rate(days[12:]))
print('full cov',rate(days[:5]),rate(days[7:12]))
random.seed(1)
def boot(a,b,n=5000):
    r=[]
    for _ in range(n):
        x=[random.choice(a) for _ in a];y=[random.choice(b) for _ in b]
        r.append(rate2(y)-rate2(x))
    r.sort();return r[int(.025*n)],r[int(.975*n)]
def rate2(l): return sum(do[d] for d in l)/sum(ds[d] for d in l)
print('contrast wk2-wk1 95% CI',boot(w1,w2))
print('wk1 daily-block CI',boot(w1,w1))
# segments
for wk,name in((w1,'wk1'),(w2,'wk2')):
    seg=C.Counter((s['device'],s['landing_page']) for s in S if s['timestamp'][:10] in wk)
    ch=C.Counter((s['device'],s['landing_page']) for s in S if s['timestamp'][:10] in wk and s['checkout_reached']=='yes')
    n=sum(seg.values());print(name,n)
    for k in sorted(seg): print(' ',k,seg[k],round(seg[k]/n,3),round(ch[k]/seg[k]*100,2))
# standardize chk rate
def segs(wk):
    seg=C.Counter((s['device'],s['landing_page']) for s in S if s['timestamp'][:10] in wk)
    ch=C.Counter((s['device'],s['landing_page']) for s in S if s['timestamp'][:10] in wk and s['checkout_reached']=='yes')
    return seg,ch
s1,c1=segs(w1);s2,c2=segs(w2)
n1=sum(s1.values());n2=sum(s2.values())
r1=sum(c1.values())/n1;r2=sum(c2.values())/n2
std=sum(s1[k]/n1*(c2[k]/s2[k]) for k in s1)
print('chk rate wk1',r1,'wk2',r2,'wk2 std to wk1 mix',std)
# versions by day
cv=C.Counter((o['timestamp'][:10],o['client_version']) for o in O)
for d in days: print(d,cv[(d,'3.4.0')],cv[(d,'3.4.1')])
# first 3.4.1 order
print(min(o['timestamp'] for o in O if o['client_version']=='3.4.1'),max(o['timestamp'] for o in O if o['client_version']=='3.4.0'))
# hourly deploy boundary: conv before/after 06-10T14
def per(lo,hi):
    s=sum(1 for x in S if lo<=x['timestamp']<hi);o=sum(1 for x in O if lo<=x['timestamp']<hi);return s,o,o/s
print('06-08..06-10T14',per('2026-06-08','2026-06-10T14'),'after to 06-14',per('2026-06-10T14','2026-06-15'),'wk1',per('2026-06-01','2026-06-08'))
