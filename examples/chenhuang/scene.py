from lib import *
from contextlib import contextmanager
@contextmanager
def layer(c,cam,p=1.0):
    cx,cy,z=cam
    c.save();c.translate(W/2,H/2);zz=1+(z-1)*p if p<=1 else z*(1+(p-1)*.5);c.scale(zz,zz);c.translate(-cx*p,-cy*p)
    try:yield zz
    finally:c.restore()
def shake(c,t,t0,amp=18,dur=.45):
    k=t-t0
    if 0<=k<dur:
        e=(1-k/dur)**2*amp;c.translate(math.sin(k*90)*e,math.cos(k*77)*e*.7)
def sky(c,top,bot,y0=-700,y1=300,x0=-2400,x1=2400):
    c.set_source(lgrad(c,0,y0,0,y1,[(0,top,1),(1,bot,1)]));c.rectangle(x0,y0-2000,x1-x0,y1-y0+4000);c.fill()
def clouds(c,t,colr,a=.5,n=10,seed=1,y=(-500,-150),spd=8,xr=(-2400,2400),sc=1.0):
    r=random.Random(seed)
    for i in range(n):
        x=r.uniform(*xr)+t*spd*r.uniform(.6,1.4);yy=r.uniform(*y);w=r.uniform(180,420)*sc
        for k in range(5):
            ell(c,x+(k-2)*w*.28,yy+r.uniform(-12,12)*sc-abs(k-2)*-6*sc,w*r.uniform(.22,.34),w*r.uniform(.07,.11),colr,a*r.uniform(.6,1))
def tri_mts(c,cx,base,n,seed,sz=60,spread=900,light='#8a6a3e',dark='#4a3822',a=1):
    r=random.Random(seed);ms=[]
    for i in range(n):ms.append((cx+r.gauss(0,spread*.5),base+r.uniform(-sz*.6,sz*.4),r.uniform(.6,1.4)))
    ms.sort(key=lambda m:m[1])
    for x,y,s in ms:
        hh=sz*1.25*s;ww=sz*.95*s
        poly(c,[(x-ww,y),(x,y-hh),(x,y)],light,a);poly(c,[(x,y-hh),(x+ww,y),(x,y)],dark,a)
def ridge(c,y,colr,amp=60,seed=1,x0=-2600,x1=2600,step=40,a=1,bottom=2000,f=(.003,.011)):
    r=random.Random(seed);ph=[r.uniform(0,6) for _ in range(3)]
    c.move_to(x0,bottom)
    x=x0
    while x<=x1:
        yy=y-amp*(.6*math.sin(x*f[0]+ph[0])+.3*math.sin(x*f[1]+ph[1])+.15*abs(math.sin(x*.031+ph[2])))
        c.line_to(x,yy);x+=step
    c.line_to(x1,bottom);c.close_path();col(c,colr,a);c.fill()
def peaks(c,y,colr,colr2,n=8,seed=2,hmin=200,hmax=420,x0=-2400,x1=2400,a=1):
    r=random.Random(seed)
    for i in range(n):
        x=lerp(x0,x1,(i+r.uniform(-.3,.3))/n);hh=r.uniform(hmin,hmax);ww=hh*r.uniform(1.1,1.6)
        sx=x+r.uniform(-.2,.2)*ww
        pts=[(x-ww,y),(x-ww*.6,y-hh*.45),(x-ww*.45,y-hh*.5),(sx-ww*.12,y-hh*.9),(sx,y-hh),(sx+ww*.1,y-hh*.88),(x+ww*.35,y-hh*.55),(x+ww*.5,y-hh*.6),(x+ww,y)]
        poly(c,pts,colr,a)
        poly(c,[(sx,y-hh),(sx+ww*.1,y-hh*.88),(x+ww*.35,y-hh*.55),(x+ww*.5,y-hh*.6),(x+ww,y),(sx+ww*.05,y),(sx-ww*.05,y-hh*.5)],colr2,a)
        # snow/ridge lines
        line(c,sx,y-hh,sx-ww*.05,y-hh*.5,colr2,2,a*.6)
def tree(c,x,y,s=1.0,colr='#2e3a2a',trunk='#2a1c12',kind='round',a=1,t=0,seed=0):
    sw=math.sin(t*1.3+x*.01)*3*s
    if kind=='dead':
        col(c,trunk,a);c.set_line_width(7*s);c.set_line_cap(1);c.move_to(x,y);c.line_to(x+sw,y-120*s);c.stroke()
        for k,(dx,dy) in enumerate([(-40,-170),(35,-160),(-20,-190),(50,-120),(-55,-110)]):
            c.set_line_width(3.2*s);c.move_to(x+sw*.6,y-(80+k*12)*s);c.line_to(x+dx*s+sw,y+dy*s);c.stroke()
        return
    col(c,trunk,a);c.set_line_width(8*s);c.move_to(x,y);c.line_to(x+sw*.3,y-70*s);c.stroke()
    if kind=='willow':
        ell(c,x+sw,y-120*s,55*s,50*s,colr,a)
        col(c,colr,a);c.set_line_width(2*s)
        for k in range(-5,6):
            c.move_to(x+k*9*s+sw,y-120*s);c.curve_to(x+k*12*s+sw*2,y-80*s,x+k*13*s+sw*3,y-50*s,x+k*14*s+sw*3.5,y-30*s);c.stroke()
    elif kind=='pine':
        for k in range(4):
            yy=y-(60+k*36)*s;ww=(60-k*12)*s
            poly(c,[(x-ww+sw,yy),(x+ww+sw,yy),(x+sw*1.4,yy-46*s)],colr,a)
    else:
        r=random.Random(seed+int(x))
        for k in range(5):
            ell(c,x+sw+r.uniform(-30,30)*s,y-r.uniform(95,150)*s,r.uniform(30,46)*s,r.uniform(24,36)*s,colr,a)
def house(c,x,y,w=220,h=110,wall='#5a4a3a',roof='#2a2420',door=True,a=1,lit=0,burn=0):
    rect(c,x-w/2,y-h,w,h,wall,a)
    for k in range(int(w//44)):rect(c,x-w/2+8+k*44,y-h,4,h,'#3a2c20',a*.6)
    if door:rect(c,x-16,y-62,32,62,'#1a120c',a)
    if lit:rect(c,x+w*.22-14,y-h*.7,28,24,'#ffb04a',lit*a);glow(c,x+w*.22,y-h*.6,60,'#ffb04a',.25*lit*a)
    rw=w*.62+28
    path(c,[(x-rw,y-h+6),(x-rw*.8,y-h-8),(x-w*.35,y-h-48),(x+w*.35,y-h-48),(x+rw*.8,y-h-8),(x+rw,y-h+6)]);col(c,roof,a);c.fill()
    line(c,x-w*.36,y-h-48,x+w*.36,y-h-48,'#15100c',5,a)
    if burn:glow(c,x,y-h-30,w*.8,'#ff6a20',.35*burn*a)
def tent(c,x,y,s=1,colr='#4a4434',a=1,lit=0):
    poly(c,[(x-70*s,y),(x,y-75*s),(x+70*s,y)],colr,a,INK,1.5,a)
    poly(c,[(x-14*s,y),(x,y-48*s),(x+14*s,y)],'#ffae4a' if lit else '#1a140e',a*(.8 if lit else 1))
    if lit:glow(c,x,y-20*s,90*s,'#ffa040',.25*a)
def reeds(c,x0,x1,y,t,colr='#3a3a24',n=60,seed=3,hh=70,a=1):
    r=random.Random(seed);col(c,colr,a);c.set_line_width(2);c.set_line_cap(1)
    for i in range(n):
        x=r.uniform(x0,x1);h=r.uniform(.5,1.2)*hh;sw=math.sin(t*2+i)*6+8
        c.move_to(x,y);c.curve_to(x,y-h*.5,x+sw*.5,y-h*.8,x+sw,y-h);c.stroke()
def rain(c,t,dens=380,ang=.22,ln=46,a=.45,seed=5,colr='#c8d4e0',spd=1500,area=(-1100,-650,2200,1300),lw=1.6):
    r=random.Random(seed);x0,y0,w,h=area;col(c,colr,a);c.set_line_width(lw)
    dx=math.sin(ang)*ln;dy=math.cos(ang)*ln
    for i in range(dens):
        x=r.uniform(0,w);ph=r.uniform(0,h);v=spd*r.uniform(.8,1.2)
        yy=(ph+t*v)%h;xx=(x+yy*math.tan(ang))%w
        c.move_to(x0+xx,y0+yy);c.line_to(x0+xx-dx,y0+yy-dy)
    c.stroke()
def splashes(c,t,y0,y1,n=60,seed=8,a=.5):
    r=random.Random(seed)
    for i in range(n):
        x=r.uniform(-1300,1300);y=r.uniform(y0,y1);ph=(t*2.5+r.random())%1
        col(c,'#c8d4e0',a*(1-ph));c.set_line_width(1.2);c.save();c.translate(x,y);c.scale(1,.3);c.arc(0,0,4+ph*16,0,6.3);c.restore();c.stroke()
def lightning(c,t,t0,x,y0=-700,y1=-50,seed=1,a=1):
    k=t-t0
    if not(0<=k<.35):return 0
    fl=(1 if k<.06 or .12<k<.18 else .35)*(1-k/.35)
    r=random.Random(seed);pts=[(x,y0)];yy=y0;xx=x
    while yy<y1:yy+=r.uniform(30,70);xx+=r.uniform(-40,40);pts.append((xx,yy))
    col(c,'#ffffff',fl*a);c.set_line_width(4);path(c,pts,False);c.stroke()
    col(c,'#aac4ff',fl*.5*a);c.set_line_width(14);path(c,pts,False);c.stroke()
    return fl
def flash(c,amt,colr='#e8eeff'):
    if amt>0:c.save();c.identity_matrix();col(c,colr,amt);c.paint();c.restore()
def fire(c,x,y,s,t,seed=0,a=1):
    r=random.Random(seed)
    glow(c,x,y-30*s,140*s,'#ff7a20',.35*a)
    for k in range(7):
        ph=t*6+k*1.7+seed
        hh=(60+30*math.sin(ph))*s*r.uniform(.7,1.2);ww=(16+6*math.sin(ph*1.3))*s;ox=(k-3)*9*s+math.sin(ph*.7)*4*s
        poly(c,[(x+ox-ww,y),(x+ox+math.sin(ph)*8*s,y-hh),(x+ox+ww,y)],['#ff5a1a','#ff8a2a','#ffc04a'][k%3],a*.85)
    poly(c,[(x-10*s,y),(x+math.sin(t*7)*4*s,y-40*s),(x+10*s,y)],'#fff0a0',a*.8)
def embers(c,t,n=60,seed=4,area=(-1000,-600,2000,1200),a=.9,colr='#ffb04a',spd=120):
    r=random.Random(seed);x0,y0,w,h=area
    for i in range(n):
        x=r.uniform(0,w);ph=r.uniform(0,h);yy=(ph-t*spd*r.uniform(.5,1.5))%h
        xx=x+math.sin(t*2+i)*30
        circ(c,x0+xx,y0+yy,r.uniform(1.2,3.2),colr,a*r.uniform(.4,1))
def smoke(c,t,x,y,s=1,n=8,seed=2,colr='#1a1410',a=.6,rise=60):
    r=random.Random(seed)
    for i in range(n):
        ph=(t*.25+i/n)%1
        xx=x+r.uniform(-40,40)*s+ph*80*s*r.uniform(.3,1);yy=y-ph*rise*6*s
        ell(c,xx,yy,(40+ph*120)*s,(30+ph*80)*s,colr,a*(1-ph)*.9)
def dust(c,t,x0,x1,y,n=30,seed=3,colr='#8a7050',a=.35,s=1):
    r=random.Random(seed)
    for i in range(n):
        x=r.uniform(x0,x1)+t*r.uniform(-30,30);ph=(t*.5+r.random())%1
        ell(c,x,y-ph*60*s,(40+ph*90)*s,(18+ph*30)*s,colr,a*(1-ph))
def arrows(c,t,t0,n=80,seed=6,src=(-1200,-200),dst=(800,300),spread=500,a=1,dur=1.4):
    r=random.Random(seed)
    for i in range(n):
        st=t0+r.uniform(0,dur*.6);k=(t-st)/dur
        if not(0<k<1):continue
        sx=src[0]+r.uniform(-spread,spread)*.4;sy=src[1]+r.uniform(-spread,spread)*.3
        ex=dst[0]+r.uniform(-spread,spread);ey=dst[1]+r.uniform(-spread*.3,spread*.3)
        x=lerp(sx,ex,k);y=lerp(sy,ey,k)-math.sin(k*math.pi)*260
        x2=lerp(sx,ex,k-.03);y2=lerp(sy,ey,k-.03)-math.sin((k-.03)*math.pi)*260
        line(c,x2,y2,x,y,'#1a1410',2,a)
def petals(c,t,n=60,colr='#efe2c4',a=.7,seed=1,area=(-1000,-600,2000,1200),spd=(40,110),size=(2,4.5)):
    r=random.Random(seed);x0,y0,w,h=area
    for i in range(n):
        x=r.uniform(0,w);sp=r.uniform(*spd);ph=r.uniform(0,h)
        y=(ph+t*sp)%h;xx=(x+math.sin(t*1.2+i)*30-t*15)%w
        circ(c,x0+xx,y0+y,r.uniform(*size),colr,a)
def banner(c,x,y,h,t,txt='',colr=RED,a=1,s=1,tc='#efe2c4',seed=0):
    line(c,x,y,x,y-h,'#2a1c10',3*s,a)
    wv=math.sin(t*4+seed)*6*s
    pts=[(x,y-h)]
    for k in range(6):pts.append((x+k*14*s,y-h+math.sin(t*5+k*.8+seed)*4*s))
    pts+= [(x+70*s,y-h+60*s+wv),(x,y-h+56*s)]
    poly(c,[(x,y-h),(x+70*s,y-h+wv*.5),(x+70*s,y-h+58*s+wv),(x,y-h+56*s)],colr,a,INK,1.2,a)
    if txt:text(c,txt,x+35*s,y-h+40*s+wv*.6,34*s,tc,a)
def citywall(c,x0,x1,ytop,ybot,colr='#4e4842',brick='#36312c',a=1):
    rect(c,x0,ytop,x1-x0,ybot-ytop,colr,a)
    col(c,brick,a*.8);c.set_line_width(1.4)
    rr=0;yy=ytop
    while yy<ybot:
        c.move_to(x0,yy);c.line_to(x1,yy)
        off=30 if rr%2 else 0;x=x0+off
        while x<x1:c.move_to(x,yy);c.line_to(x,yy+20);x+=60
        yy+=20;rr+=1
    c.stroke()
    x=x0
    while x<x1:rect(c,x,ytop-24,30,26,colr,a);x+=48
def gatetower(c,cx,ytop,ybot,s=1,roof='#1c1816',pillar='#7a1f1a',name='',a=1,gate_open=0,broken=0):
    rect(c,cx-220*s,ytop-30*s,440*s,ybot-ytop+30*s,'#58524b',a)
    c.arc(cx,ybot-120*s,80*s,math.pi,2*math.pi);c.line_to(cx+80*s,ybot);c.line_to(cx-80*s,ybot);col(c,'#0a0807',a);c.fill()
    if gate_open<1:
        ww=80*s*(1-gate_open)
        rect(c,cx-80*s,ybot-200*s,ww,200*s,'#4a2a18',a);rect(c,cx+80*s-ww,ybot-200*s,ww,200*s,'#4a2a18',a)
        for k in range(4):circ(c,cx-40*s,ybot-170*s+k*40*s,3*s,GOLD,a*(1-gate_open));circ(c,cx+40*s,ybot-170*s+k*40*s,3*s,GOLD,a*(1-gate_open))
    yb=ytop-30*s
    rect(c,cx-180*s,yb-110*s,360*s,110*s,pillar,a)
    for k in range(-3,4):rect(c,cx+k*50*s-6*s,yb-110*s,12*s,110*s,'#b8332a',a)
    for k in range(-3,3):rect(c,cx+k*50*s+10*s,yb-90*s,28*s,60*s,'#3a120e',a)
    poly(c,[(cx-270*s,yb-100*s),(cx+270*s,yb-100*s),(cx+190*s,yb-160*s),(cx-190*s,yb-160*s)],roof,a)
    poly(c,[(cx-290*s,yb-96*s),(cx-260*s,yb-112*s),(cx-250*s,yb-100*s)],roof,a);poly(c,[(cx+290*s,yb-96*s),(cx+260*s,yb-112*s),(cx+250*s,yb-100*s)],roof,a)
    poly(c,[(cx-160*s,yb-160*s),(cx+160*s,yb-160*s),(cx+120*s,yb-215*s),(cx-120*s,yb-215*s)],roof,a)
    if name:
        rect(c,cx-26*s,ybot-300*s,52*s,84*s,'#1a120c',a);rect(c,cx-22*s,ybot-296*s,44*s,76*s,'#d9b56a',a*.9)
        vtext(c,name,cx,ybot-262*s,24*s,'#1a120c',a)
def ground(c,y,top,bot,x0=-2600,x1=2600,depth=1600):
    c.set_source(lgrad(c,0,y,0,y+depth*.6,[(0,top,1),(1,bot,1)]));c.rectangle(x0,y,x1-x0,depth);c.fill()
