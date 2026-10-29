from lib import *
from fig2 import person, horse
def sky(c,top,bot,y1=H):
    g=cairo.LinearGradient(0,0,0,y1);g.add_color_stop_rgb(0,*hx(top)[:3]);g.add_color_stop_rgb(1,*hx(bot)[:3]);c.set_source(g);c.rectangle(0,0,W,y1);c.fill()
def ridge(c,y,amp,fr,colh,a,off=0,seed=0):
    c.move_to(-50,H)
    for x in range(-50,W+60,30):c.line_to(x,y-amp*(.6*math.sin((x+off)*fr+seed)+.4*math.sin((x+off)*fr*2.7+seed*2)))
    c.line_to(W+60,H);c.close_path();col(c,colh,a);c.fill()
def roof(c,x,y,w,h,colh='#1a1410',a=1):
    poly(c,[(x-w*.62,y),(x+w*.62,y),(x+w*.45,y-h),(x-w*.45,y-h)],colh,a)
    c.move_to(x-w*.62,y);c.curve_to(x-w*.66,y-6,x-w*.7,y-14,x-w*.74,y-22);c.line_to(x-w*.6,y);col(c,colh,a);c.fill()
    c.move_to(x+w*.62,y);c.curve_to(x+w*.66,y-6,x+w*.7,y-14,x+w*.74,y-22);c.line_to(x+w*.6,y);c.fill()
def mist(c,y,t,a=.25,colh='#c8b8a0'):
    for k in range(6):
        x=(k*420+t*30)%(W+600)-300;glow(c,x,y+20*math.sin(k),260,colh,a)
def stars(c,t,a):
    r=random.Random(4)
    for k in range(90):
        x=r.uniform(0,W);y=r.uniform(0,420);circ(c,x,y,r.uniform(.8,2.2),'#efe6d2',a*(.5+.5*math.sin(t*2+k)))
# ---------- 玄武门 ----------
def gate(c,t,cx=0,dawn=.5,fire=0,flags=True,name='玄武門'):
    sky(c,lerp_h('#0c1020','#2a2236',dawn),lerp_h('#2a2a40','#c9784a',dawn),760)
    stars(c,t,1-dawn)
    glow(c,W*.75-cx*.1,640,500,'#e8a060',.35*dawn)
    # far palace roofs (parallax .3)
    ox=-cx*.3
    for i in range(9):
        x=ox+i*260-100;roof(c,x,520-(i%3)*18,200,40,'#1c1620',.85);rect(c,x-70,520-(i%3)*18,140,60,'#1c1620',.85)
    mist(c,560,t,.18)
    ox=-cx
    # wall
    rect(c,ox-400,470,W+800+abs(cx),360,'#3e3a3a')
    col(c,'#26221f',.8);c.set_line_width(1.5)
    for r_ in range(0,360,24):
        c.move_to(ox-400,470+r_);c.line_to(ox+W+800,470+r_)
        for k in range(-400,W+800,64):xx=ox+k+(32 if (r_//24)%2 else 0);c.move_to(xx,470+r_);c.line_to(xx,494+r_)
    c.stroke()
    for k in range(-400,W+800,48):rect(c,ox+k,444,30,28,'#3e3a3a')
    # tower
    gx=ox+W/2
    rect(c,gx-260,420,520,410,'#4a4442')
    c.new_sub_path();c.arc(gx,720,82,math.pi,2*math.pi);c.line_to(gx+82,830);c.line_to(gx-82,830);c.close_path();col(c,'#070506');c.fill()
    if fire>0:glow(c,gx,760,160,'#ff8a3a',.5*fire)
    rect(c,gx-220,300,440,124,'#6e1c16')
    for k in range(-4,5):rect(c,gx+k*50-7,300,14,124,'#a8302a')
    for k in range(-4,4):
        col(c,'#d9b56a',.35);c.set_line_width(1.2)
        for j in range(4):c.move_to(gx+k*50+8,316+j*26);c.line_to(gx+k*50+42,316+j*26)
        c.stroke()
    poly(c,[(gx-330,312),(gx+330,312),(gx+240,244),(gx-240,244)],'#18141a')
    poly(c,[(gx-200,244),(gx+200,244),(gx+140,186),(gx-140,186)],'#18141a')
    for sx in(-1,1):
        c.move_to(gx+sx*330,312);c.curve_to(gx+sx*350,300,gx+sx*360,286,gx+sx*372,270);c.line_to(gx+sx*320,312);col(c,'#18141a');c.fill()
    rect(c,gx-34,560,68,104,'#1a120c');rect(c,gx-28,566,56,92,'#d9b56a',.9)
    c.select_font_face(FONT,0,1);c.set_font_size(24);col(c,'#1a120c')
    for i,ch in enumerate(name):e=c.text_extents(ch);c.move_to(gx-e[4]/2,594+i*28);c.show_text(ch)
    if flags:
        for fx in (gx-560,gx-380,gx+380,gx+560):
            col(c,'#15100c');c.set_line_width(4);c.move_to(fx,450);c.line_to(fx,320);c.stroke()
            wv=math.sin(t*3+fx*.01)*7
            poly(c,[(fx,322),(fx+76,326+wv),(fx+76,390+wv),(fx,386)],'#c0392b');text(c,'唐',fx+38,368+wv,32,CREAM)
    # ground
    g=cairo.LinearGradient(0,830,0,H);g.add_color_stop_rgb(0,*hx('#2a2018')[:3]);g.add_color_stop_rgb(1,*hx('#0c0806')[:3]);c.set_source(g);c.rectangle(0,830,W,H-830);c.fill()
def lerp_h(a,b,k):
    A=hx(a);B_=hx(b);return '#%02x%02x%02x'%tuple(int(255*lerp(A[i],B_[i],cl(k))) for i in range(3))
def foreground_grass(c,t,cx=0,par=1.6,y=H,colh='#0a0705'):
    ox=-cx*par;r=random.Random(2)
    for k in range(70):
        x=(ox+k*40)%(W+200)-100;hh=r.uniform(40,120);sw=math.sin(t*2+k)*8
        c.move_to(x-6,y);c.curve_to(x-3,y-hh*.3,x+sw*.5,y-hh*.6,x+sw,y-hh);c.curve_to(x+sw*.5+4,y-hh*.6,x+4,y-hh*.3,x+6,y);col(c,colh);c.fill()
# ---------- 暗室 ----------
def cell(c,t):
    sky(c,'#160c0a','#0a0605')
    for r_ in range(0,760,50):
        for k in range(0,W,110):
            xx=k+(55 if (r_//50)%2 else 0);rect(c,xx+3,r_+3,104,44,'#2a1a14',.9)
    fl=.8+.2*math.sin(t*13)+.1*math.sin(t*31)
    glow(c,W*.62,430,700,'#ff8a3a',.35*fl)
    rect(c,0,760,W,H-760,'#120a08')
    # 木架+铁链
    rect(c,W*.18,250,24,520,'#3a2418');rect(c,W*.18,250,520,24,'#3a2418');rect(c,W*.18+496,250,24,520,'#3a2418')
    for k in range(3):
        x=W*.18+120+k*140
        for j in range(8):c.save();c.translate(x+math.sin(t*1.5+k)*3,290+j*16);c.scale(.6,1);col(c,'#6a6a6a',.9);c.set_line_width(3);c.new_sub_path();c.arc(0,0,7,0,7);c.stroke();c.restore()
    # candle
    x,y=W*.62,640;rect(c,x-60,y,120,140,'#2a1a10');rect(c,x-10,y-50,20,50,'#e8dcc0')
    c.move_to(x,y-90-6*math.sin(t*17));c.curve_to(x+12,y-66,x+8,y-52,x,y-52);c.curve_to(x-8,y-52,x-12,y-66,x,y-90-6*math.sin(t*17));col(c,'#ffc060');c.fill()
    glow(c,x,y-70,90,'#ffd080',.7*fl)
# ---------- 渭水 ----------
def river(c,t,scroll,dawn=.6):
    sky(c,lerp_h('#121626','#3a2a36',dawn),lerp_h('#3a3040','#d88a50',dawn),620)
    glow(c,W*.8,560,420,'#f0a860',.5*dawn)
    ridge(c,560,40,.003,'#1e1820',.9,scroll*.15,1)
    ridge(c,610,26,.006,'#2a2028',.95,scroll*.35,3)
    g=cairo.LinearGradient(0,620,0,860);g.add_color_stop_rgb(0,*hx('#4a5a64')[:3]);g.add_color_stop_rgb(1,*hx('#1a2228')[:3]);c.set_source(g);c.rectangle(0,620,W,240);c.fill()
    for k in range(40):
        x=(k*97-scroll*.8)%(W+200)-100;y=640+(k*37)%200
        col(c,'#c8d8d0',.25);c.set_line_width(2);c.move_to(x,y);c.line_to(x+60,y);c.stroke()
    rect(c,0,860,W,H-860,'#141008')
def steppe(c,t,scroll,dust=1):
    sky(c,'#2a1410','#a8502a',700)
    circ(c,W*.72,420,90,'#e86a3a',.85);glow(c,W*.72,420,400,'#ff9a50',.35)
    ridge(c,640,30,.002,'#3a1e16',.9,scroll*.2,2)
    rect(c,0,700,W,H-700,'#4a2a18')
    for k in range(10):glow(c,(k*240-scroll*.6)%(W+400)-200,760,240,'#a86a40',.25*dust)
def citylw(c,t,name='洛阳',fl='天策'):
    sky(c,'#1a1018','#8a4a2a',640)
    glow(c,W*.5,560,600,'#e8904a',.35)
    for i in range(12):x=i*170+40;roof(c,x,560-(i%2)*24,140,34,'#20161a',.9);rect(c,x-50,560-(i%2)*24,100,80,'#20161a',.9)
    rect(c,0,600,W,260,'#4a4038')
    for k in range(0,W,48):rect(c,k,576,30,26,'#4a4038')
    col(c,'#2a2420',.8);c.set_line_width(1.4)
    for r_ in range(0,260,26):c.move_to(0,600+r_);c.line_to(W,600+r_)
    c.stroke()
    for i,fx in enumerate(range(140,W,240)):
        col(c,'#15100c');c.set_line_width(4);c.move_to(fx,600);c.line_to(fx,470);c.stroke()
        wv=math.sin(t*3+i)*7;poly(c,[(fx,472),(fx+80,476+wv),(fx+80,540+wv),(fx,536)],'#c0392b');text(c,fl[i%2],fx+40,520+wv,34,CREAM)
    rect(c,0,860,W,H-860,'#141008')
def paper(c,x,y,w,h,a=1):
    rect(c,x,y,w,h,'#e8dcbc',a);rect(c,x,y,w,h,'#c8b48a',.0)
    r=random.Random(1)
    for k in range(200):circ(c,x+r.random()*w,y+r.random()*h,r.uniform(.5,2),'#a8946a',.25*a)
    col(c,'#8a6a3a',a);c.set_line_width(3);c.rectangle(x+14,y+14,w-28,h-28);c.stroke()
