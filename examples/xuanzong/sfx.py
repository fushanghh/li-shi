import numpy as np, wave
SR=44100;T=142;N=SR*T
rng=np.random.default_rng(1)
L=np.zeros(N);R=np.zeros(N)
def add(sig,t,pan=0.0,g=1.0):
    i=int(t*SR);n=min(len(sig),N-i)
    if n<=0:return
    L[i:i+n]+=sig[:n]*g*(1-pan)/1;R[i:i+n]+=sig[:n]*g*(1+pan)/1
def env(n,a,d):
    t=np.arange(n)/SR;return np.minimum(1,t/a)*np.exp(-t/d)
def lp(x,k):
    y=np.copy(x)
    for _ in range(k):y=np.convolve(y,np.ones(8)/8,'same')
    return y
def stamp():
    n=int(.6*SR);t=np.arange(n)/SR
    body=np.sin(2*np.pi*(70*np.exp(-t*6)+45)*t)*env(n,.002,.12)
    nz=lp(rng.standard_normal(n),3)*env(n,.001,.04)
    return .8*body+.5*nz
def gong(f=110,d=3.5):
    n=int(d*SR);t=np.arange(n)/SR
    s=sum(a*np.sin(2*np.pi*f*m*t*(1+.002*np.sin(t*5))) for m,a in [(1,1),(2.02,.5),(2.76,.35),(3.9,.2),(5.4,.12)])
    return s*env(n,.01,1.2)*.35
def ding(f=1320):
    n=int(1.2*SR);t=np.arange(n)/SR
    return (np.sin(2*np.pi*f*t)+.4*np.sin(2*np.pi*f*2.7*t))*env(n,.002,.35)*.12
def tick():
    n=int(.08*SR);return lp(rng.standard_normal(n),1)*env(n,.0005,.012)*.25
def whoosh(d=.7):
    n=int(d*SR);x=rng.standard_normal(n);t=np.arange(n)/SR
    e=np.sin(np.pi*t/d)**2;y=lp(x,4)*e
    return y*.18
def cheer(d=7):
    n=int(d*SR);x=np.zeros(n)
    for k in range(60):
        st=rng.integers(0,n-SR);m=int(SR*rng.uniform(.3,.8));tt=np.arange(m)/SR
        f=rng.uniform(250,600);v=np.sin(2*np.pi*f*tt+3*np.sin(2*np.pi*6*tt))*np.sin(np.pi*tt/tt[-1])
        x[st:st+m]+=v*.05
    x+=lp(rng.standard_normal(n),6)*.08
    t=np.arange(n)/SR;return x*np.minimum(1,t/1)*np.minimum(1,(d-t)/1)
def crackle(d):
    n=int(d*SR);x=lp(rng.standard_normal(n),5)*.05
    for k in range(int(d*12)):
        i=rng.integers(0,n-500);x[i:i+400]+=rng.standard_normal(400)*np.exp(-np.arange(400)/60)*.25
    return x
# wind bed
wb=lp(rng.standard_normal(N),12);wb*= (0.6+0.4*np.sin(np.arange(N)/SR*0.3))*0.35
L+=wb*.5;R+=np.roll(wb,4000)*.5
starts=[0,7,13,19,26,33,41,48,56,64,72,81,90,99,110,117,123,132]
for s in starts[1:]:add(whoosh(),s-.45,0,1)
add(gong(98,5),0.3,0,1.2)
for t in [2.6,23,27.2,44.4,61.3,96.5,107,119.2,137]:add(stamp(),t,0,1.1)
add(gong(130,4),50.2,0,.9);add(gong(82,6),117.3,0,1.2)
for i in range(3):add(ding(1100+i*150),82.2+i*.9,(i-1)*.3)
for i in range(7):add(tick(),84.8+i*.25,(i-3)/5,1.5)
for i in range(10):add(ding(900+i*60),100.6+i*.3,(i-5)/8,.8)
add(ding(1500),99.8,0,1.2)
# timeline pops
def tlpops(start,T,y0,y1,yrs):
    for yr in yrs:
        for k in np.linspace(0,1,2000):
            x=k*k*(3-2*k);
            if y0+(y1-y0)*x>=yr:add(ding(760),start+k*(T-1.2 if y1==850 else T-1.5),0,.9);break
tlpops(33,8,805,850,[810,820,824,826,840,846]);tlpops(123,9,855,910,[859,860,868,875,880,907])
add(cheer(8),91.5,0,1.0)
add(crackle(7),110,.3,1)
# lideyu route whooshes
for t in [56.6,58,59.7]:add(whoosh(1.2),t,0,.8)
add(whoosh(4),102,0,.6)
m=np.max(np.abs(np.stack([L,R])));L/=m/0.8;R/=m/0.8
fade=np.ones(N);fade[-SR:]=np.linspace(1,0,SR);L*=fade;R*=fade
d=(np.stack([L,R],1)*32767).astype(np.int16)
w=wave.open('sfx.wav','wb');w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(d.tobytes());w.close();print('ok')
