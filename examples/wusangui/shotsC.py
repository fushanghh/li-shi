from base import *
from shotsA import chapter2
# ================= 盲区四 降维打击 =================
@shot(212,216)
def f1(c,t,T):chapter2(c,t,4,'降维打击','62岁老帅 vs 20岁雄主')
@shot(216,224,'')
def f2(c,t,T):
    k=eo(t/.5)
    # 左：暮气沉沉
    c.save();c.rectangle(0,0,W/2-6,H);c.clip()
    rect(c,0,0,W,H,'#1a1614');glow(c,W*.25,H*.4,500,'#5a4a3a',.4)
    with layer(c,(W*.25-(W/2)+(1-k)*-300,-60,1.0),1):pass
    c.restore()
    c.save();c.rectangle(0,0,W/2-6,H);c.clip();c.translate(W*.25-(1-k)*400,0)
    person(c,0,H-120,700,'wuemp',pose='stand',t=t,lean=.06,eyes='closed')
    petals(c,t,40,'#6a6460',.5,area=(-500,0,1000,H),spd=(20,60))
    c.restore()
    c.save();c.rectangle(W/2+6,0,W/2,H);c.clip()
    rect(c,W/2,0,W/2,H,'#3a1408');glow(c,W*.75,H*.4,600,'#ffb050',.45)
    for i in range(14):a_=i/14*6.28+t*.2;line(c,W*.75,H*.4,W*.75+math.cos(a_)*1200,H*.4+math.sin(a_)*1200,'#ffd080',30,.05)
    c.translate(W*.75+(1-k)*400,0);person(c,0,H-120,700,'kx',pose='point',face=-1,t=t,eyes='angry')
    c.restore()
    rect(c,W/2-6,0,12,H,'#d9b56a')
    for i,(x,lab,v,hh) in enumerate([(70,'吴三桂','62岁','#8a8580'),(W/2+80,'康熙','20岁',GOLD)]):
        counter(c,t,lab,[(bt(1+i*1.5),v)],x=x,y=110,h=hh)
    if t>bt(4):sc=slam(t,bt(4)) or 1;c.save();c.translate(W/2,H/2);c.scale(sc,sc);circ(c,0,0,90,RED);text(c,'VS',0,30,80,'#f3e6c8');c.restore()
sub(216,224,'{62岁}暮年老帅 vs {20岁}少年雄主')
@shot(224,230,'')
def f3(c,t,T):
    cam=seg(t,[(0,(0,-200,1.4)),(bt(6),(0,-60,.95))])
    with layer(c,cam,.1):rect(c,-3000,-2000,6000,4000,'#140806')
    with layer(c,cam,1):
        tilt=.05*math.sin(t*2)+ramp(t,bt(3),bt(6))*.06
        c.save();c.translate(0,-300);c.rotate(tilt)
        poly(c,[(-900,-80),(900,-80),(700,-260),(-700,-260)],'#2a1a14',1,INK,4)
        rect(c,-950,-80,1900,60,'#5a1a12')
        for x in (-700,700):rect(c,x-30,-20,60,700,'#3a1a12',.5)
        text(c,'大 周',0,-140,90,'#d9b56a',sp=20)
        c.restore()
        person(c,0,200,440,'wuemp',pose='raise',t=t,eyes='closed',arm=(-165,-195))
        rect(c,-1500,200,3000,900,'#0e0604')
        for i in range(30):
            r=random.Random(i);x=r.uniform(-900,900);ph=(t*.6+r.random())%1
            circ(c,x,-280+ph*700,r.uniform(2,6),'#8a6a4a',.6*(1-ph))
    stamp(c,t,bt(2.5),'一人苦撑',W*.76,H*.3,100)
sub(224,230,'整个政权，全靠他一人{威望死撑}')
LAZY=[(-700,'qb','stand'),(-420,'qy','cross'),(-140,'qr','kneel'),(160,'qb','stand'),(440,'qy','hold'),(720,'qr','cross')]
@shot(230,238,'八旗营')
def f4(c,t,T):
    if t<bt(4):
        cam=(seg(t,[(0,-200),(bt(4),100)]),-40,1.1)
        with layer(c,cam,.05):sky(c,'#2a2a3a','#8a7a6a',-800,100)
        with layer(c,cam,.4):
            for x in range(-1500,1600,400):tent(c,x,120,2,'#5a5a6a')
        with layer(c,cam,1):
            ground(c,200,'#4a4030','#141008')
            for x,k,p in LAZY:
                person(c,x,460,280,k,pose=p,t=t,eyes='closed',lean=.1*math.sin(t+x))
            for x in (-560,300):  # 鸟笼+酒坛
                line(c,x,200,x,140,'#2a1c10',3);ell(c,x,230,40,56,'#c9a86a',.0);col(c,'#8a6a3a');c.set_line_width(3);c.arc(x,240,40,0,7);c.stroke()
                circ(c,x,248,10,'#d9a82e')
                ell(c,x+120,430,40,50,'#6a3a1a')
        stamp(c,t,bt(1.5),'腐化',W*.75,H*.3,130)
    else:
        u=t-bt(4)
        cam=(0,-40,1.0+.05*u)
        with layer(c,cam,.05):sky(c,'#1a2024','#4a5a5a',-800,0)
        with layer(c,cam,.3):peaks(c,0,'#2a3a30','#1a2420',n=10,seed=4,hmin=300,hmax=600)
        with layer(c,cam,.7):
            rect(c,-2600,100,5200,800,'#2a4048')
            for k in range(40):x=(k*143-u*60)%4000-2000;line(c,x,140+(k*31)%300,x+80,140+(k*31)%300,'#a8c0c0',2,.4)
            for i,x in enumerate((-500,0,500)):
                sink=ramp(u,.3+i*.3,1.5+i*.3)
                c.save();c.translate(x,240+sink*80);c.rotate(sink*.4*(1 if i%2 else -1));ships(c,0,0,.7,u,sail='#3a5aa0',txt='旗');c.restore()
                for j in range(3):circ(c,x-60+j*60,320+sink*20,8,'#d8e0e0',.6*sink)
        stamp(c,u,bt(1.5),'水土不服',W*.72,H*.3,110)
sub(230,234,'而八旗兵早已{腐化}')
sub(234,238,'更打不了南方的{山地水战}')
@shot(238,246,'北京·乾清宫')
def f5(c,t,T):
    cam=seg(t,[(0,(-300,-60,1.2)),(bt(8),(150,-40,1.0))])
    with layer(c,cam,.1):rect(c,-3000,-2000,6000,4000,'#4a100c')
    with layer(c,cam,.5):
        for x in range(-1600,1700,260):rect(c,x-26,-800,52,1100,'#9a2418');rect(c,x-26,-800,10,1100,'#c8402a')
        rect(c,-2000,260,4000,800,'#2a1a10')
    with layer(c,cam,1):
        person(c,-600,380,360,'kx',pose='point',t=t,face=1,eyes='angry')
        for i,(x,n) in enumerate([(0,'张勇'),(330,'王进宝'),(660,'赵良栋')]):
            k=ramp(t,bt(1.2+i*1.3),bt(2+i*1.3))
            person(c,x+400*(1-k),380,340,'ggen',pose='hands' if False else ('raise' if k>=1 else 'stand'),face=-1,t=t,a=k)
    for i,(x,n) in enumerate([(0,'张勇'),(330,'王进宝'),(660,'赵良栋')]):
        tt=bt(2+i*1.3)
        sx=W/2+(x-150)*1.0+(-300+150)*0;badge(c,t,tt,W*.48+i*290,H*.2,n,'汉军绿营','#2a6a4a')
    stamp(c,t,bt(6),'打破满汉之防',W*.24,H*.2,80)
sub(238,246,'康熙打破满汉之防，重用{张勇、王进宝、赵良栋}')
GA=crowd(81,90,300,1800,160,460,['green','green','ggen'],('raise','hold'),60,160,faces=(-1,))
WA=crowd(82,90,-1800,-300,160,460,['wsol'],('raise','hold'),60,160,faces=(1,))
@shot(246,258,'1676—1680年')
def f6(c,t,T):
    clash=bt(3)
    k=ramp(t,0,clash)
    if t<bt(7):cam=seg(t,[(0,(0,-40,.9)),(clash,(0,-20,1.05)),(clash+.01,(0,40,1.35)),(bt(7),(80,60,1.45))])
    else:cam=seg(t,[(bt(7),(-150,120,2.0)),(bt(12),(-120,140,2.2))])
    with layer(c,cam,.05):sky(c,'#2a1410','#b0602a',-900,40);glow(c,0,-100,900,'#ff9a40',.3)
    with layer(c,cam,.25):peaks(c,40,'#3a2018','#24140e',n=9,seed=12)
    with layer(c,cam,.5):
        for x in (-1300,-500,700,1400):smoke(c,t,x,40,3,seed=x,a=.55)
        banners(c,[-1500,-1200,-900],80,260,t,'周','#efe9dc',1.2);banners(c,[900,1200,1500],80,260,t,'清','#2a6a4a',1.2)
    with layer(c,cam,1):
        ground(c,140,'#4a2a18','#120804')
        off=(1-k)*500
        draw_crowd(c,WA,t,dx=-off+k*100,march=1.4 if t<clash else .6,bob=10)
        draw_crowd(c,GA,t,dx=off-k*100,march=1.4 if t<clash else .6,bob=10)
        dust(c,t,-900,900,470,50,colr='#9a6a40',a=.4,s=2)
        if t>clash:
            for i in range(10):
                r=random.Random(i);x=r.uniform(-500,500);y=r.uniform(250,450);ph=(t*3+i)%1
                line(c,x-60,y-60*ph,x+60,y-120+60*ph,'#e8e8f0',4,.8*(1-ph))
        # 主将对决
        if t>bt(7):
            u=t-bt(7);a1=math.sin(u*9)
            person(c,-130,440,300,'wum',pose='raise' if a1>0 else 'point',face=1,t=t,eyes='angry')
            person(c,130,440,300,'ggen',pose='point' if a1>0 else 'raise',face=-1,t=t,eyes='angry')
            line(c,-60,240+a1*30,90,200-a1*40,'#e8e8f0',6);line(c,60,230-a1*30,-80,200+a1*40,'#c8c8d0',6)
            if a1>.95:glow(c,0,220,120,'#fff4c0',.8)
    arrows(c,t,.2,120,seed=2,src=(1200,-200),dst=(-500,400),spread=600,dur=1.6)
    arrows(c,t,1.0,120,seed=5,src=(-1200,-200),dst=(500,400),spread=600,dur=1.6)
    embers(c,t,60,area=(0,0,W,H))
    stamp(c,t,bt(4.5),'以汉制汉',W/2,H*.24,130)
sub(246,252,'绿营汉将对汉人军阀，{知根知底}')
sub(252,258,'直接抽干了吴三桂{唯一的军事优势}')
@shot(258,264,'1676—1680年')
def f7(c,t,T):
    sc=G.basemap(c,108,30,.72,t)
    for p,tt in (('陕甘',.5),('四川',2),('湖南',3.5),('广西',3.8),('贵州',4.5)):
        k=ramp(t,bt(tt),bt(tt+.6));G.zone(c,G.PROV[p],RED,.6*(1-k),sc);G.zone(c,G.PROV[p],GOLD,k,sc)
    G.zone(c,G.PROV['云南'],RED,.8,sc)
    G.route(c,[(108.94,34.27),(106.67,35.54)],ramp(t,0,bt(1)),sc,GOLD,6,arrow=True)
    G.route(c,[(106.5,33.5),(104.07,30.67)],ramp(t,bt(1.5),bt(2.5)),sc,GOLD,6,arrow=True)
    G.route(c,[(112.2,30.33),(113.13,29.37),(112.94,28.23),(112.57,26.9)],ramp(t,bt(3),bt(4.5)),sc,GOLD,6,arrow=True)
    G.city(c,'昆明',sc,t,'red',pulse=1);[G.city(c,n,sc,t) for n in ('西安','成都','长沙','衡阳','岳州')]
    G.endmap(c)
sub(258,264,'西北、四川、湖南，被清军{逐一收复}')
# ================= 盲区五 国力悬殊 =================
@shot(264,268)
def g1(c,t,T):chapter2(c,t,5,'国力悬殊','西南穷省 vs 天下粮仓')
@shot(268,274,'')
def g2(c,t,T):
    rect(c,0,0,W,H,'#1a120c');glow(c,W/2,H/2,700,'#5a3a1a',.4)
    tilt=ramp(t,bt(1),bt(3))*.22+math.sin(t*3)*.01
    cx,cy=W/2,H*.32
    rect(c,cx-14,cy,28,H*.5,'#5a3a1a');poly(c,[(cx-200,H*.82),(cx+200,H*.82),(cx+120,H*.76),(cx-120,H*.76)],'#5a3a1a')
    c.save();c.translate(cx,cy);c.rotate(tilt)
    rect(c,-560,-10,1120,20,'#8a6a3a')
    for sx,lab,n,colr in ((-1,'云贵川湘',2,RED),(1,'北方+江南',6,GOLD)):
        c.save();c.translate(sx*540,0);c.rotate(-tilt)
        line(c,-120,200,0,0,'#c8b48a',2);line(c,120,200,0,0,'#c8b48a',2)
        ell(c,0,210,170,30,'#6a4a2a')
        for i in range(n):
            x=(i%3-1)*90;y=170-(i//3)*80;ell(c,x,y,46,52,'#c8a86a',1);text(c,'粮' if sx>0 else '银',x,y+14,36,'#5a3a1a')
        text(c,lab,0,300,50,colr);c.restore()
    c.restore()
    if t>bt(.5):text(c,'拼的是 钱袋子',W/2,H*.13,60,'#f3e6c8',cl((t-bt(.5))*3),sp=8)
sub(268,274,'下半场，拼的不是猛将，是{钱袋子}')
@shot(274,282,'')
def g3(c,t,T):
    sc=G.basemap(c,114,32,.62,t,regions=[('江 南',(118.5,31),1),('直 隶',(115.5,38),1)])
    G.zone(c,G.QING,GOLD,ramp(t,0,bt(1)),sc)
    G.zone(c,G.JIANGNAN,GOLD,ramp(t,bt(1),bt(2)),sc,dash=False)
    for p in ('云南','贵州','四川','湖南'):G.zone(c,G.PROV[p],RED,.6,sc)
    pts=list(reversed(G.CANAL))
    for i in range(8):
        k=((t*.18+i/8)%1);xy=[G.P(*p) for p in pts];L=len(xy)-1;f=k*L;j=int(f);r=f-j
        x=lerp(xy[j][0],xy[min(j+1,L)][0],r);y=lerp(xy[j][1],xy[min(j+1,L)][1],r)
        rect(c,x-16*sc,y-10*sc,32*sc,20*sc,'#c8a86a');text(c,'粮',x,y+7*sc,16*sc,'#5a3a1a')
    G.city(c,'北京',sc,t,pulse=1,big=1.4);G.city(c,'江宁',sc,t);G.city(c,'杭州',sc,t)
    G.endmap(c)
    counter(c,t,'清廷财源',[(bt(2),'漕运不断')],note='江浙皖赋税重地')
sub(274,282,'清朝握住北方与{江南赋税}，漕运不断，越打越稳')
VIL=crowd(91,14,-1100,1100,330,440,['farm','farmw'],('cower','stand'),110,160,faces=(-1,1))
@shot(282,292,'吴军占领区')
def g4(c,t,T):
    cam=seg(t,[(0,(-200,-40,1.0)),(bt(5),(100,-40,1.1)),(bt(5.01),(0,40,1.4)),(bt(10),(60,60,1.5))])
    burn=ramp(t,bt(4),bt(6))
    with layer(c,cam,.05):sky(c,'#2a1a14',clib_mix2('#8a6a4a','#c04a1a',burn),-800,80)
    with layer(c,cam,.3):ridge(c,40,'#2a2018',amp=60,seed=6)
    with layer(c,cam,.7):
        for i,x in enumerate((-1100,-650,-200,250,700,1150)):house(c,x,220,260,130,burn=burn if i%2 else 0)
        for i,x in enumerate((-650,250,1150)):
            if burn>0:fire(c,x,90,2*burn,t,seed=i);smoke(c,t,x,40,2.5,seed=i,a=.6*burn)
    with layer(c,cam,1):
        ground(c,240,'#4a3a26','#120c06')
        for d in VIL:person(c,d['x'],d['y']+40,d['h']*1.3,d['kind'],pose='cower' if t>bt(1) else 'stand',face=d['face'],t=t)
        for i,x in enumerate((-500,0,500)):
            dx=math.sin(t*2+i)*30
            person(c,x+dx,500,260,'wsol',pose='point',face=1 if i%2 else -1,t=t,eyes='angry')
            rect(c,x+dx+60,380,70,80,'#c8a86a');text(c,'粮',x+dx+95,435,40,'#5a3a1a')
        rope=ramp(t,bt(5.5),bt(8))
        for j in range(4):person(c,-900+rope*900+j*90,480,220,'farm',pose='stand',face=1,t=t,bound=True)
        line(c,-900+rope*900,370,-900+rope*900+270,370,'#a88a5a',3)
    embers(c,t,int(60*burn),area=(0,0,W,H))
    stamp(c,t,bt(6.5),'民心尽失',W*.74,H*.28,110)
def clib_mix2(a,b,k):
    A=hx(a);B_=hx(b);return '#%02x%02x%02x'%tuple(int(255*lerp(A[i],B_[i],cl(k))) for i in range(3))
sub(282,287,'吴三桂困在{云贵川湘}，人少、底子薄')
sub(287,292,'只能{横征暴敛}、强抓壮丁，把民心彻底逼反')
@shot(292,300,'1678年8月·衡阳')
def g5(c,t,T):
    out=t>bt(5)
    cam=seg(t,[(0,(0,-40,1.0)),(bt(5),(-80,0,1.35))])
    fl=(.8+.2*math.sin(t*13))*(0 if out else 1)
    with layer(c,cam,1):
        rect(c,-2000,-1200,4000,2400,'#0e0806');glow(c,320,0,800,'#ffa040',.3*fl)
        rect(c,-600,140,1000,120,'#4a1a12');rect(c,-620,60,40,200,'#3a120c')
        rect(c,-560,90,900,60,'#e8dcc0',.85)
        person(c,-460,130,300,'wuemp',pose='fall',face=-1,t=0,eyes='closed')
        rect(c,280,40,80,200,'#2a1a10');rect(c,305,-30,30,70,'#e8dcc0')
        if not out:
            x=320;y=-40;c.move_to(x,y-60-6*math.sin(t*17));c.curve_to(x+14,y-30,x+10,y-16,x,y-14);c.curve_to(x-10,y-16,x-14,y-30,x,y-60-6*math.sin(t*17));col(c,'#ffc060');c.fill()
            glow(c,x,y-36,90,'#ffd080',.7)
        else:
            u=t-bt(5);
            for i in range(5):r=random.Random(i);circ(c,320+math.sin(u*2+i)*20*u,-60-u*80-i*30,14+u*10,'#5a5a5a',max(0,.5-u*.2))
        rect(c,-2000,260,4000,1000,'#080504')
    if out:rect(c,0,0,W,H,'#000000',.4)
    stamp(c,t,bt(5.3),'病逝',W*.72,H*.3,130)
sub(292,300,'1678年，心力交瘁的吴三桂在衡阳{病死}，称帝仅五个月')
@shot(300,308,'1681年·昆明')
def g6(c,t,T):
    cam=seg(t,[(0,(0,60,1.25)),(bt(8),(0,0,.95))])
    with layer(c,cam,.05):sky(c,'#1a0806','#c0401a',-900,0)
    with layer(c,cam,.3):
        for x in (-1200,-500,300,1100):smoke(c,t,x,-100,3.5,seed=x,a=.7)
    with layer(c,cam,.6):
        citywall(c,-2200,2200,-120,300);gatetower(c,0,-120,300,1,name='昆明',gate_open=1)
        for x in (-1300,-700,600,1200):fire(c,x,-120,2,t,seed=x)
        banners(c,[-900,-600,600,900],-120,180,t,'清','#d9b04a')
    with layer(c,cam,1):
        ground(c,300,'#3a1e14','#0a0604')
        if t<bt(4):person(c,0,330,260,'wsf',pose='stand',t=t,eyes='closed')
        else:
            draw_crowd(c,crowd(95,60,-1400,1400,320,480,['qb','qy','green'],('raise','hold'),70,150),t,march=1)
    embers(c,t,90,area=(0,0,W,H))
    if t<bt(4):badge(c,t,.3,W*.75,H*.3,'吴世璠','吴三桂之孙',RED)
    stamp(c,t,bt(5),'三藩平定',W/2,H*.26,130)
sub(300,304,'十几岁的孙子{吴世璠}仓促接班')
sub(304,308,'1681年昆明城破，{三藩之乱}落幕')
# ================= 结尾 =================
@shot(308,316,'')
def z1(c,t,T):
    sc=G.basemap(c,108,28.5,.72,t,dim=.3)
    G.endmap(c)
    cx,cy=W*.4,H*.58;r=lerp(160,420,ramp(t,0,bt(5)))+math.sin(t*6)*6
    pop_=t>bt(5.5)
    if not pop_:
        g=cairo.RadialGradient(cx-r*.3,cy-r*.3,r*.1,cx,cy,r);g.add_color_stop_rgba(0,1,.8,.7,.35);g.add_color_stop_rgba(.8,.75,.2,.15,.25);g.add_color_stop_rgba(1,.9,.3,.2,.6);c.set_source(g);c.arc(cx,cy,r,0,7);c.fill()
        ell(c,cx-r*.4,cy-r*.45,r*.2,r*.1,'#ffffff',.5)
        text(c,'十省江山',cx,cy+20,70,'#f3e6c8')
    else:
        u=t-bt(5.5)
        for i in range(40):
            a_=i/40*6.28;d=r+u*900;circ(c,cx+math.cos(a_)*d,cy+math.sin(a_)*d,10*(1-u),'#e88a6a',max(0,1-u))
        stamp(c,t,bt(5.6),'泡沫',cx,cy,170)
sub(308,316,'十省江山，本质是趁对手不备吹起来的{战略泡沫}')
@shot(316,326,'')
def z2(c,t,T):
    rect(c,0,0,W,H,'#120c08');k=eo(t/.6)
    rect(c,W/2-700*k,140,1400*k,700,'#e8dcbc');rect(c,W/2-700*k-24,120,24,740,'#5a3a1a');rect(c,W/2+700*k,120,24,740,'#5a3a1a')
    if k<.95:return
    for i,(a_,b_) in enumerate([('政治上','失尽人心'),('战略上','首鼠两端'),('格局上','只想偏安')]):
        tt=bt(.5+i*2.8);
        if t<tt:continue
        y=280+i*200;circ(c,W/2-520,y-14,14,RED)
        text(c,a_,W/2-470,y,52,'#5a4a3a',cl((t-tt)*4),align='l')
        bigword(c,t,tt+bt(.6),b_,W/2+180,y-18,110,RED)
    stamp(c,t,bt(9),'吴',W/2+560,760,80)
sub(316,326,'他这一生：政治上{失尽人心}，战略上{首鼠两端}，格局上{只想偏安}')
@shot(326,334,'')
def z3(c,t,T):
    cam=seg(t,[(0,(0,-60,1.25)),(bt(8),(0,-40,1.0))])
    with layer(c,cam,.05):sky(c,'#1a0c08','#c0502a',-900,100);circ(c,200,40,170,'#ff9a50',.95);glow(c,200,40,600,'#ff9050',.4)
    with layer(c,cam,.4):rect(c,-3000,100,6000,400,'#2a2a30');[line(c,(k*157)%3000-1500,140+(k*23)%200,(k*157)%3000-1420,140+(k*23)%200,'#ffb070',3,.4) for k in range(40)]
    with layer(c,cam,1):
        poly(c,[(-2000,300),(-200,280),(100,600),(-2000,700)],'#0a0604')
        person(c,-420,300,380,'wuemp',pose='stand',face=1,t=t,eyes='closed')
        c.save();c.translate(-420,300);col(c,'#000000',.85);c.restore()
        # 剪影：在人物上盖黑
    rect(c,0,0,W,H,'#000000',.0)
    if t>bt(1):bigword(c,t,bt(1),'投机者',W*.7,H*.3,140,'#f3e6c8')
sub(326,330,'历史从不怜悯{投机者}')
sub(330,334,'不敢押上全部筹码去赢，你就{已经开始输了}')
@shot(334,346,'1674年·岳州')
def z4(c,t,T):
    z=seg(t,[(0,1.1),(bt(12),.68)]);cx=seg(t,[(0,(113.1,29.5)),(bt(12),(114.5,33.5))])
    sc=G.basemap(c,cx[0],cx[1],z,t)
    G.zone(c,G.PROV['湖南'],RED,.6,sc)
    G.city(c,'岳州',sc,t,'red',pulse=1,big=1.5)
    k=ramp(t,bt(1),bt(7))
    G.route(c,[(113.13,29.37),(114.3,30.55),(114.6,34.5),(116.4,39.9)],k,sc,GOLD,7,dash=True,arrow=k>=1)
    G.city(c,'北京',sc,t,pulse=1,big=1.4);G.city(c,'武昌',sc,t)
    G.endmap(c)
    if t>bt(7):bigword(c,t,bt(7),'？',W*.78,H*.4,300,RED)
sub(334,340,'如果当年他没停在岳州，而是{直接渡江北上}')
sub(340,346,'中国历史，会彻底改写吗？','评论区聊聊')
