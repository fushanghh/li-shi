from lib import *
from fig import person,horse,sprite,blit,walk,mix,P as PP,OUT
from scene import *
import mapx as M
def stamp(c,txt,x,y,t,t0,size=96,rot=-6,colr=RED,sub=None):
    k=t-t0
    if k<0:return
    sc=lerp(2.6,1,eo(k/0.16)) if k<.16 else 1+0.02*math.sin(min(k,1)*3)
    a=cl(k/0.1)
    c.save();c.translate(x,y);c.rotate(math.radians(rot));c.scale(sc,sc)
    c.select_font_face(FONT,0,1);c.set_font_size(size);sp=size*.1
    w=sum(c.text_extents(ch)[4] for ch in txt.replace(' ',''))+sp*(len(txt)-1)
    pad=size*.3
    col(c,colr,.12*a);c.rectangle(-w/2-pad,-size*.98,w+2*pad,size*1.3);c.fill()
    col(c,colr,.92*a);c.set_line_width(size*.075);c.rectangle(-w/2-pad,-size*.98,w+2*pad,size*1.3);c.stroke()
    c.set_line_width(size*.025);c.rectangle(-w/2-pad+size*.1,-size*.98+size*.1,w+2*pad-size*.2,size*1.3-size*.2);c.stroke()
    text(c,txt,0,size*.04,size,colr,.95*a,sp=sp)
    rng=random.Random(len(txt)*7+int(size))
    for i in range(55):circ(c,rng.uniform(-w/2-pad,w/2+pad),rng.uniform(-size*.95,size*.3),rng.uniform(1,size*.035),'#1a120c',.5*a)
    if sub:text(c,sub,0,size*.62,size*.24,'#efe2c4',.9*a)
    c.restore()
def counter(c,label,num,note,t,a=1,x=70,y=150):
    a*=cl(t/0.5)
    if a<=0:return
    g=lgrad(c,0,0,620,0,[(0,'#000000',.6*a),(1,'#000000',0)]);c.set_source(g);c.rectangle(0,y-30,620,190);c.fill()
    text(c,label,x,y+12,28,GREY,a,align='l')
    text(c,num,x,y+92,76,GOLD,a,align='l',shadow=1)
    if note:text(c,note,x+2,y+134,22,'#a89878',a*.9,align='l',bold=False)
def chip(c,txt,x,y,t,t0,colr=GOLD,size=30):
    k=cl((t-t0)/.3)
    if k<=0:return
    c.save();c.translate(x,y);sc=eback(k);c.scale(sc,sc)
    c.select_font_face(FONT,0,1);c.set_font_size(size);w=c.text_extents(txt)[4]+size*1.2
    col(c,'#120c08',.8*k);c.rectangle(-w/2,-size*.95,w,size*1.45);c.fill()
    col(c,colr,k);c.set_line_width(2);c.rectangle(-w/2,-size*.95,w,size*1.45);c.stroke()
    text(c,txt,0,size*.1,size,colr,k);c.restore()
def beams(c,x,y,t,n=7,colr='#ffd27a',a=.12,ln=1600,spread=.9):
    for i in range(n):
        an=math.pi/2+(i-(n-1)/2)*spread/n+math.sin(t*.4+i)*.03
        w=.035
        c.move_to(x,y);c.line_to(x+math.cos(an-w)*ln,y+math.sin(an-w)*ln);c.line_to(x+math.cos(an+w)*ln,y+math.sin(an+w)*ln);c.close_path()
        c.set_source(lgrad(c,x,y,x,y+ln,[(0,colr,a),(1,colr,0)]));c.fill()
def vignette_red(c,a):
    if a<=0:return
    g=cairo.RadialGradient(W/2,H/2,300,W/2,H/2,1150);g.add_color_stop_rgba(0,.5,0,0,0);g.add_color_stop_rgba(1,.45,.02,.02,a)
    c.set_source(g);c.paint()
def letterbox(c,a=1,h=70):
    rect(c,0,0,W,h,'#000000',a);rect(c,0,H-h,W,h,'#000000',a)
def crowd_grid(seed,n,x0,x1,y0,y1,outs,poses,hfar=30,hnear=120,weapons=None,faces=(1,)):
    r=random.Random(seed);L=[]
    for i in range(n):
        y=r.uniform(y0,y1);k=(y-y0)/(y1-y0) if y1>y0 else 1
        h=lerp(hfar,hnear,k)
        L.append(dict(x=r.uniform(x0,x1),y=y,h=h,out=r.choice(outs),pose=r.choice(poses),w=r.choice(weapons) if weapons else None,ph=r.uniform(0,6.28),face=r.choice(faces)))
    L.sort(key=lambda d:d['y']);return L
def hb(h):
    for b in (36,70,130):
        if h<=b*1.15:return b
    return 130
def draw_crowd(c,L,t,bob=4,dx=0,a=1,march=0,flip=None):
    for d in L:
        b=hb(d['h']);sc=d['h']/b
        pose=d['pose']
        if march:
            fr=int((t*march*4+d['ph'])%4);pose=('walk',fr)
            spr=sprite(d['out'],walk(fr/4,run=march>1.5),b,d['face'] if flip is None else flip,d['w'],key=('walk',fr,march>1.5))
        else:
            spr=sprite(d['out'],pose,b,d['face'] if flip is None else flip,d['w'],expr='angry' if pose in('shout','cheer') else 'calm',mouth='open' if pose in('shout','cheer') else 'closed')
        yy=d['y']-abs(math.sin(t*5+d['ph']))*bob*sc
        blit(c,spr,d['x']+dx*(d['h']/100),yy,sc,a)
