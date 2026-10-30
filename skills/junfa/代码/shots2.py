from wscene import *
from shots1 import cm,ZJ
GM=army(31,150,-1800,1800,60,300,['gmsol'],('walk',),50,150,grid=True,cols=30)
# ================= 4 第二次直奉 1924 =================
@nx(5,'1924年9月·北京中南海','1924年9月17日，北京{中南海四照堂}',fx=[(0,'night',.7),(0,'wind',.4),(1.5,'steps',.5,2.5)])
def s33(c,t,T):
    cam=cm(t,(0,-160,.9),(0,-120,1.08),5)
    nightsky(c,cam,t,'#05070e','#1a2030',60,moon=(700,-400))
    with layer(c,cam,.4):ridge(c,-20,'#0a0c12',amp=20,seed=6)
    with layer(c,cam,.7):
        hall(c,0,40,1.0,'四照堂',lit=1,t=t)
        rect(c,-2600,40,5200,900,'#0c1620')
        c.save();c.translate(0,80);c.scale(1,-.45);c.translate(0,-40);hall(c,0,40,1.0,'',lit=.6,t=t);c.restore()
        rect(c,-2600,40,5200,900,'#0c1620',.6)
        for k in range(16):line(c,-1200+k*160+math.sin(t+k)*20,120+k*12,-1100+k*160,120+k*12,'#9cc0c8',1.5,.25)
    with layer(c,cam,1):
        for i,x in enumerate((-700,-460,460,700)):lantern(c,x,-140,1.0,t,i)
        for x in(-380,380):person(c,x,40,210,'zsol',pose='stand',t=t,face=1 if x<0 else -1)
@nx(6,'1924年9月·四照堂','吴佩孚{点将}：直军约{20万}，奉军约{15万}',fx=[(0,'crowd',.4),(.5,'tele',.5,2),(2,'pointer',.7),(3.4,'stamp',.6)])
def s34(c,t,T):
    cam=cm(t,(-120,-80,1.0),(80,-100,1.12),6)
    with layer(c,cam,.15):
        rect(c,-2000,-1000,4000,2000,'#24140e')
        c.save();c.rectangle(-560,-470,1120,560);c.clip()
        c.translate(-560,-470);c.scale(1120/W,560/H);sc=M.nmap(c,t,118.2,40.0,1.3,regions=False);M.cities(c,t,sc,['北京','山海关','古北口','奉天'],size=34,red=('奉天',));
        M.arrow(c,[(117.0,39.9),(118.5,39.8),(119.6,39.95)],ramp(t,bt(2),bt(3.5)),sc,h=GOLD,lw=8)
        G.endmap(c);c.restore()
        col(c,'#6a4a24');c.set_line_width(14);c.rectangle(-560,-470,1120,560);c.stroke()
        for x in(-800,800):rect(c,x-30,-700,60,1200,'#6a1c16')
    with layer(c,cam,1):
        rect(c,-2000,250,4000,600,'#1a0e0a')
        person(c,-420,250,430,'wpf',pose='point',t=t,face=1,talk=True)
        draw_army(c,[dict(d) for d in army(32,8,-100,1100,240,300,['zoff'],('stand','salute'),330,360,faces=(-1,))],t,bob=0)
    counter(c,t,'直军',[(bt(1.2),'约20万')])
    counter(c,t,'奉军',[(bt(2.2),'约15万')],y=360,h=RED)
@nx(5,'1924年9月·四照堂','{冯玉祥}任第三军总司令，出{古北口}',fx=[(0,'paper',.8),(2.0,'stamp',1.1),(2.05,'impact',.5)])
def s35(c,t,T):
    rect(c,0,0,W,H,'#140c08');glow(c,W/2,H/2,700,'#7a4a20',.3)
    z=seg(t,[(0,1.0),(bt(5),1.1)])
    c.save();c.translate(W*.45,H*.47);c.scale(z,z);c.translate(-W*.45,-H*.47)
    scroll_doc(c,W*.45,H*.47,820,640,['第三军总司令','冯玉祥','出古北口'],t,.1,title='讨逆军',seal=(bt(2),W*.45-250,H*.47+180,'令'))
    c.restore()
    c.save();c.translate(W*.82,H*.95);person(c,0,0,520,'feng',pose='stand',t=t,face=-1);c.restore()
@nx(5,'1924年9月·京畿','主力东去{山海关}，冯玉祥北上{古北口}',fx=[(0,'train',.7),(.4,'whistle',.6),(1.6,'steps',.5,3)])
def s36(c,t,T):
    sc=M.nmap(c,t,118.5,40.4,seg(t,[(0,1.5),(bt(5),1.75)]))
    M.cities(c,t,sc,['北京','山海关','古北口','奉天','锦州'],red=('奉天',),size=36)
    G.route(c,[(116.4,39.9),(117.2,39.13),(118.18,39.63),(119.6,39.93),(119.7,39.98)],ramp(t,.1,bt(2.5)),sc,h=GOLD,lw=8,arrow=True)
    G.route(c,[(116.4,39.9),(116.8,40.3),(117.15,40.66)],ramp(t,bt(1.2),bt(3)),sc,h='#9aa4ae',lw=7,arrow=True)
    M.arrow(c,[(123.43,41.8),(122.0,41.4),(121.13,41.1),(120.2,40.4)],ramp(t,bt(1),bt(3.6)),sc,lw=9)
    M.arrow(c,[(121.13,41.1),(119.5,41.2),(118.6,40.9)],ramp(t,bt(2),bt(4)),sc,lw=7)
    G.endmap(c)
    badge(c,t,bt(.4),W*.13,H*.3,'冯玉祥','第三军','#5c6670','冯',56)
    badge(c,t,bt(.8),W*.87,H*.3,'张作霖','奉军','#9a8048','张',56)
@nx(5,'1924年10月·山海关','奉军{飞机大炮}，猛攻山海关',fx=[(0,'plane',.9),(1.0,'bombfall',.8),(1.9,'expl',1.0),(2.6,'bombfall',.7),(3.4,'expl',1.0),(.5,'boom',.6)])
def s37(c,t,T):
    cam=cm(t,(0,-120,1.0),(0,-80,1.1),5)
    with layer(c,cam,.03):sky(c,'#14100e','#7a3a20',-900,60);clouds(c,t,'#2a1a14',.7,10,seed=8,spd=20)
    with layer(c,cam,.3):ridge(c,-10,'#2a2018',amp=80,seed=12);far_fires(c,t,0,5,s=.5,seed=4)
    with layer(c,cam,.6):
        citywall(c,-2400,2400,-60,220,'#4e4842','#36312c');gatetower(c,0,-60,220,1.0,name='天下第一关')
        explosion(c,-500,-60,1.6,t,bt(1.9),seed=7);explosion(c,420,-40,1.8,t,bt(3.4),seed=8)
    with layer(c,cam,1):
        for i in range(3):
            x=-1300+t*420+i*260;y=-380+i*60
            biplane(c,x,y,1.0-i*.15,t,1,colr='#7a6a40')
            for j in range(3):
                bt0=bt(1.0+i*.8+j*.2);u=t-bt0
                if 0<u<1:bomb(c,x-60+u*120,y+40+u*u*500,1.2)
    smoke(c,t,W*.5,H*.35,3,10,colr='#1a1210',a=.35)
@nx(4,'1924年10月·山海关',fx=[(0,'mg',.9),(0,'fire',.4),(.6,'boom',.9),(1.4,'expl',.9),(2.4,'boom',.9),(3.0,'expl',.8)])
def s38(c,t,T):
    cam=cm(t,(-100,-40,1.15),(100,-70,1.3),4)
    with layer(c,cam,.05):sky(c,'#100c0a','#5a2a18',-900,60)
    with layer(c,cam,.3):ridge(c,30,'#1e1812',amp=40,seed=3);far_fires(c,t,30,8,s=.5,seed=6)
    with layer(c,cam,1):
        ground(c,110,'#2e2418','#0a0604');sandbags(c,-1200,1200,230,3,'#5a4a32')
        mg(c,-450,190,1.3,t,1,True);mg(c,350,190,1.3,t+.3,1,True)
        draw_army(c,army(33,12,-1100,1000,180,240,['zsol'],('aim',),120,150),t,bob=0)
        cannon(c,-900,300,1.0,t,1,fires=(bt(.6),bt(2.4)))
        explosion(c,600,60,1.7,t,bt(1.4),seed=3);explosion(c,-200,40,1.3,t,bt(3.0),seed=5)
    embers(c,t,70,area=(0,0,W,H),a=.7)
@nx(5,'1924年10月8日·九门口','10月8日，奉军{突破九门口}',fx=[(0,'boom',.7),(1.2,'boom',.8),(2.4,'expl',1.0),(2.5,'stamp',1.2),(2.55,'impact',.8)])
def s39(c,t,T):
    sc=M.nmap(c,t,119.6,40.1,seg(t,[(0,4.0),(bt(5),5.0)]),regions=False)
    M.cities(c,t,sc,['九门口','山海关','秦皇岛'],red=('九门口',),pulse=('九门口',),size=32,off={'山海关':(16,24),'秦皇岛':(16,24)})
    M.arrow(c,[(120.1,40.5),(119.85,40.3),(119.62,40.15),(119.45,40.05)],ramp(t,.2,bt(2.4)),sc,lw=10)
    G.endmap(c)
    stamp(c,t,bt(2.4),'九门口失守',W*.3,H*.24,84,-.05)
@nx(5,'1924年10月11日·京奉线','10月11日，吴佩孚{亲赴山海关}督战',fx=[(0,'train',1.0),(.2,'whistle',1.0),(2.8,'whistle',.6)])
def s40(c,t,T):
    cam=cm(t,(0,-60,1.0),(120,-80,1.08),5)
    with layer(c,cam,.03):sky(c,'#0e0c10','#4a2a20',-900,60)
    with layer(c,cam,.2):ridge(c,40,'#1a1614',amp=50,seed=2)
    with layer(c,cam,.5):
        r=random.Random(3)
        for i in range(10):
            x=((r.uniform(-2400,2400)-t*300)%4800)-2400;telepole(c,x,170,320,.8)
    with layer(c,cam,1):
        ground(c,240,'#2a2218','#0a0604');rails(c,236,t=t,spd=900)
        train(c,300,240,1.0,t,4,1,spd=1.5,txt='',lit=1)
        r=random.Random(int(t*20))
        for i in range(5):circ(c,300+r.uniform(-500,200),240,3,'#ffd070')
    infocard(c,t,bt(.6),70,110,'吴佩孚','1924年10月',['乘专列离京','赴山海关前线'],w=420)
@nx(4,'1924年10月·山海关','前线，已经{吃紧}',fx=[(0,'wind',.7),(.5,'boom',.5),(2,'boom',.6),(1.5,'heart',.4,2.5)])
def s41(c,t,T):
    cam=cm(t,(0,-140,1.05),(-60,-160,1.2),4)
    with layer(c,cam,.03):sky(c,'#120e0c','#6a3420',-900,80)
    with layer(c,cam,.3):ridge(c,40,'#241c16',amp=80,seed=14);far_fires(c,t,40,6,s=.5,seed=2)
    with layer(c,cam,1):
        citywall(c,-2400,2400,140,800,'#4a443e','#34302a')
        person(c,-100,140,420,'wpfc',pose='point',t=t,face=1,cape_wind=8)
        person(c,-330,140,360,'zoff',pose='stand',t=t,face=1)
        banner(c,300,140,420,t,'直','#c0392b',1,1.4)
    smoke(c,t,W*.7,H*.25,3,9,colr='#1a1210',a=.4)
# ================= 5 高潮：北京政变 =================
@nx(5,'1924年10月·古北口','而古北口的冯玉祥，{按兵不前}',fx=[(0,'wind',1.0),(.5,'heart',.6)])
def s42(c,t,T):
    cam=cm(t,(0,-120,1.0),(0,-140,1.12),5)
    with layer(c,cam,.03):sky(c,'#0c0e14','#3a3a40',-900,80)
    with layer(c,cam,.2):peaks(c,60,'#2a2a2e','#1a1a1e',8,seed=5,hmin=250,hmax=480)
    with layer(c,cam,.45):
        peaks(c,120,'#3a3428','#2a241c',7,seed=9,hmin=180,hmax=320)
        pts=[(-2400,40),(-1400,-30),(-700,60),(0,-20),(700,50),(1500,-10),(2400,60)];
        for (x0,y0),(x1,y1) in zip(pts,pts[1:]):line(c,x0,y0,x1,y1,'#7a6a52',14,.9);line(c,x0,y0-12,x1,y1-12,'#5a4e3e',4,.9)
    with layer(c,cam,1):
        ground(c,160,'#3a3428','#100e0a')
        for x in(-900,-500,600,950):tent(c,x,180,2.0,'#5a5444',lit=0)
        draw_army(c,army(34,26,-1300,1300,200,300,['gmsol'],('kneel','stand'),110,160),t,bob=0)
        person(c,0,260,480,'feng',pose='stand',t=t,face=-1,eyes='closed')
    dust(c,t,0,W,H*.7,20,colr='#6a6050',a=.2)
    label(c,t,bt(2.4),'按兵不前',W*.76,H*.2,56,('#ff9a7a','#c0392b'))
@nx(5,'1924年10月·密约','他早已和{张作霖、段祺瑞}秘密约定',fx=[(0,'heart',.7),(.3,'tele',.4,4),(1,'paper',.5)])
def s43(c,t,T):
    rect(c,0,0,W,H,'#0a0806')
    sc=M.nmap(c,t,117.5,40.0,1.3,regions=False);G.endmap(c);tint(c,'#000000',.55)
    P=[(W*.5,H*.26,'冯玉祥','#5c6670','冯'),(W*.24,H*.66,'张作霖','#9a8048','张'),(W*.76,H*.66,'段祺瑞','#5a5a5e','段')]
    for i,(x,y,n,cc,ch) in enumerate(P):badge(c,t,bt(.2+i*.5),x,y,n,'',cc,ch,80)
    for i,(a_,b_) in enumerate(((0,1),(0,2),(1,2))):
        k=ramp(t,bt(1.6+i*.5),bt(2.4+i*.5))
        if k<=0:continue
        x0,y0=P[a_][:2];x1,y1=P[b_][:2]
        col(c,GOLD,.8);c.set_line_width(4);c.set_dash([16,10]);c.move_to(x0,y0);c.line_to(lerp(x0,x1,k),lerp(y0,y1,k));c.stroke();c.set_dash([])
    label(c,t,bt(3.2),'密 约',W*.5,H*.56,64,clib.GOLDG)
@nx(5,'1924年10月·密约','据当事人回忆，张作霖出了约{120万}','王坦回忆：张作霖自称出资约120万；一说50万',fx=[(0,'heart',.8),(.3,'coins',.7),(1.2,'coins',.8),(2.0,'coins',.9),(2.8,'coins',.8)])
def s44(c,t,T):
    rect(c,0,0,W,H,'#0e0a06');glow(c,W*.55,H*.55,700,'#8a6a20',.35)
    z=seg(t,[(0,1.0),(bt(5),1.18)])
    c.save();c.translate(W*.58,H*.62);c.scale(z,z)
    n=int(ramp(t,.1,bt(3.5))*14)
    for j in range(5):coinstack(c,-260+j*130,120,max(0,n-j*2),1.8)
    for i in range(min(6,n//2)):notes(c,-200+i*80,-60-i*18,1.1,txt='银元',rot=-.2+i*.08)
    c.restore()
    counter(c,t,'据王坦回忆',[(bt(.5)+i*.35,'%d万'%v) for i,v in enumerate([10,40,80,100,120])],note='一说50万',h=GOLD)
@nx(3,'',fx=[(0,'heart',1.0,3,'fast'),(0,'clock',.7,3)])
def s45(c,t,T):
    rect(c,0,0,W,H,'#050404');glow(c,W/2,H/2,600,'#5a0e0a',.4+.15*math.sin(t*9))
    bigword(c,t,.1,'10月22日',W/2,H*.4,150,h=RED)
    if t>.6:clib.htext(c,'夜',W/2,H*.68,200,('#ffffff','#c8c0b0'),cl((t-.6)*3))
@nx(5,'1924年10月22日夜·古北口→北京','冯玉祥{掉头回师}，直扑北京',fx=[(0,'heart',1.0,5,'fast'),(0,'steps',.8),(.5,'tele',.7,3,'urgent')])
def s46(c,t,T):
    sc=M.nmap(c,t,116.8,40.3,seg(t,[(0,2.6),(bt(5),3.4)]),regions=False)
    tint(c,'#000814',0)
    M.cities(c,t,sc,['古北口','北京'],red=('北京',),pulse=('北京',),size=40)
    G.route(c,[(117.15,40.69),(116.95,40.45),(116.7,40.15),(116.42,39.93)],ramp(t,.1,bt(3.5)),sc,h=RED,lw=10,arrow=True)
    G.endmap(c)
    tint(c,'#000814',.25)
    counter(c,t,'回师',[(.1,'22日夜')]+[(bt(4),'23日')],h=RED)
@nx(4,'1924年10月22日夜','部队连夜{急行军}',fx=[(0,'rain',.8),(0,'steps',1.0),(0,'heart',1.0,4,'fast'),(1,'train',.6,3)])
def s47(c,t,T):
    cam=cm(t,(0,-60,1.05),(200,-80,1.15),4)
    nightsky(c,cam,t,'#04060a','#141a24',0)
    with layer(c,cam,.3):ridge(c,30,'#0a0c10',amp=40,seed=4);bjskyline(c,60,'#0c0e14',lit=.2)
    with layer(c,cam,1):
        ground(c,100,'#14161a','#040406')
        draw_army(c,GM,t,dx=t*360,pose='walk',march=.6,spd=10)
    rain(c,t,420,.25,50,.4,area=(0,0,W,H))
    tint(c,'#06101c',.25)
@nx(4,'1924年10月23日·北京','23日，冯军开进{北京}',fx=[(0,'heart',1.0,4,'fast'),(0,'steps',.9),(.6,'creak',1.0),(2.4,'slam',.6)])
def s48(c,t,T):
    cam=cm(t,(0,-100,1.0),(0,-80,1.18),4)
    nightsky(c,cam,t,'#04060c','#18202c',40)
    with layer(c,cam,.5):
        citywall(c,-2400,2400,-140,260,'#3a3a3e','#2a2a2e');gatetower(c,0,-140,260,1.1,name='北京',gate_open=ramp(t,bt(.6),bt(2.4)),pillar='#4a1a16')
        searchlight(c,-700,-160,-1.0+math.sin(t)*.2,t);searchlight(c,700,-160,-2.1+math.sin(t*.8)*.2,t)
    with layer(c,cam,1):
        ground(c,260,'#16161a','#040406')
        L=army(35,30,-1500,600,250,300,['gmsol'],('walk',),120,160)
        draw_army(c,L,t,dx=t*120,pose='walk',march=.4,spd=8)
    tint(c,'#06101c',.2)
@nx(5,'1924年10月23日·中南海延庆楼','总统曹锟，被{软禁}在延庆楼',fx=[(0,'heart',.9,5,'fast'),(0,'steps',.6,2),(1.8,'slam',.9),(2.4,'stamp',1.0)])
def s49(c,t,T):
    cam=cm(t,(0,-140,.9),(0,-160,1.1),5)
    nightsky(c,cam,t,'#04060c','#161c26',40)
    with layer(c,cam,.7):
        westbldg(c,0,140,1.0,lit=(0,1,0,0,1,0),name='延庆楼')
        pass
    with layer(c,cam,.7):
        c.save();c.rectangle(-246,-372,80,172);c.clip();person(c,-206,-190,150,'cao',pose='stand',t=t,face=1,eyes='closed');c.restore()
    with layer(c,cam,1):
        ground(c,200,'#16161a','#040406')
        L=army(36,24,-1400,1400,220,300,['gmsol'],('hold',),120,160,faces=(1,-1))
        draw_army(c,L,t,bob=0)
    tint(c,'#06101c',.15)
    stamp(c,t,bt(2.4),'软禁',W*.78,H*.22,120,.05)
@nx(4,'1924年10月23日·北京','史称{北京政变}',fx=[(0,'heart',1.0,1.8,'fast'),(1.8,'impact',1.4),(1.8,'gong',1.2),(1.85,'stamp',1.2)])
def s50(c,t,T):
    sc=M.nmap(c,t,116.4,39.9,seg(t,[(0,2.6),(bt(1.8),3.2),(bt(4),3.4)]))
    G.city(c,'北京',sc,t,state='red',pulse=1,big=2.2,size=44,ly=50,lx=-40)
    for i in range(24):
        an=i/24*2*math.pi;x,y=G.P(116.4,39.9);k=ramp(t,bt(1.8),bt(2.6));L=(60+220*k)*sc
        line(c,x+math.cos(an)*40*sc,y+math.sin(an)*40*sc,x+math.cos(an)*L,y+math.sin(an)*L,RED,3*sc,.7*(1-k*.6))
    G.endmap(c)
    if bt(1.8)<t<bt(1.8)+.12:tint(c,'#ffffff',.6)
    stamp(c,t,bt(1.8),'北京政变',W/2,H*.23,150,-.04)
@nx(4,'1924年10月·北京','冯部改称{国民军}',fx=[(0,'bugle',.9),(0,'steps',.6)])
def s51(c,t,T):
    cam=cm(t,(0,-100,1.0),(0,-120,1.12),4)
    with layer(c,cam,.03):sky(c,'#0a0c12','#4a3a34',-900,80);glow(c,0,0,900,'#c0703a',.2)
    with layer(c,cam,.4):bjskyline(c,40,'#14141a',lit=.4)
    with layer(c,cam,1):
        ground(c,140,'#24221e','#080606')
        draw_army(c,army(37,90,-1700,1700,150,300,['gmsol'],('hold',),80,150,grid=True,cols=30),t,bob=1)
        flags(c,range(-1500,1600,250),150,320,t,'国民','#2a3a6a',1.3)
    label(c,t,bt(1),'国 民 军',W*.5,H*.2,64,clib.GOLDG)
@nx(5,'1924年10月24日·北京','24日，北京下令{停战}，免去吴佩孚职务',fx=[(0,'tele',1.0,3.5,'urgent'),(2.2,'stamp',1.2),(2.25,'impact',1.0)])
def s52(c,t,T):
    rect(c,0,0,W,H,'#0e0a08');glow(c,W/2,H/2,700,'#6a2a14',.3)
    r=random.Random(3)
    morse_tape(c,0,H*.12,W,t,spd=500)
    sk=shake_(t,bt(2.2))
    c.save();c.translate(sk,0)
    scroll_doc(c,W*.5,H*.52,860,600,['大总统令','即日停战','免吴佩孚本兼各职'],t,.1,seal=(bt(2.2),W*.5-280,H*.52+170,'印'))
    c.restore()
    telekey(c,W*.84,H*.8,1.1,t,press=1 if int(t*14)%3==0 else 0)
def shake_(t,t0):
    u=t-t0
    return math.sin(u*80)*20*(1-u/.4) if 0<u<.4 else 0
@nx(5,'1924年10月·山海关','一夜之间，他的{后路断了}',fx=[(0,'paper',.6),(.6,'heart',1.0,1.6,'fast'),(2.2,'impact',1.6),(2.3,'gong',.9)])
def s53(c,t,T):
    cam=cm(t,(0,0,1.0),(0,-40,1.25),5)
    rect(c,0,0,W,H,'#08090c')
    with layer(c,cam,.2):sea(c,t,240,colr='#0c1418',colr2='#14242a');far_fires(c,t,200,5,s=.5)
    with layer(c,cam,1):
        wu_bust(c,80,560,1.0,t,eyes='closed' if t>bt(2.2) else 'open',look=.3,cap=True,light=.4)
    u=t-bt(.3)
    if u>0:
        c.save();c.translate(W*.22+u*40,H*.4+u*u*160);c.rotate(u*1.2);rect(c,-120,-80,240,160,'#e8dcbc',.9);text(c,'免职令',0,10,40,'#7a1f1a');c.restore()
    if t>bt(2.2):tint(c,'#000000',min(.45,(t-bt(2.2))*.6))
    stamp(c,t,bt(2.2),'一夜崩塌',W*.74,H*.26,110,.05)
# ================= 6 崩塌 =================
@nx(5,'1924年10月底·京奉线','前有奉军，后有{国民军}',fx=[(0,'boom',.5),(1,'boom',.6),(1.6,'steps',.6,3),(2.6,'boom',.7),(3.6,'expl',.6)])
def s54(c,t,T):
    sc=M.nmap(c,t,118.2,39.9,seg(t,[(0,1.9),(bt(5),2.2)]))
    M.cities(c,t,sc,['山海关','秦皇岛','北京','天津','滦州'],red=('北京',),size=34,off={'秦皇岛':(16,24),'天津':(16,24)})
    for i in range(5):G.flag(c,118.6+i*.22,39.75+i*.05,sc,'直',h='#4e5f73',tc='#efe2c4',t=t)
    M.arrow(c,[(121.0,40.9),(120.3,40.4),(119.85,40.1)],ramp(t,.1,bt(2)),sc,lw=10)
    M.arrow(c,[(116.4,39.9),(117.2,39.6),(118.0,39.7),(118.5,39.75)],ramp(t,bt(1.2),bt(3.4)),sc,h='#9aa4ae',lw=10)
    G.endmap(c)
    badge(c,t,bt(.3),W*.86,H*.27,'奉军','正面','#9a8048','奉',54)
    badge(c,t,bt(1.4),W*.14,H*.27,'国民军','背后','#5c6670','国',54)
@nx(5,'1924年10月底·石家庄','{阎锡山}出兵石家庄，截断京汉路',fx=[(0,'train',.6,2),(1.4,'steps',.6,2),(3.0,'clatter',.6),(3.1,'impact',.6)])
def s55(c,t,T):
    sc=M.nmap(c,t,114.8,38.4,seg(t,[(0,1.8),(bt(5),2.1)]))
    M.cities(c,t,sc,['太原','石家庄','保定','北京'],red=('石家庄',),pulse=('石家庄',),size=36)
    G.route(c,[(112.55,37.87),(113.3,37.9),(114.0,38.0),(114.45,38.04)],ramp(t,.1,bt(2.5)),sc,h='#a8a070',lw=8,arrow=True)
    G.endmap(c)
    badge(c,t,bt(.3),W*.14,H*.3,'阎锡山','山西督军','#6a6a52','阎',56)
    xmark(c,t,bt(3),W*.56,H*.56,56)
    label(c,t,bt(3.1),'京汉路 切断',W*.78,H*.64,44,('#ff9a7a','#c0392b'))
@nx(5,'1924年11月初·秦皇岛','直军主力在山海关、秦皇岛{被围缴械}',fx=[(0,'wind',.6),(.4,'clatter',.8),(1.2,'clatter',.8),(2.0,'clatter',.8),(2.6,'stamp',1.0)])
def s56(c,t,T):
    cam=cm(t,(0,-70,1.0),(80,-90,1.15),5)
    with layer(c,cam,.03):sky(c,'#14141a','#5a4a40',-900,80)
    with layer(c,cam,.3):sea(c,t,40,colr='#141e24');gunboat(c,800,60,.35,t,-1,lit=0,smk=False)
    with layer(c,cam,1):
        ground(c,120,'#3a3428','#0e0c08')
        n=int(ramp(t,.1,bt(4))*30)
        rifle_pile(c,0,250,4+n,1.0,seed=3)
        draw_army(c,army(38,24,-1400,-200,170,300,['zsol'],('surr','stand'),120,160),t,bob=0)
        draw_army(c,army(39,14,250,1400,170,300,['fsol'],('hold',),130,170,faces=(-1,)),t,bob=0)
    stamp(c,t,bt(2.6),'缴械',W*.78,H*.22,120,.05)
@nx(4,'1924年11月','{二十万}大军，就此瓦解',fx=[(0,'heart',.5,2),(.4,'tick',.8,2.5),(3.0,'impact',1.0)])
def s57(c,t,T):
    rect(c,0,0,W,H,'#080605')
    k=ramp(t,.3,bt(3))
    n=int(200*(1-k)**1.5)
    r=random.Random(9)
    for i in range(160):
        x=W*.08+(i%20)*W*.032;y=H*.3+(i//20)*64
        a=1 if i<n*160/200 else max(0,1-(t-bt(.2))*.5)*.12
        blit(c,spr('zsol','stand',60),x,y+30,.95,a)
    v=int(lerp(20,0,k)*10)/10
    clib.htext(c,'%g万'%max(v,0) if k<.99 else '瓦解',W*.82,H*.5,130,clib.GOLDG if k<.99 else ('#ff9a7a','#c0392b'))
# ================= 7 回到塘沽 =================
@nx(6,'1924年11月3日·塘沽','11月3日，吴佩孚率残部约{两千人}，从塘沽乘舰南下','（人数一说数千）',fx=[(0,'sea',1.0),(.6,'shiphorn',1.0),(0,'wind',.4)])
def s58(c,t,T):
    cam=cm(t,(100,-60,1.15),(0,-60,1.0),6)
    with layer(c,cam,.03):
        sky(c,'#0a0d14','#4a3426',-900,40);glow(c,-500,20,700,'#c06a30',.35)
        clouds(c,t,'#1a1a22',.7,12,seed=3,y=(-520,-200),spd=6)
    with layer(c,cam,.2):ridge(c,30,'#12141a',amp=26,seed=5)
    with layer(c,cam,.5):sea(c,t,40)
    with layer(c,cam,.7):
        x=0+t*70
        gunboat(c,x,150,.9,t,1)
        c.save();c.rectangle(x-200,0,10,10);c.restore()
        person(c,x-120*.9,150-48*.9-2,64,'wpf',pose='stand',t=t,face=-1)
    with layer(c,cam,1.35):pier(c,-500,330,1200)
    vign(c,.5)
@nx(5,'1924年11月·渤海','从冯玉祥回师到登舰南下，只隔了{12天}',fx=[(0,'sea',.9),(2.5,'shiphorn',.5)])
def s59(c,t,T):
    cam=cm(t,(0,-80,1.0),(0,-60,.92),5)
    with layer(c,cam,.03):sky(c,'#0c0e16','#2a2a30',-900,80)
    with layer(c,cam,.4):sea(c,t,60,colr='#0e1a20')
    with layer(c,cam,.4):gunboat(c,300+t*20,70,.22,t,1,lit=1)
    counter(c,t,'10月22日 → 11月3日',[(bt(.3)+i*.18,'%d天'%(i+1)) for i in range(12)])
# ================= 8 复盘 =================
@nx(5,'','他以“{不入租界、不举外债}”自许，讲忠义','常见说法：不入租界、不举外债',fx=[(0,'wind',.4),(.3,'paper',.7),(2.5,'stamp',.5)])
def s60(c,t,T):
    rect(c,0,0,W,H,'#0e0a08');glow(c,W*.35,H*.5,700,'#5a3a14',.35)
    c.save();c.translate(W*.3,H*1.0);c.scale(.6,.6);wu_bust(c,0,0,1.0,t,light=.4,look=.4);c.restore()
    for i,txt in enumerate(('不入租界','不举外债')):
        k=eo((t-bt(.4+i*.6))/.5)
        if k<=0:continue
        x=W*(.62+i*.16);rect(c,x-70,H*.15,140,560*k,'#e8dcbc');col(c,RED);c.set_line_width(5);c.rectangle(x-60,H*.15+10,120,560*k-20);c.stroke()
        if k>.9:clib.vtext(c,txt,x,H*.15+110,96,'#1a120c')
@nx(7,'','但他输在：{失人心、薄待部将、对手变强、前线先失、后路被断}',fx=[(.3,'stamp',.5),(1.1,'stamp',.5),(1.9,'stamp',.5),(2.7,'stamp',.6),(3.5,'stamp',.8),(5,'paper',.4)])
def s61(c,t,T):
    rect(c,0,0,W,H,'#0d0907');glow(c,W/2,H*.5,800,'#5a3a14',.35)
    items=['贿选失人心','薄待冯玉祥','奉军整军','九门口先失','倒戈断后路']
    for i,s_ in enumerate(items):
        k=eback(cl((t-bt(.3+i*.8))/.35))
        if k<=0:continue
        x=W/2+(i-2)*300;y=H*.44
        c.save();c.translate(x,y);c.rotate((i-2)*.06);c.scale(k,k)
        rect(c,-115,-230,230,460,'#2a1a10');rect(c,-105,-220,210,440,'#e8dcbc');col(c,RED);c.set_line_width(6);c.rectangle(-95,-210,190,420);c.stroke()
        clib.vtext(c,s_,0,-150,68 if len(s_)<5 else 62,'#7a1f1a');c.restore()
@nx(6,'','枪口可以买，{人心买不回来}',fx=[(0,'sea',.5),(.3,'coins',.4),(3,'gong',.6)])
def s62(c,t,T):
    rect(c,0,0,W,H,'#070504');glow(c,W*.3,H*.5,500,'#8a6a20',.25)
    c.save();c.translate(W*.3,H*.58)
    rifle_pile(c,0,40,14,1.2,seed=5);coinstack(c,-120,90,8,1.6);coinstack(c,120,100,6,1.6)
    c.restore()
    k=ramp(t,bt(1),bt(5))
    for i in range(12):
        x=W*.62+(i%6)*70+k*240;y=H*.62+(i//6)*40
        blit(c,spr('zsol','walk',120,1,i%4),x,y,1.0,(1-k)*.8)
    glow(c,W*.3,H*.55,300,GOLD,.15)
    clib.htext(c,'枪 口',W*.3,H*.3,80,clib.GOLDG,cl((t-.3)*2))
    clib.htext(c,'人 心',W*.72,H*.3,80,('#c8c0b0','#8a8070'),cl((t-bt(1.2))*2)*(1-k*.7))
@nx(6,'',fx=[(0,'sea',.5),(.4,'paper',.5),(3.6,'stamp',.6),(4.4,'gong',.7)])
def s63(c,t,T):
    rect(c,0,0,W,H,'#0d0907');glow(c,W/2,H*.5,800,'#3a2414',.5)
    k=eo((t-.1)/.8);ww=1500*k
    rect(c,W/2-ww/2,H*.14,ww,H*.66,'#1e140e');rect(c,W/2-ww/2-16,H*.12,16,H*.7,'#5a3a1a');rect(c,W/2+ww/2,H*.12,16,H*.7,'#5a3a1a')
    ev=[('1920.7','直皖战争 · 奇袭松林店'),('1922.4','第一次直奉 · 奉军退出关外'),('1923.4','洛阳五十大寿'),('1923.10','曹锟贿选'),('1924.9','登上《时代》封面'),('1924.10','北京政变'),('1924.11','塘沽登舰南下')]
    if k>.95:
        line(c,W*.18,H*.48,W*.82,H*.48,GOLD,2,.6)
        for i,(y_,s_) in enumerate(ev):
            a=cl((t-bt(.6+i*.35))*3)
            if a<=0:continue
            x=W*.2+i*W*.1
            circ(c,x,H*.48,9,RED if i>=5 else GOLD,a)
            text(c,y_,x,H*.48-30-(i%2)*0,26,GOLD,a)
            clib.vtext(c,s_.split(' · ')[0],x,H*.48+50,30,'#efe2c4',a)
    stamp(c,t,bt(3.6),'吴佩孚',W*.82,H*.76,70,.05)
