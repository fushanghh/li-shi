# 纯音效轨（无配乐）：numpy 合成，按镜头 fx 表与切点对齐
import numpy as np, re, inspect, wave, sys
import render, common
from base import SH, B
SR=44100
TOTAL=render.TOTAL
N=int((TOTAL+1.5)*SR)
L=np.zeros(N);R=np.zeros(N)
rng=np.random.default_rng(7)
def tt(d):return np.arange(int(d*SR))/SR
def env(n,a=.01,r=.1):
    e=np.ones(n);na=max(1,int(a*SR));nr=max(1,int(r*SR))
    na=min(na,n);nr=min(nr,n)
    e[:na]=np.linspace(0,1,na);e[-nr:]*=np.linspace(1,0,nr);return e
def lp(x,fc):
    # one-pole lowpass applied twice
    a=np.exp(-2*np.pi*fc/SR);y=np.empty_like(x);s=0.0
    from scipy.signal import lfilter
    y=lfilter([1-a],[1,-a],x);y=lfilter([1-a],[1,-a],y);return y
def hp(x,fc):return x-lp(x,fc)
def bp(x,lo,hi):return lp(hp(x,lo),hi)
def noise(d):return rng.standard_normal(int(d*SR))
def put(x,t0,g=1.0,pan=0.0):
    i=int(t0*SR)
    if i>=N or i+len(x)<=0:return
    if i<0:x=x[-i:];i=0
    x=x[:N-i]
    L[i:i+len(x)]+=x*g*np.sqrt((1-pan)/2)*1.41;R[i:i+len(x)]+=x*g*np.sqrt((1+pan)/2)*1.41
# ---------- one-shots ----------
def boom(d=1.6,big=1.0):
    t=tt(d);n=noise(d)
    x=lp(n,600)*np.exp(-t*6)*1.4+np.sin(2*np.pi*(55-20*t)*t)*np.exp(-t*4)*1.2*big
    x+=lp(noise(d),180)*np.exp(-t*2.2)*.8
    return x*env(len(t),.002,.3)
def expl(d=2.4):
    t=tt(d);x=lp(noise(d),900)*np.exp(-t*3.5)*1.2+lp(noise(d),200)*np.exp(-t*1.2)*1.0+np.sin(2*np.pi*(48-18*t)*t)*np.exp(-t*2.5)
    # debris
    for k in range(14):
        i=int(rng.uniform(.15,1.6)*SR);m=int(.02*SR)
        if i+m<len(x):x[i:i+m]+=hp(noise(.02),2000)*np.exp(-np.arange(m)/SR*150)*.25
    return x*env(len(t),.003,.5)
def rifle():
    d=.6;t=tt(d);x=hp(noise(d),800)*np.exp(-t*40)*1.5+lp(noise(d),500)*np.exp(-t*7)*.5
    return x
def stamp():
    d=.7;t=tt(d);x=np.sin(2*np.pi*(90*np.exp(-t*4)+40)*t)*np.exp(-t*9)*1.4+lp(noise(d),1500)*np.exp(-t*50)*.8
    return x
def impact(d=3.0):
    t=tt(d);x=np.sin(2*np.pi*(42*np.exp(-t*.8)+22)*t)*np.exp(-t*1.6)*1.6+lp(noise(d),120)*np.exp(-t*1.5)*.8
    x+=hp(noise(d),3000)*np.exp(-t*30)*.3
    return x*env(len(t),.003,.6)
def gong(d=5.0):
    t=tt(d);x=np.zeros(len(t))
    for f,a,dec in ((82,1,.5),(164.5,.6,.7),(231,.5,.9),(287,.35,1.1),(371,.3,1.4),(448,.2,1.8),(529,.15,2.2)):
        x+=a*np.sin(2*np.pi*f*t*(1+.002*np.sin(2*np.pi*3*t)))*np.exp(-t*dec)
    x+=lp(noise(d),300)*np.exp(-t*8)*.6
    return x*env(len(t),.004,1.0)*.9
def paper(d=.8):
    n=noise(d);x=bp(n,1500,6000)*(0.4+0.6*np.abs(np.sin(np.linspace(0,9,len(n)))))*env(len(n),.05,.3)
    return x*.6
def coins(n=6):
    d=1.2;out=np.zeros(int(d*SR))
    for k in range(n):
        i=int(rng.uniform(0,.8)*SR);t=tt(.4)
        f=rng.uniform(2400,4200);y=(np.sin(2*np.pi*f*t)+.6*np.sin(2*np.pi*f*2.76*t)+.3*np.sin(2*np.pi*f*5.4*t))*np.exp(-t*18)
        m=min(len(y),len(out)-i);out[i:i+m]+=y[:m]*.35
    return out
def shutter():
    d=.5;t=tt(d);x=hp(noise(d),2500)*np.exp(-t*80)*1.2;i=int(.08*SR);x[i:]+=hp(noise(d-.08),1500)*np.exp(-np.arange(len(x)-i)/SR*60)*.8
    x+=lp(noise(d),3000)*np.exp(-t*6)*.2;return x
def whistle(d=1.8):
    t=tt(d);vib=1+.004*np.sin(2*np.pi*5*t)
    x=sum(a*np.sign(np.sin(2*np.pi*f*vib*t))*.3+a*np.sin(2*np.pi*f*vib*t) for f,a in ((523,.6),(659,.5),(784,.4)))
    x=lp(x,2500)+bp(noise(d),1500,4000)*.15
    return x*env(len(t),.08,.4)*.5
def shiphorn(d=3.2):
    t=tt(d);vib=1+.003*np.sin(2*np.pi*4*t)
    x=np.zeros(len(t))
    for f,a in ((98,1),(147,.8),(196,.5),(294,.3)):
        ph=2*np.pi*f*vib*t;x+=a*(2*((ph/(2*np.pi))%1)-1)
    x=lp(x,700)
    return x*env(len(t),.25,.9)*.45
def bugle():
    notes=[(392,.22),(523,.22),(659,.22),(784,.5),(659,.22),(784,.8)]
    out=[]
    for f,d in notes:
        t=tt(d);vib=1+.006*np.sin(2*np.pi*5.5*t)*np.clip(t*4,0,1)
        y=sum(a*np.sin(2*np.pi*f*k*vib*t) for k,a in ((1,1),(2,.6),(3,.45),(4,.25),(5,.15)))
        out.append(y*env(len(t),.03,.06))
    x=np.concatenate(out);return lp(x,3500)*.32
def rewind():
    d=1.0;t=tt(d);f=200+3000*t**2
    x=np.sin(2*np.pi*np.cumsum(f)/SR)*.25+bp(noise(d),800,5000)*.5
    return x*env(len(t),.05,.2)*np.linspace(.4,1,len(t))
def whoosh(d=.45):
    n=noise(d);t=tt(d);k=np.sin(np.pi*t/d)
    x=bp(n,300,2500)*k**2
    return x*.5
def creak(d=1.8):
    t=tt(d);f=140+40*np.sin(2*np.pi*.7*t)+20*np.sin(2*np.pi*3.1*t)
    ph=np.cumsum(f)/SR;x=(2*(ph%1)-1)*(0.5+0.5*np.abs(np.sin(2*np.pi*9*t)))
    return bp(x,200,2500)*env(len(t),.1,.3)*.5
def slam():
    d=1.2;t=tt(d);return lp(noise(d),400)*np.exp(-t*12)*1.2+np.sin(2*np.pi*60*t)*np.exp(-t*10)
def clatter():
    d=1.0;out=np.zeros(int(d*SR))
    for k in range(7):
        i=int(rng.uniform(0,.6)*SR);t=tt(.25);f=rng.uniform(600,1500)
        y=(np.sin(2*np.pi*f*t)+.5*np.sin(2*np.pi*f*2.3*t))*np.exp(-t*25)+lp(noise(.25),2000)*np.exp(-t*40)
        m=min(len(y),len(out)-i);out[i:i+m]+=y[:m]*.35
    return out
def bombfall(d=1.0):
    t=tt(d);f=1800-1300*t/d;x=np.sin(2*np.pi*np.cumsum(f)/SR)*env(len(t),.05,.05)*.25
    return x
def pointer():
    out=np.zeros(int(1.2*SR))
    for k in range(3):
        i=int(k*.3*SR);t=tt(.1);y=lp(noise(.1),900)*np.exp(-t*60)
        out[i:i+len(y)]+=y
    return out
# ---------- beds ----------
def bed_sea(d):
    n=noise(d);t=tt(d);sw=.55+.45*np.sin(2*np.pi*.12*t+1)
    x=lp(n,500)*sw*.9+bp(noise(d),1500,5000)*(sw**3)*.25
    return x*env(len(t),.4,.6)*.5
def bed_wind(d):
    n=noise(d);t=tt(d);x=bp(n,250,1400)*(0.5+0.5*np.sin(2*np.pi*.17*t)*np.sin(2*np.pi*.07*t+2))
    return x*env(len(t),.4,.5)*.5
def bed_night(d):
    t=tt(d);x=bed_wind(d)*.5
    for k in range(int(d*3)):
        i=int(rng.uniform(0,d-.2)*SR);tc=tt(.15);y=np.sin(2*np.pi*4200*tc)*(np.sin(2*np.pi*30*tc)>0)*np.exp(-tc*8)*.05
        x[i:i+len(y)]+=y
    return x
def bed_rain(d):
    t=tt(d);x=hp(noise(d),2000)*.25
    for k in range(int(d*40)):
        i=int(rng.uniform(0,d-.05)*SR);m=int(.01*SR);x[i:i+m]+=hp(noise(.01),3000)*np.exp(-np.arange(m)/SR*400)*.3
    return x*env(len(t),.3,.3)
def bed_crowd(d):
    t=tt(d);x=np.zeros(len(t))
    for lo,hi in ((200,500),(400,900),(700,1500)):x+=bp(noise(d),lo,hi)*(.5+.5*np.sin(2*np.pi*rng.uniform(2,5)*t+rng.uniform(0,6)))
    return x*env(len(t),.3,.4)*.4
def bed_jeer(d):return bed_crowd(d)*1.3
def bed_train(d):
    t=tt(d);x=np.zeros(len(t));rate=3.2
    k=0.0
    while k<d-.2:
        i=int(k*SR);y=bp(noise(.18),400,3000)*np.exp(-np.arange(int(.18*SR))/SR*14)
        x[i:i+len(y)]+=y*.6;k+=1/rate
    k=0.1
    while k<d-.1:
        for dd in (0,.12):
            i=int((k+dd)*SR);m=int(.05*SR)
            if i+m<len(x):x[i:i+m]+=lp(noise(.05),1200)*np.exp(-np.arange(m)/SR*80)*.7
        k+=.9
    x+=lp(noise(d),150)*.3
    return x*env(len(t),.2,.3)*.6
def bed_mg(d):
    t=tt(d);x=np.zeros(len(t));k=0.0
    while k<d-.1:
        if (k%1.4)<1.0:
            i=int(k*SR);y=rifle()[:int(.12*SR)]*.5;x[i:i+len(y)]+=y
        k+=1/11
    return x
def bed_steps(d,fast=False):
    t=tt(d);x=np.zeros(len(t));step=.42 if not fast else .3
    for v in range(5):
        k=rng.uniform(0,step)
        while k<d-.15:
            i=int(k*SR);m=int(.12*SR);y=lp(noise(.12),300)*np.exp(-np.arange(m)/SR*35)+bp(noise(.12),1500,4000)*np.exp(-np.arange(m)/SR*50)*.2
            x[i:i+m]+=y*.35;k+=step+rng.uniform(-.02,.02)
    return x*env(len(t),.2,.3)
def bed_heart(d,fast=False):
    t=tt(d);x=np.zeros(len(t));k=0.05
    while k<d-.3:
        u=k/d;bpm=(70+60*u) if fast else 66
        for off,a in ((0,1),(.16,.7)):
            i=int((k+off)*SR);m=int(.25*SR);tc=np.arange(m)/SR
            y=np.sin(2*np.pi*(55-15*tc*4)*tc)*np.exp(-tc*22)*a
            if i+m<len(x):x[i:i+m]+=y
        k+=60/bpm
    return lp(x,200)*1.6
def bed_tele(d,urgent=False):
    t=tt(d);x=np.zeros(len(t));k=0.0;unit=.06 if urgent else .085
    while k<d-.3:
        L_=unit*(3 if rng.random()<.35 else 1);i=int(k*SR);m=int(L_*SR);tc=np.arange(m)/SR
        y=np.sin(2*np.pi*760*tc)*env(m,.004,.004)*.35
        x[i:i+m]+=y
        c_=lp(noise(.02),3000)*np.exp(-np.arange(int(.02*SR))/SR*200)*.4;x[i:i+len(c_)]+=c_
        k+=L_+unit*(1 if rng.random()<.7 else 3)
    return x
def bed_plane(d):
    t=tt(d);f=92+6*np.sin(2*np.pi*.3*t);ph=np.cumsum(f)/SR
    x=(2*(ph%1)-1)*(0.6+0.4*np.sin(2*np.pi*f*t*0+2*np.pi*24*t))
    x=lp(x,900)*.4+bp(noise(d),300,1200)*.15
    return x*np.interp(t,[0,d*.3,d*.7,d],[.3,1,1,.4])*env(len(t),.3,.5)
def bed_fire(d):
    t=tt(d);x=lp(noise(d),400)*.25
    for k in range(int(d*25)):
        i=int(rng.uniform(0,d-.03)*SR);m=int(.01*SR);x[i:i+m]+=hp(noise(.01),2000)*.3
    return x*env(len(t),.2,.3)
def bed_firecr(d):
    t=tt(d);x=np.zeros(len(t))
    for k in range(int(d*30)):
        i=int(rng.uniform(0,d-.1)*SR);y=rifle()[:int(.08*SR)]*rng.uniform(.2,.5);x[i:i+len(y)]+=hp(y,1000)
    return x
def bed_type(d):
    t=tt(d);x=np.zeros(len(t));k=0.0
    while k<d-.1:
        i=int(k*SR);m=int(.03*SR);x[i:i+m]+=hp(noise(.03),1500)*np.exp(-np.arange(m)/SR*150)*.5;k+=rng.uniform(.07,.16)
    return x
def bed_hoof(d):
    t=tt(d);x=np.zeros(len(t));k=0.0
    while k<d-.2:
        for off in (0,.08,.2,.27):
            i=int((k+off)*SR);m=int(.08*SR)
            if i+m<len(x):x[i:i+m]+=lp(noise(.08),500)*np.exp(-np.arange(m)/SR*50)*.6
        k+=.42
    return x
def bed_clock(d):
    t=tt(d);x=np.zeros(len(t));k=0.0
    while k<d-.1:
        i=int(k*SR);m=int(.03*SR);tc=np.arange(m)/SR;x[i:i+m]+=np.sin(2*np.pi*2200*tc)*np.exp(-tc*200)*.4;k+=.5
    return x
def bed_tick(d):
    t=tt(d);x=np.zeros(len(t));k=0.0;dt=.12
    while k<d-.1:
        i=int(k*SR);m=int(.02*SR);tc=np.arange(m)/SR;x[i:i+m]+=np.sin(2*np.pi*1600*tc)*np.exp(-tc*250)*.35;k+=dt;dt*=.97
    return x
def bed_fuse(d):
    t=tt(d);return hp(noise(d),3000)*(0.6+0.4*np.sin(2*np.pi*13*t))*.18*env(len(t),.1,.2)
def bed_zap(d):
    t=tt(d);x=bp(noise(d),800,2500)*(np.sin(2*np.pi*10*t)>.3)*.2;return x*env(len(t),.1,.2)
BEDF={'sea':bed_sea,'wind':bed_wind,'night':bed_night,'rain':bed_rain,'crowd':bed_crowd,'jeer':bed_jeer,'train':bed_train,'mg':bed_mg,'steps':bed_steps,
 'heart':bed_heart,'tele':bed_tele,'plane':bed_plane,'fire':bed_fire,'firecr':bed_firecr,'type':bed_type,'hoof':bed_hoof,'clock':bed_clock,'tick':bed_tick,'fuse':bed_fuse,'zap':bed_zap}
ONE={'boom':boom,'expl':expl,'rifle':rifle,'stamp':stamp,'impact':impact,'gong':gong,'paper':paper,'coins':coins,'shutter':shutter,'whistle':whistle,
 'shiphorn':shiphorn,'bugle':bugle,'rewind':rewind,'creak':creak,'slam':slam,'clatter':clatter,'bombfall':bombfall,'pointer':pointer}
GAIN={'boom':.55,'expl':.5,'rifle':.35,'stamp':.6,'impact':.75,'gong':.45,'paper':.35,'coins':.4,'shutter':.5,'whistle':.45,'shiphorn':.6,'bugle':.4,'rewind':.45,
 'creak':.4,'slam':.5,'clatter':.45,'bombfall':.5,'pointer':.3,'sea':.55,'wind':.45,'night':.5,'rain':.45,'crowd':.35,'jeer':.4,'train':.45,'mg':.35,'steps':.45,
 'heart':.75,'tele':.3,'plane':.45,'fire':.35,'firecr':.3,'type':.35,'hoof':.45,'clock':.35,'tick':.35,'fuse':.4,'zap':.3}
FX=list(common.FX)
# 自动：源码里的 stamp()/bigword() 时间点（若手动未放 stamp）
for t0,t1,fn,pl in SH:
    try:src=inspect.getsource(fn)
    except Exception:continue
    for m in re.finditer(r"stamp\(c,t,(?:bt\(([\d.]+)\)|([\d.]+))",src):
        ts=t0+(float(m.group(1))*B if m.group(1) else float(m.group(2)))
        if not any(e['k']=='stamp' and abs(e['t']-ts)<.25 for e in FX):FX.append(dict(t=ts,k='stamp',g=.9,d=0,p=()))
    for m in re.finditer(r"bigword\(c,t,(?:bt\(([\d.]+)\)|([\d.]+))",src):
        ts=t0+(float(m.group(1))*B if m.group(1) else float(m.group(2)))
        FX.append(dict(t=ts,k='impact',g=.45,d=0,p=()))
pan_r=np.random.default_rng(3)
for e in FX:
    k=e['k'];g=e['g']*GAIN.get(k,.4);pan=float(pan_r.uniform(-.35,.35))
    if k in BEDF:
        f=BEDF[k];d=max(.3,e['d'])
        if k in('heart','steps') :x=f(d,fast=('fast' in e['p']))
        elif k=='tele':x=f(d,urgent=('urgent' in e['p']))
        else:x=f(d)
        x=x*env(len(x),.08,.25);put(x,e['t'],g,pan*.3)
    elif k in ONE:
        put(ONE[k](),e['t'],g,pan)
    else:print('unknown fx',k)
# 切点 whoosh
for ct in render.CUTS:put(whoosh(),ct-.18,.12,float(pan_r.uniform(-.5,.5)))
# 结尾海浪尾音
put(bed_sea(4.0),TOTAL-1.0,.35)
# ---------- 混音总线 ----------
st=np.stack([L,R])
# 轻压缩：0.4s 窗 RMS 超过阈值部分压缩
from scipy.ndimage import uniform_filter1d
rms=np.sqrt(uniform_filter1d(np.mean(st**2,0),int(.4*SR))+1e-9)
thr=0.22;gain=np.where(rms>thr,(thr/rms)**.5,1.0)
gain=uniform_filter1d(gain,int(.05*SR))
st*=gain
st=np.tanh(st*1.1)/np.tanh(1.1)
pk=np.max(np.abs(st));st*=0.76/pk
r=np.sqrt(np.mean(st**2));print('peak',np.max(np.abs(st)),'rms dBFS',20*np.log10(r))
out=(np.clip(st.T,-1,1)*32767).astype(np.int16)
with wave.open('sfx.wav','wb') as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(out.tobytes())
print('dur',N/SR,'events',len(FX))
