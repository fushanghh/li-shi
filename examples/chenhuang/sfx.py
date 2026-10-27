import numpy as np, wave
from render import SH,starts,TOTAL,TRD
SR=44100;N=int((TOTAL+1)*SR)
rng=np.random.default_rng(1)
L=np.zeros(N);R=np.zeros(N)
def add(sig,t,pan=0.0,g=1.0):
    i=int(t*SR)
    if i<0:sig=sig[-i:];i=0
    n=min(len(sig),N-i)
    if n<=0:return
    L[i:i+n]+=sig[:n]*g*(1-pan*.7);R[i:i+n]+=sig[:n]*g*(1+pan*.7)
def tt(d):return np.arange(int(d*SR))/SR
def env(n,a,d):t=np.arange(n)/SR;return np.minimum(1,t/max(a,1e-4))*np.exp(-t/d)
def lp(x,a):  # one-pole lowpass, a in (0,1) smaller=darker
    from scipy.signal import lfilter
    return lfilter([a],[1,a-1],x)
def hp(x,a):return x-lp(x,a)
def fadeio(x,fi=.3,fo=.5):
    n=len(x);e=np.ones(n);a=int(fi*SR);b=int(fo*SR)
    if a>0:e[:a]=np.linspace(0,1,a)
    if b>0:e[-b:]=np.minimum(e[-b:],np.linspace(1,0,b))
    return x*e
def noise(d):return rng.standard_normal(int(d*SR))
# --- generators
def rainbed(d,g=1):return fadeio(hp(lp(noise(d),.5),.05)*.25*g+lp(noise(d),.02)*.3*g,.4,.4)
def windbed(d,g=1):
    x=lp(noise(d),.004);t=tt(d);return fadeio(x*(1+.5*np.sin(t*.7))*3.0*g,.5,.6)
def firebed(d,g=1):
    x=lp(noise(d),.03)*.6
    n=len(x)
    for k in range(int(d*25)):
        i=rng.integers(0,max(1,n-800));m=rng.integers(100,600);x[i:i+m]+=rng.standard_normal(m)*np.exp(-np.arange(m)/(m/5))*rng.uniform(.3,1.2)
    return fadeio(x*.35*g,.3,.4)
def thunder(big=1.0):
    d=4;x=lp(noise(d),.01)*env(int(d*SR),.02 if big>1 else .3,1.2)*6
    cr=hp(noise(.5),.3)*env(int(.5*SR),.001,.08)*1.2*big
    out=x.copy();out[:len(cr)]+=cr;return out*.5*big
def drum(f=60,d=.9,g=1):
    t=tt(d);body=np.sin(2*np.pi*(f+f*1.5*np.exp(-t*30))*t)*env(len(t),.002,.25)
    sk=lp(noise(d),.2)*env(len(t),.001,.03)*.6
    return (body+sk)*g
def boom():
    t=tt(2.5);return (np.sin(2*np.pi*(38+80*np.exp(-t*8))*t)*env(len(t),.003,.7)*1.4+lp(noise(2.5),.03)*env(len(t),.002,.4)*2)
def stamp():
    t=tt(.7);body=np.sin(2*np.pi*(65+120*np.exp(-t*25))*t)*env(len(t),.001,.12)
    return (body*1.1+lp(noise(.7),.25)*env(len(t),.001,.035)*1.2)
def gong(f=98,d=4.5):
    t=tt(d);s=sum(a*np.sin(2*np.pi*f*m*t*(1+.002*np.sin(t*5))) for m,a in [(1,1),(2.02,.5),(2.76,.35),(3.9,.2),(5.4,.12)])
    return s*env(len(t),.01,1.4)*.35
def ding(f=1200,d=1.0,g=.12):t=tt(d);return (np.sin(2*np.pi*f*t)+.4*np.sin(2*np.pi*f*2.7*t))*env(len(t),.002,.25)*g
def tick():return hp(noise(.06),.5)*env(int(.06*SR),.0005,.01)*.4
def whoosh(d=.7,g=1,rise=False):
    x=noise(d);t=tt(d);e=np.sin(np.pi*t/d)**2
    if rise:e=(t/d)**2*np.exp(-(t/d-1)**2*0)
    return lp(x,.06)*e*1.2*g
def swish(d=.5):x=noise(d);t=tt(d);return hp(lp(x,.3),.05)*np.sin(np.pi*t/d)**3*.5
def shimmer(d=.6):t=tt(d);return sum(np.sin(2*np.pi*f*t) for f in (2100,2650,3170,3900))*env(len(t),.01,.2)*.04
def clash():
    t=tt(1.2);s=sum(np.sin(2*np.pi*f*t)*a for f,a in [(1870,1),(2930,.7),(4120,.5),(5570,.3)])*env(len(t),.0005,.18)
    return (s*.35+hp(noise(1.2),.4)*env(len(t),.0005,.02)*.8)
def unsheath():
    t=tt(.6);s=hp(noise(.6),.3)*np.sin(np.pi*t/.6)*.3;ring=sum(np.sin(2*np.pi*f*t) for f in (3200,4700))*env(len(t),.4,.3)*.08
    return s+ring
def whip():t=tt(.3);return hp(noise(.3),.5)*env(len(t),.0005,.02)*1.4
def slash():return np.pad(swish(.25)*2,(0,int(.05*SR)))+lp(noise(.3),.1)*env(int(.3*SR),.001,.05)*.8
def hooves(d,rate=7.0,g=1):
    x=np.zeros(int(d*SR));t=0
    while t<d-.1:
        for off in (0,.06,.13,.17):
            c=lp(noise(.08),.15)*env(int(.08*SR),.001,.015);i=int((t+off)*SR);n=min(len(c),len(x)-i)
            if n>0:x[i:i+n]+=c[:n]*rng.uniform(.6,1)
        t+=1/rate*4
    return x*.9*g
def steps(d,interval=.55,g=1):
    x=np.zeros(int(d*SR));t=.1
    while t<d:
        c=lp(noise(.25),.05)*env(int(.25*SR),.005,.06)*2;i=int(t*SR);n=min(len(c),len(x)-i)
        if n>0:x[i:i+n]+=c[:n]
        t+=interval
    return x*g
def crowd(d,g=1,scream=False):
    n=int(d*SR);x=np.zeros(n)
    for k in range(int(d*30)):
        m=int(SR*rng.uniform(.3,.9));m=min(m,n-1);st=rng.integers(0,max(1,n-m));t=np.arange(m)/SR
        f=rng.uniform(140,260) if not scream else rng.uniform(380,900)
        v=np.sin(2*np.pi*f*t+2*np.sin(2*np.pi*rng.uniform(4,8)*t))+.5*np.sin(2*np.pi*2*f*t)
        v*=np.sin(np.pi*t/t[-1])
        x[st:st+m]+=v*.04
    x=lp(x,.25)+lp(noise(d),.05)*.5
    return fadeio(x*g,.5,.6)
def creak(d):
    t=tt(d);return fadeio((np.sin(2*np.pi*(180+40*np.sin(t*5))*t)*(np.sin(t*9)>.6))*.05+lp(noise(d),.05)*.2,.3,.3)
def crow():
    t=tt(.4);return np.sign(np.sin(2*np.pi*(620-300*t)*t))*env(len(t),.01,.12)*.08*(np.sin(2*np.pi*30*t)>0)
def fox():t=tt(.9);return np.sin(2*np.pi*(900+300*np.sin(t*6))*t)*np.sin(np.pi*t/.9)*.06
def grind(d):t=tt(d);return fadeio(lp(noise(d),.08)*(.6+.4*np.sin(2*np.pi*t*.48))*.6,.3,.3)
def arrows(d):
    x=np.zeros(int(d*SR))
    for k in range(int(d*14)):
        a=hp(noise(.25),.2)*np.sin(np.pi*tt(.25)/.25)**2*.25;i=rng.integers(0,len(x)-len(a));x[i:i+len(a)]+=a
    return x
def heartbeat(d,bpm=60):
    x=np.zeros(int(d*SR));t=0
    while t<d:
        for o,g in ((0,1),(.18,.7)):
            c=drum(45,.4,g*.6);i=int((t+o)*SR);n=min(len(c),len(x)-i)
            if n>0:x[i:i+n]+=c[:n]
        t+=60/bpm
    return x
def bell():t=tt(3);return sum(a*np.sin(2*np.pi*f*t) for f,a in [(520,1),(1170,.5),(1690,.3)])*env(len(t),.003,.9)*.15
def paper():return hp(lp(noise(.4),.4),.08)*np.sin(np.pi*tt(.4)/.4)*.25
# ---- schedule
S=lambda name:starts[[sh['f'].__name__ for sh in SH].index(name)] if isinstance(name,str) else starts[name]
def at(i,t,sig,pan=0,g=1):add(sig,starts[i]+t,pan,g)
for i,sh in enumerate(SH):
    tr=sh.get('tr','cut');b=starts[i]
    if i==0:continue
    if tr in('push','flag'):add(whoosh(.8),b-.45,0,1.2)
    elif tr=='dive':add(whoosh(.9,1.3,True),b-.7,0,1)
    elif tr=='ink':add(swish(.7),b-.35,0,1)
    elif tr=='fire':add(whoosh(.9),b-.45,0,1);add(firebed(1.2),b-.5,0,1.4)
    elif tr=='smoke':add(whoosh(1.2,.8),b-.6,0,1)
    elif tr=='flash':add(shimmer(.7),b-.15);add(boom(),b,0,.6)
T=[sh['T'] for sh in SH]
# 0 hook1
at(0,0,windbed(4.6),0,.8);at(0,0,crowd(4.6,.6),-.5);at(0,0,firebed(4.6),.6,.8);at(0,2.0,boom(),0,1.1);at(0,2.0,drum(55,1.2,1.2))
at(1,0,paper());at(1,1.0,stamp(),-.3,1.2);at(1,2.6,stamp(),.3,1.2)
at(2,1.0,stamp(),0,1.3);at(2,1.0,gong(82,4),0,1)
at(3,0,heartbeat(3,64),0,.7)
for k in range(12):at(3,.3+k*.13,tick(),0,1)
at(3,3.0,thunder(.6),0,.8);at(3,3.0,rainbed(3.6,.6));at(3,3.6,stamp(),0,.6)
at(4,0,rainbed(3.6,1.2));at(4,.75,thunder(1.6),.3,1.2);at(4,0,windbed(3.6),0,.6)
at(5,0,rainbed(3.1,1.1));at(5,0,steps(3.1,.5,1.0))
at(6,0,rainbed(3.6,.5));at(6,0,firebed(1.5),-.5,.6);at(6,1.5,paper(),0,1.2);at(6,2.1,stamp(),0,1.5);at(6,2.1,drum(50,1.0,1))
at(7,.3,slash(),0,.7);at(7,.4,paper());at(7,1.6,firebed(1.6),.4,.8);at(7,1.9,fox(),.4,1.2);at(7,2.5,fox(),.5,.8)
at(8,.3,whip(),.2,1);at(8,.7,whip(),.2,1);at(8,1.0,unsheath(),0,1);at(8,1.45,thunder(2.0),0,1.2);at(8,1.45,clash(),0,1);at(8,1.6,stamp(),0,1);at(8,0,rainbed(3.3,.5))
at(9,0,crowd(4.7,1.3));at(9,0,firebed(4.7),0,.5)
for k,tm in enumerate([.4,.9,1.4,1.7]):at(9,tm,drum(55,.9,1))
at(9,2.0,boom(),0,1.2);at(9,2.3,stamp(),0,.8)
at(10,0,crowd(3.7,1.5))
for k in range(14):at(10,k*.26,drum(60 if k%2 else 50,.6,.9))
at(10,1.0,stamp(),0,1.1)
at(11,0,heartbeat(7,90),0,.5);at(11,2.2,stamp(),0,1.2);at(11,2.2,drum(55,1,1))
for j in range(40):at(11,4.0+j*.05,ding(900+j*25,.6,.05),(j%5-2)/3)
at(12,0,creak(2.0),0,1);at(12,0,hooves(2.0,4.5,.7));at(12,0,windbed(4.7),0,.5)
at(12,2.0,unsheath());at(12,2.9,slash(),0,1.2);at(12,2.9,drum(45,1.2,1.2));at(12,2.95,stamp(),0,.9)
for k in range(3):at(12,3.3+k*.45,crow(),(k-1)/2)
for k in range(6):at(13,.3+k*.15,whoosh(1.5,.5),(k-3)/4)
at(13,3.0,firebed(2),0,.8);at(13,3.0,stamp(),0,1.2);at(13,3.0,gong(73,4),0,1)
at(14,0,windbed(1.7),0,.8);at(14,0,gong(110,3),0,.6)
at(15,0,clash(),0,1.2);at(15,0,firebed(2.5),0,.8);at(15,0,boom(),0,.6)
at(16,0,windbed(4.5),0,.6);at(16,0,creak(2.1),0,.8);at(16,0,steps(2.1,.55,.5));at(16,2.1,crowd(2.3,.5))
at(17,0,windbed(5),0,.6)
for k in range(14):at(17,.4+k*.17,ding(1500+((k*37)%7)*120,1.2,.04),(k%3-1)/2)
at(18,0,windbed(4.6),0,1.0);at(18,0,grind(2.6));at(18,2.6,whip(),.3,1.1);at(18,3.2,whip(),.3,1.1)
for k in range(30):at(19,k*.3,drum(58 if k%2 else 48,.6,.7))
for k,tm in enumerate([.3,4.2,7.7,8.3,8.9]):at(19,tm,ding(800,1,.1))
at(20,0,firebed(4.7),0,1);at(20,0,crowd(2.4,1.3));at(20,.2,arrows(1.6),0,1)
for tm in (.2,.7,1.2):at(20,tm,boom(),0,.8)
at(20,2.3,hooves(2.3,8,1.1));at(20,2.3,rainbed(2.3,.6))
at(21,0,gong(87,4),0,.9);at(21,1.6,stamp(),0,1.2);at(21,1.6,drum(55,1,1));at(21,.6,bell(),0,.8)
at(22,0,firebed(4.7),0,1.4);at(22,0,crowd(4.7,1.0,True),-.4)
for k in range(7):at(22,.3+k*.55,clash(),.5,.5)
at(22,1.6,stamp(),0,1.2)
for k in range(7):at(23,.2+k*.6,drum(42,.8,1.1))
at(23,0,windbed(4.3),0,.8);at(23,1.5,stamp(),0,1.0)
at(24,0,rainbed(4.7,.9));at(24,0,windbed(4.7),0,.7);at(24,.8,thunder(.6),0,.8);at(24,2.2,heartbeat(2.4,50),0,.8)
at(25,.3,whoosh(1.4,.7));at(25,1.6,stamp(),0,1.2);at(25,1.6,gong(65,4),0,1)
at(26,0,paper())
for k in range(5):at(26,k*.36,tick(),0,1.5)
for r in range(5):
    i=27+r;at(i,.5,paper(),0,.8);at(i,1.2,ding(1100,1,.12));at(i,1.2,drum(70,.5,.5))
    mr=['g','h','x','x','x'][r];at(i,2.4,stamp() if mr=='x' else ding(900,1,.12),0,1)
at(32,0,windbed(3.9),0,.6);at(32,.3,bell(),0,1)
at(33,0,crowd(5,.5));at(33,.6,crowd(.8,.8));at(33,1.2,clash(),.4,.7);at(33,3.4,stamp(),0,1.1)
for k in range(4):at(34,2.0+k*.55,drum(60,.6,.9));at(34,2.0+k*.55,ding(700+k*120,1,.08))
at(35,0,paper());at(35,0,whoosh(1.2,.6));at(35,2.8,stamp(),0,1.2);at(35,2.8,gong(73,5),0,1.1)
m=np.max(np.abs(np.stack([L,R])));L/=m/0.85;R/=m/0.85
# gentle compression
Lc=np.tanh(L*1.6)/np.tanh(1.6);Rc=np.tanh(R*1.6)/np.tanh(1.6)
fade=np.ones(N);fade[-int(1.8*SR):]=np.linspace(1,0,int(1.8*SR));Lc*=fade;Rc*=fade
d=(np.stack([Lc,Rc],1)*32767*.95).astype(np.int16)
w=wave.open('sfx.wav','wb');w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(d.tobytes());w.close();print('ok',TOTAL)
