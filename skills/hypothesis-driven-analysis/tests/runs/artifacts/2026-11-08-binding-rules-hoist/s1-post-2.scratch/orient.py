import csv,collections as C,sys
d='/var/folders/4_/s6fbcjyn4b13xdxkd3lv0kw00000gn/T/arm-s1-post-2-0pd3usjn/data/s1-conversion/'
s=list(csv.DictReader(open(d+'sessions.csv')));o=list(csv.DictReader(open(d+'orders.csv')))
print(min(r['timestamp'] for r in s),max(r['timestamp'] for r in s),min(r['timestamp'] for r in o),max(r['timestamp'] for r in o))
print('blank',{k:sum(1 for r in s if not r[k]) for k in s[0]},{k:sum(1 for r in o if not r[k]) for k in o[0]})
print(len({r['session_id'] for r in s}),len(s),len({r['order_id'] for r in o}),len(o))
for k in('device','landing_page','checkout_reached'):
    c=C.Counter((r['timestamp'][:10],r[k]) for r in s)
    ks=sorted({r[k] for r in s})
    print(k,ks)
    for dd in sorted({r['timestamp'][:10] for r in s}): print(dd,[c[(dd,x)] for x in ks])
print(sorted(C.Counter(r['timestamp'][:10] for r in o).items()))
