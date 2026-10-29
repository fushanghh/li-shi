from common import *
def zmap(c,t,cx,cy,z,**k):
    R=[('东 魏',(115,36.5),1),('梁',(115,30.5),1),('西 魏',(108.5,34.8),.8)]
    return G.basemap(c,cx,cy,z,t,regions=R,**k)
def cities(c,t,sc,names,red=(),size=42,big=1.2):
    for n in names:G.city(c,n,sc,t,state='red' if n in red else 'gold',size=size,big=big)
def field(c,cam,t,skyc=('#2a2418','#a8784a')):
    with layer(c,cam,.05):sky(c,skyc[0],skyc[1],-700,200)
    with layer(c,cam,.3):ridge(c,40,'#4a3a24',amp=50,seed=4)
WEI=crowd(71,120,-1600,1600,60,300,['dwsol','dwsol','xn'],('hold','stand'),50,140)
BP=crowd(72,70,-1600,1600,90,300,['bp','bp'],('hold','raise'),60,140)
HJ=crowd(73,60,-1500,1500,100,300,['dwsol','dwsol'],('hold','raise'),65,140)
# ================= 开场 =================
@nx(5,'507年·钟离','507年，{钟离之战}，梁军大破北魏','《梁书·韦叡传》')
def o1(c,t,T):
    sc=zmap(c,t,117.5,33,1.4)
    G.route(c,[(116.4,34.4),(117,33.6),(117.55,32.9)],ramp(t,.2,bt(1.5)),sc,h='#8a8a6a',lw=8,arrow=True)
    G.route(c,[(118.78,32.06),(118.2,32.5),(117.55,32.9)],ramp(t,bt(1.5),bt(3)),sc,h=RED,lw=8,arrow=True)
    cities(c,t,sc,['钟离','建康'],size=44)
    G.endmap(c)
    badge(c,t,bt(.5),W*.15,H*.3,'韦叡','梁将','#5a3a1a','韦',60)
    stamp(c,t,bt(3.2),'大破',W*.8,H*.24,100,.05)
@nx(5,'507年·钟离','魏军投水死者{十余万}','《梁书·韦叡传》：魏军……投水死者十余万')
def o2(c,t,T):
    cam=fc(seg(t,[(0,(0,-60,1.0)),(bt(5),(0,-30,.95))]))
    with layer(c,cam,.05):sky(c,'#1a1418','#6a3a2a',-700,100)
    with layer(c,cam,1):
        rect(c,-2600,60,5200,700,'#1a3040')
        r=random.Random(2)
        for i in range(60):x=r.uniform(-1800,1800);y=r.uniform(80,500);person(c,x,y,70,'dwsol',pose='fall',t=t)
        for i in range(20):x=r.uniform(-1800,1800);y=r.uniform(80,500);line(c,x+math.sin(t+i)*20,y,x+80,y,'#6a9aaa',2,.4)
    counter(c,t,'魏军溺亡',[(bt(.4)+i*.3,'%d万'%v) for i,v in enumerate([2,5,8,10])],note='十余万',h=RED)
@nx(6,'528—529年','529年，{陈庆之}率七千白袍军，打进{洛阳}','《梁书·陈庆之传》：麾下悉着白袍，所向披靡')
def o3(c,t,T):
    cam=fc(seg(t,[(0,(0,-60,1.0)),(bt(6),(250,-40,1.1))]))
    field(c,cam,t,('#2a2a3a','#c8a878'))
    with layer(c,cam,1):
        ground(c,150,'#5a4a30','#1a120a')
        draw_crowd(c,[dict(d,x=d['x']+t*80) for d in BP],t,march=.6)
        horse(c,200+t*80,320,170,1,t,gallop=.3,col_='#e8e4dc',rider='cqz')
    counter(c,t,'白袍军',[(bt(.4),'7000人')])
    badge(c,t,bt(1),W*.85,H*.28,'陈庆之','名师大将莫自牢','#c8c4bc','陈',60)
@nx(5,'548年','548年，一个被打得只剩{八百人}的叛将起兵')
def o4(c,t,T):
    cam=fc(seg(t,[(0,(0,-60,1.0)),(bt(5),(0,-90,1.2))]))
    field(c,cam,t,('#1a1010','#6a2a14'))
    with layer(c,cam,1):
        ground(c,150,'#3a2014','#100604')
        for i in range(6):person(c,-700+i*120,300,200,'dwsol',pose='stand',t=t,face=1,eyes='closed')
        person(c,200,290,420,'hj',pose='raise',t=t,face=1)
    badge(c,t,bt(.5),W*.82,H*.3,'侯景','东魏叛将','#3a2a1a','侯',70)
    counter(c,t,'残部',[(bt(1),'800人')],h=RED)
@nx(6,'549年·建康','第二年，他攻破{建康}，梁武帝{困死台城}')
def o5(c,t,T):
    cam=fc(seg(t,[(0,(0,-60,1.2)),(bt(6),(0,-60,1.0))]))
    with layer(c,cam,.05):sky(c,'#100808','#6a2414',-800,100)
    with layer(c,cam,.5):citywall(c,-2400,2400,-160,200);gatetower(c,0,-160,200,1.1,name='台城')
    with layer(c,cam,1):
        ground(c,200,'#2a1410','#0a0504')
        for x in (-900,-400,400,900):fire(c,x,200,2,t,seed=x)
    smoke(c,t,W/2,H*.3,4,12,colr='#100606',a=.5);embers(c,t,80,area=(0,0,W,H),a=.8)
    stamp(c,t,bt(2.5),'台城陷',W*.78,H*.22,100,.05)
@nx(6,'','南梁，为什么死在{侯景}手里？')
def o6(c,t,T):
    rect(c,0,0,W,H,'#0d0907');glow(c,W*.28,H*.45,500,GOLD,.25);glow(c,W*.72,H*.45,500,RED,.35)
    badge(c,t,.2,W*.25,H*.42,'梁武帝','在位48年','#9a7012','梁',120);badge(c,t,.5,W*.75,H*.42,'侯景','八百残兵','#3a2a1a','侯',120)
    clib.htext(c,'？',W/2,H*.52,260,clib.GOLDG,cl((t-bt(1.5))*2))
# ================= 第一层 =================
@nx(4,'')
def k1(c,t,T):card(c,t,'1','武备','从百战老兵到熏香子弟',label='第一层')
@nx(5,'梁初','梁初名将：{韦叡、曹景宗、陈庆之}')
def a1(c,t,T):
    rect(c,0,0,W,H,'#0d0907');glow(c,W/2,H*.45,700,'#5a3a14',.4)
    for i,(n,ch,colr) in enumerate([('韦叡','韦','#5a3a1a'),('曹景宗','曹','#7a2a20'),('陈庆之','陈','#c8c4bc')]):badge(c,t,bt(.3+i*.6),W*(.22+i*.28),H*.42,n,'名将',colr,ch,110)
@nx(5,'梁初','都是从血战里打出来的')
def a2(c,t,T):
    cam=fc(seg(t,[(0,(0,-60,1.0)),(bt(5),(0,-60,1.12))]))
    field(c,cam,t,('#1a1010','#7a3a1a'))
    with layer(c,cam,1):
        ground(c,150,'#3a2014','#100604')
        person(c,-300,290,400,'wr',pose='raise',t=t,face=1);person(c,300,290,400,'cqz',pose='raise',t=t,face=-1)
        for x in (-800,800):fire(c,x,260,1.2,t,seed=x)
    embers(c,t,60,area=(0,0,W,H),a=.7)
@nx(5,'梁中后期','几十年后，名将凋零')
def a3(c,t,T):
    rect(c,0,0,W,H,'#0d0907')
    for i,(n,ch,yr) in enumerate([('曹景宗','曹','508年卒'),('韦叡','韦','520年卒'),('陈庆之','陈','539年卒')]):
        badge(c,t,.1,W*(.22+i*.28),H*.42,n,yr,'#5a4a3a',ch,100)
        k=ramp(t,bt(.6+i*.7),bt(1+i*.7));col(c,'#000000',.6*k);c.arc(W*(.22+i*.28),H*.42,102,0,7);c.fill()
@nx(6,'梁·建康','贵族子弟{熏衣剃面，傅粉施朱}','《颜氏家训·勉学》：无不熏衣剃面，傅粉施朱')
def a4(c,t,T):
    cam=fc(seg(t,[(0,(0,-60,1.0)),(bt(6),(0,-110,1.3))]))
    palace(c,cam,t,tone=1)
    with layer(c,cam,1):
        for i,x in enumerate((-500,0,500)):person(c,x,250,380,'gz',pose='hold' if i!=1 else 'wave',t=t,face=1 if x<0 else -1)
        r=random.Random(1)
        for i in range(20):u=(t*.3+r.random())%1;circ(c,r.uniform(-700,700),lerp(150,-300,u),8,'#f0d0e0',(1-u)*.6)
    label(c,t,bt(1.5),'熏香 · 涂粉',W/2,H*.16,56)
@nx(5,'梁·建康','出门坐{长檐车}，城里{无人骑马}','《颜氏家训·涉务》：郊郭之内，无乘马者')
def a5(c,t,T):
    cam=fc(seg(t,[(0,(-200,-60,1.0)),(bt(5),(200,-60,1.08))]))
    with layer(c,cam,.05):sky(c,'#3a4050','#d8b890',-700,200)
    with layer(c,cam,.5):
        for i in range(8):house(c,-1500+i*420,150,320,140,'#6a4a3a','#2a1a14')
    with layer(c,cam,1):
        ground(c,170,'#6a5a40','#1a140a')
        for i in range(3):
            x=-800+i*700+t*40;rect(c,x-110,140,220,110,'#7a2a20');poly(c,[(x-150,140),(x+150,140),(x+110,100),(x-110,100)],'#3a1a10')
            circ(c,x-60,270,30,'#2a1a10');circ(c,x+60,270,30,'#2a1a10');person(c,x+200,300,200,'farm',pose='walk',t=t,face=1,lean=.3)
    xmark(c,t,bt(2),W*.85,H*.25,60);clib.htext(c,'马',W*.85,H*.25+25,70,clib.IVORY)
@nx(6,'梁·建康','建康令王复第一次见马嘶，吓得说：{这是老虎吧}','《颜氏家训·涉务》：正是虎，何故名为马乎')
def a6(c,t,T):
    cam=fc(seg(t,[(0,(0,-60,1.0)),(bt(6),(0,-80,1.2))]))
    with layer(c,cam,.05):sky(c,'#3a4050','#d8b890',-700,200)
    with layer(c,cam,1):
        ground(c,170,'#6a5a40','#1a140a')
        horse(c,300,300,260,-1,t,gallop=.6 if int(t*3)%2 else 0,col_='#6a4a2a')
        person(c,-300,300,360,'gz',pose='fall' if t>bt(2) else 'stand',t=t,face=1,eyes='wide',sweat=.9)
    if t>bt(1):clib.htext(c,'嘶——',W*.62,H*.3,80,clib.GOLDG,cl((t-bt(1))*3))
    label(c,t,bt(2.5),'正是虎，何故名为马乎',W*.5,H*.14,46)
# ================= 第二层 =================
@nx(4,'')
def k2(c,t,T):card(c,t,'2','对手','北朝修罗场里的狼',label='第二层')
@nx(5,'北魏·六镇','侯景是{六镇}出身')
def b1(c,t,T):
    sc=zmap(c,t,112,38.5,.7)
    G.city(c,'六镇',sc,t,state='red',pulse=1,big=1.5,size=46);cities(c,t,sc,['晋阳','洛阳','邺'],size=38)
    G.endmap(c)
    badge(c,t,bt(.5),W*.15,H*.3,'侯景','怀朔镇兵','#3a2a1a','侯',60)
@nx(6,'524—547年','经历过{尔朱荣、高欢、宇文泰}三代混战')
def b2(c,t,T):
    cam=fc(seg(t,[(0,(0,-60,1.0)),(bt(6),(200,-40,1.1))]))
    field(c,cam,t,('#1a1010','#7a3a1a'))
    with layer(c,cam,.7):ground(c,40,'#3a2414','#100804');draw_crowd(c,WEI,t,bob=2)
    for i,(n,ch) in enumerate([('尔朱荣','尔'),('高欢','高'),('宇文泰','宇')]):badge(c,t,bt(.4+i*.7),W*(.22+i*.28),H*.24,n,'',"#3a3a2a",ch,64)
@nx(6,'547年','高欢临终：能对付侯景的，{只有慕容绍宗}','《资治通鉴》卷160：可敌侯景者唯有慕容绍宗')
def b3(c,t,T):
    cam=fc(seg(t,[(0,(0,-60,1.0)),(bt(6),(0,-90,1.2))]))
    palace(c,cam,t,tone=1)
    with layer(c,cam,1):person(c,-250,250,380,'gh',pose='point',t=t,face=1,eyes='closed');person(c,300,250,420,'mrsz',pose='hold',t=t,face=-1)
    badge(c,t,bt(.5),W*.15,H*.26,'高欢','东魏权臣','#3a3a4a','高',56);badge(c,t,bt(2),W*.85,H*.26,'慕容绍宗','东魏名将','#2a3a2a','慕',56)
@nx(6,'547年·涡阳','547年，侯景叛东魏，在涡阳被慕容绍宗打得{只剩八百人}')
def b4(c,t,T):
    sc=zmap(c,t,116.5,33.3,1.6)
    G.route(c,[(115.5,34.3),(116,33.8),(116.2,33.5)],ramp(t,.2,bt(1.5)),sc,h='#5a8a5a',lw=8,arrow=True)
    G.route(c,[(116.2,33.5),(116.5,33),(116.78,32.58)],ramp(t,bt(2),bt(3.5)),sc,h=RED,lw=5,arrow=True)
    cities(c,t,sc,['涡阳','寿阳'],red=('涡阳',),size=44)
    G.endmap(c)
    counter(c,t,'侯景兵力',[(bt(.4),'4万'),(bt(1.6),'1万'),(bt(2.8),'800')],h=RED)
@nx(5,'','一只丧家之犬，却是{百战之狼}')
def b5(c,t,T):
    rect(c,0,0,W,H,'#0c0606');glow(c,W/2,H*.5,700,'#3a1010',.5)
    with layer(c,(0,-40,1.1),1):person(c,0,250,440,'hj',pose='stand',t=t,face=1,eyes='angry')
    stamp(c,t,bt(2),'狼',W*.78,H*.3,160,.05)
# ================= 第三层 =================
@nx(4,'')
def k3(c,t,T):card(c,t,'3','昏招','八十老翁的中原梦',label='第三层')
@nx(5,'547年·建康','八十多岁的{梁武帝}，想借侯景{收复中原}')
def c1(c,t,T):
    cam=fc(seg(t,[(0,(0,-60,1.0)),(bt(5),(0,-90,1.15))]))
    palace(c,cam,t)
    with layer(c,cam,1):person(c,0,250,440,'lwd',pose='raise',t=t,face=1)
    label(c,t,bt(1.5),'收复中原',W*.78,H*.2,56,clib.GOLDG)
@nx(5,'547年','不顾群臣反对，{接纳侯景}')
def c2(c,t,T):
    cam=fc(seg(t,[(0,(0,-200,.9)),(bt(5),(0,-120,1.08))]))
    palace(c,cam,t)
    with layer(c,cam,1):
        draw_crowd(c,crowd(74,14,-1100,1100,170,290,['toff','toff2'],('kneel',),150,180),t,bob=0)
        person(c,0,-40,280,'lwd',pose='wave',t=t)
    stamp(c,t,bt(2),'纳降',W*.78,H*.22,100,.05)
@nx(5,'547年','派侄子{萧渊明}率数万人北上')
def c3(c,t,T):
    sc=zmap(c,t,117.6,33.3,1.1)
    G.route(c,[(118.78,32.06),(118,33.2),(117.18,34.26)],ramp(t,.2,bt(3)),sc,h=RED,lw=8,arrow=True)
    cities(c,t,sc,['建康','彭城'],size=44)
    G.endmap(c)
    badge(c,t,bt(.4),W*.15,H*.3,'萧渊明','梁武帝之侄','#7a2a20','萧',60)
@nx(5,'547年·寒山','547年，{寒山}大败，萧渊明被俘')
def c4(c,t,T):
    cam=fc(seg(t,[(0,(0,-60,1.0)),(bt(5),(0,-40,.95))]))
    field(c,cam,t,('#1a1010','#6a2a14'))
    with layer(c,cam,1):
        ground(c,150,'#3a2014','#100604')
        r=random.Random(4)
        for i in range(14):person(c,r.uniform(-1300,1300),r.uniform(200,320),160,'lsol',pose='fall',t=t)
        person(c,0,300,300,'lsol',pose='kneel',t=t,bound=True,eyes='closed')
        for x in (-300,300):person(c,x,300,320,'mrsz' if x>0 else 'dwsol',pose='hold',t=t,face=1 if x<0 else -1)
    stamp(c,t,bt(2),'寒山大败',W*.75,H*.22,90,.05)
@nx(5,'547—548年','侯景趁乱夺下{寿阳}，梁武帝{顺手任命}')
def c5(c,t,T):
    sc=zmap(c,t,117.3,32.8,1.5)
    G.route(c,[(116.2,33.5),(116.5,33),(116.78,32.58)],ramp(t,.2,bt(2)),sc,h='#8a8a6a',lw=7,arrow=True)
    G.city(c,'寿阳',sc,t,state='red' if t>bt(2) else 'gold',pulse=1,big=1.5,size=46);cities(c,t,sc,['建康','涡阳'],size=40)
    G.endmap(c)
    if t>bt(2.5):
        sc_=slam(t,bt(2.5)) or 1;c.save();c.translate(W*.8,H*.28);c.scale(sc_,sc_);rect(c,-140,-170,280,340,'#e8dcbc');col(c,RED);c.set_line_width(6);c.rectangle(-130,-160,260,320);c.stroke();clib.vtext(c,'南豫州牧',0,-130,64,'#1a120c');c.restore()
@nx(6,'548年','有人报侯景要反，梁武帝笑：{折根棍子就能抽他}','《资治通鉴》卷161：景有几人，何能为！吾折棰笞之')
def c6(c,t,T):
    cam=fc(seg(t,[(0,(0,-60,1.0)),(bt(6),(0,-110,1.25))]))
    palace(c,cam,t)
    with layer(c,cam,1):
        person(c,-300,250,380,'toff',pose='kneel',t=t,face=1,sweat=.6)
        person(c,250,250,440,'lwd',pose='wave',t=t,face=-1)
        if t>bt(2):line(c,450,100,520,-60,'#6a4a2a',6)
    label(c,t,bt(2.2),'吾折棰笞之',W*.78,H*.18,56,clib.GOLDG)
