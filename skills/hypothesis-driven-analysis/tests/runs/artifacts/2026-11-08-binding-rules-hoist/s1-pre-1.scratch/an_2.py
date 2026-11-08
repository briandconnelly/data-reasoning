import csv,collections as C,random
S=list(csv.DictReader(open('data/s1-conversion/sessions.csv')))
y=lambda s:s['checkout_reached']=='yes'
def r(rows): return sum(map(y,rows))/len(rows),len(rows)
W1=[s for s in S if s['timestamp']<'2026-06-08'];W2=[s for s in S if s['timestamp']>='2026-06-08']
ns=lambda L:[s for s in L if s['landing_page']!='/lp/summer-sale']
print('all',r(W1),r(W2)); print('ex summer-sale',r(ns(W1)),r(ns(W2)))
print('summer-sale first/last ts',min(s['timestamp'] for s in S if s['landing_page']=='/lp/summer-sale'),max(s['timestamp'] for s in S if s['landing_page']=='/lp/summer-sale'))
print('summer-sale by day',sorted(C.Counter(s['timestamp'][:10] for s in S if s['landing_page']=='/lp/summer-sale').items()))
D='2026-06-10T14:00:07Z'
pre=[s for s in ns(W2) if s['timestamp']<D];post=[s for s in ns(W2) if s['timestamp']>=D]
print('non-SS wk2 pre-deploy',r(pre),'post-deploy',r(post))
for dev in('desktop','mobile'):
    print(dev,'pre',r([s for s in pre if s['device']==dev]),'post',r([s for s in post if s['device']==dev]),'wk1',r([s for s in ns(W1) if s['device']==dev]))
# bootstrap by session, 95%, contrast ex-SS wk2 - wk1 and post-pre
random.seed(2)
def bs(a,b,n=3000):
    ra=[int(y(s)) for s in a];rb=[int(y(s)) for s in b];o=[]
    for _ in range(n):
        o.append(sum(random.choices(rb,k=len(rb)))/len(rb)-sum(random.choices(ra,k=len(ra)))/len(ra))
    o.sort();return round(o[int(.025*n)],4),round(o[int(.975*n)],4)
print('CI wk2-wk1 all',bs(W1,W2)); print('CI exSS wk2-wk1',bs(ns(W1),ns(W2))); print('CI exSS post-pre deploy',bs(pre,post))
print('CI pre-deploy exSS vs wk1 exSS',bs(ns(W1),pre))
SS=[s for s in W2 if s['landing_page']=='/lp/summer-sale']
print('SS rate',r(SS),'CI vs rest wk2',bs(ns(W2),SS))
# summer sale before/after deploy
print('SS pre/post',r([s for s in SS if s['timestamp']<D]),r([s for s in SS if s['timestamp']>=D]))
# by-day coverage for 06-13/14 by landing
print(sorted(C.Counter((s['timestamp'][:10],s['landing_page']) for s in S if s['timestamp'][:10]>='2026-06-12').items()))
# full coverage days only
fc1=[s for s in W1 if s['timestamp'][:10]<='2026-06-05'];fc2=[s for s in W2 if s['timestamp'][:10]<='2026-06-12']
print('full cov chk',r(fc1),r(fc2),bs(fc1,fc2))
print('---T1')
PRE=[s for s in W2 if s['timestamp']<D]; POST=[s for s in W2 if s['timestamp']>=D]
print('all pre-deploy wk2',r(PRE),'post',r(POST),'CI pre-wk1',bs(W1,PRE),'CI post-wk1',bs(W1,POST),'CI post-pre',bs(PRE,POST))
