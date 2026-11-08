import csv,statistics as st,random,collections as C
from datetime import datetime as D
f=lambda s:D.strptime(s,'%Y-%m-%dT%H:%M:%SZ')
I=list(csv.DictReader(open('incidents.csv')));A={r['incident_id']:r for r in csv.DictReader(open('activity.csv'))}
for r in I:
    r['post']=f(r['opened_at'])>=D(2026,6,8)
    a=A.get(r['incident_id'])
    r['has']=a is not None
    if a:
        r['m']=(f(a['closed_at'])-f(r['opened_at'])).total_seconds()/60
        r['rm']=float(a['responder_minutes']);r['h']=float(a['handoffs']);r['ro']=float(a['reopened_within_72h'])
print('workflow vs post mismatch',sum((r['workflow']=='assist')!=r['post'] for r in I))
print('neg',sum(1 for r in I if r['has'] and r['m']<0))
def tab(keys):
    c=C.Counter(tuple(r[k] for k in keys) for r in I);return c
for ks in (['post','service_group','severity'],['post','intake_channel'],['post','severity']):
    print(ks);[print(' ',k,v) for k,v in sorted(tab(ks).items())]
print('missing');
for ks in (['post','severity'],['post','service_group'],['post','intake_channel']):
    c=C.Counter(tuple(r[k] for k in ks) for r in I if not r['has']);print(ks,sorted(c.items()))
def sm(rows,k):
    v=[r[k] for r in rows if r['has']]
    return (len(v),round(st.median(v),1),round(st.mean(v),1)) if v else None
for sev in ('all','sev1','sev2','sev3'):
  for p in (False,True):
    rows=[r for r in I if r['post']==p and (sev=='all' or r['severity']==sev)]
    print(sev,'post' if p else 'pre',{k:sm(rows,k) for k in('m','rm','h','ro')})
print('---- standardized')
random.seed(1)
pre_w={s:sum(1 for r in I if not r['post'] and r['severity']==s)/210 for s in('sev1','sev2','sev3')}
post_n={s:sum(1 for r in I if r['post'] and r['severity']==s) for s in pre_w}
def eff(rows,k,stat=st.mean):
    t=0
    for s,w in pre_w.items():
        a=[r[k] for r in rows if r['has'] and r['post'] and r['severity']==s]
        b=[r[k] for r in rows if r['has'] and not r['post'] and r['severity']==s]
        t+=w*(stat(a)-stat(b))
    return t
def boot(k,stat=st.mean,B=2000):
    g=C.defaultdict(list)
    for r in I:g[(r['post'],r['severity'])].append(r)
    out=[]
    for _ in range(B):
        rows=[x for L in g.values() for x in random.choices(L,k=len(L))]
        try: out.append(eff(rows,k,stat))
        except: pass
    out.sort();return out[int(.025*len(out))],out[int(.975*len(out))]
for k in('m','rm','h'):
    print(k,'pre-mix standardized post-pre mean diff',round(eff(I,k),1),'95% CI',[round(x,1) for x in boot(k)])
# raw median diff CI
def rawmed(rows,k):return st.median([r[k] for r in rows if r['has'] and r['post']])-st.median([r[k] for r in rows if r['has'] and not r['post']])
for k in('m','rm'):
    print(k,'raw median diff',rawmed(I,k))
# per-stratum mean diff CI
for s in('sev1','sev2','sev3'):
  for k in('m','rm'):
    a=[r[k] for r in I if r['has'] and r['post'] and r['severity']==s];b=[r[k] for r in I if r['has'] and not r['post'] and r['severity']==s]
    d=[st.mean(random.choices(a,k=len(a)))-st.mean(random.choices(b,k=len(b))) for _ in range(2000)];d.sort()
    print(s,k,round(st.mean(a)-st.mean(b),1),[round(d[50],1),round(d[1949],1)])
# total responder minutes per incident incl. missing; total hours
tot=lambda p:sum(r['rm'] for r in I if r['has'] and r['post']==p)
print('total rm pre/post',tot(False),tot(True),'mean/inc',tot(False)/209,tot(True)/200)
# reopen
print('reopens post',sum(r['ro'] for r in I if r['has'] and r['post']),'pre',sum(r['ro'] for r in I if r['has'] and not r['post']))
print('missing rows',[(r['incident_id'],r['opened_at'][:10],r['service_group'],r['severity']) for r in I if not r['has']])
# daily staffing vs counts and interruption
S=list(csv.DictReader(open('staffing.csv')))
for p in(False,True):
    x=[r for r in S if (r['date']>='2026-06-08')==p]
    print('post' if p else 'pre','resp',st.mean(int(r['active_responders']) for r in x),'hrs',st.mean(int(r['scheduled_responder_hours']) for r in x),'interrupt',st.mean(int(r['interruption_minutes']) for r in x),'inc/day',st.mean(int(r['incidents_opened']) for r in x))
# sensitivity: missing sev1 as unclosed -> close time >= 7d? 
print('sev1 post close mins', sorted(r['m'] for r in I if r['has'] and r['post'] and r['severity']=='sev1'))
print('sev1 pre close mins', sorted(r['m'] for r in I if r['has'] and not r['post'] and r['severity']=='sev1')[:30])
print('max close lag', max(r['m'] for r in I if r['has']))
