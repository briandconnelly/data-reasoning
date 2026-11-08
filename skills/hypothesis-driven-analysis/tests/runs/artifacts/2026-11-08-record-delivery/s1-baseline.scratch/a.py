import csv,sys,datetime as D
from collections import Counter,defaultdict
d=sys.argv[1]
def wk(t):
    x=D.date.fromisoformat(t[:10]);return x-D.timedelta(days=x.weekday())
S=list(csv.DictReader(open(d+'/sessions.csv')));O=list(csv.DictReader(open(d+'/orders.csv')))
print(S[0]['timestamp'],S[-1]['timestamp'],Counter(r['checkout_reached'] for r in S))
n=Counter();c=Counter();o=Counter()
for r in S:
    w=wk(r['timestamp']);n[w]+=1;c[w]+=r['checkout_reached']=='yes'
for r in O:o[wk(r['timestamp'])]+=1
for w in sorted(n):print(w,n[w],c[w],o[w],round(o[w]/n[w]*100,2),round(c[w]/n[w]*100,2))
for k in['landing_page','device']:
    t=defaultdict(lambda:[0,0])
    for r in S:
        x=t[(k and r[k],wk(r['timestamp']))];x[0]+=1;x[1]+=r['checkout_reached']=='yes'
    for key in sorted(t):print(k,key,t[key],round(t[key][1]/t[key][0],3))
v=Counter((wk(r['timestamp']),r['client_version']) for r in O)
for key in sorted(v):print(key,v[key])
dd=defaultdict(lambda:[0,0,0])
for r in S:
    x=dd[r['timestamp'][:10]];x[0]+=1;x[1]+=r['checkout_reached']=='yes'
for r in O:dd[r['timestamp'][:10]][2]+=1
for k in sorted(dd):print(k,dd[k])
