import csv, math, random
def pct(x,p):
    x=sorted(x); return x[int(p/100*(len(x)-1))]
rows=list(csv.DictReader(open('data/signups.csv')))
d={}
for r in rows: d.setdefault(r['date'],{})[r['variant']]=(int(r['visits']),int(r['signups']))
assert len(d)==14 and all(set(v)=={'A','B'} for v in d.values())
vA=sum(v['A'][0] for v in d.values()); sA=sum(v['A'][1] for v in d.values())
vB=sum(v['B'][0] for v in d.values()); sB=sum(v['B'][1] for v in d.values())
pA,pB=sA/vA,sB/vB
print("A",sA,vA,pA,"B",sB,vB,pB)
# SRM
z=(vA-vB)/math.sqrt(vA+vB); print("SRM z",z,"p",math.erfc(abs(z)/math.sqrt(2)))
diff=pB-pA; se=math.sqrt(pA*(1-pA)/vA+pB*(1-pB)/vB)
print("diff pp",diff*100,"CI",(diff-1.96*se)*100,(diff+1.96*se)*100,"z p",math.erfc(abs(diff/se)/math.sqrt(2)))
# rel lift log-RR
lrr=math.log(pB/pA); selr=math.sqrt(1/sA-1/vA+1/sB-1/vB)
print("RR",math.exp(lrr),"CI",math.exp(lrr-1.96*selr),math.exp(lrr+1.96*selr))
# day-level bootstrap of days (paired)
days=list(d); random.seed(1); bs=[];br=[]
for _ in range(20000):
    s=[random.choice(days) for _ in days]
    a=sum(d[x]['A'][1] for x in s)/sum(d[x]['A'][0] for x in s)
    b=sum(d[x]['B'][1] for x in s)/sum(d[x]['B'][0] for x in s)
    bs.append(b-a); br.append(b/a)
print("day-bootstrap diff pp",[pct(bs,2.5)*100,pct(bs,97.5)*100],"RR",[pct(br,2.5),pct(br,97.5)])
dd=([d[x]['B'][1]/d[x]['B'][0]-d[x]['A'][1]/d[x]['A'][0] for x in days])
dd=list(dd);M=sum(dd)/len(dd);SD=math.sqrt(sum((x-M)**2 for x in dd)/(len(dd)-1))
print("daily diffs mean pp",M*100,"sd",SD*100,"t",M/(SD/math.sqrt(len(dd))),"B>A days",sum(1 for x in dd if x>0))
# halves
for nm,sl in [("wk1",days[:7]),("wk2",days[7:])]:
    a=sum(d[x]['A'][1] for x in sl)/sum(d[x]['A'][0] for x in sl); b=sum(d[x]['B'][1] for x in sl)/sum(d[x]['B'][0] for x in sl)
    print(nm,a,b,(b-a)*100)
