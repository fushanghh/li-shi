# 细长纸偶人物 + 马（战争风）
from lib import *
INK='#120c08';SKIN='#ecd0a8'
KIND={
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
 'gen':dict(robe='#7a5a2a',dark='#4a3418',armor='#8a7a5a',cape='#3a5a7a',hat='helm'),
}
def _limb(c,x0,y0,x1,y1,w,fill,a):
    c.set_line_cap(1);col(c,INK,a);c.set_line_width(w+3);c.move_to(x0,y0);c.line_to(x1,y1);c.stroke()
    col(c,fill,a);c.set_line_width(w);c.move_to(x0,y0);c.line_to(x1,y1);c.stroke()
def person(c,x,y,h,kind='sol',pose='stand',face=1,t=0,a=1,arm=None,lean=0,bound=False,eyes='dot',cape_wind=0):
    """x,y=feet; h total height"""
    K_=KIND[kind];f=K_['robe'];d=K_['dark'];s=h/100.0
    c.save();c.translate(x,y)
    if pose=='kneel':c.translate(0,0);c.scale(1,.68)
    if pose=='ride':c.scale(1,.7)
    if pose=='fall':c.rotate(-face*1.45)
    c.rotate(lean*face);c.scale(face,1)
    c.set_line_join(1)
    # cape
    if K_.get('cape'):
        wv=math.sin(t*5)*3*s+cape_wind*s
        poly(c,[(-6*s,-74*s),(-12*s,-74*s),(-26*s-wv,-6*s),(-8*s-wv*.5,-2*s)],K_['cape'],a,INK,1.4*s,a)
    # legs (only in riding we skip)
    poly(c,[(-9*s,-74*s),(9*s,-74*s),(15*s,0),(-15*s,0)],f,a,INK,1.6*s,a)
    poly(c,[(-2*s,-74*s),(2*s,-74*s),(3*s,0),(-3*s,0)],d,a)
    rect(c,-15*s,-6*s,30*s,4*s,d,a)
    for k in range(3):col(c,GOLD,.35*a);c.set_line_width(.8*s);c.move_to(-14*s,-10*s-k*3*s);c.line_to(14*s,-10*s-k*3*s);c.stroke()
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
    rect(c,-11*s,-42*s,22*s,3.5*s,'#7a1f1a' if kind in('qin','emp') else '#1a120c',a)
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
    col(c,INK,a*.8);c.set_line_width(.8*s);c.move_to(1.8*s,hy+3.6*s);c.line_to(4.4*s,hy+3.6*s);c.stroke()
    col(c,INK,a);c.set_line_width(.9*s);c.move_to(1.2*s,hy-2.8*s);c.line_to(4.8*s,hy-3.2*s);c.stroke()
    if K_.get('beard') or kind in('emp','zhang'):
        poly(c,[(-1*s,hy+3*s),(6*s,hy+3*s),(3*s,hy+(14 if kind=='emp' else 10)*s)],'#2a1e14' if kind!='emp' else '#d8d0c0',a)
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
        rect(c,-3*s,hy-12*s,7*s,5*s,'#15100c',a);col(c,'#15100c',a);c.set_line_width(1.5*s);c.move_to(-6*s,hy-4*s);c.line_to(-13*s,hy+4*s);c.stroke()
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
