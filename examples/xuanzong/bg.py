from lib import *
def palace(c,t,tone='red',dark=0):
    base={'red':'#2a1410','night':'#121520','grey':'#1e1c18'}[tone]
    g=cairo.LinearGradient(0,0,0,H);g.add_color_stop_rgb(0,*hx(base)[:3]);g.add_color_stop_rgb(1,*hx('#0e0907')[:3]);c.set_source(g);c.paint()
    wall={'red':'#5a1d16','night':'#24283a','grey':'#3a332b'}[tone]
    rect(c,0,90,W,560,wall)
    # lattice windows
    for i in range(8):
        x=40+i*240
        rect(c,x+20,190,170,300,'#3a120e' if tone=='red' else '#181a26')
        col(c,'#b8873e' if tone=='red' else '#5a6280',.55);c.set_line_width(2)
        for k in range(0,171,17):c.move_to(x+20+k,190);c.line_to(x+20+k,490)
        for k in range(0,301,17):c.move_to(x+20,190+k);c.line_to(x+190,190+k)
        c.stroke()
        if tone=='night':glow(c,x+105,340,160,'#e8a040',.18)
    # beam
    rect(c,0,60,W,50,'#7a2a1c' if tone=='red' else '#2a2e44');rect(c,0,104,W,10,'#d9b56a',.6)
    for i in range(9):
        x=i*240;rect(c,x-18,60,36,600,'#8e2a1e' if tone=='red' else '#30344a');rect(c,x-18,60,8,600,'#b8473a' if tone=='red' else '#3e4460',.6)
    # floor
    g=cairo.LinearGradient(0,650,0,H);g.add_color_stop_rgb(0,*hx('#3a2418' if tone=='red' else '#1a1c26')[:3]);g.add_color_stop_rgb(1,*hx('#120b08')[:3]);c.set_source(g);c.rectangle(0,650,W,H-650);c.fill()
    col(c,'#d9b56a',.12);c.set_line_width(1)
    for k in range(-20,40):c.move_to(W/2+k*90,650);c.line_to(W/2+k*260,H);
    c.stroke()
    # lanterns
    for i,x in enumerate([200,720,1200,1720]):
        sw=math.sin(t*1.3+i)*4
        col(c,'#15100c');c.set_line_width(2);c.move_to(x,110);c.line_to(x+sw,170);c.stroke()
        glow(c,x+sw,215,120,'#ff9a40',.35)
        poly(c,[(x+sw-28,175),(x+sw+28,175),(x+sw+34,215),(x+sw+28,255),(x+sw-28,255),(x+sw-34,215)],'#c0392b',1,'#15100c',2)
        rect(c,x+sw-30,172,60,6,'#d9b56a');rect(c,x+sw-30,252,60,6,'#d9b56a')
        col(c,'#c0392b');c.set_line_width(1.5)
        for k in range(-3,4):c.move_to(x+sw+k*6,258);c.line_to(x+sw+k*6,290);
        c.stroke()
    if dark:rect(c,0,0,W,H,'#000000',dark)
def throne(c,x,y):
    poly(c,[(x-330,y),(x+330,y),(x+290,y-50),(x-290,y-50)],'#7a1f1a',1,'#d9b56a',2)
    for k in range(3):rect(c,x-60+k*0,y+k*16,120,16,'#5a5450')
    rect(c,x-250,y-330,500,280,'#c99a2a');rect(c,x-235,y-315,470,250,'#3e5a5a')
    # screen mountains
    col(c,'#6a8a7a');c.move_to(x-235,y-65)
    for k in range(0,471,47):c.line_to(x-235+k,y-65-(60+50*math.sin(k*.05+1))*(1 if k%94 else 1.4))
    c.line_to(x+235,y-65);c.close_path();c.fill()
    circ(c,x+120,y-250,24,'#efe2c4',.8)
    poly(c,[(x-90,y-50),(x+90,y-50),(x+80,y-170),(x-80,y-170)],'#b8332a',1,'#d9b56a',3)
def citywall(c,t,sky='dusk',name='延喜门'):
    g=cairo.LinearGradient(0,0,0,700)
    tops={'dusk':('#3a1a14','#7a3a26'),'day':('#2a2a26','#6a5a40'),'red':('#2a0c0a','#8a2a1c'),'night':('#0e1018','#262c40')}[sky]
    g.add_color_stop_rgb(0,*hx(tops[0])[:3]);g.add_color_stop_rgb(1,*hx(tops[1])[:3]);c.set_source(g);c.paint()
    # far hills
    col(c,'#1c1612',.7);c.move_to(0,560)
    for x in range(0,W+60,60):c.line_to(x,520-40*math.sin(x*.004)-20*math.sin(x*.013))
    c.line_to(W,700);c.line_to(0,700);c.fill()
    rect(c,0,470,W,330,'#4a4440')
    col(c,'#2e2a27',.8);c.set_line_width(1.5)
    for r in range(0,330,22):
        c.move_to(0,470+r);c.line_to(W,470+r)
        for k in range(0,W,60):c.move_to(k+(30 if (r//22)%2 else 0),470+r);c.line_to(k+(30 if (r//22)%2 else 0),492+r)
    c.stroke()
    for k in range(0,W,46):rect(c,k,446,28,26,'#4a4440')
    # gate tower
    cx=W/2;rect(c,cx-200,400,400,400,'#55504a')
    c.arc(cx,700,70,math.pi,2*math.pi);c.line_to(cx+70,800);c.line_to(cx-70,800);col(c,'#0a0807');c.fill()
    rect(c,cx-170,300,340,110,'#7a1f1a')
    for k in range(-3,4):rect(c,cx+k*48-6,300,12,110,'#b8332a')
    poly(c,[(cx-260,310),(cx+260,310),(cx+190,250),(cx-190,250)],'#1c1816')
    poly(c,[(cx-150,250),(cx+150,250),(cx+110,200),(cx-110,200)],'#1c1816')
    rect(c,cx-26,560,52,80,'#1a120c');rect(c,cx-22,564,44,72,'#d9b56a',.85)
    vtext(c,name[:2],cx,592,22,'#1a120c')
    for fx in (cx-420,cx+420):
        col(c,'#15100c');c.set_line_width(4);c.move_to(fx,450);c.line_to(fx,330);c.stroke()
        wv=math.sin(t*3+fx)*6
        poly(c,[(fx,332),(fx+70,336+wv),(fx+70,396+wv),(fx,392)],'#c0392b')
        text(c,'唐',fx+35,376+wv,32,'#efe2c4')
    g=cairo.LinearGradient(0,800,0,H);g.add_color_stop_rgb(0,*hx('#2a2018')[:3]);g.add_color_stop_rgb(1,*hx('#0e0a07')[:3]);c.set_source(g);c.rectangle(0,800,W,H-800);c.fill()
