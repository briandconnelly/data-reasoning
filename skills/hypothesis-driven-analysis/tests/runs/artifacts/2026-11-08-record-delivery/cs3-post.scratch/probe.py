import csv,statistics as s,sys
rows=list(csv.DictReader(open(sys.argv[1]+'/daily.csv')))
def sel(r,a,b): return [float(x['completion_time_seconds']) for x in rows if x['region']==r and a<=x['date']<=b]
def col(r,a,b,c): return [float(x[c]) for x in rows if x['region']==r and a<=x['date']<=b]
for r in('East','West'):
    print(r,'dates',min(x['date'] for x in rows if x['region']==r),max(x['date'] for x in rows if x['region']==r),sum(x['region']==r for x in rows))
# weekly medians pre 02-01..03-14 (6 wks)
import datetime as d
def wk(date): return (d.date.fromisoformat(date)-d.date(2026,2,1)).days//7
for r in('East','West'):
    print(r,'weekly median CT',[round(s.median([float(x['completion_time_seconds']) for x in rows if x['region']==r and wk(x['date'])==k]),1) for k in range(10)])
    print(r,'weekly mean AOV',[round(s.mean([float(x['avg_order_value']) for x in rows if x['region']==r and wk(x['date'])==k]),1) for k in range(10)])
    print(r,'weekly mean vol',[round(s.mean([float(x['volume']) for x in rows if x['region']==r and wk(x['date'])==k]),0) for k in range(10)])
def did(a,b,c,e):
    m=lambda r,x,y:s.median(sel(r,x,y))
    w=m('West',c,e)-m('West',a,b); ea=m('East',c,e)-m('East',a,b)
    return round(w,2),round(ea,2),round(w-ea,2)
print('actual pre/post (West, East, diff) pre 02-01..03-14 post 03-15..03-28',did('2026-02-01','2026-03-14','2026-03-15','2026-03-28'))
print('placebo 02-01..02-14 vs 02-15..02-28 (W,E,diff)',did('2026-02-01','2026-02-14','2026-02-15','2026-02-28'))
print('placebo 02-15..02-28 vs 03-01..03-14',did('2026-02-15','2026-02-28','2026-03-01','2026-03-14'))
print('last 2wk pre vs post',did('2026-03-01','2026-03-14','2026-03-15','2026-03-28'))
