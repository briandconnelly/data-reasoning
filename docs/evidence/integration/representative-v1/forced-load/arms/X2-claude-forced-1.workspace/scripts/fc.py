import importlib.util
from datetime import date, timedelta
spec=importlib.util.spec_from_file_location('am','../data/analyst_model.py'); am=importlib.util.module_from_spec(spec); spec.loader.exec_module(am)
rows=am.load('../data/daily_tickets.csv'); tot={}
for d,y in rows: tot[(d.year,d.month)]=tot.get((d.year,d.month),0)+y
g=sum(tot[(2026,m)] for m in (7,8,9))/sum(tot[(2025,m)] for m in (7,8,9))
print('YoY growth Jul-Sep', round(g,3))
for m,n in ((10,31),(11,30),(12,31)):
    f=sum(am.predict(rows,date(2026,m,1)+timedelta(i)) for i in range(n))
    print(2026,m,'analyst',round(f),'| last yr',tot[(2025,m)],'| illustrative seasonal x growth',round(tot[(2025,m)]*g))
