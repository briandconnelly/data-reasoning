exec(open('analysis.py').read().split("print('neg ttc'")[0])
print('== reopen/handoffs marginal')
for w in ['manual','assist']:
    l=sel(w);print(w,'reopen',sum(r['re'] for r in l),len(l),'handoffs mean %.2f'%st.mean(r['ho'] for r in l))
print('reopens by wf x sev',C.Counter((r['workflow'],r['severity']) for r in rows if r['ttc'] is not None and r['re']==1))
print('== sev1 assist closed')
for r in sel('assist','sev1'): print(r['incident_id'],r['service_group'],r['ttc'],r['min'],r['ho'],r['re'])
print('sev1 manual ttc range',min(r['ttc'] for r in sel('manual','sev1')),max(r['ttc'] for r in sel('manual','sev1')))
print('== ttc distribution assist sev3 vs manual sev3 quantiles')
def q(l,ps=(.1,.25,.5,.75,.9)):
    l=sorted(l);return [round(l[int(p*(len(l)-1))],2) for p in ps]
for w in ['manual','assist']:
    for s in ['sev1','sev2','sev3']:
        print(w,s,q([r['ttc'] for r in sel(w,s)]),q([r['min'] for r in sel(w,s)]))
print('== bounds: marginal mean min & ttc with 11 absent incidents (impute range)')
# impute absent with covered-row same wf x severity mean (neutral), and extreme: assist absent = severity-stratum max of manual/assist closed
for w in ['manual','assist']:
    l=sel(w);print(w,'closed-only mean ttc %.2f mean min %.1f'%(st.mean(r['ttc'] for r in l),st.mean(r['min'] for r in l)))
# absent assist incidents at 06-22 23:59 cap ttc (still-open) -> mean ttc lower bound
def meanttc_open(w):
    v=[r['ttc'] for r in sel(w)]
    for r in sel(w,closed=False):
        if r['ttc'] is None: v.append((ext-r['open']).total_seconds()/3600)
    return st.mean(v)
print('mean ttc absent=open at extract: manual %.2f assist %.2f'%(meanttc_open('manual'),meanttc_open('assist')))
print('median share of assist closed-only ttc that is > 2*stratum manual median?')
# severity-standardized responder minutes
fm=lambda l:st.mean([r['min'] for r in l])
pool=C.Counter(r['severity'] for r in rows);N=sum(pool.values())
cl=[r for r in rows if r['ttc'] is not None]
sd=lambda w,d:sum(pool[s]/N*fm([r for r in d if r['workflow']==w and r['severity']==s]) for s in pool)
print('standardized mean minutes m %.1f a %.1f diff %.1f'%(sd('manual',cl),sd('assist',cl),sd('assist',cl)-sd('manual',cl)))
# hours: counterfactual using manual per-severity mean minutes on assist-period mix
tot_a=sum(r['min'] for r in sel('assist'))/60
cf=sum(st.mean(r['min'] for r in sel('manual',s))*len(sel('assist',s)) for s in pool)/60
print('assist week actual resp hrs (closed)',tot_a,'counterfactual w/ manual per-sev rates',cf,'diff (neg=saved)',tot_a-cf)
print('raw total hrs manual week closed',sum(r['min'] for r in sel('manual'))/60)
# median headline x incidents
print('headline median diff*210 incidents',1.825*210)
# group-level and incident-level: sev share by group
print(C.Counter((r['workflow'],r['service_group'],r['severity']) for r in rows))
print('intake by severity by wf',C.Counter((r['workflow'],r['intake_channel'],r['severity']) for r in rows if r['severity']!='sev3'))
