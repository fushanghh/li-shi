# 民国战争道具：火车、飞机、大炮、机枪、兵舰、电报、银元、时代封面、寿联、四照堂、延庆楼、吴佩孚半身像
from clib import *
from scene3 import fire,smoke,glow as _g
INK='#120c08'
def train(c,x,y,s,t,n=4,face=1,spd=1.0,txt='',lit=1,steam=True,colr='#2a2a2e'):
    c.save();c.translate(x,y);c.scale(face*s,s)
    # cars behind (negative x)
    for i in range(n):
        cx=-260-i*250
        rect(c,cx-110,-150,220,120,'#3a3026' if i%2 else '#34302a');rect(c,cx-118,-160,236,14,'#1a1612')
        for k in range(4):
            rect(c,cx-95+k*50,-130,30,34,'#ffc060' if lit else '#1a1612',.75 if lit else 1)
        for wx in(-70,70):
            circ(c,cx+wx,-22,22,'#141210');circ(c,cx+wx,-22,9,'#5a5048')
        rect(c,cx-115,-34,230,8,'#1a1612')
        line(c,cx+110,-40,cx+140,-40,'#141210',6)
    # loco
    rect(c,-120,-170,120,140,colr);rect(c,-128,-182,136,16,'#141210')
    rect(c,-100,-150,36,40,'#ffc060' if lit else '#1a1612',.8)
    rect(c,0,-140,190,96,colr);c.new_sub_path();c.arc(190,-92,48,-math.pi/2,math.pi/2);col(c,colr);c.fill()
    for k in range(4):line(c,20+k*45,-140,20+k*45,-44,'#4a4a50',2)
    rect(c,140,-196,30,58,'#1a1a1e');rect(c,132,-204,46,12,'#141210')
    rect(c,60,-160,40,22,'#3a3a40');circ(c,232,-92,12,'#ffe8a0');glow(c,232,-92,90,'#ffe0a0',.45)
    poly(c,[(240,-30),(290,0),(240,0)],'#2a2a2e')
    ph=t*8*spd
    for i,wx in enumerate((-60,40,130,200)):
        r=34 if i in(1,2) else 24
        circ(c,wx,-r,r,'#141210');circ(c,wx,-r,r*.35,'#7a7068')
        for k in range(6):an=k*math.pi/3+ph;line(c,wx,-r,wx+math.cos(an)*r*.85,-r+math.sin(an)*r*.85,'#4a4440',2.5)
    line(c,40+math.cos(ph)*16,-34+math.sin(ph)*16,130+math.cos(ph)*16,-34+math.sin(ph)*16,'#b0a898',5)
    if txt:text(c,txt,-60,-56,34,'#d9b56a')
    c.restore()
    if steam:
        r=random.Random(3)
        for i in range(10):
            u=(t*.9*spd+i/10)%1
            sx=x+face*(155-u*480)*s;sy=y-200*s-u*180*s
            ell(c,sx,sy,(26+u*80)*s,(20+u*50)*s,'#d8d4cc',(1-u)*.55)
def rails(c,y,x0=-3000,x1=3000,t=0,spd=0):
    rect(c,x0,y,x1-x0,10,'#3a3228');rect(c,x0,y+14,x1-x0,6,'#6a6458')
    off=(t*spd)%60
    for x in range(int(x0),int(x1),60):rect(c,x-off,y+8,30,16,'#2a2018')
def biplane(c,x,y,s,t,face=1,colr='#6a5a3a',a=1):
    c.save();c.translate(x,y+math.sin(t*2+x)*6*s);c.scale(face*s,s)
    rect(c,-90,-6,40,4,'#2a2018',a)
    poly(c,[(-110,-8),(60,-14),(80,-4),(60,6),(-100,2)],colr,a,INK,2,a)
    poly(c,[(-110,-8),(-120,-34),(-96,-30),(-90,-6)],colr,a,INK,1.5,a)
    rect(c,-50,-46,90,8,'#4a3e28',a);rect(c,-50,12,90,8,'#4a3e28',a)
    line(c,-40,-40,-40,14,'#1a1410',2,a);line(c,30,-40,30,14,'#1a1410',2,a)
    circ(c,0,-42,9,'#c0392b',a);circ(c,0,-42,4,'#f3e6c8',a)
    k=abs(math.sin(t*60));ell(c,84,-4,5,30*k+4,'#d8d0c0',.5*a)
    for wx in(-10,30):circ(c,wx,30,8,'#141210',a)
    line(c,-10,22,-10,6,'#1a1410',2,a);line(c,30,22,30,6,'#1a1410',2,a)
    c.restore()
def bomb(c,x,y,s=1):
    ell(c,x,y,6*s,12*s,'#1a1410');poly(c,[(x-6*s,y-12*s),(x+6*s,y-12*s),(x,y-20*s)],'#3a3028')
def explosion(c,x,y,s,t,t0,dur=1.2,seed=0):
    k=(t-t0)/dur
    if not(0<=k<1):return
    r=random.Random(seed)
    glow(c,x,y-40*s,(160+300*k)*s,'#ffb040',.9*(1-k))
    for i in range(9):
        an=r.uniform(-math.pi,0);d=(40+220*eo(k))*s*r.uniform(.5,1.1)
        ell(c,x+math.cos(an)*d*.7,y-40*s+math.sin(an)*d*.8-k*60*s,(50+90*k)*s*r.uniform(.6,1),(40+70*k)*s*r.uniform(.6,1),['#ff7a20','#ffb84a','#3a2a20','#2a1e18'][min(3,int(k*4+r.random()))],(1-k)*.9)
    for i in range(14):
        an=r.uniform(-math.pi*.95,-math.pi*.05);v=r.uniform(200,520)*s
        px=x+math.cos(an)*v*k;py=y+math.sin(an)*v*k+500*s*k*k
        rect(c,px,py,5*s,5*s,'#1a1410',1-k)
    if k<.12:flashc=(1-k/.12);circ(c,x,y-30*s,90*s,'#fff6d0',flashc)
def cannon(c,x,y,s,t,face=1,fires=(),colr='#3a3a34',elev=-.28):
    rc=0;mf=0
    for ft in fires:
        u=t-ft
        if 0<=u<.5:rc=max(rc,(1-u/.5)**2);mf=max(mf,1-u/.18 if u<.18 else 0)
    c.save();c.translate(x,y);c.scale(face*s,s)
    poly(c,[(-150,0),(-140,-8),(0,-50),(10,-40),(-130,6)],'#3a2a1a',1,INK,2)
    c.save();c.translate(-10-rc*26,-62);c.rotate(elev)
    rect(c,-30,-12,190,24,colr);rect(c,150,-14,14,28,'#2a2a26');rect(c,-40,-16,50,32,'#2a2a26')
    if mf>0:
        glow(c,200,0,200,'#ffc060',mf);poly(c,[(165,-20),(320,-50*mf),(260,0),(330,40*mf),(165,20)],'#fff0b0',mf)
    c.restore()
    rect(c,-40,-90,70,60,'#4a4a42',1);rect(c,-36,-86,62,52,'#3a3a34')
    circ(c,0,-40,40,'#1a1612');circ(c,0,-40,32,'#4a3a26')
    for k in range(10):an=k*math.pi/5;line(c,0,-40,math.cos(an)*32,-40+math.sin(an)*32,'#1a1612',3)
    circ(c,0,-40,8,'#1a1612')
    c.restore()
    if mf>0:smoke(c,t*3,x+face*180*s,y-130*s,s*1.2,5,colr='#8a8070',a=.35)
def mg(c,x,y,s,t,face=1,firing=True):
    c.save();c.translate(x,y);c.scale(face*s,s)
    line(c,-20,0,10,-40,'#1a1410',5);line(c,40,0,10,-40,'#1a1410',5);line(c,10,0,10,-40,'#1a1410',5)
    rect(c,-20,-62,80,26,'#3a3a32');rect(c,60,-54,60,8,'#2a2a26');rect(c,-30,-58,14,18,'#2a2a26')
    poly(c,[(40,-90),(54,-90),(54,-20),(40,-20)],'#4a4a40',1,INK,1.5)
    if firing and int(t*22)%2==0:
        glow(c,130,-50,80,'#ffd070',.9);poly(c,[(120,-58),(170,-50),(120,-42)],'#fff0b0')
    c.restore()
def sandbags(c,x0,x1,y,rows=3,colr='#6a5a3e'):
    for r_ in range(rows):
        yy=y-r_*22;off=(r_%2)*30
        x=x0+off
        while x<x1:ell(c,x,yy,32,13,colr,1);col(c,INK,.5);c.set_line_width(1.5);c.save();c.translate(x,yy);c.scale(32,13);c.arc(0,0,1,0,7);c.restore();c.stroke();x+=60
def gunboat(c,x,y,s,t,face=1,flag='#c0392b',lit=1,smk=True,colr='#3a3e44'):
    bob=math.sin(t*1.4)*5*s
    c.save();c.translate(x,y+bob);c.scale(face*s,s);c.rotate(math.sin(t*1.1)*.01)
    poly(c,[(-420,-40),(380,-40),(470,-70),(440,30),(-380,40),(-430,0)],colr,1,INK,3)
    rect(c,-400,0,820,6,'#7a1f1a')
    for k in range(10):circ(c,-330+k*70,-14,7,'#ffd080' if lit and k%3 else '#1a1a1e',.85)
    rect(c,-200,-110,300,70,'#4a4e54');rect(c,-170,-170,180,60,'#555a60')
    for k in range(5):rect(c,-160+k*34,-155,20,18,'#ffd080' if lit else '#1a1a1e',.8)
    rect(c,30,-250,46,140,'#2a2a2e');rect(c,26,-258,54,12,'#1a1a1e')
    line(c,-60,-170,-60,-330,'#2a2a2e',5);line(c,-140,-300,20,-300,'#2a2a2e',3)
    line(c,-60,-330,400,-70,'#2a2a2e',1.5);line(c,-60,-330,-420,-40,'#2a2a2e',1.5)
    rect(c,200,-70,90,30,'#4a4e54');rect(c,280,-62,110,10,'#2a2a2e')
    rect(c,-330,-70,90,30,'#4a4e54');rect(c,-420,-62,100,10,'#2a2a2e')
    wv=math.sin(t*5)*6
    poly(c,[(-60,-330),(-10,-322+wv),(-10,-292+wv),(-60,-298)],flag,1,INK,1.5)
    c.restore()
    if smk:
        for i in range(9):
            u=(t*.35+i/9)%1;sx=x+face*(53*s-u*500*s);sy=y+bob-260*s-u*220*s
            ell(c,sx,sy,(30+u*120)*s,(24+u*70)*s,'#1c1a1a',(1-u)*.6)
def sea(c,t,y,x0=-3000,x1=3000,colr='#14262e',colr2='#1e3a44',a=1):
    rect(c,x0,y,x1-x0,1400,colr,a)
    for k in range(14):
        yy=y+10+k*k*7
        col(c,colr2,.6*a);c.set_line_width(2+k*.4)
        c.move_to(x0,yy)
        x=x0
        while x<x1:c.line_to(x,yy+math.sin(x*.01+t*1.2+k)*4*(1+k*.2));x+=60
        c.stroke()
    r=random.Random(5)
    for i in range(70):
        xx=r.uniform(x0,x1);yy=y+r.uniform(5,500);ph=(t*.6+r.random())%1
        line(c,xx+ph*30,yy,xx+ph*30+r.uniform(20,60),yy,'#9cc0c8',.35*a*math.sin(ph*math.pi),2)
def pier(c,x,y,w=900):
    rect(c,x-w,y-30,w,30,'#2a2018');
    for k in range(int(w/80)):rect(c,x-w+k*80+20,y,14,200,'#1a140e')
def telepole(c,x,y,h=420,a=1):
    line(c,x,y,x,y-h,'#1e1610',8,a);line(c,x-50,y-h+30,x+50,y-h+30,'#1e1610',5,a);line(c,x-40,y-h+70,x+40,y-h+70,'#1e1610',5,a)
    for dx in(-44,-14,14,44):circ(c,x+dx,y-h+24,4,'#c8c0b0',a)
def wires(c,x0,x1,yt,sag=40,a=1,n=4):
    for k in range(n):
        y=yt+k*12;col(c,'#120c08',a*.8);c.set_line_width(1.6);c.move_to(x0,y);c.curve_to(x0+(x1-x0)*.33,y+sag,x0+(x1-x0)*.66,y+sag,x1,y);c.stroke()
def telekey(c,x,y,s,t,press=0):
    c.save();c.translate(x,y);c.scale(s,s)
    rect(c,-160,-20,320,40,'#4a3020');rect(c,-150,-30,300,12,'#5a3a26')
    c.save();c.translate(-90,-40);c.rotate(-.08+press*.08);rect(c,0,-8,190,14,'#b08a3a');c.restore()
    circ(c,96,-52+press*10,22,'#1a1410');circ(c,96,-52+press*10,14,'#3a2a20')
    for k in range(2):circ(c,-120+k*30,-30,8,'#d9b56a')
    c.restore()
def morse_tape(c,x,y,w,t,spd=200,a=1,seed=1):
    rect(c,x,y-16,w,32,'#e8dcbc',a)
    r=random.Random(seed);xx=x-(t*spd)%400
    while xx<x+w:
        L=r.choice([10,10,30]);
        if xx>x and xx+L<x+w:rect(c,xx,y-4,L,8,'#1a120c',a)
        xx+=L+r.choice([10,10,24])
def yuan(c,x,y,s=1,a=1,tilt=.35):
    c.save();c.translate(x,y);c.scale(s,s*tilt)
    circ(c,0,4/tilt*0+6,30,'#6a6a6a',a);circ(c,0,0,30,'#d8d8d8',a);circ(c,0,0,24,'#bdbdbd',a)
    c.restore()
def coinstack(c,x,y,n,s=1,a=1):
    for k in range(n):yuan(c,x,y-k*7*s,s,a)
def notes(c,x,y,s=1,a=1,txt='伍千元',rot=0):
    c.save();c.translate(x,y);c.rotate(rot);c.scale(s,s)
    rect(c,-90,-44,180,88,'#e8dcbc',a);col(c,'#2f5a3a',a);c.set_line_width(3);c.rectangle(-82,-36,164,72);c.stroke()
    text(c,txt,0,12,28,'#2f5a3a',a);text(c,'支 票',-50,-14,16,'#7a1f1a',a)
    c.restore()
def wu_bust(c,x,y,s,t=0,eyes='open',look=0,cap=False,light=1.0,coat='#4e5f73',a=1):
    """半身像：x,y=胸口底部中心"""
    c.save();c.translate(x,y);c.scale(s,s)
    # shoulders / coat
    poly(c,[(-300,0),(-270,-200),(-150,-260),(150,-260),(270,-200),(300,0)],coat,a,INK,4,a)
    poly(c,[(-60,-260),(60,-260),(40,0),(-40,0)],'#3a4858',a)
    for k in range(4):circ(c,0,-220+k*55,9,GOLD,a)
    for sx in(-1,1):
        poly(c,[(sx*150,-262),(sx*262,-205),(sx*250,-185),(sx*140,-238)],GOLD,a)
        for k in range(7):line(c,sx*(150+k*16),-235+k*7,sx*(150+k*16),-205+k*7,GOLD,2,a)
    col(c,GOLD,a);c.set_line_width(14);c.move_to(-200,-230);c.line_to(160,0);c.stroke()
    for k in range(3):rect(c,-230+k*36,-150,26,40,['#c0392b','#d9b56a','#2f5a7a'][k],a)
    # collar
    poly(c,[(-80,-300),(80,-300),(70,-250),(-70,-250)],'#c0392b',a,INK,3,a)
    rect(c,-50,-340,100,50,'#e2c39a',a)
    # head
    hx_=look*20
    c.save();c.translate(hx_,-450)
    ell(c,0,0,118,140,'#e6c49c',a);col(c,INK,a);c.set_line_width(5);c.save();c.scale(118,140);c.arc(0,0,1,0,7);c.restore();c.stroke()
    ell(c,-118,10,18,32,'#d8b08a',a);ell(c,118,10,18,32,'#d8b08a',a)
    if cap:
        poly(c,[(-130,-60),(130,-60),(150,-130),(-150,-130)],'#3e4c5c',a,INK,4,a);rect(c,-130,-78,260,22,'#c0392b',a);circ(c,0,-100,14,GOLD,a)
        poly(c,[(-120,-58),(120,-58),(100,-30),(-100,-30)],'#141210',a)
    else:
        ell(c,-30,-90,50,28,'#fff4e0',.35*light*a)
    # brows/eyes
    for sx in(-1,1):
        line(c,sx*28+hx_*.3,-22,sx*70+hx_*.3,-30,'#2a1a10',8,a)
        if eyes=='closed':line(c,sx*32+hx_*.3,6,sx*62+hx_*.3,8,'#2a1a10',5,a)
        else:circ(c,sx*47+hx_*.3,6,8,'#1a120c',a);circ(c,sx*44+hx_*.3,3,2.5,'#ffffff',a)
    line(c,hx_*.3,10,hx_*.3+6,62,'#b8906a',5,a)
    # mustache
    col(c,'#5a3a24',a);c.move_to(-56+hx_*.3,92);c.curve_to(-30,72,30,72,56+hx_*.3,92);c.curve_to(30,84,-30,84,-56+hx_*.3,92);c.fill()
    line(c,-22+hx_*.3,110,22+hx_*.3,110,'#7a4a34',4,a)
    c.restore()
    c.restore()
def time_cover(c,cx,cy,s,t,k=1):
    c.save();c.translate(cx,cy);c.scale(s,s)
    rect(c,-330,-430,660,860,'#0a0806',.5)
    rect(c,-320,-420,640,840,'#c0392b');rect(c,-296,-396,592,792,'#efe6d0')
    c.select_font_face('Noto Serif CJK SC Black',0,1);c.set_font_size(150)
    e=c.text_extents('TIME');c.move_to(-e[4]/2,-250);c.text_path('TIME');col(c,'#c0392b');c.fill()
    text(c,'THE WEEKLY NEWS-MAGAZINE',0,-216,18,'#3a2a1a')
    rect(c,-250,-196,500,470,'#cdbf9e');
    c.save();c.rectangle(-250,-196,500,470);c.clip();wu_bust(c,0,280,.92,t,coat='#4e5a66');c.restore()
    col(c,'#3a2a1a');c.set_line_width(2);c.rectangle(-250,-196,500,470);c.stroke()
    text(c,'GENERAL WU',0,325,46,'#1a120c')
    text(c,'“Biggest man in China”',0,368,30,'#3a2a1a',bold=False)
    text(c,'Vol. IV, No. 10',-250,-370,16,'#3a2a1a',align='l');text(c,'Sept. 8, 1924',250,-370,16,'#3a2a1a',align='r')
    c.restore()
def couplet(c,x,y,s,txt,k=1,a=1):
    """y=top"""
    n=len(txt);hh=(n*92+80)*k
    c.save();c.translate(x,y);c.scale(s,s)
    rect(c,-70,0,140,hh,'#a8261c',a);col(c,GOLD,a*.8);c.set_line_width(4);c.rectangle(-62,8,124,hh-16);c.stroke()
    rect(c,-80,-16,160,18,'#3a2414',a)
    for i,ch in enumerate(txt):
        if 60+i*92+40<hh:clib_vt(c,ch,0,90+i*92,76,a)
    if k<1:rect(c,-80,hh-6,160,22,'#3a2414',a)
    c.restore()
def clib_vt(c,ch,x,y,size,a):
    c.select_font_face(FONTH,0,1);c.set_font_size(size);e=c.text_extents(ch)
    c.move_to(x-e[4]/2-e[0]*0,y);c.text_path(ch);col(c,'#1a0c06',a);c.fill_preserve();col(c,'#e8c060',a);c.set_line_width(1);c.stroke()
def hall(c,cx,ybot,s=1,name='',lit=1,t=0,pillar='#7a1c16',roof='#1e1a18',w=900):
    hw=w/2
    rect(c,cx-hw-40*s,ybot-20*s,w+80*s,40*s,'#5a5048')
    rect(c,cx-hw,ybot-300*s,w,280*s,'#3a1a12')
    n=7
    for k in range(n+1):
        x=cx-hw+k*w/n;rect(c,x-12*s,ybot-300*s,24*s,282*s,pillar)
    for k in range(n):
        x=cx-hw+(k+.5)*w/n;rect(c,x-40*s,ybot-260*s,80*s,170*s,'#ffb460' if lit else '#2a1a12',.55*lit+.2)
        col(c,'#3a1a10',.9);c.set_line_width(3*s)
        for j in range(4):c.move_to(x-40*s+j*26*s,ybot-260*s);c.line_to(x-40*s+j*26*s,ybot-90*s)
        for j in range(6):c.move_to(x-40*s,ybot-260*s+j*34*s);c.line_to(x+40*s,ybot-260*s+j*34*s)
        c.stroke()
    if lit:glow(c,cx,ybot-170*s,w*.7,'#ffb050',.22*lit)
    poly(c,[(cx-hw-130*s,ybot-290*s),(cx+hw+130*s,ybot-290*s),(cx+hw+40*s,ybot-380*s),(cx-hw-40*s,ybot-380*s)],roof)
    poly(c,[(cx-hw-160*s,ybot-280*s),(cx-hw-120*s,ybot-305*s),(cx-hw-100*s,ybot-290*s)],roof);poly(c,[(cx+hw+160*s,ybot-280*s),(cx+hw+120*s,ybot-305*s),(cx+hw+100*s,ybot-290*s)],roof)
    poly(c,[(cx-hw+60*s,ybot-380*s),(cx+hw-60*s,ybot-380*s),(cx+hw-160*s,ybot-450*s),(cx-hw+160*s,ybot-450*s)],roof)
    line(c,cx-hw+150*s,ybot-450*s,cx+hw-150*s,ybot-450*s,'#141010',10*s)
    for k in range(-12,13):line(c,cx+k*w/22,ybot-292*s,cx+k*w/22*.92,ybot-378*s,'#2e2824',2*s)
    if name:
        rect(c,cx-110*s,ybot-345*s,220*s,56*s,'#1a120c');rect(c,cx-104*s,ybot-339*s,208*s,44*s,'#d9b56a',.9)
        text(c,name,cx,ybot-305*s,34*s,'#1a120c',sp=8*s)
def lantern(c,x,y,s,t,i=0,a=1):
    fl=.8+.2*math.sin(t*9+i);line(c,x,y-120*s,x,y-40*s,'#2a1c10',3*s,a)
    ell(c,x,y,32*s,44*s,'#c0392b',a);glow(c,x,y,120*s,'#ffb050',.45*fl*a)
    rect(c,x-24*s,y-48*s,48*s,8*s,'#1a0c08',a);rect(c,x-24*s,y+40*s,48*s,8*s,'#1a0c08',a)
    for k in range(5):line(c,x-10*s+k*5*s,y+48*s,x-10*s+k*5*s,y+80*s,GOLD,1.5*s,a)
def westbldg(c,cx,ybot,s=1,lit=(1,0,1,1,0,1),name=''):
    """延庆楼：两层楼"""
    w=1000*s;hw=w/2
    rect(c,cx-hw,ybot-520*s,w,520*s,'#5a4a3e')
    rect(c,cx-hw,ybot-270*s,w,18*s,'#3a2e26');rect(c,cx-hw-20*s,ybot-540*s,w+40*s,26*s,'#3a2e26')
    poly(c,[(cx-hw-40*s,ybot-530*s),(cx+hw+40*s,ybot-530*s),(cx+hw-30*s,ybot-620*s),(cx-hw+30*s,ybot-620*s)],'#22201e')
    for row in range(2):
        for k in range(6):
            x=cx-hw+90*s+k*164*s;y=ybot-(470 if row==0 else 220)*s
            on=lit[k] if row==0 else lit[5-k]*.6
            rect(c,x,y,80*s,130*s,'#ffc070' if on else '#1a1612',.85 if on else 1)
            c.new_sub_path();c.arc(x+40*s,y,40*s,math.pi,0);col(c,'#ffc070' if on else '#1a1612',.85 if on else 1);c.fill()
            if on:glow(c,x+40*s,y+60*s,160*s,'#ffb050',.18)
            line(c,x+40*s,y-40*s,x+40*s,y+130*s,'#2a1e16',3*s);line(c,x,y+60*s,x+80*s,y+60*s,'#2a1e16',3*s)
    rect(c,cx-60*s,ybot-200*s,120*s,200*s,'#1a120c')
    if name:
        rect(c,cx-110*s,ybot-262*s,220*s,50*s,'#1a120c');text(c,name,cx,ybot-226*s,32*s,GOLD,sp=8*s)
def whiteflag(c,x,y,h,t,a=1):
    line(c,x,y,x,y-h,'#2a1c10',4,a);wv=math.sin(t*5)*6
    poly(c,[(x,y-h),(x+90,y-h+wv),(x+90,y-h+60+wv),(x,y-h+56)],'#e8e4dc',a,INK,1.5,a)
def rifle_pile(c,x,y,n,s=1,seed=2):
    r=random.Random(seed)
    for i in range(n):
        xx=x+r.uniform(-200,200)*s;yy=y+r.uniform(-30,10)*s;an=r.uniform(-.5,.5)
        c.save();c.translate(xx,yy);c.rotate(an);rect(c,-90*s,-4*s,150*s,8*s,'#3a2414');rect(c,60*s,-2.5*s,50*s,5*s,'#7a7a7a');c.restore()
def searchlight(c,x,y,ang,t,L=1600,w=.12,a=.18):
    c.save();c.translate(x,y);c.rotate(ang)
    g=lgrad(c,0,0,L,0,[(0,'#f0f0e0',a),(1,'#f0f0e0',0)])
    c.move_to(0,0);c.line_to(L,-L*w);c.line_to(L,L*w);c.close_path();c.set_source(g);c.fill();c.restore()
