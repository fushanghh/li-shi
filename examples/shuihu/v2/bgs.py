"""v2 背景：每个场景多层（远山/中景建筑/近景剪影/地面花边），带视差"""
import math, random
from engine import *

GY = 880  # 地平线（世界坐标）

def sv(p):
    p.c.save()
    if p.gc is not None: p.gc.save()
def rs(p):
    p.c.restore()
    if p.gc is not None: p.gc.restore()
def par(p, cam, f):
    """视差：f=1 跟随镜头，f<1 远景移动更少"""
    for c in (p.c, p.gc):
        if c is not None: c.translate((cam[0] - SCX) * (1 - f), (cam[1] - SCY) * (1 - f) * 0.5)

def sky(p, top, bot, x0=-1500, x1=2600):
    p.vgrad(x0, -600, x1 - x0, GY + 200, top, bot)

def mountains(p, seed, y, amp, col, x0=-1600, x1=2700, step=120, snowcap=False):
    rnd = random.Random(seed); pts = [(x0, GY + 300)]
    x = x0
    peaks = []
    while x <= x1:
        h = y - rnd.uniform(0, amp); pts.append((x, h)); peaks.append((x, h)); x += step * rnd.uniform(.7, 1.3)
    pts.append((x1, GY + 300))
    p.curve(pts, None, 1, close=True, fill=col)
    if snowcap:
        for (px, py) in peaks:
            if py < y - amp * 0.55:
                p.poly([(px - 40, py + 34), (px, py - 2), (px + 40, py + 34), (px + 16, py + 26), (px, py + 40), (px - 16, py + 26)], 'SNOW', a=0.85)

def ground_band(p, col='BLK', y=GY, x0=-1600, x1=2700, pattern='chev', ln='LN'):
    p.rect(x0, y, x1 - x0, 400, col)
    p.line([(x0, y + 3), (x1, y + 3)], ln, 3)
    if pattern == 'chev':
        for i in range(int(x0), int(x1), 70):
            p.line([(i + 20, y + 34), (i + 42, y + 56), (i + 20, y + 78)], ln, 3)
    elif pattern == 'dots':
        for i in range(int(x0), int(x1), 50):
            p.ell(i, y + 30, 4, 4, ln); p.poly([(i + 20, y + 44), (i + 30, y + 30), (i + 40, y + 44)], ln)
        p.curve([(x, y + 60 + 8 * math.sin(x / 40)) for x in range(int(x0), int(x1), 20)], ln, 2)
    elif pattern == 'tiles':
        for i in range(int(x0), int(x1), 120):
            p.line([(i, y + 4), (i - 160, y + 130)], 'LN2', 2)
        for k in range(3): p.line([(x0, y + 26 + k * 34), (x1, y + 26 + k * 34)], 'LN2', 1.5)
    elif pattern == 'snow':
        p.rect(x0, y - 6, x1 - x0, 20, 'SNOW', a=0.9)
        rnd = random.Random(4)
        for i in range(int(x0), int(x1), 90): p.ell(i + rnd.uniform(0, 40), y + 6, rnd.uniform(30, 60), 12, 'SNOW')

def pine(p, x, y, h=420, s=1.0, col='BLK', snow=False):
    p.poly([(x - 10 * s, y), (x + 10 * s, y), (x + 5 * s, y - h), (x - 5 * s, y - h)], col)
    tiers = 6
    for i in range(tiers):
        k = i / tiers; yy = y - h * 0.3 - h * 0.7 * k; w_ = (120 - 85 * k) * s
        p.poly([(x - w_, yy), (x, yy - 90 * s), (x + w_, yy)], col)
        if snow: p.poly([(x - w_ * .7, yy - 22 * s), (x, yy - 90 * s), (x + w_ * .7, yy - 22 * s), (x, yy - 60 * s)], 'SNOW', a=0.9)

def gnarled(p, x, y, h=520, s=1.0, col='BLK', seed=0, snow=False):
    rnd = random.Random(seed)
    p.poly([(x - 26 * s, y), (x + 26 * s, y), (x + 14 * s, y - h * .6), (x + 4 * s, y - h), (x - 6 * s, y - h), (x - 14 * s, y - h * .6)], col)
    for i in range(6):
        yy = y - h * (0.45 + 0.09 * i); d = 1 if i % 2 else -1; L = rnd.uniform(90, 180) * s
        p.line([(x, yy), (x + d * L * .6, yy - 40 * s), (x + d * L, yy - 30 * s - rnd.uniform(0, 50) * s)], col, (12 - i) * s)
        if snow: p.line([(x + d * L * .6, yy - 46 * s), (x + d * L, yy - 36 * s)], 'SNOW', 5 * s)
    for i in range(5):
        p.ell(x + rnd.uniform(-170, 170) * s, y - h - rnd.uniform(-40, 80) * s, rnd.uniform(70, 120) * s, rnd.uniform(40, 70) * s, col)

def roof(p, x, y, w_, h_, col='BLK', ln='LN', tiles=True):
    p.poly([(x - w_ / 2 - 40, y), (x - w_ / 2, y - h_ * 0.35), (x - w_ / 2 + 30, y - h_), (x + w_ / 2 - 30, y - h_), (x + w_ / 2, y - h_ * 0.35), (x + w_ / 2 + 40, y), (x + w_ / 2 + 60, y - 22), (x + w_ / 2 + 30, y + 6), (x - w_ / 2 - 30, y + 6), (x - w_ / 2 - 60, y - 22)], col, ln, 2.5)
    if tiles:
        for i in range(int(w_ / 22)):
            xx = x - w_ / 2 + 10 + i * 22
            p.line([(xx, y - h_ + 6), (xx - (xx - x) * 0.12, y - 4)], ln, 1.4, 0.7)
    p.ell(x - w_ / 2 + 30, y - h_ - 6, 10, 14, col); p.ell(x + w_ / 2 - 30, y - h_ - 6, 10, 14, col)

def lantern(p, g, x, y, t, s=1.0, lit=True):
    p.line([(x, y - 40 * s), (x, y - 20 * s)], 'BLK', 2)
    p.ell(x, y, 18 * s, 22 * s, 'RED', 'BLK', 2); p.rect(x - 10 * s, y - 24 * s, 20 * s, 5 * s, 'BLK'); p.rect(x - 10 * s, y + 20 * s, 20 * s, 5 * s, 'BLK')
    p.line([(x, y + 24 * s), (x, y + 44 * s)], 'GOLD', 2)
    if lit and g is not None: g.ell(x, y, 22 * s, 26 * s, 'FIRE', a=0.35 + 0.1 * math.sin(t * 7 + x))

def banner(p, x, y, t, txt='禁', h=200, col='RED', s=1.0):
    p.line([(x, y), (x, y - h * s)], 'BLK', 6 * s)
    pts = []
    for i in range(7):
        k = i / 6; wv = math.sin(t * 4 + k * 4 + x * .01) * 10 * k * s
        pts.append((x + k * 90 * s, y - h * s + 6 + wv))
    bot = [(px, py + 120 * s) for px, py in reversed(pts)]
    p.poly(pts + bot[:-1] + [(x, y - h * s + 126 * s)], col, 'BLK', 2)
    p.poly([(x + 80 * s, y - h * s + 120 * s + math.sin(t * 4 + 4) * 10 * s), (x + 100 * s, y - h * s + 140 * s), (x + 60 * s, y - h * s + 128 * s)], col)
    p.text(txt, x + 44 * s, y - h * s + 82 * s + math.sin(t * 4 + 2) * 5 * s, 56 * s, 'CREAM')

def crows(p, t, x0, y0, n=5, seed=1):
    rnd = random.Random(seed)
    for i in range(n):
        x = x0 + i * 60 + t * 80 + rnd.uniform(-20, 20); y = y0 + rnd.uniform(-40, 40) + math.sin(t * 3 + i) * 8
        f = math.sin(t * 12 + i) * 10
        p.line([(x - 18, y - f), (x, y), (x + 18, y - f)], 'BLK', 4)

# ============ 场景背景 ============
def bg_moon(p, g, t, cam, dark=False):
    sv(p); par(p, cam, 0.2)
    p.rect(-1500, -600, 4000, 2000, '#6a3218' if not dark else '#2c140a')
    cx, cy = 540, 450
    for k in range(10, 0, -1):
        p.ring(cx, cy, 270 + k * 40 + math.sin(t * 1.5 + k) * 3, 'LN', 2.2, 0.28)
    p.radial(cx, cy, 520, 'FIRE', 0.25, 0)
    p.ell(cx, cy, 285, 285, '#ec9a52')
    for (x, y, r) in [(450, 360, 50), (640, 520, 34), (610, 330, 22), (480, 560, 26), (690, 420, 16)]: p.ell(x, y, r, r, '#d9823f')
    cloud_icon(p, 150, 170, 1.0); cloud_icon(p, 930, 130, 0.8); cloud_icon(p, 960, 640, 1.1); cloud_icon(p, 120, 700, 0.7)
    rs(p)
    sv(p); par(p, cam, 0.6)
    mountains(p, 3, 830, 120, '#4a2412', step=160)
    rs(p)
    ground_band(p, 'BLK', GY, pattern='chev')

def bg_drill(p, g, t, cam):
    sv(p); par(p, cam, 0.15)
    sky(p, '#c26a32', '#a85428')
    cloud_icon(p, 120, 160, 0.9); cloud_icon(p, 760, 120, 1.1); cloud_icon(p, 1500, 170, 0.9)
    mountains(p, 7, 600, 120, '#9c4c26', step=170)
    rs(p)
    sv(p); par(p, cam, 0.35)
    # 城墙 + 城楼
    p.rect(-1600, 640, 4300, 160, '#7e3b1c'); 
    for i in range(-1600, 2700, 60): p.rect(i, 620, 36, 24, '#7e3b1c')
    for k in range(3): p.line([(-1600, 680 + k * 36), (2700, 680 + k * 36)], '#6a3016', 2)
    for gx in (-500, 900, 2100):
        p.rect(gx - 170, 470, 340, 170, '#6a3016'); roof(p, gx, 470, 340, 70, '#2a1a10', 'LN2'); roof(p, gx, 400, 240, 60, '#2a1a10', 'LN2')
        for k in range(4): p.rect(gx - 150 + k * 90, 500, 40, 100, '#3a2214')
    rs(p)
    sv(p); par(p, cam, 0.7)
    for i, x in enumerate(range(-900, 2400, 300)): banner(p, x, 870, t + i, '禁', 300, 'RED' if i % 2 else 'BLK', 0.8)
    rs(p)
    ground_band(p, 'BLK', GY, pattern='tiles')

def platform(p, x, y, w_=300, h_=110):
    p.poly([(x - w_ / 2, y + h_), (x + w_ / 2, y + h_), (x + w_ / 2 - 20, y), (x - w_ / 2 + 20, y)], 'BLK', 'LN', 3)
    for k in range(3): p.line([(x - w_ / 2 + 10 + k * 6, y + 30 + k * 26), (x + w_ / 2 - 10 - k * 6, y + 30 + k * 26)], 'LN2', 2)
    # 战鼓
    p.ell(x + w_ / 2 - 40, y - 50, 40, 46, 'RED2', 'BLK', 3); p.ell(x + w_ / 2 - 40, y - 50, 30, 36, 'RED', 'GOLD', 2)

def temple_big(p, g, x, t, plaque='东岳庙'):
    y = GY
    # 台基 + 台阶
    p.rect(x - 420, y - 40, 840, 40, '#2a1a10'); p.line([(x - 420, y - 40), (x + 420, y - 40)], 'LN', 2)
    for k in range(3): p.rect(x - 120 + k * 10, y - 40 + k * 13, 240 - k * 20, 13, '#3a2416')
    # 柱 + 门
    for k in (-330, -200, 200, 330): p.rect(x + k - 16, y - 330, 32, 290, 'RED'); p.line([(x + k - 16, y - 300), (x + k + 16, y - 300)], 'GOLD', 3)
    p.rect(x - 184, y - 320, 368, 280, '#3a1c10')
    for k in range(4):
        dx = x - 176 + k * 88
        p.rect(dx, y - 300, 80, 250, '#5a2a16')
        for j in range(5): p.line([(dx + 6, y - 290 + j * 44), (dx + 74, y - 290 + j * 44)], 'BLK', 2); p.line([(dx + 40, y - 300), (dx + 40, y - 60)], 'BLK', 2)
    # 斗拱 + 双檐
    for k in range(-6, 7): p.rect(x + k * 60 - 14, y - 360, 28, 30, 'BLK'); p.rect(x + k * 60 - 20, y - 370, 40, 10, 'GOLD', a=0.8)
    roof(p, x, y - 370, 840, 120, 'BLK'); p.rect(x - 320, y - 520, 640, 50, 'BLK'); roof(p, x, y - 500, 560, 110, 'BLK')
    p.rect(x - 90, y - 470, 180, 60, 'GOLD'); p.rect(x - 82, y - 462, 164, 44, 'BLK'); p.text(plaque, x, y - 428, 34, 'GOLD')
    for k in (-260, 260): lantern(p, g, x + k, y - 300, t)

def censer(p, g, x, t):
    y = GY
    p.poly([(x - 70, y - 120), (x + 70, y - 120), (x + 56, y - 40), (x - 56, y - 40)], 'BLK', 'LN', 3)
    p.rect(x - 80, y - 134, 160, 16, 'BLK'); p.line([(x - 50, y - 40), (x - 60, y)], 'BLK', 10); p.line([(x + 50, y - 40), (x + 60, y)], 'BLK', 10)
    p.ell(x, y - 84, 24, 18, 'BLK', 'GOLD', 2)
    for k in range(3):
        xs = x - 20 + k * 20
        p.curve([(xs + 6 * math.sin(t * 2 + j * .8 + k), y - 140 - j * 40) for j in range(7)], 'CREAM', 3, 0.45)

def stone_lion(p, x, face=1):
    y = GY
    p.rect(x - 50, y - 50, 100, 50, 'BLK'); p.line([(x - 50, y - 50), (x + 50, y - 50)], 'LN', 2)
    p.curve([(x - 40, y - 50), (x - 44, y - 130), (x - 10, y - 170), (x + 30 * face, y - 160), (x + 40, y - 110), (x + 34, y - 50)], None, 1, close=True, fill='BLK')
    for k in range(4): p.arc(x - 10 + k * 10, y - 140, 10, 0, math.pi, 'LN', 2)

def bg_temple(p, g, t, cam):
    sv(p); par(p, cam, 0.15)
    sky(p, '#c66e34', '#ac5a2c')
    cloud_icon(p, 160, 150, 0.9); cloud_icon(p, 900, 110, 1.0); cloud_icon(p, 1600, 160, 0.8)
    mountains(p, 11, 620, 110, '#a45429', step=180)
    rs(p)
    sv(p); par(p, cam, 0.5)
    mountains(p, 12, 760, 80, '#8a4222', step=150)
    gnarled(p, -260, GY, 560, 1.0, '#1d140e', seed=2)
    rs(p)
    temple_big(p, g, 780, t)
    censer(p, g, 330, t); stone_lion(p, 1240, -1); stone_lion(p, 320 + 0 * 1, 1) if False else None
    ground_band(p, 'BLK', GY, pattern='dots')

def bg_street(p, g, t, cam):
    sv(p); par(p, cam, 0.2)
    sky(p, '#c46c34', '#aa582a'); cloud_icon(p, 300, 140, 0.9); cloud_icon(p, 980, 180, 0.7)
    mountains(p, 21, 640, 90, '#9c4c26', step=200)
    rs(p)
    sv(p); par(p, cam, 0.6)
    for i, hx_ in enumerate(range(-400, 1800, 280)):
        p.rect(hx_ - 120, GY - 260, 240, 260, '#5a2a16'); roof(p, hx_, GY - 260, 240, 70, 'BLK', 'LN2')
        p.rect(hx_ - 90, GY - 220, 70, 160, '#2a1a10'); p.rect(hx_ + 20, GY - 220, 70, 100, '#2a1a10')
        if i % 2: lantern(p, g, hx_ - 100, GY - 270, t, 0.8)
    rs(p)
    # 招牌“刀”
    p.line([(140, GY), (140, GY - 380)], 'BLK', 8); p.rect(140, GY - 370, 90, 200, 'CREAM', ); p.poly([(140, GY - 370), (230, GY - 370), (230, GY - 170), (140, GY - 170)], 'CREAM', 'BLK', 4)
    p.text('宝', 185, GY - 290, 60, 'RED'); p.text('刀', 185, GY - 205, 60, 'RED')
    # 柳树
    p.line([(980, GY), (990, GY - 380)], 'BLK', 26)
    for k in range(9):
        x0 = 990 + (k - 4) * 34
        p.curve([(990, GY - 380), (x0, GY - 400), (x0 + 6 * math.sin(t * 2 + k), GY - 260), (x0 + 10 * math.sin(t * 2 + k + 1), GY - 140)], 'BLK', 6)
    ground_band(p, 'BLK', GY, pattern='dots')

def tiger_screen(p, x, y, w_=520, h_=360):
    p.rect(x - w_ / 2 - 16, y - 16, w_ + 32, h_ + 32, 'BLK'); p.rect(x - w_ / 2, y, w_, h_, '#c47a3c')
    # 抽象白虎：身体 + 条纹
    p.curve([(x - 200, y + 260), (x - 120, y + 180), (x + 40, y + 170), (x + 160, y + 200), (x + 210, y + 150), (x + 230, y + 220), (x + 180, y + 280), (x + 60, y + 290), (x - 120, y + 300)], None, 1, close=True, fill='CREAM')
    p.ell(x + 200, y + 150, 46, 40, 'CREAM'); p.poly([(x + 186, y + 116), (x + 196, y + 96), (x + 206, y + 116)], 'CREAM'); p.poly([(x + 214, y + 118), (x + 228, y + 98), (x + 234, y + 122)], 'CREAM')
    for k in range(7): p.poly([(x - 140 + k * 46, y + 186), (x - 120 + k * 46, y + 186), (x - 110 + k * 46, y + 250), (x - 128 + k * 46, y + 240)], 'BLK')
    p.poly([(x + 196, y + 150), (x + 212, y + 146), (x + 208, y + 154)], 'BLK'); p.line([(x + 216, y + 170), (x + 240, y + 168)], 'BLK', 3)
    p.curve([(x - 200, y + 260), (x - 260, y + 200), (x - 230, y + 120), (x - 200, y + 100)], 'CREAM', 14)
    p.text('白虎', x - 200, y + 60, 34, 'BLK')

def bg_hall(p, g, t, cam, plaque_on=True):
    sv(p); par(p, cam, 0.5)
    p.rect(-1600, -600, 4400, 2000, '#7a321a')
    for i in range(-1600, 2800, 120): p.line([(i, STAGE_T - 200), (i, GY)], '#6a2a14', 3)
    tiger_screen(p, 540, 300, 560, 380)
    rs(p)
    # 帷幔
    for i in range(-1200, 2400, 180):
        p.curve([(i, STAGE_T - 100), (i + 90, STAGE_T + 60), (i + 180, STAGE_T - 100)], None, 1, close=True, fill='RED2')
        p.line([(i + 90, STAGE_T + 60), (i + 90, STAGE_T + 100)], 'GOLD', 4); p.ell(i + 90, STAGE_T + 106, 8, 10, 'GOLD')
    if plaque_on:
        p.rect(340, 90, 400, 110, 'BLK'); p.poly([(340, 90), (740, 90), (740, 200), (340, 200)], 'BLK', 'GOLD', 5); p.text('白虎节堂', 540, 168, 64, 'GOLD')
    for x in (-500, -40, 1120, 1580): 
        p.rect(x - 30, STAGE_T - 200, 60, GY - STAGE_T + 200, 'RED'); [p.line([(x - 30, y), (x + 30, y)], 'GOLD', 4) for y in (300, 320, 700, 720)]
    # 兵器架
    for x in (90, 990):
        p.rect(x - 60, GY - 200, 120, 12, 'BLK'); p.rect(x - 60, GY - 60, 120, 12, 'BLK')
        for k in range(4): spear_icon(p, x - 45 + k * 30, GY - 30, GY - 300)
    ground_band(p, '#1a100a', GY, pattern='tiles')

def spear_icon(p, x, y0, y1):
    p.line([(x, y0), (x, y1)], 'BLK', 5); p.poly([(x - 7, y1), (x, y1 - 40), (x + 7, y1)], 'CREAM'); p.line([(x - 6, y1 + 6), (x + 6, y1 + 6)], 'RED', 6)

def bg_road(p, g, t, cam):
    sv(p); par(p, cam, 0.1)
    sky(p, '#a85428', '#8e4220'); cloud_icon(p, 200, 150, 1.0); cloud_icon(p, 1100, 120, 0.8)
    mountains(p, 31, 520, 160, '#7e3c1c', step=220)
    rs(p)
    sv(p); par(p, cam, 0.3)
    mountains(p, 32, 680, 140, '#5e2c14', step=160)
    rs(p)
    sv(p); par(p, cam, 0.6)
    mountains(p, 33, 800, 80, '#3e1c0c', step=120)
    for x in range(-800, 2600, 380): gnarled(p, x, GY, 320, 0.6, '#24160e', seed=x)
    rs(p)
    ground_band(p, 'BLK', GY, pattern='chev')

def bg_forest(p, g, t, cam, broken_tree=None):
    sv(p); par(p, cam, 0.15)
    sky(p, '#7a3e1c', '#5a2c14')
    for k in range(3): p.rect(-1600, 300 + k * 140, 4400, 40, 'CREAM', a=0.05)
    rs(p)
    sv(p); par(p, cam, 0.3)
    for x in range(-900, 2600, 130): gnarled(p, x, GY - 40, 600, 0.55, '#4a2814', seed=x + 3)
    rs(p)
    sv(p); par(p, cam, 0.6)
    for x in range(-900, 2600, 260): gnarled(p, x + 60, GY, 700, 0.85, '#2e1a0e', seed=x + 7)
    rs(p)
    ground_band(p, 'BLK', GY, pattern='dots')

def bg_manor(p, g, t, cam):
    sv(p); par(p, cam, 0.15)
    sky(p, '#c26a32', '#a85428'); cloud_icon(p, 140, 130, 0.8); cloud_icon(p, 860, 160, 1.0)
    mountains(p, 41, 600, 100, '#9c4c26', step=190)
    rs(p)
    sv(p); par(p, cam, 0.45)
    p.rect(-1600, GY - 240, 4400, 240, '#7e3b1c'); roof(p, 540, GY - 240, 4000, 40, 'BLK', 'LN2', False)
    for i in range(-1600, 2800, 80): p.line([(i, GY - 236), (i, GY)], '#6a3016', 2)
    # 庄门
    p.rect(380, GY - 420, 320, 420, '#3a1c10'); roof(p, 540, GY - 420, 380, 90, 'BLK')
    p.rect(450, GY - 340, 180, 340, '#5a2a16'); p.line([(540, GY - 340), (540, GY)], 'BLK', 3)
    p.rect(470, GY - 400, 140, 50, 'GOLD'); p.rect(476, GY - 394, 128, 38, 'BLK'); p.text('柴府', 540, GY - 362, 30, 'GOLD')
    lantern(p, g, 420, GY - 320, t); lantern(p, g, 660, GY - 320, t)
    # 竹
    for x in (-200, 150, 1000, 1300):
        for k in range(5):
            xx = x + k * 18; p.line([(xx, GY), (xx + 10 * math.sin(t + k), GY - 420)], '#24160e', 6)
            for j in range(4): p.poly([(xx, GY - 120 - j * 80), (xx + 40, GY - 140 - j * 80), (xx + 6, GY - 126 - j * 80)], '#24160e')
    rs(p)
    ground_band(p, 'BLK', GY, pattern='tiles')

def haystack(p, x, s=1.0, snow=True, burn=0.0):
    p.curve([(x - 110 * s, GY), (x - 100 * s, GY - 120 * s), (x - 40 * s, GY - 200 * s), (x + 40 * s, GY - 200 * s), (x + 100 * s, GY - 120 * s), (x + 110 * s, GY)], None, 1, close=True, fill='#2a1e14')
    for k in range(5): p.curve([(x - 90 * s + k * 40 * s, GY - 20 * s), (x - 70 * s + k * 34 * s, GY - 140 * s)], 'LN2', 1.5, 0.5)
    if snow and burn < 0.2: p.curve([(x - 80 * s, GY - 150 * s), (x - 30 * s, GY - 205 * s), (x + 30 * s, GY - 205 * s), (x + 80 * s, GY - 150 * s), (x, GY - 170 * s)], None, 1, close=True, fill='SNOW')

def small_temple(p, g, x, t, door=0.0, lit=True):
    y = GY
    p.rect(x - 150, y - 200, 300, 200, '#1e1610'); roof(p, x, y - 200, 300, 90, 'BLK')
    p.poly([(x - 170, y - 230), (x + 170, y - 230), (x + 120, y - 290), (x - 120, y - 290)], 'SNOW', a=0.9)
    p.rect(x - 60, y - 150, 120, 150, '#0e0a08')
    if lit and g is not None: g.rect(x - 56, y - 146, 112, 146, 'FIRE', a=0.25)
    # 门扇
    dw = 60 * (1 - door)
    p.rect(x - 60, y - 150, dw, 150, '#5a2a16'); p.rect(x + 60 - dw, y - 150, dw, 150, '#5a2a16')
    p.rect(x - 50, y - 240, 100, 34, 'GOLD'); p.text('山神庙', x, y - 214, 24, 'BLK')
    lantern(p, g, x - 110, y - 160, t, 0.7); 

def bg_snowfield(p, g, t, cam, fire_k=0.0):
    sv(p); par(p, cam, 0.1)
    sky(p, 'NIGHT', 'NIGHT2')
    p.ell(860, 170, 70, 70, 'SNOW', a=0.9); g.ell(860, 170, 90, 90, 'SNOW', a=0.15)
    if fire_k > 0: p.vgrad(-1600, 200, 4400, GY, '#00000000', '#f39a36') if False else p.rect(-1600, -600, 4400, 2000, 'FIRE', a=0.28 * fire_k)
    rs(p)
    sv(p); par(p, cam, 0.3)
    mountains(p, 51, 640, 160, 'NIGHT3', step=200, snowcap=True)
    rs(p)
    sv(p); par(p, cam, 0.6)
    mountains(p, 52, 780, 70, '#151b2c', step=140)
    for x in range(-800, 2600, 340): gnarled(p, x, GY, 360, 0.6, '#0f1320', seed=x, snow=True)
    rs(p)
    ground_band(p, '#0e1018', GY, pattern='snow')

def bg_lake(p, g, t, cam):
    sv(p); par(p, cam, 0.1)
    sky(p, 'NIGHT', 'NIGHT2'); p.ell(300, 180, 60, 60, 'SNOW', a=0.85)
    rs(p)
    sv(p); par(p, cam, 0.35)
    p.poly([(500, 760), (640, 520), (720, 580), (820, 400), (900, 480), (1000, 360), (1200, 560), (1400, 760)], '#10141f')
    p.rect(940, 300, 6, 80, 'BLK'); banner(p, 943, 380, t, '义', 90, 'RED', 0.5)
    for k in range(5): g.ell(800 + k * 60, 560 - k * 20, 5, 5, 'FIRE', a=0.8)
    rs(p)
    p.rect(-1600, 760, 4400, 400, 'TEAL')
    for i in range(14):
        x = -200 + i * 120 + (t * 25) % 120
        p.curve([(x, 800 + (i % 3) * 30), (x + 30, 794 + (i % 3) * 30), (x + 60, 800 + (i % 3) * 30)], 'SNOW', 2.5, 0.5)
    # 芦苇
    for x in range(-200, 1400, 40):
        h = 140 + (x * 7) % 90
        p.line([(x, GY + 40), (x + 14 * math.sin(t * 1.5 + x), GY + 40 - h)], 'BLK', 3)
        p.ell(x + 14 * math.sin(t * 1.5 + x), GY + 40 - h, 5, 16, 'BLK')
