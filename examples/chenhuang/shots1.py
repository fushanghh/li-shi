from common import *
# ================= HOOK =================
def s_hook1(c,t,T):
    # split screen: left Chen (gold dawn), right Huang (red fire)
    k=ease(t/T)
    def left(c):
        cam=(lerp(-520,-470,k),lerp(40,-20,k),1.05+.06*k)
        with layer(c,cam,.1):sky(c,'#1a1208','#7a4a1e',-700,300)
        with layer(c,cam,.2):glow(c,-600,120,700,'#e8a040',.35);clouds(c,t,'#3a2614',.5,8,3,(-450,-150),10)
        with layer(c,cam,.25):circ(c,-1100,60,90,'#f2c46a',.5);glow(c,-1100,60,300,'#f2c46a',.3)
        with layer(c,cam,.35):peaks(c,250,'#4a3420','#2e2014',7,4,120,260,-2000,200)
        with layer(c,cam,.55):
            ridge(c,280,'#2a1e12',50,7,-2200,600)
            for i,x in enumerate(range(-1700,-200,170)):tree(c,x,285,.9,'#241a10','#1a120a','round' if i%3 else 'willow',t=t)
            for x in (-1300,-1000,-700):banner(c,x,300,200,t,'楚',RED,1,1.2,seed=x)
        with layer(c,cam,.7):
            ridge(c,300,'#1c140c',40,2,-2000,800)
            draw_crowd(c,CR_HOOK_L,t,3)
        with layer(c,cam,1.0):
            poly(c,[(-1100,330),(-900,215),(-700,330)],'#120c08')
            person(c,-900,222,250,'chen','hoe_up',1,'angry','open',weapon='hoe')
    def right(c):
        cam=(lerp(470,520,k),lerp(-20,40,k),1.05+.06*k)
        with layer(c,cam,.1):sky(c,'#1a0606','#8a2414',-700,300)
        with layer(c,cam,.3):
            ridge(c,180,'#2a0e0a',30,5,-200,2400)
            for i in range(9):house(c,200+i*190,180,150,70,'#2a1410','#140808',door=False,burn=1)
            for i in range(6):fire(c,260+i*260,120,1.2,t,i)
            smoke(c,t,700,40,2,8,1,'#120606',.5)
        with layer(c,cam,.7):draw_crowd(c,CR_HOOK_R,t,3)
        with layer(c,cam,1.0):horse(c,880,330,230,-1,t,True,'#5a3a24',rider='huang',rpose='sword',rweapon='gsword')
        with layer(c,cam,1.2):embers(c,t,50,4,(0,-600,1200,1200))
    off=lerp(30,0,eo(t/1))
    sl=[(0,0),(W/2+80+off,0),(W/2-80-off,H),(0,H)];sr=[(W/2+80+off,0),(W,0),(W,H),(W/2-80-off,H)]
    c.save();path(c,sl);c.clip();left(c);c.restore()
    c.save();path(c,sr);c.clip();right(c);c.restore()
    line(c,W/2+80+off,0,W/2-80-off,H,'#f2d48a',4,.9);glow(c,W/2,H/2,240,'#f2d48a',.15)
    a=cl((t-.6)/.4)
    text(c,'陈 胜',300,170,58,GOLD,a,shadow=1,sp=10);text(c,'前209年 · 大泽乡',300,214,24,'#c9b88e',a)
    text(c,'黄 巢',W-300,170,58,'#e8705a',a,shadow=1,sp=10);text(c,'880年 · 长安',W-300,214,24,'#c9b88e',a)
    k2=t-2.0
    if k2>0:
        sc=lerp(2.2,1,eo(k2/.18));c.save();c.translate(W/2,H/2-40);c.scale(sc,sc)
        rect(c,-330,-90,660,130,'#000000',.55*cl(k2/.2))
        text(c,'同样是造反',0,10,100,'#efe2c4',cl(k2/.12),sp=16,shadow=1);c.restore()
CR_HOOK_L=crowd_grid(11,90,-1500,-250,300,360,['qinsol','qinsol2','qinsol3','chu'],['cheer','shout','raise'],40,70,['pole','flag',None,'hoe'])
CR_HOOK_R=crowd_grid(12,90,250,1600,300,360,['hsol','hsol2','huang'],['cheer','sword','raise'],40,70,['spear','gsword','flag',None],faces=(-1,))
def book(c,x,y,title,sub,colr,t,open_k=1):
    # bound book on table
    rect(c,x-230,y-300,460,600,'#2a1a10');rect(c,x-220,y-290,440,580,'#d8c49a')
    for k in range(9):line(c,x-200+k*48,y-260,x-200+k*48,y+260,'#b8a070',1,.6)
    c.select_font_face(FONT,0,1)
    vtext(c,title,x+150,y-230,40,'#2a1a10')
    r=random.Random(int(x))
    for col_ in range(6):
        for row in range(11):
            if r.random()<.85:rect(c,x+80-col_*48-9,y-210+row*42,18,26,'#3a2a1c',.55)
    rect(c,x+120,y-260,60,4,colr,.8)
def s_hook2(c,t,T):
    cam=seg(t,[(0,(-430,-40,1.55)),(1.6,(-400,-20,1.5)),(2.3,(430,-20,1.5)),(3.2,(450,0,1.45)),(4.0,(0,40,0.95)),(4.5,(0,40,0.92))])
    with layer(c,cam,.4):
        c.set_source(lgrad(c,0,-700,0,700,[(0,'#1a1209',1),(1,'#2a1c10',1)]));c.paint()
        glow(c,0,-200,900,'#e8a040',.18)
    with layer(c,cam,1):
        rect(c,-1200,330,2400,600,'#1c120a')
        book(c,-430,0,'史记·陈涉世家','',GOLD,t);book(c,430,0,'新唐书·逆臣传','',RED,t)
        stamp(c,'世 家',-470,40,t,1.0,110,-8)
        stamp(c,'逆 臣',390,40,t,2.6,110,6)
        text(c,'与诸侯同列',-430,230,34,'#7a1f1a',cl((t-1.3)/.3))
        text(c,'与叛贼同卷',430,230,34,'#7a1f1a',cl((t-2.9)/.3))
    with layer(c,cam,1.4):
        glow(c,-900,-300,300,'#ffb04a',.2);
    petals(c,t,25,'#d9b56a',.35,9)
def s_hook3(c,t,T):
    z=seg(t,[(0,.75),(2.2,.85),(T,2.6)])
    s=M.basemap(c,113,33,z,t)
    M.route(c,[M.CITIES['大泽乡'],M.CITIES['陈']],1,s,GOLD,3,head=False,a=.6)
    M.route(c,M.smooth([M.CITIES[n] for n in ['冤句','洪州','广州','潭州','泗州','洛阳','长安']]),1,s,RED,3,head=False,a=.6)
    M.endmap(c)
    rect(c,0,0,W,H,'#000000',.45)
    def chen(c,x,y,r):person(c,x-r*.2,y+r*1.9,r*2.4,'chen','stand',1,'calm',detail=True)
    def huang(c,x,y,r):person(c,x+r*.2,y+r*1.9,r*2.4,'huang','stand',-1,'proud',detail=True)
    a=cl(t/.3)
    M.badge(c,560,430,110,'陈胜','美誉 · 千古首义',GOLD,1,a,chen)
    M.badge(c,W-560,430,110,'黄巢','差评 · 屠城逆贼',RED,1,a,huang)
    # zigzag
    pts=[];n=16
    for i in range(n+1):pts.append((lerp(700,W-700,i/n),430+(18 if i%2 else -18)))
    kk=cl((t-.3)/.5);col(c,RED,.8*kk);c.set_line_width(3);path(c,pts[:max(2,int(len(pts)*kk))],False);c.stroke()
    shake(c,t,1.0,22)
    stamp(c,'凭 什 么',W/2,760,t,1.0,120,-4)
