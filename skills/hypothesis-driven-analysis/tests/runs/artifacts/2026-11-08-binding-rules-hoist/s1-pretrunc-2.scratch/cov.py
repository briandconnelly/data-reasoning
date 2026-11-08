import csv,collections as C
d='/var/folders/4_/s6fbcjyn4b13xdxkd3lv0kw00000gn/T/arm-s1-pretrunc-2-jry5744h/data/s1-conversion/'
S=list(csv.DictReader(open(d+'sessions.csv')));O=list(csv.DictReader(open(d+'orders.csv')))
print(len(S),len(O),sum(1 for r in S for v in r.values() if v==''),sum(1 for r in O for v in r.values() if v==''))
print(len({r['session_id'] for r in S}),len({r['order_id'] for r in O}))
print(min(r['timestamp'] for r in S),max(r['timestamp'] for r in S),min(r['timestamp'] for r in O),max(r['timestamp'] for r in O))
def ct(rows,k):
    c=C.Counter((r['timestamp'][:10],r[k]) for r in rows);ks=sorted({b for _,b in c})
    print('day',ks)
    for dd in sorted({a for a,_ in c}):print(dd,[c[(dd,x)] for x in ks])
ct(S,'device');ct(S,'landing_page');ct(S,'checkout_reached');ct(O,'client_version')
