from lib import *
ROBES={'emp':('#d9a82e','#8a6512'),'emp2':('#c99a2a','#7a5810'),'eun':('#2e3558','#1a1f36'),'off':('#3d6a6a','#223e3e'),
'off2':('#8a3a34','#5a221e'),'boy':('#6a5a8a','#3e3456'),'prince':('#5a6e8a','#33415a'),'sol':('#6b6f74','#3c3f43'),
'hu':('#2f7a6a','#1b4a40'),'maid':('#b8433a','#7a2a24'),'monk':('#7a5a3a','#4a3420'),'tang':('#c9a24a','#7a5a22')}
def person(c,x,y,h,kind='off',pose='stand',face=1,t=0,hat=None,arm=None,a=1,bob=0):
    """x,y = feet. h total height. thin paper puppet."""
    f,d=ROBES[kind]
    c.save();c.translate(x,y+bob)
    if pose=='kneel':c.scale(1,0.66)
    if pose=='bow':c.rotate(0.12*face)
    if pose=='lie':
        c.rotate(-face*math.pi/2*0.98);
    c.scale(face,1)
    s=h/100.0
    lw=max(1.2,1.6*s)
    # robe
    c.set_line_join(1)
    poly(c,[(-9*s,-74*s),(9*s,-74*s),(15*s,0),(-15*s,0)],f,a,'#120c08',lw,a)
    poly(c,[(-2*s,-74*s),(2*s,-74*s),(3*s,0),(-3*s,0)],d,a)
    # hem pattern
    col(c,d,a);c.rectangle(-15*s,-6*s,30*s,4*s);c.fill()
    if kind=='hu':
        for i in range(5):col(c,['#c0392b','#d9b56a','#2e3558'][i%3],a);c.rectangle(-13*s,-60*s+i*12*s,26*s,4*s);c.fill()
    if kind=='sol':
        for i in range(4):
            col(c,'#4a4d52',a);c.rectangle(-11*s,-66*s+i*8*s,22*s,5*s);c.fill()
    # belt
    rect(c,-10*s,-50*s,20*s,3.5*s,'#1a120c' if kind!='emp' else '#7a1f1a',a)
    # arms
    if arm is None:
        arm={'stand':(25,25),'raise':(-150,25),'bow':(8,8),'kneel':(12,12),'sit':(50,50),'point':(-80,25),'lie':(20,20),'wave':(-140,-140),'hold':(80,30)}.get(pose,(25,25))
    for i,ang in enumerate(arm):
        sx=7*s if i==0 else -7*s
        ra=math.radians(90-ang) if i==0 else math.radians(90+ang)
        ex=sx+math.cos(ra)*30*s*(1 if i==0 else 1);ey=-70*s+math.sin(ra)*30*s
        c.set_line_cap(1);col(c,'#120c08',a);c.set_line_width(9*s);c.move_to(sx,-70*s);c.line_to(ex,ey);c.stroke()
        col(c,f,a);c.set_line_width(6.5*s);c.move_to(sx,-70*s);c.line_to(ex,ey);c.stroke()
        circ(c,ex,ey,2.4*s,'#e8c9a0',a)
    # neck/head
    rect(c,-2*s,-79*s,4*s,6*s,'#e8c9a0',a)
    hy=-86*s;hr=7.2*s
    circ(c,0,hy,hr+lw*.6,'#120c08',a);circ(c,0,hy,hr,'#ecd0a8',a)
    circ(c,2.6*s,hy-0.5*s,0.9*s,'#120c08',a)
    col(c,'#120c08',a*.8);c.set_line_width(.8*s);c.move_to(1.5*s,hy+3.5*s);c.line_to(4*s,hy+3.5*s);c.stroke()
    hat=hat or {'emp':'crown','emp2':'crown','eun':'cap','off':'futou','off2':'futou','boy':'bun','prince':'futou','sol':'helm','hu':'hu','maid':'bun2','monk':'none','tang':'futou'}[kind]
    if hat=='crown':
        poly(c,[(-8*s,hy-5*s),(8*s,hy-5*s),(9*s,hy-12*s),(-9*s,hy-12*s)],'#1a120c',a)
        rect(c,-12*s,hy-14*s,24*s,2.5*s,'#1a120c',a)
        for k in range(-3,4):col(c,'#d9b56a',a);c.set_line_width(.7*s);c.move_to(k*3.5*s,hy-12*s);c.line_to(k*3.5*s,hy-7*s);c.stroke()
    elif hat in('futou','cap'):
        c.arc(0,hy-2*s,hr+1*s,math.pi,2*math.pi);col(c,'#15100c',a);c.fill()
        rect(c,-3*s,hy-12*s,7*s,5*s,'#15100c',a)
        if hat=='futou':col(c,'#15100c',a);c.set_line_width(1.5*s);c.move_to(-6*s,hy-4*s);c.line_to(-13*s,hy+4*s);c.stroke()
    elif hat=='helm':
        c.arc(0,hy-1*s,hr+1.5*s,math.pi,2*math.pi);col(c,'#5a5e63',a);c.fill()
        col(c,'#c0392b',a);c.set_line_width(2*s);c.move_to(0,hy-9*s);c.line_to(0,hy-17*s);c.stroke();circ(c,0,hy-17*s,2.5*s,'#c0392b',a)
    elif hat=='hu':
        poly(c,[(-8*s,hy-4*s),(8*s,hy-4*s),(4*s,hy-16*s),(-3*s,hy-15*s)],'#a8402e',a)
    elif hat=='bun':
        circ(c,-1*s,hy-8*s,3.5*s,'#15100c',a);c.arc(0,hy-1*s,hr+.5*s,math.pi,2*math.pi);col(c,'#15100c',a);c.fill()
    elif hat=='bun2':
        circ(c,0,hy-10*s,4.5*s,'#15100c',a);c.arc(0,hy-1*s,hr+.5*s,math.pi,2*math.pi);col(c,'#15100c',a);c.fill()
    c.restore()
