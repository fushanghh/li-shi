from common import *
ROWS=[('起兵原因','失期当斩，被逼','饥荒苛税，也被逼','g','g'),
      ('反的是谁','公认暴政的秦','后人怀念的唐','g','h'),
      ('对待百姓','未见屠城记载','屠城、洗城（史载）','g','x'),
      ('留下什么','自身速败，却首事亡秦','唐亡，五代乱世','h','x'),
      ('谁写历史','汉朝人司马迁','五代、宋的史官','g','x')]
RY=[-170+i*105 for i in range(5)]
def mark(c,x,y,kind,k):
    if k<=0:return
    sc=lerp(2.2,1,eo(k/1));a=cl(k*3)
    c.save();c.new_path();c.translate(x,y);c.scale(sc,sc)
    if kind=='g':col(c,GOLD,a);c.set_line_width(6);c.arc(0,0,22,0,6.3);c.stroke()
    elif kind=='h':col(c,'#9a8a70',a);c.set_line_width(5);path(c,[(0,-24),(22,16),(-22,16)]);c.stroke()
    else:line(c,-20,-20,20,20,RED,7,a);line(c,20,-20,-20,20,RED,7,a)
    c.restore()
def chen_fig(c,x,y,r):person(c,x-r*.15,y+r*1.95,r*2.5,'chen','stand',1,'calm',detail=True)
def huang_fig(c,x,y,r):person(c,x+r*.15,y+r*1.95,r*2.5,'huang','stand',-1,'proud',detail=True)
def scorecard(c,cam,t,nrows,cur=None,tcur=0):
    with layer(c,cam,.2):
        c.set_source(lgrad(c,0,-700,0,700,[(0,'#1a130c',1),(1,'#0e0a06',1)]));c.paint()
        glow(c,-450,-300,700,GOLD,.08);glow(c,450,-300,700,RED,.08)
    with layer(c,cam,1):
        rect(c,-800,-470,1600,880,'#241a10',.92);col(c,GOLD,.5);c.set_line_width(2);c.rectangle(-800,-470,1600,880);c.stroke()
        c.rectangle(-788,-458,1576,856);c.set_line_width(1);c.stroke()
        M.badge(c,-430,-360,62,'','',GOLD,1,1,chen_fig);M.badge(c,430,-360,62,'','',RED,1,1,huang_fig)
        text(c,'陈 胜',-300,-345,44,GOLD,sp=6,align='l');text(c,'前209',-300,-305,22,GREY,align='l')
        text(c,'黄 巢',300,-345,44,'#e8705a',sp=6,align='r');text(c,'875',300,-305,22,GREY,align='r')
        line(c,-760,-250,760,-250,GOLD,1.5,.4)
        for i in range(5):
            k=cl(nrows-i)
            if k<=0:continue
            y=RY[i];lab,l,r,ml,mr=ROWS[i]
            foc=(cur==i)
            if foc:rect(c,-790,y-48,1580,92,'#3a2a18',.8*cl(tcur/.3))
            a=k
            c.save();c.translate(lerp(-60,0,eo(k)),0)
            rect(c,-95,y-26,190,46,'#120c08',a);col(c,GOLD,.6*a);c.set_line_width(1.5);c.rectangle(-95,y-26,190,46);c.stroke()
            text(c,lab,0,y+8,28,'#efe2c4',a)
            c.restore()
            lt=cl((tcur-.5)/.3) if foc else (1 if (cur is None or i<cur) else 0)
            rt=cl((tcur-1.6)/.3) if foc else lt
            if cur is None and nrows<5:lt=rt=0
            c.new_path();text(c,l,-370,y+10,32,'#efe2c4',lt,shadow=1);text(c,r,370,y+10,32,'#efe2c4',rt,shadow=1)
            mark(c,-620,y,ml,cl((tcur-1.2)/.25) if foc else lt);mark(c,620,y,mr,cl((tcur-2.4)/.25) if foc else rt)
            line(c,-760,y+52,760,y+52,GOLD,1,.15*a)
def s_card(c,t,T):
    cam=seg(t,[(0,(0,-60,1.25)),(T,(0,-20,0.98))])
    scorecard(c,cam,t,cl(t/1.8)*5,None,0)
def mkrow(i):
    def f(c,t,T):
        y=RY[i]
        cam=seg(t,[(0,(0,y-40,1.0)),(.5,(0,y,1.32)),(T-.7,(0,y,1.38)),(T,(0,-20,1.0))])
        scorecard(c,cam,t,5,i,t)
        if i==2 and t>2.4:vignette_red(c,.3*cl((t-2.4)/.4))
    return f
def s_hgaozu(c,t,T):
    cam=seg(t,[(0,(0,-260,1.0)),(T,(0,-60,1.12))])
    with layer(c,cam,.05):sky(c,'#1e2420','#6a7460',-900,200);glow(c,300,-300,600,'#e8e0c0',.2)
    with layer(c,cam,.2):peaks(c,120,'#4a5446','#3a4436',8,9,140,260)
    with layer(c,cam,.4):
        for i in range(6):ell(c,-1600+i*600+t*30,40,500,60,'#c8ccc0',.18)
    with layer(c,cam,.7):
        ground(c,200,'#3a4232','#141810')
        ell(c,0,200,330,120,'#2a3024');c.arc(0,200,300,math.pi,2*math.pi);col(c,'#3a4430');c.fill()
        rect(c,-30,60,60,140,'#6a6458');text(c,'陈',0,110,30,'#1a1a14');text(c,'胜',0,145,30,'#1a1a14')
        for i in range(15):
            for side in (-1,1):
                x=side*(420+(i%5)*150);y=150+(i//5)*70
                house(c,x,y,110,50,'#5a5444','#2a2a24',door=False)
        for x in (-80,80):
            line(c,x,230,x,180,'#8a6a3a',4);smoke(c,t,x,170,.3,6,int(x),'#c8c8c0',.4,40)
        for i,x in enumerate([-260,-170,170,260]):person(c,x,300,190,'tangoff2' if i%2 else 'scholar','hands',1 if x<0 else -1,'calm')
    counter(c,'汉高祖下令','守冢三十家','在砀为陈胜守墓，世代祭祀',t-.4)
def s_flaws(c,t,T):
    if t<2.6:
        cam=seg(t,[(0,(0,0,0.95)),(2.6,(-80,-20,1.08))])
        with layer(c,cam,.2):
            c.set_source(lgrad(c,0,-700,0,400,[(0,'#1a0c08',1),(1,'#3a1810',1)]));c.paint()
            for i in range(-6,7):rect(c,i*260-22,-700,44,1000,'#1a1210');rect(c,i*260-22,-700,8,1000,'#5a2014')
            rect(c,-300,-380,600,300,'#2a1a10');poly(c,[(-280,-100),(-120,-260),(0,-180),(140,-300),(280,-100)],'#5a3a20')
        with layer(c,cam,.7):
            ground(c,250,'#2a140c','#0c0604')
            poly(c,[(-300,250),(300,250),(240,90),(-240,90)],'#4a1a10',1,GOLD,2)
            person(c,0,90,300,'chu','sit',1,'angry','frown')
            person(c,560,262,330,'farmer','shout',-1,'angry','open')
            person(c,430,262,340,'tangsol','sword',1,'angry','closed',weapon='sword')
            person(c,700,262,340,'tangsol','point',-1,'angry','closed',weapon='spear')
            for i,x in enumerate([-560,-720,-860]):person(c,x,262+i*10,320,'chu','stand' if i else 'stand2',-1,'sad','frown')
        if t>.6:
            c.save();x,y=1460,330;c.select_font_face(FONT,0,1)
            a=cl((t-.6)/.2);rect(c,x-110,y-60,220,80,'#efe2c4',.9*a);poly(c,[(x-20,y+20),(x+10,y+20),(x-40,y+60)],'#efe2c4',.9*a)
            text(c,'夥颐！',x,y-6,40,'#2a1a10',a);c.restore()
        return
    tt=t-2.6
    cam=(-720,-80,lerp(2.0,2.3,tt/2.4))
    with layer(c,cam,.2):c.set_source(lgrad(c,0,-700,0,400,[(0,'#1a0c08',1),(1,'#3a1810',1)]));c.paint()
    with layer(c,cam,1):
        ground(c,250,'#2a140c','#0c0604')
        for i,x in enumerate([-560,-720,-860]):person(c,x,262+i*10,320,'chu','stand',-1 if tt<.6 else 1,'sad','frown')
    stamp(c,'众叛亲离',W/2+330,300,t,3.4,96,-5)
def s_answer(c,t,T):
    z=seg(t,[(0,1.0),(T,.82)])
    s=M.basemap(c,114,31.5,z,t,())
    M.route(c,[M.CITIES['大泽乡'],M.CITIES['蕲'],(115.4,33.9),M.CITIES['陈']],1,s,GOLD,4,head=False)
    M.route(c,M.smooth([M.CITIES[n] for n in ['冤句','郓州','汝州','洪州','越州','福州','广州','桂州','潭州','江陵','宣州','泗州','汝州','洛阳','潼关','长安']],10),1,s,RED,4,head=False,a=.85)
    M.city(c,'大泽乡',s,t,'gold',pulse=1);M.city(c,'长安',s,t,'red',pulse=1)
    M.endmap(c)
    rect(c,0,0,W,H,'#000000',.4*cl((t-1.5)/.5))
    for j,(w,x,y) in enumerate([('反的是谁',560,380),('伤了多少百姓',W-560,380),('留下了什么',560,600),('谁来写历史',W-560,600)]):
        chip(c,w,x,y,t,2.0+j*.55,GOLD if j%2==0 else '#f2c48a',46)
def s_end(c,t,T):
    z=lerp(1.08,1.0,ease(t/T))
    c.save();c.translate(W/2,H/2);c.scale(z,z);c.translate(-W/2,-H/2)
    c.set_source(lgrad(c,0,0,0,H,[(0,'#120c08',1),(1,'#1e150c',1)]));c.paint()
    k=eo(t/1.2);w=lerp(60,1500,k)
    rect(c,W/2-w/2,150,w,640,'#d8c49a');rect(c,W/2-w/2-26,140,26,660,'#5a3a20');rect(c,W/2+w/2,140,26,660,'#5a3a20')
    if k>.95:
        cols=[('陈胜','前209 大泽乡起兵','反暴秦 · 六月而亡','首事亡秦 · 汉为置守冢',GOLD),('黄巢','875 起兵','881 入长安称帝','884 败亡 · 屠城载于史册',RED)]
        for j,(nm,a1,a2,a3,cc) in enumerate(cols):
            x=W/2+(350 if j==0 else -350)
            a=cl((t-1.2-j*.4)/.4)
            vtext(c,nm,x+150,230,56,'#7a1f1a' if j else '#5a3a10',a)
            for q,s_ in enumerate([a1,a2,a3]):
                circ(c,x+50-q*90,215,7,RED,a);vtext(c,s_,x+50-q*90,250,26,'#2a1a10',a)
    c.restore()
    stamp(c,'刀 口 向 谁',W/2,890,t,2.8,72,-3)
