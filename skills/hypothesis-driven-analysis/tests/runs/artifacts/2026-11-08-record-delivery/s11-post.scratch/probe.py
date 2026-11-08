import sys,csv,math
from collections import Counter,defaultdict

def ppf(q,n,p):
    c=0
    for k in range(n+1):
        c+=math.exp(math.lgamma(n+1)-math.lgamma(k+1)-math.lgamma(n-k+1)+k*math.log(p)+(n-k)*math.log(1-p))
        if c>=q: return k
rows=list(csv.DictReader(open(sys.argv[1])))
print(len(rows), rows[0], rows[-1])
ts=[r['timestamp'] for r in rows]; print(min(ts),max(ts))
print('days',Counter(t[:10] for t in ts))
print('dup ids',len(rows)-len({r['request_id'] for r in rows}),'blank',sum(1 for r in rows if not r['latency_ms'] or not r['timestamp']))
d=[r for r in rows if r['timestamp'].startswith('2026-07-15')]
h=defaultdict(list)
for r in d:
    h[r['timestamp'][11:13]].append(float(r['latency_ms']))
def p95(v):
    v=sorted(v);return v[math.ceil(.95*len(v))-1]
for k in sorted(h): print(k,len(h[k]),round(p95(h[k]),1),max(h[k]))
v=sorted(float(r['latency_ms']) for r in d); n=len(v)
print('n',n,'p95',p95(v),'max',v[-1],'min',v[0], 'count>500',sum(x>500 for x in v))
# order-stat CI for quantile .95
lo=ppf(.025,n,.95); hi=ppf(.975,n,.95)+1
print('CI',v[max(lo-1,0)],v[min(hi-1,n-1)],lo,hi)

# bound for missing 20-23h: 240 missing of 1440 min; how much could p95 move?
import random
# worst case: all 240 missing rows > 500 => overall n=1440
full=sorted(v+[501.0]*240); print('worst-case p95 if all 240 missing rows >500:',full[math.ceil(.95*1440)-1])
need=math.ceil(.05*1440); print('rows >500 needed for p95>500 in 1440:',need, 'have',sum(x>500 for x in v),'so missing must supply',need-sum(x>500 for x in v)+0)
