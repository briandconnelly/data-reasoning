import csv,sys,random,statistics as st,collections as C
from datetime import datetime as dt
D=sys.argv[1];random.seed(1)
r=lambda f:list(csv.DictReader(open(D+'/'+f)))
i=r('incidents.csv');a={x['incident_id']:x for x in r('activity.csv')};s=r('staffing.csv')
P=lambda t:dt.strptime(t,'%Y-%m-%dT%H:%M:%SZ')
rows=[]
for x in i:
    y=a.get(x['incident_id'])
    x=dict(x)
    if y:
        x['ttc']=(P(y['closed_at'])-P(x['opened_at'])).total_seconds()/3600
        x['rm']=float(y['responder_minutes']);x['ho']=float(y['handoffs']);x['re']=float(y['reopened_within_72h'])
    else:x['ttc']=None
    rows.append(x)
cl=[x for x in rows if x['ttc'] is not None]
G=lambda rs,w:[x for x in rs if x['workflow']==w]
med=st.median
def boot(f,rs,n=2000):
    A=G(rs,'assist');M=G(rs,'manual');d=[]
    for _ in range(n):
        a_=[random.choice(A) for _ in A];m_=[random.choice(M) for _ in M]
        d.append(f(a_)-f(m_))
    d.sort();return d[int(.025*n)],d[int(.975*n)]
def rep(name,f,rs):
    A=G(rs,'assist');M=G(rs,'manual')
    if len(A)<3 or len(M)<3:print(name,'n',len(A),len(M));return
    lo,hi=boot(f,rs);print(f'{name}: assist {f(A):.2f} (n{len(A)}) manual {f(M):.2f} (n{len(M)}) diff {f(A)-f(M):.2f} CI[{lo:.2f},{hi:.2f}]')
print('neg ttc',sum(1 for x in cl if x['ttc']<0), 'ttc range',min(x['ttc'] for x in cl),max(x['ttc'] for x in cl))
print('== headline (closed only)')
rep('median ttc h',lambda r:med([x['ttc'] for x in r]),cl)
rep('mean ttc h',lambda r:st.mean([x['ttc'] for x in r]),cl)
rep('mean rm',lambda r:st.mean([x['rm'] for x in r]),cl)
rep('median rm',lambda r:med([x['rm'] for x in r]),cl)
print('== T2 mix')
for w in('manual','assist'):
    g=G(rows,w);print(w,{k:round(v/len(g),3) for k,v in sorted(C.Counter(x['severity'] for x in g).items())})
print('== T1 strata')
for sv in('sev1','sev2','sev3'):
    sub=[x for x in cl if x['severity']==sv]
    rep(f'{sv} median ttc',lambda r:med([x['ttc'] for x in r]),sub)
    rep(f'{sv} mean ttc',lambda r:st.mean([x['ttc'] for x in r]),sub)
    rep(f'{sv} mean rm',lambda r:st.mean([x['rm'] for x in r]),sub)
    rep(f'{sv} mean handoffs',lambda r:st.mean([x['ho'] for x in r]),sub)
    rep(f'{sv} reopen rate',lambda r:st.mean([x['re'] for x in r]),sub)
for g_ in('identity','storage'):
    sub=[x for x in cl if x['service_group']==g_]
    rep(f'{g_} median ttc',lambda r:med([x['ttc'] for x in r]),sub)
# standardized to manual mix
def std(f,rs):
    M=G(rs,'manual');w=C.Counter(x['severity'] for x in M)
    out={}
    for wf in('manual','assist'):
        out[wf]=sum(w[sv]*f([x for x in G(rs,wf) if x['severity']==sv]) for sv in w)/len(M)
    return out
print('standardized to manual mix, mean ttc',std(lambda r:st.mean([x['ttc'] for x in r]),cl))
print('standardized mean rm',std(lambda r:st.mean([x['rm'] for x in r]),cl))
print('raw mean ttc',{w:st.mean([x['ttc'] for x in G(cl,w)]) for w in('manual','assist')})
print('raw mean rm',{w:st.mean([x['rm'] for x in G(cl,w)]) for w in('manual','assist')})
# standardized median: reweight resample
def stdmed(rs,w_):
    tgt=C.Counter(x['severity'] for x in G(rs,'manual'))
    pool=[x for x in G(rs,w_)];by={sv:[x['ttc'] for x in pool if x['severity']==sv] for sv in tgt}
    return by,tgt
for w_ in('manual','assist'):
    by,tgt=stdmed(cl,w_)
    vals=[];
    for _ in range(4000):
        vals.append(random.choice(by['sev1'] if False else by[random.choices(list(tgt),list(tgt.values()))[0]]))
    print('std-median',w_,round(med(vals),2))
print('== T3 missing')
for w in('manual','assist'):
    g=G(rows,w);m=[x for x in g if x['ttc'] is None];print(w,len(m),len(g),C.Counter(x['severity'] for x in m))
print('sev1 missing rate assist',sum(1 for x in G(rows,'assist') if x['severity']=='sev1' and x['ttc'] is None),sum(1 for x in G(rows,'assist') if x['severity']=='sev1'))
# permutation test missing assist vs manual
mm=[(x['workflow']=='assist',x['ttc'] is None) for x in rows]
obs=sum(1 for a_,m_ in mm if a_ and m_);na=sum(1 for a_,_ in mm if a_);tot=sum(1 for _,m_ in mm if m_)
cnt=0
for _ in range(20000):
    smp=random.sample(range(len(mm)),na);k=sum(1 for j in smp if mm[j][1]);cnt+= (k>=obs)
print('perm p (assist missing>=obs)',cnt/20000)
# bounds: impute missing as open at extract (06-22 23:59) -> censored ttc
ext=P('2026-06-22T23:59:00Z')
rows2=[]
for x in rows:
    y=dict(x)
    if y['ttc'] is None:y['ttc']=(ext-P(y['opened_at'])).total_seconds()/3600
    rows2.append(y)
print('== bound: missing treated as still open (ttc lower bound)')
rep('median ttc all',lambda r:med([x['ttc'] for x in r]),rows2)
rep('mean ttc all',lambda r:st.mean([x['ttc'] for x in r]),rows2)
print('== T4 staffing')
for k in('active_responders','scheduled_responder_hours','interruption_minutes'):
    for g_ in('identity','storage'):
        b=[float(x[k]) for x in s if x['service_group']==g_ and x['date']<'2026-06-08'];c=[float(x[k]) for x in s if x['service_group']==g_ and x['date']>='2026-06-08']
        print(k,g_,'pre',round(st.mean(b),1),'post',round(st.mean(c),1))
# hours per incident vs ttc relation within each week by day
print('== daily median ttc by workflow week')
by=C.defaultdict(list)
for x in cl:by[x['opened_at'][:10]].append(x['ttc'])
print({d:round(med(v),1) for d,v in sorted(by.items())})
print('== T5 sev1/2 pooled hard')
hard=[x for x in cl if x['severity'] in('sev1','sev2')]
for m_,f in(('rm',lambda r:st.mean([x['rm'] for x in r])),('ho',lambda r:st.mean([x['ho'] for x in r])),('re',lambda r:st.mean([x['re'] for x in r])),('ttc',lambda r:st.mean([x['ttc'] for x in r]))):
    rep('hard mean '+m_,f,hard)
# all-severity handoffs reopens
rep('all handoffs',lambda r:st.mean([x['ho'] for x in r]),cl)
rep('all reopen',lambda r:st.mean([x['re'] for x in r]),cl)
# responder hours headline
nA=len(G(cl,'assist'));print('Finance-style: n assist closed',nA)
