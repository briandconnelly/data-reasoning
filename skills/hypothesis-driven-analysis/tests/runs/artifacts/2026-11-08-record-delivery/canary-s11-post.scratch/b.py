import csv,sys,random,math
from collections import Counter,defaultdict
r=list(csv.DictReader(open(sys.argv[1])))
print(len(r), len({x['request_id'] for x in r}))
bad=[x for x in r if not x['latency_ms'].strip()]; print('missing',len(bad))
ts=sorted(x['timestamp'] for x in r); print(ts[0],ts[-1])
print(Counter(x['timestamp'][:10] for x in r))
print(Counter(len(x['timestamp']) for x in r))
seen=set(); v=[];byh=defaultdict(list)
for x in r:
    if x['request_id'] in seen or not x['latency_ms'].strip(): continue
    seen.add(x['request_id'])
    if x['timestamp'].startswith('2026-07-15'):
        l=float(x['latency_ms']); v.append(l); byh[x['timestamp'][11:13]].append(l)
v.sort(); n=len(v); print('n',n,'min',v[0],'max',v[-1])
def pct(s,p):
    k=(len(s)-1)*p; f=math.floor(k); c=min(f+1,len(s)-1); return s[f]+(s[c]-s[f])*(k-f)
print('p95 linear',pct(v,.95),'nearest-rank',v[math.ceil(.95*n)-1])
print('n>500',sum(a>500 for a in v), 'top5',v[-5:])
# order-stat CI via binomial
def bcdf(k,n,p): return sum(math.exp(math.lgamma(n+1)-math.lgamma(i+1)-math.lgamma(n-i+1)+i*math.log(p)+(n-i)*math.log(1-p)) for i in range(k+1))
lo=next(k for k in range(n) if bcdf(k,n,.95)>=.025); hi=next(k for k in range(n) if bcdf(k,n,.95)>=.975)
print('CI95 ranks',lo,hi,v[max(lo-1,0)],v[min(hi,n-1)])
random.seed(0); b=sorted(pct(sorted(random.choices(v,k=n)),.95) for _ in range(2000)); print('boot',b[50],b[1949])
for h in sorted(byh): s=sorted(byh[h]); print(h,len(s),round(pct(s,.95),1),s[-1])
