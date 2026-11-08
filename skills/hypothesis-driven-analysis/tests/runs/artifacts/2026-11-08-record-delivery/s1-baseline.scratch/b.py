import csv
from collections import Counter
d='../data/s1-conversion'
S=list(csv.DictReader(open(d+'/sessions.csv')));O=list(csv.DictReader(open(d+'/orders.csv')))
c=Counter()
for r in S:
    c[(r['timestamp'][:10],r['landing_page'],r['device'],'n')]+=1
    c[(r['timestamp'][:10],r['landing_page'],r['device'],'k')]+=r['checkout_reached']=='yes'
for k in sorted(c):
    if k[3]=='n' and k[0]>='2026-06-07':print(k[:3],c[k],c[k[:3]+('k',)])
v=Counter((r['timestamp'][:10],r['client_version']) for r in O)
for k in sorted(v):print(k,v[k])
print(sorted(set(r['timestamp'] for r in O if r['client_version']=='3.4.1'))[0])
import statistics
print(len({r['order_id'] for r in O}),len(O))
