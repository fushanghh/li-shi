import numpy as np, wave, math
import synth
from synth import *
B=60/96;NB=216;TOT=NB*B
N=int((TOT+3)*SR);L=np.zeros(N);R=np.zeros(N);RV=np.zeros(N);SF=np.zeros(N);K=np.zeros(N)
def put(sig,t0,g=1.0,pan=0.0,rev=0.0,sfx=False):
    i=int(t0*SR)
    if i<0 or i>=N:return
    j=min(N,i+len(sig));s=sig[:j-i]*g
    l=math.cos((pan+1)*math.pi/4)*1.41;r=math.sin((pan+1)*math.pi/4)*1.41
    if sfx:SF[i:j]+=s
    else:L[i:j]+=s*l;R[i:j]+=s*r
    if rev:RV[i:j]+=s*rev
C={}
def ca(k,f):
    if k not in C:C[k]=f()
    return C[k]
def b(x):return x*B
D=50  # D3
MIN=[0,3,5,7,10]
def sc(deg,base=D):o,i=divmod(deg,5);return base+12*o+MIN[i]
def kickat(bb,g=.85):put(ca('k',kick),b(bb),g);i=int(b(bb)*SR);K[i:i+5000]=1
def gallop(t0,dur):
    t=t0
    while t<t0+dur:
        for d in (0,.09,.18):put(ca('st',step),t+d,.5,0)
        t+=B
# ---- 0-24 钩子 ----
put(pad([D-12,D-5,D],b(24),500),0,.45,0,.3)
for bb in range(0,24,2):put(ca('tk',lambda:taiko(55)),b(bb),.7);K[int(b(bb)*SR):int(b(bb)*SR)+4000]=1
for bb in range(8,14):put(ca(('ss',D+12),lambda:strings_stac(D+12)),b(bb+.5),.35,.3)
put(bigimpact(),b(2),.9);put(mx(hit(),wood(800)),b(4),.7);put(mx(hit(),wood(700)),b(9),.7)
put(tremolo([D,D+3,D+7],b(6)),b(14),.4,0,.4)
put(riser(b(2)),b(18),.5);put(bigimpact(),b(20),1.0,0,.4);put(gong(),b(20),.5,0,.5)
# ---- 24-56 张亮：神秘拨弦 ----
pat=[0,3,2,3,0,4,3,2]
for bb in range(24,56):
    for q in range(2):
        m=sc(pat[(bb*2+q)%8]+5);put(ca(('pl',m),lambda:pluck(m,1.0,.5)),b(bb)+q*B/2,.38,-.3+.6*q,.3)
    if bb%2==0:kickat(bb,.6)
    put(ca('h',hat),b(bb+.5),.22,.4)
    if bb%8==0:put(ca(('bsl',bb//8),lambda:bass(D-12+[0,0,-2,-4][(bb//8)%4],b(8),'hold')),b(bb),.5)
for bb in (24.5,27,32,38,39,44.5):put(mx(hit(),wood(900)),b(bb),.5)
for bb in (46,48):put(mx(crack(),hit()),b(bb),.9,sfx=False)
put(erhu(sc(7,D),b(4)),b(50),.45,0,.5);put(erhu(sc(5,D),b(2)),b(54),.45,0,.5)
put(bigimpact(),b(52),.8,0,.4)
# ---- 56-80 地形：渐强 ----
for bb in range(56,80):
    put(ca(('ss2',bb%4),lambda:strings_stac(sc([0,2,3,4][bb%4]+10))),b(bb),.35,.2)
    put(ca(('ss2',bb%4),lambda:strings_stac(sc([0,2,3,4][bb%4]+10))),b(bb+.5),.25,-.2)
    if bb>=64:kickat(bb,.7)
    elif bb%2==0:kickat(bb,.5)
    if bb>=64 and bb%2==1:put(ca('sn',snare),b(bb),.45)
put(pad([D-12,D-9,D-5],b(24),900),b(56),.3,0,.3)
put(mx(brass([D,D+7,D+12],.8),crash()*.5),b(64),.9,0,.3)
put(mx(brass([D-1,D+6,D+11],.8),bigimpact()*.6),b(70),.9,0,.3)
put(mx(hit(),wood(800)),b(76.3),.6);put(stab(),b(78),.8)
put(riser(b(2)),b(78),.6);put(revcym(b(1)),b(79),.7)
# ---- 80-100 逃亡：双倍速 ----
for bb in range(80,100):
    kickat(bb,.9)
    if bb%2==1:put(ca('sn',snare),b(bb),.6);put(ca('cl',clap),b(bb),.3)
    for q in range(4):put(ca('h',hat),b(bb)+q*B/4,.3 if q%2 else .4,.35)
    root=[0,0,-2,-4][((bb-80)//4)%4]
    for q in range(2):put(ca(('b8',root),lambda:bass(D-12+root,B*.45)),b(bb)+q*B/2,.6)
    for q in range(4):
        m=sc([0,2,3,4][q]+(5 if bb%2 else 6),D+root);put(ca(('p16',m),lambda:pluck(m,.5,.8)),b(bb)+q*B/4,.3,-.4+.25*q,.2)
gallop(b(80),b(6));gallop(b(92),b(4))
for bb in (86.5,88,90):put(mx(taiko(70),hit()),b(bb),.8)
t=b(84)
for dg,du in [(7,1),(8,1),(9,2),(8,1),(7,1),(5,2),(7,2),(9,1),(10,1),(12,4)]:
    m=sc(dg,D+12);put(dizi(m,du*B*.9),t,.45,.1,.4);t+=du*B
put(mx(bigimpact(),brass([D,D+7,D+12],.8)),b(96),1.0,0,.4)
# ---- 100-120 关东：英雄铜管 ----
put(choir([D-12,D-5,D,D+3],b(16)),b(100),.4,0,.5)
for bb in range(100,120):
    if bb%2==0:put(ca('tk',lambda:taiko(55)),b(bb),.6)
    kickat(bb,.5)
    put(ca('h',hat),b(bb+.5),.2,.4)
for bb,ch in ((100,[D,D+7,D+12]),(104,[D-2,D+5,D+10]),(108,[D-4,D+3,D+8]),(112,[D-5,D+2,D+7])):put(brass(ch,1.4),b(bb),.6,0,.3)
for bb in (102,104):put(stab(),b(bb),.8)
for bb in (108.5,109.7,110.9):put(mx(hit(),wood(1000)),b(bb),.6)
put(gong(),b(115.5),.6,0,.5)
put(tremolo([D,D+3,D+7],b(4)),b(114),.35,0,.3)
# ---- 120-144 三步：军鼓推进 ----
for bb in range(120,144):
    put(ca('tk2',lambda:taiko(62)),b(bb),.55);K[int(b(bb)*SR):int(b(bb)*SR)+4000]=1
    for q in range(2):put(ca('sn2',lambda:snare()*.5),b(bb)+q*B/2+B/4,.3)
    if bb%4==0:put(brass([D-12,D-5],b(1)),b(bb),.45)
put(pad([D-12,D-9,D-5],b(24),700),b(120),.3,0,.3)
for bb in (120,128,136):put(bigimpact(),b(bb),.8,0,.3)
for bb in (122,124):put(mx(metal([600,900,1350],.8,6),hit()),b(bb),.8)
put(mx(crashfx(),hit()),b(130),.8);
for bb in (132,134):put(mx(hit(),wood(600)),b(bb),.6)
put(stab(),b(141),.8);put(gong(),b(141),.4,0,.5)
# ---- 144-176 天下两分 + 突厥 ----
put(choir([D-12,D-5,D,D+3],b(8)),b(144),.55,0,.5)
for bb in range(144,152):kickat(bb,.7);put(ca('tk',lambda:taiko(55)),b(bb),.5)
put(mx(bigimpact(),crash()*.6),b(148),1.0,0,.4)
put(tremolo([D-12,D-11,D-5],b(8)),b(152),.5,0,.3)
for bb in range(152,160,2):put(brass([D-24,D-17],b(1.5)),b(bb),.5);kickat(bb,.7)
for bb in (154,155):put(mx(taiko(60),hit()),b(bb),.8)
for bb in range(160,168):
    kickat(bb,.9);put(ca('tk',lambda:taiko(55)),b(bb),.6)
    for q in range(4):put(ca('tm',lambda:tom(110)),b(bb)+q*B/4,.25 if q else .4,-.2)
    put(ca('sn',snare),b(bb+.5),.4)
gallop(b(160),b(8))
put(choir([D-12,D-9,D-5,D],b(8)),b(160),.45,0,.5)
put(mx(bigimpact(),gong()*.6),b(170),1.0,0,.5)
put(pad([D-14,D-10,D-7],b(6),500),b(170),.4,0,.4)
# ---- 176-200 那一箭 ----
put(tremolo([D,D+1,D+7],b(6)),b(176),.45,0,.3)
for bb in (176,178,180):put(ca('tk',lambda:taiko(55)),b(bb),.6)
for bb in (182,183):put(heartbeat(),b(bb),.9,sfx=True)
put(breath(),b(183),.8,sfx=True)
put(arrow(),b(184),1.0,sfx=True)
put(mx(bigimpact(),crashfx()*.8,gong()*.5),b(188),1.1,0,.5)
for bb in range(188,194):kickat(bb,.6)
put(choir([D-12,D-5,D,D+3],b(6)),b(188),.45,0,.5)
put(erhu(sc(7,D),b(3)),b(194),.45,0,.6);put(erhu(sc(6,D),b(3)),b(197),.45,0,.6)
put(pad([D-12,D-5,D],b(6),600),b(194),.35,0,.4)
# ---- 200-216 尾声 ----
t=b(200)
for dg,du in [(7,2),(8,1),(7,1),(5,2),(4,2),(5,4),(3,4)]:
    m=sc(dg,D+12);put(dizi(m,du*B*.95),t,.45,0,.6);t+=du*B
put(pad([D-12,D-5,D,D+3],b(16),700),b(200),.35,0,.5)
for bb in range(200,212,2):put(ca(('pl',sc(5)),lambda:pluck(sc(5),1.4)),b(bb),.3,.2,.4)
put(mx(gong(),boom()*.6),b(205),.9,0,.6)
for bb in (201,201.8,202.6,203.5):put(mx(hit(),wood(1000)),b(bb),.5)
for bb in (2,20,52,78,96,141,148,170,188):put(swish(),b(bb)-.18,.5,sfx=True)
def fftconvolve(x,h):
    n=len(x)+len(h);nf=1<<(n-1).bit_length()
    return np.fft.irfft(np.fft.rfft(x,nf)*np.fft.rfft(h,nf),nf)
duck=1-.35*np.convolve(K,np.ones(2000)/2000,'same').clip(0,1)
ir=rng.standard_normal(int(2.4*SR))*np.exp(-T(int(2.4*SR))*2.6);ir[:800]=0
rv=fftconvolve(fft_filt(RV,200,6000),ir)[:N]*.03
oL=L*duck*.6+SF*.75+rv;oR=R*duck*.6+SF*.75+rv
n=int(TOT*SR);oL=oL[:n];oR=oR[:n]
f=int(2.5*SR);oL[-f:]*=np.linspace(1,0,f);oR[-f:]*=np.linspace(1,0,f)
pk=np.percentile(np.abs(np.r_[oL,oR]),99.8)+1e-9
oL=np.tanh(oL/pk*.95)*.9;oR=np.tanh(oR/pk*.95)*.9
w=wave.open('xuanwu.wav','wb');w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR)
w.writeframes((np.stack([oL,oR],1)*32767).astype(np.int16).tobytes());w.close();print('ok',n/SR)
