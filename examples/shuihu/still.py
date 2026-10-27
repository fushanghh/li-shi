exec(open('lc_young_lib.py').read())
import numpy as np, math
rng=np.random.default_rng(11)
# 主舞台：陶土橙，远处山神庙与草料场火光
poly([(0,0),(W,0),(W,1010),(0,1010)],ORG)
ell(860,700,240,150,'#d98444'); ell(860,730,140,90,'#e39a52')        # 火光映天
for i in range(9): x=i*140-40; poly([(x,800),(x+70,690+(i%3)*25),(x+140,800)],'#a9552a')
# 远处草料场：黑剪影棚屋+金色火焰
for x,w in [(760,90),(860,110),(950,70)]: poly([(x-w/2,820),(x-w/2,790),(x,762),(x+w/2,790),(x+w/2,820)],DARK)
for k in range(12):
    x=730+k*20; h=rng.uniform(30,80); poly([(x-14,792),(x-6,792-h*0.6),(x,792-h),(x+8,792-h*0.5),(x+14,792)],GOLD if k%2 else '#f0d58a')
# 近景：黑剪影山神庙（左）、地面、枯树
poly([(0,1010),(0,860)]+[(xx,850+16*math.sin(xx/100)) for xx in range(0,W+1,40)]+[(W,1010)],DARK)
poly([(40,860),(40,690),(300,690),(300,860)],DARK)
poly([(0,700),(170,610),(340,700),(300,712),(170,640),(40,712)],DARK)
poly([(130,860),(130,770),(210,770),(210,860)],'#e39a52')                # 庙门透光
line([(990,860),(1000,640)],DARK,14); line([(996,720),(1060,660)],DARK,8); line([(998,690),(940,630)],DARK,7)
# 雪 + 风线
for _ in range(110): r=rng.uniform(2.5,6); ell(rng.uniform(0,W),rng.uniform(0,850),r,r,CREAM)
for k in range(5): line([(80+k*40,260+k*70),(300+k*40,290+k*70)],CREAM,3)
lin(440,880,1.08,'walk')
# 右上计数器
text('忍',930,96,30,CREAM)
c.save(); c.translate(960,190); c.scale(1.1,1.1)
text('×3',0,0,110,GOLD); c.restore()
for k in range(4): line([(870+k*30,215),(890+k*30,240)],'#f0d58a',3)   # 裂纹预兆
# 拟声字
c.save(); c.translate(170,200); c.rotate(-0.12); text('呼——',0,0,72,CREAM); c.restore()
# 字幕区
poly([(0,1010),(W,1010),(W,H),(0,H)],DARK)
line([(40,1030),(W-40,1030)],GOLD,3); line([(40,1040),(W-40,1040)],GOLD,1.5)
text('风雪压草厅，',W/2,1150,64,CREAM)
c.select_font_face("Noto Serif CJK SC",0,1); c.set_font_size(64)
w1=c.text_extents('一把火烧')[4]; w2=c.text_extents('到天明')[4]; x0=W/2-(w1+w2)/2
text('一把火烧',x0,1250,64,CREAM,'l'); text('到天明',x0+w1,1250,64,'#e39a52','l')
for i in range(12): x=45+i*90; poly([(x,1340),(x+22,1365),(x,1390),(x-22,1365)],ORG); ell(x+45,1365,6,6,ORG)
s.write_to_png('still.png')
