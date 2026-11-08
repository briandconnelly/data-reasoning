import csv,sys,math,collections
r=list(csv.DictReader(open(sys.argv[1])))
print(len(r),len({x['request_id'] for x in r}))
bad=[x for x in r if not x['latency_ms'].strip()];print('missing',len(bad))
v=[(x['timestamp'],float(x['latency_ms'])) for x in r if x['latency_ms'].strip()]
print(collections.Counter(t[:10] for t,_ in v), v[0][0],v[-1][0])
l=sorted(y for _,y in v);n=len(l)
print('nearest-rank p95',l[math.ceil(.95*n)-1],'linear',l[int(.95*(n-1))]+(.95*(n-1)%1)*(l[int(.95*(n-1))+1]-l[int(.95*(n-1))]),'max',l[-1],'min',l[0],'n>500',sum(y>500 for y in l))
h=collections.defaultdict(list)
for t,y in v:h[t[11:13]].append(y)
for k in sorted(h):
    s=sorted(h[k]);print(k,len(s),s[math.ceil(.95*len(s))-1],s[-1])
print(sorted(v,key=lambda z:-z[1])[:6])
