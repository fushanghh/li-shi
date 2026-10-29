import json
exec(open('score.py').read().split('# ---- 0-24')[0].replace('NB=216','NB=346').replace('B=60/96','B=60/100'))
import kinetic
import render
SH=render.SH
SB=['groove']*346  # 每拍段落
def sec(a,b_,m):
    for i in range(a,b_):SB[i]=m
for a,b_,m in [(0,12,'hook'),(12,14,'drop'),(14,24,'hook'),(24,30,'epic'),(30,34,'card'),(34,40,'groove'),(40,52,'epic'),(52,64,'dark'),(64,68,'drop'),(68,76,'epic'),
 (76,82,'groove'),(82,90,'march'),(90,96,'dark'),(96,100,'card'),(100,110,'build'),(110,120,'war'),(120,128,'build'),(128,132,'hit'),(132,146,'soft'),(146,154,'heavy'),
 (154,160,'build'),(160,164,'card'),(164,172,'march'),(172,180,'groove'),(180,190,'war'),(190,196,'dark'),(196,204,'heavy'),(204,212,'epic'),(212,216,'card'),(216,224,'march2'),
 (224,230,'dark'),(230,238,'groove'),(238,246,'build'),(246,252,'chase'),(252,258,'war'),(258,264,'epic'),(264,268,'card'),(268,282,'groove'),(282,292,'heavy'),(292,300,'soft'),
 (300,308,'war'),(308,316,'build'),(316,326,'march'),(326,342,'finale'),(342,346,'end')]:sec(a,b_,m)
ST=[0]*346
for gb in range(346):ST[gb]=gb if gb==0 or SB[gb]!=SB[gb-1] else ST[gb-1]
NX=[0]*346
for gb in range(345,-1,-1):NX[gb]=gb+1 if gb==345 or SB[gb+1]!=SB[gb] else NX[gb+1]
CH=[[D,D+3,D+7],[D-4,D,D+3],[D-2,D+2,D+5],[D-5,D-1,D+2]]   # Dm Bb C A
RT=[D-12,D-16,D-14,D-17]
THEME=[(9,1),(10,.5),(11,.5),(12,2),(11,1),(10,1),(9,1),(10,1),(7,2),(9,1),(10,1),(12,1.5),(14,.5),(12,1),(11,1),(10,1),(9,1),(7,2)]
def theme_at(gb,base):
    tot=sum(d for _,d in THEME);x=gb%tot;acc=0
    for i,(dg,du) in enumerate(THEME):
        if abs(x-acc)<1e-6:return dg,du
        acc+=du
    return None
def tk(t,g=.7,f=58):put(ca(('tk',f),lambda:taiko(f)),t,g,0,.15)
def kk(bb,g=.85):kickat(bb,g)
for gb in range(346):
    m=SB[gb];st=ST[gb];nx=NX[gb];bar=gb//4;bi=gb%4;ch=CH[bar%4];rt=RT[bar%4];t=b(gb)
    if m=='hook':
        # 每拍大鼓+八分底鼓，逐步加密；弦乐十六分音推进；铜管每小节
        kk(gb,.9);tk(t,.6)
        if gb>=8:kk(gb+.5,.5)
        put(ca('sn',snare),t+B/2,.35 if gb<8 else .5)
        for q in range(4):put(ca(('ss',ch[q%3]+12),lambda:strings_stac(ch[q%3]+12)),t+q*B/4,.45,(-.3,.3)[q%2])
        if gb>=16:[put(ca('h',hat),t+q*B/4,.3,.4) for q in range(4)]
        if bi==0:put(pad(ch,b(4),1400),t,.35,0,.3);put(bass(rt,b(4),'hold'),t,.6);put(brass([x+12 for x in ch],.5),t,.6,0,.3)
        if gb>=20:[put(ca('sn',snare),t+q*B/4,.15+.1*q,.1) for q in range(4)]
        if gb>=8:
            th=theme_at(gb%40,0)
            if th:put(dizi(sc(th[0],D),th[1]*B*.95),t,.42,.15,.4)
    elif m=='drop':
        if gb==st:put(heartbeat(),t,.9,sfx=True);put(tremolo([D,D+1,D+7],b(nx-st)),t,.35,0,.4);put(bass(D-12,b(nx-st),'hold'),t,.5);put(riser(b(nx-st)),t,.5)
        if gb==nx-1:[put(ca('sn',snare),t+q*B/4,.3+.1*q) for q in range(4)]
    elif m in('epic','finale'):
        kk(gb,1);tk(t,.75,55);kk(gb+.5,.45)
        if bi%2:put(ca('sn',snare),t,.6);put(ca('cl',clap),t,.35)
        for q in range(4):put(ca('h',hat),t+q*B/4,.25 if q%2 else .35,.4)
        for q in range(2):put(ca(('b8',rt),lambda:bass(rt+12,B*.45)),t+q*B/2,.55)
        for q in range(4):put(ca(('ss',ch[q%3]+12),lambda:strings_stac(ch[q%3]+12)),t+q*B/4,.4,(-.35,.35)[q%2])
        if bi==0:put(choir([x for x in ch]+[ch[0]+12],b(4)),t,.45,0,.5);put(brass([x+12 for x in ch],.9),t,.75,0,.3);put(crash(),t,.4,.3)
        if bi==2:put(brass([x+12 for x in ch],.4),t+B/2,.5,0,.3)
        th=theme_at(gb,0)
        if th:put(dizi(sc(th[0],D),th[1]*B*.95),t,.45,.15,.4)
    elif m=='groove':
        if bi in(0,2):kk(gb,.8)
        if bi==2:kk(gb+.5,.4)
        if bi in(1,3):put(ca('sn',snare),t,.45);put(ca('cl',clap),t,.25)
        for q in range(4):put(ca('h',hat),t+q*B/4,.2 if q%2 else .3,.4)
        pat=[0,3,2,3,1,3,2,4]
        for q in range(2):
            mm=ch[pat[(gb*2+q)%8]%3]+12;put(ca(('pl',mm),lambda:pluck(mm,.9,.6)),t+q*B/2,.38,(-.3,.3)[q],.25)
        for q in range(2):put(ca(('b8',rt),lambda:bass(rt+12,B*.45)),t+q*B/2,.45)
        if bi==0:put(pad(ch,b(4),900),t,.25,0,.3)
        if (gb-st)>=4:
            th=theme_at(gb-st,0)
            if th:put(dizi(sc(th[0],D),th[1]*B*.95),t,.36,.15,.4)
        if bi==0 and bar%2==0:tk(t,.5)
    elif m=='heavy':
        if bi in(0,2):tk(t,.85,50);kk(gb,.9)
        if bi in(1,3):put(ca('sn',snare),t,.55);put(ca('cl',clap),t,.4)
        put(ca(('tm',90),lambda:tom(90)),t+B*.75,.35)
        if bi==0:put(bass(rt,b(4),'hold'),t,.55);put(tremolo([x+12 for x in ch],b(4)),t,.3,0,.3)
        if gb==st:put(erhu(sc(9,D),b(3)),t,.45,0,.5);put(erhu(sc(8,D),b(3)),t+b(3),.45,0,.5)
    elif m=='build':
        kk(gb,.9)
        if bi%2:put(ca('sn',snare),t,.5)
        for q in range(4):
            mm=sc([0,2,3,4][q]+10);put(ca(('ss',mm),lambda:strings_stac(mm)),t+q*B/4,.42,(-.3,.3)[q%2])
        [put(ca('h',hat),t+q*B/2,.3,.4) for q in range(2)]
        if bi==0:put(pad(ch,b(4),1600),t,.3,0,.3);put(bass(rt,b(4),'hold'),t,.55);put(brass([x+12 for x in ch],.6),t,.55,0,.3)
        if gb>=nx-2:[put(ca('sn',snare),t+q*B/4,.2+.08*q+.04*(gb%4),.1) for q in range(4)]
    elif m=='chase':
        for q in range(2):kk(gb+q/2,.85)
        put(ca('sn',snare),t+B/2,.6);bi%2 and put(ca('sn',snare),t,.5)
        for q in range(4):put(ca('h',hat),t+q*B/4,.3 if q%2 else .4,.35)
        r_=[0,0,-2,-4][((gb-st)//4)%4]
        for q in range(4):put(ca(('b16',r_),lambda:bass(D-12+r_,B*.22)),t+q*B/4,.5)
        for q in range(4):mm=sc([0,2,3,4][q]+(5 if gb%2 else 6),D+r_);put(ca(('p16',mm),lambda:pluck(mm,.45,.8)),t+q*B/4,.3,-.4+.25*q,.2)
        if bi==0:put(brass([x+12 for x in ch],.4),t,.6,0,.3);put(crash(),t,.3)
        th=theme_at((gb-st)*2,0)
        if th:put(dizi(sc(th[0],D+12),th[1]*B*.48),t,.4,.1,.3)
        th=theme_at((gb-st)*2+1,0)
        if th:put(dizi(sc(th[0],D+12),th[1]*B*.48),t+B/2,.4,.1,.3)
    elif m in('march','march2'):
        tk(t,.65,60);kk(gb,.8)
        for q in range(2):put(ca('sn2',lambda:snare()*.6),t+q*B/2+B/4,.35)
        if bi in(1,3):put(ca('sn',snare),t,.55)
        if bi==0:put(brass([x+12 for x in ch],1.2),t,.7,0,.3);put(choir(ch,b(4)),t,.35,0,.5);put(bass(rt,b(4),'hold'),t,.55)
        for q in range(2):put(ca(('ss',ch[q]+12),lambda:strings_stac(ch[q]+12)),t+q*B/2,.4,(-.3,.3)[q])
        if m=='march2':[put(ca('h',hat),t+q*B/4,.28,.4) for q in range(4)];kk(gb+.5,.45)
        th=theme_at(gb-st,0)
        if th:put(dizi(sc(th[0],D),th[1]*B*.95),t,.42,.15,.4)
    elif m=='dark':
        kk(gb,.9);tk(t,.7,48)
        put(ca('sn',snare),t+B/2,.35)
        for q in range(4):put(ca(('tm',110),lambda:tom(110)),t+q*B/4,.2,-.2)
        if bi==0:put(brass([D-24,D-17,D-12],b(3.5)),t,.55,0,.3);put(tremolo([D,D+1,D+7],b(4)),t,.35,0,.3)
    elif m=='war':
        kk(gb,1);kk(gb+.5,.6);tk(t,.75,55)
        for q in range(4):put(ca(('tm',120),lambda:tom(120)),t+q*B/4,.3 if q else .45,-.2)
        put(ca('sn',snare),t+B/2,.5);bi%2 and put(ca('cl',clap),t,.4)
        for q in range(4):put(ca(('ss',ch[q%3]+12),lambda:strings_stac(ch[q%3]+12)),t+q*B/4,.45,(-.35,.35)[q%2])
        if bi==0:put(choir([D-12,D-9,D-5,D],b(4)),t,.5,0,.5);put(brass([x+12 for x in ch],.8),t,.75,0,.3);put(crash(),t,.4)
    elif m=='hit':
        if gb==st:put(mx(bigimpact(),gong()*.6),t,1.0,0,.5);put(pad([D-14,D-10,D-7],b(nx-st),500),t,.4,0,.4)
        if gb>=nx-2:tk(t,.6);gb==nx-1 and [put(ca('sn',snare),t+q*B/4,.5) for q in range(4)]
    elif m=='soft':
        if bi==0:tk(t,.5,50);put(pad([D-12,D-5,D],b(4),700),t,.35,0,.4);put(bass(rt,b(4),'hold'),t,.45)
        if bi==2:kk(gb,.5)
        put(ca('h',hat),t+B/2,.15,.4)
        if gb==st:
            tt=t
            for dg,du in [(7,3),(6,3),(5,4),(4,4)]:put(erhu(sc(dg,D),b(du)),tt,.45,0,.6);tt+=b(du)
    elif m=='card':
        if gb==st:put(mx(bigimpact(),gong()*.5),t,1.0,0,.5);put(brass([D,D+7,D+12],1.2),t,.7,0,.4)
        else:[tk(t+q*B/2,.5+.1*q,56) for q in range(2)];put(ca('sn',snare),t+B/2,.4)
        if gb==nx-1:[put(ca('sn',snare),t+q*B/4,.3+.12*q) for q in range(4)]
    elif m=='end':
        if gb==st:put(mx(bigimpact(),gong()*.7),t,1.0,0,.6);put(choir([D-12,D-5,D,D+3],b(4)),t,.45,0,.6)
# ===== 拟声与对拍 =====
CUTS=sorted(set(round(a,4) for a,b_,f,p in SH if a>0))
used=[]
def free(tt,w=.07):return all(abs(tt-u)>w for u in used)
for i,ct in enumerate(CUTS):
    ty=['punch','flash','whip'][i%3];used.append(ct)
    if ty=='punch':put(mx(boom()*.8,hit()),ct,.7,0,.2)
    elif ty=='flash':put(mx(crashfx()*.6,hit()),ct,.6,0,.3)
    else:put(swish(),ct-.18,.7,sfx=True);put(ca('hit',hit),ct,.55)
for tt,mode in kinetic.slam_times():
    if mode in 'LR':put(swish(),tt-.12,.5,sfx=True);put(ca(('tm',140),lambda:tom(140)),tt,.5)
    elif mode=='S':put(mx(boom(),hit(),taiko(52)*.6),tt,.85,0,.3);put(brass([D+12,D+19,D+24],.35),tt,.4,0,.3)
    else:put(stab(),tt,.9);put(mx(crack(),hit()),tt,.6)
    used.append(tt)
for tt,k in json.load(open('events.json')):
    if tt<kinetic.HOOK_END:continue
    if not free(tt):continue
    used.append(tt)
    if k=='stamp':put(mx(bigimpact()*.8,gong()*.3),tt,.85,0,.4)
    elif k=='big':put(mx(boom()*.7,hit()),tt,.7,0,.3);put(swish(),tt-.15,.4,sfx=True)
    elif k=='counter':put(stab(),tt,.5)
    elif k=='badge':put(mx(wood(1000),hit()*.4),tt,.55)
# 关键音效
put(heartbeat(),b(12),.9,sfx=True);put(heartbeat(),b(13),.9,sfx=True)
put(mx(crack(),hit()),b(66.2),1.0)                       # 剪辫
put(arrow(),b(110.3),.6,sfx=True);put(arrow(),b(112.3),.6,sfx=True)
for bb in (59.0,60.3):put(tension(),b(bb),.5)
put(mx(crashfx(),boom()),b(131.2),.9)
put(shatter(),b(147.2),.7,sfx=True)                       # 撕信
put(shatter(),b(86.5),.6,sfx=True)                        # 撕复明旗
gallop(b(246),b(3))
for k in range(12):put(stab(),b(249+k*.75),.45)          # 刀兵交击
put(mx(boom(),hit()),b(313.5),1.0)                         # 泡沫破
put(arrow(),b(337),.7,sfx=True)

exec(open('score.py').read().split("for bb in (2,20,52,78,96,141,148,170,188)")[1].split('\n',1)[1].replace("'xuanwu.wav'","'wsg.wav'").replace('.35*np.convolve','.45*np.convolve'))
