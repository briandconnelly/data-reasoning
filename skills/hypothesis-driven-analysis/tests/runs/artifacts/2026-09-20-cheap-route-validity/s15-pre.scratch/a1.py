from load import *
import statistics as st,random
random.seed(1)
def med(x):return st.median(x)
def q(x,p):
    x=sorted(x);return x[int(p*(len(x)-1))]
def boot(f,A,B,n=4000):
    d=[]
    for _ in range(n):
        a=[random.choice(A) for _ in A];b=[random.choice(B) for _ in B];d.append(f(a)-f(b))
    d.sort();return d[int(.025*n)],d[int(.975*n)]
cl=[r for r in inc if r['has']]
def g(w,s=None,k='ttc'):return [r[k] for r in cl if r['workflow']==w and (s is None or r['severity']==s)]
for k in('ttc','rm','ho'):
  print('==',k)
  for s in (None,'sev1','sev2','sev3'):
    A,M=g('assist',s,k),g('manual',s,k)
    print(s,len(M),len(A),'med man %.2f assist %.2f'%(med(M),med(A)),'mean %.2f %.2f'%(st.mean(M),st.mean(A)),'dmed CI',[round(x,2) for x in boot(med,A,M)],'dmean CI',[round(x,2) for x in boot(st.mean,A,M)])
print('reopen',[ (w,sum(r['ro'] for r in cl if r['workflow']==w),sum(1 for r in cl if r['workflow']==w)) for w in('manual','assist')])
for s in('sev1','sev2','sev3'):
  print(s,'reopen',[(w,sum(r['ro'] for r in cl if r['workflow']==w and r['severity']==s),sum(1 for r in cl if r['workflow']==w and r['severity']==s)) for w in('manual','assist')])
# ttc quantiles
for w in('manual','assist'):
    x=g(w);print(w,[round(q(x,p),1) for p in(.1,.25,.5,.75,.9,.99)],'max',round(max(x),1))
