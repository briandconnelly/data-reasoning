import csv,random,statistics as S,collections as C
from datetime import datetime as D
f=lambda s:D.strptime(s,'%Y-%m-%dT%H:%M:%SZ')
I=list(csv.DictReader(open('incidents.csv')));A={r['incident_id']:r for r in csv.DictReader(open('activity.csv'))}
rows=[]
for r in I:
    a=A.get(r['incident_id']);o=f(r['opened_at'])
    r['ttc']=(f(a['closed_at'])-o).total_seconds()/3600 if a else None
    r['min']=float(a['responder_minutes']) if a else None
    r['ho']=float(a['handoffs']) if a else None
    r['re']=float(a['reopened_within_72h']) if a else None
    rows.append(r)
def g(w,sev=None,k='ttc',grp=None):
    return [r[k] for r in rows if r['workflow']==w and r[k] is not None and (sev is None or r['severity']==sev) and (grp is None or r['service_group']==grp)]
med=S.median
random.seed(1)
def bci(x,y,fn=med,n=4000):
    d=[]
    for _ in range(n):
        d.append(fn([random.choice(x) for _ in x])-fn([random.choice(y) for _ in y]))
    d.sort();return d[int(.025*n)],d[int(.975*n)]
print('overall TTC median manual/assist',med(g('manual')),med(g('assist')),'CI(a-m)',bci(g('assist'),g('manual')))
print('overall minutes mean',S.mean(g('manual',k='min')),S.mean(g('assist',k='min')))
print('overall minutes median',med(g('manual',k='min')),med(g('assist',k='min')))
for s in ['sev1','sev2','sev3']:
    for k in ['ttc','min','ho','re']:
        m,a=g('manual',s,k),g('assist',s,k)
        print(s,k,'n',len(m),len(a),'manual med/mean %.2f %.2f assist %.2f %.2f'%(med(m),S.mean(m),med(a),S.mean(a)),'CI med(a-m)',tuple(round(x,2) for x in bci(a,m)))
# standardized to manual mix
mix=C.Counter(r['severity'] for r in rows if r['workflow']=='manual')
tot=sum(mix.values())
for k in ['ttc','min']:
    sm=sum(mix[s]/tot*S.mean(g('manual',s,k)) for s in mix);sa=sum(mix[s]/tot*S.mean(g('assist',s,k)) for s in mix)
    print('std mean',k,sm,sa,sa-sm)
# mean ttc raw
print('mean ttc',S.mean(g('manual')),S.mean(g('assist')))
# T3 bounds: missing assist set to worst (max sev-specific manual 90th pct) etc
# imputation: missing get sev-specific assist-observed median x ; and worst = sev-specific 95th pct of manual
def q(x,p):x=sorted(x);return x[int(p*(len(x)-1))]
for label,fill in [('assist sev-median',lambda r:med(g('assist',r['severity']))),('manual sev-p90',lambda r:q(g('manual',r['severity']),.9)),('manual sev-median',lambda r:med(g('manual',r['severity'])))]:
    xs=[r['ttc'] if r['ttc'] is not None else fill(r) for r in rows if r['workflow']=='assist']
    print('assist overall median with missing filled by',label,med(xs))
    for s in ['sev1','sev2','sev3']:
        xs=[r['ttc'] if r['ttc'] is not None else fill(r) for r in rows if r['workflow']=='assist' and r['severity']==s]
        print('  ',s,med(xs),'manual',med(g('manual',s)))
# missing detail
for r in rows:
    if r['ttc'] is None:print(r['incident_id'],r['workflow'],r['service_group'],r['severity'],r['intake_channel'],r['opened_at'])
# group & channel stratification
for grp in ['identity','storage']:
    print(grp,'ttc med m/a',med(g('manual',grp=grp)),med(g('assist',grp=grp)),'min',S.mean(g('manual',k='min',grp=grp)),S.mean(g('assist',k='min',grp=grp)))
print(C.Counter((r['workflow'],r['intake_channel']) for r in rows))
for w in ['manual','assist']:
  print(w,'sev x channel',C.Counter((r['severity'],r['intake_channel']) for r in rows if r['workflow']==w))
# closed hours spill: ttc relative to opened; closures after 06-14? 
print('max ttc',max(r['ttc'] for r in rows if r['ttc']))
# total responder minutes
for w in ['manual','assist']:
    print(w,'total min',sum(g(w,k='min')),'n',len(g(w,k='min')))
print('---- extra')
print('mean min diff CI',bci(g('assist',k='min'),g('manual',k='min'),S.mean))
print('mean ttc diff CI',bci(g('assist'),g('manual'),S.mean))
print('median ttc diff pooled',med(g('assist'))-med(g('manual')))
print('sev3 share',{w:sum(r['severity']=='sev3' for r in rows if r['workflow']==w)/210 for w in ['manual','assist']})
st=list(csv.DictReader(open('staffing.csv')))
for w,lo,hi in [('pre','2026-06-01','2026-06-07'),('post','2026-06-08','2026-06-14')]:
    x=[r for r in st if lo<=r['date']<=hi]
    print(w,'resp',S.mean(int(r['active_responders']) for r in x),'sched hrs/day',S.mean(int(r['scheduled_responder_hours']) for r in x),'interrupt min',S.mean(int(r['interruption_minutes']) for r in x))
