import csv,collections as C
s=list(csv.DictReader(open('data/s1-conversion/sessions.csv')))
c=C.Counter((r['timestamp'][:10],r['landing_page'],r['device']) for r in s)
for dd in sorted({k[0] for k in c}):
    print(dd,' '.join(f"{p[:5]}/{v[:1]}={c[(dd,p,v)]}" for p in ['/home','/lp/summer-sale','/product'] for v in ['desktop','mobile']))
h=C.Counter((r['timestamp'][:10],r['timestamp'][11:13]) for r in s if r['timestamp'][:10] in('2026-06-12','2026-06-13'))
print(sorted(h.items()))
