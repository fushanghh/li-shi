import json,cairocffi as cairo
import render
import shotsA,shotsB,shotsC,base
EV=[];cur={'T':0}
def wrap(mod,name,kind):
    f=getattr(mod,name)
    def g(c,t,*a,**k):
        try:
            if kind=='counter':
                for tt,v in a[1]:EV.append((round(cur['T']-t+tt,3),'counter'))
            else:EV.append((round(cur['T']-t+a[0],3),kind))
        except Exception:pass
        return f(c,t,*a,**k)
    setattr(mod,name,g)
for m in (shotsA,shotsB,shotsC):
    for n,k in [('bigword','big'),('stamp','stamp'),('badge','badge'),('counter','counter')]:wrap(m,n,k)
sf=cairo.ImageSurface(cairo.FORMAT_ARGB32,192,108);c=cairo.Context(sf);c.scale(.1,.1)
for t0,t1,fn,pl in base.SH:
    T=t0
    while T<t1:
        cur['T']=T
        try:fn(c,T-t0,T)
        except Exception as e:pass
        T+=0.2
d={}
for t,k in sorted(set(EV)):
    if 0<=t<render.TOTAL:
        key=round(t,2)
        if key not in d or k=='stamp':d[key]=k
json.dump(sorted(d.items()),open('events.json','w'));print(len(d))
