import cairocffi as cairo, math, numpy as np
W,H=1080,1440
s=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H); c=cairo.Context(s)
c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
def hx(h,a=1): h=h.lstrip('#'); return (int(h[:2],16)/255,int(h[2:4],16)/255,int(h[4:],16)/255,a)
BG,BG2,BLK,LN,CREAM,GOLD,RED,MOON='#7a3a1c','#5e2c15','#17110d','#d0773a','#f2dcb0','#e2a548','#b8332a','#e8964f'
def poly(p,col,stroke=None,w=2.5):
    c.move_to(*p[0]); [c.line_to(*q) for q in p[1:]]; c.close_path(); c.set_source_rgba(*hx(col))
    if stroke: c.fill_preserve(); c.set_source_rgba(*hx(stroke)); c.set_line_width(w); c.stroke()
    else: c.fill()
def line(p,col,w): c.move_to(*p[0]); [c.line_to(*q) for q in p[1:]]; c.set_source_rgba(*hx(col)); c.set_line_width(w); c.stroke()
def ell(x,y,rx,ry,col,stroke=None,w=2.5):
    c.save(); c.translate(x,y); c.scale(rx,ry); c.arc(0,0,1,0,6.283); c.restore(); c.set_source_rgba(*hx(col))
    if stroke: c.fill_preserve(); c.set_source_rgba(*hx(stroke)); c.set_line_width(w); c.stroke()
    else: c.fill()
def text(t,x,y,size,col,anchor='c',bold=1,outline=None):
    c.select_font_face("Noto Serif CJK SC",0,bold); c.set_font_size(size); e=c.text_extents(t)
    c.move_to(x-{'c':e[4]/2,'l':0,'r':e[4]}[anchor],y)
    if outline: c.text_path(t); c.set_source_rgba(*hx(outline)); c.set_line_width(size*0.14); c.stroke_preserve(); c.set_source_rgba(*hx(col)); c.fill()
    else: c.set_source_rgba(*hx(col)); c.show_text(t)

def face(x,y,sc=1.0,close=False):
    """长椭圆米白脸、尖下巴、凌厉杏眼、粗剑眉、左颊金印；长黑发垂两侧"""
    c.save(); c.translate(x,y); c.scale(sc,sc)
    poly([(-60,-60),(-66,40),(-70,150),(-50,170),(-40,40)],BLK)          # 两侧长发
    poly([(60,-60),(66,40),(70,150),(50,170),(40,40)],BLK)
    poly([(-44,-50),(44,-50),(42,30),(16,86),(0,96),(-16,86),(-42,30)],CREAM)   # 脸
    poly([(-14,86),(14,86),(16,140),(-16,140)],CREAM)                    # 颈
    poly([(-48,-50),(48,-50),(46,-26),(10,-34),(0,-22),(-10,-34),(-46,-26)],BLK)  # 中分刘海
    for sgn in (-1,1):
        poly([(sgn*8,-6),(sgn*40,-18),(sgn*42,-10),(sgn*10,0)],BLK)       # 剑眉上挑
        poly([(sgn*10,10),(sgn*36,2),(sgn*30,14),(sgn*14,16)],BLK)        # 杏眼
    line([(0,16),(-3,52),(4,54)],'#c99a6a',2)
    line([(-8,70),(8,70)],RED,3)
    poly([(20,30),(32,30),(32,44),(20,44)],GOLD)                         # 金印（他的“第三只眼”）
    if close:
        for k in range(3): line([(20,30+k*5),(32,30+k*5)],'#8a5a1f',1)
    c.restore()

def hat(x,y,sc=1.0):
    """白范阳毡笠剪影化：黑笠身+橙线刻纹，红缨像冠饰一样竖起"""
    c.save(); c.translate(x,y); c.scale(sc,sc)
    poly([(-110,0),(-40,-20),(40,-20),(110,0),(96,10),(-96,10)],BLK,LN,2.5)
    poly([(-46,-16),(-40,-62),(40,-62),(46,-16)],BLK,LN,2.5)
    line([(-44,-26),(44,-26)],LN,2)
    for k in range(7):
        a=-math.pi/2+(k-3)*0.25
        poly([(0,-64),(70*math.cos(a)-6,-74+60*math.sin(a)),(70*math.cos(a)+6,-74+60*math.sin(a))],RED)
    poly([(-10,-70),(0,-86),(10,-70),(0,-60)],GOLD)
    c.restore()

def spear(x0,y0,x1,y1,w=7):
    """红缨枪：直杆、柳叶形米白枪头、枪头下一大团红缨"""
    line([(x0,y0),(x1,y1)],BLK,w); line([(x0,y0),(x1,y1)],LN,1.5)
    a=math.atan2(y1-y0,x1-x0); dx,dy=math.cos(a),math.sin(a); nx,ny=-dy,dx
    P=lambda d,o:(x1+dx*d+nx*o,y1+dy*d+ny*o)
    poly([P(0,-6),P(8,-6),P(8,6),P(0,6)],GOLD)                 # 枪颈箍
    poly([P(8,0),P(30,-14),P(80,-8),P(110,0),P(80,8),P(30,14)],CREAM)   # 柳叶枪头
    line([P(14,0),P(96,0)],'#c9a777',2)                          # 枪脊
    for k in range(9):                                           # 红缨散开下垂
        o=(k-4)*7
        poly([P(2,o*0.3-2),P(2,o*0.3+2),P(-58-abs(o)*0.6,o*1.9+3),P(-62-abs(o)*0.6,o*1.9-3)],RED)
def linchong(x,y,sc=1.0):
    """宽站姿：方肩甲、长身甲片、V形护腹、圆拳、黑披风；全黑剪影+橙色刻线"""
    c.save(); c.translate(x,y); c.scale(sc,sc)
    # 披风
    poly([(-70,-430),(70,-430),(140,-60),(60,-40),(0,-80),(-90,-40),(-150,-70)],BLK)
    # 腿靴
    for sgn in (-1,1):
        poly([(sgn*20,-170),(sgn*58,-170),(sgn*80,-40),(sgn*44,-40)],BLK,LN)
        poly([(sgn*40,-50),(sgn*88,-50),(sgn*92,0),(sgn*30,0)],BLK,LN)
    # 身甲
    poly([(-58,-440),(58,-440),(64,-260),(84,-130),(-84,-130),(-64,-260)],BLK,LN)
    for k in range(-3,4): line([(k*18,-250),(k*22,-140)],LN,2)         # 甲裙竖片
    poly([(-40,-430),(40,-430),(0,-300)],BLK,LN)                        # V形护胸
    line([(-30,-400),(0,-330),(30,-400)],LN,2)
    ell(0,-282,16,10,BLK,LN)                                           # 护腹圆扣
    poly([(-66,-268),(66,-268),(66,-248),(-66,-248)],RED)               # 朱红腰带
    poly([(30,-250),(48,-250),(58,-170),(40,-168)],RED)
    # 方肩甲
    for sgn in (-1,1):
        poly([(sgn*50,-450),(sgn*112,-440),(sgn*118,-380),(sgn*58,-388)],BLK,LN)
        for k in range(3): line([(sgn*60,-430+k*16),(sgn*112,-424+k*16)],LN,1.5)
    # 手臂：短而方，圆拳
    poly([(-110,-400),(-86,-404),(-96,-300),(-122,-300)],BLK,LN); ell(-110,-290,16,16,CREAM)
    poly([(86,-404),(112,-400),(150,-340),(130,-326)],BLK,LN); ell(150,-322,16,16,CREAM)
    spear(146,-80,146,-640)
    ell(150,-322,16,16,CREAM)
    # 酒葫芦挂腰
    line([(-58,-250),(-70,-216)],LN,2); ell(-72,-204,10,10,GOLD); ell(-74,-178,16,18,GOLD)
    face(0,-560,0.95)
    hat(0,-600,1.0)
    c.restore()

# ---- 舞台 ----
poly([(0,0),(W,0),(W,1010),(0,1010)],BG)
rng=np.random.default_rng(2)
for _ in range(1500): ell(rng.uniform(0,W),rng.uniform(0,1010),1,1,'#6c3318')   # 纸纹颗粒
cx,cy=560,470
for k in range(8,0,-1):
    c.arc(cx,cy,280+k*40,0,6.283); c.set_source_rgba(*hx(LN,0.35)); c.set_line_width(2.5); c.stroke()
ell(cx,cy,290,290,MOON)
for (x,y,r) in [(480,380,46),(650,520,30),(620,340,20)]: ell(x,y,r,r,'#d9813f')
def cloud(x,y):   # 自家云：雪花卷，而不是∞纹
    poly([(x-46,y),(x-30,y-22),(x,y-30),(x+30,y-22),(x+46,y)],BLK)
    c.arc(x-12,y-12,8,0,6.283); c.set_source_rgba(*hx(LN)); c.set_line_width(2.5); c.stroke()
    c.arc(x+12,y-12,8,0,6.283); c.stroke()
cloud(160,170); cloud(920,140); cloud(880,560)
# 雪
for _ in range(80): r=rng.uniform(2,4); ell(rng.uniform(0,W),rng.uniform(0,860),r,r,CREAM)
# 地面条：黑底 + 雪花菱纹
poly([(0,880),(W,880),(W,1010),(0,1010)],BLK)
line([(0,884),(W,884)],LN,2)
for i in range(14): x=i*80+20; poly([(x,920),(x+14,940),(x,960),(x-14,940)],BG)
linchong(540,880,1.0)
# 名牌（学杨戬片里角色出场挂名签的做法）
text('LIN CHONG',790,330,20,CREAM,'l',0); text('豹子头',790,370,34,CREAM,'l',1)
# 字幕区
poly([(0,1010),(W,1010),(W,H),(0,H)],'#120d0a')
line([(40,1030),(W-40,1030)],LN,3)
text('八十万禁军教头，',W/2,1130,56,CREAM)
text('一杆红缨枪',W/2-120,1220,56,CREAM); text('镇京城',W/2+160,1220,56,GOLD)
for i in range(12): x=45+i*90; poly([(x,1340),(x+22,1365),(x,1390),(x-22,1365)],LN); ell(x+45,1365,6,6,LN)
s.write_to_png('yj_lin_full.png')

# ---- 脸部特写 ----
s2=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H); c=cairo.Context(s2); c.set_line_cap(1); c.set_line_join(1)
poly([(0,0),(W,0),(W,1010),(0,1010)],'#3b1c0f')
ell(540,560,430,430,BG); ell(540,560,380,380,'#9a4a22')
face(540,620,2.8,True)
hat(540,508,2.6)
poly([(0,1010),(W,1010),(W,H),(0,H)],'#120d0a'); line([(40,1030),(W-40,1030)],LN,3)
text('豹子头 · 林冲',W/2,1120,56,CREAM)
text('风雪夜 · 一杆枪',W/2,1250,92,GOLD,outline='#3b1c0f')
for i in range(12): x=45+i*90; poly([(x,1340),(x+22,1365),(x,1390),(x-22,1365)],LN); ell(x+45,1365,6,6,LN)
s2.write_to_png('yj_lin_face.png')
