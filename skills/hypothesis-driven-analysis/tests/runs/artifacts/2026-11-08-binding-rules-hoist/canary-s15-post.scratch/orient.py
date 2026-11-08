import csv,sys,collections as C
D=sys.argv[1]
r=lambda f:list(csv.DictReader(open(D+'/'+f)))
i=r('incidents.csv');a=r('activity.csv');s=r('staffing.csv')
print(len(i),len({x['incident_id'] for x in i}),len(a),len({x['incident_id'] for x in a}))
for n,t in(('i',i),('a',a),('s',s)):
    print(n,{k:sum(1 for x in t if x[k]=='') for k in t[0]})
ad={x['incident_id']:x for x in a}
print('act not in inc',set(ad)-{x['incident_id'] for x in i})
c=C.Counter();m=C.Counter()
for x in i:
    c[(x['opened_at'][:10],x['service_group'],x['workflow'])]+=1
    m[(x['opened_at'][:10],x['service_group'],x['incident_id'] in ad)]+=1
for k in sorted(c):print(k,c[k])
print('--activity coverage (date,group,present)')
for k in sorted(m):print(k,m[k])
print(C.Counter((x['workflow'],x['incident_id'] in ad) for x in i))
print(C.Counter((x['workflow'],x['severity'],x['incident_id'] in ad) for x in i))
print(C.Counter(x['intake_channel'] for x in i))
for x in s:print(x)
for x in i:
    if '2026-06-07T21'<x['opened_at']<'2026-06-08T03':print(x)
