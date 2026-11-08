import csv,collections as C
d='/var/folders/4_/s6fbcjyn4b13xdxkd3lv0kw00000gn/T/arm-canary-s1-posttrunc-arl3whg1/data/s1-conversion/'
S=list(csv.DictReader(open(d+'sessions.csv')));O=list(csv.DictReader(open(d+'orders.csv')))
print(len(S),len(O),S[0]['timestamp'],S[-1]['timestamp'],O[0]['timestamp'],O[-1]['timestamp'])
for r in S+O:
    assert all(v!='' for v in r.values()),r
print(len({r['session_id'] for r in S}),len({r['order_id'] for r in O}))
def tab(rows,k,f=lambda r:r['timestamp'][:10]):
    t=C.defaultdict(C.Counter)
    for r in rows:t[f(r)][r[k]]+=1
    for x in sorted(t):print(x,dict(t[x]))
tab(S,'device');tab(S,'landing_page');tab(S,'checkout_reached');tab(O,'client_version')
