import csv,statistics as s,sys
r=list(csv.DictReader(open('daily.csv')))
def w(reg,a,b,k='completion_time_seconds'):
    v=[float(x[k]) for x in r if x['region']==reg and a<=x['date']<=b]
    return round(s.median(v),2),len(v)
P=[('pre6wk','2026-02-01','2026-03-14'),('pre last2wk','2026-03-01','2026-03-14'),('pre first2wk','2026-02-01','2026-02-14'),('post2wk','2026-03-15','2026-03-28'),('post all','2026-03-15','2026-04-11')]
for n,a,b in P:
  for reg in('East','West'): print(n,reg,w(reg,a,b),'AOV',w(reg,a,b,'avg_order_value')[0],'vol',w(reg,a,b,'volume')[0])
for reg in('East','West'):
  print(reg,[w(reg,f'2026-02-{d:02d}',f'2026-02-{d+6:02d}')[0] for d in (1,8,15,22)])
