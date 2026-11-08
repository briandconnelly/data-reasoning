import csv,collections as C,sys
d='data/s1-conversion/'
s=list(csv.DictReader(open(d+'sessions.csv')));o=list(csv.DictReader(open(d+'orders.csv')))
print({k:sum(1 for r in s if not r[k]) for k in s[0]},{k:sum(1 for r in o if not r[k]) for k in o[0]})
print(C.Counter(r['checkout_reached'] for r in s),C.Counter(r['landing_page'] for r in s),C.Counter(r['device'] for r in s))
print(len(s),len({r['session_id'] for r in s}),len(o),len({r['order_id'] for r in o}))
days=sorted({r['timestamp'][:10] for r in s})
print('day  '+' '.join(sorted({r['landing_page'] for r in s})))
pages=sorted({r['landing_page'] for r in s});devs=sorted({r['device'] for r in s})
for dd in days:
    print(dd,[sum(1 for r in s if r['timestamp'][:10]==dd and r['landing_page']==p) for p in pages],[sum(1 for r in s if r['timestamp'][:10]==dd and r['device']==v) for v in devs],
      dict(C.Counter(r['client_version'] for r in o if r['timestamp'][:10]==dd)))
print(pages,devs)
