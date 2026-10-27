from lib import *
from fig import person
from bg import palace,throne,citywall
import mapx as M
from mapx import P
def stamp(c,txt,x,y,t,t0,size=96,rot=-6):
    k=t-t0
    if k<0:return
    sc=lerp(2.4,1,eo(k/0.18)) if k<.18 else 1
    a=cl(k/0.12)
    c.save();c.translate(x,y);c.rotate(math.radians(rot));c.scale(sc,sc)
    c.select_font_face(FONT,0,1);c.set_font_size(size);w=sum(c.text_extents(ch)[4] for ch in txt)+size*.08*(len(txt)-1)
    pad=size*.28
    col(c,RED,.9*a);c.set_line_width(size*.08);c.rectangle(-w/2-pad,-size*.95,w+2*pad,size*1.25);c.stroke()
    text(c,txt,0,size*.02,size,RED,.92*a,sp=size*.08)
    rng=random.Random(len(txt))
    for i in range(40):circ(c,rng.uniform(-w/2-pad,w/2+pad),rng.uniform(-size*.95,size*.3),rng.uniform(1,4),'#1a120c',.55*a)
    c.restore()
def counter(c,label,num,note,t,a=1):
    a*=cl(t/0.5)
    g=cairo.LinearGradient(0,0,560,0);g.add_color_stop_rgba(0,0,0,0,.55*a);g.add_color_stop_rgba(1,0,0,0,0);c.set_source(g);c.rectangle(0,120,560,180);c.fill()
    text(c,label,70,165,28,GREY,a,align='l')
    text(c,num,70,240,72,GOLD,a,align='l')
    if note:text(c,note,72,280,22,GREY,a*.8,align='l')
def bubble(c,x,y,s,t,t0,a=1):
    k=cl((t-t0)/.25)
    if k<=0:return
    c.save();c.translate(x,y);c.scale(eback(k),eback(k))
    c.select_font_face(FONT,0,1);c.set_font_size(26);w=c.text_extents(s)[4]+36
    col(c,'#efe2c4',.92*a);c.rectangle(-w/2,-52,w,46);c.fill();poly(c,[(-8,-6),(8,-6),(0,8)],'#efe2c4',.92*a)
    text(c,s,0,-20,26,'#2a1a10',a);c.restore()
def petals(c,t,n=60,h='#efe2c4',a=.7,seed=1):
    r=random.Random(seed)
    for i in range(n):
        x0=r.uniform(0,W);sp=r.uniform(40,110);ph=r.uniform(0,H)
        y=(ph+t*sp)%(H+40)-20;x=x0+math.sin(t*1.2+i)*30-t*15
        x%=W;circ(c,x,y,r.uniform(2,4.5),h,a)
# ---------------- shots ----------------
def s_title(c,t,T):
    s=M.basemap(c,108,32,0.75+t*.02,t,regions=[('大 唐',(108,33,1))]);M.city(c,'长安',s,t,pulse=1,label=False);M.endmap(c)
    rect(c,0,0,W,H,'#000000',.45)
    n=int(lerp(1,36,eo(t/2.2)))
    text(c,f'{n}',W/2-40,520,260,GOLD,cl(t/.4),align='r')
    text(c,'年',W/2-20,520,110,GOLD,cl(t/.4),align='l')
    text(c,'装 疯 卖 傻',W/2,620,52,'#efe2c4',cl((t-1.2)/.5),sp=10)
    stamp(c,'唐宣宗',W/2+330,470,t,2.6,90,-8)
def s_prince(c,t,T):
    c.save();c.translate(-t*25,0);palace(c,t,'red')
    for i,(x,k) in enumerate([(380,'prince'),(560,'off2'),(820,'prince'),(1000,'off'),(1250,'prince')]):
        person(c,x,860,260,k,'stand',face=1 if i%2==0 else -1,arm=(25+15*math.sin(t*3+i),25+25*math.sin(t*2.2+i)))
    person(c,1720,860,190,'boy','stand',face=-1)
    c.restore()
    x=1720-t*25;glow(c,x,760,140,GOLD,.18)
    text(c,'光王 李忱',x,580,30,GOLD,cl((t-1)/.5))
    text(c,'（宪宗第十三子）',x,616,20,GREY,cl((t-1)/.5))
def s_banquet(c,t,T):
    palace(c,t,'red');throne(c,W/2,640)
    person(c,W/2,560,230,'emp','sit')
    for i,x in enumerate([300,470,1450,1620]):
        bob=-abs(math.sin(t*7+i))*10
        person(c,x,880,250,'prince' if i%2 else 'off2','raise' if (int(t*2)+i)%3==0 else 'point',face=1 if x<W/2 else -1,bob=bob)
    person(c,W/2,900,230,'boy','stand',face=1)
    bubble(c,470,580,'光叔，说句话呀！',t,1.0);bubble(c,1450,590,'哈哈哈哈',t,2.2)
    text(c,'……',W/2+40,620,40,'#efe2c4',cl((t-3.2)/.4))
def s_wuzong(c,t,T):
    palace(c,t,'red',dark=.25);throne(c,W/2,620)
    person(c,W/2,540,240,'emp','point' if t>1.5 else 'sit',face=1)
    for x in (650,1270):person(c,x,820,220,'eun','bow',face=1 if x<W/2 else -1)
    person(c,W/2,960,230,'boy','kneel',face=1)
    text(c,'唐武宗',W/2,250,30,GOLD,cl(t/.5));text(c,'（侄子）',W/2,284,20,GREY,cl(t/.5))
    stamp(c,'装 傻',W/2+330,880,t,4.0,80,-6)
def s_legend(c,t,T):
    palace(c,t,'night',dark=.35)
    x=lerp(400,1500,ease(t/T))
    person(c,x-70,900,240,'eun','hold',face=1,bob=-abs(math.sin(t*6))*8)
    person(c,x+70,900,240,'eun','hold',face=1,bob=-abs(math.sin(t*6+1))*8)
    c.save();c.translate(x,760);c.rotate(-0.1);person(c,-90,0,200,'boy','lie',face=1);c.restore()
    petals(c,t,50,'#cfd6e6',.5)
    stamp(c,'野 史',300,300,t,1.2,70,-10)
def timeline(c,t,y0,y1,events,cur_t,label_span=None):
    x0,x1=200,1720;Y=640
    col(c,'#8a7d68',.7);c.set_line_width(2);c.move_to(x0,Y);c.line_to(x1,Y);c.stroke()
    def X(yr):return lerp(x0,x1,(yr-y0)/(y1-y0))
    step=10 if y1-y0>40 else 5
    for yr in range((y0//step)*step,y1+1,step):
        if yr<y0:continue
        col(c,'#8a7d68',.7);c.move_to(X(yr),Y);c.line_to(X(yr),Y+12);c.stroke();text(c,str(yr),X(yr),Y+46,24,GREY)
    prog=lerp(y0,y1,ease(cur_t))
    col(c,RED,.9);c.set_line_width(5);c.move_to(x0,Y);c.line_to(X(prog),Y);c.stroke()
    glow(c,X(prog),Y,50,RED,.8)
    for i,(yr,lab,sub,h) in enumerate(events):
        if prog<yr:continue
        k=cl((prog-yr)/((y1-y0)*.05))
        hh=120+(i%2)*90
        col(c,h,.8*k);c.set_line_width(2);c.move_to(X(yr),Y);c.line_to(X(yr),Y-hh*eo(k));c.stroke()
        circ(c,X(yr),Y,6,h,k)
        text(c,lab,X(yr),Y-hh-18,30,'#efe2c4',k)
        if sub:text(c,sub,X(yr),Y-hh+12,20,h,k)
    return X
def s_tl1(c,t,T):
    rect(c,0,0,W,H,'#17110b')
    ev=[(810,'李忱出生','',GOLD),(820,'穆宗','哥哥',GOLD),(824,'敬宗','侄子',GOLD),(826,'文宗','侄子',GOLD),(840,'武宗','侄子',GOLD),(846,'宣宗','他自己',RED)]
    timeline(c,t,805,850,ev,t/(T-1.2))
    counter(c,'龙椅换人','5 位','父亲、哥哥、三个侄子',t)
def s_eunuch(c,t,T):
    palace(c,t,'night',dark=.2)
    cx=W/2
    for i in range(5):
        a=i/5*math.pi*2+t*.15;x=cx+math.cos(a)*300;y=880+math.sin(a)*40
        person(c,x,y,240,'eun','bow' if i%2 else 'point',face=1 if math.cos(a)<0 else -1)
    glow(c,cx,700,260,'#e8a040',.25)
    c.save();c.translate(cx,700);c.rotate(math.sin(t)*.05);rect(c,-90,-60,180,120,'#e6d3a8');
    for k in range(5):rect(c,-70+k*30,-40,6,80,'#2a1a10',.7)
    rect(c,40,10,36,36,RED,.85);c.restore()
    stamp(c,'皇太叔',W/2,330,t,3.4,84,-5)
    text(c,'宦官马元贽等',300,300,28,GOLD,cl((t-.5)/.5))
def s_rise(c,t,T):
    palace(c,t,'red');k=ease((t-1)/2)
    glow(c,W/2,450,lerp(100,700,k),'#ffd27a',.35*k)
    throne(c,W/2,640)
    person(c,W/2,560,lerp(230,250,k),'emp','raise' if t>2.2 else 'sit')
    for i in range(4):
        for sd in (-1,1):
            x=W/2+sd*(420+i*160);person(c,x,900+i*10,220,'off' if i%2 else 'off2','bow' if t>2.5 else 'stand',face=-sd)
    counter(c,'他装了','36 年','一朝登基，判若两人',t-1)
def s_lideyu(c,t,T):
    s=M.basemap(c,lerp(109,111,ease(t/T)),lerp(30,23,ease(t/T)),lerp(.95,.72,ease(t/T)),t)
    M.city(c,'长安',s,t,pulse=1)
    pts=[M.CITIES['长安'],M.CITIES['荆南'],M.CITIES['洛阳'],M.CITIES['潮州'],M.CITIES['崖州']]
    M.route(c,[M.CITIES['长安'],M.CITIES['荆南']],(t-.6)/1.2,s,RED)
    M.route(c,[M.CITIES['荆南'],M.CITIES['潮州']],(t-2)/1.5,s,RED)
    M.route(c,[M.CITIES['潮州'],M.CITIES['崖州']],(t-3.7)/1.5,s,RED)
    for nm,t0 in (('荆南',1.8),('潮州',3.5),('崖州',5.2)):
        if t>t0:M.city(c,nm,s,t,'red',pulse=(nm=='崖州'),a=cl((t-t0)/.3))
    M.endmap(c)
    counter(c,'权相','李德裕','荆南 → 潮州 → 崖州',t)
    stamp(c,'贬',1560,800,t,5.3,110,-8)
def s_study(c,t,T):
    palace(c,t,'night')
    rect(c,560,760,800,40,'#5a3a22');rect(c,600,800,30,180,'#3a2416');rect(c,1290,800,30,180,'#3a2416')
    for i in range(7):
        for j in range(min(6,int(2+t*.6+i%3))):rect(c,620+i*60,745-j*14,46,12,'#e6d3a8' if j%2 else '#cdb88a')
    for x in (520,1400):
        rect(c,x-6,650,12,110,'#7a5a3a');glow(c,x,630,120+6*math.sin(t*9+x),'#ffb050',.5);poly(c,[(x-7,645),(x+7,645),(x,612+3*math.sin(t*11+x))],'#ffd27a')
    person(c,1140,980,250,'emp','hold',face=-1)
    c.save();c.translate(1000,700);c.rotate(.15);rect(c,-80,-30,160,60,'#efe2c4');
    for k in range(int(cl(t/T)*8)):rect(c,60-k*18,-22,4,44,'#2a1a10')
    c.restore()
    counter(c,'大中年间','亲阅','刺史赴任，必先召见',t)
def s_hexi(c,t,T):
    s=M.basemap(c,lerp(104,100,ease(t/T)),37,lerp(.8,1.05,ease(t/T)),t,tibet=cl(t/1.5),regions=[('吐 蕃',(88,33,1)),('河 西',(98,40.6,1)),('陇 右',(103,35.2,1))])
    M.city(c,'长安',s,t,pulse=1)
    for nm in ('沙州','瓜州','肃州','甘州','凉州','鄯州','河州','秦州','原州','安乐州','伊州','西州'):
        M.city(c,nm,s,t,'red',a=cl((t-1.5)/1),size=20)
    M.endmap(c)
    counter(c,'河陇沦陷','86 年','763 — 849',t)
def s_849(c,t,T):
    s=M.basemap(c,105.5,35.5,lerp(1.5,1.65,t/T),t,tibet=1-0.35*cl((t-1)/3),regions=[('陇 右',(103,35.2,1))])
    M.city(c,'长安',s,t)
    for i,nm in enumerate(('秦州','原州','安乐州')):
        t0=1.2+i*.9;st='gold' if t>t0 else 'red'
        M.city(c,nm,s,t,st,pulse=t>t0,size=22)
        if t>t0:
            lo,la=M.CITIES[nm];M.flag(c,lo+.25,la+.15,s,a=cl((t-t0)/.3))
    for i,(lo,la) in enumerate([(106.6,35.4),(106.1,35.9),(106.0,36.4),(105.4,36.7),(106.4,36.9),(105.0,35.2),(106.8,36.2)]):
        t0=3.8+i*.25
        if t>t0:M.flag(c,lo,la,s,'关',cl((t-t0)/.25))
    M.endmap(c)
    counter(c,'不战而复','三州七关','849年 · 吐蕃内乱',t-1)
def s_gate(c,t,T):
    citywall(c,t,'dusk','延喜门')
    person(c,W/2,300,95,'emp','raise' if t>3 else 'stand')
    r=random.Random(2);n=26
    for i in range(n):
        x=120+i*(W-240)/n+r.uniform(-20,20);y=880+r.uniform(-20,20);hh=r.uniform(120,145)
        sw=2+i*0.12
        kind='tang' if t>sw else 'hu'
        jump=-abs(math.sin(t*6+i))*22 if t>sw else 0
        person(c,x,y,hh,kind,'wave' if t>sw else 'stand',face=1 if i%2 else -1,bob=jump)
    text(c,'河陇父老 千余人',300,160,30,GOLD,cl((t-.5)/.5))
    stamp(c,'归 唐',1550,240,t,6.5,80,-6)
def s_851(c,t,T):
    z=lerp(1.2,0.85,ease((t-2.5)/5));cx=lerp(96,102.5,ease((t-2.5)/5));cy=lerp(40,37.5,ease((t-2.5)/5))
    s=M.basemap(c,cx,cy,z,t,tibet=0.65*(1-cl((t-1)/4)),regions=[('河 西',(98,40.6,1))])
    M.city(c,'长安',s,t,pulse=t>7)
    zs=['沙州','瓜州','伊州','西州','肃州','甘州','凉州','鄯州','河州','兰州']
    for i,nm in enumerate(zs):
        t0=.8 if nm=='沙州' else 1.6+i*.3
        M.city(c,nm,s,t,'gold' if t>t0 else 'red',pulse=(nm=='沙州'),size=22)
    M.route(c,[M.CITIES['沙州'],M.CITIES['瓜州'],M.CITIES['肃州'],M.CITIES['甘州'],M.CITIES['凉州'],M.CITIES['兰州'],M.CITIES['秦州'],M.CITIES['长安']],(t-3)/4,s,GOLD,4)
    M.endmap(c)
    num=int(cl((t-1.6)/3)*11)
    counter(c,'张议潮 献图籍',f'{max(1,num)} 州','851年 · 沙州起兵',t)
    stamp(c,'河西归唐',1500,850,t,8.0,90,-6)
def s_dan(c,t,T):
    palace(c,'night' and t,'night',dark=.35)
    x=1200;rect(c,x-80,800,160,120,'#4a3a2a');poly(c,[(x-110,800),(x+110,800),(x+70,740),(x-70,740)],'#5a4a36')
    glow(c,x,760,200,'#ff7a30',.4+.1*math.sin(t*8))
    for i in range(10):
        k=((t*.35+i*.1)%1);circ(c,x+math.sin(k*6+i)*60*k,740-k*500,20+60*k,'#8a8070',.25*(1-k))
    person(c,700,950,250,'emp','hold',face=1)
    person(c,1420,950,230,'monk','point',face=-1)
    text(c,'丹 药',x,700,34,GOLD,cl((t-1)/.5),sp=8)
def s_death(c,t,T):
    palace(c,t,'grey',dark=.3);throne(c,W/2,640)
    petals(c,t,90,'#e8e4da',.65,3)
    stamp(c,'崩',W/2+460,420,t,2.2,150,-4)
    counter(c,'859年','50 岁','宣宗驾崩',t)
def s_tl2(c,t,T):
    rect(c,0,0,W,H,'#17110b')
    ev=[(859,'宣宗崩','懿宗即位',GOLD),(860,'裘甫起义','',RED),(868,'庞勋兵变','',RED),(875,'黄巢起兵','',RED),(880,'长安陷落','',RED),(907,'唐亡','',RED)]
    timeline(c,t,855,910,ev,t/(T-1.5))
    counter(c,'他走之后','48 年','859 — 907',t)
def s_end(c,t,T):
    rect(c,0,0,W,H,'#120d08')
    k=ease(t/1.5);w=lerp(60,1300,k)
    rect(c,W/2-w/2,190,w,560,'#2a2016');col(c,GOLD,.6);c.set_line_width(2);c.rectangle(W/2-w/2+16,206,w-32,528);c.stroke()
    for sx in (-1,1):rect(c,W/2+sx*w/2-14,170,28,600,'#5a3a22')
    items=[('810','李忱出生，宪宗第十三子'),('810—846','装傻三十六年'),('846','即位，罢李德裕'),('849','收复三州七关'),('851','张议潮献河西十一州'),('859','服丹而崩')]
    for i,(y,s) in enumerate(items):
        a=cl((t-1.5-i*.35)/.4)
        circ(c,W/2-480,280+i*76,7,RED,a);text(c,y,W/2-450,290+i*76,28,GOLD,a,align='l');text(c,s,W/2-260,290+i*76,30,'#efe2c4',a,align='l')
    vtext(c,'小太宗',W/2+500,300,64,GOLD,cl((t-4)/.6))
    stamp(c,'大中之治',W/2+380,690,t,5.0,56,-6)
