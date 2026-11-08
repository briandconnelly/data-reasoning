import csv,random,math,collections
r=list(csv.DictReader(open('../data/signups.csv')))
d=collections.defaultdict(dict)
for x in r: d[x['date']][x['variant']]=(int(x['visits']),int(x['signups']))
print(len(r),len(d),[k for k,v in d.items() if set(v)!={'A','B'}])
print(all(s<=v for x in d.values() for v,s in x.values()))
T={'A':[0,0],'B':[0,0]}
for x in r:
    T[x['variant']][0]+=int(x['visits']);T[x['variant']][1]+=int(x['signups'])
print(T)
(na,sa),(nb,sb)=T['A'],T['B'];pa,pb=sa/na,sb/nb
se=math.sqrt(pa*(1-pa)/na+pb*(1-pb)/nb);df=pb-pa
print(pa,pb,df,df-1.96*se,df+1.96*se,pb/pa)
# srm
tot=na+nb;chi=(na-tot/2)**2/(tot/2)+(nb-tot/2)**2/(tot/2);print('srm chi2',chi)
# pooled z
p=(sa+sb)/tot;z=df/math.sqrt(p*(1-p)*(1/na+1/nb));print('z',z)
# day bootstrap
random.seed(1);ds=list(d);R=[];L=[]
for _ in range(10000):
    s=[random.choice(ds) for _ in ds]
    a=sum(d[k]['A'][1] for k in s)/sum(d[k]['A'][0] for k in s)
    b=sum(d[k]['B'][1] for k in s)/sum(d[k]['B'][0] for k in s)
    R.append(b-a);L.append(b/a-1)
R.sort();L.sort();print('boot diff',R[250],R[9749],'rel',L[250],L[9749])
# relative-lift delta interval
lse=math.sqrt((1-pa)/sa+(1-pb)/sb);print('rel',math.exp(math.log(pb/pa)-1.96*lse)-1,math.exp(math.log(pb/pa)+1.96*lse)-1)
w=sum(1 for k in ds if d[k]['B'][1]/d[k]['B'][0]>d[k]['A'][1]/d[k]['A'][0]);print('days B>A',w,'of',len(ds))
