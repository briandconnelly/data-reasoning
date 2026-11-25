import math,random
a,b,n=100,120,1000
d=(b-a)/n;se=math.sqrt(a/n*(1-a/n)/n+b/n*(1-b/n)/n)
print("diff",d,"wald",d-1.96*se,d+1.96*se,"z",d/se)
# Newcombe hybrid score
def w(x):
    p=x/n;z=1.96;c=(p+z*z/2/n)/(1+z*z/n);h=z*math.sqrt(p*(1-p)/n+z*z/4/n/n)/(1+z*z/n);return p,c-h,c+h
pa,la,ua=w(a);pb,lb,ub=w(b)
print("newcombe",d-math.sqrt((pb-lb)**2+(ua-pa)**2),d+math.sqrt((ub-pb)**2+(pa-la)**2))
random.seed(1);r=[]
for _ in range(5000):
    x=sum(random.random()<a/n for _ in range(n));y=sum(random.random()<b/n for _ in range(n));r.append((y-x)/n)
r.sort();print("boot",r[125],r[4874],sum(v>=.01 for v in r)/5000)
