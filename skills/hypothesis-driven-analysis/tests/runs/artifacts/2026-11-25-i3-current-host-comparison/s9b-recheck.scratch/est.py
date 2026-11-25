from math import sqrt
def d(sa,na,sb,nb):
    pa,pb=sa/na,sb/nb; se=sqrt(pa*(1-pa)/na+pb*(1-pb)/nb); x=pb-pa
    return round(x*100,2),round((x-1.96*se)*100,2),round((x+1.96*se)*100,2)
print("complete-case",d(100,1000,96,800))
print("lower (B unk=fail)",d(100,1000,96,1000))
print("upper (B unk=success)",d(100,1000,296,1000))
