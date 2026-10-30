from wscene import *
def cm(t,k0,k1,n):return seg(t,[(0,k0),(bt(n),k1)])
DECK=army(11,46,-300,300,-60,-40,['zsol','zsol','zsol'],('stand','kneel'),26,34,faces=(1,-1))
ZJ=army(12,140,-1700,1700,40,300,['zsol'],('walk',),50,150,grid=True,cols=28)
WJ=army(13,120,-1700,1700,40,300,['wsol2'],('walk',),50,150,grid=True,cols=24)
FJ=army(14,90,-1600,1600,60,300,['fsol'],('stand','hold'),50,150)
# ================= 0 开场：塘沽 =================
@nx(6,'1924年11月·塘沽','1924年11月3日，一艘兵舰驶离{塘沽}',fx=[(0,'sea',1.0),(0,'wind',.5),(1,'shiphorn',1.0)])
def s01(c,t,T):
    cam=cm(t,(0,-60,1.0),(120,-80,1.12),6)
    with layer(c,cam,.03):
        sky(c,'#0a0d14','#4a3426',-900,40);glow(c,-500,20,700,'#c06a30',.35)
        clouds(c,t,'#1a1a22',.7,12,seed=3,y=(-520,-200),spd=6)
    with layer(c,cam,.2):
        ridge(c,30,'#12141a',amp=26,seed=5);
        for k in range(8):circ(c,-1300+k*90,24,4,'#ffb050',.7)
    with layer(c,cam,.5):sea(c,t,40)
    with layer(c,cam,.7):
        x=-150+t*45
        gunboat(c,x,170,1.25,t,1)
        for d in DECK:blit(c,spr(d['kind'],d['pose'],60,d['face']),x+d['x']*1.1,170-50*1.25+5,d['h']/60*1.25)
    with layer(c,cam,1.35):
        pier(c,-500,330,1200)
        for k in range(4):rect(c,-1300+k*240,260,18,400,'#0c0906')
    vign(c,.5)
@nx(4,'1924年11月·塘沽','船上挤着约{两千}名残兵','（人数一说数千）',fx=[(0,'sea',.7),(0,'wind',.6)])
def s02(c,t,T):
    cam=cm(t,(0,-80,1.05),(-80,-100,1.18),4)
    with layer(c,cam,.03):sky(c,'#0c0f16','#3a2c24',-900,100)
    with layer(c,cam,.3):sea(c,t,60,colr='#101e24')
    with layer(c,cam,1):
        rect(c,-2400,210,4800,400,'#2a2c30');rect(c,-2400,200,4800,12,'#4a4e54')
        r=random.Random(5)
        L=army(15,34,-1300,1300,190,320,['zsol','zsol'],('kneel','stand','kneel'),170,280,faces=(1,-1))
        draw_army(c,L,t,bob=1)
        for x in range(-1400,1400,60):line(c,x,120,x,200,'#1a1a1e',4)
        line(c,-2400,120,2400,120,'#1a1a1e',6)
    vign(c,.6)
@nx(6,'1924年11月·塘沽','{两个月前}，这个人手握{二十万}大军',fx=[(0,'sea',.5),(.4,'heart',1.0,1.2),(2.4,'rewind',1.0),(3.3,'impact',.8)])
def s03(c,t,T):
    cam=cm(t,(0,0,1.0),(0,-30,1.12),6)
    rect(c,0,0,W,H,'#0a0b10')
    with layer(c,cam,.2):
        g=lgrad(c,0,-600,0,600,[(0,'#0a0c12',1),(1,'#1a2a30',1)]);c.set_source(g);c.rectangle(-2000,-1000,4000,2000);c.fill()
        sea(c,t,200,colr='#0e1a20')
    with layer(c,cam,1):wu_bust(c,-260,620,1.3,t,eyes='open',look=-.6,light=.6)
    k=ramp(t,bt(2.4),bt(3.3))
    if 0<k<1:
        r=random.Random(int(t*20))
        for j in range(40):y=r.uniform(0,H);line(c,0,y,W,y,'#f3e6c8',r.uniform(1,4),.5*(1-abs(k-.5)*2))
        tint(c,'#f3e6c8',.25*(1-abs(k-.5)*2))
    if t>bt(3.3):
        tint(c,'#2a1a08',.35)
        bigword(c,t,bt(3.3),'20万',W*.73,H*.42,190)
        text(c,'直系兵力（约）',W*.73,H*.58,34,'#c8b48a',cl((t-bt(3.6))*3))
    vign(c,.5)
@nx(5,'1924年9月8日·美国','1924年9月8日，他登上美国《时代》周刊{封面}','《时代》1924年9月8日封面：GENERAL WU，“Biggest man in China”',fx=[(.3,'shutter',1.0),(.4,'paper',.6),(2.6,'paper',.5)])
def s04(c,t,T):
    rect(c,0,0,W,H,'#120d09')
    r=random.Random(3)
    for i in range(9):
        c.save();c.translate(r.uniform(0,W),r.uniform(0,H));c.rotate(r.uniform(-.6,.6));rect(c,-200,-140,400,280,'#2a2218');
        for k in range(8):rect(c,-180,-120+k*30,360,8,'#3a3024')
        c.restore()
    z=seg(t,[(0,.6),(bt(1),.92),(bt(5),1.02)]);rot=seg(t,[(0,-.3),(bt(1),-.04),(bt(5),-.02)])
    c.save();c.translate(W*.36,H*.47);c.rotate(rot);time_cover(c,0,0,z*.95,t);c.restore()
    if t<.25:tint(c,'#ffffff',.9*(1-t/.25))
    label(c,t,bt(2.3),'第一位登上《时代》封面的中国人',W*.73,H*.3,40)
    label(c,t,bt(3.2),'“中国最强者”',W*.73,H*.46,52,clib.GOLDG)
@nx(5,'1924年·上海','美国记者鲍威尔说：他{比其他任何人更有可能统一中国}','鲍威尔《我在中国二十五年》',fx=[(0,'type',.8,2.5),(3,'paper',.4)])
def s05(c,t,T):
    cam=cm(t,(0,-60,1.0),(80,-90,1.12),5)
    with layer(c,cam,.1):
        rect(c,-2000,-1000,4000,2000,'#1e1812')
        rect(c,350,-450,380,420,'#c8b48a',.25);
        for k in range(1,4):line(c,350+k*95,-450,350+k*95,-30,'#1e1812',8);line(c,350,-450+k*105,730,-450+k*105,'#1e1812',8)
        glow(c,540,-240,520,'#e8c890',.25)
    with layer(c,cam,1):
        rect(c,-800,160,1300,40,'#4a3020');rect(c,-760,200,30,300,'#3a2418');rect(c,420,200,30,300,'#3a2418')
        rect(c,-420,90,240,70,'#1a1a1a');rect(c,-400,60,200,40,'#2a2a2a');rect(c,-360,20,120,46,'#e8e4dc')
        for k in range(10):circ(c,-400+k*20,120,6,'#c8c8c8')
        person(c,-40,180,330,'powell',pose='hold',t=t,face=-1,talk=True)
        rect(c,200,120,120,40,'#e8dcbc');rect(c,240,90,90,30,'#e8dcbc')
    label(c,t,bt(1.6),'“比其他任何人更有可能统一中国”',W*.6,H*.2,46,clib.GOLDG)
    infocard(c,t,bt(.4),70,110,'鲍威尔','美国记者',['《密勒氏评论报》主编'],w=420)
@nx(6,'',fx=[(0,'impact',1.0),(.2,'gong',1.0),(2.2,'stamp',1.0),(3.2,'stamp',1.2),(3.3,'impact',.8)])
def s06(c,t,T):
    rect(c,0,0,W,H,'#0b0806')
    sc=M.nmap(c,t,117.5,39.4,seg(t,[(0,1.4),(bt(6),1.6)]),regions=False);G.endmap(c)
    tint(c,'#000000',.55)
    glow(c,W/2,H*.42,700,'#7a2a14',.35)
    c.save();c.translate(W*.22,H*.98);c.scale(.62,.62);wu_bust(c,0,0,1.0,t,coat='#141820',light=.2);c.restore()
    tint(c,'#000000',.25)
    bigword(c,t,.15,'吴 佩 孚',W*.6,H*.36,190)
    stamp(c,t,bt(2.2),'四年封神',W*.45,H*.64,90,-.05,'#d9a040')
    stamp(c,t,bt(3.2),'一夜崩塌',W*.77,H*.66,90,.06)
# ================= 1 直皖 1920 =================
@nx(5,'1920年7月·京畿','1920年7月14日，{直皖战争}爆发',fx=[(0,'tele',.8,2.5),(2.5,'boom',.5),(3.6,'boom',.6)])
def s07(c,t,T):
    sc=M.nmap(c,t,116.2,38.8,seg(t,[(0,1.6),(bt(5),2.0)]))
    M.cities(c,t,sc,['北京','保定','天津','洛阳'],size=34,pulse=('北京',))
    G.endmap(c)
    badge(c,t,bt(.5),W*.2,H*.32,'段祺瑞','皖系','#5a6448','段',70)
    badge(c,t,bt(1.2),W*.8,H*.32,'吴佩孚','直系 · 前敌总指挥','#4e5f73','吴',70)
    if t>bt(1.8):vs_line(c,W*.2+90,H*.32,W*.8-90,H*.32,t)
    stamp(c,t,bt(2.6),'开战',W*.5,H*.62,90,-.04)
@nx(5,'1920年7月·京汉线','皖军有{日本借款}编练的边防军，开局占上风','《北洋军阀史话》',fx=[(0,'steps',.8),(.4,'bugle',.7),(3,'boom',.5)])
def s08(c,t,T):
    cam=cm(t,(-150,-40,1.0),(150,-70,1.1),5)
    with layer(c,cam,.05):sky(c,'#2a2418','#a8784a',-900,60)
    with layer(c,cam,.25):ridge(c,30,'#4a3a24',amp=50,seed=4);ridge(c,60,'#3a2e1c',amp=30,seed=7)
    with layer(c,cam,1):
        ground(c,40,'#5a4a30','#1a120a')
        flags(c,range(-1500,1600,300),40,260,t,'皖','#5a6448')
        draw_army(c,WJ,t,dx=t*70,march=.5)
        dust(c,t,-1600,1600,300,30,a=.25)
    label(c,t,bt(1.4),'日本借款 · 边防军',W*.72,H*.18,44)
@nx(5,'1920年7月17日·松林店','7月17日，吴佩孚{奇袭松林店}',fx=[(0,'hoof',.8,3),(1,'tele',.5,1.5),(3.4,'boom',.7)])
def s09(c,t,T):
    sc=M.nmap(c,t,115.8,39.25,seg(t,[(0,3.6),(bt(5),4.6)]),regions=False)
    M.cities(c,t,sc,['松林店','保定','北京'],red=('松林店',),pulse=('松林店',),size=36,off={'北京':(16,-12)})
    M.arrow(c,[(116.1,39.75),(115.95,39.5),(115.75,39.2)],ramp(t,.1,bt(1.5)),sc,h=RED,lw=9)
    G.route(c,[(115.55,38.95),(115.45,39.15),(115.6,39.38),(115.88,39.42)],ramp(t,bt(1.5),bt(3.5)),sc,h=GOLD,lw=7,arrow=True)
    G.endmap(c)
    label(c,t,bt(2),'夜 袭',W*.75,H*.2,56,clib.GOLDG)
    badge(c,t,bt(.4),W*.12,H*.3,'吴佩孚','直军前敌总指挥','#4e5f73','吴',60)
@nx(5,'1920年7月17日·松林店','直取皖军{西路前敌司令部}',fx=[(0,'mg',.8),(0,'fire',.6),(1.2,'expl',1.0),(2.8,'expl',.9),(.5,'rifle',.6),(2,'rifle',.6)])
def s10(c,t,T):
    cam=cm(t,(-200,-60,1.05),(150,-90,1.2),5)
    nightsky(c,cam,t,'#06070c','#2a1a18',30)
    with layer(c,cam,.3):ridge(c,40,'#0e0c10',amp=40,seed=3);far_fires(c,t,40,6,s=.4)
    with layer(c,cam,1):
        ground(c,60,'#1e1814','#060404')
        for i,x in enumerate((300,620,900)):tent(c,x,140,2.2,'#4a4434',lit=1)
        fire(c,750,160,1.5,t,seed=2);fire(c,420,170,1.1,t,seed=5)
        L=army(16,26,-1300,200,120,300,['zsol'],('run',),90,170)
        draw_army(c,L,t,dx=t*260,pose='run',spd=10)
        for i in range(5):person(c,500+i*130,250+(i%2)*30,150,'wsol2',pose='fall' if t>bt(1.4+i*.3) else 'stand',t=t,face=-1)
        r=random.Random(int(t*12))
        for i in range(6):
            x=r.uniform(-900,300);y=r.uniform(130,240);glow(c,x,y,40,'#ffd070',.8);circ(c,x,y,6,'#fff0b0')
        explosion(c,700,150,1.4,t,bt(1.2),seed=1);explosion(c,950,170,1.2,t,bt(2.8),seed=2)
    embers(c,t,60,area=(0,0,W,H),a=.7)
@nx(4,'1920年7月17日·松林店','俘虏前敌总指挥{曲同丰}','《北洋军阀史话》',fx=[(0,'night',.6),(.4,'steps',.5,1.5)])
def s11(c,t,T):
    cam=cm(t,(0,-60,1.1),(0,-90,1.25),4)
    nightsky(c,cam,t,'#070810','#24161a',30)
    with layer(c,cam,1):
        ground(c,150,'#1e1814','#060404');fire(c,-700,260,1.6,t,seed=3);fire(c,800,250,1.3,t,seed=4)
        person(c,0,290,340,'qtf',pose='kneel',t=t,bound=True,eyes='closed')
        person(c,-260,290,380,'zsol',pose='hold',t=t,face=1);person(c,260,290,380,'zsol',pose='hold',t=t,face=-1)
    infocard(c,t,bt(.3),70,110,'曲同丰','皖军',['西路前敌总指挥'],w=420)
    stamp(c,t,bt(1.6),'被俘',W*.78,H*.24,110,.05)
@nx(5,'1920年7月·京畿','几天之内，皖军{全线溃败}',fx=[(0,'tele',.6,2),(1,'boom',.4),(2.2,'boom',.4)])
def s12(c,t,T):
    sc=M.nmap(c,t,116.0,39.0,seg(t,[(0,2.4),(bt(5),2.1)]))
    r=random.Random(4)
    for i in range(10):
        lo=115.4+r.uniform(0,1.2);la=39.0+r.uniform(0,.8);k=ramp(t,bt(.5+i*.25),bt(1+i*.25))
        G.flag(c,lo,la,sc,'皖',a=1-k*.85,h='#7a8a6a',tc='#1a1a10',t=t)
    M.cities(c,t,sc,['北京','保定','天津'],size=36)
    G.route(c,[(115.47,38.87),(115.9,39.42),(116.25,39.8)],ramp(t,bt(1),bt(3.5)),sc,h=GOLD,lw=7,arrow=True)
    G.endmap(c)
    counter(c,t,'开战',[(bt(.3)+i*.45,'第%d天'%(i+1)) for i in range(5)],note='7月14日—19日前后')
@nx(4,'1920年7月·北京','皖系首领{段祺瑞}下野',fx=[(0,'wind',.4),(1.4,'paper',.5)])
def s13(c,t,T):
    cam=cm(t,(0,-60,1.0),(-60,-80,1.15),4)
    with layer(c,cam,.1):rect(c,-2000,-1000,4000,2000,'#1a140f');glow(c,-300,-200,600,'#c89050',.18)
    with layer(c,cam,.5):
        rect(c,-900,-420,500,560,'#2a2018');
        for k in range(6):rect(c,-880,-400+k*90,460,10,'#3a2c20')
    with layer(c,cam,1):
        rect(c,-2000,250,4000,500,'#120e0a')
        person(c,100,280,470,'duan',pose='stand',t=t,face=-1 if t<bt(1.5) else 1,eyes='closed')
        r=random.Random(2)
        for i in range(5):
            u=ramp(t,bt(1.4)+i*.1,bt(3.5));c.save();c.translate(lerp(250,600+i*90,u),lerp(80,260,u));c.rotate(u*3+i);rect(c,-40,-30,80,60,'#e8dcbc',.9);c.restore()
    stamp(c,t,bt(1.6),'下野',W*.78,H*.25,120,.05)
@nx(5,'1920年','这一年，吴佩孚{46岁}，一战成名',fx=[(0,'crowd',.6),(.3,'bugle',.8),(2.8,'gong',.6)])
def s14(c,t,T):
    cam=cm(t,(0,-80,1.0),(0,-120,1.15),5)
    with layer(c,cam,.05):sky(c,'#2a1a10','#c08a4a',-900,60);glow(c,0,-100,900,'#ffc070',.25)
    with layer(c,cam,.4):
        ground(c,20,'#5a4a30','#2a1c10')
        draw_army(c,army(17,160,-1700,1700,20,120,['zsol'],('hold','stand'),34,60,grid=True,cols=40),t,bob=1)
        flags(c,range(-1600,1700,180),40,200,t,'吴','#c0392b')
    with layer(c,cam,1):
        ground(c,230,'#4a3a24','#120c06')
        horse(c,0,320,330,1,t,gallop=0,col_='#3a2418',rider='wpfc',rider_pose='ride')
    infocard(c,t,bt(.6),70,110,'吴佩孚','1874—1939',['字子玉，山东蓬莱人','1920年：46岁'],w=430)
# ================= 2 第一次直奉 1922 =================
@nx(5,'1922年4月·京奉线','1922年4月29日，奉军约{12万}入关，直军约{10万}',fx=[(0,'train',.7),(.2,'whistle',.8),(2.5,'boom',.6),(3.4,'boom',.6)])
def s15(c,t,T):
    sc=M.nmap(c,t,118.6,40.2,seg(t,[(0,1.35),(bt(5),1.6)]))
    M.cities(c,t,sc,['奉天','山海关','天津','北京','长辛店','保定'],red=('奉天',),size=36,off={'长辛店':(-16,22),'天津':(16,26)})
    M.arrow(c,[(123.43,41.8),(121.13,41.1),(119.75,40.0),(118.2,39.6),(117.45,39.05)],ramp(t,.1,bt(2.2)),sc,lw=9)
    M.arrow(c,[(119.75,40.0),(118.0,39.8),(116.8,39.7),(116.2,39.83)],ramp(t,bt(1.2),bt(3.2)),sc,lw=8)
    G.endmap(c)
    counter(c,t,'奉军入关',[(bt(.4),'约12万')],h=RED)
    counter(c,t,'直军',[(bt(1.6),'约10万')],y=360)
    badge(c,t,bt(.6),W*.86,H*.3,'张作霖','奉系 · 坐镇军粮城','#9a8048','张',60)
@nx(5,'1922年4月·长辛店','{长辛店}，两军炮战',fx=[(0,'boom',1.0),(1,'boom',.9),(1.6,'expl',.9),(2.4,'boom',1.0),(3.2,'expl',1.0),(4.0,'boom',.8),(0,'fire',.4)])
def s16(c,t,T):
    cam=cm(t,(-150,-60,1.0),(150,-80,1.12),5)
    with layer(c,cam,.04):sky(c,'#1a1210','#7a4a2a',-900,60)
    with layer(c,cam,.25):ridge(c,30,'#2a2018',amp=40,seed=8);far_fires(c,t,30,7,s=.5,seed=9)
    with layer(c,cam,.6):
        ground(c,60,'#3a2e20','#1a120a');rails(c,110,t=t)
        house(c,300,100,520,170,'#6a5a48','#2a2420');rect(c,170,-110,260,46,'#1a120c');text(c,'长 辛 店',300,-76,32,GOLD)
        for x in (700,1100):explosion(c,x,100,1.5,t,bt(1.6) if x==700 else bt(3.2),seed=x)
    with layer(c,cam,1):
        ground(c,230,'#3a2e20','#0a0604')
        for i,x in enumerate((-900,-500,-100)):cannon(c,x,300,1.1,t,1,fires=(bt(0+i*.35),bt(2.4+i*.3),bt(4.0)))
        draw_army(c,army(18,10,-1100,100,240,300,['zsol'],('hold','kneel'),120,150),t,bob=0)
    smoke(c,t,W*.6,H*.4,3,8,colr='#2a2018',a=.4)
@nx(4,'1922年4月·长辛店','一天之内，阵地反复{易手}','史载：一日之间，攻守九次易手',fx=[(0,'mg',.7),(.5,'expl',.8),(1.5,'boom',.8),(2.6,'expl',.9)])
def s17(c,t,T):
    cam=cm(t,(0,-40,1.25),(60,-60,1.4),4)
    with layer(c,cam,.05):sky(c,'#140e0c','#6a3a22',-900,60)
    with layer(c,cam,1):
        ground(c,120,'#2e2418','#0a0604');sandbags(c,-1000,1000,240,3)
        mg(c,-200,200,1.4,t,1,True)
        L=army(19,8,-900,700,180,260,['zsol'],('aim',),130,160)
        draw_army(c,L,t,bob=0)
        explosion(c,500,60,1.6,t,bt(.5),seed=4);explosion(c,-500,40,1.3,t,bt(2.6),seed=6)
    counter(c,t,'阵地易手',[(bt(.2)+i*.22,'%d次'%(i+1)) for i in range(9)],h=RED)
    embers(c,t,50,area=(0,0,W,H),a=.6)
@nx(5,'1922年5月·西线','吴佩孚出奇兵绕到背后，奉军{第十六师}倒戈',fx=[(0,'hoof',.7,2.5),(2.4,'tele',.6,1.2),(3.0,'stamp',1.0)])
def s18(c,t,T):
    sc=M.nmap(c,t,116.3,39.6,seg(t,[(0,3.4),(bt(5),3.9)]),regions=False)
    M.cities(c,t,sc,['长辛店','北京'],size=36,off={'长辛店':(-16,24)})
    for i in range(6):G.flag(c,116.05+i*.08,39.72-i*.04,sc,'奉',h='#9a8048',tc='#2a1a10',t=t)
    G.route(c,[(115.9,39.3),(115.65,39.55),(115.75,39.9),(116.1,39.98)],ramp(t,.1,bt(2.5)),sc,h=GOLD,lw=7,arrow=True)
    G.endmap(c)
    k=ramp(t,bt(2.5),bt(3.2))
    badge(c,t,bt(.5),W*.82,H*.3,'奉军第十六师','临阵倒戈','#9a8048' if k<.5 else '#4e5f73','16',64)
    stamp(c,t,bt(3.0),'倒戈',W*.3,H*.7,100,-.05)
@nx(4,'1922年5月·西线','奉军西路{崩溃}',fx=[(0,'wind',.5),(.4,'clatter',.8),(1.6,'clatter',.7),(2.4,'rifle',.4)])
def s19(c,t,T):
    cam=cm(t,(0,-60,1.05),(-80,-80,1.15),4)
    with layer(c,cam,.05):sky(c,'#1e1814','#8a6a4a',-900,60)
    with layer(c,cam,.3):ridge(c,40,'#3a2e20',amp=40,seed=2);smoke(c,t,300,0,2,8,colr='#2a2018',a=.4)
    with layer(c,cam,1):
        ground(c,120,'#4a3a26','#120c06')
        L=army(20,22,-200,1300,140,300,['fsol'],('surr','kneel','surr','fall'),110,170,faces=(-1,))
        draw_army(c,L,t,bob=0)
        whiteflag(c,500,240,300,t)
        rifle_pile(c,300,300,10,1.0)
        draw_army(c,army(21,8,-1300,-500,180,300,['zsol'],('hold',),130,170),t,dx=t*40)
@nx(5,'1922年5月·河南','同时，{冯玉祥}在河南击败亲奉的赵倜',fx=[(0,'tele',.5,2),(1.2,'boom',.5),(2.6,'boom',.5),(3,'steps',.5,2)])
def s20(c,t,T):
    sc=M.nmap(c,t,113.6,34.9,seg(t,[(0,2.2),(bt(5),2.6)]))
    M.cities(c,t,sc,['洛阳','郑州','开封'],red=('开封',),size=36)
    G.route(c,[(112.45,34.62),(113.0,34.7),(113.65,34.75),(114.2,34.8)],ramp(t,.2,bt(3)),sc,h=GOLD,lw=7,arrow=True)
    G.endmap(c)
    badge(c,t,bt(.4),W*.14,H*.3,'冯玉祥','直系将领','#5c6670','冯',60)
    badge(c,t,bt(1.4),W*.86,H*.3,'赵倜','河南督军 · 亲奉','#9a8048','赵',60)
    xmark(c,t,bt(3.3),W*.86,H*.3,60)
@nx(5,'1922年6月·山海关','奉军{退出山海关}',fx=[(0,'train',.6),(1,'whistle',.6),(3,'gong',.7)])
def s21(c,t,T):
    sc=M.nmap(c,t,119.8,40.6,seg(t,[(0,1.9),(bt(5),1.6)]))
    M.cities(c,t,sc,['山海关','奉天','锦州','秦皇岛'],size=36,off={'秦皇岛':(16,26)},pulse=('山海关',))
    M.arrow(c,[(119.5,40.0),(120.3,40.5),(121.13,41.1),(122.6,41.6)],ramp(t,.1,bt(3)),sc,h='#a07a4a',lw=9)
    G.route(c,[(118.2,39.7),(119.0,39.85),(119.65,39.98)],ramp(t,bt(.5),bt(2.5)),sc,h=GOLD,lw=7,arrow=True)
    G.endmap(c)
    stamp(c,t,bt(3),'退回关外',W*.72,H*.22,80,.04)
@nx(5,'1922年','直系从此{控制北京政府}',fx=[(0,'crowd',.6),(.2,'bugle',.9),(2.4,'gong',1.0),(2.45,'impact',.7)])
def s22(c,t,T):
    cam=cm(t,(0,-140,1.0),(0,-120,1.15),5)
    with layer(c,cam,.03):sky(c,'#1a0e08','#b0703a',-900,60);glow(c,0,-120,1000,'#ffc070',.3)
    with layer(c,cam,.3):
        ground(c,10,'#5a4a30','#2a1c10')
        draw_army(c,army(22,220,-1800,1800,10,120,['zsol'],('hold',),30,56,grid=True,cols=50),t,bob=1)
    with layer(c,cam,.6):flags(c,range(-1600,1700,140),130,300,t,'直','#c0392b',1.3)
    with layer(c,cam,1):
        rect(c,-300,170,600,60,'#3a2416');rect(c,-340,230,680,30,'#2a1810')
        person(c,0,170,360,'wpf',pose='raise',t=t,face=1,cape_wind=6)
    stamp(c,t,bt(2.4),'封神',W*.8,H*.24,150,.06)
# ================= 3 巅峰 1923 =================
@nx(5,'1923年4月·洛阳','1923年4月，吴佩孚在{洛阳}过五十大寿',fx=[(0,'crowd',.8),(0,'firecr',.7,2.5),(3,'firecr',.5,2)])
def s23(c,t,T):
    cam=cm(t,(0,-120,.95),(0,-100,1.12),5)
    palace(c,cam,t,tone=0)
    with layer(c,cam,.75):
        rect(c,-230,-360,460,320,'#a8261c');clib.htext(c,'寿',0,-120,260,clib.GOLDG)
    with layer(c,cam,1):
        draw_army(c,army(23,22,-1200,1200,180,300,['guest','guest2','zoff','yy'],('kneel','stand'),150,200),t,bob=0)
        person(c,0,150,300,'wpf',pose='stand',t=t)
        r=random.Random(int(t*15))
        for side in(-1,1):
            for i in range(10):x=side*r.uniform(700,1100);y=r.uniform(-200,200);circ(c,x,y,r.uniform(3,8),'#ffd070',.9);glow(c,x,y,30,'#ff8040',.5)
    badge(c,t,bt(.5),W*.14,H*.28,'吴佩孚','直鲁豫巡阅使','#4e5f73','吴',56)
@nx(6,'1923年4月·洛阳','康有为送来寿联：{八方风雨会中州}','康有为寿联：牧野鹰扬，百岁功名才半世；洛阳虎踞，八方风雨会中州',fx=[(0,'paper',.8),(.6,'paper',.6),(3,'gong',.5)])
def s24(c,t,T):
    rect(c,0,0,W,H,'#1e0c08');glow(c,W/2,H*.45,800,'#c04020',.3)
    oy=seg(t,[(0,30),(bt(6),-20)])
    k1=eo((t-.1)/1.2);k2=eo((t-.6)/1.2)
    couplet(c,W*.66,100+oy,.7,'牧野鹰扬百岁功名才半世',k1)
    couplet(c,W*.34,100+oy,.7,'洛阳虎踞八方风雨会中州',k2)
    badge(c,t,bt(2),W*.5,H*.32,'康有为','维新派领袖','#6a3a2a','康',56)
@nx(5,'1923年·洛阳','那一年，他站在{最高处}',fx=[(0,'wind',.4),(.3,'tele',.5,3),(3,'impact',.5)])
def s25(c,t,T):
    sc=M.nmap(c,t,114.5,37.0,seg(t,[(0,1.05),(bt(5),1.25)]))
    x0,y0=G.P(112.45,34.62)
    for i in range(8):
        an=i/8*2*math.pi;k=ramp(t,bt(.4+i*.12),bt(1.8+i*.12));L=520*k
        line(c,x0,y0,x0+math.cos(an)*L,y0+math.sin(an)*L*.8,GOLD,3*sc,.6)
    M.cities(c,t,sc,['洛阳','北京','天津','保定','开封'],size=36,pulse=('洛阳',),big=1.2)
    G.endmap(c)
    label(c,t,bt(1.2),'洛阳虎踞',W*.75,H*.2,52,clib.GOLDG)
@nx(4,'','但两颗{雷}，已经埋下',fx=[(0,'heart',.7,4),(.4,'fuse',.7,3),(2.6,'impact',.6)])
def s26(c,t,T):
    rect(c,0,0,W,H,'#0b0806')
    for i,(x,txt) in enumerate(((W*.34,'贿选'),(W*.66,'冯玉祥'))):
        k=pop(t,bt(.3+i*.8))
        if k<=0:continue
        c.save();c.translate(x,H*.48);c.scale(k,k)
        glow(c,0,0,300,RED,.3);circ(c,0,0,110,'#1a1210');circ(c,0,0,100,'#3a1a14');col(c,RED);c.set_line_width(6);c.arc(0,0,100,0,7);c.stroke()
        col(c,'#c8b48a');c.set_line_width(5);c.move_to(0,-100);c.curve_to(30,-150,-20,-180,10,-210);c.stroke()
        r=random.Random(int(t*20)+i)
        for j in range(8):circ(c,10+r.uniform(-14,14),-210+r.uniform(-14,14),r.uniform(2,5),'#ffd070')
        clib.htext(c,txt,0,24,64 if len(txt)<3 else 52,clib.IVORY);c.restore()
        text(c,'第'+'一二'[i]+'颗',x,H*.48+170,34,'#c8b48a',k)
@nx(5,'1923年10月·北京','1923年10月，{曹锟贿选}总统，每票{5000元}','史称“曹锟贿选”',fx=[(0,'crowd',.5),(.6,'coins',.7),(1.8,'coins',.7),(3.0,'coins',.8),(1.2,'paper',.4)])
def s27(c,t,T):
    cam=cm(t,(-150,-60,1.0),(100,-80,1.12),5)
    with layer(c,cam,.1):
        rect(c,-2000,-1000,4000,2000,'#1e1a16')
        for x in range(-1400,1500,260):rect(c,x-30,-500,60,700,'#4a3e32');rect(c,x-44,-520,88,30,'#5a4c3e')
        rect(c,-2000,-560,4000,60,'#2a221a');text(c,'众 议 院',0,-350,60,GOLD,.7,sp=20)
    with layer(c,cam,1):
        rect(c,-2000,220,4000,600,'#2a1c14');rect(c,200,100,520,130,'#4a3020');rect(c,200,90,520,16,'#6a4a30')
        person(c,520,100,240,'clerk',pose='hold',t=t,face=-1)
        for i in range(3):notes(c,300+i*60,80,.6,rot=-.1+i*.08)
        L=army(24,12,-1500,100,200,260,['yy','yy2'],('walk',),190,210)
        draw_army(c,[dict(d,x=d['x']*.7) for d in L],t,dx=t*60,pose='walk',spd=4,bob=1)
        coinstack(c,620,90,6+int(t*3),1.0)
    counter(c,t,'每票',[(bt(.8),'5000元')])
@nx(4,'1923年10月·北京','被收买的议员，被骂作“{猪仔议员}”',fx=[(0,'crowd',.7),(.3,'coins',.8),(1.5,'jeer',.8,2),(2.2,'stamp',1.0)])
def s28(c,t,T):
    rect(c,0,0,W,H,'#14100c');glow(c,W/2,H*.5,700,'#5a3a14',.4)
    z=seg(t,[(0,1.0),(bt(4),1.15)])
    c.save();c.translate(W/2,H*.55);c.scale(z,z)
    person(c,-150,300,620,'yy',pose='hold',t=t,face=1,eyes='closed')
    for i in range(4):notes(c,140+i*20,-40-i*14,1.2,rot=.2-i*.07)
    coinstack(c,330,200,10,1.6);coinstack(c,420,230,7,1.6)
    c.restore()
    label(c,t,bt(1.2),'猪仔议员',W*.74,H*.3,60,('#ff9a7a','#c0392b'))
    stamp(c,t,bt(2.2),'贿选',W*.24,H*.24,120,-.06)
@nx(4,'1923年10月·北京','曹锟当上总统，直系的{名声一落千丈}',fx=[(0,'paper',.6,3),(1,'crowd',.5)])
def s29(c,t,T):
    cam=cm(t,(0,-80,1.0),(0,-110,1.15),4)
    palace(c,cam,t,tone=1)
    with layer(c,cam,1):
        rect(c,-200,200,400,50,'#5a2a1a');person(c,0,200,380,'cao',pose='stand',t=t)
    r=random.Random(7)
    for i in range(14):
        u=(t*.4+r.random())%1;x=r.uniform(0,W);y=lerp(-100,H,u)
        c.save();c.translate(x+math.sin(t*2+i)*60,y);c.rotate(r.uniform(-1,1)+t);rect(c,-70,-46,140,92,'#d8ccb0',.85)
        text(c,'贿选',0,10,30,'#7a1f1a',.9);c.restore()
    badge(c,t,bt(.3),W*.14,H*.28,'曹锟','直系首领 · 大总统','#2e3a5a','曹',56)
@nx(5,'1922年10月·河南→北京','另一颗雷：1922年10月，{冯玉祥}被调离河南',fx=[(0,'tele',.6,2),(1,'train',.5,3),(1.5,'whistle',.4)])
def s30(c,t,T):
    sc=M.nmap(c,t,115.2,37.4,seg(t,[(0,1.3),(bt(5),1.5)]))
    M.cities(c,t,sc,['开封','北京','保定','石家庄'],size=36)
    G.route(c,M.RAIL['京汉'][::-1][:1]+[(114.35,34.8),(113.65,34.75),(114.5,38.04),(115.47,38.87),(116.4,39.78)],ramp(t,.3,bt(3.5)),sc,h='#9aa4ae',lw=6,dash=True,arrow=True)
    G.endmap(c)
    badge(c,t,bt(.4),W*.86,H*.3,'冯玉祥','原河南督军','#5c6670','冯',60)
@nx(5,'1922年10月·北京南苑','只给一个没有地盘的“{陆军检阅使}”，部队{缺饷}',fx=[(0,'wind',.9),(1.5,'heart',.4,2)])
def s31(c,t,T):
    cam=cm(t,(0,-60,1.0),(60,-90,1.14),5)
    with layer(c,cam,.04):sky(c,'#14161c','#4a4a50',-900,80)
    with layer(c,cam,.3):ridge(c,40,'#22242a',amp=30,seed=11)
    with layer(c,cam,1):
        ground(c,140,'#3a3830','#121010')
        L=army(25,30,-1300,1300,170,300,['gmsol'],('stand','kneel'),110,160)
        draw_army(c,L,t,bob=0)
        person(c,-380,280,470,'feng',pose='stand',t=t,face=1)
        ell(c,200,290,80,24,'#2a2a2a');ell(c,200,280,70,18,'#121212')
    snow(c,t,90,.6)
    label(c,t,bt(1),'陆军检阅使',W*.75,H*.2,52)
    label(c,t,bt(2.6),'部队缺饷',W*.75,H*.34,44,('#ff9a7a','#c0392b'))
@nx(4,'1923—1924年','冯玉祥和吴佩孚，{积怨}越来越深',fx=[(0,'heart',.6),(1.2,'zap',.6,2)])
def s32(c,t,T):
    rect(c,0,0,W,H,'#0b0806');glow(c,W*.3,H*.45,500,'#5c6670',.25);glow(c,W*.7,H*.45,500,'#4e5f73',.25)
    badge(c,t,.1,W*.27,H*.45,'冯玉祥','陆军检阅使','#5c6670','冯',120)
    badge(c,t,.3,W*.73,H*.45,'吴佩孚','直鲁豫巡阅使','#4e5f73','吴',120)
    if t>bt(1.2):vs_line(c,W*.27+150,H*.45,W*.73-150,H*.45,t)
    label(c,t,bt(1.6),'积 怨',W*.5,H*.27,60,('#ff9a7a','#c0392b'))
