import csv,statistics as st,sys
rows=list(csv.DictReader(open(sys.argv[1]+'/daily.csv')))
def sel(r,a,b): return [float(x['completion_time_seconds']) for x in rows if x['region']==r and a<=x['date']<=b]
def sel2(r,a,b,k): return [float(x[k]) for x in rows if x['region']==r and a<=x['date']<=b]
def slope(y):
    n=len(y);xm=(n-1)/2;ym=sum(y)/n
    return sum((i-xm)*(v-ym) for i,v in enumerate(y))/sum((i-xm)**2 for i in range(n))
for r in('West','East'):
    pre=sel(r,'2026-02-01','2026-03-14');post=sel(r,'2026-03-15','2026-03-28');ext=sel(r,'2026-03-29','2026-04-11')
    print(r,'n',len(pre),len(post),len(ext))
    print(' median pre',st.median(pre),'post2w',st.median(post),'ext2w+',st.median(ext))
    print(' slope/day pre',round(slope(pre),3),' first wk',round(st.mean(pre[:7]),2),'last pre wk',round(st.mean(pre[-7:]),2))
    print(' slope/day post+ext',round(slope(post+ext),3))
    print(' weekly means',[round(st.mean(sel(r,*w)),1) for w in [('2026-02-01','2026-02-07'),('2026-02-08','2026-02-14'),('2026-02-15','2026-02-21'),('2026-02-22','2026-02-28'),('2026-03-01','2026-03-07'),('2026-03-08','2026-03-14'),('2026-03-15','2026-03-21'),('2026-03-22','2026-03-28'),('2026-03-29','2026-04-04'),('2026-04-05','2026-04-11')]])
    for k in('volume','avg_order_value'):
        print(' ',k,'pre',round(st.mean(sel2(r,'2026-02-01','2026-03-14',k)),2),'post',round(st.mean(sel2(r,'2026-03-15','2026-03-28',k)),2))
