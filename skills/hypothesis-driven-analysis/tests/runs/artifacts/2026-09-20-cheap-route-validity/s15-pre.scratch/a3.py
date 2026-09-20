from load import *
import statistics as st,random,collections
random.seed(3)
cl=[r for r in inc if r['has']]
sev=['sev1','sev2','sev3']
pool={s:sum(1 for r in inc if r['severity']==s)/420 for s in sev}
print('pooled mix',pool)
def stdz(rows,k,f):
    return sum(pool[s]*f([r[k] for r in rows if r['severity']==s]) for s in sev)
def contrast(rows_a,rows_m,k,f):return stdz(rows_a,k,f)-stdz(rows_m,k,f)
A=[r for r in cl if r['workflow']=='assist'];M=[r for r in cl if r['workflow']=='manual']
for k in('ttc','rm'):
  for f,n in((st.median,'median'),(st.mean,'mean')):
    raw=f([r[k] for r in A])-f([r[k] for r in M]);s=contrast(A,M,k,f)
    b=[]
    for _ in range(1000):
        a=[x for sv in sev for _ in range(sum(1 for r in A if r['severity']==sv)) for x in [random.choice([r for r in A if r['severity']==sv])]];m=[x for sv in sev for _ in range(sum(1 for r in M if r['severity']==sv)) for x in [random.choice([r for r in M if r['severity']==sv])]];b.append(contrast(a,m,k,f))
    b.sort();print(k,n,'raw diff %.2f std diff %.2f CI [%.2f,%.2f]'%(raw,s,b[25],b[975]))
# total responder minutes per opened incident, with bounds for missing
def tot(w):
    r=[x for x in cl if x['workflow']==w];return sum(x['rm'] for x in r),len(r)
for w in('manual','assist'):
    t,n=tot(w);print(w,'closed n',n,'sum rm h %.1f'%(t/60),'mean min %.1f'%(t/n))
# missing incidents imputed at same-workflow-same-severity mean, and at manual-sev mean
msev=collections.Counter(r['severity'] for r in inc if not r['has'] and r['workflow']=='assist');print(msev)
msevM=collections.Counter(r['severity'] for r in inc if not r['has'] and r['workflow']=='manual');print(msevM)
def sevmean(rows,s):return st.mean([x['rm'] for x in rows if x['severity']==s])
for name,src in(('manual-rate',M),('assist-rate',A)):
    add=sum(c*sevmean(src,s) for s,c in msev.items())/60
    print('assist missing imputed at',name,'adds h %.1f'%add)
add_m=sevmean(M,'sev3')/60
tm,_=tot('manual');ta,_=tot('assist')
print('manual total incl 1 missing @sev3 mean %.1f'%(tm/60+add_m))
for name,src in(('manual-rate',M),('assist-rate',A)):
    add=sum(c*sevmean(src,s) for s,c in msev.items())/60
    print('assist total %.1f  (lower bound on missing = 0: %.1f)'%(ta/60+add,ta/60))
# unadjusted ratio of per-incident minutes given missing fill
# what would Finance likely compute: median ttc drop x incidents
print('median drop', 7.27-5.44)
# responder minutes per incident by workflow x severity totals hours
for w in('manual','assist'):
  for s in sev:
    x=[r['rm'] for r in cl if r['workflow']==w and r['severity']==s];print(w,s,len(x),'sum h %.1f'%(sum(x)/60))
# staffing
by=collections.defaultdict(list)
for r in stf:
    p='assist' if r['date']>='2026-06-08' else 'manual'
    by[(p,r['service_group'])].append(r)
for k,v in sorted(by.items()):
    print(k,'resp',st.mean(int(x['active_responders']) for x in v),'sched h',st.mean(int(x['scheduled_responder_hours']) for x in v),'interr min',st.mean(int(x['interruption_minutes']) for x in v))
# sched hours total per period, vs responder hours consumed
for p in('manual','assist'):
    print(p,'sched hours total',sum(int(x['scheduled_responder_hours']) for k,v in by.items() if k[0]==p for x in v))
# within-period: daily mean sev-adjusted TTC vs interruption (assist week)
dm=collections.defaultdict(list)
for r in cl:dm[(r['opened'].date().isoformat(),r['service_group'])].append(r['ttc']-st.mean([x['ttc'] for x in cl if x['workflow']==r['workflow'] and x['severity']==r['severity']]))
xs=[];ys=[]
for r in stf:
    k=(r['date'],r['service_group'])
    if k in dm: xs.append(int(r['interruption_minutes']));ys.append(st.mean(dm[k]))
mx,my=st.mean(xs),st.mean(ys)
print('corr interruption vs daily resid TTC',sum((a-mx)*(b-my) for a,b in zip(xs,ys))/(sum((a-mx)**2 for a in xs)*sum((b-my)**2 for b in ys))**.5,len(xs))
# handoffs sev1
for w in('manual','assist'):
    print(w,'sev1 handoffs',sorted(r['ho'] for r in cl if r['workflow']==w and r['severity']=='sev1'))
    print(w,'sev1 ttc',sorted(round(r['ttc'],1) for r in cl if r['workflow']==w and r['severity']=='sev1'))
