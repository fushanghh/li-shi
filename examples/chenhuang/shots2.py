from common import *
QIN_REG=[('秦',(108.5,35.6,1)),('楚 地',(116,32.2,1)),('赵',(114.5,37.6,.8)),('燕',(116.5,40.9,.8)),('齐',(118.6,36.4,.8))]
def s_qinmap(c,t,T):
    cx=seg(t,[(0,112.5),(2.5,115.5),(5.3,117.2),(T,117.4)]);cy=seg(t,[(0,35),(2.5,36.4),(5.3,33.6),(T,33.4)])
    z=seg(t,[(0,.62),(2.5,.95),(5.3,1.7),(T,2.4)])
    s=M.basemap(c,cx,cy,z,t,QIN_REG)
    M.city(c,'咸阳',s,t,'red',label=True)
    M.city(c,'渔阳',s,t,'gold',pulse=1)
    # planned route north (dashed)
    path_=[M.CITIES['大泽乡'],(116.9,35),(116.5,37.5),(116.6,39.2),M.CITIES['渔阳']]
    M.route(c,path_,(t-.6)/2.0,s,GOLD,3,dash=True,head=True,a=.85)
    if t>3:
        # cut back: route fails, rain at 大泽乡
        x,y=M.P(*M.CITIES['大泽乡'])
        a=cl((t-3)/.4)
        for i in range(5):ell(c,x+(i-2)*30*s,y-70*s+math.sin(t*2+i)*4*s,34*s,16*s,'#4a5466',.8*a)
        r=random.Random(2);col(c,'#9ab0c8',.7*a);c.set_line_width(1.4*s)
        for i in range(40):
            xx=x+r.uniform(-90,90)*s;yy=y-60*s+((r.uniform(0,80)+t*120)%80)*s
            c.move_to(xx,yy);c.line_to(xx-3*s,yy+10*s)
        c.stroke()
        # X on route
        xm,ym=M.P(116.8,36);k=cl((t-3.6)/.3)
        line(c,xm-18*s,ym-18*s,xm-18*s+36*s*k,ym-18*s+36*s*k,RED,5*s,k);line(c,xm+18*s,ym-18*s,xm+18*s-36*s*k,ym-18*s+36*s*k,RED,5*s,k)
    M.city(c,'大泽乡',s,t,'gold',pulse=1,size=26)
    M.endmap(c)
    n=int(lerp(0,900,eo((t-.3)/1.6)))
    counter(c,'闾左戍卒',f'{n} 人','征发北上，戍守渔阳',t-.3)
# ---- rain night at 大泽乡 ----
CR_CAMP=crowd_grid(21,260,-1600,1600,170,330,['qinsol','qinsol2','qinsol3'],['stand','stand2','hands','cower'],30,95,[None,None,'pole','bundle'])
def rainnight_bg(c,cam,t,flashk=0):
    with layer(c,cam,.05):
        sky(c,'#0a0d16','#222a38',-800,300)
        if flashk:col(c,'#b8c8ff',flashk*.5);c.paint()
    with layer(c,cam,.15):clouds(c,t,'#141822',.8,14,2,(-650,-250),40,sc=1.6)
    with layer(c,cam,.3):
        peaks(c,140,'#1a1e28','#12151c',9,3,180,360,-2600,2600)
    with layer(c,cam,.5):
        ridge(c,170,'#141820',30,4,-2600,2600)
        for i,x in enumerate(range(-2200,2300,260)):tree(c,x+((i*53)%80),175,.8,'#10141a','#0c0e12','willow' if i%2 else 'round',t=t*2)
        for i,x in enumerate(range(-1500,1600,420)):tent(c,x,180,.9,'#2a2a26',lit=(i%2==0))
    with layer(c,cam,.75):
        ground(c,200,'#1a1c1c','#0a0a0a')
        for i in range(10):ell(c,-1800+i*400,260+(i%3)*30,180,14,'#3a4658',.5)  # puddles
        draw_crowd(c,CR_CAMP,t,1.5)
    with layer(c,cam,1.0):splashes(c,t,240,360,70)
def s_rainwide(c,t,T):
    cam=seg(t,[(0,(-260,-160,1.0)),(T,(180,-20,1.18))])
    fl=lightning(c,t,.75,0,seed=3) if False else 0
    k=t-.75;fk=(1 if 0<k<.06 or .12<k<.18 else .3)*(1-k/.35) if 0<k<.35 else 0
    rainnight_bg(c,cam,t,fk)
    with layer(c,cam,.2):lightning(c,t,.75,500,-700,60,seed=3)
    with layer(c,cam,1.3):
        reeds(c,-1700,1700,520,t,'#0c0e0c',120,5,240)
    with layer(c,cam,1.0):
        # qin officer on horse
        horse(c,520,300,150,-1,t*.4,False,'#2a2220',rider='qinoff',rpose='point',rweapon=None,expr='angry')
    rain(c,t,520,.25,56,.5)
    flash(c,fk*.35)
def s_mudfeet(c,t,T):
    cam=(lerp(-200,250,t/T),0,1)
    with layer(c,cam,.2):
        sky(c,'#141822','#2a3240',-800,0)
        ridge(c,-120,'#181c24',40,6,-2000,2000)
    with layer(c,cam,.6):ground(c,-80,'#2a2a26','#141412')
    with layer(c,cam,1):
        # mud road
        c.set_source(lgrad(c,0,100,0,600,[(0,'#2e2a22',1),(1,'#1a1612',1)]));c.rectangle(-2000,60,4000,800);c.fill()
        for i in range(14):ell(c,-1500+i*260,200+(i%4)*70,90+(i%3)*40,18,'#465264',.55)
        # three walkers; huge figures so we only see legs
        for j,(x0,sp,hh,o) in enumerate([(-500,140,1500,'qinsol'),(150,120,1650,'qinsol2'),(800,150,1450,'qinsol3')]):
            x=x0+t*sp if not(j==1 and t>1.8) else x0+1.8*sp
            ph=t*.9 if not(j==1 and t>1.8) else 1.8*.9
            person(c,x,340+j*30,hh,o,walk(ph,run=False,amp=26),1,detail=True)
        # mud splash at foot
        for j in range(3):
            ph=(t*1.8+j*.33)%1
            ell(c,-300+j*450+t*130,440+j*40,30+ph*60,8+ph*10,'#3a3428',(1-ph)*.7)
    splashes(c,t,600,1000,40,11,.6)
    rain(c,t,420,.2,50,.45,seed=8)
def s_law(c,t,T):
    if t<1.5:
        cam=seg(t,[(0,(-80,-120,1.25)),(1.5,(0,-160,1.5))])
        with layer(c,cam,.1):
            c.set_source(lgrad(c,0,-700,0,400,[(0,'#0c0a0c',1),(1,'#1e1812',1)]));c.paint()
        with layer(c,cam,.5):
            # tent interior wall
            rect(c,-1500,-500,3000,800,'#2a2016');
            for k in range(-12,13):line(c,k*120,-500,k*120+40,300,'#1e160e',6,.8)
            glow(c,-300,-120,600,'#ffa040',.3)
        with layer(c,cam,1):
            ground(c,250,'#2a1e14','#120c08')
            person(c,-260,260,560,'qinoff','read',1,'angry','open',weapon='bamboo')
            fire(c,-620,250,1.0,t,1)
            for i,x in enumerate([200,420,640]):person(c,x,300+i*12,400,'qinsol' if i!=1 else 'wu','kneel',-1,'fear','open' if i==0 else 'frown')
        return
    tt=t-1.5
    z=lerp(1,1.18,tt/2)
    c.save();c.translate(W/2,H/2);c.scale(z,z);c.rotate(-.04);c.translate(-W/2,-H/2)
    c.set_source(lgrad(c,0,0,0,H,[(0,'#1e140c',1),(1,'#0e0906',1)]));c.paint()
    glow(c,W/2,H/2,900,'#ffa040',.22)
    # bamboo slips
    n=12;x0=W/2-n*58/2
    for k in range(n):
        x=x0+k*58;rect(c,x,150,50,760,'#c9a76a');rect(c,x+40,150,10,760,'#a8854a')
        line(c,x,250,x+50,250,'#4a3018',3,.8);line(c,x,800,x+50,800,'#4a3018',3,.8)
    cols=['失期','法皆斩','发闾左','適戍渔阳','九百人','会天大雨','道不通','度已失期']
    for k,s_ in enumerate(cols):
        x=x0+(n-1-k)*58+25
        hl=s_ in('失期','法皆斩')
        vtext(c,s_,x,300,40,'#7a1f1a' if hl else '#2a1a0c',1 if hl else .75)
    c.restore()
    stamp(c,'斩',W/2-230,640,t,2.1,190,-8)
def s_fish(c,t,T):
    if t<1.6:
        z=lerp(1.0,1.25,t/1.6)
        c.save();c.translate(W/2,H/2);c.scale(z,z);c.translate(-W/2,-H/2)
        rect(c,0,0,W,H,'#2a1c10');
        for k in range(8):rect(c,0,k*140,W,4,'#1a1008',.8)
        glow(c,W/2,H/2,800,'#ffa040',.25)
        # fish
        cx,cy=W/2-80,H/2+40
        ell(c,cx,cy,420,130,INK);ell(c,cx,cy,412,122,'#7a8a8a')
        ell(c,cx-20,cy-30,360,60,'#9aaaa8',.6)
        poly(c,[(cx+400,cy),(cx+560,cy-120),(cx+540,cy),(cx+560,cy+120)],'#6a7a7a',1,INK,3)
        circ(c,cx-330,cy-30,16,'#f4ead8');circ(c,cx-326,cy-30,8,INK)
        for k in range(10):c.arc(cx-200+k*55,cy,40,-1,1);col(c,'#5a6a6a',.6);c.set_line_width(3);c.stroke()
        # slit and silk
        poly(c,[(cx-150,cy+60),(cx+200,cy+70),(cx+180,cy+110),(cx-140,cy+100)],'#5a1a14')
        k=eo((t-.3)/.9)
        c.save();c.translate(cx+20,cy+80);c.rotate(-.25*k)
        rect(c,-60,-20-380*k,120,380*k+30,'#efe0c0')
        if k>.2:vtext(c,'陈胜王',0,-330*k+30,96*min(1,k*1.2),'#b8261c',cl((k-.2)/.4))
        c.restore()
        c.restore()
        return
    tt=t-1.6
    cam=(lerp(-100,60,tt/1.4),-60,lerp(1.1,1.25,tt/1.4))
    with layer(c,cam,.1):sky(c,'#06080e','#141a26',-700,300);circ(c,600,-380,40,'#cfd6e6',.6);glow(c,600,-380,200,'#cfd6e6',.12)
    with layer(c,cam,.4):
        ridge(c,120,'#0c0e14',60,9)
        for x in range(-1600,1700,140):tree(c,x,140,1.1,'#0a0c10','#08090c','pine' if x%280 else 'round',t=t)
        # shrine
        rect(c,280,20,180,120,'#1a140e');poly(c,[(240,30),(500,30),(370,-40)],'#0e0a08')
        fire(c,370,140,1.1,t,3)
        # fox silhouette
        fx=180+math.sin(t*2)*6
        poly(c,[(fx,140),(fx+20,100),(fx+50,95),(fx+60,70),(fx+68,92),(fx+80,96),(fx+60,110),(fx+50,140)],'#050405')
        poly(c,[(fx,140),(fx-50,120),(fx-60,128),(fx-10,145)],'#050405')
    with layer(c,cam,1):
        ground(c,240,'#10100e','#060605')
        for i,x in enumerate([-700,-420,-150]):tent(c,x,260,1.6,'#1a1a18',lit=i==1)
        person(c,-560,300,330,'qinsol2','cower',1,'fear','open')
        person(c,-300,320,350,'qinsol','stand2',1,'fear','open')
    text(c,'“大楚兴，陈胜王”',W-420,300,46,'#e8c97a',cl((tt-.3)/.4)*(.7+.3*math.sin(t*12)),shadow=1)
def s_kill(c,t,T):
    sl=1.0 if t<1.45 else .25  # slow motion after flash
    tt=t if t<1.45 else 1.45+(t-1.45)*.35
    cam=seg(t,[(0,(0,-60,1.15)),(1.4,(80,-80,1.45)),(1.5,(40,-60,1.0)),(T,(30,-60,1.08))])
    k=t-1.45;fk=(1-k/.4) if 0<k<.4 else 0
    c.save();shake(c,t,1.45,24)
    with layer(c,cam,.1):
        c.set_source(lgrad(c,0,-700,0,400,[(0,'#0c0a0c',1),(1,'#1e1812',1)]));c.paint()
    with layer(c,cam,.5):
        rect(c,-1500,-600,3000,900,'#2a2016')
        for kk in range(-12,13):line(c,kk*120,-600,kk*120+40,300,'#1e160e',6,.8)
        glow(c,0,-100,700,'#ffa040',.28)
    with layer(c,cam,1):
        ground(c,250,'#2a1e14','#120c08')
        # jars, table
        rect(c,-760,150,260,30,'#3a2414');ell(c,-700,140,26,30,'#5a3a20');ell(c,-600,140,22,28,'#5a3a20')
        if tt<1.0:
            person(c,120,260,520,'qinoff','whip',-1,'angry','open',weapon='sword')
            person(c,-180,262,500,'wu','cower',1,'angry','frown')
        elif tt<1.45:
            person(c,120,260,520,'qinoff','stand2',-1,'fear','open')
            person(c,-120,262,500,'wu','sword',1,'angry','open',weapon='sword')
        else:
            fk2=cl((tt-1.45)/.6)
            person(c,lerp(150,200,fk2),262,520,'qinoff','fall',-1,'fear','open',rot=lerp(0,math.pi/2*0.95,eo(fk2)))
            person(c,-80,262,500,'wu','slash',1,'angry','open',weapon='sword')
            person(c,-460,262,500,'chen','sword',1,'angry','open',weapon='sword') if tt>1.6 else None
    c.restore()
    if fk>0:
        col(c,'#ffffff',fk*.85);c.paint()
    if t>1.45:vignette_red(c,.5)
    stamp(c,'杀 尉',W-380,330,t,1.6,100,-8)
CR_SHOUT=crowd_grid(31,420,-1700,1700,260,520,['qinsol','qinsol2','qinsol3','wu'],['cheer','shout','raise'],60,180,['pole','hoe',None,'flag','pole'])
def s_shout(c,t,T):
    cam=seg(t,[(0,(0,40,0.95)),(1.5,(0,-40,1.02)),(2.1,(-150,-330,3.2)),(T,(-160,-340,3.45))])
    with layer(c,cam,.05):sky(c,'#100c10','#3a2418',-800,200);glow(c,0,-200,800,'#e86a2a',.25)
    with layer(c,cam,.15):clouds(c,t,'#1a1210',.7,12,7,(-600,-300),25,sc=1.5)
    with layer(c,cam,.35):peaks(c,180,'#1e1610','#140e0a',8,5,160,300)
    with layer(c,cam,.6):
        poly(c,[(-700,300),(-420,140),(420,140),(700,300)],'#1e140c')  # 涉故台
        for x in (-560,560):banner(c,x,150,260,t,'楚',RED,1,1.4,seed=x)
        for x in (-380,380):
            line(c,x,150,x,40,'#2a1c10',4);fire(c,x,40,.7,t,x)
    with layer(c,cam,.6):
        person(c,0,142,420,'chen','shout',1,'angry','open',weapon='hoe' if False else None)
        person(c,-220,142,360,'wu','raise',1,'angry','open',weapon='sword')
    with layer(c,cam,1.0):
        draw_crowd(c,CR_SHOUT,t,6)
    rain(c,t*(.35 if t>2.1 else 1),200,.15,40,.3,seed=12)
    k=t-2.0
    if k>0:
        a=cl(k/.15)
        for j,(s_,x) in enumerate([('王侯将相',W-380),('宁有种乎',W-250)]):
            kk=cl((k-j*.3)/.2);sc=lerp(1.8,1,eo(kk))
            c.save();c.translate(x,200);c.scale(sc,sc);vtext(c,s_,0,0,96,'#f2d48a' if j==0 else '#ff6a4a',kk,shadow=1);c.restore()
    embers(c,t,30,7,(0,0,W,H),.6)
CR_POLES=crowd_grid(41,1500,-2400,2400,40,560,['qinsol','qinsol2','qinsol3','chu','farmer','farmer2'],['cheer','raise','carry','shout'],22,170,['pole','pole','flag','hoe',None])
def s_poles(c,t,T):
    cam=seg(t,[(0,(-500,-60,1.1)),(T,(450,-40,1.0))])
    with layer(c,cam,.05):sky(c,'#24100a','#c06a2a',-800,100);circ(c,0,60,120,'#ffd27a',.8);glow(c,0,60,600,'#ffb04a',.45)
    with layer(c,cam,.15):clouds(c,t,'#5a2a14',.6,10,8,(-500,-200),15,sc=1.6)
    with layer(c,cam,.3):peaks(c,90,'#4a2a18','#341c10',10,6,120,240)
    with layer(c,cam,.7):draw_crowd(c,CR_POLES,t,5)
    with layer(c,cam,1.0):dust(c,t,-1500,1500,560,40,3,'#8a5a30',.3,2)
    stamp(c,'揭竿而起',W/2,300,t,1.0,110,-5)
