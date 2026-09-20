exec(open('analysis.py').read().split("print('neg ttc'")[0])
a=sorted(r['ttc'] for r in sel('assist'));m=sorted(r['ttc'] for r in sel('manual'))
print(len(a),len(m))
lo=sorted(a+[-1]*10);hi=sorted(a+[1e9]*10)
print('assist median if 10 absent all fastest / all slowest:',med(lo),med(hi),'closed-only',med(a))
lo=sorted(m+[-1]);hi=sorted(m+[1e9]);print('manual bound',med(lo),med(hi))
print('worst-case headline diff range',med(hi if False else sorted(a+[1e9]*10))-med(sorted(m+[-1])),med(sorted(a+[-1]*10))-med(sorted(m+[1e9])))
# sev-stratum: if 5 absent sev1 assist were fast as manual sev1 median
print('sev1 assist absent share',5/14)
# marginal mean min if absent imputed with same-wf same-sev mean: 
def imp(w):
    v=[r['min'] for r in sel(w)]
    for r in sel(w,closed=False):
        if r['ttc'] is None: v.append(st.mean(x['min'] for x in sel(w,r['severity'])))
    return st.mean(v)
print('imputed mean minutes m %.1f a %.1f'%(imp('manual'),imp('assist')))
# stratified bootstrap CI for marginal median with design-fixed mix
def g():
    d={w:[] for w in ['manual','assist']}
    for w in d:
        for s in ['sev1','sev2','sev3']:
            d[w]+=rs(sel(w,s))
    return med([r['ttc'] for r in d['assist']])-med([r['ttc'] for r in d['manual']])
print('marginal median diff CI, mix held at design counts',boot(g,3000))
