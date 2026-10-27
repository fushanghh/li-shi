import re, math
src=open('lc_shenhua.py').read()
head=src.split('# ---- 舞台 ----')[0]
linsrc=src.split('# ---- 林冲 ----')[1].split("lin(170")[0]
exec(head)          # 画布与工具函数
exec(linsrc)        # lin()
import numpy as np
# 背景：雪夜深蓝 + 金色放射光
poly([(0,0),(W,0),(W,H),(0,H)],'#162027')
cx,cy=W/2,640
for k in range(36):
    a=k/36*6.283; a2=a+0.06
    poly([(cx,cy),(cx+1200*math.cos(a),cy+1200*math.sin(a)),(cx+1200*math.cos(a2),cy+1200*math.sin(a2))],'#1f2d35' if k%2 else '#25363f')
c.save(); g=cairo.RadialGradient(cx,cy,0,cx,cy,520); g.add_color_stop_rgba(0,0.95,0.75,0.35,0.55); g.add_color_stop_rgba(1,0.95,0.75,0.35,0)
c.set_source(g); c.paint(); c.restore()
rng=np.random.default_rng(5)
for _ in range(90): ell(rng.uniform(0,W),rng.uniform(0,H),rng.uniform(2,4),rng.uniform(2,4),CREAM)
for _ in range(30):  # 金箔碎屑
    x,y=rng.uniform(80,W-80),rng.uniform(150,1150); poly([(x,y),(x+8,y+3),(x+3,y+10)],GOLD)
def rrect(x,y,w,h,r,col):
    c.new_sub_path(); c.arc(x+w-r,y+r,r,-1.57,0); c.arc(x+w-r,y+h-r,r,0,1.57); c.arc(x+r,y+h-r,r,1.57,3.14); c.arc(x+r,y+r,r,3.14,4.71); c.close_path()
    c.set_source_rgba(*hx(col)); c.fill()
CW,CH=440,640
def card_frame(x,y,rot):
    c.save(); c.translate(x,y); c.rotate(rot)
    rrect(-CW/2+10,-CH/2+16,CW,CH,26,'#0a0a0a')            # 投影
    rrect(-CW/2-8,-CH/2-8,CW+16,CH+16,30,GOLD)            # 金边
    rrect(-CW/2,-CH/2,CW,CH,24,DARK)
    return
# ---- 正面 ----
card_frame(300,640,-0.07)
rrect(-CW/2+18,-CH/2+18,CW-36,CH-150,16,ORG)
c.save(); c.rectangle(-CW/2+18,-CH/2+18,CW-36,CH-150); c.clip()
ell(110,-180,60,60,'#d98444')
for i in range(5): x=-200+i*100; poly([(x,130),(x+50,60+(i%2)*20),(x+100,130)],'#a9552a')
poly([(-CW/2+18,170),(-CW/2+18,110),(-60,100),(60,110),(CW/2-18,104),(CW/2-18,170)],DARK)
for _ in range(25): ell(rng.uniform(-190,190),rng.uniform(-290,90),2.5,2.5,CREAM)
lin(-10,150,0.62,'stand')
c.restore()
# 左上星位徽记
ell(-CW/2+52,-CH/2+52,34,34,GOLD); ell(-CW/2+52,-CH/2+52,28,28,DARK)
text('天雄',-CW/2+52,-CH/2+62,22,GOLD)
text('★★★★★',CW/2-80,-CH/2+60,22,GOLD)
text('豹子头 · 林冲',0,CH/2-80,44,CREAM)
text('天罡星 · 第六位',0,CH/2-35,24,'#d98444',bold=0)
c.restore()
# ---- 背面 ----
card_frame(780,690,0.06)
text('林冲',0,-CH/2+70,50,CREAM)
text('马军五虎将 · 前八十万禁军教头',0,-CH/2+112,20,'#d98444',bold=0)
line([(-CW/2+30,-CH/2+132),(CW/2-30,-CH/2+132)],GOLD,2)
rows=[('星位','天罡星 · 天雄星'),('武器','丈八蛇矛'),('必杀','风雪一枪')]
for i,(k,v) in enumerate(rows):
    y=-CH/2+180+i*48; text(k,-CW/2+40,y,24,GOLD,'l'); text(v,-CW/2+120,y,24,CREAM,'l',0)
# 数值条
stats=[('攻击',95,RED),('防御',88,'#3f7f86'),('忍耐',99,GOLD)]
for i,(k,v,col) in enumerate(stats):
    y=-CH/2+340+i*46; text(k,-CW/2+40,y,24,GOLD,'l')
    rrect(-CW/2+110,y-18,230,18,9,'#3a302a'); rrect(-CW/2+110,y-18,230*v/100,18,9,col)
    text(str(v),CW/2-40,y,26,CREAM,'r')
line([(-CW/2+30,-CH/2+480),(CW/2-30,-CH/2+480)],GOLD,2)
for i,t in enumerate(['京城枪棒第一师，被高俅陷害','刺配沧州。风雪山神庙手刃仇人，','雪夜投奔梁山。']):
    text(t,-CW/2+36,-CH/2+520+i*34,21,CREAM,'l',0)
c.restore()
# 标题印字
text('获得英雄卡！',W/2,150,84,GOLD)
text('水浒英雄卡 · 第一号',W/2,1300,40,CREAM,bold=0)
s.write_to_png('card.png')
