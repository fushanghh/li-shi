from common import *
TANG_REG=[('关 中',(108.6,35.4,1)),('河 南',(114,34.9,.9)),('江 南',(118,29.5,.9)),('岭 南',(111,24.2,.9)),('山 东',(117.2,36.8,.9)),('蜀',(103.8,31.6,.8))]
CR_EXAM=crowd_grid(51,26,-900,900,250,300,['scholar','tangoff2','scholar'],['cheer','stand','hands','stand2'],150,190,[None])
def s_salt(c,t,T):
    if t<2.1:
        cam=(lerp(-150,100,t/2.1),-30,lerp(1.0,1.1,t/2.1))
        with layer(c,cam,.05):sky(c,'#2a2418','#8a7450',-800,200)
        with layer(c,cam,.2):clouds(c,t,'#6a5a40',.4,8,4,(-450,-200),10)
        with layer(c,cam,.3):peaks(c,140,'#5a4a34','#463826',8,3,140,280)
        with layer(c,cam,.6):
            ridge(c,180,'#4a3c28',30,8)
            for i,x in enumerate(range(-2000,2200,300)):tree(c,x,190,1,'#3a3a24','#2a2014','willow' if i%2 else 'round',t=t)
            # salt flats / white heaps
            for i in range(6):poly(c,[(-1200+i*450,230),(-1120+i*450,180),(-1040+i*450,230)],'#e8e2d0',.9)
        with layer(c,cam,1):
            ground(c,240,'#6a5838','#2a2010')
            x0=-200+t*90
            # cart with sacks
            poly(c,[(x0-140,250),(x0+60,250),(x0+60,200),(x0-140,200)],'#5a3a20',1,INK,2)
            for k in range(4):ell(c,x0-110+k*48,185,30,22,'#e0d8c0',1)
            circ(c,x0-40,280,40,INK);circ(c,x0-40,280,34,'#3a2a1a')
            person(c,x0+120,300,330,'salt',walk(t*.9),1,'calm',weapon=None)
            person(c,x0-300,300,300,'hsol2',walk(t*.9+.3),1,'calm',weapon='spear')
            person(c,x0+330,300,300,'farmer',walk(t*.9+.6),1,'calm',weapon='bundle')
        with layer(c,cam,1.4):reeds(c,-1500,1500,560,t,'#2a2414',60,3,200)
        return
    tt=t-2.1
    cam=seg(tt,[(0,(0,-60,1.0)),(.8,(0,-60,1.0)),(1.9,(-330,-330,2.6))])
    with layer(c,cam,.05):sky(c,'#1a1a1e','#4a4a50',-800,200)
    with layer(c,cam,.4):
        # exam wall (贡院)
        citywall(c,-1600,1600,-260,260,'#7a2a1c','#5a1c12')
        poly(c,[(-1700,-280),(1700,-280),(1600,-340),(-1600,-340)],'#1a1412')
        rect(c,-520,-200,1040,380,'#e8dcc0');rect(c,-520,-200,1040,50,'#7a1f1a')
        text(c,'进 士 榜',0,-162,34,'#f2d48a',sp=10)
        r=random.Random(5)
        for col_ in range(20):
            for row in range(8):rect(c,470-col_*50,-130+row*36,26,22,'#2a1a10',.6 if r.random()<.9 else 0)
    with layer(c,cam,.8):
        draw_crowd(c,CR_EXAM,t,6)
    with layer(c,cam,1):
        person(c,-330,330,380,'scholar','stand',1,'sad','frown')
def chrys(c,x,y,r,colr='#e8b23a',colr2='#a86a10',t=0,a=1):
    for k in range(18):
        an=k/18*6.283+t*.2
        c.save();c.translate(x,y);c.rotate(an);ell(c,r*.55,0,r*.5,r*.11,colr if k%2 else colr2,a);c.restore()
    circ(c,x,y,r*.22,'#7a4a10',a)
def s_poem(c,t,T):
    cam=seg(t,[(0,(-200,0,1.0)),(T,(150,-40,1.15))])
    with layer(c,cam,.05):sky(c,'#0e0a06','#3a2a10',-800,300);circ(c,500,-330,70,'#f2e2b0',.8);glow(c,500,-330,300,'#f2d48a',.25)
    with layer(c,cam,.3):
        ridge(c,40,'#1a140a',60,4)
        # distant Chang'an silhouette
        for i in range(12):rect(c,-900+i*150,-40-((i*37)%60),110,90,'#140e08')
    with layer(c,cam,.6):
        r=random.Random(3)
        for i in range(90):chrys(c,r.uniform(-1600,1600),r.uniform(60,300),r.uniform(14,26),t=t+i,a=.9)
        person(c,-260,250,360,'scholar','stand2',1,'angry','closed')
    with layer(c,cam,1.5):
        r=random.Random(9)
        for i in range(14):chrys(c,r.uniform(-1500,1500),r.uniform(380,600),r.uniform(70,120),t=t+i)
    petals(c,t,70,'#f2c45a',.7,4,(0,0,W,H),(60,140),(2,5))
    for j,(s_,x,t0) in enumerate([('冲天香阵透长安',W-330,.4),('满城尽带黄金甲',W-220,1.8)]):
        n=int(cl((t-t0)/1.2)*7)
        for q in range(n):
            a=cl((t-t0-q*.17)/.2)
            vtext(c,s_[q],x,170+q*80,64,'#f2d48a' if j else '#efe2c4',a,shadow=1)
def s_famine(c,t,T):
    cam=seg(t,[(0,(-440,170,3.0)),(1.4,(-420,160,2.7)),(2.6,(-100,-20,1.0)),(T,(-60,-30,1.05))])
    with layer(c,cam,.05):sky(c,'#3a2410','#a8703a',-800,200);circ(c,300,-120,110,'#f2b05a',.7);glow(c,300,-120,400,'#f2a040',.3)
    with layer(c,cam,.3):ridge(c,160,'#5a3a1e',30,5)
    with layer(c,cam,.6):
        house(c,700,220,260,110,'#5a4430','#2a2018',lit=0)
        tree(c,-850,230,1.6,'#2a1c10','#2a1c10','dead')
        tree(c,950,230,1.2,'#2a1c10','#2a1c10','dead')
    with layer(c,cam,1):
        ground(c,230,'#7a5a34','#3a2814')
        r=random.Random(4);col(c,'#4a3018',.8);c.set_line_width(2)
        for i in range(80):
            x=r.uniform(-1500,1500);y=r.uniform(250,700);c.move_to(x,y)
            for k in range(3):x+=r.uniform(-50,50);y+=r.uniform(-10,20);c.line_to(x,y)
        c.stroke()
        # grinding stone
        cx_,cy_=-440,250
        ell(c,cx_,cy_,80,24,'#5a5450');rect(c,cx_-80,cy_-40,160,40,'#6a6460');ell(c,cx_,cy_-40,80,24,'#7a746e')
        an=t*3;line(c,cx_,cy_-40,cx_+math.cos(an)*60,cy_-40+math.sin(an)*18,'#4a3018',8)
        for k in range(10):circ(c,cx_-60+k*12,cy_-44+(k%3)*4,3,'#6a7a3a')
        person(c,cx_-140,262,300,'woman','kneel',1,'sad','frown')
        person(c,cx_+130,262,200,'child','stand',-1,'sad','frown')
        person(c,250,262,320,'farmer','beg',1,'sad','open')
        person(c,520,262,380,'tangsol','whip',-1,'angry','open',weapon='whip')
        person(c,700,262,360,'tangoff2','point',-1,'proud','closed')
    dust(c,t,0,W,H,20,3,'#8a6a40',.2,3)
    if t>2.8:counter(c,'关东大旱','麦才半收','秋稼几无，州县催税照旧',t-2.8)
CHO={'冤句':(110,40),'广州':(0,70),'洛阳':(110,60),'潼关':(20,-60),'长安':(-110,40)}
def s_huangmap(c,t,T):
    pts=[M.CITIES[n] for n in ['冤句','郓州','汝州','洪州','越州','福州','广州','桂州','潭州','江陵','宣州','泗州','汝州','洛阳','潼关','长安']]
    sm=M.smooth(pts,10)
    k=cl((t-.3)/(T-1.0))
    # head position
    xy=[M.P(*p) for p in sm];L=[0]
    for i in range(1,len(xy)):L.append(L[-1]+math.dist(xy[i-1],xy[i]))
    tgt=L[-1]*eio(k)
    j=max(i for i in range(len(L)) if L[i]<=tgt)
    hx_,hy_=xy[min(j,len(xy)-1)]
    lon=hx_/M.K+110;lat=-hy_/(M.K*1.18)+31
    cx=lerp(113.5,lon,.45);cy=lerp(29.5,lat,.45)
    z=seg(t,[(0,.62),(1.5,.78),(T-1,.82),(T,.95)])
    s=M.basemap(c,cx,cy,z,t,TANG_REG)
    M.route(c,sm,eio(k),s,RED,4)
    evs=[('冤句','875 起兵',0),('广州','879 破广州',.47),('洛阳','880 入洛阳',.86),('潼关','880 破潼关',.93),('长安','881 入长安',.99)]
    for nm,lab,kk in evs:
        if k>=kk:
            a=cl((k-kk)/.04)
            M.city(c,nm,s,t,'red',pulse=nm in('广州','长安'),size=26,a=a)
            x,y=M.P(*M.CITIES[nm]);ox,oy=CHO[nm];chip(c,lab,x+ox*s,y+oy*s,k*10,kk*10,'#ff8a6a',int(22*s)+2)
    for nm in ('成都',):M.city(c,nm,s,t,'gold')
    M.endmap(c)
    counter(c,'转战','875—880','从山东打到岭南，再杀回关中',t)
CR_FLOOD=crowd_grid(61,700,-1600,1600,230,420,['hsol','hsol','hsol2','huang'],['cheer','sword','raise'],34,110,['spear','gsword','flag','torch'],faces=(1,))
def s_changan(c,t,T):
    if t<2.3:
        cam=seg(t,[(0,(-200,-150,0.9)),(2.3,(120,-60,1.12))])
        with layer(c,cam,.05):sky(c,'#140406','#6a1a10',-800,100);glow(c,0,-100,900,'#ff5a20',.25)
        with layer(c,cam,.15):clouds(c,t,'#2a0c08',.7,12,6,(-600,-250),20,sc=1.5)
        with layer(c,cam,.4):
            citywall(c,-2400,2400,-60,230,'#3e3632','#2a2420')
            gatetower(c,0,-60,230,1.1,name='春明',gate_open=1)
            for x in (-700,700,-1300,1300):banner(c,x,-80,180,t,'齐',GOLD,1,1.1,'#7a1f1a',seed=x)
            for x in (-1000,400,1100):fire(c,x,-90,1.4,t,x);smoke(c,t,x,-150,1.5,6,x%7,'#140808',.5)
        with layer(c,cam,.8):
            ground(c,230,'#2a1a14','#100806')
            dx=(t*150)%400
            draw_crowd(c,[dict(d,x=d['x']*0.6+(t*120*(1 if d['x']<0 else -1))*.6) for d in CR_FLOOD],t,4,march=2)
        with layer(c,cam,1.2):embers(c,t,70,5,(-1200,-700,2400,1400))
        arrows(c,t,.2,60,6,(-200,-300),(0,-60),700)
        return
    tt=t-2.3
    cam=(lerp(300,-200,tt/2.2),-40,1.05)
    with layer(c,cam,.05):sky(c,'#06060c','#1a1e2a',-800,200)
    with layer(c,cam,.25):peaks(c,140,'#12141c','#0c0e14',9,3,200,380)
    with layer(c,cam,.55):ridge(c,180,'#0e1016',40,2);
    with layer(c,cam,1):
        ground(c,230,'#14141a','#06060a')
        bx=-tt*320
        horse(c,bx,260,170,-1,t,True,'#c9a24a',rider='emp',rpose='hands',rweapon=None,expr='fear',mouth='open')
        for i,o in enumerate(['eunuch','tangoff','tangsol','eunuch']):
            horse(c,bx+260+i*230,262+(i%2)*14,150,-1,t+i*.3,True,['#4a3a2a','#3a2a20','#5a4a3a','#2a2a2a'][i],rider=o,rpose='hands' if o!='tangsol' else 'point',rweapon=None if o!='tangsol' else 'spear',expr='fear')
    rain(c,t,160,.3,40,.25,seed=4)
    text(c,'唐僖宗 逃往成都',W/2-300,250,34,'#c9d0e0',cl(tt/.4),shadow=1)
CR_HALL=[]
for side in (-1,1):
    for i in range(5):
        for j in range(2):CR_HALL.append(dict(x=side*(330+i*150+j*60),y=280+j*36,h=200+j*20,out='tangoff' if (i+j)%2 else 'tangoff2',pose='hands',w=None,ph=i,face=-side))
CR_HALL.sort(key=lambda d:d['y'])
def palace_bg(c,cam,t,tone='gold'):
    with layer(c,cam,.2):
        c.set_source(lgrad(c,0,-700,0,400,[(0,'#2a0e08',1),(1,'#5a1c12',1)]));c.paint()
        for i in range(-6,7):
            x=i*260;rect(c,x-26,-700,52,1000,'#8e2a1e');rect(c,x-26,-700,10,1000,'#b8473a',.6)
            rect(c,x+40,-400,170,300,'#3a120e')
            col(c,'#b8873e',.5);c.set_line_width(2)
            for k in range(0,171,17):c.move_to(x+40+k,-400);c.line_to(x+40+k,-100)
            for k in range(0,301,17):c.move_to(x+40,-400+k);c.line_to(x+210,-400+k)
            c.stroke()
        rect(c,-2000,-560,4000,60,'#6a1c12');rect(c,-2000,-506,4000,8,GOLD,.6)
    with layer(c,cam,.5):
        for x in (-900,-450,450,900):
            sw=math.sin(t*1.3+x)*4
            line(c,x,-500,x+sw,-430,'#15100c',2);glow(c,x+sw,-380,120,'#ff9a40',.35)
            poly(c,[(x+sw-28,-430),(x+sw+28,-430),(x+sw+34,-390),(x+sw+28,-350),(x+sw-28,-350),(x+sw-34,-390)],'#c0392b',1,INK,2)
def s_throne(c,t,T):
    cam=seg(t,[(0,(0,60,0.9)),(1.4,(0,20,1.0)),(T,(0,-200,2.3))])
    palace_bg(c,cam,t)
    with layer(c,cam,.7):
        ground(c,250,'#3a1810','#120806')
        poly(c,[(-420,250),(420,250),(330,40),(-330,40)],'#5a2014',1,'#d9b56a',2)
        for k in range(5):rect(c,-330+k*10,40+k*42,660-k*20,4,GOLD,.3)
        rect(c,-260,-300,520,280,'#c99a2a');rect(c,-245,-285,490,250,'#3e5a5a')
        poly(c,[(-240,-40),(-120,-200),(-40,-120),(60,-230),(240,-40)],'#6a8a7a')
        poly(c,[(-110,40),(110,40),(100,-110),(-100,-110)],'#b8332a',1,GOLD,3)
        person(c,0,40,300,'huangrobe','sit',1,'proud','closed')
        beams(c,0,-500,t,9,'#ffd27a',.08,1200,1.6)
    with layer(c,cam,1):draw_crowd(c,CR_HALL,t,0)
    stamp(c,'大 齐',W/2+560,330,t,1.6,120,-6,sub='金统元年')
CR_FLEE=crowd_grid(71,60,-1400,1400,250,420,['woman','woman2','farmer','farmer2','child','scholar'],['x'],120,240,[None])
def s_wash(c,t,T):
    cam=seg(t,[(0,(200,-40,1.15)),(T,(-200,-20,1.0))])
    c.save();c.translate(math.sin(t*23)*4,math.cos(t*19)*3)
    with layer(c,cam,.05):sky(c,'#1a0404','#7a1a0c',-800,100);glow(c,0,-100,1000,'#ff4a1a',.3)
    with layer(c,cam,.3):
        for i in range(10):house(c,-1800+i*400,140,300,120,'#2a1410','#120606',door=False,burn=1)
        for i in range(10):fire(c,-1800+i*400,20,1.6,t,i)
        smoke(c,t,0,-100,3,10,2,'#100404',.55)
    with layer(c,cam,.7):
        ground(c,230,'#2a1410','#0a0404')
        for i in range(4):house(c,-1500+i*1000,250,380,170,'#3a2014','#1a0c08',lit=1)
        for d in CR_FLEE:
            x=d['x']-t*260*(d['h']/200)
            person(c,x,d['y'],d['h'],d['out'],walk(t*1.3+d['ph'],run=True),-1,'fear','open')
        for i in range(4):
            x=900+i*220-t*150
            person(c,x,260+i*30,300,'hsol','slash' if (int(t*3)+i)%2 else 'sword',-1,'angry','open',weapon='gsword')
    with layer(c,cam,1.3):embers(c,t,90,5,(-1300,-700,2600,1400))
    c.restore()
    vignette_red(c,.65)
    stamp(c,'洗 城',W/2+420,300,t,1.6,120,-6,sub='史书记载')
def s_mill(c,t,T):
    cam=seg(t,[(0,(-120,0,1.0)),(T,(120,-20,1.12))])
    with layer(c,cam,.05):sky(c,'#100808','#3a1a14',-800,200);glow(c,0,0,900,'#8a2a1a',.3)
    with layer(c,cam,.3):
        ridge(c,120,'#1a0e0c',30,6)
        for i in range(14):
            x=-2000+i*300;ph=math.sin(t*2.4+i*.9)
            rect(c,x-4,0,8,110,'#140808');poly(c,[(x-90,10-ph*14),(x+90,10+ph*14),(x+90,16+ph*14),(x-90,16-ph*14)],'#140808')
            ell(c,x+90,40+ph*14,16,12,'#140808')
    with layer(c,cam,.6):
        for i in range(7):
            x=-1500+i*500;ph=math.sin(t*2.4+i*1.3)
            rect(c,x-10,-40,20,300,'#0a0404');
            c.save();c.translate(x,-30);c.rotate(ph*.18)
            rect(c,-260,-10,520,22,'#0a0404');rect(c,220,-10,34,150,'#0a0404');ell(c,237,150,40,30,'#0a0404')
            c.restore()
            ell(c,x+237,280,110,34,'#0a0404');rect(c,x+137,250,200,30,'#0a0404')
    with layer(c,cam,.9):
        ground(c,300,'#1a0c0a','#050202')
        for i in range(10):ell(c,-2200+i*480+t*80,180,520,120,'#3a2420',.45)
    vignette_red(c,.55)
    stamp(c,'存 疑',W/2+420,300,t,1.5,120,-6,colr='#b8a888',sub='后世多疑夸大')
def s_wolf(c,t,T):
    if t<2.2:
        cam=seg(t,[(0,(0,-120,0.9)),(2.2,(60,-60,1.0))])
        with layer(c,cam,.05):sky(c,'#0e1014','#2e3238',-800,200)
        with layer(c,cam,.2):peaks(c,220,'#1e2228','#16191e',7,3,500,800)
        with layer(c,cam,.45):
            for i in range(6):ell(c,-1500+i*600+t*40,0,500,80,'#3a3e44',.35)
            peaks(c,260,'#14171c','#0e1014',6,8,350,600)
        with layer(c,cam,.8):
            poly(c,[(-1800,220),(-500,-300),(-250,220)],'#0a0c0e');poly(c,[(1800,220),(500,-360),(250,220)],'#0a0c0e')
            ground(c,200,'#101214','#060708')
            for i in range(9):person(c,-120+i*30+t*20,200,46,'hsol2',walk(t+i*.2),1,'sad')
            person(c,-170+t*20,200,52,'huang',walk(t),1,'sad')
        rain(c,t,240,.2,40,.35,seed=3)
        return
    tt=t-2.2
    cam=(0,-260,lerp(2.4,2.9,tt/2.3))
    with layer(c,cam,.1):sky(c,'#0e1014','#2e3238',-800,200);peaks(c,100,'#1e2228','#16191e',7,3,500,800)
    with layer(c,cam,1):
        person(c,-40,40,330,'huang','stand2',1,'sad','frown',weapon='gsword')
        person(c,200,40,300,'hsol2','stand',-1,'fear','closed',weapon='sword',a=.9)
    rain(c,t,240,.2,46,.35,seed=3)
    col(c,'#000000',cl((tt-1.6)/.7)*.6);c.paint()
def s_tang(c,t,T):
    s=M.basemap(c,113.5,34.5,seg(t,[(0,1.1),(T,1.25)]),t,TANG_REG,tone='#2a2016')
    M.city(c,'狼虎谷',s,t,'red',size=24)
    M.city(c,'长安',s,t,'gold')
    e=M.route(c,[M.CITIES['长安'],M.CITIES['洛阳'],M.CITIES['汴州']],(t-.3)/1.2,s,'#9a9aa8',3)
    M.city(c,'汴州',s,t,'gold',pulse=1,a=cl((t-1)/.3))
    M.endmap(c)
    stamp(c,'唐 亡',W/2+330,770,t,1.6,120,-6,sub='907年 · 朱温篡位')
