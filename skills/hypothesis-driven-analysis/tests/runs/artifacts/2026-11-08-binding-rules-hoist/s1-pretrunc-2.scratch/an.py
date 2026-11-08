import csv,collections as C
d='/var/folders/4_/s6fbcjyn4b13xdxkd3lv0kw00000gn/T/arm-s1-pretrunc-2-jry5744h/data/s1-conversion/'
S=list(csv.DictReader(open(d+'sessions.csv')));O=list(csv.DictReader(open(d+'orders.csv')))
wk=lambda t:1 if t<'2026-06-08' else 2
for w in(1,2):
    s=[r for r in S if wk(r['timestamp'])==w];o=[r for r in O if wk(r['timestamp'])==w]
    print('week',w,len(s),len(o),round(100*len(o)/len(s),2),'chk',round(100*sum(r['checkout_reached']=='yes' for r in s)/len(s),2))
    for k in('landing_page','device'):
        for v in sorted({r[k] for r in s}):
            x=[r for r in s if r[k]==v];print(' ',k,v,len(x),'checkout%',round(100*sum(r['checkout_reached']=='yes' for r in x)/len(x),2))
# T1: before/after deploy within week2 and checkout rate by page
D='2026-06-10T14:00'
for lab,f in(('wk2 pre-deploy',lambda t:'2026-06-08'<=t<D),('wk2 post-deploy',lambda t:t>=D)):
    s=[r for r in S if f(r['timestamp'])];o=[r for r in O if f(r['timestamp'])]
    n=[r for r in s if r['landing_page']!='/lp/summer-sale'];print(lab,'sessions',len(s),'nonLP',len(n),'orders',len(o),'orders/nonLP-sessions%',round(100*len(o)/len(n),2),'orders/all%',round(100*len(o)/len(s),2))
# orders by hour wk2 around deploy
print(C.Counter(r['timestamp'][:10]+' '+r['client_version'] for r in O if r['timestamp']>='2026-06-10'))
# T3 days 13/14 hourly sessions mobile
for day in('2026-06-12','2026-06-13'):
    print(day,sorted(C.Counter(r['timestamp'][11:13] for r in S if r['timestamp'][:10]==day and r['device']=='mobile').items()))
