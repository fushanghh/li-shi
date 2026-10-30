from common import *
from props import *
import nmap as M
from figq import person,horse
_SP2={}
def spr(kind,pose,h,face=1,ph=0,eyes='dot'):
    k=(kind,pose,int(h),face,ph,eyes)
    if k not in _SP2:
        sw,shh=int(h*1.6),int(h*1.5)
        sf=cairo.ImageSurface(cairo.FORMAT_ARGB32,sw,shh);cc=cairo.Context(sf)
        person(cc,sw/2,shh*.92,h,kind,pose=pose,face=face,eyes=eyes,t=ph*0.26+.05)
        _SP2[k]=(sf,sw/2,shh*.92)
    return _SP2[k]
def army(seed,n,x0,x1,y0,y1,kinds,poses=('stand',),hfar=40,hnear=130,faces=(1,),grid=False,cols=20):
    r=random.Random(seed);L=[]
    for i in range(n):
        if grid:
            row=i//cols;cc=i%cols;rows=max(1,(n+cols-1)//cols)
            y=lerp(y0,y1,row/max(1,rows-1));x=lerp(x0,x1,cc/max(1,cols-1))+(row%2)*((x1-x0)/cols/2)+r.uniform(-6,6)
        else:
            y=r.uniform(y0,y1);x=r.uniform(x0,x1)
        k=(y-y0)/(y1-y0) if y1>y0 else 1
        L.append(dict(x=x,y=y,h=lerp(hfar,hnear,k),kind=r.choice(kinds),pose=r.choice(poses),ph=r.uniform(0,6.28),face=r.choice(faces),i=i))
    L.sort(key=lambda d:d['y']);return L
def hbk(h):
    for b in (60,120,200):
        if h<=b*1.15:return b
    return 200
def draw_army(c,L,t,dx=0,bob=3,march=0,pose=None,face=None,a=1,spd=6,tint=None):
    for d in L:
        b=hbk(d['h']);sc=d['h']/b
        p=pose or d['pose']
        ph=int((t*spd*.5+d['ph'])%4) if p in('walk','run') else 0
        sp=spr(d['kind'],p,b,d['face'] if face is None else face,ph)
        yy=d['y']-abs(math.sin(t*(4+march*5)+d['ph']))*(bob+march*5)*sc
        blit(c,sp,d['x']+dx*(d['h']/100),yy,sc,a)
def flags(c,xs,y,h,t,txt,colr,s=1,a=1,tc='#efe2c4'):
    for i,x in enumerate(xs):banner(c,x,y,h,t,txt,colr,a,s,tc=tc,seed=i)
def nightsky(c,cam,t,top='#070a12',bot='#1c2030',stars=60,moon=None,y1=200):
    with layer(c,cam,.03):
        sky(c,top,bot,-900,y1)
        r=random.Random(4)
        for i in range(stars):circ(c,r.uniform(-1400,1400),r.uniform(-700,-100),r.uniform(1,2.4),'#e8e8f0',r.uniform(.2,.7)*(.7+.3*math.sin(t*2+i)))
        if moon:circ(c,moon[0],moon[1],46,'#e8e4d8',.85);glow(c,moon[0],moon[1],200,'#c8d0e0',.25)
def far_fires(c,t,y,n=8,seed=3,x0=-1600,x1=1600,s=.6):
    r=random.Random(seed)
    for i in range(n):x=r.uniform(x0,x1);fire(c,x,y+r.uniform(-20,20),s*r.uniform(.6,1.2),t,seed=i);smoke(c,t,x,y-60,s*1.5,6,seed=i,colr='#151010',a=.45)
def bjskyline(c,y,colr='#14121a',t=0,lit=.6):
    r=random.Random(8)
    x=-2600
    while x<2600:
        w=r.uniform(120,260);h=r.uniform(50,110)
        rect(c,x,y-h,w,h+400,colr)
        poly(c,[(x-20,y-h),(x+w+20,y-h),(x+w-10,y-h-30),(x+10,y-h-30)],colr)
        if r.random()<lit:rect(c,x+w*.4,y-h*.6,16,14,'#ffb050',.5)
        x+=w+r.uniform(10,40)
def vign(c,a=.6):
    g=cairo.RadialGradient(W/2,H/2,300,W/2,H/2,1100);g.add_color_stop_rgba(0,0,0,0,0);g.add_color_stop_rgba(1,0,0,0,a);c.set_source(g);c.paint()
def tint(c,h,a):rect(c,0,0,W,H,h,a)
def label2(c,t,t0,s,x,y,size=40,colr=None):label(c,t,t0,s,x,y,size,colr)
def infocard(c,t,t0,x,y,name,yrs,lines,w=430):
    k=eo((t-t0)/.35)
    if k<=0:return
    a=k
    rect(c,x,y,w,90+len(lines)*40,'#0a0705',.72*a);rect(c,x,y,6,90+len(lines)*40,RED,a)
    clib.htext(c,name,x+30,y+56,46,clib.IVORY,a,align='l');text(c,yrs,x+40+len(name)*48,y+54,24,'#c8b48a',a,align='l')
    for i,l in enumerate(lines):text(c,l,x+30,y+100+i*40,26,'#d8ccb0',a,align='l')
