import csv, sys
from datetime import date, timedelta
from collections import defaultdict
rows=[(date.fromisoformat(r['date']),int(r['tickets'])) for r in csv.DictReader(open(sys.argv[1]))]
ds=[d for d,_ in rows]
print(len(rows), ds[0], ds[-1], 'dups', len(ds)-len(set(ds)))
full={ds[0]+timedelta(i) for i in range((ds[-1]-ds[0]).days+1)}
print('missing dates', sorted(full-set(ds))[:10], len(full-set(ds)))
v=[y for _,y in rows]; print('min/max', min(v), max(v))
m=defaultdict(list)
for d,y in rows: m[(d.year,d.month)].append(y)
for k in sorted(m): print(k, len(m[k]), sum(m[k]), round(sum(m[k])/len(m[k])))
