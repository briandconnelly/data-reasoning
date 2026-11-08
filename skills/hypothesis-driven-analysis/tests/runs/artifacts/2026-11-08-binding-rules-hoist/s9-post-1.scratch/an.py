import csv,sys,random,collections
r=list(csv.DictReader(open(sys.argv[1])))
d=collections.defaultdict(dict)
for x in r: d[x['date']][x['variant']]=(int(x['visits']),int(x['signups']))
print(len(d),"dates", sorted(d)[0],sorted(d)[-1])
print("incomplete days:",[k for k,v in d.items() if len(v)!=2], "dup rows:",len(r)-sum(len(v) for v in d.values()))
print("bad:",[x for x in r if int(x['signups'])>int(x['visits']) or int(x['visits'])<=0])
T={v:[0,0] for v in 'AB'}
for k,v in d.items():
  for a in v: T[a][0]+=v[a][0];T[a][1]+=v[a][1]
print(T)
pa=T['A'][1]/T['A'][0];pb=T['B'][1]/T['B'][0];print(pa,pb,pb-pa,pb/pa-1)
import math
se=math.sqrt(pa*(1-pa)/T['A'][0]+pb*(1-pb)/T['B'][0]);print("wald diff CI",pb-pa-1.96*se,pb-pa+1.96*se)
days=[k for k,v in d.items() if len(v)==2]
random.seed(1);ds=[];rs=[]
for _ in range(10000):
  s=[random.choice(days) for _ in days]
  a=[sum(d[k]['A'][i] for k in s) for i in(0,1)];b=[sum(d[k]['B'][i] for k in s) for i in(0,1)]
  ds.append(b[1]/b[0]-a[1]/a[0]);rs.append((b[1]/b[0])/(a[1]/a[0]))
ds.sort();rs.sort();print("boot diff",ds[250],ds[9750],"rr",rs[250],rs[9750])
for k in sorted(d):print(k,*(f"{v}:{d[k][v][0]},{d[k][v][1]}" for v in d[k]))
