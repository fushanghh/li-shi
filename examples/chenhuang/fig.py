from lib import *
SKIN='#e9c9a0';SKIN2='#c99a6e'
# outfits
OUT={
 'qinsol':dict(robe='#8a7a5e',trim='#5e5038',pants='#6e604a',shoe='straw',hat='qin_bun',len='short',armor=None,belt='#3a2c1c'),   # 戍卒麻衣草鞋
 'qinsol2':dict(robe='#7a6e58',trim='#4e4432',pants='#5e5444',shoe='straw',hat='kerchief',len='short',armor=None,belt='#3a2c1c'),
 'qinsol3':dict(robe='#958568',trim='#6a5a40',pants='#6a5c48',shoe='straw',hat='qin_bun',len='short',armor=None,belt='#2a1c10'),
 'chen':dict(robe='#9a7b4e',trim='#c0392b',pants='#6a5638',shoe='straw',hat='redband_bun',len='short',armor=None,belt='#c0392b',beard=1),  # 陈胜
 'wu':dict(robe='#6f7a5a',trim='#3c4630',pants='#5a5a44',shoe='straw',hat='qin_bun',len='short',armor=None,belt='#2a1c10',beard=1),     # 吴广
 'qinoff':dict(robe='#1d1a1c',trim='#7a1f1a',pants='#151214',shoe='boot',hat='qin_cap',len='long',armor='qin',belt='#7a1f1a',beard=1), # 秦吏/尉 黑衣
 'chu':dict(robe='#7a2e24',trim='#d9b56a',pants='#3a2418',shoe='boot',hat='redband_bun',len='short',armor=None,belt='#d9b56a'),   # 楚地服
 'tangoff':dict(robe='#7a2f2a',trim='#d9b56a',pants='#2a1a14',shoe='boot',hat='futou',len='long',armor=None,belt='#1a120c',beard=1),  # 唐官 绯袍
 'tangoff2':dict(robe='#2f5a52',trim='#c9a24a',pants='#1a1a14',shoe='boot',hat='futou',len='long',armor=None,belt='#1a120c'),         # 绿袍
 'tangsol':dict(robe='#6e3a2e',trim='#3a3e44',pants='#3a3530',shoe='boot',hat='tang_helm',len='short',armor='tang',belt='#2a1c10'),     # 唐军甲胄
 'huang':dict(robe='#a8331f',trim='#d9b56a',pants='#4a2a14',shoe='boot',hat='gold_helm',len='short',armor='gold',belt='#d9b56a',beard=1),   # 黄巢 金甲
 'hsol':dict(robe='#8a3324',trim='#d9b56a',pants='#4a3020',shoe='boot',hat='redband',len='short',armor='gold',belt='#5a3a14'),        # 黄巢军
 'hsol2':dict(robe='#7a5a2a',trim='#c0392b',pants='#4a3420',shoe='straw',hat='redband',len='short',armor=None,belt='#c0392b'),
 'salt':dict(robe='#6a6a62',trim='#3a3a34',pants='#4a4a42',shoe='straw',hat='strawhat',len='short',armor=None,belt='#2a2a24',beard=1),  # 盐贩
 'scholar':dict(robe='#e0d6bc',trim='#6a5a40',pants='#5a5040',shoe='boot',hat='scholar',len='long',armor=None,belt='#3a2c1c',beard=1),
 'huangrobe':dict(robe='#d9a82e',trim='#7a1f1a',pants='#5a3a10',shoe='boot',hat='crown',len='long',armor=None,belt='#7a1f1a',beard=1),
 'emp':dict(robe='#d9a82e',trim='#8a6512',pants='#5a3a10',shoe='boot',hat='crown',len='long',armor=None,belt='#7a1f1a'),
 'farmer':dict(robe='#6e6250',trim='#4a4030',pants='#5a5040',shoe='straw',hat='kerchief',len='short',armor=None,belt='#2a2018',beard=1),
 'farmer2':dict(robe='#5a6458',trim='#3a4038',pants='#4a4a40',shoe='straw',hat='none',len='short',armor=None,belt='#2a2018'),
 'woman':dict(robe='#8a5a52',trim='#d9b56a',pants='#5a3a34',shoe='straw',hat='bun_f',len='long',armor=None,belt='#3a2018'),
 'woman2':dict(robe='#4e6070',trim='#c9a24a',pants='#3a3a44',shoe='straw',hat='bun_f',len='long',armor=None,belt='#2a2018'),
 'child':dict(robe='#9a7a5a',trim='#6a4a30',pants='#6a5a40',shoe='straw',hat='tuft',len='short',armor=None,belt='#3a2018'),
 'eunuch':dict(robe='#2e3558',trim='#c9a24a',pants='#1a1f36',shoe='boot',hat='futou',len='long',armor=None,belt='#1a120c'),
 'driver':dict(robe='#4a3e30',trim='#2a2018',pants='#3a3028',shoe='straw',hat='kerchief',len='short',armor=None,belt='#1a120c'),
}
def V(a,L):r=math.radians(a);return (math.sin(r)*L,math.cos(r)*L)
POSES={
 'stand':dict(ba=(8,4),fa=(-6,-2),bl=(-4,-3),fl=(4,3),lean=0),
 'stand2':dict(ba=(18,40),fa=(-10,-4),bl=(-5,-4),fl=(6,4),lean=0),
 'raise':dict(ba=(10,20),fa=(165,175),bl=(-8,-6),fl=(10,8),lean=-4),       # front arm straight up
 'hoe_up':dict(ba=(140,165),fa=(150,175),bl=(-12,-8),fl=(18,6),lean=-8),    # both hands holding up
 'shout':dict(ba=(20,-30),fa=(150,160),bl=(-14,-8),fl=(16,6),lean=-10),
 'point':dict(ba=(10,5),fa=(80,88),bl=(-6,-4),fl=(8,5),lean=2),
 'sword':dict(ba=(40,10),fa=(110,150),bl=(-18,-10),fl=(22,10),lean=6),
 'slash':dict(ba=(-30,-50),fa=(70,40),bl=(-24,-12),fl=(30,6),lean=14),
 'kneel':dict(ba=(30,70),fa=(35,75),bl=(5,-90),fl=(70,0),lean=10),
 'kowtow':dict(ba=(70,85),fa=(75,90),bl=(80,-90),fl=(85,-90),lean=60),
 'cower':dict(ba=(120,40),fa=(130,60),bl=(60,-30),fl=(80,0),lean=30),
 'read':dict(ba=(40,95),fa=(45,100),bl=(-4,-3),fl=(4,3),lean=-2),
 'sit':dict(ba=(25,80),fa=(30,85),bl=(85,0),fl=(88,2),lean=0),
 'fall':dict(ba=(150,120),fa=(-150,-120),bl=(30,40),fl=(-20,10),lean=-70),
 'dead':dict(ba=(90,100),fa=(100,120),bl=(4,8),fl=(-6,0),lean=-88),
 'carry':dict(ba=(150,175),fa=(155,178),bl=(-4,-3),fl=(4,3),lean=0),
 'cheer':dict(ba=(160,175),fa=(140,175),bl=(-6,-4),fl=(6,4),lean=-4),
 'hands':dict(ba=(30,85),fa=(30,85),bl=(-3,-2),fl=(3,2),lean=0),  # 拱手
 'beg':dict(ba=(40,100),fa=(50,110),bl=(5,-90),fl=(70,0),lean=0),
 'whip':dict(ba=(10,5),fa=(170,120),bl=(-10,-6),fl=(12,6),lean=-6),
}
def walk(t,speed=1.0,amp=24,run=False):
    p=math.sin(t*speed*2*math.pi)
    a=amp*(1.5 if run else 1)
    d=dict(ba=(-p*a*.8,-p*a*.8+(30 if run else 6)),fa=(p*a*.8,p*a*.8+(50 if run else 8)),
           bl=(p*a,p*a-(max(0,p)*30 if True else 0)),fl=(-p*a,-p*a-max(0,-p)*30),lean=(14 if run else 2))
    return d
def mix(p1,p2,k):
    out={}
    for key in p1:
        v1,v2=p1[key],p2[key]
        out[key]=tuple(lerp(a,b,k) for a,b in zip(v1,v2)) if isinstance(v1,tuple) else lerp(v1,v2,k)
    return out
def P(name):return dict(POSES[name])
def person(c,x,y,h,out='qinsol',pose='stand',face=1,expr='calm',mouth='closed',weapon=None,a=1,rot=0,blink=False,detail=None,wsc=1.0):
    o=OUT[out] if isinstance(out,str) else out
    p=P(pose) if isinstance(pose,str) else pose
    s=h/100.0
    if detail is None:detail=h>220
    lw=max(1.0,1.5*s)
    lean=math.radians(p.get('lean',0))
    # hip and neck
    hip=(0,-46)
    nk=(hip[0]+math.sin(lean)*30,hip[1]-math.cos(lean)*30)
    # legs
    def leg(an):
        k=(hip[0]+V(an[0],21)[0],hip[1]+V(an[0],21)[1]);f=(k[0]+V(an[1],22)[0],k[1]+V(an[1],22)[1]);return k,f
    bk,bf=leg(p['bl']);fk,ff=leg(p['fl'])
    low=max(bf[1],ff[1],bk[1]+3,fk[1]+3,hip[1]+6)
    if p.get('lean',0)<-60:  # lying: put body on ground
        low=max(low,nk[1]+9,hip[1]+6)
    dy=-low
    c.save();c.translate(x,y);c.rotate(rot);c.scale(face*s,s);c.translate(0,dy)
    ink=INK
    def limb(p0,p1,p2,w,colr):
        c.set_line_cap(1);c.set_line_join(1)
        col(c,ink,a);c.set_line_width(w+2.2);c.move_to(*p0);c.line_to(*p1);c.line_to(*p2);c.stroke()
        col(c,colr,a);c.set_line_width(w);c.move_to(*p0);c.line_to(*p1);c.line_to(*p2);c.stroke()
    def foot(f,an):
        sh=o['shoe'];fc='#b8955a' if sh=='straw' else '#1a1410'
        poly(c,[(f[0]-2,f[1]-3),(f[0]+6.5,f[1]-2),(f[0]+7,f[1]+.8),(f[0]-2.5,f[1]+.8)],fc,a,ink,.9,a)
        if sh=='straw' and detail:
            for k in range(3):line(c,f[0]-1+k*2.5,f[1]-2.6,f[0]+k*2.5,f[1]+.5,'#7a5a30',.5,a)
    # arms
    sh_b=(nk[0]-3,nk[1]+3);sh_f=(nk[0]+3,nk[1]+3)
    def arm(sh,an):
        e=(sh[0]+V(an[0],15)[0],sh[1]+V(an[0],15)[1]);hnd=(e[0]+V(an[1],14)[0],e[1]+V(an[1],14)[1]);return e,hnd
    be,bh=arm(sh_b,p['ba']);fe,fh=arm(sh_f,p['fa'])
    sleeve=o['robe'] if o['armor']!='gold' else '#b8873a'
    # back leg + back arm
    limb(hip,bk,bf,6,o['pants']);foot(bf,p['bl'][1])
    limb(sh_b,be,bh,5.2,_dark(sleeve));circ(c,bh[0],bh[1],2.3,SKIN2,a)
    # weapon held in back hand (two-handed hoe)
    def weapon_draw(hp,ang):
        if not weapon:return
        c.save();c.translate(*hp);c.rotate(math.radians(-ang));c.scale(wsc,wsc)
        if weapon=='hoe':
            line(c,0,22,0,-46,'#7a5530',2.6,a);poly(c,[(-1.5,-46),(9,-47),(11,-38),(-1.5,-42)],'#8a8c88',a,ink,.8,a)
        elif weapon=='pole':
            line(c,0,24,0,-70,'#8a6a40',2.2,a)
        elif weapon=='flag':
            line(c,0,24,0,-80,'#5a4026',2.2,a)
            poly(c,[(0,-80),(26,-77),(24,-60),(0,-58)],detail_flag_col(o),a,ink,.8,a)
        elif weapon=='sword':
            line(c,0,4,0,-4,'#3a2c1c',2.4,a);line(c,-3.5,-4,3.5,-4,GOLD,1.6,a)
            poly(c,[(-1.3,-4),(1.3,-4),(0.8,-38),(0,-41),(-0.8,-38)],'#d8d8d0',a,ink,.6,a)
        elif weapon=='gsword':
            line(c,0,4,0,-4,'#3a2c1c',2.4,a);line(c,-4,-4,4,-4,GOLD,2,a)
            poly(c,[(-1.6,-4),(1.6,-4),(1,-44),(0,-48),(-1,-44)],'#efe2c4',a,ink,.6,a)
        elif weapon=='spear':
            line(c,0,30,0,-62,'#6a4a2a',2,a);poly(c,[(0,-74),(2.2,-62),(-2.2,-62)],'#c8c8c0',a,ink,.6,a);circ(c,0,-61,2.2,RED,a)
        elif weapon=='torch':
            line(c,0,8,0,-20,'#6a4a2a',2.2,a);glow(c,0,-26,22,'#ffb347',.6*a);circ(c,0,-25,4,'#ffcf6a',a)
        elif weapon=='scroll':
            rect(c,-2,-12,24,14,'#e6d3a8',a);line(c,-2,-13,-2,3,'#6a4a2a',2.4,a);line(c,22,-13,22,3,'#6a4a2a',2.4,a)
        elif weapon=='bamboo':
            for k in range(6):rect(c,-6+k*3.2,-16,2.6,18,'#c9a86a',a)
        elif weapon=='whip':
            c.set_line_width(1.2);col(c,'#3a2c1c',a);c.move_to(0,0);c.curve_to(10,-20,30,-10,40,8);c.stroke()
        elif weapon=='bow':
            c.set_line_width(1.8);col(c,'#6a4a2a',a);c.arc(0,0,22,-1.2,1.2);c.stroke();line(c,math.cos(1.2)*22,-math.sin(1.2)*22*-1,math.cos(1.2)*22,math.sin(-1.2)*22,'#ddd',.6,a)
        elif weapon=='bundle':
            ell(c,4,-4,10,8,'#8a7a5a',a);
        c.restore()
    # torso / robe
    hemy=-24 if o['len']=='short' else -2
    if o['len']=='short':
        hx0=min(bk[0],fk[0],-8)-5;hx1=max(bk[0],fk[0],8)+5
        hb=(hx0,max(bk[1],fk[1],hip[1]+18)+1 if abs(bk[0]-fk[0])>14 else hip[1]+21)
    else:
        hx0=min(bf[0],ff[0],bk[0],fk[0],-11)-3;hx1=max(bf[0],ff[0],bk[0],fk[0],11)+3
        hb=(hx0,max(bf[1],ff[1])-3)
    rb=[(nk[0]-7,nk[1]),(nk[0]+7,nk[1]),(hip[0]+9,hip[1]),(hx1,hb[1]),(hx0,hb[1]),(hip[0]-9,hip[1])]
    poly(c,rb,o['robe'],a,ink,1.2,a)
    if detail:
        # robe folds
        col(c,_dark(o['robe']),a*.6);c.set_line_width(.7)
        for k in (-4,2,6):c.move_to(hip[0]+k,hip[1]+2);c.line_to(hip[0]+k*1.6,hb[1]-1);c.stroke()
    # hem trim
    col(c,o['trim'],a);c.set_line_width(2.2);c.move_to(hx0+1,hb[1]-1.2);c.line_to(hx1-1,hb[1]-1.2);c.stroke()
    # collar (cross collar 交领)
    if o['hat'] not in('crown',) or True:
        col(c,o['trim'],a);c.set_line_width(1.6);c.move_to(nk[0]-5,nk[1]+.5);c.line_to(nk[0]+4,nk[1]+12);c.stroke()
        c.move_to(nk[0]+5,nk[1]+.5);c.line_to(nk[0]+1,nk[1]+6);c.stroke()
    ar=o['armor']
    mx=(nk[0]+hip[0])/2;my=(nk[1]+hip[1])/2
    if ar=='qin':
        for r in range(4):
            for k in range(-2,3):rect(c,mx+k*3.6-1.6,nk[1]+5+r*4.4,3.2,3.6,'#3a3436',a)
    elif ar=='tang':
        poly(c,[(nk[0]-7,nk[1]+3),(nk[0]+7,nk[1]+3),(hip[0]+8,hip[1]-2),(hip[0]-8,hip[1]-2)],'#5a5e64',a,ink,.8,a)
        circ(c,mx-3,nk[1]+9,2.8,'#c8ccd0',a);circ(c,mx+3,nk[1]+9,2.8,'#c8ccd0',a)
        for r in range(3):line(c,hip[0]-8,hip[1]-6-r*3,hip[0]+8,hip[1]-6-r*3,'#3a3e44',.7,a)
        poly(c,[(hip[0]-10,hip[1]),(hip[0]+10,hip[1]),(hip[0]+12,hip[1]+12),(hip[0]-12,hip[1]+12)],'#4a4e54',a,ink,.6,a)
    elif ar=='gold':
        poly(c,[(nk[0]-7.5,nk[1]+2),(nk[0]+7.5,nk[1]+2),(hip[0]+9,hip[1]-1),(hip[0]-9,hip[1]-1)],'#c99a3a',a,ink,.8,a)
        if detail:
            for r in range(5):
                for k in range(-2,3):circ(c,mx+k*3.2,nk[1]+6+r*4,1.3,'#8a6514',a)
        circ(c,mx,nk[1]+9,3.2,'#f2d48a',a)
        poly(c,[(hip[0]-11,hip[1]),(hip[0]+11,hip[1]),(hip[0]+13,hip[1]+13),(hip[0]-13,hip[1]+13)],'#b8873a',a,ink,.6,a)
        # shoulder guards
        ell(c,nk[0]-6,nk[1]+4,5,3.5,'#d9b56a',a);ell(c,nk[0]+6,nk[1]+4,5,3.5,'#d9b56a',a)
    # belt
    poly(c,[(hip[0]-9.5,hip[1]-3),(hip[0]+9.5,hip[1]-3),(hip[0]+9.5,hip[1]+.5),(hip[0]-9.5,hip[1]+.5)],o['belt'],a)
    # front leg (if visible below short robe)
    limb(hip,fk,ff,6,o['pants']) if o['len']=='short' else None
    if o['len']=='short':
        # re-cover thigh by robe hem front part
        poly(c,[(hip[0]-9,hip[1]),(hip[0]+9,hip[1]),(hx1,hb[1]),(hx0,hb[1])],o['robe'],a,ink,1.0,a)
        col(c,o['trim'],a);c.set_line_width(2.2);c.move_to(hx0+1,hb[1]-1.2);c.line_to(hx1-1,hb[1]-1.2);c.stroke()
        if ar in ('tang','gold'):
            poly(c,[(hip[0]-10,hip[1]),(hip[0]+10,hip[1]),(hip[0]+12,hip[1]+12),(hip[0]-12,hip[1]+12)],'#4a4e54' if ar=='tang' else '#b8873a',a,ink,.6,a)
        poly(c,[(hip[0]-9.5,hip[1]-3),(hip[0]+9.5,hip[1]-3),(hip[0]+9.5,hip[1]+.5),(hip[0]-9.5,hip[1]+.5)],o['belt'],a)
    foot(ff,p['fl'][1])
    if weapon in('hoe',) and p is not None and pose in('hoe_up',):weapon_draw(bh,p['ba'][1]+180)
    # head
    head(c,nk,o,expr,mouth,a,detail,lean)
    # front arm
    limb(sh_f,fe,fh,5.2,sleeve)
    if detail and o['armor'] in (None,'qin'):
        col(c,o['trim'],a);c.set_line_width(1.4);
        cx_,cy_=lerp(fe[0],fh[0],.75),lerp(fe[1],fh[1],.75)
    circ(c,fh[0],fh[1],2.5,SKIN,a);col(c,ink,a);c.set_line_width(.7);c.arc(fh[0],fh[1],2.5,0,6.3);c.stroke()
    if weapon and not (weapon=='hoe' and pose=='hoe_up'):
        wa=p['fa'][1]+180 if weapon not in('scroll','bamboo','bundle') else 0
        weapon_draw(fh,wa)
    c.restore()
    return
def detail_flag_col(o):return '#c0392b' if o['hat'] in('redband','redband_bun','gold_helm') else '#c0392b'
def _dark(h,k=.7):
    r,g,b,_=hx(h);return '#%02x%02x%02x'%(int(r*255*k),int(g*255*k),int(b*255*k))
def head(c,nk,o,expr,mouth,a,detail,lean=0):
    ink=INK
    hx_,hy=nk[0]+math.sin(lean)*10,nk[1]-10
    hr=8.6
    rect(c,nk[0]-2,nk[1]-4,4,5,SKIN2,a)
    hat=o['hat']
    # back hair / bun behind
    if hat in('qin_bun','redband_bun'):
        circ(c,hx_-2+4,hy-9.5,3.6,'#17110c',a)  # 右偏髻
    if hat=='bun_f':
        circ(c,hx_-3,hy-9,4.5,'#17110c',a);circ(c,hx_-7,hy-4,3.2,'#17110c',a)
    # face
    circ(c,hx_,hy,hr+1.1,ink,a);circ(c,hx_,hy,hr,SKIN,a)
    # hair cap
    c.save();c.arc(hx_,hy,hr,0,2*math.pi);c.clip()
    col(c,'#17110c',a);c.arc(hx_-2.2,hy-3.2,hr*1.02,math.pi*0.82,math.pi*2.05);c.fill()
    c.restore()
    # ear
    ell(c,hx_-1.5,hy+0.5,1.6,2.2,SKIN2,a)
    # eye
    ex,ey=hx_+4.2,hy+.2
    if detail:
        ell(c,ex,ey,1.9,1.2,'#f4ead8',a);circ(c,ex+.5,ey,.95,ink,a)
    else:
        circ(c,ex,ey,1.0,ink,a)
    # brow
    by=hy-2.6
    bro={'calm':(0,0),'angry':(1.6,-0.6),'sad':(-1.4,0.4),'fear':(-1.8,-.6),'proud':(0.6,-.8)}.get(expr,(0,0))
    line(c,ex-2.3,by+bro[0]*.5,ex+2.2,by-bro[0]*.5+bro[1],ink,.95,a)
    # nose
    line(c,hx_+7.6,hy+.6,hx_+8.8,hy+2.6,ink,.6,a*.7)
    # mouth
    mx_,my_=hx_+6.2,hy+4.8
    if mouth=='open':
        ell(c,mx_,my_+.6,1.6,1.9,'#4a1610',a)
    elif mouth=='frown':
        c.set_line_width(.7);col(c,ink,a);c.arc(mx_,my_+1.6,1.7,math.pi*1.15,math.pi*1.85);c.stroke()
    elif mouth=='smile':
        c.set_line_width(.7);col(c,ink,a);c.arc(mx_,my_-.8,1.7,math.pi*.15,math.pi*.85);c.stroke()
    else:
        line(c,mx_-1.4,my_,mx_+1.2,my_,ink,.7,a)
    if o.get('beard'):
        poly(c,[(hx_+3,hy+5.6),(hx_+7.6,hy+6.2),(hx_+5,hy+11.5),(hx_+2.5,hy+8)],'#17110c',a*.92)
        line(c,mx_-2.4,my_-1.1,mx_+1.8,my_-1.2,'#17110c',.8,a)
    # hats
    if hat=='qin_bun':
        poly(c,[(hx_-7,hy-5),(hx_+6,hy-7.5),(hx_+5,hy-4),(hx_-8,hy-1.5)],'#3a2c1c',a)
    elif hat=='redband_bun':
        poly(c,[(hx_-8.4,hy-4),(hx_+7.4,hy-6.2),(hx_+7.8,hy-3.5),(hx_-8.6,hy-1.2)],RED,a)
        poly(c,[(hx_-8,hy-3),(hx_-15,hy+2),(hx_-14,hy+4),(hx_-8,hy-1)],RED,a)
    elif hat=='redband':
        poly(c,[(hx_-8.4,hy-4.6),(hx_+7.6,hy-6.6),(hx_+8,hy-3.4),(hx_-8.6,hy-1.4)],RED,a)
        poly(c,[(hx_-8,hy-3),(hx_-16,hy+3),(hx_-15,hy+5.5),(hx_-8,hy-.6)],RED,a)
    elif hat=='kerchief':
        c.save();c.arc(hx_,hy,hr+1.2,math.pi,2*math.pi);c.close_path();col(c,'#5a4e3a',a);c.fill();c.restore()
        circ(c,hx_-6,hy-6,2.6,'#5a4e3a',a)
    elif hat=='qin_cap':
        c.arc(hx_,hy-1,hr+1,math.pi,2*math.pi);col(c,'#0e0c0c',a);c.fill()
        poly(c,[(hx_-3,hy-8),(hx_+5,hy-9),(hx_+9,hy-20),(hx_+1,hy-20)],'#0e0c0c',a)
        line(c,hx_+5,hy-2,hx_+4,hy+9,'#0e0c0c',.6,a)
    elif hat=='futou':
        c.arc(hx_,hy-1.5,hr+1.1,math.pi,2*math.pi);col(c,'#100c0a',a);c.fill()
        ell(c,hx_-.5,hy-10.5,5,4,'#100c0a',a)
        col(c,'#100c0a',a);c.set_line_width(1.6);c.move_to(hx_-6,hy-6);c.curve_to(hx_-12,hy-6,hx_-14,hy+1,hx_-12,hy+8);c.stroke()
    elif hat=='scholar':
        c.arc(hx_,hy-1.5,hr+1,math.pi,2*math.pi);col(c,'#100c0a',a);c.fill()
        rect(c,hx_-4,hy-14,8,6,'#100c0a',a)
    elif hat=='tang_helm':
        c.arc(hx_,hy-1,hr+2,math.pi*.95,2.05*math.pi);col(c,'#6a6e74',a);c.fill_preserve();col(c,ink,a);c.set_line_width(.8);c.stroke()
        poly(c,[(hx_-9.5,hy-1),(hx_-4,hy-1),(hx_-4,hy+8),(hx_-10.5,hy+6)],'#5a5e64',a)
        line(c,hx_,hy-10.5,hx_,hy-16,'#3a3e44',1.4,a);circ(c,hx_,hy-17.5,3,RED,a)
    elif hat=='gold_helm':
        c.arc(hx_,hy-1,hr+2,math.pi*.95,2.05*math.pi);col(c,'#d9a83a',a);c.fill_preserve();col(c,ink,a);c.set_line_width(.8);c.stroke()
        poly(c,[(hx_-9.8,hy-1),(hx_-4,hy-1),(hx_-4,hy+8),(hx_-10.8,hy+6)],'#b8873a',a)
        poly(c,[(hx_-2,hy-10),(hx_+2,hy-10),(hx_+1,hy-19),(hx_-1,hy-19)],'#f2d48a',a)
        circ(c,hx_,hy-20,2.4,RED,a)
        poly(c,[(hx_-9,hy-2),(hx_-18,hy+4),(hx_-17,hy+7),(hx_-9,hy+1)],RED,a)
    elif hat=='strawhat':
        poly(c,[(hx_-15,hy-3),(hx_+15,hy-3),(hx_+1,hy-15)],'#c9a86a',a,ink,.8,a)
        line(c,hx_-14,hy-3.2,hx_+14,hy-3.2,'#8a6a3a',1.2,a)
    elif hat=='crown':
        poly(c,[(hx_-7,hy-6),(hx_+7,hy-6),(hx_+8,hy-13),(hx_-8,hy-13)],'#1a120c',a)
        rect(c,hx_-13,hy-15.5,26,2.6,'#1a120c',a)
        for k in range(-3,4):line(c,hx_+k*3.8,hy-13,hx_+k*3.8,hy-7,GOLD,.7,a)
    elif hat=='tuft':
        circ(c,hx_-1,hy-9,2.6,'#17110c',a)
# ---------- horse ----------
def horse(c,x,y,h,face=1,t=0,gallop=True,colr='#6a4a30',rider=None,a=1,rpose='sword',rweapon='gsword',expr='angry',mouth='closed'):
    s=h/100.0;ink=INK
    c.save();c.translate(x,y);c.scale(face*s,s)
    ph=t*2*math.pi*(2.2 if gallop else 1.1)
    bob=-abs(math.sin(ph))*4 if gallop else -abs(math.sin(ph))*1.5
    c.translate(0,bob)
    def legp(bx,by,off,front):
        sw=math.sin(ph+off)*(32 if gallop else 14)
        k=(bx+math.sin(math.radians(sw))*24,by+math.cos(math.radians(sw))*24)
        sw2=sw+(-35 if front else 25)*max(0,math.sin(ph+off+1))
        f=(k[0]+math.sin(math.radians(sw2))*26,k[1]+math.cos(math.radians(sw2))*26)
        col(c,ink,a);c.set_line_width(7.5);c.set_line_cap(1);c.move_to(bx,by);c.line_to(*k);c.line_to(*f);c.stroke()
        col(c,_dark(colr,.8),a);c.set_line_width(5.5);c.move_to(bx,by);c.line_to(*k);c.line_to(*f);c.stroke()
    legp(-30,-52,0.6,False);legp(32,-52,2.4,True)
    # tail
    col(c,'#1a120c',a);c.set_line_width(5);c.move_to(-44,-72);c.curve_to(-62,-66,-64,-48+math.sin(ph)*4,-70,-40+math.sin(ph)*6);c.stroke()
    # body
    ell(c,0,-70,46,20,ink,a);ell(c,0,-70,44.5,18.5,colr,a)
    # neck/head
    poly(c,[(28,-82),(40,-112),(54,-118),(70,-100),(64,-94),(50,-100),(42,-72)],colr,a,ink,1.4,a)
    col(c,'#1a120c',a);c.set_line_width(4);c.move_to(30,-84);c.line_to(44,-114);c.stroke()
    circ(c,56,-108,1.6,ink,a)
    # saddle cloth
    poly(c,[(-18,-88),(16,-88),(20,-62),(-22,-62)],'#7a1f1a',a);line(c,-22,-63,20,-63,GOLD,2,a)
    legp(-24,-52,3.6,False);legp(38,-52,5.2,True)
    c.restore()
    if rider:
        pr=P(rpose);pr['bl']=(70,10);pr['fl']=(72,12)
        person(c,x+2*s*face,y+bob*s-60*s,h*0.88,rider,pr,face,expr,mouth,weapon=rweapon,a=a)
# ---------- sprite cache for crowds ----------
_SP={}
def sprite(out,pose,h,face=1,weapon=None,expr='calm',mouth='closed',key=None):
    k=(out,str(pose) if key is None else key,h,face,weapon,expr,mouth)
    if k not in _SP:
        wpad=int(h*1.1)
        sw,shh=int(h*1.6)+wpad,int(h*2.0)
        sf=surf(sw,shh);cc=cairo.Context(sf)
        person(cc,sw/2,shh*0.82,h,out,pose,face,expr,mouth,weapon=weapon,detail=False)
        _SP[k]=(sf,sw/2,shh*0.82)
    return _SP[k]
def blit(c,spr,x,y,sc=1.0,a=1.0):
    sf,ox,oy=spr
    if sc!=1.0:
        c.save();c.translate(x,y);c.scale(sc,sc);c.set_source_surface(sf,-ox,-oy);c.paint_with_alpha(a) if a<1 else c.paint();c.restore()
    else:
        c.set_source_surface(sf,x-ox,y-oy);c.paint_with_alpha(a) if a<1 else c.paint()
