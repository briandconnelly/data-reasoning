from load import *
import statistics as st,random
random.seed(2)
print('missing:');[print(r['incident_id'],r['opened_at'],r['service_group'],r['severity'],r['intake_channel'],r['workflow']) for r in inc if not r['has']]
# permutation: missing share by workflow
mw=[r['workflow']=='assist' for r in inc if not r['has']]
# exact hypergeometric p: 10 of 11 missing in assist (210/420)
from math import comb
p=sum(comb(210,k)*comb(210,11-k) for k in(10,11))/comb(420,11);print('P(>=10 of 11 assist)=',p)
# sev1: 5/14 vs 0/28 Fisher one-sided
p=comb(14,5)*comb(28,0)/comb(42,5);print('sev1 5 missing all in assist p=',p)
# extract age of missing
end=dt.datetime(2026,6,22,23,59)
print('ages h',[round((end-r['opened']).total_seconds()/3600) for r in inc if not r['has']])
# bounds: missing = still open, ttc >= age, treat as ttc=age (lower bound of true)
cl=[r for r in inc if r['has']]
def T(w,fill):
    x=[r['ttc'] for r in inc if r['workflow']==w and r['has']]
    if fill: x+= [(end-r['opened']).total_seconds()/3600 for r in inc if r['workflow']==w and not r['has']]
    return x
for f in(0,1):
  print('fill',f,{w:(round(st.median(T(w,f)),2),round(st.mean(T(w,f)),2),len(T(w,f))) for w in('manual','assist')})
# by day within workflow, severity-standardised: mean ttc sev3 by day
import collections
d=collections.defaultdict(list)
for r in cl:d[(r['opened'].date(),r['severity'])].append(r['ttc'])
for k in sorted(d):
    if k[1]=='sev3':print(k[0],k[1],len(d[k]),round(st.mean(d[k]),2))
