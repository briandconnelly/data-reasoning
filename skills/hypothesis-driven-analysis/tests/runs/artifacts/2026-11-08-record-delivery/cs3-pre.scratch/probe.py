import csv,sys,statistics as s
rows=list(csv.DictReader(open(sys.argv[1])))
for r in rows:
    r['t']=float(r['completion_time_seconds']);r['a']=float(r['avg_order_value']);r['v']=float(r['volume'])
def sel(reg,lo,hi): return [r for r in rows if r['region']==reg and lo<=r['date']<=hi]
def slope(y):
    n=len(y);x=range(n);mx=(n-1)/2;my=sum(y)/n
    return sum((a-mx)*(b-my) for a,b in zip(x,y))/sum((a-mx)**2 for a in x)
pre=('2026-02-01','2026-03-14');post=('2026-03-15','2026-03-28');late=('2026-03-29','2026-04-11')
for reg in ('East','West'):
    print(reg)
    for wk in range(6):
        d=sel(reg,'2026-02-01','2026-03-14')[wk*7:wk*7+7]
        print(' wk',wk+1,'median t',round(s.median(r['t'] for r in d),1))
    p=sel(reg,*pre)
    print(' pre slope sec/day',round(slope([r['t'] for r in p]),3))
    for nm,w in (('pre',pre),('post2w',post),('late',late)):
        d=sel(reg,*w)
        print(' ',nm,'median t',round(s.median(r['t'] for r in d),1),'mean AOV',round(s.mean(r['a'] for r in d),2),'mean vol',round(s.mean(r['v'] for r in d),1))
    # last 2 pre weeks
    d=sel(reg,'2026-03-01','2026-03-14');print('  last2preweeks median t',round(s.median(r['t'] for r in d),1))
