import csv,collections as C
d='/var/folders/4_/s6fbcjyn4b13xdxkd3lv0kw00000gn/T/arm-s1-post-2-0pd3usjn/data/s1-conversion/'
s=list(csv.DictReader(open(d+'sessions.csv')))
c=C.Counter((r['timestamp'][5:10],r['device'],r['landing_page']) for r in s)
for dd in('06-12','06-13'):
  for dv in('desktop','mobile'):print(dd,dv,{lp:c[(dd,dv,lp)] for lp in('/home','/product','/lp/summer-sale')})
# SS by device wk2
k=C.Counter((r['device'],r['checkout_reached']) for r in s if r['landing_page']=='/lp/summer-sale' and r['timestamp']<'2026-06-13');print(k)
# 06-08..12 only (complete days): overall vs wk1 days 1-5
for a,b,l in(('06-01','06-05','wk1 d1-5'),('06-08','06-12','wk2 d1-5')):
  n=[r for r in s if a<=r['timestamp'][5:10]<=b];print(l,len(n),sum(r['checkout_reached']=='yes' for r in n)/len(n))
