import csv,statistics as st,random
from datetime import datetime as D
from collections import defaultdict,Counter
d='/var/folders/4_/s6fbcjyn4b13xdxkd3lv0kw00000gn/T/arm-s15-pre-3-szny70uq/data/s15-assist-rollout/'
P=lambda s:D.strptime(s,'%Y-%m-%dT%H:%M:%SZ')
I=list(csv.DictReader(open(d+'incidents.csv')));A={r['incident_id']:r for r in csv.DictReader(open(d+'activity.csv'))}
print(len(I),len(A),len(set(r['incident_id'] for r in I)),set(A)-set(r['incident_id'] for r in I))
for r in I:
    r['post']=P(r['opened_at'])>=D(2026,6,8)
    a=A.get(r['incident_id'])
    r['miss']=a is None
    if a:
        r['ttc']=(P(a['closed_at'])-P(r['opened_at'])).total_seconds()/3600
        r['min']=float(a['responder_minutes']);r['ho']=float(a['handoffs']);r['re']=float(a['reopened_within_72h'])
print('workflow vs date mismatch',Counter((r['post'],r['workflow']) for r in I))
def f(rows,k): 
    v=[r[k] for r in rows if k in r];return (len(v),round(st.median(v),2),round(st.mean(v),2)) if v else None
for key in ['severity','intake_channel','service_group']:
    print(key,'mix',{p:Counter(r[key] for r in I if r['post']==p) for p in (0,1)})
print('missing',{(p,s):(sum(r['miss'] for r in I if r['post']==p and r['severity']==s),sum(1 for r in I if r['post']==p and r['severity']==s)) for p in (0,1) for s in ('sev1','sev2','sev3')})
print('missing by group',{(p,s):sum(r['miss'] for r in I if r['post']==p and r['service_group']==s) for p in (0,1) for s in ('identity','storage')})
for lab,rows in [('all',I)]+[(s,[r for r in I if r['severity']==s]) for s in ('sev1','sev2','sev3')]+[(c,[r for r in I if r['intake_channel']==c]) for c in set(r['intake_channel'] for r in I)]:
    for k in ('ttc','min','ho','re'):
        print(lab,k,'pre',f([r for r in rows if not r['post']],k),'post',f([r for r in rows if r['post']],k))
# bootstrap median diff
random.seed(1)
def boot(k,rows):
    a=[r[k] for r in rows if not r['post'] and k in r];b=[r[k] for r in rows if r['post'] and k in r]
    ds=[st.median(random.choices(b,k=len(b)))-st.median(random.choices(a,k=len(a))) for _ in range(4000)]
    ds.sort();return round(st.median(b)-st.median(a),2),round(ds[100],2),round(ds[3899],2)
for k in ('ttc','min'):
    print('boot',k,'all',boot(k,I))
    for s in ('sev1','sev2','sev3'): print('boot',k,s,boot(k,[r for r in I if r['severity']==s]))
# total minutes among closed, per incident opened
for p in (0,1):
    rows=[r for r in I if r['post']==p]
    print('post',p,'sum min',sum(r.get('min',0) for r in rows),'n',len(rows),'closed',sum(not r['miss'] for r in rows))
print([ (r['incident_id'],r['severity'],r['post']) for r in I if r['miss']])
# daily
dd=defaultdict(list)
for r in I:
    if 'ttc' in r: dd[r['opened_at'][:10]].append(r['ttc'])
print({k:round(st.median(v),1) for k,v in sorted(dd.items())})
