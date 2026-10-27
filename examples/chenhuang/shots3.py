from common import *
from shots2 import QIN_REG
R=random.Random(77);RESP=[(R.uniform(111,120),R.uniform(31,38)) for _ in range(40)]
def s_chenmap(c,t,T):
    cx=seg(t,[(0,116.6),(3,115.6),(T,113.5)]);cy=seg(t,[(0,33.6),(3,33.8),(T,34.6)])
    z=seg(t,[(0,1.9),(3,1.55),(T,.95)])
    s=M.basemap(c,cx,cy,z,t,QIN_REG)
    M.city(c,'咸阳',s,t,'red')
    main=[M.CITIES['大泽乡'],M.CITIES['蕲'],(116.6,33.62),(116.1,33.75),(115.4,33.9),M.CITIES['陈']]
    M.route(c,main,t/2.0,s,GOLD,4)
    for nm,t0 in (('大泽乡',0),('蕲',.4)):M.city(c,nm,s,t,'gold',a=cl((t-t0)/.3),ly=24 if nm=='蕲' else -10)
    if t>1.9:M.city(c,'陈',s,t,'gold',pulse=1,size=30,a=cl((t-1.9)/.3))
    br=[([M.CITIES['陈'],(113.8,34.3),M.CITIES['荥阳']],3.4,'吴广'),([M.CITIES['陈'],(112,34.6),(110.5,34.5),M.CITIES['戏']],3.7,'周文'),([M.CITIES['陈'],(115,35.4),M.CITIES['邯郸']],4.0,'武臣')]
    for pts,t0,nm in br:
        e=M.route(c,pts,(t-t0)/1.6,s,GOLD,3)
        if e and t>t0+.3:text(c,nm,e[0]+10*s,e[1]-12*s,20*s,GOLD,cl((t-t0-.3)/.3),align='l',shadow=1)
    for i,(lo,la) in enumerate(RESP):
        t0=4.0+i*.05
        if t>t0:
            x,y=M.P(lo,la);a=cl((t-t0)/.3);glow(c,x,y,18*s,GOLD,.5*a);circ(c,x,y,3.5*s,'#f2d48a',a)
    M.endmap(c)
    counter(c,'抵达陈县时','数万人','车六七百乘，骑千余',t-.6)
    if t>2.2:
        x=W/2+lerp(0,-300,ease((t-2.2)/3));stamp(c,'张 楚',W/2+330,330,t,2.2,110,-6,sub='陈胜称王 · 国号')
def s_chenfall(c,t,T):
    if t<2.0:
        cam=(lerp(-100,200,t/2),-40,1.0)
        with layer(c,cam,.05):sky(c,'#06080e','#1a2230',-800,200);circ(c,-500,-360,36,'#cfd6e6',.5)
        with layer(c,cam,.25):peaks(c,120,'#10141c','#0c0f14',9,8,140,260)
        with layer(c,cam,.55):
            ridge(c,170,'#0c0f14',20,3)
            for i,x in enumerate(range(-2400,2600,180)):tree(c,x-t*0,180,.9,'#0a0c10','#08090c','dead' if i%3==0 else 'round',t=t)
        with layer(c,cam,1):
            ground(c,240,'#14161a','#08090a')
            cx_=-200+t*260
            # cart
            poly(c,[(cx_-120,200),(cx_+80,200),(cx_+70,140),(cx_-110,140)],'#3a2a1c',1,INK,2)
            for wx in (cx_-80,cx_+40):
                circ(c,wx,230,46,INK);circ(c,wx,230,40,'#2a1e14')
                for q in range(8):an=q/8*6.28+t*6;line(c,wx,230,wx+math.cos(an)*38,230+math.sin(an)*38,'#4a3a2a',3)
            horse(c,cx_+260,255,140,1,t,False,'#3a3028')
            person(c,cx_+100,170,200,'driver','stand',1,'calm' if t<1.4 else 'angry',weapon=None)
            person(c,cx_-40,150,220,'chu','sit',1,'sad')
        return
    tt=t-2.0
    if tt<.9:
        z=lerp(2.6,3.4,tt/.9)
        cam=(330,-20,z)
        with layer(c,cam,.05):sky(c,'#06080e','#1a2230',-800,200)
        with layer(c,cam,1):
            person(c,300,170,220,'driver','sword',1,'angry','frown',weapon='sword')
        vignette_red(c,.4*tt)
        return
    tt2=tt-.9
    cam=(0,-40,lerp(1.05,1.0,tt2/1.6))
    with layer(c,cam,.05):sky(c,'#100406','#3a1010',-800,200)
    with layer(c,cam,.25):peaks(c,120,'#1a0c0c','#120808',9,8,140,260)
    with layer(c,cam,1):
        ground(c,240,'#1a1010','#080404')
        poly(c,[(-120,200),(80,200),(70,140),(-110,140)],'#2a1a14',1,INK,2)
        for wx in (-80,40):circ(c,wx,230,46,INK);circ(c,wx,230,40,'#1e1410')
        person(c,-150,240,220,'chu','stand',1,'calm',rot=-math.pi/2)
        person(c,200,250,220,'driver','stand2',-1,'calm',weapon='sword')
        for i in range(4):
            bx=-500+i*240+math.sin(t*3+i)*30;by=-300+math.cos(t*2+i)*20
            poly(c,[(bx-20,by),(bx,by+6),(bx+20,by),(bx,by-4+math.sin(t*14+i)*8)],INK)
    stamp(c,'六 个 月',W/2,300,t,2.95,96,-5)
def s_qinfall(c,t,T):
    z=seg(t,[(0,1.0),(T,1.35)]);cx=seg(t,[(0,112.5),(T,109.8)]);cy=34.3
    s=M.basemap(c,cx,cy,z,t,QIN_REG)
    srcs=[(118.5,34.7),(119.8,31.8),(117,37),(114.5,36.6),(112.5,32.5),(116.35,34.1)]
    for i,p in enumerate(srcs):
        pts=M.smooth([p,(lerp(p[0],108.7,.5),lerp(p[1],34.33,.5)+(.6 if i%2 else -.6)),M.CITIES['咸阳']],6)
        M.route(c,pts,(t-.3-i*.15)/2.4,s,GOLD,2.5,a=.85)
    M.city(c,'咸阳',s,t,'red' if t<3 else 'gold',pulse=1,size=28)
    if t>3:
        x,y=M.P(*M.CITIES['咸阳']);fire(c,x,y,.6*s,t,2,cl((t-3)/.3))
    M.city(c,'陈',s,t,'gold')
    M.endmap(c)
    stamp(c,'秦 亡',W/2+300,360,t,3.0,120,-6,sub='前207年')
def s_match(c,t,T,who='chen'):
    # same composition: silhouette raising weapon against huge backlight
    z=lerp(1.0,1.08,t/T)
    c.save();c.translate(W/2,H/2);c.scale(z,z);c.translate(-W/2,-H/2)
    if who=='chen':top,bot,gl='#1a1206','#8a5a1a','#f2c46a'
    else:top,bot,gl='#1a0404','#8a1a10','#ff6a3a'
    c.set_source(lgrad(c,0,0,0,H,[(0,top,1),(1,bot,1)]));c.paint()
    glow(c,W/2,620,700,gl,.55);circ(c,W/2,640,260,gl,.35)
    beams(c,W/2,640,t,12,gl,.06,1400,6.0)
    ridge(c,860,'#0a0604',40,3,0,W)
    tmp=surf();cc=cairo.Context(tmp)
    person(cc,W/2,880,640,'chen' if who=='chen' else 'huang','hoe_up' if who=='chen' else 'raise',1,'angry','open',weapon='hoe' if who=='chen' else 'gsword')
    cc.set_operator(cairo.OPERATOR_ATOP);col(cc,'#0a0604');cc.paint()
    c.set_source_surface(tmp);c.paint()
    if who=='huang':embers(c,t,60,3,(0,0,W,H),.8)
    else:petals(c,t,40,'#f2d48a',.5,3,(0,0,W,H))
    c.restore()
def s_matchA(c,t,T):s_match(c,t,T,'chen')
def s_matchB(c,t,T):
    s_match(c,t,T,'huang')
    a=cl((t-.5)/.4);text(c,'一千多年后',W/2,200,40,'#efe2c4',a,sp=12,shadow=1)
