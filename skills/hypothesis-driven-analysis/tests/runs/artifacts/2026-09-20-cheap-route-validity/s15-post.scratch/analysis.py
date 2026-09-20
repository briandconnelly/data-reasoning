import csv,random,statistics as st,collections as C
from datetime import datetime as D
D_='/var/folders/4_/s6fbcjyn4b13xdxkd3lv0kw00000gn/T/arm-s15-post-e3rjemnw/data/s15-assist-rollout/'
p=lambda s:D.strptime(s,'%Y-%m-%dT%H:%M:%SZ')
I=list(csv.DictReader(open(D_+'incidents.csv')));A={r['incident_id']:r for r in csv.DictReader(open(D_+'activity.csv'))}
S=list(csv.DictReader(open(D_+'staffing.csv')))
random.seed(1)
rows=[]
for r in I:
    a=A.get(r['incident_id'])
    r=dict(r); r['open']=p(r['opened_at'])
    if a:
        r['ttc']=(p(a['closed_at'])-r['open']).total_seconds()/3600
        r['min']=float(a['responder_minutes']);r['ho']=float(a['handoffs']);r['re']=float(a['reopened_within_72h'])
    else: r['ttc']=None
    rows.append(r)
ext=p('2026-06-22T23:59:00Z')
med=st.median
def sel(w=None,s=None,g=None,closed=True):
    return [r for r in rows if (w is None or r['workflow']==w) and (s is None or r['severity']==s) and (g is None or r['service_group']==g) and (not closed or r['ttc'] is not None)]
def boot(f,n=5000):
    xs=[]
    for _ in range(n): xs.append(f())
    xs.sort();return xs[int(.025*n)],xs[int(.975*n)]
def rs(l): return [random.choice(l) for _ in l]
print('neg ttc',sum(1 for r in rows if r['ttc'] is not None and r['ttc']<0))
print('== marginal (closed only)')
for w in ['manual','assist']:
    t=[r['ttc'] for r in sel(w)];m=[r['min'] for r in sel(w)]
    print(w,len(t),'med ttc %.2f mean %.2f | med min %.1f mean min %.1f'%(med(t),st.mean(t),med(m),st.mean(m)))
mt=[r['ttc'] for r in sel('manual')];at=[r['ttc'] for r in sel('assist')]
print('marg diff med ttc',med(at)-med(mt),boot(lambda:med(rs(at))-med(rs(mt))))
mm=[r['min'] for r in sel('manual')];am=[r['min'] for r in sel('assist')]
print('marg diff mean min',st.mean(am)-st.mean(mm),boot(lambda:st.mean(rs(am))-st.mean(rs(mm))),'total hrs manual/assist per incident',st.mean(mm)/60,st.mean(am)/60)
print('== by severity')
for s in ['sev1','sev2','sev3']:
    a_=sel('assist',s);m_=sel('manual',s)
    at_=[r['ttc'] for r in a_];mt_=[r['ttc'] for r in m_]
    am_=[r['min'] for r in a_];mm_=[r['min'] for r in m_]
    print(s,'n m/a',len(m_),len(a_),'med ttc m %.2f a %.2f diff %.2f CI %s'%(med(mt_),med(at_),med(at_)-med(mt_),tuple(round(x,2) for x in boot(lambda:med(rs(at_))-med(rs(mt_))))),
      '| mean min m %.1f a %.1f diff %.1f CI %s'%(st.mean(mm_),st.mean(am_),st.mean(am_)-st.mean(mm_),tuple(round(x,1) for x in boot(lambda:st.mean(rs(am_))-st.mean(rs(mm_))))),
      '| handoffs m %.2f a %.2f'%(st.mean([r['ho'] for r in m_]),st.mean([r['ho'] for r in a_])),
      '| reopen m %.3f a %.3f'%(st.mean([r['re'] for r in m_]),st.mean([r['re'] for r in a_])))
print('== severity mix (all opened)')
for w in ['manual','assist']:
    c=C.Counter(r['severity'] for r in sel(w,closed=False));print(w,dict(c))
print('== T3 standardization (pooled mix over all opened incidents), median-by-stratum weighted, and mean ttc')
pool=C.Counter(r['severity'] for r in rows);N=sum(pool.values())
def std(w,f,data):
    return sum(pool[s]/N*f([r for r in data if r['workflow']==w and r['severity']==s]) for s in pool)
cl=[r for r in rows if r['ttc'] is not None]
fm=lambda l:med([r['ttc'] for r in l]); fa=lambda l:st.mean([r['ttc'] for r in l])
print('std med-of-strata diff',std('assist',fm,cl)-std('manual',fm,cl),' std mean diff',std('assist',fa,cl)-std('manual',fa,cl),' marginal mean diff',st.mean(at)-st.mean(mt))
def sb(f):
    def g():
        d=[]
        for w in ['manual','assist']:
            for s in ['sev1','sev2','sev3']:
                d+=rs(sel(w,s))
        return std('assist',f,d)-std('manual',f,d)
    return g
print('CI std med',boot(sb(fm),2000),'CI std mean',boot(sb(fa),2000))
print('== by group (marginal and within severity)')
for g in ['identity','storage']:
    for w in ['manual','assist']:
        l=sel(w,None,g);print(g,w,len(l),'med ttc %.2f'%med([r['ttc'] for r in l]),'mean min %.1f'%st.mean([r['min'] for r in l]))
print('== T4 censoring bound')
ab=[r for r in sel('assist',closed=False) if r['ttc'] is None];mb=[r for r in sel('manual',closed=False) if r['ttc'] is None]
def cens(w,val):
    l=[r['ttc'] for r in sel(w)]
    for r in sel(w,closed=False):
        if r['ttc'] is None: l.append((ext-r['open']).total_seconds()/3600 if val=='open' else 0)
    return med(l),len(l)
for w in ['manual','assist']:
    print(w,'closed-only',med([r['ttc'] for r in sel(w)]),'absent=still open',cens(w,'open'))
print('missing counts by sev/wf',C.Counter((r['workflow'],r['severity']) for r in rows if r['ttc'] is None))
print('missing share by wf x sev',{(w,s):(len(sel(w,s,closed=False))-len(sel(w,s)),len(sel(w,s,closed=False))) for w in ['manual','assist'] for s in ['sev1','sev2','sev3']})
print('== daily series: median ttc, mean min per day')
for d in sorted({r['opened_at'][:10] for r in rows}):
    l=[r for r in rows if r['opened_at'][:10]==d and r['ttc'] is not None]
    print(d,len(l),'med ttc %.2f'%med([r['ttc'] for r in l]),'mean min %.0f'%st.mean([r['min'] for r in l]),'sev3 share %.2f'%(sum(r['severity']=='sev3' for r in rows if r['opened_at'][:10]==d)/30))
print('== staffing')
for w,dates in [('pre',range(1,8)),('post',range(8,15))]:
    l=[r for r in S if int(r['date'][-2:]) in dates]
    print(w,'active',st.mean(float(r['active_responders']) for r in l),'sched hrs/day/group',st.mean(float(r['scheduled_responder_hours']) for r in l),'interrupt',st.mean(float(r['interruption_minutes']) for r in l))
