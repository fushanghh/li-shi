exec(open('lc_young_lib.py').read())
import numpy as np, math
rng=np.random.default_rng(21)
poly([(0,0),(W,0),(W,1010),(0,1010)],'#5a2a14')
cx,cy=540,520
for k in range(7,0,-1):   # 同心风雪环
    c.arc(cx,cy,300+k*38,0,6.283); c.set_source_rgba(*hx('#c4692f',0.10+0.04*(7-k))); c.set_line_width(3); c.stroke()
g=cairo.RadialGradient(cx,cy,0,cx,cy,330); g.add_color_stop_rgba(0,*hx('#f2b56a')[:3],1); g.add_color_stop_rgba(0.85,*hx('#e08a3e')[:3],1); g.add_color_stop_rgba(1,*hx('#c4692f')[:3],1)
c.arc(cx,cy,320,0,6.283); c.set_source(g); c.fill()
for (x,y,r) in [(450,420,40),(640,600,28),(600,380,18),(470,650,22)]: ell(x,y,r,r,'#e7a35a')   # 月面斑
# 绕月旋转的雪粒
for _ in range(260):
    a=rng.uniform(0,6.283); r=rng.uniform(260,460); sz=rng.uniform(2,6)
    x,y=cx+r*math.cos(a),cy+r*math.sin(a)*0.95
    if y<900: ell(x,y,sz,sz,'#f7e3b8' if rng.random()<0.6 else '#f0c060')
for k in range(5):   # 弧形风线
    c.arc(cx,cy,350+k*22,3.6+k*0.1,4.4+k*0.1); c.set_source_rgba(*hx(CREAM,0.7)); c.set_line_width(3); c.stroke()
# 地面：黑剪影台阶纹
poly([(0,1010),(0,880),(W,880),(W,1010)],DARK)
for i in range(14): x=i*80; line([(x+10,910),(x+40,930),(x+70,910)],'#3a2a20',3)
# 林冲：正面亮相，花枪立地
lin(520,885,0.9,'stand')
# 一旁插着的酒葫芦
ell(840,868,14,14,GOLD); ell(840,846,9,9,GOLD); line([(840,838),(846,826)],RED,3)
# 名号 + 标语
def big(t,y,size,col,stroke):
    c.select_font_face("Noto Serif CJK SC",0,1); c.set_font_size(size); e=c.text_extents(t)
    c.move_to(W/2-e[4]/2,y); c.text_path(t); c.set_source_rgba(*hx(stroke)); c.set_line_width(10); c.stroke_preserve(); c.set_source_rgba(*hx(col)); c.fill()
big('豹子头 · 林冲',105,72,CREAM,DARK)
big('能打不能还手',205,88,GOLD,DARK)
# 字幕区
poly([(0,1010),(W,1010),(W,H),(0,H)],DARK)
line([(40,1030),(W-40,1030)],GOLD,3); line([(40,1040),(W-40,1040)],GOLD,1.5)
text('水浒英雄卡 · 第1集',W/2,1150,48,CREAM)
text('林冲',W/2,1230,48,'#e39a52')
for i in range(12): x=45+i*90; poly([(x,1340),(x+22,1365),(x,1390),(x-22,1365)],ORG); ell(x+45,1365,6,6,ORG)
s.write_to_png('open_still.png')
