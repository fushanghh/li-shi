from base import *
CN=['','一','二','三','四','五']
def chapter2(c,t,n,title,sub_):
    rect(c,0,0,W,H,'#0d0907')
    for i in range(16):
        k=eo(t*2.4-i*.04);col(c,'#2a1c12',.55);c.set_line_width(90);c.move_to(-300+i*150,H+120);c.line_to(-300+i*150+700*k,H+120-1400*k);c.stroke()
    glow(c,W*.3,H/2,560,'#c0392b',.28)
    sc=slam(t,0,.22) or 1
    c.save();c.translate(W*.3,H/2);c.scale(sc,sc);text(c,str(n),0,150,440,'#c0392b',.92);c.restore()
    text(c,'致命盲区 · 其'+CN[n],W*.63,H/2-130,40,GREY,cl(t*3),sp=12)
    bigword(c,t,.3,title,W*.63,H/2-10,160)
    if t>.8:text(c,sub_,W*.63,H/2+120,44,'#c8b48a',cl((t-.8)*3),sp=6)
# ================= 钩子 =================
WSOL=['wsol','wsol','wsol','wum']
ARMY=crowd(11,150,-1500,1500,40,420,['wsol'],('stand','hold','raise'),40,150)
@shot(0,8,'1673年·云南')
def h1(c,t,T):
    cam=seg(t,[(0,(0,-40,1.0)),(4.8,(60,0,1.12))])
    with layer(c,cam,.05):sky(c,'#2a1410','#d8783a',-700,120);glow(c,300,-80,520,'#ffb060',.5);circ(c,300,-60,120,'#ffd08a',.9)
    with layer(c,cam,.2):peaks(c,60,'#3a1e16','#2a140e',n=9,seed=3,hmin=220,hmax=420)
    with layer(c,cam,.4):ridge(c,90,'#2a160e',amp=50,seed=2);clouds(c,t,'#ffb080',.12,8,4,(-300,-120))
    with layer(c,cam,.8):
        ground(c,40,'#3a2216','#120a06')
        banners(c,[-1300,-1000,-700,-400,300,600,900,1200],60,260,t,'吴','#e8e0cc',1.1)
        draw_crowd(c,ARMY,t,march=.6)
        dust(c,t,-1500,1500,420,40,seed=2,colr='#a0603a',a=.25,s=1.5)
    with layer(c,cam,1.0):
        horse(c,-40,520,300,1,t,gallop=.0,col_='#2a1c14',rider='wum')
    embers(c,t,40,area=(0,0,W,H),colr='#ffcc80',a=.5)
@shot(8,16,'平西王')
def h2(c,t,T):
    ash=ramp(t,bt(4),bt(7.5))
    cam=seg(t,[(0,(0,-120,1.25)),(bt(8),(0,-200,1.6))])
    g1='#5a1810' if ash<1 else '#2a2a2a'
    with layer(c,cam,.05):sky(c,clib_mix('#3a1410','#1a1a1c',ash),clib_mix('#c0502a','#4a4644',ash),-900,200)
    with layer(c,cam,.3):peaks(c,120,clib_mix('#2a120c','#222222',ash),'#141414',n=8,seed=5)
    with layer(c,cam,1.0):
        ground(c,140,clib_mix('#3a2016','#2a2828',ash),'#0a0a0a')
        person(c,0,820,900,'wu',pose='stand',t=t,a=1-ash*.9,eyes='angry',cape_wind=6)
        r=random.Random(3)
        for i in range(260):
            st=r.uniform(0,1);x0=r.uniform(-160,160);y0=r.uniform(-100,800)
            k=cl((ash-st*.6)/.4)
            if k<=0:continue
            circ(c,x0+k*r.uniform(200,900),y0-k*r.uniform(200,700),r.uniform(2,6),r.choice(['#8a8580','#c8c0b8','#5a5450','#ff9a50']),.9*(1-k*.7))
    petals(c,t,50,'#9a948e',.5*ash,area=(0,0,W,H),spd=(-80,-30))
def clib_mix(a,b,k):
    A=hx(a);B_=hx(b);return '#%02x%02x%02x'%tuple(int(255*lerp(A[i],B_[i],cl(k))) for i in range(3))
@shot(16,24,'')
def h3(c,t,T):
    sc=G.basemap(c,108,30,.7,t,dim=.55)
    G.endmap(c)
    for i in range(5):
        x=W/2+(i-2)*300;y=H/2+40;k=pop(t,bt(4+i*.8),.3)
        if k<=0:circ(c,x,y,100,'#1a120c',.8);continue
        glow(c,x,y,200,RED,.4*k);circ(c,x,y,100*k,'#2a0c08',.95);col(c,RED,1);c.set_line_width(6);c.arc(x,y,100*k,0,7);c.stroke()
        text(c,str(i+1),x,y+38*k,110*k,'#f3e6c8')
# ================= 片名 =================
@shot(24,30,'1673年·云南')
def ti(c,t,T):
    z=seg(t,[(0,.75),(bt(6),.95)])
    sc=G.basemap(c,106,28,z,t,regions=[('云南',(101,24.5),1),('湖南',(111.5,27.5),1)])
    k=ramp(t,.2,1.2)
    G.zone(c,G.PROV['云南'],RED,k,sc)
    G.city(c,'昆明',sc,t,'red',pulse=1);G.city(c,'北京',sc,t)
    G.endmap(c)
    stamp(c,t,bt(1),'三藩之乱',W/2,H/2-40,150,-.04)
    if t>bt(3):text(c,'1673 — 1681',W/2,H/2+120,56,GOLD,cl((t-bt(3))*3),sp=14)
for x in [(24,30,'复盘这场赌上国运的{三藩之乱}')]:sub(*x)
# ================= 盲区一 信用破产 =================
@shot(30,34)
def c1(c,t,T):chapter2(c,t,1,'信用破产','反复横跳的小丑')
@shot(34,40,'')
def c2(c,t,T):
    cam=seg(t,[(0,(0,0,1.0)),(bt(6),(0,-40,1.15))])
    with layer(c,cam,.1):sky(c,'#1a0e0a','#2a1810',-700,400)
    with layer(c,cam,.5):
        for x in (-700,-350,350,700):rect(c,x-30,-500,60,900,'#6e1c16');rect(c,x-30,-500,8,900,'#a8302a')
        rect(c,-900,380,1800,400,'#1e140e')
    with layer(c,cam,1):
        k=ramp(t,.3,1.2);glow(c,0,-120,500,GOLD,.35*k)
        rect(c,-320,-300,640,190,'#1a120c',k);rect(c,-300,-284,600,158,'#d9b56a',k)
        text(c,'名 正 言 顺',0,-180,90,'#1a120c',k,sp=12)
        for i,x in enumerate((-500,-250,250,500)):
            fl=.8+.2*math.sin(t*11+i);rect(c,x-12,200,24,120,'#e8dcc0');glow(c,x,180,80,'#ffc060',.6*fl);circ(c,x,182,10,'#ffd080')
    bigword(c,t,bt(2),'名分',W/2,H*.72,170)
sub(34,40,'造反的第一生产力，是{名分}')
QWAVE=crowd(21,90,-1600,600,120,420,['qb','qr','qy','qb'],('stand','hold'),50,150)
@shot(40,52,'1644年·山海关')
def c3(c,t,T):
    cam=seg(t,[(0,(0,-60,1.0)),(bt(6),(0,-60,1.0)),(bt(6.01),(-200,0,1.35)),(bt(12),(-120,0,1.45))])
    op=ramp(t,bt(.5),bt(3))
    with layer(c,cam,.05):sky(c,'#141826','#5a4a50',-800,100);clouds(c,t,'#2a2a3a',.6,10,3,(-500,-200))
    with layer(c,cam,.25):ridge(c,40,'#1e1e26',amp=90,seed=4)
    with layer(c,cam,.6):
        citywall(c,-2000,2000,-180,260);gatetower(c,0,-180,260,1.1,name='天下第一关',gate_open=op)
        banners(c,[-600,-450,450,600],-180,170,t,'明' if t<bt(6) else '清','#c0392b' if t<bt(6) else '#d9b04a')
    with layer(c,cam,1):
        ground(c,260,'#2a2420','#0c0a08')
        if t>bt(2.5):
            k=t-bt(2.5);draw_crowd(c,QWAVE,t,dx=-200+k*420,march=1.2,a=cl(k*2))
            dust(c,t,-800,800,420,30,colr='#6a5a4a',a=.3,s=1.6)
        person(c,520,470,300,'wu44',pose='kneel' if t>bt(6) else 'stand',face=-1,t=t)
        if t>bt(7):
            k=cl((t-bt(7))/.6)
            c.save();c.translate(520,470-300*.86);col(c,'#15100c',k);c.set_line_width(9);c.move_to(16,0);c.curve_to(40,40,44,80,54,120);c.stroke();c.restore()
    stamp(c,t,bt(3.5),'开关降清',W*.24,H*.62,110,.05)
sub(40,46,'1644年，他打开{山海关}，放清军入关')
sub(46,52,'剃发留辫，替清廷{追亡逐北}')
@shot(52,64,'1662年·昆明')
def c4(c,t,T):
    if t<bt(7):
        cam=seg(t,[(0,(0,-40,1.0)),(bt(7),(80,-20,1.15))])
        with layer(c,cam,.05):sky(c,'#06080e','#1a2030',-800,200)
        with layer(c,cam,.3):ridge(c,60,'#0e1218',amp=80,seed=7)
        with layer(c,cam,1):
            ground(c,160,'#1a1c20','#060708')
            for x in (-700,-560,560,700):
                line(c,x,420,x,250,'#2a1c10',6);fire(c,x,250,.7,t,seed=x)
            person(c,-80,470,330,'yongli',pose='kneel',face=1,t=t,eyes='closed')
            person(c,320,470,360,'wu',pose='point',face=-1,t=t,eyes='angry')
            for i,x in enumerate((480,560,640,720)):person(c,x,470,300,'qb',pose='hold',face=-1,t=t)
            rain(c,t,dens=300,area=(-1100,-650,2200,1300))
    else:
        u=t-bt(7)
        cam=(0,0,1+.08*u)
        with layer(c,cam,1):
            rect(c,-1000,-600,2000,1200,'#0a0806')
            k=ramp(u,0,1.6)
            # 弓弦特写：两手拉紧
            for sx in(-1,1):
                x=sx*(240+160*k);ell(c,x,0,70,44,'#ecd0a8');poly(c,[(x+sx*40,-30),(x+sx*400,-60),(x+sx*400,60),(x+sx*40,30)],'#5a1a14')
            col(c,'#e8dcc0');c.set_line_width(5);c.move_to(-240-160*k,0);c.curve_to(-80,40*(1-k),80,40*(1-k),240+160*k,0);c.stroke()
            glow(c,0,0,300,RED,.3*k)
        if u>1.4:rect(c,0,0,W,H,'#ffffff',.6*max(0,1-(u-1.4)/.2))
    if t>bt(9.5):stamp(c,t,bt(9.5),'弑主',W*.5,H*.42,170,-.05)
sub(52,58,'1662年，他从缅甸抓回南明{永历帝}')
sub(58,64,'在昆明下令，用{弓弦}将其勒死','《清史稿·吴三桂传》')
WHITE=crowd(31,160,-1700,1700,60,420,['wsol'],('raise','hold','stand'),40,150)
@shot(64,76,'1673年·昆明')
def c5(c,t,T):
    if t<bt(4):
        cam=(0,0,1+.05*t)
        with layer(c,cam,1):
            rect(c,-1000,-600,2000,1200,'#1a0e0a');glow(c,0,0,700,'#8a3a1a',.4)
            # 辫子+刀特写
            cut=t>bt(2.2);fall=max(0,t-bt(2.2))
            ell(c,-300,-200,260,300,'#15100c')
            col(c,'#15100c');c.set_line_width(46)
            c.move_to(-200,-20);c.curve_to(-120,120,-100,240,-80,300);c.stroke()
            if cut:
                c.save();c.translate(0,fall*fall*900);c.rotate(fall*.8)
                col(c,'#15100c');c.set_line_width(46);c.move_to(-80,300);c.curve_to(-60,420,-40,520,-20,620);c.stroke();circ(c,-20,630,20,RED)
                c.restore()
            else:
                col(c,'#15100c');c.set_line_width(46);c.move_to(-80,300);c.curve_to(-60,420,-40,520,-20,620);c.stroke();circ(c,-20,630,20,RED)
            kx=seg(t,[(0,600),(bt(2),200),(bt(2.3),-300)])
            poly(c,[(kx-200,290),(kx+260,270),(kx+280,300),(kx-200,320)],'#c8ccd0',1,INK,3);rect(c,kx+270,268,140,40,'#5a3a1a')
            if bt(2.2)<t<bt(2.5):line(c,-400,300,400,300,'#ffffff',6,1-(t-bt(2.2))/(bt(.3)))
        counter(c,t,'起兵时 吴三桂',[(bt(.5),'62岁')],note='康熙下令撤藩')
    else:
        u=t-bt(4)
        cam=seg(u,[(0,(0,-80,1.3)),(bt(8),(0,-40,1.0))])
        with layer(c,cam,.05):sky(c,'#3a1610','#e09050',-800,120);circ(c,0,-40,140,'#ffe0a0',.9);glow(c,0,-40,600,'#ffb060',.5)
        with layer(c,cam,.3):peaks(c,60,'#4a2418','#301810',n=10,seed=9)
        with layer(c,cam,.8):
            ground(c,40,'#4a2a18','#140a06')
            banners(c,[-1400,-1100,-800,-500,500,800,1100,1400],60,280,u,'兴明','#efe9dc',1.1)
            draw_crowd(c,WHITE,u,bob=8)
        with layer(c,cam,1):person(c,0,480,420,'wum',pose='raise',t=u,eyes='angry',cape_wind=10)
        bigword(c,u,bt(1.5),'反清复明',W/2,H*.24,150,'#f3e6c8')
sub(64,70,'{62岁}那年，康熙要撤他的藩')
sub(70,76,'他剪掉辫子，突然高喊{“反清复明”}')
SCH=crowd(41,40,-1000,1000,100,360,['sch','off','sch'],('stand','cross','point'),90,190)
@shot(76,82,'')
def c6(c,t,T):
    cam=seg(t,[(0,(-80,-30,1.05)),(bt(6),(80,-30,1.15))])
    with layer(c,cam,.1):sky(c,'#2a2018','#4a3a28',-700,200)
    with layer(c,cam,.5):
        for x in range(-1200,1300,300):rect(c,x,-400,40,600,'#3a2a20')
        rect(c,-1500,180,3000,600,'#2a2018')
    with layer(c,cam,1):
        for d in SCH:
            sh=math.sin(t*9+d['ph'])*.08 if t>bt(1) else 0
            person(c,d['x'],d['y']+120,d['h']*1.6,d['kind'],pose=d['pose'],face=1 if d['x']<0 else -1,t=t,lean=sh)
    for i,(s_,x,y) in enumerate([('开关的是你',W*.22,H*.28),('杀明帝的也是你',W*.74,H*.32)]):
        if t>bt(1+i*1.4):text(c,s_,x,y,64,'#f3e6c8',cl((t-bt(1+i*1.4))*4))
    stamp(c,t,bt(4),'荒唐',W/2,H*.5,190)
sub(76,82,'天下汉人精英只觉得{荒唐}')
@shot(82,90,'1678年·衡阳')
def c7(c,t,T):
    cam=seg(t,[(0,(0,-60,1.0)),(bt(4),(0,-120,1.2)),(bt(8),(0,-160,1.3))])
    with layer(c,cam,.1):rect(c,-2000,-1500,4000,3000,'#3a0e0a')
    with layer(c,cam,.5):
        for x in range(-1100,1200,220):rect(c,x-26,-600,52,900,'#8a2018');rect(c,x-26,-600,10,900,'#c0392b')
        for x in (-500,500):line(c,x,-500,x,-300,'#1a120c',3);ell(c,x,-270,40,56,'#d84a2a');glow(c,x,-270,120,'#ffb060',.4)
    with layer(c,cam,1):
        rect(c,-260,0,520,200,'#5a2014');poly(c,[(-200,0),(200,0),(160,-260),(-160,-260)],'#d9a82e',1,INK,3)
        rect(c,-700,200,1400,600,'#2a0e0a')
        for k in range(5):rect(c,-300+k*30,200+k*36,600-k*60,36,'#7a1f1a');rect(c,-300+k*30,200+k*36,600-k*60,5,'#c0392b')
        person(c,0,40,260,'wuemp',pose='raise',t=t)
        # 撕开的复明旗
        rk=ramp(t,bt(4.5),bt(6))
        for sx in (-1,1):
            c.save();c.translate(sx*(560+rk*120),-160);c.rotate(sx*rk*.35)
            rect(c,-80 if sx<0 else 0,-200,80,400,'#efe9dc',1-rk*.4);clib.vtext(c,'复' if sx<0 else '明',-40 if sx<0 else 40,-120,64,'#1a120c',1-rk*.4)
            c.restore()
    if t>bt(1):
        sc=slam(t,bt(1)) or 1;c.save();c.translate(W*.5,H*.24);c.scale(sc,sc);rect(c,-90,-90,180,180,'#d9a82e',.95);text(c,'周',0,52,150,'#7a1f1a');c.restore()
sub(82,86,'1678年，他干脆在衡阳{称帝}，国号{大周}')
sub(86,90,'连“复明”这块{遮羞布}也亲手撕了')
@shot(90,96,'')
def c8(c,t,T):
    z=seg(t,[(0,1.4),(bt(6),.8)])
    with layer(c,(0,-60,z),1):
        rect(c,-3000,-2000,6000,4000,'#1a0806')
        for x in range(-2000,2100,260):rect(c,x-22,-900,44,1200,'#3a1210')
        rect(c,-3000,200,6000,1200,'#120604')
        poly(c,[(-140,40),(140,40),(110,-160),(-110,-160)],'#7a5a1a',1,INK,2)
        person(c,0,60,200,'wuemp',pose='stand',t=t,eyes='closed')
        glow(c,0,-60,300,'#d9a82e',.15)
    stamp(c,t,bt(2),'失道寡助',W/2,H*.32,140)
sub(90,96,'失道寡助，只能做{军阀}，成不了{天下共主}')
