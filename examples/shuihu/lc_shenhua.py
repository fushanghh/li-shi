import cairocffi as cairo, math, numpy as np
from PIL import Image
W,H=1080,1440
s=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H); c=cairo.Context(s)
c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
def hx(h,a=1): h=h.lstrip('#'); return (int(h[:2],16)/255,int(h[2:4],16)/255,int(h[4:],16)/255,a)
ORG,DARK,ROBE,ROBE2,GOLD,CREAM,RED,STEEL='#c4692f','#1c1612','#22302e','#2f4440','#d9a441','#f1e3c8','#b8332a','#c9ccc6'
def poly(pts,col):
    c.move_to(*pts[0]); [c.line_to(*p) for p in pts[1:]]; c.close_path(); c.set_source_rgba(*hx(col)); c.fill()
def line(pts,col,w):
    c.move_to(*pts[0]); [c.line_to(*p) for p in pts[1:]]; c.set_source_rgba(*hx(col)); c.set_line_width(w); c.stroke()
def ell(x,y,rx,ry,col):
    c.save(); c.translate(x,y); c.scale(rx,ry); c.arc(0,0,1,0,6.283); c.restore(); c.set_source_rgba(*hx(col)); c.fill()
def text(t,x,y,size,col,anchor='c',bold=1):
    c.select_font_face("Noto Serif CJK SC",0,bold); c.set_font_size(size); e=c.text_extents(t)
    c.move_to(x-{'c':e[4]/2,'l':0,'r':e[4]}[anchor],y); c.set_source_rgba(*hx(col)); c.show_text(t)
# ---- 舞台 ----
poly([(0,0),(W,0),(W,1010),(0,1010)],ORG)
ell(860,170,90,90,'#d98444')                     # 落日
for (x,y) in [(230,130),(700,90)]:               # 卷云
    for k,dx in enumerate((-22,0,22)): ell(x+dx,y-(8 if k==1 else 0),20,18,DARK)
    poly([(x-44,y),(x+44,y),(x+44,y+10),(x-44,y+10)],DARK)
for i in range(9):                                # 远山压暗一档
    x=i*140-40; poly([(x,820),(x+70,700+(i%3)*25),(x+140,820)],'#a9552a')
poly([(0,1010),(0,860)]+[(x,850+18*math.sin(x/90)) for x in range(0,W+1,40)]+[(W,1010)],DARK)  # 黑剪影地面
# 雪
rng=np.random.default_rng(3)
for _ in range(70):
    x,y=rng.uniform(0,W),rng.uniform(0,840); ell(x,y,3,3,CREAM)
# ---- 林冲 ----
def lin(x,y,sc=1.0,pose='stand',face=1):
    c.save(); c.translate(x,y); c.scale(sc*face,sc)
    lean={'stand':0,'thrust':0.12,'walk':0.05}[pose]
    # 腿与靴
    sp={'stand':18,'thrust':60,'walk':34}[pose]
    for d in (-sp,sp):
        line([(d*0.4,-110),(d,-12)],DARK,16); poly([(d-14,-14),(d+22,-14),(d+26,0),(d-14,0)],DARK)
    c.rotate(lean)
    # 袍：细长剪影，下摆金线
    poly([(-40,-470),(40,-470),(66,-100),(-70,-100)],ROBE)
    poly([(4,-468),(22,-468),(10,-100),(-6,-100)],ROBE2)
    line([(-68,-112),(64,-112)],GOLD,4); line([(-38,-462),(4,-420),(40,-462)],GOLD,4)
    poly([(-52,-300),(52,-300),(53,-280),(-53,-280)],RED)               # 朱红腰带
    poly([(26,-282),(40,-282),(52,-200),(36,-198)],RED)
    # 头
    line([(0,-470),(2,-492)],CREAM,16)
    ell(4,-528,30,36,CREAM)
    ell(16,-534,4.5,5.5,DARK)                                   # 环眼
    line([(4,-548),(26,-542)],DARK,5)                           # 怒眉
    poly([(-14,-520),(30,-516),(34,-490),(22,-470),(14,-484),(8,-466),(0,-482),(-8,-470),(-14,-492)],DARK)  # 虎须
    poly([(-2,-526),(6,-526),(6,-518),(-2,-518)],GOLD)          # 金印
    # 白毡笠 + 红缨
    poly([(-58,-556),(64,-556),(50,-566),(-46,-566)],CREAM)
    c.move_to(-28,-562); c.curve_to(-26,-600,30,-600,32,-562); c.close_path(); c.set_source_rgba(*hx(CREAM)); c.fill()
    for k in range(5): line([(2,-596),(-30+k*16,-570)],RED,5)
    ell(2,-598,6,6,GOLD)
    # 手臂与蛇矛
    def spear(px,py,ang,L=430):
        dx,dy=math.sin(ang),-math.cos(ang)
        line([(px-dx*150,py-dy*150),(px+dx*L,py+dy*L)],'#6e3c20',7)
        tx,ty=px+dx*L,py+dy*L; nx,ny=-dy,dx
        # 蛇形矛头（波浪刃）
        pts=[(tx+nx*6,ty+ny*6)]
        for k in range(1,6): w=8*math.sin(k*1.6); pts.append((tx+dx*k*14+nx*(6+w),ty+dy*k*14+ny*(6+w)))
        pts.append((tx+dx*86,ty+dy*86))
        for k in range(5,0,-1): w=8*math.sin(k*1.6); pts.append((tx+dx*k*14-nx*(6-w),ty+dy*k*14-ny*(6-w)))
        pts.append((tx-nx*6,ty-ny*6)); poly(pts,STEEL)
        for k in range(4): line([(tx,ty),(tx-dx*30+nx*(k*8-12)-14,ty-dy*30+ny*(k*8-12)+20)],RED,5)
        return tx,ty
    if pose=='stand':
        line([(-30,-450),(-48,-330)],ROBE2,26); ell(-48,-322,10,10,CREAM)
        line([(30,-450),(70,-380),(84,-400)],ROBE2,26); ell(88,-404,11,11,CREAM)
        spear(88,-404,0.02,400)
    elif pose=='thrust':
        line([(-30,-450),(-80,-400)],ROBE2,26); ell(-86,-398,10,10,CREAM)
        line([(30,-450),(110,-420)],ROBE2,26); ell(118,-420,11,11,CREAM)
        tx,ty=spear(118,-420,1.57,170)
        for k in range(6): line([(tx+95+k*4,ty-50+k*20),(tx+135+k*10,ty-70+k*28)],GOLD,4)   # 放射光
        for r in range(3): line([(-160-r*40,-380+r*30),(-60-r*30,-380+r*30)],CREAM,3)      # 风线
    else:  # walk：花枪挑葫芦
        line([(-30,-450),(-60,-350)],ROBE2,26); ell(-62,-342,10,10,CREAM)
        line([(30,-450),(60,-420),(40,-470)],ROBE2,26); ell(38,-476,11,11,CREAM)
        dx,dy=math.sin(0.9),-math.cos(0.9)
        tx,ty=spear(38,-476,0.9,300)
        gx,gy=38+dx*230,-476+dy*230; line([(gx,gy),(gx,gy+40)],DARK,3)
        ell(gx,gy+52,11,11,GOLD); ell(gx,gy+80,18,20,GOLD)
    c.restore()
lin(170,880,0.88,'stand'); lin(470,880,0.88,'walk'); lin(700,880,0.88,'thrust')
# 姿势小签
for x,t in [(170,'亮相'),(470,'挑葫芦'),(730,'出枪')]: text(t,x,985,30,GOLD)
# ---- 下方字幕区 ----
poly([(0,1010),(W,1010),(W,H),(0,H)],DARK)
line([(40,1030),(W-40,1030)],GOLD,3); line([(40,1040),(W-40,1040)],GOLD,1.5)
text('豹子头 · 林冲',W/2,1130,70,CREAM)
text('白毡笠 红缨 · 环眼虎须 · 脸上金印',W/2,1210,34,'#d98444',bold=0)
text('皂袍金边 · 朱红腰带 · 丈八蛇矛',W/2,1265,34,'#d98444',bold=0)
for i in range(12):                              # 底部自有纹样：雪花菱格
    x=45+i*90; poly([(x,1340),(x+22,1365),(x,1390),(x-22,1365)],ORG); ell(x+45,1365,6,6,ORG)
s.write_to_png('lc_shenhua.png')
