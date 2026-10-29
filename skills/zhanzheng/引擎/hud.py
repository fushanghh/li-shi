from lib import *
def slam(t,th,d=.16):
    u=(t-th)/d
    if u<0:return None
    if u>=1:return 1
    return lerp(2.3,1,ease(u))
def pop(t,th,d=.3):
    u=(t-th)/d
    if u<0:return 0
    if u>=1:return 1
    return max(.05,eback(u))
def shake(t,hits,amp=14):
    ox=oy=0
    for h in hits:
        u=t-h
        if 0<=u<.4:k=(1-u/.4)**2;ox+=math.sin(u*90)*amp*k;oy+=math.cos(u*71)*amp*k
    return ox,oy
def topbar(c,t,frac,place):
    rect(c,0,0,W,74,'#000000',.35)
    text(c,'621',60,46,22,GREY,align='l');text(c,'626',560,46,22,GREY,align='l')
    col(c,GREY,.6);c.set_line_width(2);c.move_to(110,38);c.line_to(545,38);c.stroke()
    col(c,RED);c.set_line_width(4);c.move_to(110,38);c.line_to(110+435*frac,38);c.stroke();circ(c,110+435*frac,38,7,RED)
    text(c,'（推演示意）',600,46,20,GREY,align='l')
    if place:
        rect(c,W-48-len(place)*28-30,22,6,34,RED);text(c,place,W-50,48,26,CREAM,align='r')
def subtitle(c,t,t0,s,src=None,t1=None):
    a=cl((t-t0)/.2)
    if t1 is not None:a*=cl((t1-t)/.15)
    if a<=0:return
    g=cairo.LinearGradient(0,H-210,0,H);g.add_color_stop_rgba(0,0,0,0,0);g.add_color_stop_rgba(1,0,0,0,.75*a);c.set_source(g);c.rectangle(0,H-210,W,210);c.fill()
    c.save();c.translate(0,(1-eo(a))*18);rich(c,s,W/2,H-92,54,a)
    if src:text(c,src,W/2,H-40,24,'#a89878',a*.9)
    c.restore()
def stamp(c,t,th,s,x,y,size=110,rot=-.06,h=RED):
    sc=slam(t,th)
    if sc is None:return
    c.save();c.translate(x,y);c.rotate(rot);c.scale(sc,sc)
    c.select_font_face('Noto Serif CJK SC Black',0,1);c.set_font_size(size);tw=sum(c.text_extents(ch)[4] for ch in s)+size*.15*(len(s)-1)
    pw=tw+size*.7;ph=size*1.35
    col(c,h,.92);c.rectangle(-pw/2,-ph/2,pw,ph);c.set_line_width(size*.08);c.stroke()
    col(c,h,.92);c.rectangle(-pw/2+size*.1,-ph/2+size*.1,pw-size*.2,ph-size*.2);c.set_line_width(size*.025);c.stroke()
    c.select_font_face('Noto Serif CJK SC Black',0,1);c.set_font_size(size);xx=-tw/2
    for ch_ in s:col(c,h,.95);c.move_to(xx,size*.36);c.show_text(ch_);xx+=c.text_extents(ch_)[4]+size*.15
    r=random.Random(len(s))
    for k in range(30):circ(c,r.uniform(-pw/2,pw/2),r.uniform(-ph/2,ph/2),r.uniform(2,size*.05),'#1a120c',.5)
    c.restore()
def bigword(c,t,th,s,x,y,size=150,h=GOLD,rot=0,a=1):
    sc=slam(t,th)
    if sc is None:return
    c.save();c.translate(x,y);c.rotate(rot);c.scale(sc,sc)
    import clib as _c
    _c.htext(c,s,0,size*.36,size,_c.GOLDG if h==GOLD else (_c.IVORY if h=='ivory' else ('#ff8a6a',h)),a)
    c.restore()
def counter(c,t,label,vals,x=70,y=120,note=None,h=GOLD):
    cur=None;th=0
    for tt,v in vals:
        if t>=tt:cur=v;th=tt
    if cur is None:return
    a=cl((t-vals[0][0])/.2)
    rect(c,x-20,y-10,380,200,'#0a0705',.55*a)
    text(c,label,x,y+30,28,'#c8b48a',a,align='l')
    p=pop(t,th,.3)
    c.save();c.translate(x,y+130);c.scale(p,p);
    c.select_font_face(FONT,0,1);c.set_font_size(104);c.move_to(0,0);c.text_path(cur);col(c,'#000000',a);c.set_line_width(8);c.stroke_preserve();col(c,h,a);c.fill()
    c.restore()
    if note:text(c,note,x,y+176,22,GREY,a,align='l')
def badge(c,t,t0,x,y,name,role,kind_col=RED,ch=None,r=56):
    p=pop(t,t0,.35)
    if p<=0:return
    c.save();c.translate(x,y);c.scale(p,p)
    glow(c,0,0,r*1.8,kind_col,.35)
    circ(c,0,0,r+5,GOLD);circ(c,0,0,r,'#1e150e');circ(c,0,0,r-6,kind_col,.85)
    text(c,ch or name[-1],0,r*.36,r*1.0,CREAM)
    rect(c,-r*1.6,r+10,r*3.2,70,'#0a0705',.7)
    text(c,name,0,r+46,32,CREAM);text(c,role,0,r+72,20,'#c8b48a')
    c.restore()
def vs_line(c,x0,y0,x1,y1,t,a=1):
    n=14;pts=[]
    for i in range(n+1):
        k=i/n;px=lerp(x0,x1,k);py=lerp(y0,y1,k)
        off=(12 if i%2 else -12)*(1 if 0<i<n else 0);dx,dy=y1-y0,x0-x1;L=math.hypot(dx,dy) or 1
        pts.append((px+dx/L*off,py+dy/L*off))
    c.move_to(*pts[0])
    for p in pts[1:]:c.line_to(*p)
    col(c,RED,a*(.7+.3*math.sin(t*10)));c.set_line_width(5);c.stroke()
