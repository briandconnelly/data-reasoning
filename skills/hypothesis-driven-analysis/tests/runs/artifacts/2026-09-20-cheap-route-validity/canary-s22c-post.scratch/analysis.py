import csv,collections
o=list(csv.DictReader(open('orders.csv')));a=list(csv.DictReader(open('accounts.csv')))
print(len(o),len(a))
ids=collections.Counter(r['account_id'] for r in a)
print('accounts rows',len(a),'unique ids',len(ids),'dups',{k:v for k,v in ids.items() if v>1})
for k,v in ids.items():
    if v>1: print([r for r in a if r['account_id']==k])
print('order_id unique',len({r['order_id'] for r in o})==len(o))
print('date range',min(r['order_date'] for r in o),max(r['order_date'] for r in o))
print('orphans',{r['account_id'] for r in o}-set(ids))
print('bad amounts',[r for r in o if not r['amount_usd'] or float(r['amount_usd'])<=0][:5])
# monthly coverage
m=collections.Counter(r['order_date'][:7] for r in o);print(sorted(m.items()))
print(collections.Counter(r['segment'] for r in a))

print('--- Q2 Enterprise')
seg=collections.defaultdict(set)
for r in a: seg[r['account_id']].add(r['segment'])
print('accounts with >1 segment:',{k:v for k,v in seg.items() if len(v)>1})
q2=[r for r in o if '2026-04-01'<=r['order_date']<='2026-06-30']
print('Q2 orders',len(q2), 'sum',round(sum(float(r['amount_usd']) for r in q2),2))
# correct: as-of join (latest version with valid_from<=order_date), one row per order
def asof(r):
    c=[x for x in a if x['account_id']==r['account_id'] and x['valid_from']<=r['order_date']]
    return max(c,key=lambda x:x['valid_from'])['segment'] if c else None
tot=collections.Counter();n=collections.Counter();unm=0
for r in q2:
    s=asof(r)
    if s is None: unm+=1;continue
    tot[s]+=float(r['amount_usd']);n[s]+=1
print('as-of',{k:(round(v,2),n[k]) for k,v in tot.items()},'unmatched',unm)
# by unique account (segment constant)
sm={k:next(iter(v)) for k,v in seg.items()}
t2=collections.Counter();n2=collections.Counter()
for r in q2: t2[sm[r['account_id']]]+=float(r['amount_usd']);n2[sm[r['account_id']]]+=1
print('per-account',{k:(round(v,2),n2[k]) for k,v in t2.items()})
# naive fanout join
naive=0;nn=0
for r in q2:
    for x in a:
        if x['account_id']==r['account_id'] and x['segment']=='Enterprise': naive+=float(r['amount_usd']);nn+=1
print('naive join Enterprise',round(naive,2),nn)
# month split and date-format check
print(collections.Counter(len(r['order_date']) for r in o))
