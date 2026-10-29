from base import *
from shotsA import chapter2
# ================= 盲区二 战略短视 =================
@shot(96,100)
def d1(c,t,T):chapter2(c,t,2,'战略短视','把生死战打成商务谈判')
R1=[(102.7,25.04),(104.8,25.9),(106.7,26.6),(109.2,27.6),(111.7,29.03)]
R2=[(109.2,27.6),(110.8,26.9),(112.57,26.9),(112.94,28.23),(113.13,29.37)]
@shot(100,110,'1674年·湖南')
def d2(c,t,T):
    z=seg(t,[(0,.8),(bt(10),1.05)]);cx=seg(t,[(0,(106,27)),(bt(10),(110,28))])
    sc=G.basemap(c,cx[0],cx[1],z,t,regions=[('云南',(101.5,24.5),1),('贵州',(106.2,26.2),1),('湖南',(111.5,27.6),1)])
    G.zone(c,G.PROV['云南'],RED,1,sc);G.zone(c,G.PROV['贵州'],RED,ramp(t,bt(2),bt(4)),sc);G.zone(c,G.PROV['湖南'],RED,ramp(t,bt(5),bt(8)),sc)
    G.route(c,R1,ramp(t,bt(.5),bt(4)),sc,RED,6,arrow=t>bt(4))
    G.route(c,R2,ramp(t,bt(3.5),bt(7.5)),sc,RED,6,arrow=t>bt(7.5))
    for n in ('昆明','贵阳','常德','长沙','衡阳'):G.city(c,n,sc,t,'red')
    G.city(c,'岳州',sc,t,'red',pulse=1,big=1.4)
    for n in ('武昌','荆州'):G.city(c,n,sc,t)
    G.endmap(c)
    counter(c,t,'起兵仅',[(bt(1),'2个月'),(bt(5),'数月')],note='连下贵州、湖南')
sub(100,106,'起兵仅数月，吴军{平推湖南}')
sub(106,110,'兵锋直抵{岳州}，饮马长江')
STORM=crowd(51,70,-1200,1200,300,460,['wsol'],('raise','hold'),70,150)
DEF=crowd(52,24,-900,900,-170,-150,['qb','qr'],('hold','stand'),40,48)
@shot(110,120,'1674年·湖南')
def d3(c,t,T):
    cam=seg(t,[(0,(0,40,1.0)),(bt(5),(150,60,1.15)),(bt(5.01),(-100,-60,1.45)),(bt(10),(0,-80,1.55))])
    with layer(c,cam,.05):sky(c,'#1a0c08','#a03a1a',-900,0);glow(c,0,-200,900,'#ff7a30',.25)
    with layer(c,cam,.2):
        for x in (-1500,-800,600,1300):smoke(c,t,x,-150,3,seed=x,a=.7)
    with layer(c,cam,.6):
        citywall(c,-2200,2200,-140,300)
        gatetower(c,0,-140,300,1,name='长沙')
        flg='清' if t<bt(6) else '周'
        banners(c,[-900,-600,600,900],-140,180,t,flg,'#3a5aa0' if t<bt(6) else '#d9a82e')
        draw_crowd(c,DEF,t,a=1 if t<bt(6) else 0)
        for x in (-1200,-400,500,1100):fire(c,x,-140,1.6,t,seed=x)
        for i,x in enumerate((-1000,-700,-300,300,700,1000)):
            line(c,x,320,x+120,-130,'#5a3a1a',8);[line(c,x+k*20,320-k*75,x+40+k*20,320-k*75,'#5a3a1a',5) for k in range(6)]
            kk=((t*.8+i*.3)%1);person(c,x+kk*110,320-kk*440,90,'wsol',pose='raise',t=t)
        arrows(c,t,.2,90,seed=3,src=(0,-160),dst=(0,450),spread=900,dur=1.6)
        arrows(c,t,2.2,90,seed=4,src=(0,-160),dst=(0,450),spread=900,dur=1.6)
    with layer(c,cam,1):
        ground(c,300,'#3a1e14','#0a0604')
        draw_crowd(c,STORM,t,bob=10,march=.8)
    embers(c,t,80,area=(0,0,W,H))
    stamp(c,t,bt(6),'清军溃退',W*.74,H*.34,110)
sub(110,115,'清军节节败退，{江南兵力空虚}')
sub(115,120,'这一刻，大清离崩盘只差{一步}')
@shot(120,128,'1674年·岳州')
def d4(c,t,T):
    z=seg(t,[(0,.95),(bt(8),.62)]);cx=seg(t,[(0,(113,29.5)),(bt(8),(115,33))])
    sc=G.basemap(c,cx[0],cx[1],z,t,regions=[('江 南',(118.5,31),1),('直 隶',(116,38.5),1)])
    G.zone(c,G.PROV['湖南'],RED,1,sc)
    G.zone(c,G.JIANGNAN,GOLD,ramp(t,bt(3.5),bt(5)),sc)
    G.route(c,[(113.13,29.37),(114.3,30.55),(114.5,34.5),(116.4,39.9)],ramp(t,bt(.5),bt(4)),sc,GOLD,5,dash=True,arrow=t>bt(4))
    G.route(c,[(113.13,29.37),(114.3,30.6),(115.9,29.7),(117,30.5),(118.8,32.05),(120.15,30.27)],ramp(t,bt(3),bt(6.5)),sc,GOLD,5,dash=True,arrow=t>bt(6.5))
    G.city(c,'岳州',sc,t,'red',pulse=1,big=1.3);[G.city(c,n,sc,t) for n in ('武昌','江宁','杭州')]
    G.city(c,'北京',sc,t,pulse=1,big=1.3)
    G.endmap(c)
    if t>bt(2):text(c,'渡江北伐',W*.38,H*.3,52,GOLD,cl((t-bt(2))*3))
    if t>bt(5):text(c,'顺江东下 · 江浙财赋',W*.66,H*.66,48,GOLD,cl((t-bt(5))*3))
sub(120,128,'只要渡江北上，或顺江东下拿下{江浙财赋}，大清大概率崩盘')
HALT=crowd(61,70,-1400,-200,250,440,['wsol'],('hold','stand'),60,130,faces=(1,))
@shot(128,138,'1674年·长江')
def d5(c,t,T):
    cam=seg(t,[(0,(300,60,1.0)),(bt(4),(-200,80,1.15)),(bt(4.01),(-420,120,1.7)),(bt(10),(-460,110,1.8))])
    with layer(c,cam,.05):sky(c,'#1a2026','#7a6a5a',-900,60)
    with layer(c,cam,.15):ridge(c,-40,'#3a3a3a',amp=40,seed=8,a=.6)
    with layer(c,cam,.3):
        rect(c,-2600,-20,5200,600,'#3a5058')
        for k in range(50):x=(k*137-t*40)%4000-2000;line(c,x,30+(k*31)%200,x+80,30+(k*31)%200,'#a8c0c0',2,.4)
        for x in (900,1200,1500):banner(c,x,-30,90,t,'清','#3a5aa0',.5,.6)
        for i in range(6):ell(c,-1200+i*500+(t*30)%500,-10,300,40,'#c8c0b0',.12)
    with layer(c,cam,.7):
        poly(c,[(-2600,140),(-300,120),(0,200),(200,600),(-2600,700)],'#2a2018')
        for x in (-1000,-700,-400):ships(c,x+300,200,.6,t,txt='周')
    with layer(c,cam,1):
        poly(c,[(-2600,260),(-500,240),(-300,300),(-200,700),(-2600,800)],'#1a120c')
        draw_crowd(c,HALT,t,dx=0 if t>bt(4) else -100+t*40)
        horse(c,-380,280,190,1,t,col_='#2a1c14',rider='wum',rider_pose='raise' if t>bt(3) else 'ride')
    stamp(c,t,bt(3.2),'停',W*.66,H*.4,220)
sub(128,133,'结果，他在长江边{停下了}！')
sub(133,138,'这一停，就{再也没有渡江}')
@shot(138,146,'1674—1678年·岳州')
def d6(c,t,T):
    yr=min(4,int(t/bt(2)));ph=(t/bt(2))%1
    seas=['#7a8a6a','#8a6a3a','#c8c8d0','#6a8a5a']
    cam=(0,-60,1.05+.02*t)
    with layer(c,cam,.05):sky(c,'#1a1e24',seas[yr%4],-800,120)
    with layer(c,cam,.4):
        rect(c,-2000,40,4000,600,'#3a5058');ridge(c,40,'#2a3030',amp=30,seed=3)
    with layer(c,cam,1):
        ground(c,300,'#2a2018','#0a0806')
        tree(c,-600,320,2.2,colr=seas[yr%4],t=t)
        person(c,120,330,380,'wum',pose='stand',face=-1,t=t,lean=.04*yr,eyes='closed' if yr>1 else 'dot')
    if yr%4==1:petals(c,t,60,'#c8783a',.8,area=(0,0,W,H))
    if yr%4==2:petals(c,t,120,'#ffffff',.8,area=(0,0,W,H))
    counter(c,t,'按兵不动',[(0,'1674'),(bt(2),'1675'),(bt(4),'1676'),(bt(6),'1677')],note='吴军始终没有渡江')
    if t>bt(3):
        k=pop(t,bt(3));c.save();c.translate(W*.72,H*.36);c.scale(k,k);rect(c,-200,-120,400,240,'#e8dcbc',.95);text(c,'划江而治',0,20,72,'#1a120c');text(c,'—— 吴三桂的算盘',40,90,28,'#7a1f1a');c.restore()
sub(138,146,'他老了，不想搏命，只想逼康熙{划江而治}')
@shot(146,154,'1674年·北京')
def d7(c,t,T):
    cam=seg(t,[(0,(0,-80,1.0)),(bt(4),(-180,-140,1.3)),(bt(4.01),(0,-80,1.05))])
    with layer(c,cam,.1):rect(c,-2000,-1500,4000,3000,'#4a100c')
    with layer(c,cam,.5):
        for x in range(-1200,1300,240):rect(c,x-26,-700,52,1000,'#9a2418');rect(c,x-26,-700,10,1000,'#c8402a')
        rect(c,-1500,250,3000,800,'#2a1a10')
    with layer(c,cam,1):
        poly(c,[(-180,60),(180,60),(140,-200),(-140,-200)],'#d9a82e',1,INK,3)
        person(c,0,120,300,'kx',pose='point' if t>bt(2) else 'stand',t=t,eyes='angry',face=1)
        k=ramp(t,bt(1),bt(2.5))
        for sx in(-1,1):
            c.save();c.translate(260+sx*k*120,-60+k*k*300);c.rotate(sx*k*.8);rect(c,-60 if sx<0 else 0,-80,60,160,'#e8dcbc');c.restore()
        if t<bt(1.5):text(c,'划江',260,-40,40,'#1a120c')
        for i,x in enumerate((-600,-450,450,600)):person(c,x,380,260,'qy',pose='hold',face=1 if x<0 else -1,t=t)
    if t>bt(4):
        k=pop(t,bt(4))
        c.save();c.translate(W*.72,H*.5);c.rotate(-.12*k);c.scale(k,k)
        rect(c,-160,-200,320,400,'#1a120c',.85);person(c,0,140,240,'off',pose='fall',t=t)
        text(c,'吴应熊',0,-150,48,'#f3e6c8');text(c,'吴三桂之子',0,190,26,GREY);c.restore()
        stamp(c,t,bt(5),'斩',W*.72,H*.5,150,.1)
sub(146,150,'20岁的康熙{一口回绝}')
sub(150,154,'还处死了吴三桂留在京城的儿子{吴应熊}','1674年')
@shot(154,160,'1674年')
def d8(c,t,T):
    sc=G.basemap(c,113,32,.7,t)
    G.zone(c,G.PROV['湖南'],RED,1,sc)
    for i,(a_,b_) in enumerate([((116.4,39.9),(112.2,30.33)),((118.8,32.05),(114.3,30.55)),((108.94,34.27),(110.5,30.8)),((120.15,30.27),(116.5,28.5))]):
        G.route(c,[a_,b_],ramp(t,bt(.5+i*.8),bt(3+i*.8)),sc,GOLD,7,arrow=True)
    for n in ('北京','江宁','西安','荆州','武昌','杭州'):G.city(c,n,sc,t)
    G.city(c,'岳州',sc,t,'red',pulse=1)
    G.endmap(c)
    stamp(c,t,bt(3.5),'错失良机',W*.72,H*.36,110)
sub(154,160,'用谈判心态打生死战，等于把大清{从鬼门关放了回来}')
# ================= 盲区三 塑料同盟 =================
@shot(160,164)
def e1(c,t,T):chapter2(c,t,3,'塑料同盟','各怀鬼胎的乌合之众')
TEN=['云南','贵州','湖南','四川','广西','福建','广东','陕甘']
@shot(164,172,'1674—1676年')
def e2(c,t,T):
    sc=G.basemap(c,109,28.5,.72,t)
    for i,p in enumerate(TEN):G.zone(c,G.PROV[p],RED,ramp(t,bt(.3+i*.7),bt(.8+i*.7)),sc);G.plabel(c,p,sc,cl((t-bt(.5+i*.7))*3))
    G.city(c,'北京',sc,t,pulse=1)
    G.endmap(c)
    counter(c,t,'叛军声势',[(bt(.3),'1省'),(bt(2),'4省'),(bt(4),'7省'),(bt(5.5),'十省响应')],note='含江西、浙江部分地区',h=RED)
sub(164,172,'{十省响应}，看着吓人')
AL=[('耿精忠','福建','#2a6a8a',(119.3,26.08)),('尚之信','广东','#6a8a2a',(113.26,23.13)),('王辅臣','陕甘','#7a5a2a',(106.67,35.54)),('郑经','台湾','#2a4a7a',(120.2,23.0))]
@shot(172,180,'')
def e3(c,t,T):
    sc=G.basemap(c,112,29,.72,t,dim=.2)
    for p in TEN:G.zone(c,G.PROV[p],RED,.6,sc)
    G.city(c,'昆明',sc,t,'red',big=1.4)
    pts=[]
    for i,(n,r_,cc,ll) in enumerate(AL):
        x,y=G.P(*ll);pts.append((x,y))
    G.endmap(c)
    m=c.get_matrix()
    for i,(n,r_,cc,ll) in enumerate(AL):
        x0,y0=G.P(*ll);zz=.72;sx=W/2+(x0-G.P(112,29)[0])*zz;sy=H/2+(y0-G.P(112,29)[1])*zz
        sy=cl(sy,170,760);sx=cl(sx,140,W-200)
        badge(c,t,bt(.5+i*1.2),sx,sy,n,r_,cc)
        if t>bt(1+i*1.2):text(c,'墙头草' if i<2 else ('孤军' if i==2 else '抢地盘'),sx+90,sy-60,30,RED,cl((t-bt(1+i*1.2))*3),align='l')
sub(172,180,'可盟友全是{看风向的投机客}')
FUJ=crowd(71,40,-1300,-100,200,440,['geng'],('raise','hold'),70,140)
ZHE=crowd(72,30,100,1300,200,440,['zj'],('raise','hold'),70,140,faces=(-1,))
@shot(180,190,'1676年·福建沿海')
def e4(c,t,T):
    cam=seg(t,[(0,(0,-80,1.0)),(bt(5),(0,-80,1.1)),(bt(5.01),(200,-160,1.45)),(bt(10),(260,-180,1.55))])
    with layer(c,cam,.05):sky(c,'#1a1a24','#7a5a4a',-800,40)
    with layer(c,cam,.3):
        rect(c,-2600,0,5200,300,'#2a4a5a')
        for k in range(40):x=(k*151+t*30)%4000-2000;line(c,x,40+(k*29)%200,x+70,40+(k*29)%200,'#a8c0c8',2,.4)
        for i,x in enumerate((500,900,1300)):ships(c,x,120,.8,t,face=-1,txt='郑',fire_=t>bt(4) and i==1)
        for x in (700,1100):smoke(c,t,x,40,2,seed=x,colr='#d8d0c8',a=.4)
    with layer(c,cam,1):
        ground(c,200,'#6a5a3a','#1a140c')
        k=ramp(t,0,bt(3))
        draw_crowd(c,FUJ,t,dx=k*300,march=1)
        draw_crowd(c,ZHE,t,dx=-k*300,march=1)
        dust(c,t,-400,400,440,30,colr='#8a7050',a=.35,s=1.6)
        arrows(c,t,.5,60,seed=8,src=(900,-100),dst=(-600,400),spread=500,dur=1.4)
        arrows(c,t,2.5,60,seed=9,src=(-900,-100),dst=(600,400),spread=500,dur=1.4)
    badge(c,t,.3,W*.14,H*.22,'耿精忠','福建',RED);badge(c,t,.6,W*.86,H*.22,'郑经','台湾','#2a4a7a')
    vs_line(c,W*.14+70,H*.22,W*.86-70,H*.22,t)
    stamp(c,t,bt(6),'内讧',W/2,H*.4,170)
sub(180,185,'耿精忠不打清军')
sub(185,190,'先和台湾{郑经}抢地盘，打成一团')
@shot(190,196,'陕甘')
def e5(c,t,T):
    sc=G.basemap(c,109,32,.85,t)
    G.zone(c,G.PROV['陕甘'],RED,1,sc);G.zone(c,G.PROV['湖南'],RED,.6,sc);G.zone(c,G.PROV['四川'],RED,.4,sc)
    G.route(c,[(106.67,35.54),(109,32),(112.5,28.5)],ramp(t,0,bt(2)),sc,RED,4,dash=True,head=False)
    if t>bt(2.2):
        x,y=G.P(109.6,31.8);line(c,x-30*sc,y-30*sc,x+30*sc,y+30*sc,RED,8*sc);line(c,x+30*sc,y-30*sc,x-30*sc,y+30*sc,RED,8*sc)
    G.city(c,'平凉',sc,t,'red',pulse=1,big=1.4);G.city(c,'西安',sc,t)
    for i in range(6):a_=i*1.05+t*.3;G.route(c,[(107.5+math.cos(a_)*3,36+math.sin(a_)*2),(106.9,35.6)],ramp(t,bt(1+i*.3),bt(3+i*.3)),sc,GOLD,4,arrow=True)
    G.endmap(c)
    badge(c,t,.3,W*.2,H*.3,'王辅臣','陕甘',RED)
sub(190,196,'西北{王辅臣}孤军作战，毫无配合')
@shot(196,204,'北京')
def e6(c,t,T):
    rect(c,0,0,W,H,'#1a0e0a');glow(c,W/2,H/2,800,'#8a3a1a',.3)
    c.save();c.translate(W/2,H/2);s_=1+.04*t;c.scale(s_,s_);c.translate(-W/2,-H/2)
    scroll_doc(c,W/2,H/2-40,900,640,['只诛吴三桂一人','其余投诚者','一概既往不咎'],t,.1,title='康熙诏谕',seal=(bt(4),W/2-320,H/2+180,'敕命'))
    c.restore()
sub(196,204,'康熙甩出一张牌：只诛{吴三桂一人}，其余投降{既往不咎}')
@shot(204,212,'1676—1677年')
def e7(c,t,T):
    sc=G.basemap(c,112,29,.72,t,dim=.2)
    for i,p in enumerate(TEN):
        flip={'陕甘':1,'福建':2.5,'广东':4}.get(p)
        k=ramp(t,bt(flip),bt(flip+.6)) if flip else 0
        G.zone(c,G.PROV[p],RED,.6*(1-k),sc);G.zone(c,G.PROV[p],GOLD,k,sc)
    G.endmap(c)
    for i,(n,yr,ll) in enumerate([('王辅臣','1676',(106.67,35.54)),('耿精忠','1676',(119.3,26.08)),('尚之信','1677',(113.26,23.13))]):
        x0,y0=G.P(*ll);zz=.72;sx=W/2+(x0-G.P(112,29)[0])*zz;sy=H/2+(y0-G.P(112,29)[1])*zz
        sy=cl(sy,170,760);sx=cl(sx,140,W-200)
        tt=bt([1,2.5,4][i])
        badge(c,t,0,sx,sy,n,yr+(' 降清' if t>tt else ''),GOLD if t>tt else RED)
        if t>tt:stamp(c,t,tt,'降',sx+80,sy-50,60)
    stamp(c,t,bt(6),'联盟瓦解',W/2,H*.18,120)
sub(204,212,'王辅臣、耿精忠、尚之信{接连投降}，联盟瞬间瓦解')
