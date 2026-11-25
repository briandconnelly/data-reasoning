import importlib.util, sys
from datetime import date, timedelta
from collections import defaultdict
spec=importlib.util.spec_from_file_location('am','../data/analyst_model.py'); am=importlib.util.module_from_spec(spec); spec.loader.exec_module(am)
rows=am.load('../data/daily_tickets.csv')
am.main('../data/daily_tickets.csv')   # reproduce claim
def month_add(y,m,k):
    t=y*12+m-1+k; return t//12, t%12+1
tot=defaultdict(int)
for d,y in rows: tot[(d.year,d.month)]+=y
res=[]
print('origin  h  forecast  actual  err%  (signed)')
for oy,om in sorted(tot):
    # origin = end of month (oy,om); need 3 future months and >=6 months history
    if month_add(oy,om,3) not in tot: continue
    if (oy*12+om)-(2024*12+10) < 5: continue
    end=date(oy,om,1)
    train=[(d,y) for d,y in rows if (d.year,d.month)<=(oy,om)]
    errs=[]
    for h in (1,2,3):
        ty,tm=month_add(oy,om,h)
        days=[d for d,_ in rows if (d.year,d.month)==(ty,tm)]
        f=sum(am.predict(train,d) for d in days); a=tot[(ty,tm)]
        e=(f-a)/a; errs.append(e)
        print(f'{oy}-{om:02d}  {h}  {f:8.0f} {a:7d} {100*abs(e):5.1f} {100*e:+6.1f}')
    res.append(((oy,om),sum(abs(e) for e in errs)/3))
print()
for o,m in res: print(o, f'avg abs err of 3 months: {100*m:.1f}%')
print('mean over origins', f'{100*sum(m for _,m in res)/len(res):.1f}%', 'n=',len(res))
