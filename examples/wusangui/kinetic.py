from lib import *
from hud import slam,eback
B=60/100
CREAM_='#f3e6c8';GD='#d9b56a';RD='#e0402e';ICE='#9fd0ff'
# (拍, 文字, 字号, 颜色, x, y, 方式)
G=[
 (0,4,[(0,'手握',120,CREAM_,620,330,'L'),(1,'天胡开局',240,GD,960,600,'S')]),
 (4,8,[(4,'麾下',120,CREAM_,620,320,'L'),(5,'百战精兵',240,GD,960,600,'S')]),
 (8,12,[(8,'平西王',130,CREAM_,960,300,'R'),(9,'吴三桂',280,RD,960,610,'S')]),
 (12,16,[(12,'短短几年',120,CREAM_,960,300,'L'),(13,'灰飞烟灭',250,'#c8c0b8',960,600,'S')]),
 (16,20,[(16,'他不是输在',110,CREAM_,960,270,'L'),(17,'军事',200,GD,760,560,'S'),(18,'✕',220,RD,1180,560,'P')]),
 (20,24,[(20,'而是死在',110,CREAM_,960,300,'R'),(21,'5个',240,RD,640,620,'S'),(22,'致命盲区',200,GD,1230,620,'S')]),
]
HOOK_END=24*B
def slam_times():
    out=[]
    for g0,g1,ws in G:
        for w in ws:out.append((w[0]*B,w[6]))
    return out
def word(c,T,w):
    b,s,size,h,x,y,mode=w;t0=b*B;u=T-t0
    if u<0:return
    c.save()
    if mode in 'LR':
        k=min(1,u/.18);e=1-(1-k)**3;dx=(1-e)*(-500 if mode=='L' else 500);c.translate(x+dx,y);a=k
    elif mode=='S':
        k=min(1,u/.16);sc=lerp(2.6,1,1-(1-k)**3)+ (0.08*math.sin(u*40)*math.exp(-u*10) if u>.16 else 0);c.translate(x,y);c.scale(sc,sc);a=k
    else:
        k=min(1,u/.14);sc=lerp(3,1,k);c.translate(x,y);c.rotate(-.08);c.scale(sc,sc);a=k
    c.select_font_face(FONT,0,1);c.set_font_size(size)
    tw=c.text_extents(s)[4]
    if mode=='P':
        pw=tw+size*.6;ph=size*1.3
        col(c,h,.95*a);c.set_line_width(size*.08);c.rectangle(-pw/2,-ph/2,pw,ph);c.stroke()
    c.move_to(-tw/2,size*.36);c.text_path(s)
    col(c,'#0a0604',a);c.set_line_width(size*.16);c.set_line_join(1);c.stroke_preserve()
    g=cairo.LinearGradient(0,-size*.5,0,size*.4);g.add_color_stop_rgba(0,*hx('#ffffff',a));g.add_color_stop_rgba(1,*hx(h,a));c.set_source(g);c.fill()
    c.restore()
    if mode=='S' and u<.12:
        # 冲击光圈
        r=lerp(80,700,u/.12);col(c,h,.5*(1-u/.12));c.set_line_width(14);c.new_sub_path();c.arc(x,y,r,0,2*math.pi);c.stroke()
def draw(c,T):
    if T>=HOOK_END:return
    rect(c,0,0,W,H,'#000000',.55)
    for g0,g1,ws in G:
        if g0*B<=T<g1*B:
            out=cl((T-(g1*B-.12))/.12)
            c.save()
            if out>0:c.translate(W/2,H/2);s_=1-.3*out;c.scale(s_,s_);c.translate(-W/2,-H/2)
            c.push_group()
            for w in ws:word(c,T,w)
            c.pop_group_to_source();c.paint_with_alpha(1-out)
            c.restore()
