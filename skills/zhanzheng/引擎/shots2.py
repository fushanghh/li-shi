from common import *
from shots1 import zmap,cities,field,HJ
# ================= 第四层 =================
@nx(4,'')
def k4(c,t,T):card(c,t,'4','内鬼','有人开门',label='第四层')
@nx(6,'548年八月起','548年，侯景起兵，杀到长江北岸，{没有船}')
def d1(c,t,T):
    sc=zmap(c,t,118,32,1.4)
    G.route(c,[(116.78,32.58),(117.6,32.2),(118.4,31.7)],ramp(t,.2,bt(3)),sc,h='#8a8a6a',lw=8,arrow=True)
    cities(c,t,sc,['寿阳','横江','建康'],size=44)
    G.endmap(c)
    xmark(c,t,bt(3.5),W*.62,H*.6,50)
    label(c,t,bt(3.3),'长江天险',W*.7,H*.2,56)
@nx(5,'548年','守江的，是梁武帝的养子{萧正德}')
def d2(c,t,T):
    cam=fc(seg(t,[(0,(0,-60,1.0)),(bt(5),(0,-90,1.15))]))
    with layer(c,cam,.05):sky(c,'#1a2030','#5a5a6a',-700,100)
    with layer(c,cam,1):
        rect(c,-2600,100,5200,600,'#1e3640')
        ground(c,100,'#3a3428','#141210') if False else None
        person(c,0,90,420,'xzd',pose='stand',t=t,face=1,eyes='angry')
    badge(c,t,bt(.5),W*.8,H*.3,'萧正德','临贺王 · 平北将军','#5a2a4a','萧',66)
@nx(5,'501年后','萧统出生后，他被{送回本家}，一直怀恨')
def d3(c,t,T):
    cam=fc(seg(t,[(0,(0,-60,1.0)),(bt(5),(0,-80,1.12))]))
    palace(c,cam,t)
    with layer(c,cam,1):
        person(c,350,250,440,'lwd',pose='hold',t=t,face=-1);person(c,200,250,160,'gz',pose='stand',t=t,face=-1)
        k=ramp(t,bt(1),bt(3.5));person(c,-200-k*600,250,300,'xzd',pose='walk',t=t,face=-1,eyes='angry')
    label(c,t,bt(1),'太子萧统',W*.65,H*.2,46)
@nx(6,'548年十月','他派{几十艘大船}，假称{运芦苇}','《资治通鉴》卷161：正德遣大船数十艘，诈称载荻，密以济景')
def d4(c,t,T):
    cam=fc(seg(t,[(0,(0,-60,1.0)),(bt(6),(150,-60,1.1))]))
    with layer(c,cam,.05):sky(c,'#0c0c18','#2a2a3a',-700,0);circ(c,600,-300,50,'#e8e8f0',.5)
    with layer(c,cam,1):
        rect(c,-2600,-20,5200,700,'#142a34')
        for i in range(6):
            x=-1500+i*520+t*40;y=60+(i%2)*80
            poly(c,[(x-150,y),(x+150,y),(x+120,y+50),(x-120,y+50)],'#4a3018',1,INK,2)
            for k in range(4):ell(c,x-90+k*60,y-20,34,24,'#a8a060')
    label(c,t,bt(2),'诈称载荻',W*.5,H*.16,56)
@nx(5,'548年十月','把侯景{八千人}，送过了长江','《资治通鉴》卷161：马数百匹，兵八千人')
def d5(c,t,T):
    sc=zmap(c,t,118.6,31.9,2.0)
    G.route(c,[(118.4,31.7),(118.55,31.85),(118.78,32.06)],ramp(t,.2,bt(3)),sc,h=RED,lw=10,arrow=True)
    cities(c,t,sc,['横江','建康'],red=('建康',),size=48)
    G.endmap(c)
    counter(c,t,'渡江',[(bt(.4)+i*.3,'%d人'%v) for i,v in enumerate([1000,3000,5000,8000])],h=RED)
@nx(5,'548年十月','天险，{一夜失守}')
def d6(c,t,T):
    cam=fc(seg(t,[(0,(0,-60,1.0)),(bt(5),(300,-60,1.1))]))
    with layer(c,cam,.05):sky(c,'#100808','#4a1a10',-700,100)
    with layer(c,cam,1):
        ground(c,100,'#2a1a10','#0a0604')
        draw_crowd(c,[dict(d,x=d['x']+t*120) for d in HJ],t,march=.7)
    stamp(c,t,bt(2),'失守',W*.75,H*.22,110,.05)
# ================= 第五层 =================
@nx(4,'')
def k5(c,t,T):card(c,t,'5','围观','城外的援军',label='第五层')
@nx(6,'548年十月—549年三月','侯景围{台城}，一围{一百三十多天}')
def e1(c,t,T):
    cam=fc(seg(t,[(0,(0,-60,1.0)),(bt(6),(0,-80,1.12))]))
    with layer(c,cam,.05):sky(c,'#1a1010','#5a2a1a',-700,100)
    with layer(c,cam,.5):citywall(c,-2400,2400,-160,200);gatetower(c,0,-160,200,1.1,name='台城')
    with layer(c,cam,1):ground(c,200,'#2a1a10','#0a0604');draw_crowd(c,HJ,t,bob=1)
    counter(c,t,'围城',[(bt(.4)+i*.4,'%d天'%v) for i,v in enumerate([1,30,60,90,120,130])])
@nx(5,'549年','城外援军号称{二三十万}')
def e2(c,t,T):
    sc=zmap(c,t,118.4,32,1.6)
    r=random.Random(3)
    for i in range(14):
        lo=118.78+r.uniform(-1.5,1.2);la=32.06+r.uniform(-1,1)
        if (lo-118.78)**2+(la-32.06)**2>.25 and t>bt(.2+i*.2):x,y=G.P(lo,la);glow(c,x,y,30,GOLD,.6);circ(c,x,y,8,'#fff0c0')
    G.city(c,'建康',sc,t,state='red',pulse=1,big=1.7,size=48)
    G.endmap(c)
    counter(c,t,'援军',[(bt(.5)+i*.4,'%d万'%v) for i,v in enumerate([5,10,20,30])],note='号称')
@nx(6,'549年·荆州','湘东王{萧绎}，在荆州{按兵不动}')
def e3(c,t,T):
    sc=zmap(c,t,115.5,31.2,.85)
    G.route(c,[(112.2,30.3),(113.5,30.5),(114.3,30.6)],ramp(t,.2,bt(2))*.4,sc,h=GOLD,lw=6)
    cities(c,t,sc,['江陵','建康'],red=('建康',),size=44)
    G.endmap(c)
    badge(c,t,bt(.5),W*.15,H*.3,'萧绎','湘东王','#2f4a5a','绎',60)
    stamp(c,t,bt(2.5),'按兵不动',W*.5,H*.2,80,-.04)
@nx(6,'549年·建康城外','援军统帅{柳仲礼}，整日{饮酒作乐}，不肯出战')
def e4(c,t,T):
    cam=fc(seg(t,[(0,(0,-60,1.0)),(bt(6),(0,-90,1.18))]))
    with layer(c,cam,.05):sky(c,'#1a1418','#4a3a3a',-700,200)
    with layer(c,cam,1):
        ground(c,150,'#3a3024','#100c08')
        tent(c,0,160,2.4,'#c8b89a')
        person(c,-200,290,360,'lzl',pose='raise',t=t,face=1)
        for x in (150,320):person(c,x,290,280,'gz',pose='wave',t=t,face=-1)
        rect(c,-60,250,120,40,'#5a3a1a');circ(c,-20,240,12,GOLD);circ(c,20,240,12,GOLD)
    badge(c,t,bt(.5),W*.15,H*.26,'柳仲礼','大都督','#6a3a2a','柳',56)
@nx(5,'549年','各路宗室{互不统属}，各打算盘')
def e5(c,t,T):
    rect(c,0,0,W,H,'#0d0907');glow(c,W/2,H*.45,500,RED,.25)
    badge(c,t,.1,W/2,H*.45,'台城','','#7a1f1a','台',90)
    for i,(n,ch) in enumerate([('萧绎','绎'),('萧纶','纶'),('萧纪','纪'),('柳仲礼','柳')]):
        a_=i/4*2*math.pi+math.pi/4;badge(c,t,bt(.4+i*.3),W/2+math.cos(a_)*480,H*.45+math.sin(a_)*260,n,'',"#4a3a2a",ch,60)
    if t>bt(2):clib.htext(c,'？',W/2,H*.2,120,clib.GOLDG,cl((t-bt(2))*3))
@nx(5,'549年三月','549年三月，{台城陷落}')
def e6(c,t,T):
    cam=fc(seg(t,[(0,(0,-60,1.2)),(bt(5),(0,-60,1.0))]))
    with layer(c,cam,.05):sky(c,'#100808','#6a2414',-800,100)
    with layer(c,cam,.5):citywall(c,-2400,2400,-160,200);gatetower(c,0,-160,200,1.1,name='台城')
    with layer(c,cam,1):
        ground(c,200,'#2a1410','#0a0504')
        for x in (-900,-400,400,900):fire(c,x,200,2,t,seed=x)
        banner(c,-250,300,360,t,'梁','#c0392b',1-ramp(t,bt(1),bt(3))*.8,1.4)
    smoke(c,t,W/2,H*.3,4,12,colr='#100606',a=.5);embers(c,t,80,area=(0,0,W,H),a=.8)
    stamp(c,t,bt(2.5),'陷落',W*.74,H*.22,96,.05)
# ================= 结局 =================
@nx(6,'549年五月·台城','549年五月，八十六岁的梁武帝{困死台城}')
def f1(c,t,T):
    cam=fc(seg(t,[(0,(0,-60,1.0)),(bt(6),(0,-120,1.3))]))
    palace(c,cam,t,tone=1)
    with layer(c,cam,1):person(c,0,250,420,'lwd',pose='kneel' if t>bt(3) else 'stand',t=t,eyes='closed')
    if t>bt(3.5):rect(c,0,0,W,H,'#000000',min(.6,(t-bt(3.5))*.5))
@nx(5,'','他没输给侯景，输给了{自己人}')
def f2(c,t,T):
    rect(c,0,0,W,H,'#0d0907');glow(c,W/2,H*.45,600,'#3a1210',.5)
    for i,s_ in enumerate(['熏香子弟','萧正德','柳仲礼','萧绎']):label(c,t,bt(.3+i*.5),s_,W*(.17+i*.22),H*.35,50,('#ff9a7a','#c0392b'))
    bigword(c,t,bt(2.6),'自己人',W/2,H*.65,130)
# ================= 结尾 =================
@nx(6,'','武备废弛、引狼入室、内鬼开门、援军观望')
def g1(c,t,T):
    rect(c,0,0,W,H,'#0d0907');glow(c,W/2,H*.5,800,'#5a3a14',.35)
    for i,s_ in enumerate(['武备废弛','引狼入室','内鬼开门','援军观望']):
        k=eback(cl((t-bt(.2+i*.5))/.35))
        if k<=0:continue
        x=W/2+(i-1.5)*300;y=H*.46
        c.save();c.translate(x,y);c.rotate((i-1.5)*.08);c.scale(k,k)
        rect(c,-115,-190,230,380,'#2a1a10');rect(c,-105,-180,210,360,'#e8dcbc');col(c,RED);c.set_line_width(6);c.rectangle(-95,-170,190,340);c.stroke()
        clib.vtext(c,s_,0,-120,64,'#7a1f1a');c.restore()
@nx(5,'','南梁不是被打垮的，是{自己散架的}')
def g2(c,t,T):
    rect(c,0,0,W,H,'#0d0907')
    k=ramp(t,bt(1),bt(3.5))
    r=random.Random(3)
    for i in range(16):
        x=W*.3+(i%4)*120;y=H*.3+(i//4)*80
        dx=r.uniform(-300,300)*k;dy=r.uniform(100,500)*k*k
        c.save();c.translate(x+dx,y+dy);c.rotate(r.uniform(-1,1)*k);rect(c,-56,-36,112,72,'#7a2a20');col(c,'#2a1a10');c.set_line_width(3);c.rectangle(-56,-36,112,72);c.stroke();c.restore()
    if t>bt(1):clib.htext(c,'梁',W*.48,H*.44,100,clib.IVORY,1-k)
    bigword(c,t,bt(3),'散架',W*.78,H*.3,130)
@nx(7,'','如果你是梁武帝，会不会收留侯景？')
def g3(c,t,T):
    rect(c,0,0,W,H,'#070504');glow(c,W/2,H*.45,700,'#3a2414',.6)
    with layer(c,(0,0,1.0),1):person(c,-450,280,420,'lwd',pose='stand',t=t,face=1);person(c,450,280,420,'hj',pose='kneel',t=t,face=-1)
    clib.htext(c,'？',W/2,H*.45,260,clib.GOLDG,cl(t*1.5)*(.85+.15*math.sin(t*3)))
