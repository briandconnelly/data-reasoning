import csv,math,random,sys
rows=list(csv.DictReader(open(sys.argv[1])))
d={}
for r in rows: d.setdefault(r['date'],{})[r['variant']]=(int(r['visits']),int(r['signups']))
assert all(len(v)==2 for v in d.values()); print(len(d),'days')
V={'A':0,'B':0};S={'A':0,'B':0}
for v in d.values():
  for k,(a,b) in v.items(): V[k]+=a;S[k]+=b
pa,pb=S['A']/V['A'],S['B']/V['B'];print(V,S,pa,pb)
diff=pb-pa;se=math.sqrt(pa*(1-pa)/V['A']+pb*(1-pb)/V['B'])
print('diff',diff,'CI',diff-1.96*se,diff+1.96*se,'rel',pb/pa-1)
# SRM
n=V['A']+V['B'];z=(V['A']-n/2)/math.sqrt(n/4);print('SRM z',z)
random.seed(1);days=list(d);ds=[];rs=[]
for _ in range(10000):
  s=[random.choice(days) for _ in days]
  a=sum(d[x]['A'][1] for x in s)/sum(d[x]['A'][0] for x in s)
  b=sum(d[x]['B'][1] for x in s)/sum(d[x]['B'][0] for x in s)
  ds.append(b-a);rs.append(b/a-1)
ds.sort();rs.sort();print('day-boot diff',ds[250],ds[9750],'rel',rs[250],rs[9750])
