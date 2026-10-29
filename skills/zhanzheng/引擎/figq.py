# 细长纸偶人物 + 马（战争风）
from lib import *
INK='#120c08';SKIN='#ecd0a8'
KIND={
 'wu':dict(robe='#5a1a14',dark='#3a0e0a',armor='#b08a3a',cape='#7a1f1a',hat='qhelm',beard='#cfc8b8',queue=1),
 'wu44':dict(robe='#4a2a1a',dark='#2a160c',armor='#8a7040',cape='#7a1f1a',hat='helm_gold',beard='#2a1e14'),
 'wum':dict(robe='#e8e2d4',dark='#a8a090',armor='#b08a3a',cape='#f0ece0',hat='helm_gold',beard='#cfc8b8'),
 'wuemp':dict(robe='#c99a2e',dark='#7a5a12',armor=None,cape='#7a1f1a',hat='crown',beard='#cfc8b8'),
 'kx':dict(robe='#e8b830',dark='#9a7012',armor=None,cape=None,hat='qcrown',queue=1,dragon=1),
 'kxa':dict(robe='#e8b830',dark='#9a7012',armor='#d9b56a',cape='#c0392b',hat='qhelm',queue=1),
 'qb':dict(robe='#2e4a8a',dark='#1a2a52',armor='#3a5aa0',cape=None,hat='qhelm',queue=1,stud=1),
 'qr':dict(robe='#9a2a20',dark='#5e1712',armor='#b0382a',cape=None,hat='qhelm',queue=1,stud=1),
 'qy':dict(robe='#c99a2e',dark='#7a5a12',armor='#d9b04a',cape=None,hat='qhelm',queue=1,stud=1),
 'green':dict(robe='#3a5a3a',dark='#203a20',armor='#5a7050',cape=None,hat='qhelm',queue=1),
 'ggen':dict(robe='#2f5a3a',dark='#1a3a22',armor='#7a8a5a',cape='#2a6a4a',hat='qhelm',queue=1,beard='#2a1e14'),
 'wsol':dict(robe='#6a2a20',dark='#401712',armor='#5a5048',cape=None,hat='white'),
 'yongli':dict(robe='#d9a82e',dark='#8a6512',armor=None,cape=None,hat='yishan'),
 'sch':dict(robe='#2a4a6a',dark='#18304a',armor=None,cape=None,hat='qhat',queue=1,beard='#2a1e14'),
 'off':dict(robe='#3a2a4a',dark='#22182e',armor=None,cape=None,hat='qhat',queue=1),
 'farm':dict(robe='#6a5a40',dark='#4a3e2a',armor=None,cape=None,hat='straw'),
 'farmw':dict(robe='#7a4a4a',dark='#4a2a2a',armor=None,cape=None,hat='bun'),
 'wsf':dict(robe='#c99a2e',dark='#7a5a12',armor=None,cape=None,hat='crown'),
 'geng':dict(robe='#2a4a5a',dark='#18303a',armor='#4a6a7a',cape='#2a3a6a',hat='white',beard='#2a1e14'),
 'zj':dict(robe='#3a3a5a',dark='#22223a',armor='#5a5a7a',cape='#1a3a5a',hat='helm',beard='#2a1e14'),

 'qin':dict(robe='#9a2a20',dark='#5e1712',armor='#c99a3a',cape='#c0392b',hat='helm_gold'),   # 李世民
 'jian':dict(robe='#5a3a7a',dark='#352248',armor=None,cape=None,hat='crown'),               # 李建成
 'yuanji':dict(robe='#2f3a4a',dark='#1b222c',armor='#5a6470',cape='#4a2a3a',hat='helm'),    # 李元吉
 'zhang':dict(robe='#4a5a5a',dark='#2a3434',armor=None,cape=None,hat='futou'),             # 张亮
 'yuchi':dict(robe='#2a2a30',dark='#141418',armor='#3a3e46',cape='#7a1f1a',hat='helm',beard=1),# 尉迟恭
 'sol':dict(robe='#6b6f74',dark='#3c3f43',armor='#555a60',cape=None,hat='helm'),
 'tsol':dict(robe='#7a2a20',dark='#4a1712',armor='#6a5a40',cape=None,hat='helm'),          # 天策府兵
 'dsol':dict(robe='#3a3550',dark='#22203a',armor='#4a4a5a',cape=None,hat='helm'),          # 东宫兵
 'turk':dict(robe='#2f6a5a',dark='#1b4038',armor=None,cape=None,hat='turk',stripe=1),
 'emp':dict(robe='#d9a82e',dark='#8a6512',armor=None,cape=None,hat='crown'),               # 李渊
 'guard':dict(robe='#3a2a24',dark='#201612',armor=None,cape=None,hat='futou'),
 'xz':dict(robe='#e8b830',dark='#9a7012',armor=None,cape=None,hat='crown',beard='#2a1e14',dragon=1),
 'zjl':dict(robe='#a02a26',dark='#5e1712',armor=None,cape=None,hat='futou',beard='#2a1e14'),
 'llf':dict(robe='#5a2a6a',dark='#331840',armor=None,cape=None,hat='futou',beard='#2a1e14'),
 'ygz':dict(robe='#7a2a50',dark='#4a1830',armor=None,cape=None,hat='futou',beard='#2a1e14'),
 'pei':dict(robe='#2f5a7a',dark='#1a3448',armor=None,cape=None,hat='futou',beard='#2a1e14'),
 'ald':dict(robe='#2f6a5a',dark='#1b4038',armor=None,cape='#7a1f1a',hat='turk',beard='#2a1e14',stripe=1,fat=1),
 'aldw':dict(robe='#2f6a5a',dark='#1b4038',armor='#8a7040',cape='#7a1f1a',hat='turk',beard='#2a1e14',stripe=1,fat=1),
 'hsol':dict(robe='#6a4a2a',dark='#40301a',armor='#7a6a4a',cape=None,hat='turk',stripe=1),
 'toff':dict(robe='#2f5a3a',dark='#1a3a22',armor=None,cape=None,hat='futou'),
 'toff2':dict(robe='#3a4a7a',dark='#22284a',armor=None,cape=None,hat='futou'),
 'merch':dict(robe='#8a5a2a',dark='#5a3418',armor=None,cape=None,hat='turk',stripe=1,beard='#2a1e14'),
 'ygf':dict(robe='#c0392b',dark='#7a1f1a',armor=None,cape='#efe2c4',hat='bun'),
 'idle':dict(robe='#6a6050',dark='#40382c',armor='#7a7468',cape=None,hat='helm'),
 'hw':dict(robe='#2a1814',dark='#140a08',armor=None,cape='#7a1f1a',hat='crown',beard='#2a1e14',dragon=1),   # 汉武帝 玄衣
 'lsm':dict(robe='#e8b830',dark='#9a7012',armor=None,cape=None,hat='crown',beard='#2a1e14',dragon=1),  # 李世民
 'wq':dict(robe='#7a1f1a',dark='#4a1210',armor='#4a4440',cape='#c0392b',hat='helm',beard='#2a1e14'),   # 卫青
 'hqb':dict(robe='#8a2a20',dark='#5a1712',armor='#6a5a40',cape='#e04a30',hat='helm_gold'),               # 霍去病
 'lgl':dict(robe='#4a2a4a',dark='#2a182a',armor='#5a5050',cape='#3a2a4a',hat='helm',beard='#2a1e14'),  # 李广利
 'hansol':dict(robe='#7a2a20',dark='#4a1712',armor='#3e3a38',cape=None,hat='helm'),                       # 汉军
 'hoff':dict(robe='#1e1a1e',dark='#0e0a0e',armor=None,cape=None,hat='jin',beard='#2a1e14'),             # 汉官
 'hoff2':dict(robe='#5a1a14',dark='#3a0e0a',armor=None,cape=None,hat='jin',beard='#2a1e14'),
 'xn':dict(robe='#6a5030',dark='#3e2e1a',armor=None,cape=None,hat='fur',stripe=1,beard='#2a1e14'),     # 匈奴
 'lj':dict(robe='#5a3a1a',dark='#3a2410',armor='#9a8050',cape='#2f5a7a',hat='helm_gold',beard='#cfc8b8'),# 李靖
 'wz':dict(robe='#2f5a3a',dark='#1a3a22',armor=None,cape=None,hat='futou',beard='#2a1e14'),            # 魏征
 'fxl':dict(robe='#7a2a2a',dark='#4a1818',armor=None,cape=None,hat='futou',beard='#2a1e14'),           # 房玄龄
 'lzj':dict(robe='#2a4a5a',dark='#18303a',armor='#5a6a6a',cape='#7a1f1a',hat='helm',beard='#2a1e14'),   # 李正己 高句丽将
 'lsd':dict(robe='#5a2a4a',dark='#3a1830',armor=None,cape='#7a1f1a',hat='futou',beard='#2a1e14'),       # 李师道
 'lw':dict(robe='#3a3a2a',dark='#22221a',armor='#6a6a50',cape='#2f5a3a',hat='helm',beard='#2a1e14'),    # 刘悟
 'xzong':dict(robe='#e8b830',dark='#9a7012',armor=None,cape=None,hat='crown',beard='#2a1e14',dragon=1),# 唐宪宗
 'wyh':dict(robe='#a02a26',dark='#5e1712',armor=None,cape=None,hat='futou',beard='#cfc8b8'),          # 武元衡
 'cike':dict(robe='#1a1a1e',dark='#0a0a0c',armor=None,cape=None,hat='bun'),                            # 刺客
 'qsol':dict(robe='#2a4a5a',dark='#18303a',armor='#4a5a5a',cape=None,hat='helm'),                      # 淄青兵
 'ldy':dict(robe='#5a2a6a',dark='#381a44',armor=None,cape=None,hat='futou',beard='#2a1e14'),   # 李德裕 紫袍
 'nsr':dict(robe='#7a2420',dark='#4a1412',armor=None,cape=None,hat='futou',beard='#3a2e24'),   # 牛僧孺
 'lzm':dict(robe='#8a3a2a',dark='#5a2418',armor=None,cape=None,hat='futou',beard='#2a1e14'),   # 李宗闵
 'wenz':dict(robe='#e8b830',dark='#9a7012',armor=None,cape=None,hat='crown',beard='#2a1e14',dragon=1),
 'wuz':dict(robe='#d8a020',dark='#8a6010',armor=None,cape='#7a1f1a',hat='crown',beard='#2a1e14',dragon=1),
 'xuanz':dict(robe='#f0c040',dark='#a07a18',armor=None,cape=None,hat='crown',beard='#cfc8b8',dragon=1),
 'huan':dict(robe='#4a4a52',dark='#2a2a30',armor=None,cape='#7a1f1a',hat='futou'),            # 宦官
 'xdm':dict(robe='#8a3a1a',dark='#5a2410',armor='#7a6a4a',cape=None,hat='turk',beard='#2a1e14'), # 悉怛谋 吐蕃
 'lsy':dict(robe='#2f5a3a',dark='#1a3a22',armor=None,cape=None,hat='futou'),                   # 李商隐 青袍
 'bjy':dict(robe='#d8d0c0',dark='#9a9488',armor=None,cape=None,hat='futou',beard='#e8e4dc'),   # 白居易
 'jin':dict(robe='#3a3a5a',dark='#22223a',armor='#6a6a7a',cape=None,hat='helm'),              # 神策军
 'jwg':dict(robe='#2a3a5a',dark='#18243a',armor=None,cape='#7a1f1a',hat='qcrown',beard='#cfc8b8'),  # 晋文公
 'ccw':dict(robe='#7a1f1a',dark='#4a1210',armor=None,cape='#2a1a10',hat='qcrown',beard='#2a1e14'),   # 楚成王
 'ziyu':dict(robe='#8a2a20',dark='#5a1712',armor='#6a3a2a',cape='#c0392b',hat='qhelm',beard='#2a1e14'),# 子玉
 'xz':dict(robe='#2a3a5a',dark='#18243a',armor='#4a5a6a',cape='#2f5a7a',hat='qhelm',beard='#2a1e14'),  # 先轸
 'hy':dict(robe='#3a3a4a',dark='#22222e',armor=None,cape=None,hat='qhat',beard='#cfc8b8'),            # 狐偃
 'jsol':dict(robe='#2a3a5a',dark='#18243a',armor='#4a5058',cape=None,hat='qhelm'),
 'csol':dict(robe='#7a2a20',dark='#4a1712',armor='#5a3a2a',cape=None,hat='qhelm'),
 'cc':dict(robe='#6a6a4a',dark='#3e3e2a',armor=None,cape=None,hat='qhat'),
 'lwd':dict(robe='#e8b830',dark='#9a7012',armor=None,cape='#7a1f1a',hat='crown',beard='#e8e4dc',dragon=1),  # 梁武帝
 'hj':dict(robe='#3a2a1a',dark='#22180e',armor='#4a4038',cape='#5a1a10',hat='helm',beard='#2a1e14'),          # 侯景
 'cqz':dict(robe='#e8e4dc',dark='#b8b0a0',armor='#d8d4cc',cape='#f4f0e8',hat='helm',beard='#2a1e14'),         # 陈庆之 白袍
 'bp':dict(robe='#e8e4dc',dark='#b8b0a0',armor='#c8c4bc',cape=None,hat='helm'),                                 # 白袍军
 'wr':dict(robe='#5a3a1a',dark='#3a2410',armor='#8a7050',cape='#7a1f1a',hat='helm_gold',beard='#cfc8b8'),      # 韦叡
 'gz':dict(robe='#e8a8b8',dark='#b07888',armor=None,cape=None,hat='futou'),                                      # 贵游子弟
 'lsol':dict(robe='#7a2a20',dark='#4a1712',armor='#5a4a3a',cape=None,hat='helm'),                                # 梁兵
 'dwsol':dict(robe='#3a3a2a',dark='#22221a',armor='#5a5a4a',cape=None,hat='helm'),                               # 北兵/侯景兵
 'xzd':dict(robe='#5a2a4a',dark='#3a1830',armor=None,cape=None,hat='futou',beard='#2a1e14'),                    # 萧正德
 'xy':dict(robe='#2f4a5a',dark='#1a2e3a',armor=None,cape=None,hat='futou',beard='#2a1e14'),                     # 萧绎
 'lzl':dict(robe='#6a3a2a',dark='#4a2418',armor='#7a6a4a',cape='#3a2a1a',hat='helm',beard='#2a1e14'),          # 柳仲礼
 'mrsz':dict(robe='#2a3a2a',dark='#18241a',armor='#5a6a5a',cape='#2f5a3a',hat='helm_gold',beard='#2a1e14'),    # 慕容绍宗
 'gh':dict(robe='#3a3a4a',dark='#22222e',armor=None,cape='#5a1a10',hat='crown',beard='#cfc8b8'),               # 高欢
 'gen':dict(robe='#7a5a2a',dark='#4a3418',armor='#8a7a5a',cape='#3a5a7a',hat='helm'),
}
def _limb(c,x0,y0,x1,y1,w,fill,a):
    c.set_line_cap(1);col(c,INK,a);c.set_line_width(w+3);c.move_to(x0,y0);c.line_to(x1,y1);c.stroke()
    col(c,fill,a);c.set_line_width(w);c.move_to(x0,y0);c.line_to(x1,y1);c.stroke()
def person(c,x,y,h,kind='sol',pose='stand',face=1,t=0,a=1,arm=None,lean=0,bound=False,eyes='dot',cape_wind=0,talk=False,sweat=0):
    """x,y=feet; h total height"""
    K_=KIND[kind];f=K_['robe'];d=K_['dark'];s=h/100.0
    c.save();c.translate(x,y)
    if pose=='kneel':c.translate(0,0);c.scale(1,.68)
    if pose=='ride':c.scale(1,.7)
    if pose=='fall':c.rotate(-face*1.45)
    c.rotate(lean*face);c.scale(face,1)
    if K_.get('fat'):c.scale(1.38,1)
    c.set_line_join(1)
    if K_.get('queue') and pose!='fall':
        hy0=-86*s;col(c,'#15100c',a);c.set_line_width(3*s);c.move_to(-6*s,hy0+1*s);c.curve_to(-13*s,hy0+12*s,-14*s,hy0+24*s,-16*s,hy0+36*s+math.sin(t*3)*2*s);c.stroke()
        circ(c,-16*s,hy0+37*s,1.8*s,'#c0392b',a)
    # cape
    if K_.get('cape'):
        wv=math.sin(t*5)*3*s+cape_wind*s
        poly(c,[(-6*s,-74*s),(-12*s,-74*s),(-26*s-wv,-6*s),(-8*s-wv*.5,-2*s)],K_['cape'],a,INK,1.4*s,a)
    # legs (only in riding we skip)
    # legs + shoes (always visible)
    stp=math.sin(t*6)*1.5*s if pose in('walk',) else 0
    for lx in(-5,5):
        _limb(c,lx*s+(stp if lx>0 else -stp),-16*s,lx*1.2*s+(stp if lx>0 else -stp),-2.5*s,5.2*s,'#2a1e16',a)
        c.save();c.translate(lx*1.2*s+2.5*s+(stp if lx>0 else -stp),-1.6*s);c.scale(5*s,2.2*s);circ(c,0,0,1,'#120c08',a);c.restore()
    poly(c,[(-9*s,-74*s),(9*s,-74*s),(14*s,-13*s),(-14*s,-13*s)],f,a,INK,1.6*s,a)
    poly(c,[(-2*s,-74*s),(2*s,-74*s),(3*s,-13*s),(-3*s,-13*s)],d,a)
    rect(c,-14*s,-17*s,28*s,4*s,d,a)
    for k in range(3):col(c,GOLD,.35*a);c.set_line_width(.8*s);c.move_to(-13*s,-21*s-k*3*s);c.line_to(13*s,-21*s-k*3*s);c.stroke()
    if K_.get('stripe'):
        for i in range(5):rect(c,-12*s,-62*s+i*11*s,24*s,3.5*s,['#c0392b','#d9b56a','#2e3558'][i%3],a)
    if K_.get('armor'):
        ar=K_['armor']
        poly(c,[(-11*s,-74*s),(11*s,-74*s),(12*s,-40*s),(-12*s,-40*s)],ar,a,INK,1.2*s,a)
        for i in range(5):
            col(c,INK,.5*a);c.set_line_width(.7*s);c.move_to(-11*s,-68*s+i*6*s);c.line_to(11*s,-68*s+i*6*s);c.stroke()
        circ(c,0,-62*s,3.5*s,GOLD,a)
        poly(c,[(-13*s,-40*s),(13*s,-40*s),(16*s,-22*s),(-16*s,-22*s)],ar,a*.9,INK,1*s,a)
        # 肩甲
        for sx in(-1,1):c.save();c.translate(sx*10*s,-72*s);c.scale(1,.6);circ(c,0,0,6*s,ar,a);c.restore()
    if K_.get('stud'):
        for i in range(4):
            for j in range(3):circ(c,(-7+j*7)*s,(-68+i*7)*s,1.1*s,'#e8d090',a)
    if K_.get('dragon'):
        col(c,'#c0392b',.8*a);c.set_line_width(1.4*s);c.move_to(-8*s,-66*s);c.curve_to(6*s,-60*s,-6*s,-52*s,8*s,-46*s);c.stroke();circ(c,0,-62*s,2.5*s,'#c0392b',a)
        for i in range(4):col(c,'#3a6a9a',.8*a);c.set_line_width(1.2*s);c.move_to(-14*s,-12*s-i*3*s);c.curve_to(-6*s,-16*s-i*3*s,6*s,-8*s-i*3*s,14*s,-12*s-i*3*s);c.stroke()
    rect(c,-11*s,-42*s,22*s,3.5*s,'#7a1f1a' if kind in('qin','emp','kx','wuemp','wu') else '#1a120c',a)
    # arms
    if arm is None:
        arm={'stand':(20,20),'raise':(-150,20),'point':(-90,25),'kneel':(15,15),'fall':(40,-60),'draw':(-90,-80),'hold':(70,25),'cross':(40,40),'wave':(-140,-150),'ride':(60,40)}.get(pose,(20,20))
    sc=SKIN
    for i,ang in enumerate(arm):
        sx=7*s if i==0 else -7*s
        ra=math.radians(90-ang) if i==0 else math.radians(90+ang)
        L1=30*s
        ex=sx+math.cos(ra)*L1;ey=-70*s+math.sin(ra)*L1
        if bound:ex,ey=(-6*s if i==0 else -9*s),-48*s
        _limb(c,sx,-70*s,ex,ey,6.5*s,f,a);circ(c,ex,ey,2.6*s,sc,a)
    if bound:
        col(c,'#a88a5a',a);c.set_line_width(1.6*s)
        for k in range(3):c.move_to(-13*s,-62*s+k*6*s);c.line_to(13*s,-58*s+k*6*s)
        c.stroke()
    rect(c,-2*s,-79*s,4*s,6*s,sc,a)
    hy=-86*s;hr=7.4*s
    circ(c,0,hy,hr+1.2*s,INK,a);circ(c,0,hy,hr,SKIN,a)
    # face
    if eyes=='dot':circ(c,3*s,hy-.6*s,1*s,INK,a)
    elif eyes=='angry':col(c,INK,a);c.set_line_width(1*s);c.move_to(1.2*s,hy-3*s);c.line_to(5*s,hy-1.4*s);c.stroke();circ(c,3.4*s,hy,.9*s,INK,a)
    elif eyes=='closed':col(c,INK,a);c.set_line_width(.9*s);c.move_to(1.8*s,hy);c.line_to(4.6*s,hy+.4*s);c.stroke()
    elif eyes=='wide':circ(c,3.2*s,hy-.4*s,1.8*s,'#ffffff',a);circ(c,3.4*s,hy-.4*s,.8*s,INK,a)
    if talk:
        mo=(.35+.65*abs(math.sin(t*13)))*2.2*s
        c.save();c.translate(3.2*s,hy+3.8*s);c.scale(1.5*s,mo);circ(c,0,0,1,'#5a1410',a);c.restore()
    else:
        col(c,INK,a*.8);c.set_line_width(.8*s);c.move_to(1.8*s,hy+3.6*s);c.line_to(4.4*s,hy+3.6*s);c.stroke()
    if sweat:
        r_=random.Random(int(t*3))
        for k in range(4):
            u=(t*1.3+k*.27)%1;sx_=(-6+k*4)*s;sy_=hy-6*s+u*14*s
            col(c,'#cfe6ff',sweat*a*(1-u));c.move_to(sx_,sy_-2.4*s);c.curve_to(sx_+1.6*s,sy_,sx_+1.6*s,sy_+1.6*s,sx_,sy_+1.6*s);c.curve_to(sx_-1.6*s,sy_+1.6*s,sx_-1.6*s,sy_,sx_,sy_-2.4*s);c.fill()
    col(c,INK,a);c.set_line_width(.9*s);c.move_to(1.2*s,hy-2.8*s);c.line_to(4.8*s,hy-3.2*s);c.stroke()
    if K_.get('beard') or kind in('emp','zhang'):
        bc=K_.get('beard') if isinstance(K_.get('beard'),str) else ('#2a1e14' if kind!='emp' else '#d8d0c0')
        bt_=6.2 if talk else 3
        poly(c,[(-1*s,hy+bt_*s),(6*s,hy+bt_*s),(3*s,hy+(14 if kind in('emp','wu','wum','wuemp') else 10)*s)],bc,a)

    hat=K_['hat']
    if hat in('helm','helm_gold'):
        hc='#c99a3a' if hat=='helm_gold' else '#5a5e63'
        c.new_sub_path();c.arc(0,hy-1*s,hr+1.8*s,math.pi,2*math.pi);col(c,hc,a);c.fill_preserve();col(c,INK,a);c.set_line_width(1*s);c.stroke()
        rect(c,-hr-2*s,hy-2*s,2*hr+4*s,2.2*s,hc,a)
        col(c,'#c0392b',a);c.set_line_width(2.2*s);c.move_to(0,hy-10*s);c.line_to(-2*s,hy-19*s);c.stroke();circ(c,-2*s,hy-19*s,3*s,'#c0392b',a)
        if hat=='helm_gold':
            for sx in(-1,1):col(c,GOLD,a);c.set_line_width(1.2*s);c.move_to(sx*4*s,hy-9*s);c.curve_to(sx*9*s,hy-14*s,sx*12*s,hy-16*s,sx*14*s,hy-20*s);c.stroke()
    elif hat=='crown':
        poly(c,[(-8*s,hy-5*s),(8*s,hy-5*s),(9*s,hy-12*s),(-9*s,hy-12*s)],'#1a120c',a)
        rect(c,-12*s,hy-14*s,24*s,2.5*s,'#1a120c',a)
        for k in range(-3,4):col(c,GOLD,a);c.set_line_width(.7*s);c.move_to(k*3.5*s,hy-12*s);c.line_to(k*3.5*s,hy-7*s);c.stroke()
    elif hat=='futou':
        c.new_sub_path();c.arc(0,hy-2*s,hr+1*s,math.pi,2*math.pi);col(c,'#15100c',a);c.fill()
        rect(c,-3*s,hy-12*s,7*s,5*s,'#15100c',a);col(c,'#15100c',a);c.set_line_width(1.3*s);c.move_to(-hr-9*s,hy-7*s);c.line_to(hr+9*s,hy-7*s);c.stroke()
    elif hat=='qhelm':
        c.new_sub_path();c.arc(0,hy-1*s,hr+1.6*s,math.pi,2*math.pi);col(c,'#3a3a40' if kind not in('wu','kxa') else '#a8802a',a);c.fill_preserve();col(c,INK,a);c.set_line_width(1*s);c.stroke()
        rect(c,-hr-3*s,hy-2*s,2*hr+6*s,2.4*s,'#1a120c',a)
        col(c,'#d9b56a',a);c.set_line_width(1.6*s);c.move_to(0,hy-9*s);c.line_to(0,hy-24*s);c.stroke()
        circ(c,0,hy-15*s,1.8*s,'#d9b56a',a)
        poly(c,[(-2.5*s,hy-24*s),(2.5*s,hy-24*s),(1*s,hy-33*s+math.sin(t*4)*1*s),(-3*s,hy-31*s)],'#c0392b',a)
    elif hat=='qcrown':
        c.save();c.scale(1,.5);c.new_sub_path();c.arc(0,(hy-6*s)*2,hr+5*s,0,2*math.pi);col(c,'#1a120c',a);c.fill();c.restore()
        c.new_sub_path();c.arc(0,hy-4*s,hr+.5*s,math.pi,2*math.pi);col(c,'#b0302a',a);c.fill()
        for k in range(-3,4):col(c,'#c0392b',a);c.set_line_width(1*s);c.move_to(0,hy-11*s);c.line_to(k*3*s,hy-5*s);c.stroke()
        circ(c,0,hy-13*s,2.4*s,'#d9b56a',a);circ(c,0,hy-16*s,1.6*s,'#f3e6c8',a)
    elif hat=='qhat':
        poly(c,[(-hr-3*s,hy-3*s),(hr+3*s,hy-3*s),(0,hy-13*s)],'#2a1e18',a,INK,.6*s,a)
        for k in range(-3,4):col(c,'#c0392b',a);c.set_line_width(.9*s);c.move_to(0,hy-12*s);c.line_to(k*2.8*s,hy-4*s);c.stroke()
        circ(c,0,hy-13*s,1.8*s,'#3a5aa0',a)
    elif hat=='white':
        c.new_sub_path();c.arc(0,hy-1*s,hr+1.4*s,math.pi,2*math.pi);col(c,'#ece6da',a);c.fill_preserve();col(c,INK,a);c.set_line_width(.8*s);c.stroke()
        rect(c,-hr-1.5*s,hy-3*s,2*hr+3*s,2.5*s,'#d8d0c0',a)
        col(c,'#ece6da',a);c.set_line_width(1.6*s);c.move_to(-hr,hy-2*s);c.curve_to(-hr-5*s,hy+2*s,-hr-7*s,hy+6*s+math.sin(t*5)*2*s,-hr-10*s,hy+8*s);c.stroke()
    elif hat=='yishan':
        c.new_sub_path();c.arc(0,hy-2*s,hr+1*s,math.pi,2*math.pi);col(c,'#15100c',a);c.fill()
        rect(c,-5*s,hy-13*s,10*s,6*s,'#15100c',a)
        for sx in(-1,1):c.save();c.translate(sx*4*s,hy-13*s);c.rotate(sx*.5);c.scale(.6,1.2);circ(c,0,0,3*s,'#15100c',a);c.restore()
    elif hat=='straw':
        poly(c,[(-hr-7*s,hy-2*s),(hr+7*s,hy-2*s),(0,hy-12*s)],'#b8984a',a,INK,.6*s,a)
    elif hat=='bun':
        c.new_sub_path();c.arc(0,hy-2*s,hr,math.pi,2*math.pi);col(c,'#15100c',a);c.fill();circ(c,-4*s,hy-8*s,4*s,'#15100c',a)
    elif hat=='jin':
        poly(c,[(-hr*.8,hy-4*s),(hr*.9,hy-4*s),(hr*.6,hy-12*s),(-hr*.5,hy-16*s)],'#15100c',a)
        rect(c,-hr-1*s,hy-5*s,2*hr+2*s,2.4*s,'#15100c',a)
    elif hat=='fur':
        poly(c,[(-9*s,hy-4*s),(9*s,hy-4*s),(3*s,hy-19*s),(-2*s,hy-18*s)],'#4a3a2a',a,INK,.8*s,a)
        rect(c,-10*s,hy-6*s,20*s,4*s,'#c8b89a',a)
    elif hat=='turk':
        poly(c,[(-8*s,hy-4*s),(8*s,hy-4*s),(4*s,hy-17*s),(-3*s,hy-16*s)],'#a8402e',a,INK,.8*s,a)
        rect(c,-9*s,hy-5*s,18*s,3*s,'#6a4a2a',a)
    # bow in draw pose
    if pose=='draw':
        bx=36*s;by=-70*s
        col(c,'#5a3a1a',a);c.set_line_width(2.2*s);c.new_sub_path();c.arc(bx-14*s,by,20*s,-1.2,1.2);c.stroke()
        col(c,'#efe2c4',a*.8);c.set_line_width(.7*s);c.move_to(bx-14*s+math.cos(-1.2)*20*s,by+math.sin(-1.2)*20*s);c.line_to(-2*s,by);c.line_to(bx-14*s+math.cos(1.2)*20*s,by+math.sin(1.2)*20*s);c.stroke()
        col(c,'#d9c9a0',a);c.set_line_width(1.2*s);c.move_to(-2*s,by);c.line_to(bx+16*s,by);c.stroke()
        poly(c,[(bx+16*s,by-2.4*s),(bx+22*s,by),(bx+16*s,by+2.4*s)],'#c8c8c8',a)
    c.restore()
def horse(c,x,y,h,face=1,t=0,gallop=0,col_='#3a2a20',a=1,rider=None,rider_pose='ride',speed=8):
    """x,y=hooves ground; h=horse height to back"""
    s=h/100;ph=t*speed
    c.save();c.translate(x,y+ (-abs(math.sin(ph))*6*s*gallop));c.scale(face,1)
    # legs
    for i,(lx,off) in enumerate([(-34,0),(-26,1.6),(26,.6),(34,2.2)]):
        sw=math.sin(ph+off)*.6*gallop
        kx=lx*s+math.sin(sw)*22*s;ky=-30*s+abs(math.cos(sw))*0
        _limb(c,lx*s,-58*s,kx,-26*s,7*s,col_ if i%2 else '#2a1e16',a)
        _limb(c,kx,-26*s,kx+math.sin(sw*1.4)*14*s,-2*s,5*s,col_ if i%2 else '#2a1e16',a)
    # tail
    tw=math.sin(ph*.7)*6*s
    c.move_to(-46*s,-70*s);c.curve_to(-66*s,-66*s+tw,-74*s,-40*s+tw,-70*s,-26*s+tw);c.set_line_width(7*s);col(c,'#15100c',a);c.stroke()
    # body
    c.move_to(-48*s,-74*s);c.curve_to(-48*s,-90*s,30*s,-92*s,42*s,-80*s);c.line_to(48*s,-56*s);c.curve_to(20*s,-46*s,-30*s,-46*s,-46*s,-56*s);c.close_path()
    col(c,col_,a);c.fill_preserve();col(c,INK,a);c.set_line_width(1.6*s);c.stroke()
    # neck+head
    nk=math.sin(ph)*3*s*gallop
    poly(c,[(30*s,-84*s),(46*s,-122*s+nk),(58*s,-126*s+nk),(74*s,-104*s+nk),(66*s,-98*s+nk),(52*s,-104*s+nk),(48*s,-66*s)],col_,a,INK,1.6*s,a)
    poly(c,[(32*s,-86*s),(46*s,-124*s+nk),(40*s,-122*s+nk),(26*s,-86*s)],'#15100c',a)
    circ(c,60*s,-116*s+nk,1.6*s,'#efe2c4',a)
    # saddle
    poly(c,[(-12*s,-88*s),(16*s,-88*s),(18*s,-74*s),(-14*s,-74*s)],'#7a1f1a',a,INK,1*s,a)
    rect(c,-14*s,-76*s,32*s,4*s,GOLD,a)
    c.restore()
    if rider:
        person(c,x+(2*s*face),y-74*s-(abs(math.sin(ph))*6*s*gallop),h*.92,rider,pose=rider_pose,face=face,t=t,a=a,cape_wind=10*gallop)
