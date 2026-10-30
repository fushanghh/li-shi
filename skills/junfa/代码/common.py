from base import *
import clib
CUR=[0]
FX=[]
def nx(n,place='',s=None,src=None,fx=()):
    b0=CUR[0];CUR[0]+=n
    if s:sub(b0,b0+n,s,src)
    for e in fx:FX.append(dict(t=bt(b0+e[0]),k=e[1],g=e[2] if len(e)>2 else 1.0,d=bt(e[3]) if len(e)>3 and e[3] else bt(n-e[0]),p=tuple(e[4:])))
    def d(fn):SH.append((bt(b0),bt(b0+n),fn,place));return fn
    return d
BEDS=('sea','wind','rain','crowd','train','mg','steps','heart','tele','plane','fire','firecr','night')
CN=['','一','二','三']
def card(c,t,n,title,sub_,label=None):
    rect(c,0,0,W,H,'#0d0907')
    for i in range(16):
        k=eo(t*2.4-i*.04);col(c,'#2a1c12',.55);c.set_line_width(90);c.move_to(-300+i*150,H+120);c.line_to(-300+i*150+700*k,H+120-1400*k);c.stroke()
    glow(c,W*.3,H/2,560,'#c0392b',.28)
    sc=slam(t,0,.22) or 1
    c.save();c.translate(W*.3,H/2+20);c.scale(sc,sc)
    clib.htext(c,n,0,150,420,('#ff7a5a','#a8261c'),.95);c.restore()
    text(c,label or '第'+'一二三'[int(n)-1]+'件事',W*.64,H/2-130,40,'#c8b48a',cl(t*3),sp=14)
    bigword(c,t,.3,title,W*.64,H/2-10,160)
    if t>.8:clib.htext(c,sub_,W*.64,H/2+130,46,clib.IVORY,cl((t-.8)*3))
def bubble(c,t,t0,x,y,s,w=None,face=1,size=46):
    k=eback(cl((t-t0)/.3))
    if k<=0:return
    c.save();c.translate(x,y);c.scale(k,k)
    c.select_font_face(clib.FONTH,0,1);c.set_font_size(size)
    lines=s.split('|');tw=max(c.text_extents(l)[4] for l in lines);bw=tw+80;bh=len(lines)*size*1.3+50
    clib.path(c,[(-bw/2,-bh),(bw/2,-bh),(bw/2,0),(30*face,0),(-10*face,50),(-20*face,0),(-bw/2,0)])
    col(c,'#f6ecd4',.96);c.fill_preserve();col(c,'#2a160b');c.set_line_width(5);c.stroke()
    for i,l in enumerate(lines):
        e=c.text_extents(l)[4];c.move_to(-e/2,-bh+40+size*.9+i*size*1.3);c.text_path(l);col(c,'#5a1410');c.fill()
    c.restore()
def palace(c,cam,t,tone=0,lamp=1):
    han=tone==2
    if han:tone=0
    # tone 0 盛世金红, 1 冷暗
    with layer(c,cam,.1):sky(c,'#1a0e0a' if tone==0 else '#0c0c12','#3a1c12' if tone==0 else '#1a1820',-700,400)
    with layer(c,cam,.45):
        for x in (-1100,-750,-400,400,750,1100):
            rect(c,x-34,-700,68,1000,('#2a1210' if han else '#7a1c16') if tone==0 else '#3a1a18');rect(c,x-34,-700,10,1000,('#8a2a20' if han else '#b03028') if tone==0 else '#4a2420')
        for x in (-575,575):
            rect(c,x-150,-420,300,330,'#2a140c');col(c,GOLD,.55 if tone==0 else .25);c.set_line_width(3)
            for k in range(7):c.move_to(x-150+k*50,-420);c.line_to(x-150+k*50,-90)
            for k in range(7):c.move_to(x-150,-420+k*55);c.line_to(x+150,-420+k*55)
            c.stroke();glow(c,x,-250,260,'#ffb050',(.25 if tone==0 else .08))
        rect(c,-2400,-720,4800,90,'#1a0c08')
        for i in range(-12,13):rect(c,i*200-60,-640,120,24,'#c99a3a' if tone==0 else '#5a4a30')
    with layer(c,cam,.75):
        rect(c,-260,-380,520,360,'#3a2414');rect(c,-240,-360,480,320,'#c8b48a' if tone==0 else '#6a6050')
        tri_mts(c,0,-60,9,4,sz=70,spread=200,light='#6a7a5a',dark='#3a4a30',a=.7)
        ground(c,250,'#2a1810' if tone==0 else '#16141a','#0a0604')
        rect(c,-500,250,1000,30,'#7a1f1a' if tone==0 else '#3a1a18')
    if lamp:
        with layer(c,cam,.9):
            for i,x in enumerate((-900,-650,650,900)):
                fl=.8+.2*math.sin(t*9+i);line(c,x,-700,x,-420,'#2a1c10',3)
                ell(c,x,-380,40,55,'#c0392b');glow(c,x,-380,140,'#ffb050',.45*fl*(1 if tone==0 else .4))
                rect(c,x-30,-440,60,10,'#1a0c08');rect(c,x-30,-325,60,10,'#1a0c08')
def map_(c,t,cx,cy,z,regions=True,dim=0):
    R=[('关 中',(107.6,33.6),1),('河 北',(116,37.6),1),('江 南',(118.2,30.2),1),('中 原',(114.5,33.8),1)] if regions else []
    return G.basemap(c,cx,cy,z,t,regions=R,dim=dim)
def snow(c,t,n=120,a=.8,seed=3,rev=False):
    r=random.Random(seed)
    for i in range(n):
        x=r.uniform(0,W);sp=r.uniform(40,120);y=(r.uniform(0,H)+(-1 if rev else 1)*t*sp)%H
        circ(c,x+math.sin(t+i)*20,y,r.uniform(1.5,4),'#f3f0ea',a*r.uniform(.4,1))
def xmark(c,t,t0,x,y,r=70):
    k=cl((t-t0)/.25)
    if k<=0:return
    col(c,'#e0402e');c.set_line_width(r*.22);c.set_line_cap(1)
    c.move_to(x-r,y-r);c.line_to(x-r+2*r*min(1,k*2),y-r+2*r*min(1,k*2));c.stroke()
    if k>.5:kk=(k-.5)*2;c.move_to(x+r,y-r);c.line_to(x+r-2*r*kk,y-r+2*r*kk);c.stroke()

def fc(cam,F=300,lim=880):
    cx,cy,z=cam;return (cx,max(cy,F-(lim-540)/z),z)

def sheep(c,x,y,s=1,t=0,a=1,dead=False):
    if dead:ell(c,x,y+6*s,22*s,9*s,'#d8d0c0',a);circ(c,x+20*s,y+6*s,6*s,'#3a3030',a);return
    b=math.sin(t*6+x)*2*s
    for lx in(-12,-4,6,13):line(c,x+lx*s,y,x+lx*s,y+14*s,'#2a2020',3*s,a)
    ell(c,x,y-4*s+b*.3,20*s,12*s,'#e8e0d0',a);circ(c,x+19*s,y-9*s,6*s,'#3a3030',a)
def ingot(c,x,y,s=1,a=1):
    poly(c,[(x-22*s,y),(x+22*s,y),(x+30*s,y-14*s),(x+12*s,y-8*s),(x-12*s,y-8*s),(x-30*s,y-14*s)],'#e8b840',a,'#6a4a10',2*s,a)
    ell(c,x,y-10*s,11*s,7*s,'#ffd870',a)
def dunes(c,y,colr='#8a6a3a',colr2='#5a4024',seed=1):
    r=random.Random(seed)
    for k in range(3):
        pts=[(-2600,y+k*80+300)]
        for i in range(14):pts.append((-2600+i*400,y+k*80+r.uniform(-60,20)))
        pts.append((2600,y+k*80+300))
        poly(c,pts,[colr,'#7a5a30',colr2][k])
def label(c,t,t0,s,x,y,size=44,colr=None):
    k=pop(t,t0)
    if k<=0:return
    c.save();c.translate(x,y);c.scale(k,k)
    c.select_font_face(clib.FONTH,0,1);c.set_font_size(size);w=c.text_extents(s)[4]
    rect(c,-w/2-24,-size*.85,w+48,size*1.35,'#1e140e',.88);col(c,GOLD,.7);c.set_line_width(2.5);c.rectangle(-w/2-24,-size*.85,w+48,size*1.35);c.stroke()
    clib.htext(c,s,0,size*.32,size,colr or clib.IVORY);c.restore()

def chariot(c,x,y,s=1,d=1,t=0,colr='#5a3a1a',rider='jsol',tiger=False,brush=False,a=1):
    c.save();c.translate(x,y);c.scale(d*s,s)
    if brush:
        for i in range(5):line(c,-120,-10,-260-i*20,10+i*8,'#5a4a2a',4,a)
    for k in (0,1):horse(c,90+k*30,0,110,1,t,gallop=.6,col_='#8a5a2a' if not tiger else '#d8a040')
    if tiger:
        for k in (0,1):
            for j in range(4):line(c,60+k*30+j*16,-70,66+k*30+j*16,-40,'#1a1008',5,a)
    line(c,-20,-30,60,-50,'#3a2410',6,a)
    rect(c,-90,-80,90,50,colr,a);circ(c,-45,-20,32,'#2a1a10',a);circ(c,-45,-20,26,colr,a)
    for k in range(6):ang=k*math.pi/3+t*8;line(c,-45,-20,-45+math.cos(ang)*26,-20+math.sin(ang)*26,'#2a1a10',3,a)
    c.restore()
    person(c,x-35*d*s,y-60*s,150*s,rider,pose='hold',t=t,face=d)
