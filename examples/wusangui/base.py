from lib import *
import clib
from scene3 import layer,sky,clouds,tri_mts,ridge,peaks,tree,house,tent,reeds,rain,splashes,lightning,fire,embers,smoke,dust,arrows,petals,banner,citywall,gatetower,ground
from figq import person,horse
from hud import slam,pop,bigword,stamp,counter,badge,vs_line
import geo3 as G
INK='#120c08';seg=clib.seg;eio=clib.eio;ell=clib.ell;line=clib.line
BPM=100;B=60/BPM
def bt(b):return b*B
SH=[];SUBS=[]
def shot(b0,b1,place=''):
    def d(fn):SH.append((bt(b0),bt(b1),fn,place));return fn
    return d
def sub(b0,b1,s,src=None):SUBS.append((bt(b0),bt(b1),s,src))
def ramp(t,t0,t1):return ease((t-t0)/(t1-t0)) if t1>t0 else float(t>=t1)
# ---- 人群精灵缓存 ----
_SP={}
def sprite(kind,pose,h,face=1,eyes='dot'):
    k=(kind,pose,int(h),face,eyes)
    if k not in _SP:
        sw,shh=int(h*1.4),int(h*1.5)
        sf=cairo.ImageSurface(cairo.FORMAT_ARGB32,sw,shh);cc=cairo.Context(sf)
        person(cc,sw/2,shh*.92,h,kind,pose=pose,face=face,eyes=eyes,t=.3)
        _SP[k]=(sf,sw/2,shh*.92)
    return _SP[k]
def blit(c,spr,x,y,sc=1.0,a=1.0):
    sf,ox,oy=spr
    c.save();c.translate(x,y);c.scale(sc,sc);c.set_source_surface(sf,-ox,-oy)
    c.paint_with_alpha(a) if a<1 else c.paint();c.restore()
def crowd(seed,n,x0,x1,y0,y1,kinds,poses=('stand',),hfar=40,hnear=130,faces=(1,)):
    r=random.Random(seed);L=[]
    for i in range(n):
        y=r.uniform(y0,y1);k=(y-y0)/(y1-y0) if y1>y0 else 1
        L.append(dict(x=r.uniform(x0,x1),y=y,h=lerp(hfar,hnear,k),kind=r.choice(kinds),pose=r.choice(poses),ph=r.uniform(0,6.28),face=r.choice(faces)))
    L.sort(key=lambda d:d['y']);return L
def hb(h):
    for b in (50,100,180):
        if h<=b*1.2:return b
    return 180
def draw_crowd(c,L,t,bob=4,dx=0,a=1,march=0,flip=None,pose=None):
    for d in L:
        b=hb(d['h']);sc=d['h']/b
        spr=sprite(d['kind'],pose or d['pose'],b,d['face'] if flip is None else flip)
        yy=d['y']-abs(math.sin(t*(5+march*4)+d['ph']))*(bob+march*6)*sc
        blit(c,spr,d['x']+dx*(d['h']/100),yy,sc,a)
def banners(c,xs,y,h,t,txt,colr,s=1,a=1):
    for i,x in enumerate(xs):banner(c,x,y,h,t,txt,colr,a,s,seed=i)
def letterbox(c,a=1,h=80):rect(c,0,0,W,h*a,'#000000');rect(c,0,H-h*a,W,h*a,'#000000')
def scroll_doc(c,x,y,w,h,lines,t,t0,title='',seal=None,a=1):
    k=eo((t-t0)/.6);ww=w*k
    rect(c,x-ww/2,y-h/2,ww,h,'#e8dcbc',a);rect(c,x-ww/2-14,y-h/2-8,14,h+16,'#5a3a1a',a);rect(c,x+ww/2,y-h/2-8,14,h+16,'#5a3a1a',a)
    if k<.95:return
    for i,ln in enumerate(lines):
        clib.vtext(c,ln,x+w/2-80-i*70,y-h/2+70,46,'#1a120c',a)
    if title:clib.vtext(c,title,x-w/2+60,y-h/2+60,30,'#7a1f1a',a)
    if seal and t>seal[0]:
        sc=slam(t,seal[0]) or 1;c.save();c.translate(seal[1],seal[2]);c.scale(sc,sc);rect(c,-60,-60,120,120,RED,.9);clib.vtext(c,seal[3],0,-22,40,'#f3e6c8');c.restore()
def chapter(c,t,num,title,sub_):
    # 章节卡：墨色背景+大号数字+标题
    rect(c,0,0,W,H,'#0d0907')
    for i in range(14):
        k=cl(t*2.2-i*.05);col(c,'#2a1c12',.6*k);c.set_line_width(80);c.move_to(-200+i*170,H+100);c.line_to(-200+i*170+600*k,-100+0*k);c.stroke()
    glow(c,W*.32,H/2,520,'#c0392b',.25)
    sc=slam(t,.0,.22) or 1
    c.save();c.translate(W*.32,H/2+40);c.scale(sc,sc);text(c,num,0,150,420,'#c0392b',.9);c.restore()
    text(c,'盲区 · '+['','一','二','三','四','五'][int({'①':1,'②':2,'③':3,'④':4,'⑤':5}.get(num,0)) if num in '①②③④⑤' else 0],W*.62,H/2-110,40,GREY,cl(t*3),sp=12)
    bigword(c,t,.35,title,W*.64,H/2+10,150)
    if t>.9:text(c,sub_,W*.64,H/2+140,42,'#c8b48a',cl((t-.9)*3),sp=6)
def place_tag(c,txt,a=1):
    text(c,txt,W-60,120,30,'#f3e6c8',a,align='r')
def topbar(c,T,frac,place,yrs=('1673','1681')):
    rect(c,0,0,W,74,'#000000',.35)
    text(c,yrs[0],60,46,22,GREY,align='l');text(c,yrs[1],560,46,22,GREY,align='l')
    col(c,GREY,.6);c.set_line_width(2);c.move_to(120,38);c.line_to(545,38);c.stroke()
    col(c,RED);c.set_line_width(4);c.move_to(120,38);c.line_to(120+425*frac,38);c.stroke();circ(c,120+425*frac,38,7,RED)
    if place:rect(c,W-48-len(place)*28-30,22,6,34,RED);text(c,place,W-50,48,26,CREAM,align='r')
def ships(c,x,y,s,t,colr='#3a2a1c',sail='#d8ccb0',face=1,fire_=0,txt=''):
    c.save();c.translate(x,y+math.sin(t*2+x)*4*s);c.scale(face*s,s)
    poly(c,[(-120,0),(120,0),(90,40),(-100,40)],colr,1,INK,2)
    line(c,0,0,0,-170,'#2a1c10',5)
    poly(c,[(4,-165),(80,-150),(80,-30),(4,-20)],sail,1,INK,1.5)
    for k in range(5):line(c,4,-150+k*26,80,-140+k*26,'#8a7a5a',1.2)
    if txt:text(c,txt,42,-80,40,'#7a1f1a')
    if fire_:fire(c,-40,0,1.2,t,seed=int(x))
    c.restore()
